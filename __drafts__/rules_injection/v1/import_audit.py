"""
AUDIT TOOL: Scans for non-standard imports and suggests replacements

Functionality:
1. Scan all project files for import statements
2. Flag prohibited packages (requests, bs4, pandas, etc.)
3. Suggest standard library alternatives
4. Generate migration path report
"""
import ast
import os
import sys

PROHIBITED = {
    'requests': 'urllib.request',
    'bs4': 'html.parser',
    'pandas': 'csv or json',
    'numpy': 'math or plain python lists',
    'typer': 'argparse',
    'click': 'argparse',
    'rich': 'sys.stdout + ANSI codes'
}

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return []

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in PROHIBITED:
                    violations.append((alias.name, PROHIBITED[alias.name.split('.')[0]]))
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in PROHIBITED:
                violations.append((node.module, PROHIBITED[node.module.split('.')[0]]))
    return violations

def main():
    root_dir = '.'
    print("Starting Compliance Audit...")
    found_violations = False
    for root, dirs, files in os.walk(root_dir):
        if '__drafts__' in root:
            continue # Skip drafts
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                violations = scan_file(path)
                if violations:
                    found_violations = True
                    print(f"[FAIL] {path}")
                    for v, sugg in violations:
                        print(f"  - Prohibited: {v} -> Use: {sugg}")

    if not found_violations:
        print("[PASS] No prohibited imports found.")

if __name__ == '__main__':
    main()
