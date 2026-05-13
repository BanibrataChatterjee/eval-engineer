# Eval Engineer Progress

## 2026-05-12

### Done

- Added `docs/plan.md` and `docs/tasks.md`.
- Added root `AGENTS.md` with repo operating instructions for coding agents
  (`GAL-84`).
- Added dated repo notes under `notes/`.
- Added first reference agent under `tests/agents/tool-calling-support/`.
- Copied the Nexus support agent and 10 frozen cases from
  `../autoresearch-for-agents`.
- Added local deterministic scoring.
- Added Galileo metric config with non-Luna metrics only.
- Added a LangGraph runner using Galileo's LangChain callback integration.
- Found that function-based experiments in `galileo==1.39.0` do not start the
  requested non-system scorer jobs automatically.
- Added an explicit `log_stream_scorer` trigger for `tool_selection_quality`.
- Confirmed `average_tool_selection_quality` appears in fresh runs:
  - OpenAI: `0.3333333432674408`
    (`tool-calling-support-langgraph-20260512T120526Z`).
- Patched the runner to wait for the explicit scorer job before writing
  aggregate metrics.
  - Anthropic: `0.1666666716337204`
    (`tool-calling-support-langgraph-20260512T122334Z`).
- Saved first debug packet:
  `tests/agents/tool-calling-support/galileo/debug-packets/TC-1-anthropic-20260512T122334Z.json`.
- Added first repo-local skill:
  `skills/galileo-eval-engineer/SKILL.md`.
- Added reusable debug-packet skill support:
  `skills/galileo-eval-engineer/scripts/summarize_debug_packet.py` and
  `skills/galileo-eval-engineer/references/debug-packets.md`.
- Reworked the skill away from the first support-agent case and toward the
  general repo-local `.galileo/current/` working-set model described in the blog
  drafts.
- Added `.galileo/config.yml`, `.galileo/learnings.md`, `.galileo/index.json`,
  and reviewed eval-dataset files for future candidate promotion.
- Added deterministic skill checks under
  `tests/skills/test_galileo_eval_engineer_skill.py` so the skill stays general
  and the summarizer handles a non-agent-specific RAG packet.
- Added RCA/discoverability framing to the plan and blog drafts: reduce
  time-to-RCA, improve Galileo discoverability for non-developers, focus on
  log streams/traces/sessions/failure patterns, and ground answers with links or
  stable IDs back to Galileo data.
- Completed `GAL-79` by adding artifact templates for `diagnosis.md`,
  `fix-plan.md`, and `verification-plan.md`, plus deterministic tests for RAG
  and tool-calling debug-packet fixtures.
- Completed `GAL-80` local all-case support-agent eval: 10 cases, overall score
  `0.15`, 1 perfect, 1 partial, 8 zero-score cases. Curated report saved at
  `tests/agents/tool-calling-support/eval/reports/local-all-2026-05-13.md`.
- Started `GAL-81` with representative TC-8 Galileo run. Experiment
  `tool-calling-support-langgraph-20260513T055340Z`
  (`52c5931b-44fa-47ca-9179-107c806228af`) returned only system aggregate
  metrics; `tool_selection_quality` did not populate, and the debug packet
  showed trace `tool_selection_status: error` with 0 scored tool-selection spans.
  Report saved at
  `tests/agents/tool-calling-support/galileo/reports/representative-runs-2026-05-13.md`.
- Completed `GAL-81` with a fresh OpenAI TC-1 Galileo experiment after earlier
  OpenAI runs failed and could not be retriggered. Experiment
  `tool-calling-support-langgraph-20260513T062239Z`
  (`87fca833-ff9e-4ec0-a559-14fd33cad464`) produced fetched
  `average_tool_selection_quality: 0.0`, trace `tool_selection_status: success`,
  and 8 scored tool-selection spans. The debug packet is saved at
  `tests/agents/tool-calling-support/galileo/debug-packets/TC-1-openai-20260513T062239Z.json`.
- Started `GAL-86` as the first diagnose-fix-verify loop. Promoted the TC-1
  packet to `.galileo/current/debug-packet.json`, wrote current diagnosis,
  fix-plan, and verification-plan artifacts, and updated the support-agent
  system prompt with a general jurisdiction/payment-routing checklist rather
  than fixture-specific instructions.
