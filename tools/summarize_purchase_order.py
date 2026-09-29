from typing import Any, Dict
from contracts.tool_contract import ToolContract

class SummarizePurchaseOrderTool:
    @property
    def name(self) -> str:
        return "summarize-purchase-order"

    @property
    def description(self) -> str:
        return "Synthesizes overall PO information deterministically."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "purchase_order_id": {"type": "string"},
                "supplier": {"type": "string"},
                "items": {"type": "array"},
                "quantities": {"type": "array"},
                "unit_prices": {"type": "array"},
                "status": {"type": "string"}
            },
            "required": ["purchase_order_id", "items", "quantities", "unit_prices"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        po_id = input_data.get("purchase_order_id")
        items = input_data.get("items")
        quantities = input_data.get("quantities")
        prices = input_data.get("unit_prices")
        
        if not po_id or not isinstance(po_id, str):
            raise ValueError("Invalid purchase_order_id.")
            
        if not (isinstance(items, list) and isinstance(quantities, list) and isinstance(prices, list)):
            raise ValueError("items, quantities, and unit_prices must be lists.")
            
        if not (len(items) == len(quantities) == len(prices)):
            raise ValueError("Mismatched lengths for items, quantities, and prices.")
            
        total_qty = 0
        total_val = 0.0
        
        for q, p in zip(quantities, prices):
            if not isinstance(q, (int, float)) or not isinstance(p, (int, float)):
                raise ValueError("Quantities and prices must be numeric.")
            if q < 0 or p < 0:
                raise ValueError("Quantities and prices cannot be negative.")
            total_qty += q
            total_val += q * p
            
        return {
            "total_item_quantity": total_qty,
            "total_order_value": total_val,
            "supplier": input_data.get("supplier", "Unknown"),
            "order_status": input_data.get("status", "Unknown"),
            "expected_delivery": input_data.get("expected_date", "Unknown"),
            "item_summary": f"PO {po_id} has {len(items)} items.",
            "detected_inconsistencies": []
        }
