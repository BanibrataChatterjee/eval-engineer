# Galileo Evidence Sources

Eval Engineer should support two Galileo evidence paths:

- experiments for controlled sample evals
- log streams for production or live-traffic RCA

Both paths should be normalized into compact debug packets before diagnosis.

## Experiments

Use experiments when the task is to run a known sample, compare before/after
behavior, or verify a candidate fix against a controlled dataset.

Experiments are best for:

- reference implementations under `tests/agents/`
- repeatable regression cases
- prompt, tool, retriever, or guardrail comparisons
- metric experiments and scorer wiring checks
- CI-like verification

Experiment packets should preserve:

- project ID or name
- experiment ID and name
- dataset row or case metadata
- aggregate metrics
- relevant traces and scored spans
- before/after packet identity

## Log Streams

Use log streams when the task is to diagnose real production or live-traffic
behavior and improve the implementation from observed failures.

Log streams are best for:

- recurring failures in production traffic
- monitoring slices by time, user segment, route, agent, tool, model, or metric
- session-level investigation
- trace/span drilldown from observed degradation
- discovering new candidate eval cases from real traffic

Log-stream packets should preserve:

- project ID or name
- log stream ID or name
- time window and filters
- session IDs and trace IDs
- relevant metrics and metric rationales
- representative failing examples
- links or stable IDs back to Galileo

## Shared Packet Shape

Do not make separate reasoning workflows for experiments and log streams unless
the evidence requires it. Normalize both into the same debug-packet contract:

- identity
- metrics
- expected behavior, if known
- actual behavior
- traces, spans, sessions, or dataset rows
- Galileo links or stable IDs
- uncertainty

For controlled tests, expected behavior often comes from the dataset. For log
streams, expected behavior may come from policies, product specs, prior good
sessions, user intent, or a human-supplied rubric.

## Fix Loop

For experiments:

1. run a controlled sample
2. fetch a debug packet
3. diagnose and fix
4. run another experiment
5. compare baseline and verification packets

For log streams:

1. query production traces/sessions by metric, time window, or segment
2. fetch representative debug packets
3. diagnose recurring failure patterns
4. make a bounded implementation change
5. verify with a controlled experiment or a fresh log-stream slice
6. promote reusable failures into candidate eval cases when appropriate

Production evidence should often become future controlled evals. That is how
real failures feed the self-improvement loop.
