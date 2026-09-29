import os

def test_required_docs_exist():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required_docs = ["README.md", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md", "agent.yaml"]
    for doc in required_docs:
        assert os.path.exists(os.path.join(base_dir, doc)), f"Missing required document: {doc}"
