# Agents Architecture
- **Agent Core (`AgentCore`)**: Initializes the agent, manages tool registration and invocation. Framework-independent.
- **Dynamic Tool Registry (`DynamicToolRegistry`)**: Dynamically registers, validates, and discovers tools.
- **Contracts (`ToolContract`)**: Defines input schemas, determinism, and safety checks for tools.
- **Tools**: Seven implemented tools covering inventory, shipments, suppliers, reorder calculations, exceptions, PO summaries, and priority.
- **Adapters (`PortableAdapter`)**: Provides a boundary to translate between the core agent and external frameworks. Currently includes a basic interface for framework portability.
- **Verification**: `readiness_audit.py` checks file, documentation, and contract hygiene.
- **Portability**: This project does not hardcode frameworks such as LangChain, CrewAI, AutoGen, OpenAI SDK, etc. It can be integrated into them via Adapters.
