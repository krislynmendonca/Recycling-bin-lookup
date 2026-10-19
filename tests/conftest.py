"""Pytest bootstrap: make the project root importable.

Tests live in tests/ without a package marker, so pytest would only add tests/
itself to sys.path. Adding the project root here lets every test import the
project modules (normalize, lookup, refusal) directly.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
