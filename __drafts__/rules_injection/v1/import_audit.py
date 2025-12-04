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

STANDARD_LIBS = {
    'os', 'sys', 're', 'json', 'time', 'random', 'logging', 'argparse',
    'threading', 'concurrent', 'urllib', 'http', 'html', 'socket',
    'hashlib', 'gzip', 'base64', 'csv', 'sqlite3', 'cmd', 'xml', 'abc'
}

PROHIBITED_LIBS = {
    'requests': 'urllib.request',
    'bs4': 'html.parser or xml.etree.ElementTree',
    'beautifulsoup4': 'html.parser or xml.etree.ElementTree',
    'pandas': 'csv or json + dicts',
    'typer': 'argparse',
    'click': 'argparse',
    'rich': 'print with ANSI codes',
    'lxml': 'xml.etree.ElementTree',
    'selenium': 'None (CLI only)',
    'playwright': 'None (CLI only)',
}

def is_standard_lib(module_name):
    if module_name in STANDARD_LIBS:
        return True
    # Heuristic for submodules
    base = module_name.split('.')[0]
    return base in STANDARD_LIBS

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not is_standard_lib(alias.name) and not alias.name.startswith(('utils', 'engine', 'libs')):
                        violations.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module and not is_standard_lib(node.module) and not node.module.startswith(('utils', 'engine', 'libs')):
                    violations.append((node.module, node.lineno))
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return violations

def main():
    report_lines = []
    report_lines.append("# COMPLIANCE AUDIT REPORT")
    report_lines.append("\n## VIOLATIONS FOUND")

    root_dir = "."
    violations_found = False

    for root, dirs, files in os.walk(root_dir):
        if "__drafts__" in root or ".git" in root or "__pycache__" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                file_violations = scan_file(filepath)

                if file_violations:
                    violations_found = True
                    report_lines.append(f"\n### {filepath}")
                    for lib, line in file_violations:
                        suggestion = PROHIBITED_LIBS.get(lib, "Check if standard library or internal module")
                        report_lines.append(f"- Line {line}: Import `{lib}` -> Suggestion: `{suggestion}`")

    if not violations_found:
        report_lines.append("\nNo violations found! Codebase appears compliant with standard library rules.")

    report_content = "\n".join(report_lines)
    print(report_content)

    # Save report
    os.makedirs("__drafts__/rules_compliance/v1", exist_ok=True)
    with open("__drafts__/rules_compliance/v1/COMPLIANCE_REPORT.md", "w") as f:
        f.write(report_content)

if __name__ == "__main__":
    main()
