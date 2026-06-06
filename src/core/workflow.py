"""Shared workflow utility helpers for repo orchestration."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def ensure_workspace(workspace: str) -> None:
    Path(workspace).mkdir(parents=True, exist_ok=True)


def sanitize_branch_name(task_description: str) -> str:
    safe_name = "_".join(task_description.strip().split())
    return f"feature/{safe_name}"


def execute_command(command: list[str], cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)


def write_code(output_path: str, code: str) -> None:
    Path(output_path).write_text(code, encoding="utf-8")
