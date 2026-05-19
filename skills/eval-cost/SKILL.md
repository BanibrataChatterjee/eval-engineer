---
name: eval-cost
description: Use when reducing token, latency, model, retrieval, tool-call, rerank, self-check, retry, or evaluator cost while preserving AI app quality metrics.
---

# Eval Cost

Use this skill for tokenomics RCA. Cost changes are accepted only when Galileo
quality metrics do not regress.

## Required Reference

Use `skills/eval-engineer/references/tokenomics-rca.md`,
`skills/eval-engineer/scripts/compare_tokenomics_packets.py`,
`skills/eval-engineer/assets/cost-diagnosis-template.md`,
`skills/eval-engineer/assets/tokenomics-fix-plan-template.md`, and
`skills/eval-engineer/assets/quality-preserving-verification-template.md`.

## Do

- Compare cost, latency, tokens, retrieved context, tool calls, retries,
  rerank/self-check spans, model spans, and evaluator cost.
- Run `compare_tokenomics_packets.py` without explicit quality metrics first
  when packets use custom quality names, then inspect the inferred
  `Quality metrics compared` list before accepting the decision.
- Treat behavior counters such as handoff count, tool count, step count,
  retry count, and self-check count as efficiency or workflow evidence, not
  quality gates by default. Promote one to quality only when the metric profile
  states the desired direction for that route or segment.
- Protect named quality metrics and segment gates.
- Reject cheaper candidates when quality metrics do not regress only in the
  aggregate but fail a segment.
- Treat lower traffic volume as inconclusive unless per-trace efficiency also
  improves.

## Output

State keep/reject/inconclusive first. Explain why the cost moved, which quality
metrics do not regress, and which latency/tool-count tradeoffs remain.