- Completed `GAL-86`. Prompt-only and tool-description-only changes improved
  local behavior but remained unstable in OpenAI/Galileo, so the final fix added
  a narrow policy-derived tool availability gate, enum preservation for
  LangGraph structured tools, and `parallel_tool_calls=False` for OpenAI. Final
  Galileo experiment `tool-calling-support-langgraph-20260513T065346Z`
  (`88e2b26e-3b10-4a75-a4bc-9d4b9c297d8a`) produced fetched
  `average_tool_selection_quality: 1.0`, trace `tool_selection_status: success`,
  and one `escalate_to_billing` call. Final local all-case score is `0.20`
  versus the `0.15` baseline.
- Started the generalized Galileo RCA recipe in
  `skills/galileo-eval-engineer/references/rca-recipe.md`. The recipe captures
  the reusable loop from the first diagnose-fix-verify run: fetched packets as
  source of truth, metric-contract scoping, expected-vs-actual comparison, fix
  surface classification, before/after Galileo proof, and durable learning
  capture.
- Added `skills/galileo-eval-engineer/agents/openai.yaml` and validated the
  skill with `quick_validate.py`.
- Created Galileo project `eval-engineer`
  (`160fb99e-a0a7-4726-a7e2-6a2beb1c765f`).
- Created timestamped Galileo experiments.
- Moved `plan.md`, `tasks.md`, and `progress.md` under `docs/` to keep the
  root clean.
- Removed overlapping `memories/` content; use `notes/` for dated narrative
  notes and `.galileo/learnings.md` for reusable Galileo debugging patterns.
- Expanded the 2026-05-13 notes with the skill architecture decisions: skills
  as portable eval-loop contracts, `.galileo/` as evidence workspace,
  experiments versus log streams, metric selection by failure contract, RCA
  templates, debug-packet naming, and tests for the skill itself (`GAL-89`).
- Drafted `blogs/skills-robust-eval-loop.md`, a blog on how skills add a
  Galileo-backed eval loop to generic Codex and Claude workflows (`GAL-89`).
- Ran a TC-1 Anthropic correctness-without-ground-truth trial for `GAL-87`:
  `tool-calling-support-correctness-no-gt-20260513T071203Z`
  (`b9e4b120-66f8-4b4a-acb6-e57addb68ace`). The runner sent only
  `case_id` as dataset input and returned only the final answer as output.
  Galileo returned `average_factuality: 0.0`; the explicit scorer job failed
  with the known missing `inputs.feather` artifact error, but the aggregate
  metric was still available. Debug packet saved at
  `tests/agents/tool-calling-support/galileo/debug-packets/TC-1-anthropic-correctness-no-gt-20260513T071203Z.json`.
- Created Linear issues:
  - `GAL-73`: one-sample Galileo metric gate.
  - `GAL-74`: reference agent testbed cleanup.
  - `GAL-75`: Galileo skill evidence reference.
  - `GAL-76`: obsolete model-availability follow-up.
  - `GAL-77`: reference-agent TC-1 verification follow-up.
  - `GAL-78`: completed general skill working-set correction.
  - `GAL-79`: behavioral fixture tests for Eval Engineer outputs.
  - `GAL-80`: completed all-case local support-agent eval.
  - `GAL-81`: completed representative Galileo support-agent eval.
  - `GAL-86`: completed first diagnose-fix-verify loop from TC-1 Galileo evidence.
  - `GAL-87`: answer correctness follow-up for policy explanations.
  - `GAL-88`: completed first generalized Galileo RCA recipe.
  - `GAL-89`: completed skills eval-loop notes and blog.
  - `GAL-82`: first RAG reference implementation.
  - `GAL-84`: completed root `AGENTS.md` repo operating instructions.
  - `GAL-85`: completed RCA and Galileo discoverability framing.

### Current Blocker

The `tool_selection_quality` metric and trace-fetch gates are now passed.
`claude-sonnet-4-6` is the canonical Anthropic model for the reference agent.
The skill is now framed as a general Galileo evidence and RCA workflow. The
first diagnose-fix-verify loop is complete for tool selection. A first
correctness-without-ground-truth trial works mechanically and returns
`average_factuality`, but it is a coarse answer-quality signal without a
reference or context rubric.

### Next Move

Start `GAL-82`: add the first RAG reference implementation with the same
standard structure as the support-agent fixture, including local evals, Galileo
experiment config, and debug-packet fetch support. Separately, refine `GAL-87`
into a reference-backed or context-backed policy-answer metric instead of using
bare correctness as the only signal.
