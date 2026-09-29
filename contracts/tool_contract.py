from typing import Any, Dict, Protocol

class ToolContract(Protocol):
    @property
    def name(self) -> str:
        ...
        
    @property
    def description(self) -> str:
        ...

    def get_input_schema(self) -> Dict[str, Any]:
        ...

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        ...
