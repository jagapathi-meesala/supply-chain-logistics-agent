import pytest
from core.agent import AgentCore
from tools.analyze_inventory import AnalyzeInventoryTool

def test_agent_initialization():
    agent = AgentCore("test-agent", "1.0.0")
    assert agent.get_metadata()["name"] == "test-agent"
    assert agent.get_metadata()["version"] == "1.0.0"

def test_agent_register_and_list_tools():
    agent = AgentCore("test-agent", "1.0.0")
    tool = AnalyzeInventoryTool()
    agent.register_tool(tool)
    assert "analyze-inventory" in agent.list_tools()

def test_agent_execute_tool():
    agent = AgentCore("test-agent", "1.0.0")
    agent.register_tool(AnalyzeInventoryTool())
    
    input_data = {
        "inventory": [
            {
                "item_id": "item1",
                "item_name": "Test Item",
                "warehouse_id": "W1",
                "current_stock": 10,
                "reorder_level": 5,
                "maximum_stock": 100,
                "unit_cost": 2.5
            }
        ]
    }
    
    result = agent.execute_tool("analyze-inventory", input_data)
    assert "error" not in result
    assert result["total_items"] == 1
    assert result["total_inventory_value"] == 25.0
