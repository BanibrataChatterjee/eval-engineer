# Eval Engineer v0.1 Tasks

## Milestone 1: Planning and Notes

- [x] Add `docs/plan.md` with the v0.1 direction.
- [x] Add `docs/tasks.md` with implementation milestones.
- [x] Add dated repo notes under `notes/`.
- [x] Pin SDK dependencies and add reusable env loading.
- [x] Add root `AGENTS.md` with repo operating instructions (`GAL-84`).
- [x] Add RCA/discoverability goal to plan, blogs, and agent instructions (`GAL-85`).
- [x] Move plan, tasks, and progress into `docs/` to keep the repo root clean.
- [x] Remove overlapping `memories/` notes in favor of `notes/` and `.galileo/learnings.md`.
- [x] Capture skills-as-eval-loop notes and draft the Codex/Claude blog
  (`GAL-89`).

## Milestone 2: Reference Agent

- [x] Create `tests/agents/tool-calling-support/`.
- [x] Copy the support-agent implementation and cases from `../autoresearch-for-agents`.
- [x] Set the agent default model to `claude-sonnet-4-6`.
- [x] Add deterministic local scoring for one or many cases.
- [x] Confirm `TC-1` runs successfully against `claude-sonnet-4-6`.

## Milestone 3: Galileo One-Sample Wire-Up

- [x] Add Galileo metric configuration for agent experiments.
- [x] Remove Luna metrics from the first metric configuration.
- [x] Include `tool_selection_quality` in the first metric configuration.
- [x] Add a one-sample Galileo runner.
- [x] Add a `run_experiment`-based one-sample runner following SDK examples.
- [x] Add a LangGraph runner using Galileo's LangChain callback integration.
- [x] Create or reuse the Galileo project `eval-engineer`.
- [x] Run `TC-1` into a timestamped Galileo experiment.
- [x] Capture current blocker: aggregate metrics only returned `average_cost`.
- [x] Replace string metric inputs with `GalileoMetrics` constants where exposed by SDK.
- [x] Align the LangGraph runner with the SDK example metric set:
  `agentic_workflow_success`, `agentic_session_success`,
  `tool_selection_quality`, `tool_error_rate`.
- [x] Confirm LangGraph traces land in Galileo with system metrics.
- [x] Identify SDK behavior: function experiments upsert scorer settings but
  do not start non-system scorer jobs in the installed SDK path.
- [x] Trigger an explicit `log_stream_scorer` job for
  `tool_selection_quality`.
- [x] Fetch agent/tool aggregate metrics from Galileo:
  `average_tool_selection_quality` or `count_tool_error_rate`.
- [x] Resolve why Galileo experiment scorer jobs are not producing judged
  metrics despite LangGraph traces landing.
- [x] Fetch the logged trace/session data back from Galileo.
- [x] Save a first debug-packet fixture once fetch behavior is confirmed.

## Milestone 3 Linear Tracking

- [x] Create `GAL-73` for the one-sample Galileo metric gate.
- [x] Move `GAL-73` to In Progress.
- [x] Move `GAL-73` to Done after metric and trace evidence gates passed.
- [x] Create `GAL-74` for the reference agent testbed.
- [x] Create `GAL-75` for the Galileo skill reference.
- [x] Close `GAL-76` as obsolete after confirming `claude-sonnet-4-6` is the
  intended model.
- [x] Move `GAL-77` to Backlog as a reference-agent verification follow-up.
- [x] Create and close `GAL-78` for generalizing the skill around `.galileo/`.
- [x] Create `GAL-79` for behavioral fixture tests.
- [x] Create `GAL-80` for all-case local support-agent eval.
- [x] Create `GAL-81` for all-case Galileo support-agent eval.
- [x] Create `GAL-82` for the first RAG reference implementation.
- [x] Create and close `GAL-84` for root `AGENTS.md`.
- [x] Create and close `GAL-85` for RCA and Galileo discoverability framing.
- [x] Create and close `GAL-88` for the first generalized Galileo RCA recipe.
- [x] Create and close `GAL-89` for the skills eval-loop notes and blog.

## Milestone 4: Skill Knowledge

- [x] Add a Galileo experiments reference under `skills/`.
- [x] Update the reference with docs-backed non-Luna metric guidance.
- [x] Draft the first general `SKILL.md` for diagnose-fix-verify.
- [x] Teach the skill to read `.galileo/current/debug-packet.json` before raw traces.
- [x] Add a reusable generic debug-packet summarizer for skill runs.
- [x] Add a debug-packet reference for failure-contract extraction across agents and RAG apps.
- [x] Add a repo-local `.galileo/` scaffold for config, learnings, current evidence, sessions, and eval candidates.
- [x] Add skill UI metadata in `agents/openai.yaml`.
- [x] Keep Galileo SDK details in references and scripts, not in the core skill.
- [x] Teach skill artifacts to preserve grounded Galileo links for RCA workflows.
- [x] Start a generalized Galileo RCA recipe from diagnose-fix-verify learnings.

## Milestone 5: Expand After One Sample Works

- [x] Add behavioral tests that ensure the skill stays general and does not hardcode TC-1.
- [x] Add behavioral tests that check skill output shape against fixtures (`GAL-79`).
- [x] Run all 10 tool-calling support cases locally (`GAL-80`).
- [x] Run representative support-agent cases as Galileo experiments and fetch
  metric/trace debug packets (`GAL-81`).
- [x] Complete the first diagnose-fix-verify loop from TC-1 Galileo evidence
  without hardcoding the fixture (`GAL-86`).
- [x] Try Galileo `correctness` without ground truth for the TC-1 final answer
  and fetch the resulting packet (`GAL-87`).
- [ ] Add the first RAG reference implementation (`GAL-82`).
