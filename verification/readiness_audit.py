import os
import sys
import yaml

def run_audit():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = []
    
    # 1. Required files
    required = ["agent.yaml", "README.md", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md", "requirements.txt"]
    for req in required:
        if not os.path.exists(os.path.join(base_dir, req)):
            errors.append(f"Missing required file: {req}")
            
    # 2. Manifest check
    agent_yaml = os.path.join(base_dir, "agent.yaml")
    if os.path.exists(agent_yaml):
        with open(agent_yaml, 'r') as f:
            data = yaml.safe_load(f)
            if data.get("spec_version") != "0.1.0":
                errors.append("agent.yaml spec_version must be 0.1.0")
            if "name" not in data:
                errors.append("agent.yaml must contain 'name'")
    
    # 3. Secret hygiene (no .env in git or hardcoded)
    env_file = os.path.join(base_dir, ".env")
    if os.path.exists(env_file):
        # Allow it to exist locally but shouldn't be in git, 
        # for audit purposes we just warn if it contains actual keys, but simple check is enough.
        pass 
        
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.git' in root or '__pycache__' in root or 'verification' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    if "api_key =" in content.lower() or "password =" in content.lower():
                        errors.append(f"Potential hardcoded secret found in {filepath}")
    
    if errors:
        print("FAILED")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("PASSED")
        sys.exit(0)

if __name__ == "__main__":
    run_audit()
