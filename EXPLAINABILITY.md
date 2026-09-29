# Explainability

## Tools

### 1. analyze-inventory
- **Purpose**: Assess the health and value of inventory.
- **Input**: List of inventory dictionaries (item_id, current_stock, reorder_level, maximum_stock, unit_cost).
- **Calculations**: Sums up items, finds items where `current_stock <= reorder_level`, items where `current_stock > maximum_stock`, and healthy ones. Calculates `total_value` as `current_stock * unit_cost`.
- **Validation**: Rejects invalid numeric values or negative counts.

### 2. analyze-shipment
- **Purpose**: Interpret shipment tracking records.
- **Input**: Shipment metadata (shipment_id, expected_delivery, actual_delivery, status, priority).
- **Calculations**: Determines if a shipment is delayed by comparing `actual_delivery` (if completed) or current date (if pending) against `expected_delivery` (if provided).
- **Validation**: Expects valid status strings and properly formatted dates (ISO 8601).
- **Limitations**: No real-time data lookup.

### 3. analyze-supplier
- **Purpose**: Derive deterministic performance metrics for a supplier.
- **Input**: Supplier details and aggregate order stats (completed_orders, delayed_orders, defective_orders).
- **Calculations**: `completion_rate`, `delay_rate`, `defect_rate` based on division over total orders.
- **Validation**: Safe division by zero handling.

### 4. calculate-reorder
- **Purpose**: Calculate whether replenishment is needed and by how much.
- **Calculations**: 
  - `required_stock = average_daily_demand * lead_time_days`
  - Replenishment needed if `current_stock <= reorder_level`
  - `target_stock = maximum_stock`
  - `suggested_reorder_quantity = max(0, target_stock - current_stock)`
- **Validation**: Rejects `reorder_level > maximum_stock`, negative stocks, invalid demand.

### 5. detect-logistics-exceptions
- **Purpose**: Find structural inconsistencies in supply chain data.
- **Calculations**: Identifies missing origin/destination, delivery dates occurring before shipping dates, and missing required IDs.
- **Validation**: Based entirely on deterministic rule sets.

### 6. summarize-purchase-order
- **Purpose**: Synthesize overall PO information.
- **Calculations**: `total_order_value = sum(qty * price)`.
- **Validation**: Ensures lists for items, quantities, and prices match in length.

### 7. calculate-supply-chain-priority
- **Purpose**: Calculate a standardized priority score (0-100).
- **Formula**: `score = clamp( (demand_level * 20) + (shipment_delay_days * 10) + (supplier_delay_days * 5) - (current_stock / max(1, reorder_level) * 10), 0, 100 )` modified by item_criticality multipliers.
- **Thresholds**: 0-33 (Low), 34-66 (Medium), 67-100 (High).
- **Validation**: No ML used. Strictly deterministic.
