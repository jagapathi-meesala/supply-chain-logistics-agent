import os
import yaml
import json
import pytest
from jsonschema import validate, ValidationError

def test_open_gap_schema():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    agent_yaml_path = os.path.join(base_dir, "agent.yaml")
    schema_path = os.path.join(base_dir, "agent-yaml.schema.json")
    
    assert os.path.exists(agent_yaml_path), "agent.yaml not found"
    assert os.path.exists(schema_path), "agent-yaml.schema.json not found"
    
    with open(agent_yaml_path, 'r') as f:
        manifest = yaml.safe_load(f)
        
    with open(schema_path, 'r') as f:
        schema = json.load(f)
        
    try:
        validate(instance=manifest, schema=schema)
    except ValidationError as e:
        pytest.fail(f"agent.yaml failed schema validation: {e}")

def test_tool_schemas():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tool_schema_path = os.path.join(base_dir, "tool.schema.json")
    tools_dir = os.path.join(base_dir, "tools")
    
    if not os.path.exists(tool_schema_path):
        pytest.skip("tool.schema.json not found")
        
    with open(tool_schema_path, 'r') as f:
        tool_schema = json.load(f)
        
    for tool_file in os.listdir(tools_dir):
        if tool_file.endswith(".yaml"):
            with open(os.path.join(tools_dir, tool_file), 'r') as f:
                tool_manifest = yaml.safe_load(f)
            try:
                validate(instance=tool_manifest, schema=tool_schema)
            except ValidationError as e:
                pytest.fail(f"{tool_file} failed schema validation: {e}")
