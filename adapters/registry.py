from typing import Dict
from contracts.adapter import AgentAdapter

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, AgentAdapter] = {}

    def register(self, name: str, adapter: AgentAdapter) -> None:
        self._adapters[name] = adapter

    def get(self, name: str) -> AgentAdapter:
        return self._adapters.get(name)
