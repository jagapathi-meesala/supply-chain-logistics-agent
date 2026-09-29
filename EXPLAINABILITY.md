# Explainability

This document details the deterministic operations, trust boundaries, calculations, and execution flow of the Supply Chain & Logistics Agent.

*(Note: The exact official HiDevs Checkpoint 2 specification does not exist locally within this repository. This documentation is structured to satisfy the explicit explainability requirements provided.)*

## A. Agent Purpose
- **What the agent does**: The agent deterministically analyzes supply chain and logistics records (inventory, shipments, purchase orders, suppliers) to calculate priority scores, suggest reorder quantities, and detect anomalies.
- **What problem it solves**: It converts raw, structured supply chain data into structured insights (metrics, thresholds, delays, exceptions) using predictable, static rules.
- **What it does NOT do**: It does NOT track real-world physical shipments, place live orders, communicate with external carriers, or make autonomous adjustments to real-world logistics systems.

## B. Input Contract
- **Accepted input structure**: The agent accepts JSON objects representing specific supply chain entities (e.g., inventory lists, shipment details).
- **Required fields**: Vary by tool (e.g., `calculate-reorder` requires `current_stock`, `reorder_level`, `maximum_stock`, `average_daily_demand`, `lead_time_days`).
- **Types**: Heavily enforces explicit types (strings for IDs/statuses, numbers for stock/delays, ISO 8601 strings for dates).
- **Validation rules**: Numbers cannot be negative. Dates must be parseable. Required fields must be present. Parallel arrays must be identical in length.
- **Invalid-input behavior**: The agent immediately halts and throws a deterministic `ValueError` describing exactly which field or type failed validation.

## C. Output Contract
- **Output structure**: A structured JSON dictionary containing calculated values, categorizations, and boolean flags.
- **Meaning of every important output**: Each tool returns mathematically derived facts (e.g., `calculated_score` in priority, `suggested_reorder_quantity` in reorders) and human-readable summaries (`priority_category`, `delivery_state`).
- **Deterministic error behavior**: If an error occurs during execution (e.g., division by zero handled safely, or negative inputs), execution fails with a precise string message rather than producing a hallucinated or partial output.

## D. Complete Execution Lifecycle
1. **Input**: A JSON payload is received.
2. **AgentCore**: The core orchestrator receives the tool execution request.
3. **Tool selection**: The request specifies the target tool (e.g., `analyze-inventory`).
4. **Registry**: The `DynamicToolRegistry` looks up the tool by name.
5. **Contract validation**: The payload is validated against the tool's `get_input_schema()`.
6. **Tool execution**: The tool's `execute()` method runs hardcoded deterministic logic.
7. **Result**: The tool returns a structured dictionary of derived facts.
8. **Error handling**: Any validation or logic failure raises a `ValueError`, failing the execution cleanly.

## E. Decision/Rule Transparency (Tool-by-Tool) & N. Tool-by-Tool Examples

### 1. analyze-inventory
- **Decision**: Determines if stock is low, healthy, or overstocked, and calculates total inventory value.
- **Inputs influencing decision**: `current_stock`, `reorder_level`, `maximum_stock`, `unit_cost`.
- **Exact rule/formula**:
  - Low stock: `current_stock <= reorder_level`
  - Overstocked: `current_stock > maximum_stock`
  - Value: `sum(current_stock * unit_cost)`
- **Thresholds**: Evaluated strictly based on the provided reorder and maximum levels.
- **Boundary conditions**: A stock exactly equal to `reorder_level` is considered "low stock".
- **Missing/invalid values**: Raises `ValueError` for negative values or missing fields.
- **Concrete Example**:
  - *Input*: `{"inventory": [{"item_id": "A1", "current_stock": 5, "reorder_level": 10, "maximum_stock": 50, "unit_cost": 2.0}]}`
  - *Output*: `{"total_inventory_value": 10.0, "low_stock_items": ["A1"], "overstocked_items": [], ...}`

