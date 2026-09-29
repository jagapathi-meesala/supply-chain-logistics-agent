from typing import Dict, List, Any
from contracts.tool_contract import ToolContract

class DynamicToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        if not hasattr(tool, "name") or not tool.name:
            raise ValueError("Tool must have a valid name.")
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        if not hasattr(tool, "execute") or not callable(tool.execute):
            raise ValueError(f"Tool '{tool.name}' does not implement execute().")
        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> ToolContract:
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not found in registry.")
        return self._tools[tool_name]

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def execute(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.get(tool_name)
        try:
            return tool.execute(input_data)
        except Exception as e:
            return {"error": str(e), "tool": tool_name}
