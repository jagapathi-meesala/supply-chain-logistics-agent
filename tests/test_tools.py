import pytest
from tools.analyze_inventory import AnalyzeInventoryTool
from tools.analyze_shipment import AnalyzeShipmentTool
from tools.analyze_supplier import AnalyzeSupplierTool
from tools.calculate_reorder import CalculateReorderTool
from tools.detect_logistics_exceptions import DetectLogisticsExceptionsTool
from tools.summarize_purchase_order import SummarizePurchaseOrderTool
from tools.calculate_supply_chain_priority import CalculateSupplyChainPriorityTool

def test_inventory_analysis():
    tool = AnalyzeInventoryTool()
    data = {
        "inventory": [
            {"item_id": "A", "item_name": "N", "warehouse_id": "W", "current_stock": 2, "reorder_level": 5, "maximum_stock": 10, "unit_cost": 10.0}
        ]
    }
    res = tool.execute(data)
    assert res["total_items"] == 1
    assert "A" in res["low_stock_items"]
    assert res["total_inventory_value"] == 20.0

def test_inventory_invalid_input():
    tool = AnalyzeInventoryTool()
    with pytest.raises(ValueError):
        tool.execute({"inventory": [{"item_id": "A", "current_stock": -5, "reorder_level": 5, "maximum_stock": 10, "unit_cost": 10.0}]})

def test_shipment_analysis():
    tool = AnalyzeShipmentTool()
    data = {
        "shipment_id": "S1",
        "status": "Delivered",
        "expected_delivery": "2023-01-01",
        "actual_delivery": "2023-01-05"
    }
    res = tool.execute(data)
    assert res["delay_information"]["is_delayed"] == True
    assert res["delay_information"]["delay_days"] == 4

def test_supplier_analysis():
    tool = AnalyzeSupplierTool()
    res = tool.execute({"supplier_id": "S1", "orders": 100, "completed_orders": 90, "delayed_orders": 5, "defective_orders": 2})
    assert res["completion_rate"] == 0.9
    assert res["delay_rate"] == 0.05

def test_calculate_reorder():
    tool = CalculateReorderTool()
    data = {
        "current_stock": 10,
        "reorder_level": 15,
        "maximum_stock": 100,
        "average_daily_demand": 5,
        "lead_time_days": 2
    }
    res = tool.execute(data)
    assert res["replenishment_needed"] == True
    assert res["suggested_reorder_quantity"] == 90

def test_detect_exceptions():
    tool = DetectLogisticsExceptionsTool()
    data = {
        "records": [
            {"shipment_id": "S1"} # missing status and locations
        ]
    }
    res = tool.execute(data)
    assert res["exceptions_found"] == 2
    types = [e["type"] for e in res["exceptions"]]
    assert "missing_status" in types
    assert "missing_location" in types

def test_summarize_po():
    tool = SummarizePurchaseOrderTool()
    res = tool.execute({
        "purchase_order_id": "PO1",
        "items": ["A", "B"],
        "quantities": [2, 3],
        "unit_prices": [10.0, 5.0]
    })
    assert res["total_item_quantity"] == 5
    assert res["total_order_value"] == 35.0

def test_calculate_priority():
    tool = CalculateSupplyChainPriorityTool()
    res = tool.execute({
        "stock_level": 5,
        "reorder_level": 10,
        "shipment_delay_days": 2,
        "demand_level": 5,
        "supplier_delay_days": 1,
        "item_criticality": 1.5
    })
    # base = (5*20) + (2*10) + (1*5) - (5/10*10) = 100 + 20 + 5 - 5 = 120
    # with crit = 120 * 1.5 = 180 -> clamped to 100
    assert res["calculated_score"] == 100.0
    assert res["priority_category"] == "High"
