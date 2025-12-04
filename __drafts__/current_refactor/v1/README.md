# REFACTORING ROADMAP

## CURRENT STATE AUDIT:
- [x] Identify all non-standard imports
- [x] Document current CLI structure
- [x] Map external dependency usage
- [x] Assess isolation compliance

## REFACTORING PRIORITIES:
1. **HIGH PRIORITY**: Replace `requests` with `urllib.request` (Done in `libs/fetch.py`)
2. **HIGH PRIORITY**: Replace `bs4/BeautifulSoup` with `html.parser` or regex (Codebase seems to use regex and native html parser)
3. **MEDIUM PRIORITY**: Convert any pandas DataFrames to `csv`/`json` + dicts (None found)
4. **LOW PRIORITY**: Remove any GUI/web server code (None found)

## ISOLATION PREPARATION:
- All new development goes to `__drafts__/{feature}/v{num}/`
- Each iteration creates complete file snapshots
- No diffs, only full versions
