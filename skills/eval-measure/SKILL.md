---
name: eval-measure
description: Use when deciding whether an AI app is measured correctly, choosing Galileo metrics, writing expected-output contracts, or defining eval cases before optimizing.
---

# Eval Measure

Use this skill before optimization or broad fixture work. Its job is to make the
measurement contract explicit.

## Required Reference

Use `skills/eval-engineer/references/metric-profile-checklist.md` and
`skills/eval-engineer/assets/metric-profile-template.md`.

## Do

- Define risk profile and quality dimensions.
- Write the full expected-output contract: expected decision, required and
  forbidden citations, tools, answer constraints, abstention, permissions, and
  safety requirements.
- Include retrieved-source gates when source authority matters:
  `required_retrieved_sources`, `forbidden_retrieved_sources`, and whether
  final citations alone are sufficient for the case risk.
- Prefer independent observations over agent self-reports for safety gates.
  Check answer text, citations, retrieved source IDs, tool calls, and Galileo
  scorers before accepting flags emitted by the app under test.
- Choose Galileo metrics by failure contract, not by one global list.
- Identify metric gaps before accepting a cost or quality change.

## Output

Findings first. Start with the highest-risk metric gaps and the keep/reject/
inconclusive measurement decision, then produce a metric profile or explain
what evidence is missing. Do not improve the app until the expected-output
contract and acceptance gates are clear.
