from typing import Any, Dict, List
from core.registry import DynamicToolRegistry
from contracts.tool_contract import ToolContract

class AgentCore:
    def __init__(self, name: str, version: str):
        self._name = name
        self._version = version
        self.registry = DynamicToolRegistry()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self._name,
            "version": self._version,
            "tools": self.list_tools()
        }

    def register_tool(self, tool: ToolContract) -> None:
        self.registry.register(tool)

    def list_tools(self) -> List[str]:
        return self.registry.list_tools()

    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.registry.execute(tool_name, input_data)