### 2. analyze-shipment
- **Decision**: Determines shipment completion state and calculates delivery delay.
- **Inputs influencing decision**: `expected_delivery`, `actual_delivery`.
- **Exact rule/formula**: `delay_days = (actual_delivery - expected_delivery).days` (only if > 0).
- **Boundary conditions**: Delivery on the exact expected day is 0 delay.
- **Missing/invalid values**: If dates are not ISO 8601, raises `ValueError`.
- **Concrete Example**:
  - *Input*: `{"shipment_id": "S1", "status": "Delivered", "expected_delivery": "2023-01-01", "actual_delivery": "2023-01-03"}`
  - *Output*: `{"delivery_state": "Completed", "delay_information": {"is_delayed": true, "delay_days": 2}, ...}`

### 3. analyze-supplier
- **Decision**: Computes objective supplier performance ratios.
- **Inputs influencing decision**: `completed_orders`, `delayed_orders`, `defective_orders`, `orders`.
- **Exact rule/formula**: `rate = metric / orders`.
- **Boundary conditions**: If `orders == 0`, all rates safely return `0.0`.
- **Missing/invalid values**: Rejects negative order counts.
- **Concrete Example**:
  - *Input*: `{"supplier_id": "V1", "orders": 100, "delayed_orders": 5}`
  - *Output*: `{"delay_rate": 0.05, ...}`

### 4. calculate-reorder
- **Decision**: Decides if an item needs replenishment and computes the exact quantity.
- **Inputs influencing decision**: `current_stock`, `reorder_level`, `maximum_stock`.
- **Exact rule/formula**: `suggested_reorder_quantity = max(0, maximum_stock - current_stock)` if `current_stock <= reorder_level`, else `0`.
- **Thresholds**: Triggers when `current_stock <= reorder_level`.
- **Boundary conditions**: If `current_stock` is 0, suggests full `maximum_stock`.
- **Missing/invalid values**: If `reorder_level > maximum_stock`, raises an error as illogical.
- **Concrete Example**:
  - *Input*: `{"current_stock": 10, "reorder_level": 20, "maximum_stock": 100, ...}`
  - *Output*: `{"replenishment_needed": true, "suggested_reorder_quantity": 90}`

### 5. detect-logistics-exceptions
- **Decision**: Identifies missing or illogical fields in shipment records.
- **Inputs influencing decision**: `status`, `origin`, `destination`, `actual_delivery`, `expected_delivery`.
- **Exact rule/formula**: Flags missing status (high severity), missing origin/destination (medium), actual delivery without expected delivery (low).
- **Missing/invalid values**: This tool specifically hunts for missing fields, outputting an array of anomalies.
- **Concrete Example**:
  - *Input*: `{"records": [{"shipment_id": "S1"}]}`
  - *Output*: `{"exceptions": [{"type": "missing_status", "affected_shipment": "S1", "severity": "high", ...}, {"type": "missing_location", ...}]}`

### 6. summarize-purchase-order
- **Decision**: Aggregates quantities and calculates total PO financial value.
- **Inputs influencing decision**: `items`, `quantities`, `unit_prices` (arrays).
- **Exact rule/formula**: `total_order_value = sum(quantities[i] * unit_prices[i])`.
- **Boundary conditions**: Empty arrays return 0 totals.
- **Missing/invalid values**: If array lengths do not match, raises `ValueError`.
- **Concrete Example**:
  - *Input*: `{"purchase_order_id": "PO1", "items": ["A"], "quantities": [5], "unit_prices": [10.0]}`
  - *Output*: `{"total_item_quantity": 5, "total_order_value": 50.0}`

