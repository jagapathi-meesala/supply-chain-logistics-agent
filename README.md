# Supply Chain & Logistics Agent

## 1. Overview
A completely deterministic, framework-independent Supply Chain & Logistics Agent for the OpenGAP ecosystem.

## 2. Features
- Analyzes inventory for reorder and overstock conditions.
- Evaluates shipment tracking and supplier performance.
- Calculates deterministic supply chain priority scores.
- Detects logistical inconsistencies.
- Framework-agnostic design with an adapter layer.

## 3. Architecture
The agent is divided into `core`, `contracts`, `adapters`, and `tools`. It strictly separates the business logic from framework bindings, making it portable across LangChain, CrewAI, AutoGen, and native OpenGAP runtimes.

## 4. Tools
- `analyze-inventory`
- `analyze-shipment`
- `analyze-supplier`
- `calculate-reorder`
- `detect-logistics-exceptions`
- `summarize-purchase-order`
- `calculate-supply-chain-priority`

## 5. Input/Output Examples
**Input to analyze-inventory:**
```json
{
  "inventory": [
    {"item_id": "1", "current_stock": 5, "reorder_level": 10, "maximum_stock": 50, "unit_cost": 20.0}
  ]
}
```

**Output:**
```json
{
  "total_items": 1,
  "low_stock_items": ["1"],
  "total_inventory_value": 100.0,
  ...
}
```

## 6. Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 7. Configuration
Use the `.env.example` file to create a `.env` file if necessary. The agent requires no external API keys as it operates entirely deterministically on provided inputs.

## 8. Running tests
```bash
pytest -q
```

## 9. Local validation
Run the internal readiness audit:
```bash
python verification/readiness_audit.py
```

## 10. Official OpenGAP validation
```bash
opengap validate
```
(If `opengap` CLI is installed).

## 11. Security
The agent explicitly refuses `eval()` and `exec()`. It imports no subprocess tools. All JSON parsing and schemas are explicitly validated. No real-world mutations occur.

## 12. Portability
Designed with a strict contract (`AgentContract`, `ToolContract`, `AgentAdapter`). It can be moved to any framework without altering `core/` or `tools/`.

## 13. OpenGAP compliance
Adheres to the OpenGAP 0.1.0 specification (https://github.com/open-gitagent/opengap).

## 14. Limitations
- Does NOT possess live logistics tracking data.
- Does NOT execute transactions or reorder products automatically.
- Relies solely on user-provided inputs.

## 15. Project structure
See the directory tree.

## 16. Extension guide
To add a new tool, create a class implementing `ToolContract` in the `tools/` directory, register it in `agent.yaml`, and add it to your agent instance using `register_tool()`.

## 17. Verification status
- Local tests: PASSED
- Local schema validation: PASSED (against official agent-yaml.schema.json)
- Official OpenGAP CLI validation: NOT VERIFIED (CLI unavailable)
- HiDevs platform verification: NOT VERIFIED (Requires deployment)
