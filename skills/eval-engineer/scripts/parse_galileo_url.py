#!/usr/bin/env python3
"""Parse Galileo console URLs into fetch-intake metadata."""

from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse


def parse_galileo_url(url: str) -> dict:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    result = {
        "console_url": url,
        "console_host": parsed.netloc,
        "workspace_slug": None,
        "project_id": None,
        "artifact_type": "unknown",
        "fetch_ready": False,
        "next_questions": [],
    }

    if len(parts) < 3 or parts[1] != "project":
        result["next_questions"].append(
            "Provide a Galileo project, log stream, experiment, session, or trace URL."
        )
        return result

    result["workspace_slug"] = parts[0]
    result["project_id"] = parts[2]

    if len(parts) == 3:
        result["artifact_type"] = "project"
        result["next_questions"].append(
            "Which log stream, experiment, session, trace, time window, or failure metric should I inspect?"
        )
        return result

    section = parts[3]
    artifact_id = parts[4] if len(parts) > 4 else None

    if section == "log-streams":
        result["artifact_type"] = "log_stream"
        result["log_stream_id"] = artifact_id
        result["fetch_ready"] = artifact_id is not None
        if artifact_id is None:
            result["next_questions"].append("Which log stream ID should I fetch?")
        else:
            result["next_questions"].append(
                "Should I fetch latest traces, failed traces, a time window, or aggregate metrics first?"
            )
        return result

    if section == "experiments":
        if artifact_id is None:
            result["artifact_type"] = "experiments_index"
            result["next_questions"].append(
                "Which specific experiment should I fetch: latest, named, failed, or a provided experiment ID?"
            )
        else:
            result["artifact_type"] = "experiment"
            result["experiment_id"] = artifact_id
            result["fetch_ready"] = True
        return result

    if section == "sessions":
        result["artifact_type"] = "session"
        result["session_id"] = artifact_id
        result["fetch_ready"] = artifact_id is not None
        if artifact_id is None:
            result["next_questions"].append("Which session ID should I fetch?")
        return result

    if section == "traces":
        result["artifact_type"] = "trace"
        result["trace_id"] = artifact_id
        result["fetch_ready"] = artifact_id is not None
        if artifact_id is None:
            result["next_questions"].append("Which trace ID should I fetch?")
        return result

    result["next_questions"].append(
        "I found the project, but not a recognized artifact type. Provide log stream, experiment, session, or trace context."
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse a Galileo console URL.")
    parser.add_argument("url")
    args = parser.parse_args()
    print(json.dumps(parse_galileo_url(args.url), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
