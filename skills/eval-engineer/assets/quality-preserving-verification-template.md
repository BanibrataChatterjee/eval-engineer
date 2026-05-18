# Quality-Preserving Verification Plan

## Baseline

Name the baseline packet, experiment, log stream, trace/session slice, cost
metrics, latency metrics, token metrics, and quality metrics.

## Verification Run

Name the command, experiment, log-stream query, or production slice that will
produce the after-change packet.

## Cost Comparison

Use `scripts/compare_tokenomics_packets.py` or an equivalent comparison to
report:

- cost delta
- latency delta
- input token delta
- output token delta
- total token delta
- response or span-count delta
- quality metric delta

## Quality Gates

State the exact thresholds:

- Minimum acceptable quality:
- Allowed cost movement:
- Allowed latency movement:
- Required local checks:
- Required Galileo packet fields:

## Regression Check

Name the broader local suite, experiment slice, or log-stream segment that
should not regress.

## Go No-Go

- Keep the change if:
- Revert or revise if:
- Required artifacts to save:
- Residual behavior outside this cost/quality contract:

## Follow-Up

List candidate eval cases, production segments, metric sampling changes,
instrumentation improvements, or model-routing experiments to inspect next.

