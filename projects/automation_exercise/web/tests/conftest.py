"""
tests/conftest.py
-----------------
Ensures the project root directory is on sys.path so that top-level packages
(pages, utils, fixtures) are importable both at runtime and inside IDEs such
as PyCharm.

How it works
------------
pytest inserts the directory that contains a conftest.py into sys.path.
By placing this file in `tests/`, pytest adds `tests/` to the path.
The explicit `sys.path.insert` below additionally adds the *project root*
(one level up), which is where `pages/`, `utils/`, and `fixtures/` live.

For PyCharm specifically
------------------------
1. Open **File → Project Structure** (⌘;).
2. Select the project root folder (`automation_exercise/`).
3. Click **Mark as → Sources Root** (blue folder icon).
4. Click OK — the "unresolved reference" errors will disappear immediately.

Alternatively, the `pyproject.toml` at the project root contains Pyright /
Pylance settings that achieve the same result for VS Code users.
"""

import sys
import os

# Insert the project root (parent of the `tests/` directory) at the front of
# sys.path so that `from pages import ...` and `from utils import ...` work
# in every test file without needing to install the project as a package.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
