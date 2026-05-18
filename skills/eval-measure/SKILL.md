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
- Choose Galileo metrics by failure contract, not by one global list.
- Identify metric gaps before accepting a cost or quality change.

## Output

Produce a metric profile or explain what evidence is missing. Do not improve
the app until the expected-output contract and acceptance gates are clear.
