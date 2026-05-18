# Eval Engineer

Eval Engineer turns generic coding agents like Codex and Claude Code into
Galileo-backed eval engineers.

The idea is simple: coding agents are good at changing code, but AI apps should
not improve by guesswork. They should improve through evidence. Eval Engineer
gives a coding agent the loop it needs to inspect Galileo traces and metrics,
diagnose the failure, make one bounded change, and verify whether the next run
actually improved.

## Why This Matters

AI failures rarely live in source code alone. The important evidence is often in
tool calls, retrieved context, spans, sessions, metric scores, experiment runs,
or production log streams.

A generic coding agent can edit prompts, tools, retrievers, and configs. What it
does not automatically know is:

- which Galileo artifact to inspect first
- which metric is relevant to the failure
- what that metric proves and does not prove
- whether the fix belongs in the prompt, tool schema, retriever, model config,
  guardrail, dataset, or metric setup
- how to verify that a change improved behavior instead of only sounding better

Eval Engineer adds that missing eval discipline as a portable skill.

## How The Loop Works

Eval Engineer is built around a small, repeatable loop:

```text
AI app behavior
    -> Galileo traces and metrics
    -> compact debug packet
    -> diagnosis
    -> bounded fix plan
    -> verification run
    -> keep the change only if evidence improves
```

The skill does not start by editing code. It starts by grounding the problem:

1. Identify whether the evidence came from a controlled experiment, production
   log stream, or mixed source.
2. Read the current debug packet.
3. Name the metric contract.
4. Compare expected behavior with actual trace behavior.
5. Choose the fix surface.
6. Propose the smallest useful change.
7. Verify with a fresh local or Galileo run.

This is the practical path toward self-improving agents: not autonomous
rewriting, but measured change retention.

## What The Skill Adds

The core artifact is the portable skill in
`skills/eval-engineer/`.

The host agent provides repo access, command execution, and code edits. The
skill provides the eval workflow:

- Galileo evidence literacy
- metric selection by failure contract
- root-cause analysis structure
- bounded fix planning
- before/after verification
- durable learnings and candidate eval cases

The skill is intentionally general. The first fixture is a tool-calling support
agent, but Eval Engineer is meant to work across agents, RAG apps, workflows,
providers, experiments, log streams, and custom metrics.

## Install And Start

Install Eval Engineer into the project you want to debug or improve:

```bash
uvx --from git+https://github.com/Galileo-Agent-Labs/eval-engineer.git \
  eval-engineer install --target both --scope project --project-dir .
```

Project install writes skills into `.agents/skills/eval-*` for Codex and
`.claude/skills/eval-*` for Claude Code. It also prepares a minimal `.galileo/`
workspace without overwriting existing files.

Start a new Claude Code or Codex session from this same project folder after
installing. Codex discovers project skills from `.agents/skills` in the current
directory and its parents; if Codex was opened somewhere else, it will not see
this project's skills.

Claude Code surfaces the skills as slash commands:

```text
/eval-engineer   front door, readiness check, router, and short explanation
/eval-setup      prepare or inspect the .galileo workspace
/eval-fetch      turn Galileo URLs/IDs into local debug packets
/eval-measure    choose metrics and expected-output contracts
/eval-diagnose   perform RCA from traces, spans, sessions, and metrics
/eval-cost       reduce cost while protecting quality metrics
/eval-audit      review launch, safety, OWASP, and coverage risk
```

Codex surfaces the same skills as `$` mentions:

```text
$eval-engineer   front door, readiness check, router, and short explanation
$eval-setup      prepare or inspect the .galileo workspace
$eval-fetch      turn Galileo URLs/IDs into local debug packets
$eval-measure    choose metrics and expected-output contracts
$eval-diagnose   perform RCA from traces, spans, sessions, and metrics
$eval-cost       reduce cost while protecting quality metrics
$eval-audit      review launch, safety, OWASP, and coverage risk
```

If the skills do not appear, restart the host agent. For Codex, also confirm the
skills were installed under the project you opened:

```bash
find .agents/skills -maxdepth 2 -name SKILL.md | sort
```

The first useful prompt is usually:

```text
$eval-engineer inspect this project and tell me the best next step.
```

In Claude Code, use `/eval-engineer` instead. If you already have Galileo
evidence, start with the artifact you have:

```text
$eval-fetch https://console.demo-v2.galileocloud.io/.../log-streams/...
$eval-diagnose .galileo/current/debug-packet.json
$eval-cost compare the baseline and verification packets
```

See `docs/installation.md` for user-scope installs, detailed command behavior,
and plugin packaging guidance.

## A Small Example

In the first reference loop, a support agent selected the wrong tool for a user
request. Galileo exposed the failure with `tool_selection_quality`.

The first instinct was to improve the prompt. That helped locally, but the
Galileo runs showed the behavior was still unstable. The evidence pointed to a
different fix surface: the runtime tool contract was too loose.

The durable fix combined:

- a narrow policy-derived tool availability gate
- preservation of enum schemas in the tool adapter
- disabling parallel tool calls for that runner

After the fix, the relevant Galileo experiment returned
`average_tool_selection_quality: 1.0`.

That did not mean the whole agent was solved. It meant the tool-selection metric
had done its job. A new gap appeared: the final answer could still need better
policy-quality evaluation. That becomes the next eval.

This is the core Eval Engineer pattern:

```text
metric exposes failure
    -> evidence points to fix surface
    -> bounded change
    -> metric improves
    -> remaining gap becomes the next eval
```

## What Lives In This Repo

This repo contains the first draft of that workflow:

- `skills/eval-engineer/` is the portable skill.
- `.galileo/` is the local evidence working set used by the skill.
- `tests/agents/tool-calling-support/` is the first reference fixture.
- `tests/skills/` checks that the skill stays general and does not overfit to
  the first fixture.
- `docs/` tracks the current plan, tasks, and progress.
- `notes/` and `blogs/` preserve the product thinking behind the work.

The key design choice is separation of concerns. Galileo stores behavior
evidence. The coding agent edits the repo. The skill connects them through a
repeatable eval loop.

## Direction

The next step is to expand from the first tool-calling fixture into RAG and
production log-stream RCA. The product shape should stay the same: read
evidence, diagnose precisely, change one thing, verify with metrics, and keep
only what measurably improves.
