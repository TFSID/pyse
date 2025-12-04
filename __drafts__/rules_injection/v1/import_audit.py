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

PROHIBITED_IMPORTS = {
    'requests': 'urllib.request',
    'bs4': 'html.parser',
    'beautifulsoup4': 'html.parser',
    'pandas': 'csv or json module',
    'numpy': 'math module or native lists',
    'typer': 'argparse',
    'click': 'argparse',
    'rich': 'sys.stdout + ANSI codes'
}

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] in PROHIBITED_IMPORTS:
                        violations.append((alias.name, PROHIBITED_IMPORTS[alias.name.split('.')[0]]))
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] in PROHIBITED_IMPORTS:
                    violations.append((node.module, PROHIBITED_IMPORTS[node.module.split('.')[0]]))
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return violations

def main():
    root_dir = os.getcwd()
    report = []

    print(f"Scanning {root_dir} for violations...")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip __drafts__ and .git
        if '__drafts__' in dirpath or '.git' in dirpath:
            continue

        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                violations = scan_file(filepath)
                if violations:
                    for v in violations:
                        report.append(f"VIOLATION in {filepath}: Imported '{v[0]}'. Use '{v[1]}' instead.")

    if report:
        print("\n=== COMPLIANCE REPORT ===")
        for line in report:
            print(line)
        print("\nFAILURE: Violations found.")
        sys.exit(1)
    else:
        print("\nSUCCESS: No prohibited imports found.")
        sys.exit(0)

if __name__ == '__main__':
    main()
