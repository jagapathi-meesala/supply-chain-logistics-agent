from typing import Any, Dict, Protocol, List

class AgentContract(Protocol):
    def get_metadata(self) -> Dict[str, Any]:
        ...
        
    def list_tools(self) -> List[str]:
        ...
        
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        ...
