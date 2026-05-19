# Eval Engineer Plan

## Vision

Eval Engineer is the path from Galileo evidence to self-improving agents. The
first version should prove a small loop: run an agent, log the behavior to
Galileo, fetch traces and metrics, diagnose what failed, propose a bounded
change, and verify whether the next run improved.

The immediate product goal is to reduce time-to-RCA for agent builders and
owners. Eval Engineer should help users move from "something is wrong" to a
grounded explanation of what failed, where it failed, which traces/sessions show
it, which metrics support the claim, and what should be checked next.

It should also increase Galileo discoverability for non-developer personas. A
PM, support lead, solutions engineer, or agent owner should be able to ask
RCA-shaped questions and get useful Galileo-backed answers without already
knowing which log stream, trace view, session, metric, or experiment comparison
to open.

## First Goal

Wire Galileo well using one sample from one reference agent. Before building a
large skill, we need confidence that experiments, traces, metrics, and fetched
evidence work end to end.

The first sample is a validation fixture, not the product shape. The skill must
be general enough to work across tool-calling agents, RAG apps, workflows,
custom metrics, and future Galileo evidence packets. Until the one-sample gate
passes, do not expand the reference testbed; after it passes, keep skill logic
organized around Galileo concepts rather than that one fixture.

The first product workflows should be RCA workflows:

- Query relevant log streams and experiments.
- Inspect traces, spans, and sessions.
- Identify recurring failure patterns.
- Compare behavior over time or across before/after runs.
- Return grounded answers with links or IDs back to the underlying Galileo data:
  traces, spans, sessions, metrics, datasets, and experiments.

## Reference Agent

The first implementation lives in `tests/agents/tool-calling-support/`. It uses
the Nexus support-agent cases from `../autoresearch-for-agents`, runs the agent
with `claude-sonnet-4-6`, and starts with a single sample case, `TC-1`.

Each future agent or RAG implementation should follow the same standard shape:

- `agent/` for runnable implementation and prompts.
- `cases/` for frozen test cases.
- `eval/` for local deterministic scoring.
- `galileo/` for project, experiment, and metric configuration.
- `runs/` for generated outputs, ignored by git.

## Galileo Strategy

Use Galileo experiments, not production log streams, for the reference testbeds.
The project name is `eval-engineer`. Experiment names should include the agent
name and UTC timestamp, for example `tool-calling-support-20260512T101500Z`.

Use the official experiment path from the SDK examples:

- Pass one dataset row to `run_experiment`.
- Pass one runner function that executes the reference agent.
- Run the agent through LangGraph and Galileo's LangChain callback integration.
- Pass preset metrics using `GalileoMetrics` constants where the installed SDK
  exposes them.
- For function-based experiments in this installed SDK, explicitly trigger a
  `log_stream_scorer` job for `tool_selection_quality` after traces are flushed.
- Poll `get_experiment` until the expected aggregate metric keys appear.

Metric configuration starts with non-Luna agent/tool metrics:

- `agentic_workflow_success`
- `agentic_session_success`
- `tool_selection_quality`
- `tool_error_rate`

Do not use Luna metrics for the initial reference path. The Galileo metrics docs split normal preset
metrics and Luna-2 metrics into separate families, and this workspace does not
have Luna metrics available.

The skill should store Galileo operating knowledge in `skills/` reference files,
not in scattered scripts. Scripts can implement deterministic evidence
summaries, imports, and validation, but the skill references should explain what
evidence to read and how to reason about it generally.

## Skill Strategy

The skill is one canonical portable package that can be installed for Codex and
Claude. It should read a repo-local working set under `.galileo/`, not hardcode
one reference implementation:

- `.galileo/config.yml` defines agent type, metrics, editable files, blocked
  files, and verification commands.
- `.galileo/current/` contains the current debug packet, diagnosis, fix plan,
  and verification plan.
- `.galileo/sessions/` stores historical runs.
- `.galileo/eval-dataset/` stores candidate, accepted, and rejected eval cases.
- `.galileo/learnings.md` stores reusable repo-specific patterns.

The skill's durable value is Galileo literacy: datasets, metrics, experiments,
traces, spans, custom metrics, and run comparison. It should not over-teach
generic debugging or encode a static failure taxonomy.

Every diagnosis artifact should preserve evidence links. If the skill claims a
failure pattern, it should name the supporting traces/sessions/spans, cite the
metric values, and include the Galileo URL or stable ID when available.

## Success Criteria

- A Galileo project named `eval-engineer` exists.
- The support agent defaults to `claude-sonnet-4-6`.
- One `TC-1` support-agent sample can run with `claude-sonnet-4-6`.
- The sample creates a timestamped Galileo experiment.
- The run returns at least one expected aggregate key for
  `tool_selection_quality` or `tool_error_rate`.
- Generated local outputs are ignored by git.
- The repo has `docs/plan.md`, `docs/tasks.md`, `docs/progress.md`, dated
  notes, and `.galileo/learnings.md` so future iterations preserve what we
  learn without cluttering the root.
- The skill works from `.galileo/current/` and does not assume one test case,
  provider, architecture, or metric.
- RCA outputs include grounded evidence references back to traces, spans,
  sessions, metrics, datasets, or experiments.

## Progress So Far

- Created Galileo project `eval-engineer`
  (`160fb99e-a0a7-4726-a7e2-6a2beb1c765f`).
- Created timestamped experiments, including
  `tool-calling-support-20260512T110153Z`.
- Added a LangGraph runner using Galileo's `GalileoCallback`, matching the SDK
  example integration path.
- Latest LangGraph/OpenAI run:
  `tool-calling-support-langgraph-20260512T120526Z`
  (`d8530c37-c557-42f8-a0e9-69c5def4452c`) returned
  `average_tool_selection_quality: 0.3333333432674408`.
- Latest verified LangGraph/Anthropic run:
  `tool-calling-support-langgraph-20260512T122334Z`
  (`7b4360d8-d868-4582-a726-3637624bcc19`) returned
  `average_tool_selection_quality: 0.1666666716337204`.
- Saved the first compact debug packet at
  `tests/agents/tool-calling-support/galileo/debug-packets/TC-1-anthropic-20260512T122334Z.json`.
- The first metric and trace-fetch gates are now passed for `tool_selection_quality`.
- `claude-sonnet-4-6` is the canonical Anthropic model for this reference
  implementation.
- Drafted the first repo-local diagnose/fix/verify skill at
  `skills/eval-engineer/SKILL.md`.
- Reworked the skill to use the general `.galileo/` working-set model from the
  blog drafts rather than hardcoded support-agent case instructions.
- Linear tracking:
  - `GAL-73`: one-sample Galileo metric gate.
  - `GAL-74`: reference agent testbed cleanup.
  - `GAL-75`: Galileo evidence reference for the skill.
  - `GAL-76`: closed as obsolete after confirming `claude-sonnet-4-6` is the
    intended model.
