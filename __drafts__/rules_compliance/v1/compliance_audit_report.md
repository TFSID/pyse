# COMPLIANCE AUDIT REPORT

## 1. Import Audit
- **Status**: PASSED
- **Findings**:
  - No usage of `requests`, `bs4`, `selenium`, `pandas`, `numpy`, or `lxml` found in the codebase.
  - All scanned files (`pyse.py`, `libs/fetch.py`, `libs/html_parser.py`, `engine/*.py`) use only Python Standard Library modules (`os`, `sys`, `argparse`, `threading`, `logging`, `urllib`, `html.parser`, `xml.etree`, `json`, `re`, `random`, `configparser`, `hashlib`, `gzip`).

## 2. File Write Audit
- **Status**: ACTION REQUIRED
- **Findings**:
  - `pyse.py`: Writes directly to `results.txt` (or user specified path) in the current working directory.
  - `engine/*.py` (e.g., `google.py`): The `__main__` block writes directly to `google_results.txt` by default.
  - `libs/fetch.py`: Writes cookies to `cookie/` directory in the current working directory.
  - `config.ini`: Is read from the current working directory.

## 3. Structure & Isolation
- **Status**: ACTION REQUIRED
- **Findings**:
  - The project currently writes output files to the root directory.
  - To comply with the "Isolation Mode", outputs should be directed to `__drafts__/{session}/v{n}/`.

## Refactoring Roadmap
1.  **Refactor `pyse.py`**:
    - Update default output path to point to a designated results folder (or strictly use stdout/redirection if adhering to strict CLI philosophy, but the tool has `-o` argument).
    - For the purpose of this draft, I will modify `pyse.py` to default to `__drafts__/rules_compliance/v1/results.txt` if run from the root, or ensure it respects the isolation path.
    - However, since `pyse.py` is the entry point, users might expect `results.txt` in CWD. The "Isolation Mode" instruction "All code output must go to `__drafts__/`" likely refers to *my* development outputs (the code files I create), OR it means the *tool itself* should write data there during this dev phase.
    - The prompt says: "If you find direct file writes: Redirect to `__drafts__/{session}/v{n}/`". This implies the tool's runtime behavior should also be modified for this session.

2.  **Refactor `engine/*.py`**:
    - Update `__main__` blocks to write to the draft folder or remove the file writing defaults in favor of stdout.

3.  **Refactor `libs/fetch.py`**:
    - Cookie directory should be configurable or point to a temp dir / draft dir.

4.  **Refactor `utils/static.py`**:
    - Ensure `config.ini` is looked for in the CWD (standard) or a specific path. No major change needed if we assume CWD execution, but for isolation, we might want to ensure it doesn't clutter root.

## Plan for `rules_compliance/v1`
- I will create a compliant copy of `pyse.py` and `libs/fetch.py` in `__drafts__/rules_compliance/v1/`.
- I will verify that running `pyse.py` from that directory (with proper PYTHONPATH) writes results to the draft folder or a subdirectory within it.
