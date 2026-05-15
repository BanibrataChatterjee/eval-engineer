"""Data loading for the agentic RAG case-resolution fixture."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


EXAMPLE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXAMPLE_DIR / "data"


def load_json(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def load_cases(case_id: str | None = None) -> list[dict[str, Any]]:
    cases = load_json("cases.json")
    if case_id:
        cases = [case for case in cases if case["id"] == case_id]
        if not cases:
            raise ValueError(f"Case not found: {case_id}")
    return cases


def load_documents() -> list[dict[str, Any]]:
    return load_json("corpus.json")


def load_accounts() -> dict[str, dict[str, Any]]:
    return {item["account_id"]: item for item in load_json("accounts.json")}


def load_tickets() -> list[dict[str, Any]]:
    return load_json("tickets.json")


def load_audit_logs() -> list[dict[str, Any]]:
    return load_json("audit_logs.json")

