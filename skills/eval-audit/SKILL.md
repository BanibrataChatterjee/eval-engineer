---
name: eval-audit
description: Use when reviewing an AI app for launch readiness, safety, security, OWASP agentic AI risks, metric coverage, traceability, or production RCA gaps.
---

# Eval Audit

Use this skill to find risk before changing the app. Audits inspect evidence,
code, metrics, and workflow coverage. Do not fix by default.

## Audit Areas

- OWASP agentic AI risks: control plane, tool permissions, data exposure,
  indirect prompt injection, identity boundaries, approval gates, and unsafe
  autonomy.
- Metric coverage: quality, safety, grounding, cost, latency, tool behavior,
  segment regressions, and missing expected-output contracts.
- Evidence quality: links back to Galileo traces, spans, sessions, log streams,
  experiments, and scorer status.
- Launch readiness: failure cases, rollback criteria, verification commands,
  privacy/PII risks, and production monitoring gaps.

## Secret Handling

Do not read secret values from `.env`, shell history, key files, or credential
stores during an audit. It is okay to report variable names, expected variable
presence, whether `.env` is ignored by git, and whether a project is a git repo.
If values were already exposed in chat, logs, or committed files, recommend
rotation; do not infer compromise merely because a local ignored `.env` exists.

## Output

Produce findings first, ordered by severity. Include evidence references and
the next command: `/eval-measure`, `/eval-fetch`, `/eval-diagnose`, or
`/eval-cost`.
