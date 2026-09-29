from typing import Any, Dict
from datetime import datetime
from contracts.tool_contract import ToolContract

class AnalyzeShipmentTool:
    @property
    def name(self) -> str:
        return "analyze-shipment"

    @property
    def description(self) -> str:
        return "Analyzes shipment data to determine status and delays."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "shipment_id": {"type": "string"},
                "origin": {"type": "string"},
                "destination": {"type": "string"},
                "status": {"type": "string"},
                "expected_delivery": {"type": "string", "format": "date"},
                "actual_delivery": {"type": "string", "format": "date"},
                "priority": {"type": "string"}
            },
            "required": ["shipment_id", "status"]
        }

    def _parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {date_str}. Expected ISO 8601.")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        shipment_id = input_data.get("shipment_id")
        if not isinstance(shipment_id, str) or not shipment_id.strip():
            raise ValueError("Missing or invalid shipment_id.")
            
        status = input_data.get("status")
        if not isinstance(status, str):
            raise ValueError("Missing or invalid status.")
            
        expected_delivery = input_data.get("expected_delivery")
        actual_delivery = input_data.get("actual_delivery")
        
        delay_days = 0
        is_delayed = False
        
        if expected_delivery and actual_delivery:
            exp_date = self._parse_date(expected_delivery)
            act_date = self._parse_date(actual_delivery)
            diff = act_date - exp_date
            if diff.days > 0:
                is_delayed = True
                delay_days = diff.days
                
        return {
            "shipment_status": status,
            "delivery_state": "Completed" if actual_delivery else "Pending",
            "delay_information": {
                "is_delayed": is_delayed,
                "delay_days": delay_days
            },
            "priority": input_data.get("priority", "Unknown"),
            "structured_analysis": f"Shipment {shipment_id} is {status}."
        }
