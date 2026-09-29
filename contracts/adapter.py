from typing import Any, Dict, Protocol
from contracts.agent_contract import AgentContract

class AgentAdapter(Protocol):
    def attach(self, agent: AgentContract) -> None:
        ...

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        ...
