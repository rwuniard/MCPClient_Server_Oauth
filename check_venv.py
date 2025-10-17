#!/usr/bin/env python3
"""Quick script to check which virtual environment is active"""
import sys
from pathlib import Path

venv_path = Path(sys.prefix)
print(f"Active Python: {sys.executable}")
print(f"Virtual Environment: {venv_path}")
print(f"Is venv active: {sys.prefix != sys.base_prefix}")
