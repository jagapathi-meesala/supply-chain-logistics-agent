# Explainability

This document details the deterministic operations, trust boundaries, calculations, and execution flow of the Supply Chain & Logistics Agent to satisfy HiDevs Agent Passport / OpenGAP requirements.

## Complete Execution Flow
1. **Input**: The agent receives structured data (typically JSON).
2. **AgentCore**: The agent's core component initializes and exposes metadata without hardcoding domain logic.
3. **Tool Registry**: The `DynamicToolRegistry` discovers and stores registered tools.
4. **Tool Contract validation**: Input passes through a strict `ToolContract` validation to ensure schemas and data types match.
5. **Selected Tool**: The appropriate tool is identified and invoked based on the `tool_name` property.
6. **Deterministic processing**: The tool runs explicit, hardcoded mathematical and logical operations.
7. **Structured result**: The tool returns a predictable JSON dictionary of insights or throws a structured ValueError on failure.

## Data Provenance and Trust Boundaries
The agent maintains strict boundaries between data sources:
- **USER-SUPPLIED DATA**: Information explicitly provided in the tool's input payload (e.g., inventory lists, shipment records).
- **DERIVED DATA**: The deterministic conclusions calculated by the agent (e.g., low stock count, priority score, reorder amount).
- **CONFIGURATION**: Purely technical settings (e.g., log levels).
- **EXTERNAL DATA**: None. The agent does **NOT** connect to external carrier APIs, ERP systems, or live logistics tracking databases. It operates solely on user-supplied data.

## Tools

### 1. analyze-inventory
- **Purpose**: Assesses the health and total value of structured inventory data.
- **Input**: List of objects containing `item_id` (string), `current_stock` (number), `reorder_level` (number), `maximum_stock` (number), and `unit_cost` (number).
- **Validation**: Requires all fields to be numeric. Rejects negative values for stock, reorder levels, or cost. Rejects duplicate `item_id`s within the same list.
- **Processing logic**: Iterates over items, accumulating total value and classifying stock status.
- **Formula/rules**: 
  - `total_value = sum(current_stock * unit_cost)`
  - Low stock: `current_stock <= reorder_level`
  - Overstocked: `current_stock > maximum_stock`
  - Healthy stock: Any condition not meeting the above.
- **Output**: Returns counts, total value, and lists of `low_stock_items`, `overstocked_items`, and `healthy_stock_items`.
- **Error cases**: Missing required fields, invalid types, duplicate item IDs, negative values.
- **Assumptions**: Value is linearly dependent on unit cost.
- **Limitations**: No awareness of pending inbound shipments for inventory calculations.

### 2. analyze-shipment
- **Purpose**: Interprets shipment tracking records to determine status and calculate delays based strictly on supplied records.
- **Input**: `shipment_id` (string), `status` (string), and optionally `expected_delivery` (date string) and `actual_delivery` (date string).
- **Validation**: Requires `shipment_id` and `status`. Validates ISO 8601 formatting for date fields.
- **Processing logic**: Compares actual delivery date against expected delivery date to calculate delay.
- **Formula/rules**: 
  - `delay_days = (actual_delivery - expected_delivery).days` if `delay_days > 0`.
- **Output**: `shipment_status`, `delivery_state` ("Completed" or "Pending"), `delay_information`, and `structured_analysis`.
- **Error cases**: Missing IDs or status, malformed ISO 8601 dates.
- **Assumptions**: If `actual_delivery` is present, the shipment is "Completed".
- **Limitations**: Does NOT provide real-time shipment tracking. Analyzes supplied records only.

### 3. analyze-supplier
- **Purpose**: Derives deterministic performance metrics for a supplier based on historical aggregate numbers.
- **Input**: `supplier_id` (string), `orders` (number), `completed_orders` (number), `delayed_orders` (number), `defective_orders` (number), `average_delivery_days` (number).
- **Validation**: Rejects negative values. Handles division-by-zero safely by returning `0.0` for rates when `orders == 0`.
- **Processing logic**: Computes ratios of completion, delay, and defect over total orders.
- **Formula/rules**: 
  - `completion_rate = completed_orders / orders`
  - `delay_rate = delayed_orders / orders`
  - `defect_rate = defective_orders / orders`
- **Output**: Ratios and average delivery days.
- **Error cases**: Missing ID/orders, non-numeric values, negative order counts.
- **Assumptions**: Rates are based purely on total order volume provided by the user.
- **Limitations**: Does not evaluate subjective supplier quality (e.g., communication speed).

