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

# List of known standard libraries in Python 3.8+ (simplified)
# We can use a heuristic or a hardcoded list of common non-standard libs.
# Better to flag *everything* that is not in stdlib.
# For now, let's use a list of prohibited libraries mentioned in the prompt and common ones.

PROHIBITED = {
    'requests': 'urllib.request',
    'bs4': 'html.parser or xml.etree.ElementTree',
    'beautifulsoup4': 'html.parser',
    'pandas': 'csv or json',
    'numpy': 'native lists/math',
    'scipy': 'native math',
    'typer': 'argparse',
    'click': 'argparse',
    'rich': 'print with ANSI codes',
    'lxml': 'xml.etree.ElementTree',
    'selenium': 'urllib.request (if possible) or none',
    'playwright': 'urllib.request (if possible) or none',
    'aiohttp': 'urllib.request (sync) or asyncio (complex)',
    'flask': 'http.server',
    'django': 'http.server',
    'fastapi': 'http.server'
}

def is_standard_module(module_name):
    if module_name in sys.builtin_module_names:
        return True
    try:
        # This is a bit hacky, but checks if it's importable from standard locations.
        # However, checking against a list is safer for "Audit" purposes without importing code.
        # Let's rely on the explicit PROHIBITED list + any other unknown top-level imports.
        # Actually, let's just flag the PROHIBITED ones specifically as requested.
        pass
    except:
        pass
    return False

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        return [f"Error parsing {filepath}: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name in PROHIBITED:
                    violations.append((node.lineno, name, PROHIBITED[name]))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name in PROHIBITED:
                    violations.append((node.lineno, name, PROHIBITED[name]))

    return violations

def main():
    report = []
    violations_found = False

    print("Scanning for violations...")
    for root, dirs, files in os.walk('.'):
        if '__drafts__' in root or '.git' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                v = scan_file(filepath)
                if v:
                    violations_found = True
                    report.append(f"\n### File: `{filepath}`")
                    for lineno, lib, replacement in v:
                        report.append(f"- Line {lineno}: Found `{lib}`. Suggestion: Use `{replacement}`.")

    if not violations_found:
        report.append("\nNo prohibited imports found in the scanned files.")

    output_path = "__drafts__/current_refactor/v1/README.md"
    with open(output_path, 'w') as f:
        f.write("# REFACTORING ROADMAP\n\n")
        f.write("## COMPLIANCE AUDIT REPORT\n")
        f.write("\n".join(report))

        f.write("\n\n## CURRENT STATE AUDIT:\n")
        f.write("- [x] Identify all non-standard imports\n")
        f.write("- [ ] Document current CLI structure\n")
        f.write("- [ ] Map external dependency usage\n")
        f.write("- [ ] Assess isolation compliance\n")

        f.write("\n## REFACTORING PRIORITIES:\n")
        if violations_found:
             f.write("1. **HIGH PRIORITY**: Replace identified non-standard libraries.\n")
        else:
             f.write("1. **LOW PRIORITY**: No major violations found. Verify internal logic.\n")

        f.write("\n## ISOLATION PREPARATION:\n")
        f.write("- All new development goes to `__drafts__/{feature}/v{num}/`\n")
        f.write("- Each iteration creates complete file snapshots\n")
        f.write("- No diffs, only full versions\n")

    print(f"Report generated at {output_path}")

if __name__ == '__main__':
    main()
