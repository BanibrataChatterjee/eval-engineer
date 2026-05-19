---
name: eval-fetch
description: Use when a user provides Galileo URLs, project IDs, log stream IDs, experiment IDs, session IDs, trace IDs, or asks to bring Galileo evidence into the repo.
---

# Eval Fetch

Use this skill to turn messy Galileo console links and IDs into local evidence.
The goal is a grounded debug packet, not a diagnosis.

## First Parse The Input

Use `skills/eval-engineer/scripts/parse_galileo_url.py` when the user provides a
Galileo URL. Follow `skills/eval-engineer/references/galileo-url-intake.md` for
artifact-specific behavior.

Preserve source metadata in the packet:

- `source.console_url`
- `source.console_host`
- `source.workspace_slug`
- `source.project_id`
- artifact IDs such as `log_stream_id`, `experiment_id`, `session_id`, or
  `trace_id`

## Ask Only For Missing Information

- project URL: ask for log stream, experiment, session, trace, time window, or
  failure metric.
- Experiments list URL: ask for latest experiment, specific experiment, failing
  experiment, or comparison pair.
- Log stream URL: ask for latest N traces, failed traces, time window, or
  aggregate metrics if the user did not specify.
- Trace/session URL: fetch that artifact and ask whether to compare against a
  baseline only if needed.
- If the URL parser returns `fetch_ready: true`, say the Galileo artifact is
  resolved. If a slice is still needed, ask which slice to fetch; do not label
  the URL as not fetch-ready.

## Output

Write or guide writing `.galileo/current/debug-packet.json`. If fetching cannot
complete, state the blocker exactly: missing credentials, permission denied,
ambiguous URL, incomplete scorer jobs, or missing metric results.
