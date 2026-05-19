---
name: eval-diagnose
description: Use when Galileo evidence is available and the user wants root-cause analysis for failed, low-quality, unsafe, regressed, or unreliable AI app behavior.
---

# Eval Diagnose

Use this skill for evidence-backed RCA once a packet, URL-derived evidence, or
trace/session/log-stream context is available.

## Required Reference

Use `skills/eval-engineer/references/rca-recipe.md`,
`skills/eval-engineer/references/debug-packets.md`, and
`skills/eval-engineer/assets/diagnosis-template.md`.

## Do

- Start from fetched evidence, not source-code guesses.
- Name the failing metric contract and what it proves.
- Inspect traces, spans, sessions, tool calls, retrieval context, and scorer
  status to classify the fix surface.
- Classify the fix surface: prompt, tool schema, adapter, retriever, ranker,
  guardrail, metric, dataset, or SDK wiring.
- Write diagnosis and bounded fix plan only when evidence supports it.
- Honor read-only requests. If the user says read-only, dry run, no edits, or
  "do not edit files", do not write `.galileo/` artifacts. Return the RCA
  inline and include a short "Would write" list for any suggested artifact
  paths.

## Output

Produce `.galileo/current/diagnosis.md` and, when justified,
`.galileo/current/fix-plan.md`. If evidence is insufficient, route to
`/eval-fetch` or `/eval-measure`.
