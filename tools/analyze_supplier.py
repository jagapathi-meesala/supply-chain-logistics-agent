from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzeSupplierTool:
    @property
    def name(self) -> str:
        return "analyze-supplier"

    @property
    def description(self) -> str:
        return "Analyzes supplier performance deterministically."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "supplier_id": {"type": "string"},
                "supplier_name": {"type": "string"},
                "orders": {"type": "number"},
                "completed_orders": {"type": "number"},
                "delayed_orders": {"type": "number"},
                "defective_orders": {"type": "number"},
                "average_delivery_days": {"type": "number"}
            },
            "required": ["supplier_id", "orders"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        supplier_id = input_data.get("supplier_id")
        orders = input_data.get("orders")
        
        if not supplier_id or not isinstance(supplier_id, str):
            raise ValueError("Invalid supplier_id.")
        if not isinstance(orders, (int, float)) or orders < 0:
            raise ValueError("Invalid orders count.")
            
        completed = input_data.get("completed_orders", 0)
        delayed = input_data.get("delayed_orders", 0)
        defective = input_data.get("defective_orders", 0)
        avg_delivery = input_data.get("average_delivery_days", 0)
        
        if any(not isinstance(x, (int, float)) or x < 0 for x in [completed, delayed, defective, avg_delivery]):
            raise ValueError("Invalid numeric values for supplier metrics.")

        if orders == 0:
            return {
                "completion_rate": 0.0,
                "delay_rate": 0.0,
                "defect_rate": 0.0,
                "average_delivery_days": avg_delivery,
                "structured_findings": "No orders to analyze."
            }
            
        return {
            "completion_rate": completed / orders,
            "delay_rate": delayed / orders,
            "defect_rate": defective / orders,
            "average_delivery_days": avg_delivery,
            "structured_findings": "Supplier analysis completed deterministically."
        }
