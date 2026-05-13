# Galileo Experiments Reference

Eval Engineer v0.1 should use Galileo experiments for controlled reference-agent
evaluation. Experiments are for sample evals and repeatable before/after
verification. Log streams are the production or live-traffic RCA path and are
covered separately in `galileo-sources.md`.

## Project and Naming

- Project: `eval-engineer`
- Experiment format: `<implementation>-<UTC timestamp>`
- Example: `checkout-agent-20260512T101500Z`

## Metrics

Choose experiment metrics from the behavior being tested. Do not default to
agent metrics unless the failure is actually about agent/tool behavior. See
`metrics.md` for metric families and selection guidance.

The preferred implementation pattern is the SDK example style:

```python
from galileo import GalileoMetrics
from galileo.experiments import run_experiment

run_experiment(
    experiment_name,
    project="eval-engineer",
    dataset=[{"input": {...}}],
    function=runner_function,
    metrics=[
        # Choose metrics from the failure contract.
        # Examples:
        # GalileoMetrics.tool_selection_quality,
        # GalileoMetrics.correctness,
        # GalileoMetrics.context_adherence,
        # GalileoMetrics.instruction_adherence,
    ],
)
```

This implementation pattern is useful because it gives Eval Engineer a
repeatable dataset/function/metrics loop. The example metric list is not a
recommendation to use agent metrics for every app.

For function-based experiments in `galileo==1.39.0`, `run_experiment` may upsert
scorer settings without starting the non-system scorer job. If requested agent
metrics do not appear after traces flush, explicitly create a
`log_stream_scorer` job for the missing metric with:

- `scorer_config`: the missing metric's scorer config from
  `create_metric_configs`.
- `stream_metrics=True`.
- `process_existing_inference_runs=True`.

If the installed SDK does not expose a docs-listed constant, use the exact
metric string only as a temporary compatibility fallback and record it in
`.galileo/learnings.md`.

The first milestone is not perfect metric interpretation. It is confirming that
experiments, traces, metrics, and fetches work end to end for one focused slice.

The current gate is passed when a fetched experiment includes the requested
agent, RAG, or custom metric values. Experiment creation alone is not enough.

## Evidence Rule

The skill should prefer compact debug packets over raw SDK responses. Raw traces
and metrics are source evidence; debug packets are the reasoning input for the
coding agent.