### 4. calculate-reorder
- **Purpose**: Calculates whether replenishment is needed and suggests exact quantities deterministically.
- **Input**: `current_stock`, `reorder_level`, `maximum_stock`, `average_daily_demand`, `lead_time_days` (all numbers).
- **Validation**: All inputs must be positive numbers. Rejects requests where `reorder_level > maximum_stock`.
- **Processing logic**: Determines if stock is at or below the reorder threshold, and computes the gap to maximum stock.
- **Formula/rules**: 
  - `required_stock = average_daily_demand * lead_time_days`
  - `replenishment_needed = current_stock <= reorder_level`
  - `target_stock = maximum_stock`
  - `suggested_reorder_quantity = max(0, target_stock - current_stock)` if `replenishment_needed` else `0`
- **Output**: Contains formulas used, boolean `replenishment_needed`, and `suggested_reorder_quantity`.
- **Error cases**: Negative values, illogical configurations (`reorder_level > maximum_stock`).
- **Assumptions**: Target stock is always equal to `maximum_stock`.
- **Limitations**: Does not account for batch sizes or minimum order quantities.

### 5. detect-logistics-exceptions
- **Purpose**: Finds structural anomalies in shipment records based on deterministic validation rules.
- **Input**: An array of `records` (objects).
- **Validation**: Verifies data structure (list of dictionaries).
- **Processing logic**: Scans each record against a hardcoded list of data anomalies.
- **Formula/rules**: 
  - `missing_status`: Triggered if "status" is omitted (Severity: high).
  - `missing_location`: Triggered if "origin" or "destination" is omitted (Severity: medium).
  - `unexpected_delivery`: Triggered if "actual_delivery" exists but "expected_delivery" is missing (Severity: low).
- **Output**: Array of exception objects detailing the type, severity, reason, and affected shipment.
- **Error cases**: Malformed root structures (e.g., non-list `records`).
- **Assumptions**: Every shipment must possess origin, destination, and status fields to be considered structurally sound.
- **Limitations**: Does not flag real-world logistics emergencies, only data inconsistencies.

### 6. summarize-purchase-order
- **Purpose**: Synthesizes PO information and calculates total valuation.
- **Input**: `purchase_order_id`, and parallel lists for `items`, `quantities`, and `unit_prices`.
- **Validation**: Rejects negative quantities or prices. Requires lists to be identical in length.
- **Processing logic**: Iterates through parallel arrays to compute total quantities and cost.
- **Formula/rules**: 
  - `total_item_quantity = sum(quantities)`
  - `total_order_value = sum(quantity * price)` for each matching item.
- **Output**: Returns calculated totals and basic PO details.
- **Error cases**: Mismatched array lengths, negative values, non-numeric prices/quantities.
- **Assumptions**: Parallel arrays correspond to the same index exactly.
- **Limitations**: Does not handle taxes, discounts, or shipping fees.

### 7. calculate-supply-chain-priority
- **Purpose**: Calculates a standardized, deterministic supply chain priority score. Note: This score is NOT an industry standard; it is a proprietary, hardcoded heuristic specific to this agent.
- **Input**: `stock_level`, `reorder_level`, `shipment_delay_days`, `demand_level`, `supplier_delay_days`, `item_criticality`.
- **Validation**: All inputs must be non-negative numeric values.
- **Processing logic**: Evaluates a weighted formula, applies a criticality multiplier, and clamps the result between 0 and 100.
- **Formula/rules**: 
  - `base_score = (demand_level * 20) + (shipment_delay_days * 10) + (supplier_delay_days * 5) - (stock_level / max(1, reorder_level) * 10)`
  - `score_with_criticality = base_score * max(1.0, item_criticality)`
  - `final_score = max(0.0, min(100.0, score_with_criticality))`
- **Thresholds**: 
  - Low: `0-33`
  - Medium: `34-66`
  - High: `67-100`
- **Output**: Outputs `calculated_score`, the threshold category, and the explanation of the calculation.
- **Error cases**: Negative inputs, non-numeric values.
- **Assumptions**: Negative modifiers (healthy stock) reduce urgency, while delays and high demand increase urgency.
- **Limitations**: Weights are static and cannot be adjusted via runtime arguments.

## Known Limitations
- The agent explicitly operates **offline and deterministically**. It does not perform active scraping, real-time API integrations, or real-world package location estimation.
- The agent does not use LLMs, Machine Learning, or AI to infer, guess, or hallucinate missing data. It relies solely on explicit rules applied to provided JSON data.
- The agent is entirely read-only; it does not issue purchase orders or mutate underlying databases.

## Security Boundaries & Portability
- **Security Boundaries**: The agent rejects dynamic code execution (`eval`/`exec`), subprocess imports, and shell scripts. It strictly requires validated JSON input.
- **Portability**: Code is framework-independent. The Core agent logic runs on pure Python. A `PortableAdapter` exists to connect the agent to specific frameworks (LangChain, CrewAI, AutoGen, etc.) without altering the underlying logic.
