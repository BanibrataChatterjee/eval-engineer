#!/usr/bin/env python3
"""Summarize an Eval Engineer Galileo debug packet.

The script accepts both the current generic packet shape and the first
reference-agent packet shape. It is intentionally conservative: it prints the
evidence that is present without assuming a specific agent architecture.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _compact(value: Any) -> str:
    if isinstance(value, str):
        return " ".join(value.split())
    return json.dumps(value, sort_keys=True)


def _tool_call_text(call: dict[str, Any]) -> str:
    tool = call.get("tool") or call.get("name") or call.get("function", {}).get("name") or "<unknown>"
    args = call.get("args") or call.get("arguments") or call.get("function", {}).get("arguments") or {}
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            pass
    return f"{tool}({_compact(args)})"


def _metric_items(packet: dict[str, Any]) -> list[tuple[str, Any]]:
    metrics = packet.get("metrics") or packet.get("aggregate_metrics") or {}
    summary = packet.get("summary") or {}
    if not metrics and isinstance(summary.get("metrics"), dict):
        metrics = summary["metrics"]
    if isinstance(metrics, dict):
        return sorted(metrics.items())
    return []


def _expected_items(packet: dict[str, Any]) -> list[str]:
    dataset = packet.get("dataset") or {}
    expected_calls = dataset.get("expected_tool_calls") or packet.get("expected_tool_calls") or []
    if expected_calls:
        return [_tool_call_text(call) for call in expected_calls]

    expected = (
        dataset.get("expected_output")
        or dataset.get("ground_truth")
        or packet.get("expected_output")
        or packet.get("ground_truth")
    )
    return [_compact(expected)] if expected is not None else []


def _actual_items(packet: dict[str, Any]) -> list[str]:
    output = packet.get("session_output") or {}
    actual_calls = output.get("actual_tool_calls") or packet.get("actual_tool_calls") or []
    if actual_calls:
        return [_tool_call_text(call) for call in actual_calls]

    actual = output.get("final_response") or output.get("output") or packet.get("output")
    return [_compact(actual)] if actual is not None else []


def _rationales(packet: dict[str, Any]) -> list[str]:
    rationales = []
    for span in packet.get("scored_spans", []):
        for key, value in span.items():
            if key.endswith("_rationale") and value:
                rationales.append(_compact(value))
    return rationales[:3]


def _trace_lines(packet: dict[str, Any]) -> list[str]:
    lines = []
    for trace in packet.get("traces", [])[:5]:
        trace_id = trace.get("trace_id") or trace.get("id") or "<unknown>"
        scores = trace.get("scores") or trace.get("metrics") or {}
        notes = trace.get("notes") or trace.get("rationale") or ""
        parts = [f"- {trace_id}"]
        if scores:
            parts.append(f"scores={_compact(scores)}")
        if notes:
            parts.append(f"notes={_compact(notes)}")
        lines.append(" | ".join(parts))
    return lines


def summarize(packet: dict[str, Any]) -> str:
    dataset = packet.get("dataset") or {}
    summary = packet.get("summary") or {}
    identity = {
        "schema_version": packet.get("schema_version", "<missing>"),
        "project": packet.get("project") or packet.get("project_id") or "<unknown>",
        "run": packet.get("run_name") or packet.get("experiment_name") or packet.get("run_id") or "<unknown>",
        "agent_type": packet.get("agent_type") or summary.get("agent_type") or "<unknown>",
        "case": dataset.get("case_id") or packet.get("case_id") or "<none>",
    }

    lines = [f"{key}: {value}" for key, value in identity.items()]

    metric_items = _metric_items(packet)
    if metric_items:
        lines.append("metrics:")
        lines.extend(f"- {name}: {value}" for name, value in metric_items)

    top_failing = summary.get("top_failing_metrics") or packet.get("top_failing_metrics") or []
    if top_failing:
        lines.append("top_failing_metrics:")
        lines.extend(f"- {item}" for item in top_failing)

    expected = _expected_items(packet)
    if expected:
        lines.append("expected:")
        lines.extend(f"- {item}" for item in expected)

    actual = _actual_items(packet)
    if actual:
        lines.append("actual:")
        lines.extend(f"- {item}" for item in actual)

    tempting = dataset.get("wrong_but_tempting") or packet.get("wrong_but_tempting")
    if tempting:
        lines.append(f"known_trap: {_compact(tempting)}")

    trace_lines = _trace_lines(packet)
    if trace_lines:
        lines.append("traces:")
        lines.extend(trace_lines)

    rationales = _rationales(packet)
    if rationales:
        lines.append("galileo_rationales:")
        lines.extend(f"- {item}" for item in rationales)

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", nargs="?", type=Path, default=Path(".galileo/current/debug-packet.json"))
    args = parser.parse_args()

    with open(args.packet, encoding="utf-8") as handle:
        packet = json.load(handle)
    print(summarize(packet))


if __name__ == "__main__":
    main()
