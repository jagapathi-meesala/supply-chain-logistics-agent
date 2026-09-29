from typing import Any, Dict, Optional
from contracts.agent_contract import AgentContract
from contracts.adapter import AgentAdapter

class PortableAdapter(AgentAdapter):
    def __init__(self):
        self._agent: Optional[AgentContract] = None

    def attach(self, agent: AgentContract) -> None:
        self._agent = agent

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if not self._agent:
            return {"error": "No agent attached"}
        
        action = request.get("action")
        if action == "metadata":
            return {"status": "success", "data": self._agent.get_metadata()}
        elif action == "execute":
            tool_name = request.get("tool")
            input_data = request.get("input_data", {})
            if not tool_name:
                return {"error": "Missing tool name in execute action"}
            result = self._agent.execute_tool(tool_name, input_data)
            if "error" in result:
                return {"status": "error", "error": result["error"]}
            return {"status": "success", "data": result}
        else:
            return {"error": f"Unknown action: {action}"}
