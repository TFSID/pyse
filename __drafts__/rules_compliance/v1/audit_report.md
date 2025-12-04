# Compliance Audit Report

## 1. Violations Found

### A. Non-Standard Library Imports
- **Status:** PASS.
- **Details:** No external dependencies (requests, bs4, pandas) were found. The codebase uses `urllib`, `html.parser`, and other standard libraries.

### B. Direct File Writes (Isolation Violation)
- **Status:** FAIL.
- **Details:**
    - `pyse.py` writes directly to `filename` (default `results.txt`) in the current directory.
    - `pyse.py` reads `args.keyword_list` from the current directory (though reading is less critical, it assumes path).
    - `libs/fetch.py` writes to `cookie_file` (default `cookies.txt`) in the current directory.
    - `engine/*.py` files have standalone execution blocks (`if __name__ == '__main__':`) that write to `output_file` (default `[engine]_results.txt`) in the current directory.

## 2. Refactoring Roadmap

### Phase 2: Refactoring Execution
- **Objective:** Redirect all output files to `__drafts__/rules_compliance/v1/outputs/` or similar isolation paths.
- **Steps:**
    1.  Refactor `pyse.py` to:
        -   Default output file to `__drafts__/rules_compliance/v1/results.txt`.
        -   Or, wrap file I/O to prefix paths with the isolation directory if they are relative.
    2.  Refactor `libs/fetch.py` to:
        -   Default cookie file to `__drafts__/rules_compliance/v1/cookies.txt`.
    3.  Refactor `engine/*.py`:
        -   Update standalone output defaults to `__drafts__/rules_compliance/v1/[engine]_results.txt`.
    4.  Verify all imports work within the `__drafts__` structure. Since we are moving the code *into* `__drafts__/rules_compliance/v1/`, the relative imports should work fine if we run from that directory.

### Phase 3: Continued Development Protocol
- New features will follow the `__drafts__/feat_{name}/v1/` structure.
