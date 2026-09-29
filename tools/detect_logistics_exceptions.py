from typing import Any, Dict
from contracts.tool_contract import ToolContract

class DetectLogisticsExceptionsTool:
    @property
    def name(self) -> str:
        return "detect-logistics-exceptions"

    @property
    def description(self) -> str:
        return "Detects structural anomalies in shipment records."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "records": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                }
            },
            "required": ["records"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        records = input_data.get("records")
        if not isinstance(records, list):
            raise ValueError("Records must be a list.")
            
        exceptions = []
        for i, rec in enumerate(records):
            if not isinstance(rec, dict):
                exceptions.append({"type": "format_error", "affected_shipment": f"index_{i}", "reason": "Record is not a dictionary.", "severity": "high", "deterministic_rule_used": "type_check"})
                continue
                
            shipment_id = rec.get("shipment_id", f"index_{i}")
            
            if "status" not in rec:
                exceptions.append({"type": "missing_status", "affected_shipment": shipment_id, "reason": "Missing status field.", "severity": "high", "deterministic_rule_used": "missing_required_field"})
            
            if "origin" not in rec or "destination" not in rec:
                exceptions.append({"type": "missing_location", "affected_shipment": shipment_id, "reason": "Missing origin or destination.", "severity": "medium", "deterministic_rule_used": "location_completeness"})
                
            # Date inconsistency check if dates exist
            exp = rec.get("expected_delivery")
            act = rec.get("actual_delivery")
            if act and not exp:
                exceptions.append({"type": "unexpected_delivery", "affected_shipment": shipment_id, "reason": "Actual delivery exists without expected delivery.", "severity": "low", "deterministic_rule_used": "date_consistency"})

        return {
            "exceptions_found": len(exceptions),
            "exceptions": exceptions
        }
