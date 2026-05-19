# Tool-Calling Support Agent

This is the first reference agent for Eval Engineer. It is adapted from
`../autoresearch-for-agents` and gives us a frozen tool-calling agent plus
adversarial cases for testing whether Eval Engineer can use Galileo evidence
well.

## Goal

The first milestone is deliberately small:

1. Run one sample case with `claude-sonnet-4-6`.
2. Log the trace to the Galileo project `eval-engineer`.
3. Use timestamped experiment names such as
   `tool-calling-support-20260512T101500Z`.
4. Confirm traces and metric data can be fetched before expanding to all cases.

## Local Evaluation

```bash
python3 tests/agents/tool-calling-support/eval/evaluate.py --case TC-1
```

## Galileo One-Sample Run

```bash
python3 tests/agents/tool-calling-support/galileo/run_one_sample_experiment.py \
  --case TC-1 \
  --output tests/agents/tool-calling-support/runs/latest.json
```

Generated run outputs belong under `runs/` and are gitignored.
