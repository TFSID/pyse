# REFACTORING ROADMAP

## CURRENT STATE AUDIT:
- [x] Identify all non-standard imports (None found).
- [x] Document current CLI structure (Argparse used in `pyse.py` and engines).
- [x] Map external dependency usage (None).
- [x] Assess isolation compliance (Violations found in file writes, fixed in `pyse.py`).

## REFACTORING PRIORITIES:
1. **HIGH PRIORITY**: Ensure `pyse.py` writes to isolation paths. (Done)
2. **MEDIUM PRIORITY**: Update engines to write to isolation paths if run standalone. (Pending)
3. **LOW PRIORITY**: Clean up duplicate code in engines.

## ISOLATION PREPARATION:
- All new development goes to `__drafts__/{feature}/v{num}/`
- Each iteration creates complete file snapshots
- No diffs, only full versions
