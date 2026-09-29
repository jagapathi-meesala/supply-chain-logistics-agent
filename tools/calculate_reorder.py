from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CalculateReorderTool:
    @property
    def name(self) -> str:
        return "calculate-reorder"

    @property
    def description(self) -> str:
        return "Calculates if replenishment is needed and suggests quantity."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "current_stock": {"type": "number"},
                "reorder_level": {"type": "number"},
                "maximum_stock": {"type": "number"},
                "average_daily_demand": {"type": "number"},
                "lead_time_days": {"type": "number"}
            },
            "required": ["current_stock", "reorder_level", "maximum_stock", "average_daily_demand", "lead_time_days"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        current_stock = input_data.get("current_stock")
        reorder_level = input_data.get("reorder_level")
        max_stock = input_data.get("maximum_stock")
        demand = input_data.get("average_daily_demand")
        lead_time = input_data.get("lead_time_days")

        if any(not isinstance(x, (int, float)) for x in [current_stock, reorder_level, max_stock, demand, lead_time]):
            raise ValueError("All inputs must be numeric.")

        if current_stock < 0 or max_stock < 0 or demand < 0 or lead_time < 0:
            raise ValueError("Inputs cannot be negative.")
            
        if reorder_level > max_stock:
            raise ValueError("Reorder level cannot be greater than maximum stock.")

        required_stock = demand * lead_time
        target_stock = max_stock
        
        replenishment_needed = current_stock <= reorder_level
        suggested = max(0, target_stock - current_stock) if replenishment_needed else 0
        
        return {
            "formula": "suggested_reorder_quantity = max(0, target_stock - current_stock)",
            "inputs": input_data,
            "intermediate_values": {
                "required_stock": required_stock,
                "target_stock": target_stock
            },
            "replenishment_needed": replenishment_needed,
            "suggested_reorder_quantity": suggested,
            "assumptions": "Target stock equals maximum stock."
        }
