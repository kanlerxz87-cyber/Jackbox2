#!/usr/bin/env python3
"""Regression check for the repository-wide public-site audit entry point."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
result = subprocess.run(
    [sys.executable, "tools/public_site_audit.py"],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
if "PUBLIC SITE AUDIT: PASS" not in result.stdout:
    raise SystemExit("Audit completed without its expected PASS marker.\n" + result.stdout)
for surface in ("root-current:", "central-la-2026:", "alternative-research:"):
    if surface not in result.stdout:
        raise SystemExit("Audit did not report all required verified surfaces.\n" + result.stdout)
print("Public-site audit regression: OK")
