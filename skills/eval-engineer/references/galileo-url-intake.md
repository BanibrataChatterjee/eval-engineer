# Galileo URL Intake

Users often start with a console URL, not a local debug packet. Parse the URL,
preserve source metadata, and ask only for the missing information needed to
fetch useful evidence.

## Supported URL Shapes

```text
https://{console_host}/{workspace_slug}/project/{project_id}
https://{console_host}/{workspace_slug}/project/{project_id}/log-streams/{log_stream_id}
https://{console_host}/{workspace_slug}/project/{project_id}/experiments
https://{console_host}/{workspace_slug}/project/{project_id}/experiments/{experiment_id}
https://{console_host}/{workspace_slug}/project/{project_id}/sessions/{session_id}
https://{console_host}/{workspace_slug}/project/{project_id}/traces/{trace_id}
```

## Artifact Behavior

| Artifact | Fetch Readiness | Next Step |
| --- | --- | --- |
| project | not ready | Ask for log stream, experiment, session, trace, time window, or failure metric. |
| experiments_index | not ready | Ask for latest experiment, named experiment, failing experiment, or comparison pair. |
| log_stream | partially ready | Ask for latest N, failed traces, time window, or aggregate metrics if unspecified. |
| experiment | ready | Fetch run metrics, traces, scorer status, and dataset contract. |
| session | ready | Fetch session traces, spans, tool calls, metrics, and surrounding context. |
| trace | ready | Fetch the trace and ask whether comparison context is needed. |

## Packet Source Metadata

Every URL-derived packet should include:

```json
{
  "source": {
    "console_url": "...",
    "console_host": "...",
    "workspace_slug": "...",
    "project_id": "...",
    "artifact_type": "...",
    "log_stream_id": "...",
    "experiment_id": "...",
    "session_id": "...",
    "trace_id": "..."
  }
}
```

Do not print secrets. Report environment variable presence only.
