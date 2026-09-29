from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzeInventoryTool:
    @property
    def name(self) -> str:
        return "analyze-inventory"

    @property
    def description(self) -> str:
        return "Analyzes structured inventory data for stock health and value."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "inventory": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item_id": {"type": "string"},
                            "item_name": {"type": "string"},
                            "warehouse_id": {"type": "string"},
                            "current_stock": {"type": "number"},
                            "reorder_level": {"type": "number"},
                            "maximum_stock": {"type": "number"},
                            "unit_cost": {"type": "number"}
                        },
                        "required": ["item_id", "current_stock", "reorder_level", "maximum_stock", "unit_cost"]
                    }
                }
            },
            "required": ["inventory"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        inventory = input_data.get("inventory")
        if inventory is None or not isinstance(inventory, list):
            raise ValueError("Input must contain 'inventory' as a list.")

        total_items = len(inventory)
        low_stock = []
        overstocked = []
        healthy_stock = []
        total_value = 0.0

        seen_ids = set()

        for item in inventory:
            item_id = item.get("item_id")
            
            if not isinstance(item_id, str):
                raise ValueError("Missing or invalid item_id in inventory item.")
                
            if item_id in seen_ids:
                raise ValueError(f"Duplicate item_id found: {item_id}")
            seen_ids.add(item_id)

            current_stock = item.get("current_stock")
            reorder_level = item.get("reorder_level")
            max_stock = item.get("maximum_stock")
            unit_cost = item.get("unit_cost")

            if not all(isinstance(x, (int, float)) for x in [current_stock, reorder_level, max_stock, unit_cost]):
                raise ValueError(f"Invalid numeric values for item: {item_id}")
                
            if any(x < 0 for x in [current_stock, reorder_level, max_stock, unit_cost]):
                raise ValueError(f"Negative values not allowed for item: {item_id}")

            total_value += current_stock * unit_cost

            if current_stock <= reorder_level:
                low_stock.append(item_id)
            elif current_stock > max_stock:
                overstocked.append(item_id)
            else:
                healthy_stock.append(item_id)

        return {
            "total_items": total_items,
            "low_stock_items": low_stock,
            "overstocked_items": overstocked,
            "healthy_stock_items": healthy_stock,
            "total_inventory_value": total_value,
            "structured_findings": {
                "low_stock_count": len(low_stock),
                "overstocked_count": len(overstocked),
                "healthy_count": len(healthy_stock)
            }
        }
