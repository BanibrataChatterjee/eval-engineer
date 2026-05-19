---
name: eval-dataset
description: Use when turning Galileo failures, traces, metric gaps, or production examples into Eval Engineer dataset cases or reviewing candidate cases.
---

# Eval Dataset

Use this skill to build durable eval cases from evidence. Its job is dataset
quality control, not diagnosis or app fixing.

## Required Reference

Use `skills/eval-engineer/references/eval-datasets.md` for the canonical case
schema precedence, optional review metadata, promotion rules, bootstrap
guidance for different use cases, and Galileo SDK dataset usage.

## Required Inputs

Start from at least one evidence source:

- `.galileo/current/debug-packet.json`
- `.galileo/current/diagnosis.md`
- Galileo trace, session, experiment, or log-stream IDs
- production symptom with enough context to define expected behavior

If there is no concrete failure, regression, policy requirement, or metric gap,
ask for evidence before writing a case.

## Do

- Write new unreviewed cases to `.galileo/eval-dataset/candidates.jsonl`
  unless the user asks to accept or reject a case.
- When accepting or rejecting cases, update `.galileo/eval-dataset/changelog.md`.
- Bootstrap datasets by use case: RAG, tool-calling agent, multi-turn,
  workflow, safety/compliance, and tokenomics.
- Choose failure triggers that should be caught by named Galileo metrics or
  explicit local gates.
- Follow the user-provided schema when the user gives one.
- Follow the existing Galileo dataset schema when appending to a fixed dataset.
- Do not force Eval Engineer fields into an upload schema. Put optional review
  metadata in `.galileo/eval-dataset/candidates.jsonl`, `metadata`, or a
  sidecar file when needed.
- Use retrieved-source gates when source authority matters and the chosen
  schema can carry them. Final citations alone are not enough for
  prompt-injection, privacy, stale-source, or source-authority cases.
- When the user wants to upload, reuse, or run cases in Galileo, use the SDK
  workflow in the reference instead of improvising dataset shapes.
- Do not promote candidates without human review.

## Output

State whether the result is candidate, accepted, rejected, or blocked. Include
the target JSONL path, case IDs changed, evidence source, and remaining metric
gaps.
