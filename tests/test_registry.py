import pytest
from core.registry import DynamicToolRegistry
from tools.analyze_inventory import AnalyzeInventoryTool

class DummyTool:
    @property
    def name(self): return "dummy"
    def get_input_schema(self): return {}
    def execute(self, data): return data

def test_registry_registration():
    registry = DynamicToolRegistry()
    tool = AnalyzeInventoryTool()
    registry.register(tool)
    assert tool.name in registry.list_tools()
    
def test_duplicate_registration_fails():
    registry = DynamicToolRegistry()
    tool = AnalyzeInventoryTool()
    registry.register(tool)
    with pytest.raises(ValueError):
        registry.register(tool)

def test_missing_tool_fails():
    registry = DynamicToolRegistry()
    with pytest.raises(ValueError):
        registry.get("nonexistent")

def test_tool_contract_validation():
    registry = DynamicToolRegistry()
    class BadTool:
        pass
    with pytest.raises(ValueError):
        registry.register(BadTool())
