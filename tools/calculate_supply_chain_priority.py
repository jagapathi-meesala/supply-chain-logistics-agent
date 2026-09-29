from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CalculateSupplyChainPriorityTool:
    @property
    def name(self) -> str:
        return "calculate-supply-chain-priority"

    @property
    def description(self) -> str:
        return "Calculates a deterministic supply chain priority score."

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "stock_level": {"type": "number"},
                "reorder_level": {"type": "number"},
                "shipment_delay_days": {"type": "number"},
                "demand_level": {"type": "number"},
                "supplier_delay_days": {"type": "number"},
                "item_criticality": {"type": "number"}
            },
            "required": ["stock_level", "reorder_level", "shipment_delay_days", "demand_level", "supplier_delay_days", "item_criticality"]
        }

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        stock = input_data.get("stock_level")
        reorder = input_data.get("reorder_level")
        shipment_delay = input_data.get("shipment_delay_days")
        demand = input_data.get("demand_level")
        supplier_delay = input_data.get("supplier_delay_days")
        criticality = input_data.get("item_criticality")
        
        inputs = [stock, reorder, shipment_delay, demand, supplier_delay, criticality]
        
        if any(not isinstance(x, (int, float)) for x in inputs):
            raise ValueError("All priority factors must be numeric.")
            
        if any(x < 0 for x in inputs):
            raise ValueError("Priority factors cannot be negative.")
            
        # Formula: score = clamp( (demand * 20) + (shipment_delay * 10) + (supplier_delay * 5) - (stock / max(1, reorder) * 10), 0, 100 )
        base_score = (demand * 20) + (shipment_delay * 10) + (supplier_delay * 5) - (stock / max(1.0, float(reorder)) * 10)
        
        # Apply criticality multiplier
        score_with_criticality = base_score * max(1.0, float(criticality))
        
        # Clamp to 0-100
        final_score = max(0.0, min(100.0, score_with_criticality))
        
        if final_score < 34:
            category = "Low"
        elif final_score < 67:
            category = "Medium"
        else:
            category = "High"

        return {
            "calculated_score": final_score,
            "contributing_factors": input_data,
            "calculation_explanation": "score = clamp(((demand*20) + (ship_delay*10) + (sup_delay*5) - (stock/max(1,reorder)*10)) * max(1, criticality), 0, 100)",
            "priority_category": category,
            "thresholds": {
                "Low": "0-33",
                "Medium": "34-66",
                "High": "67-100"
            }
        }
