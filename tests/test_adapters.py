from adapters.portable_adapter import PortableAdapter
from core.agent import AgentCore
from tools.analyze_inventory import AnalyzeInventoryTool

def test_portable_adapter_metadata():
    agent = AgentCore("test", "1.0")
    adapter = PortableAdapter()
    adapter.attach(agent)
    
    res = adapter.handle_request({"action": "metadata"})
    assert res["status"] == "success"
    assert res["data"]["name"] == "test"

def test_portable_adapter_execute():
    agent = AgentCore("test", "1.0")
    agent.register_tool(AnalyzeInventoryTool())
    adapter = PortableAdapter()
    adapter.attach(agent)
    
    res = adapter.handle_request({
        "action": "execute",
        "tool": "analyze-inventory",
        "input_data": {
            "inventory": []
        }
    })
    
    assert res["status"] == "success"
    assert res["data"]["total_items"] == 0
