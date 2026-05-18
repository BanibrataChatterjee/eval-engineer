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
- Protect named quality metrics and segment gates.
- Reject cheaper candidates when quality metrics do not regress only in the
  aggregate but fail a segment.
- Treat lower traffic volume as inconclusive unless per-trace efficiency also
  improves.

## Output

State keep/reject/inconclusive. Explain why the cost moved and which quality
metrics do not regress.
