# Agent Instructions

This file is repo-local guidance for Codex, Claude Code, and other coding
agents working on Eval Engineer. Keep it short and update it whenever the repo
workflow, source-of-truth files, or recurring operating rules change.

## Project Intent

Eval Engineer is a general Galileo evidence workflow for improving AI agents,
RAG apps, and future AI systems. Do not shape the product around the first
support-agent fixture. The support-agent cases are validation fixtures, not the
skill's scope.

The near-term product goal is to reduce time-to-RCA for agent builders and
owners while increasing Galileo discoverability for non-developer personas.
Prefer RCA workflows that query log streams, inspect traces/sessions/spans,
identify failure patterns, compare behavior over time, and return grounded
answers with links or stable IDs back to Galileo data.

The north-star loop is:

1. run the AI app
2. log traces and metrics to Galileo
3. fetch compact evidence
4. diagnose failure
5. propose a bounded fix
6. verify with local and Galileo evidence
7. keep only changes that improve measured behavior

## Read First

- `docs/plan.md`: product direction and architecture.
- `docs/tasks.md`: current task checklist and Linear issue mapping.
- `docs/progress.md`: latest work completed and next move.
- `.galileo/learnings.md`: repo-specific durable learnings.
- `blogs/`: product thinking; useful for design intent, but do not treat as
  runtime instructions.

## Skill Rules

- Canonical skill source: `skills/galileo-eval-engineer/`.
- Codex install link: `.agents/skills/galileo-eval-engineer`.
- Claude install link: `.claude/skills/galileo-eval-engineer`.
- Keep `SKILL.md` general across agents, RAG, workflows, metrics, and providers.
- Keep RCA outputs grounded in trace, span, session, metric, dataset, and
  experiment evidence.
- Use `skills/galileo-eval-engineer/references/rca-recipe.md` for generalized
  diagnose-fix-verify work and update it when a reusable Galileo RCA pattern is
  discovered.
- Keep detailed Galileo mechanics in `skills/galileo-eval-engineer/references/`.
- Keep deterministic helpers in `skills/galileo-eval-engineer/scripts/`.
- Do not hardcode `TC-1`, the Nexus support agent, Brazil, one model, or one
  metric into the general skill.

## Working Set

- `.galileo/config.yml`: agent type, metrics, editable files, verification
  commands.
- `.galileo/current/`: current evidence and working artifacts.
- `.galileo/sessions/`: historical evidence.
- `.galileo/eval-dataset/`: candidate, accepted, and rejected eval cases.
- `.galileo/learnings.md`: durable patterns discovered while working.

Read `.galileo/current/` by default. Do not scan historical raw sessions unless
the user asks for history or comparison.

## Verification

After skill changes, run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 -m unittest tests.skills.test_galileo_eval_engineer_skill
python3 /Users/pratik/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/galileo-eval-engineer
```

For the generic packet summarizer:

```bash
python3 skills/galileo-eval-engineer/scripts/summarize_debug_packet.py tests/skills/fixtures/generic-rag-debug-packet.json
```

Use live model or Galileo calls only when the task explicitly requires runtime
verification. Do not print secret values.

## Linear Hygiene

Keep Linear up to date manually after response completion when task status
changes. There are no repo hooks for this.

- Create Linear issues for new meaningful work.
- Move completed Linear issues to Done.
- Move obsolete issues to Canceled or Backlog with an explanatory comment.
- Keep `docs/tasks.md` issue IDs aligned with Linear.
- Mention the relevant Linear IDs in `docs/progress.md`.

Current active planning issues:

- `GAL-87`: answer-quality check for policy explanation correctness.
- `GAL-82`: add first RAG reference implementation.

## Secrets And Generated Files

- Never print `.env` values. It is okay to list variable names.
- Keep generated runs, raw traces, temporary logs, and `.omc/` out of git.
- Preserve user changes. Do not revert unrelated edits.

## Maintenance Rule

If you discover a new durable workflow rule, repeated mistake, packaging
decision, or verification command, update this `AGENTS.md` in the same change.
