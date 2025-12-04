"""
FEATURE DEVELOPMENT TEMPLATE
Use this structure for all new feature implementations

GUIDELINES:
1. Session Name: feat_{feature_name} (e.g., feat_proxy_manager)
2. Start from v1, increment with each change
3. Output ALL modified files in each version
4. Assume imports will be relative to draft structure
"""

import argparse
import sys
import os
from typing import Dict, List, Optional

class VanillaFeature:
    """Base class for all feature implementations"""

    def __init__(self):
        self.session_name = "feat_template"
        self.version = "v1"
        self.draft_root = f"__drafts__/{self.session_name}/{self.version}"

    def ensure_draft_structure(self):
        """Create necessary directory structure"""
        os.makedirs(self.draft_root, exist_ok=True)

    def implement(self) -> Dict[str, str]:
        """
        Returns: Dictionary of {file_path: content}
        Override this method in actual feature implementations
        """
        return {
            f"{self.draft_root}/implementation.py": self._template_content()
        }

    def _template_content(self) -> str:
        """Template method for actual implementation"""
        return '''"""
FEATURE IMPLEMENTATION TEMPLATE

RULES COMPLIANCE CHECKLIST:
✓ Only standard library imports
✓ CLI-focused (argparse, print)
✓ No external dependencies
✓ Outputs to __drafts__ structure
✓ Complete file snapshots (no diffs)
✓ Version increments with changes
"""

def main():
    print("Feature implementation here")

if __name__ == "__main__":
    main()'''