### 7. calculate-supply-chain-priority
- **Decision**: Assigns a deterministic priority score and Low/Medium/High category.
- **Inputs influencing decision**: `demand_level`, `shipment_delay_days`, `supplier_delay_days`, `stock_level`, `reorder_level`, `item_criticality`.
- **Exact rule/formula**: `score = clamp(((demand*20) + (shipment_delay*10) + (supplier_delay*5) - (stock/max(1,reorder)*10)) * max(1, criticality), 0, 100)`.
- **Thresholds**: 0-33 = Low, 34-66 = Medium, 67-100 = High.
- **Boundary conditions**: Result is rigidly clamped between 0 and 100.
- **Missing/invalid values**: Rejects negative multipliers or missing fields.
- **Concrete Example**:
  - *Input*: `{"stock_level": 50, "reorder_level": 10, "demand_level": 2, "shipment_delay_days": 1, "supplier_delay_days": 0, "item_criticality": 1.0}`
  - *Output*: `{"calculated_score": 0.0, "priority_category": "Low"}` (Formula drops base below 0, clamped to 0).

## F. Explainability of Calculated Results
Every calculated value in the agent is traceable directly back to a static formula.
- **Source inputs**: Mapped directly from the JSON payload.
- **Transformation**: Pure arithmetic (+, -, *, /) or logical thresholds (<=, >). No fuzzy logic is used.
- **Formula**: Fully exposed in the documentation (see Section E) and sometimes embedded in the tool's JSON output (e.g., `calculate_supply_chain_priority`).
- **Final interpretation**: The results are categorized using hardcoded boundaries (e.g., Low/Medium/High) explicitly designed by the developer, not learned by a model.

## G. Provenance
Data handled by this agent is strictly categorized:
- **User-supplied data**: 100% of the input data processed by the agent (e.g., shipment IDs, quantities) originates directly from the caller's JSON payload.
- **Configuration**: Technical environment settings (if any).
- **Derived/calculated data**: Aggregations, priority scores, and delay days produced by the agent's logic.
- **External data**: NONE. The agent does NOT make API calls to external databases, carrier networks, or ERPs.

## H. Determinism
- **Same valid input → same output**: Given the exact same JSON payload, the agent will execute the same code path and yield the exact same output bytes every single time.
- **No randomness**: `random` or stochastic libraries are not used.
- **No LLM / ML inference**: The agent's logic does not rely on Large Language Models, embeddings, or neural networks.
- **No hidden external state**: The agent is entirely stateless between invocations.
- **No live API dependency**: The agent executes purely offline.

## I. Traceability
An evaluator can easily trace the system logic:
1. Identify the input JSON.
2. Read the corresponding tool's `get_input_schema()` for validation requirements.
3. Trace the values into the respective Python `execute()` method.
4. Compare the arithmetic directly to the Python source code (e.g., `calculate_reorder.py`).
5. Verify the mathematical output matches the JSON response exactly.

## J. Error/Edge Cases
- **Malformed data**: Missing JSON keys or incorrect types (e.g., strings instead of numbers) immediately throw validation errors.
- **Zero values**: Safely handled. For example, `analyze_supplier.py` detects `orders == 0` and returns `0.0` for all rates to prevent `ZeroDivisionError`.
- **Negative boundaries**: `calculate_reorder.py` rejects negative stock.
- **Invalid dates**: `analyze_shipment.py` attempts to parse ISO 8601 and raises a `ValueError` if the format is corrupted.
- **Mismatched arrays**: `summarize-purchase-order` explicitly asserts `len(items) == len(quantities) == len(unit_prices)` before proceeding.
- **Duplicate IDs**: `analyze_inventory.py` uses a `seen_ids` set and halts if a duplicate `item_id` is passed.

## K. Limitations
- The system cannot know if a shipment is physically delayed in the real world; it only knows what the JSON payload states as `actual_delivery` vs `expected_delivery`.
- The system cannot adjust thresholds dynamically based on seasonality or market trends.
- The system cannot automatically fetch missing data from external databases.

## L. Security Boundaries
- The agent explicitly rejects dynamic code evaluation. There are no `eval()` or `exec()` statements.
- The agent has no access to the host shell (`subprocess` is prohibited).
- Inputs are restricted mathematically and type-wise. Malicious input strings simply fail type validation or date parsing before they can be processed.

## M. Human/System Boundary
The agent analyzes supplied data passively. It **does not autonomously make real-world changes**. It will calculate that an item should be reordered, but it relies on a human operator or external system to actually place the purchase order.
