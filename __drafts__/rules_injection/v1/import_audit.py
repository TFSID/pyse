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

PROHIBITED_MODULES = {
    'requests': 'urllib.request',
    'bs4': 'html.parser or re',
    'beautifulsoup4': 'html.parser or re',
    'pandas': 'csv or json',
    'numpy': 'math or standard lists',
    'typer': 'argparse',
    'click': 'argparse',
    'rich': 'sys.stdout (ANSI codes)',
    'lxml': 'xml.etree.ElementTree',
}

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read(), filename=filepath)
            except SyntaxError:
                return []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split('.')[0] in PROHIBITED_MODULES:
                            violations.append((alias.name, PROHIBITED_MODULES[alias.name.split('.')[0]]))
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.split('.')[0] in PROHIBITED_MODULES:
                        violations.append((node.module, PROHIBITED_MODULES[node.module.split('.')[0]]))
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
    return violations

def main():
    print("Starting Compliance Audit...")
    root_dir = '.'
    all_violations = {}

    for dirpath, _, filenames in os.walk(root_dir):
        if '__drafts__' in dirpath or '.git' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                path = os.path.join(dirpath, filename)
                v = scan_file(path)
                if v:
                    all_violations[path] = v

    if not all_violations:
        print("COMPLIANCE AUDIT PASSED: No prohibited imports found.")
    else:
        print("COMPLIANCE AUDIT FAILED: Violations found.")
        for path, v_list in all_violations.items():
            print(f"\nFile: {path}")
            for mod, replacement in v_list:
                print(f"  - Uses '{mod}'. Suggestion: Use '{replacement}'")

if __name__ == '__main__':
    main()
