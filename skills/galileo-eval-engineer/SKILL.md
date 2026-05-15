---
name: galileo-eval-engineer
description: Use when debugging or improving AI agents/RAG apps with Galileo evidence. Reads packets, diagnoses failures, writes bounded fix and verification plans, compares runs, and records learnings.
---

# Galileo Eval Engineer

Use this skill to help a coding agent use Galileo like an eval engineer. The
skill should ground the model in Galileo evidence and repo-local context, not
replace the model's general debugging ability with a fixed failure taxonomy.

## Core Loop

1. **Find the working set.**
   - Prefer `.galileo/current/debug-packet.json`.
   - Treat `.galileo/current/debug-packet.json` as the baseline or active
     packet being diagnosed.
   - Treat `.galileo/current/verification-debug-packet.json` as the optional
     after-change packet used for comparison.
   - Read `.galileo/config.yml` for agent type, editable files, blocked files,
     metrics, and verification commands.
   - Read `.galileo/learnings.md` if it exists.
   - If no current packet exists, use a user-provided packet path or help import
     Galileo evidence before diagnosing.

2. **Summarize evidence before reasoning.**
   - Run:
     `python3 skills/galileo-eval-engineer/scripts/summarize_debug_packet.py <packet>`
   - Use raw traces only when the compact packet is missing required evidence.

3. **Diagnose from Galileo concepts.**
   - Use metrics to identify what degraded.
   - Use traces/spans to identify where behavior diverged.
   - For new eval cases, fixture expansion, or tokenomics work, use
     `references/metric-profile-checklist.md` before changing behavior.
   - For cost, latency, or token-efficiency work, use
     `references/tokenomics-rca.md` and compare cost evidence against quality
     metrics before proposing optimization.
   - Check whether the issue is in the app, the test case, the metric, or the
     Galileo integration before proposing code changes.
   - Use the RCA recipe in `references/rca-recipe.md` to select the smallest
     evidence-backed fix surface.
   - Prefer Galileo-specific reasoning: datasets, metrics, experiments, log
     streams, traces, spans, sessions, custom metrics, and run comparison.
   - Treat experiments as controlled sample evals and log streams as production
     or live-traffic RCA sources.

4. **Write bounded artifacts.**
   - Write or update `.galileo/current/diagnosis.md`.
   - Write or update `.galileo/current/fix-plan.md`.
   - Write or update `.galileo/current/verification-plan.md`.
   - Use the templates in `assets/` for expected artifact shape.
   - Preserve Galileo evidence links or stable IDs in every RCA artifact.
   - Keep edits inside allowed paths from `.galileo/config.yml`.
   - If useful, append a concise general pattern to `.galileo/learnings.md`.

5. **Create candidate eval cases carefully.**
   - Propose candidates only for clear, reusable failures.
   - Avoid duplicates, ambiguous cases, and sensitive data.
   - Write candidates to `.galileo/eval-dataset/candidates.jsonl` only when the
     failure is suitable for human review.

6. **Verify before claiming improvement.**
   - Use exact local and Galileo commands from `.galileo/config.yml` when
     available.
   - Save or reference the after-change packet as
     `.galileo/current/verification-debug-packet.json` when working in the
     current set.
   - Compare the new run against `.galileo/current/debug-packet.json`, the
     verification packet, or a session manifest.
   - Report improved, regressed, and unchanged metrics.
   - A prompt or code diff alone is never proof of improvement.

## Guardrails

- Do not hardcode one reference agent, one dataset, one metric, or one provider.
- Do not scan historical raw sessions unless asked or needed for comparison.
- Do not silently overwrite session evidence.
- Do not use ambiguous packet names such as `debug-packet-after.json`; use
  `verification-debug-packet.json` for after-change evidence in `.galileo/current/`.
- Do not promote eval candidates without human review.
- Do not make broad rewrites when a bounded prompt, tool, retriever, guardrail,
  metric, or dataset fix is enough.
- Do not provide RCA claims without trace, span, session, metric, dataset,
  experiment, or log-stream evidence.

## References

- Working-set structure: `references/working-set.md`
- Debug packet schema and usage: `references/debug-packets.md`
- Galileo evidence sources: `references/galileo-sources.md`
- Galileo metric selection: `references/metrics.md`
- Metric-profile checklist for cases and segments:
  `references/metric-profile-checklist.md`
- Galileo experiment wiring: `references/galileo-experiments.md`
- General RCA recipe: `references/rca-recipe.md`
- Tokenomics RCA for cost, latency, and token reduction:
  `references/tokenomics-rca.md`
- Output artifact templates: `assets/diagnosis-template.md`,
  `assets/fix-plan-template.md`, `assets/verification-plan-template.md`,
  `assets/cost-diagnosis-template.md`,
  `assets/tokenomics-fix-plan-template.md`,
  `assets/quality-preserving-verification-template.md`,
  `assets/metric-profile-template.md`
- Repo plan/status context: `docs/plan.md`, `docs/tasks.md`, `docs/progress.md`
