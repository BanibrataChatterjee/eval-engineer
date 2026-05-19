#!/usr/bin/env python3
"""Fetch a compact Eval Engineer debug packet for a Galileo log stream."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from galileo.search import get_sessions, get_spans, get_traces


DEFAULT_OUTPUT = Path(".galileo/current/debug-packet.json")
SYSTEM_METRIC_TERMS = (
    "cost",
    "token",
    "latency",
    "duration",
    "time",
    "response",
    "request",
)
STATUS_SUFFIXES = ("_status", "_rationale", "_explanation", "_reasoning")
EXCLUDED_METRIC_SUFFIXES = ("_ems_error_code",)


def to_dict(record: Any) -> dict[str, Any]:
    if isinstance(record, dict):
        return record
    if hasattr(record, "to_dict"):
        return record.to_dict()
    return dict(getattr(record, "__dict__", {}))


def parse_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def truncate(value: Any, max_chars: int = 2000) -> Any:
    if isinstance(value, str) and len(value) > max_chars:
        return f"{value[:max_chars]}...[truncated]"
    if isinstance(value, list):
        return [truncate(item, max_chars=max_chars) for item in value]
    if isinstance(value, dict):
        return {key: truncate(item, max_chars=max_chars) for key, item in value.items()}
    return value


def numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def metric_base_name(name: str) -> str:
    base = name.split("@", 1)[0]
    for suffix in STATUS_SUFFIXES:
        if base.endswith(suffix):
            return base[: -len(suffix)]
    return base


def aggregate_name(name: str) -> str:
    base = metric_base_name(name)
    return base if base.startswith("average_") else f"average_{base}"


def is_system_metric(name: str) -> bool:
    lowered = metric_base_name(name).lower()
    return any(term in lowered for term in SYSTEM_METRIC_TERMS)


def is_excluded_metric(name: str) -> bool:
    lowered = metric_base_name(name).lower()
    return any(lowered.endswith(suffix) for suffix in EXCLUDED_METRIC_SUFFIXES)


def record_metrics(record: dict[str, Any]) -> dict[str, Any]:
    metrics = record.get("metrics") or {}
    return metrics if isinstance(metrics, dict) else {}


def aggregate_numeric_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    values_by_name: dict[str, list[float]] = {}
    for record in records:
        for name, value in record_metrics(record).items():
            if any(metric_base_name(name).endswith(suffix) for suffix in STATUS_SUFFIXES):
                continue
            if is_excluded_metric(name):
                continue
            metric_value = numeric(value)
            if metric_value is None:
                continue
            values_by_name.setdefault(aggregate_name(name), []).append(metric_value)

    return {
        name: sum(values) / len(values)
        for name, values in sorted(values_by_name.items())
        if values
    }


def scorer_metric_summary(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    numeric_counts: dict[str, int] = {}
    for record in records:
        metrics = record_metrics(record)
        for name, value in metrics.items():
            base = metric_base_name(name)
            if not base or is_system_metric(base):
                continue
            if is_excluded_metric(base):
                continue
            if numeric(value) is not None:
                numeric_counts[base] = numeric_counts.get(base, 0) + 1
                summary.setdefault(base, {"numeric_records": 0})
            if name.endswith("_status"):
                status = str(value)
                metric_summary = summary.setdefault(base, {"numeric_records": 0})
                metric_summary[status] = metric_summary.get(status, 0) + 1

    for base, count in numeric_counts.items():
        summary.setdefault(base, {})["numeric_records"] = count
    return dict(sorted(summary.items()))


def records_from_response(response: Any) -> list[dict[str, Any]]:
    records = getattr(response, "records", response)
    if records is None:
        return []
    return [to_dict(record) for record in records]


def trace_summary(trace: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in {
            "id": trace.get("id"),
            "trace_id": trace.get("trace_id"),
            "name": trace.get("name"),
            "scores": record_metrics(trace),
        }.items()
        if value not in (None, {}, [])
    }


def span_summary(span: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in {
            "id": span.get("id"),
            "trace_id": span.get("trace_id"),
            "parent_id": span.get("parent_id"),
            "type": span.get("type"),
            "name": span.get("name"),
            "model": span.get("model"),
            "status_code": span.get("status_code"),
            "input": truncate(parse_json(span.get("input"))),
            "output": truncate(parse_json(span.get("output"))),
            "metrics": record_metrics(span),
        }.items()
        if value not in (None, {}, [])
    }


def parse_log_stream_url(url: str) -> dict[str, Any]:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    source: dict[str, Any] = {
        "console_url": url,
        "console_host": parsed.netloc,
    }
    if len(parts) >= 5 and parts[1] == "project" and parts[3] == "log-streams":
        source.update(
            {
                "workspace_slug": parts[0],
                "project_id": parts[2],
                "log_stream_id": parts[4],
            }
        )
    return source


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip("\"'")


def missing_env_vars(required: tuple[str, ...]) -> list[str]:
    return [name for name in required if not os.getenv(name)]


def build_packet(
    *,
    project_id: str,
    log_stream_id: str,
    limit: int = 20,
    span_limit: int | None = None,
    session_limit: int | None = None,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    span_limit = span_limit or limit * 5
    session_limit = session_limit or limit
    traces = records_from_response(get_traces(project_id, log_stream_id=log_stream_id, limit=limit))
    spans = records_from_response(get_spans(project_id, log_stream_id=log_stream_id, limit=span_limit))
    sessions = records_from_response(get_sessions(project_id, log_stream_id=log_stream_id, limit=session_limit))

    records = traces + spans
    aggregate_metrics = aggregate_numeric_metrics(records)
    aggregate_metrics["total_responses"] = len(traces)
    scorer_metrics = scorer_metric_summary(records)
    metric_fetch_status = "ok" if len(aggregate_metrics) > 1 else "missing_metric_results"
    span_types = sorted({span.get("type") for span in spans if span.get("type")})

    merged_source = {
        "project_id": project_id,
        "log_stream_id": log_stream_id,
    }
    if source:
        merged_source.update(source)
    merged_source["project_id"] = project_id
    merged_source["log_stream_id"] = log_stream_id

    return {
        "schema_version": "0.2",
        "source_type": "log_stream",
        "agent_type": "unknown",
        "project_id": project_id,
        "log_stream_id": log_stream_id,
        "source": merged_source,
        "metric_fetch_status": metric_fetch_status,
        "aggregate_metrics": aggregate_metrics,
        "scorer_metrics": scorer_metrics,
        "traces": [trace_summary(trace) for trace in traces],
        "sessions": [
            {key: value for key, value in {"id": session.get("id"), "name": session.get("name")}.items() if value}
            for session in sessions
        ],
        "span_counts": {
            "total": len(spans),
            "by_type": {span_type: sum(1 for span in spans if span.get("type") == span_type) for span_type in span_types},
        },
        "scored_spans": [span_summary(span) for span in spans if record_metrics(span)],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch a Galileo log stream debug packet.")
    parser.add_argument("--url", help="Galileo console log-stream URL.")
    parser.add_argument("--project-id", help="Galileo project ID.")
    parser.add_argument("--log-stream-id", help="Galileo log stream ID.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum traces to fetch.")
    parser.add_argument("--span-limit", type=int, help="Maximum spans to fetch. Defaults to limit * 5.")
    parser.add_argument("--session-limit", type=int, help="Maximum sessions to fetch. Defaults to limit.")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Optional env file to load without printing values.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output debug packet path.")
    parser.add_argument("--json", action="store_true", help="Print the full packet JSON.")
    args = parser.parse_args(argv)

    load_env_file(args.env_file)
    missing = missing_env_vars(("GALILEO_API_KEY", "GALILEO_CONSOLE_URL"))
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
        return 2

    source = parse_log_stream_url(args.url) if args.url else {}
    project_id = args.project_id or source.get("project_id")
    log_stream_id = args.log_stream_id or source.get("log_stream_id")
    if not project_id or not log_stream_id:
        print("Provide --url or both --project-id and --log-stream-id.", file=sys.stderr)
        return 2

    packet = build_packet(
        project_id=project_id,
        log_stream_id=log_stream_id,
        limit=args.limit,
        span_limit=args.span_limit,
        session_limit=args.session_limit,
        source=source,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2, ensure_ascii=True), encoding="utf-8")
    if args.json:
        print(json.dumps(packet, indent=2, ensure_ascii=True))
    else:
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "metric_fetch_status": packet["metric_fetch_status"],
                    "aggregate_metric_count": len(packet["aggregate_metrics"]) - 1,
                    "scorer_metric_count": len(packet["scorer_metrics"]),
                    "trace_count": len(packet["traces"]),
                    "span_count": packet["span_counts"]["total"],
                },
                indent=2,
                ensure_ascii=True,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
