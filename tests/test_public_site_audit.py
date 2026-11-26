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
if "root-current:" not in result.stdout or "central-la-2026:" not in result.stdout:
    raise SystemExit("Audit did not report the current public surfaces.\n" + result.stdout)
print("Public-site audit regression: OK")
