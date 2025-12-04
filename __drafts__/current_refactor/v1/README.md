# REFACTORING ROADMAP

## CURRENT STATE AUDIT:
- [x] Identify all non-standard imports
- [x] Document current CLI structure
- [x] Map external dependency usage
- [x] Assess isolation compliance

## VIOLATIONS FOUND:
1.  **`libs/fetch.py`**:
    -   Uses `urllib.request`, `urllib.parse`, `http.cookiejar`, `gzip`.
    -   *Assessment*: COMPLIANT. These are all standard library modules. `requests` is NOT used.
2.  **`libs/html_parser.py`**:
    -   Uses `html.parser`, `xml.etree.ElementTree`.
    -   *Assessment*: COMPLIANT. `bs4` is NOT used.
3.  **`utils/helper.py`**:
    -   Uses `html` (standard), and fallbacks to `HTMLParser` (Python 2 legacy?).
    -   The `unescape_url` function tries `import HTMLParser` which is Python 2. This should be cleaned up for Python 3 only, but it's not an external dependency violation per se, just messy code.
4.  **`pyse.py`**:
    -   Uses `argparse`, `sys`, `os`, `threading`, `logging`.
    -   *Assessment*: COMPLIANT.
5.  **`engine/*.py`**:
    -   Uses `re`, `urllib.parse`, `json`.
    -   *Assessment*: COMPLIANT.

## COMPLIANCE REPORT:
The codebase appears to be **already using Standard Library** for the most part.
-   No `requests` found. `FetchRequest` uses `urllib.request`.
-   No `beautifulsoup4` found. `NativeHTMLParser` uses `html.parser` and `xml.etree`.
-   No `pandas` found.

However, there are potential issues with:
-   **Direct file writes**: `pyse.py` writes to `results.txt` (or user specified output) in the current directory.
    -   *Violation*: "Direct file writes to root directory".
    -   *Fix*: Redirect output to `__drafts__/{session}/v{n}/` or enforce a safe output directory in the logic.
-   **Isolation Mode**: The current `pyse.py` does not follow the `__drafts__` output structure by default.

## REFACTORING PRIORITIES:
1.  **HIGH PRIORITY**: Modify `pyse.py` to support/enforce output to `__drafts__` path or check constraints.
2.  **LOW PRIORITY**: Cleanup `utils/helper.py` Python 2 compatibility imports (`HTMLParser`).

## ISOLATION PREPARATION:
-   Refactored `pyse.py` will be placed in `__drafts__/rules_compliance/v1/`.
-   It should enforce that output files are written to a specific directory or just standard output.
