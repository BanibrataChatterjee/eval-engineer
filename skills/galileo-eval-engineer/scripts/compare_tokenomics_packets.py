#!/usr/bin/env python3
"""Compare tokenomics evidence across two Galileo debug packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COST_FIELDS = [
    "average_cost",
    "total_cost",
    "average_latency",
    "total_latency",
    "average_num_input_tokens",
    "average_num_output_tokens",
    "average_num_total_tokens",
    "total_responses",
]

TRAFFIC_OR_VOLUME_FIELDS = {"total_responses"}
TRAFFIC_OR_VOLUME_TERMS = (
    "traffic",
    "volume",
    "request_count",
    "response_count",
    "trace_count",
    "session_count",
    "total_requests",
    "total_responses",
)
EFFICIENCY_TERMS = (
    "cost",
    "latency",
    "duration",
    "token",
    "retry",
    "agent_step",
    "span_count",
    "call_count",
    "retrieved_context",
    "retrieved_document",
    "rerank",
    "self_check",
    "planner",
    "reflection",
    "evaluator",
    "sampling_rate",
    "cache_miss",
)
LOWER_IS_BETTER_QUALITY_TERMS = (
    "error_rate",
    "failure_rate",
    "fail_rate",
    "toxicity",
    "hallucination",
    "violation_rate",
    "unsafe_rate",
)


def _metrics(packet: dict[str, Any]) -> dict[str, Any]:
    metrics = packet.get("metrics") or packet.get("aggregate_metrics") or {}
    summary = packet.get("summary") or {}
    if not metrics and isinstance(summary.get("metrics"), dict):
        metrics = summary["metrics"]
    return metrics if isinstance(metrics, dict) else {}


def _segments(packet: dict[str, Any]) -> dict[str, Any]:
    segments = packet.get("segments") or packet.get("segment_metrics") or {}
    return segments if isinstance(segments, dict) else {}


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _delta(before: float | None, after: float | None) -> dict[str, Any]:
    if before is None or after is None:
        return {"before": before, "after": after, "delta": None, "pct_delta": None}
    pct_delta = None if before == 0 else ((after - before) / abs(before)) * 100
    return {
        "before": before,
        "after": after,
        "delta": after - before,
        "pct_delta": pct_delta,
    }


def _cost_classification(name: str) -> str:
    normalized = name.lower()
    if name in TRAFFIC_OR_VOLUME_FIELDS:
        return "traffic_or_volume"
    if any(term in normalized for term in TRAFFIC_OR_VOLUME_TERMS):
        return "traffic_or_volume"
    return "efficiency"


def _is_efficiency_or_volume_field(name: str, quality_metrics: set[str]) -> bool:
    if name in quality_metrics:
        return False
    normalized = name.lower()
    if any(term in normalized for term in TRAFFIC_OR_VOLUME_TERMS):
        return True
    if any(term in normalized for term in EFFICIENCY_TERMS):
        return True
    return False


def _quality_direction(name: str, lower_is_better: set[str]) -> str:
    normalized = name.lower()
    if name in lower_is_better:
        return "lower_is_better"
    if any(term in normalized for term in LOWER_IS_BETTER_QUALITY_TERMS):
        return "lower_is_better"
    return "higher_is_better"


def _quality_regressed(values: dict[str, Any]) -> bool:
    delta = values.get("delta")
    if delta is None:
        return False
    if values.get("direction") == "lower_is_better":
        return delta > 0
    return delta < 0


def _format_number(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        if value == 0:
            return "0"
        return f"{value:.6g}"
    return str(value)


def _compare_metric_sets(
    before_metrics: dict[str, Any],
    after_metrics: dict[str, Any],
    quality_metrics: list[str],
    lower_is_better: set[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    quality_metric_set = set(quality_metrics)
    candidate_cost_fields = []
    all_metric_names = set(before_metrics) | set(after_metrics)
    for field in COST_FIELDS:
        if field in all_metric_names:
            candidate_cost_fields.append(field)
    candidate_cost_fields.extend(
        sorted(
            field
            for field in all_metric_names
            if field not in candidate_cost_fields
            and _is_efficiency_or_volume_field(field, quality_metric_set)
        )
    )

    cost = {}
    for field in candidate_cost_fields:
        values = _delta(_numeric(before_metrics.get(field)), _numeric(after_metrics.get(field)))
        values["classification"] = _cost_classification(field)
        cost[field] = values

    quality = {}
    for field in quality_metrics:
        if field not in before_metrics and field not in after_metrics:
            continue
        values = _delta(_numeric(before_metrics.get(field)), _numeric(after_metrics.get(field)))
        values["direction"] = _quality_direction(field, lower_is_better)
        quality[field] = values

    return cost, quality


def _compare_segments(
    baseline: dict[str, Any],
    verification: dict[str, Any],
    quality_metrics: list[str],
    lower_is_better: set[str],
) -> dict[str, dict[str, Any]]:
    before_segments = _segments(baseline)
    after_segments = _segments(verification)
    compared_segments = {}
    for name in sorted(set(before_segments) & set(after_segments)):
        cost, quality = _compare_metric_sets(
            _metrics(before_segments[name]),
            _metrics(after_segments[name]),
            quality_metrics,
            lower_is_better,
        )
        compared_segments[name] = {"cost": cost, "quality": quality}
    return compared_segments


def _any_quality_regressed(quality: dict[str, Any]) -> bool:
    return any(_quality_regressed(values) for values in quality.values())


def compare(
    baseline: dict[str, Any],
    verification: dict[str, Any],
    quality_metrics: list[str],
    lower_is_better_quality_metrics: list[str] | None = None,
) -> dict[str, Any]:
    before_metrics = _metrics(baseline)
    after_metrics = _metrics(verification)
    lower_is_better = set(lower_is_better_quality_metrics or [])
    cost, quality = _compare_metric_sets(
        before_metrics,
        after_metrics,
        quality_metrics,
        lower_is_better,
    )
    segments = _compare_segments(baseline, verification, quality_metrics, lower_is_better)

    improved_cost = [
        name
        for name, values in cost.items()
        if values["delta"] is not None and values["delta"] < 0
        and values["classification"] == "efficiency"
    ]
    segment_quality = {
        name: values["quality"]
        for name, values in segments.items()
        if values["quality"]
    }
    has_quality_evidence = bool(quality or segment_quality)
    regressed_quality = _any_quality_regressed(quality) or any(
        _any_quality_regressed(values) for values in segment_quality.values()
    )

    if not cost:
        decision = "inconclusive: no comparable cost, latency, token, or response metrics"
    elif not has_quality_evidence:
        decision = "inconclusive: no comparable quality metrics"
    elif regressed_quality:
        decision = "reject: quality regressed"
    elif improved_cost:
        decision = "keep-candidate: cost evidence improved and quality did not regress"
    else:
        decision = "inconclusive: quality held but efficiency evidence did not improve"

    return {
        "baseline": baseline.get("experiment_name") or baseline.get("run_name") or baseline.get("run_id"),
        "verification": verification.get("experiment_name") or verification.get("run_name") or verification.get("run_id"),
        "cost": cost,
        "quality": quality,
        "segments": segments,
        "decision": decision,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Tokenomics Packet Comparison",
        "",
        f"- Baseline: `{result.get('baseline') or '<unknown>'}`",
        f"- Verification: `{result.get('verification') or '<unknown>'}`",
        f"- Decision: {result['decision']}",
        "",
        "## Cost, Latency, And Token Metrics",
        "",
        "| Metric | Baseline | Verification | Delta | Percent Delta |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, values in result["cost"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    _format_number(values["before"]),
                    _format_number(values["after"]),
                    _format_number(values["delta"]),
                    _format_number(values["pct_delta"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Quality Metrics",
            "",
            "| Metric | Direction | Baseline | Verification | Delta | Percent Delta |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for name, values in result["quality"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    name,
                    values.get("direction", "higher_is_better"),
                    _format_number(values["before"]),
                    _format_number(values["after"]),
                    _format_number(values["delta"]),
                    _format_number(values["pct_delta"]),
                ]
            )
            + " |"
        )
    if result.get("segments"):
        lines.extend(["", "## Segment Quality Metrics", ""])
        for segment, values in result["segments"].items():
            if not values["quality"]:
                continue
            lines.extend(
                [
                    f"### {segment}",
                    "",
                    "| Metric | Direction | Baseline | Verification | Delta | Percent Delta |",
                    "| --- | --- | ---: | ---: | ---: | ---: |",
                ]
            )
            for name, metric_values in values["quality"].items():
                lines.append(
                    "| "
                    + " | ".join(
                        [
                            name,
                            metric_values.get("direction", "higher_is_better"),
                            _format_number(metric_values["before"]),
                            _format_number(metric_values["after"]),
                            _format_number(metric_values["delta"]),
                            _format_number(metric_values["pct_delta"]),
                        ]
                    )
                    + " |"
                )
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", nargs="?", type=Path, default=Path(".galileo/current/debug-packet.json"))
    parser.add_argument(
        "verification",
        nargs="?",
        type=Path,
        default=Path(".galileo/current/verification-debug-packet.json"),
    )
    parser.add_argument(
        "--quality-metrics",
        default="average_tool_selection_quality,tool_selection_quality,tool_error_rate,count_tool_error_rate,correctness,groundedness,context_adherence,instruction_adherence",
        help="Comma-separated quality metrics that must not regress.",
    )
    parser.add_argument(
        "--lower-is-better-quality-metrics",
        default="",
        help="Comma-separated quality metrics where an increase is a regression, such as tool_error_rate.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    verification = json.loads(args.verification.read_text(encoding="utf-8"))
    quality_metrics = [metric.strip() for metric in args.quality_metrics.split(",") if metric.strip()]
    lower_is_better_quality_metrics = [
        metric.strip() for metric in args.lower_is_better_quality_metrics.split(",") if metric.strip()
    ]
    result = compare(baseline, verification, quality_metrics, lower_is_better_quality_metrics)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_markdown(result))


if __name__ == "__main__":
    main()
