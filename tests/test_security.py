import pytest
import os
import ast

def test_no_eval_exec_in_codebase():
    """Security check to ensure no eval or exec is used."""
    disallowed = ['eval(', 'exec(']
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.venv' in root or '.git' in root or '__pycache__' in root or 'tests' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    for bad in disallowed:
                        assert bad not in content, f"Found {bad} in {filepath}"

def test_no_subprocess_import():
    """Ensure we don't import subprocess to avoid arbitrary command execution."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for root, dirs, files in os.walk(base_dir):
        if 'venv' in root or '.venv' in root or '.git' in root or 'tests' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for name in node.names:
                                    assert name.name != 'subprocess', f"Found subprocess import in {filepath}"
                            elif isinstance(node, ast.ImportFrom):
                                assert node.module != 'subprocess', f"Found subprocess import in {filepath}"
                    except SyntaxError:
                        pass
