# Debug Packet Reference

Debug packets are compact Galileo evidence for Eval Engineer's
diagnose/fix/verify loop. They are not tied to one agent, test case, or metric.
They can be built from either controlled experiments or production log streams.

## Purpose

The packet is the bridge between Galileo observability and code changes. It
should contain enough information for a coding agent to understand what failed
without loading raw trace exports into context.

## Recommended Fields

- `schema_version`: packet schema version.
- `run_id`, `run_name`, `experiment_id`, `experiment_name`, `project_id`:
  experiment evidence identity, when applicable.
- `log_stream_id` or `log_stream_name`: production evidence source, when
  applicable.
- `time_window` and `filters`: production query context, when built from a log
  stream.
- `agent_type`: for example `tool_calling`, `rag`, `workflow`, or `chat`.
- `summary`: high-level counts, top failing metrics, and metric values.
- `metrics` or `aggregate_metrics`: run-level scores.
- `traces`: a small set of relevant traces or spans with input, output, scores,
  short notes, stable IDs, and Galileo URLs when available.
- `sessions`: optional session-level grouping for production RCA.
- `dataset`: optional dataset row, expected output, expected tool calls, ground
  truth, or metadata.
- `session_output`: optional normalized output from the app under test.
- `scored_spans`: optional Galileo spans with metric rationales.

## Failure Contract

For every diagnosis, extract:

- relevant metric names and scores
- expected behavior, if available
- actual behavior
- evidence source: trace ID, span ID, dataset row, or experiment/run ID
  or log-stream/session ID
- Galileo link or stable ID for each key claim
- Galileo rationale, if present
- uncertainty: app bug, metric issue, dataset issue, integration issue, or
  insufficient evidence

## Use In A Skill Run

1. Summarize the current packet:

   ```bash
   python3 skills/galileo-eval-engineer/scripts/summarize_debug_packet.py .galileo/current/debug-packet.json
   ```

2. Diagnose from Galileo concepts:

   - datasets for repeatable test cases
   - metrics for quality signals
   - experiments for before/after comparison
   - log streams for production RCA and failure discovery
   - traces/spans for behavior
   - sessions for multi-turn or production workflows
   - custom metrics for domain-specific judgment

3. Change only the smallest allowed artifact.

4. Verification is complete only when a new local or Galileo run can be compared
   against the baseline evidence.

## Naming Convention

Inside `.galileo/current/`, use role-based names:

- `debug-packet.json`: baseline or active packet being diagnosed.
- `verification-debug-packet.json`: fresh packet from the after-change
  verification run.

In implementation-specific evidence folders, use descriptive timestamped names:

```text
<case-or-scope>-<provider-or-source>-<short-purpose>-<UTC timestamp>.json
```

The goal is for a future reader to know whether a packet is a baseline,
verification result, representative run, or metric trial without opening it.

## Source-Specific Expectations

Experiment packets should make the dataset row, expected behavior, aggregate
metrics, and experiment identity easy to compare across runs.

Log-stream packets should make the production slice explicit: log stream, time
window, filters, sessions, representative traces, and why those examples were
selected.
