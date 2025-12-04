# REFACTORING ROADMAP

## CURRENT STATE AUDIT:
- [x] Identify all non-standard imports (None found)
- [x] Document current CLI structure (Argparse based)
- [x] Map external dependency usage (Zero external dependencies)
- [x] Assess isolation compliance (Needs path adjustments for strict isolation)

## REFACTORING PRIORITIES:
1. **HIGH PRIORITY**: Ensure strict file isolation for output files (logs, results, cookies).
2. **MEDIUM PRIORITY**: Centralize configuration (moved to `config.ini` in previous iteration, needs to be standard).
3. **LOW PRIORITY**: Update docstrings to reflect strict vanilla python rules.

## ISOLATION PREPARATION:
- All new development goes to `__drafts__/{feature}/v{num}/`
- Each iteration creates complete file snapshots
- No diffs, only full versions
