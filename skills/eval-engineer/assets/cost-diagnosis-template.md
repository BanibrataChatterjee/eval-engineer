# Cost Diagnosis

## RCA Summary

State the cost, latency, token, request-volume, retry, retrieval, tool, or
evaluation-cost issue in one or two sentences. Include whether this appears to
be app behavior, traffic mix, instrumentation, metric configuration, or
insufficient evidence.

## Evidence Source

- Source type:
- Galileo project:
- Experiment, log stream, session, or trace identity:
- Baseline packet:
- Time window or dataset slice:

## Cost Signals

- Cost:
- Latency:
- Input tokens:
- Output tokens:
- Total tokens:
- Responses or trace count:
- Span counts by type:
- Status or failure pattern:

## Quality Contract

Name the quality metrics that must not regress. Explain what each metric proves
and what remains outside its contract.

## Cost Driver

Identify the primary cost driver:

- prompt/context size
- RAG retrieval volume
- model routing
- output length
- retry or loop behavior
- tool overuse or tool errors
- evaluator or metric cost
- production traffic segment
- instrumentation gap

## Evidence Links

- Trace IDs:
- Span IDs:
- Session IDs:
- Metric values:
- Galileo URLs or stable IDs:

## Expected Versus Actual Spend

- Expected:
- Actual:
- First divergent trace, span, route, or segment:

## Uncertainty

List missing attribution, missing quality metrics, traffic-mix uncertainty,
metric sampling gaps, or instrumentation work needed before changing code.

