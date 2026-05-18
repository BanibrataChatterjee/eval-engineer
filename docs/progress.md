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
  `skills/eval-engineer/SKILL.md`.
- Added reusable debug-packet skill support:
  `skills/eval-engineer/scripts/summarize_debug_packet.py` and
  `skills/eval-engineer/references/debug-packets.md`.
- Reworked the skill away from the first support-agent case and toward the
  general repo-local `.galileo/current/` working-set model described in the blog
  drafts.
- Added `.galileo/config.yml`, `.galileo/learnings.md`, `.galileo/index.json`,
  and reviewed eval-dataset files for future candidate promotion.
- Added deterministic skill checks under
  `tests/skills/test_eval_engineer_skill.py` so the skill stays general
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
  `skills/eval-engineer/references/rca-recipe.md`. The recipe captures
  the reusable loop from the first diagnose-fix-verify run: fetched packets as
  source of truth, metric-contract scoping, expected-vs-actual comparison, fix
  surface classification, before/after Galileo proof, and durable learning
  capture.
- Added `skills/eval-engineer/agents/openai.yaml` and validated the
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
- Reworked the main `README.md` to lead with the Galileo-backed eval loop,
  explain why the skill matters for Codex and Claude workflows, show the
  debug-packet flow, and use version-neutral project language (`GAL-90`).
- Trimmed `README.md` again so it focuses on why Eval Engineer exists, how the
  eval loop works, what the skill adds, and one concrete example instead of
  setup and repo-maintenance detail (`GAL-91`).
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
  - `GAL-90`: completed README framing and draft wording cleanup.
  - `GAL-91`: completed README narrative cleanup.
  - `GAL-93`: Eval Engineer launch blog.
  - `GAL-94`: Eval Engineer launch graphics.
  - `GAL-95`: completed Galileo tokenomics RCA sub-skill.
  - `GAL-82`: completed first RAG reference implementation.
  - `GAL-96`: completed second reference implementation for the tokenomics loop.
  - `GAL-97`: completed policy RAG Galileo log streams and metrics.
  - `GAL-98`: completed policy RAG tokenomics cost-reduction loop.
  - `GAL-99`: completed tokenomics skill improvements from the policy RAG loop.
  - `GAL-100`: completed tokenomics robustness tests across use cases.
  - `GAL-101`: completed broader tokenomics robustness across RAG, agent,
    model-routing, evaluator-cost, and segment-regression scenarios.
  - `GAL-102`: completed May 14 learning capture in repo notes.
  - `GAL-84`: completed root `AGENTS.md` repo operating instructions.
  - `GAL-85`: completed RCA and Galileo discoverability framing.

## 2026-05-14

### Done

- Created launch-package Linear issues and moved them to In Progress:
  - `GAL-93`: Eval Engineer launch blog.
  - `GAL-94`: Eval Engineer launch graphics.
- Completed `GAL-95` by adding tokenomics RCA as a sub-workflow inside
  `skills/eval-engineer/`. The addition includes
  `references/tokenomics-rca.md`, cost diagnosis/fix/quality-preserving
  verification templates, `scripts/compare_tokenomics_packets.py`, and tests.
  The helper compared the current TC-1 baseline and verification packets as a
  keep-candidate: `average_cost` decreased about 41%, `average_latency`
  decreased about 80%, `average_num_total_tokens` decreased about 41%, and
  `average_tool_selection_quality` improved from `0.0` to `1.0`.
- Completed `GAL-96` / `GAL-82` by adding a deterministic policy RAG reference
  implementation under `tests/agents/policy-rag/` with wide and focused
  retrieval modes, three policy-answer cases, local scoring, and local
  tokenomics estimates.
- Completed `GAL-97` by creating Galileo log streams for both policy RAG modes:
  `policy-rag-tokenomics-wide-v2-20260514T1505Z`
  (`b31b8f3b-89a0-4ccc-ae46-25db867b8b47`) and
  `policy-rag-tokenomics-focused-v2-20260514T1505Z`
  (`99d60440-7862-4602-9dac-3529f14e5d01`). Enabled
  `context_adherence`, `context_relevance`, and `completeness`.
- Completed `GAL-98` by using the tokenomics RCA helper to compare fetched
  Galileo packets. Focused retrieval reduced `average_cost` by about 41%,
  `average_num_input_tokens` by about 58%, `average_num_total_tokens` by about
  53%, and `average_latency` by about 52%, while
  `average_completeness_gpt`, `average_groundedness`, and
  `average_context_relevance` stayed at `1.0`.
- Completed `GAL-99` by folding the policy RAG loop back into the skill
  artifacts: small cost values now render with significant digits in
  `compare_tokenomics_packets.py`, the policy RAG fetcher aggregates
  tokenomics metrics from fetched traces/spans, and the durable learning notes
  now require Galileo quality gates for tokenomics changes.
- Recorded the policy RAG tokenomics RCA at
  `tests/agents/policy-rag/galileo/reports/tokenomics-rca-2026-05-14.md`.
- Completed `GAL-100` after reviewing whether the policy RAG tokenomics test was
  sufficient. The review found it was too happy-path-heavy: it did not cover
  lower-is-better quality metrics such as `tool_error_rate`, quality regression
  rejection, or traffic-volume-only comparisons. Added failing pressure tests
  for those cases before patching the comparison helper.
- Improved `compare_tokenomics_packets.py` for `GAL-100`: it now records quality
  metric direction, treats `tool_error_rate`-style metrics as lower-is-better,
  rejects cost wins that increase lower-is-better quality metrics, and does not
  keep a candidate when only `total_responses` drops without efficiency evidence.
- Completed `GAL-101` by adding curated tokenomics pressure scenarios under
  `tests/skills/fixtures/tokenomics-scenarios.json` and broadening the compare
  helper beyond the policy RAG happy path. The new coverage includes agent
  tool/retry-loop efficiency, RAG pruning quality regression, evaluator-cost
  sampling, model-routing span reduction, and hidden segment-level quality
  regression despite aggregate quality holding.
- `compare_tokenomics_packets.py` now recognizes broader efficiency metrics
  such as span counts, tool-call counts, retry counts, retrieved context tokens,
  evaluator cost, sampling rate, and model span counts. It also compares shared
  segment quality metrics and rejects candidates with segment regressions.
- Completed `GAL-102` by expanding
  `notes/2026-05-14/launch-and-skill-expansion.md` with the day's durable
  learnings: launch framing, keeping Linear out of the user-facing operating
  model, tokenomics evidence contracts, policy RAG live log-stream evidence,
  why the first focused retrieval attempt failed, why curated packet fixtures
  matter, and the broader robustness model across RAG, agents, model routing,
  evaluator sampling, and segments.
- Completed `GAL-103` by making the policy RAG fixture harder with six cases,
  including multi-source enterprise refund, legal-hold export, and promotional
  trial-extension denial cases. The naive `focused` candidate cut average cost
  by about 52% but was rejected because local answer quality dropped from `1.0`
  to `0.8111` and segments such as enterprise refund regressed. The `balanced`
  candidate cut average cost by about 44%, input tokens by about 62%, and total
  tokens by about 56% while preserving all hard-suite quality segments at
  `1.0`.
- Created hard-suite Galileo log streams:
  `policy-rag-hard-wide-20260514T1640Z`
  (`3828b1e4-3eb3-4f35-b805-372a3de1dd43`),
  `policy-rag-hard-focused-20260514T1640Z`
  (`1180ffc1-dc66-4673-ba0b-052a00326db3`), and
  `policy-rag-hard-balanced-20260514T1640Z`
  (`6f54d537-f2b4-4edd-988e-c763e7f8d1ce`).
- Added hard-suite curated tokenomics fixtures:
  `hard-wide-baseline-debug-packet.json`,
  `hard-focused-risky-debug-packet.json`, and
  `hard-balanced-verification-debug-packet.json`.
- Updated the tokenomics skill reference, repo agent instructions, Galileo
  learnings, policy RAG README, RCA report, and May 14 notes with the new rule:
  RAG retrieval pruning needs hard multi-source or multi-hop evidence before a
  cost win is accepted.

### Current Blocker

No current blocker for the policy RAG tokenomics loop. The next open product
work is launch content, live non-RAG agent tool-loop tokenomics evidence, and
stronger policy-answer metrics beyond bare correctness.

### Next Move

Draft `GAL-93` and `GAL-94` for the launch package while keeping the
user-facing Eval Engineer operating model independent of any specific task
tracker. Separately, refine `GAL-87` into a reference-backed or context-backed
policy-answer metric instead of using bare correctness as the only signal, and
plan a live agent tool-loop run for the broader tokenomics skill scenarios.

## 2026-05-15

### Done

- Completed `GAL-104` by adding a realistic agentic RAG case-resolution fixture
  under `tests/agents/agentic-rag/`. The fixture includes cached embeddings,
  account lookup, ticket search, audit-log inspection, embedding retrieval,
  reranking, self-checking, structured decisions, and deterministic scoring
  across the initial eight hard cases.
- Created final Galileo log streams with cached OpenAI embeddings:
  `agentic-rag-baseline-safe-20260515T1024Z`
  (`a43a6f1a-d7fb-4335-ad69-5a9bfd07927c`),
  `agentic-rag-cheap-unsafe-20260515T1024Z`
  (`929bdd8e-bc5f-4a29-ac2c-8ecc6a50bcbe`), and
  `agentic-rag-adaptive-20260515T1024Z`
  (`214f2b90-72a4-4e0e-81ae-b096e2fd612c`).
- Initial tokenomics result: `cheap_unsafe` cut average cost by about 68% but
  was rejected because average case success dropped from `1.0` to `0.25`.
  `adaptive` cut average cost by about 22% while preserving the named quality
  gates at `1.0`.
- Improved the tokenomics comparison helper and skill reference so agentic
  efficiency fields such as `agent_steps`, `rerank`, `planner`, `reflection`,
  and `self_check` are treated as first-class efficiency evidence.
- Completed `GAL-105` by expanding the agentic RAG fixture from 8 to 14 cases
  to cover unclear export,
  malicious credential social engineering, PII disclosure, brand-damage,
  multi-source information integration, and counterfactual untrusted context.
- Tightened the Galileo metric contract for the agentic RAG fixture:
  `context_adherence`, `chunk_attribution_utilization`, `correctness`,
  `ground_truth_adherence`, `agent_efficiency`, `agent_flow`, PII, toxicity,
  and tone metrics are now represented in the case metric profiles.
- Updated the log-stream runner to attach the full expected-output contract to
  `dataset_output` for each case instead of a generic quality-contract string.
- Rebuilt the curated agentic RAG tokenomics packets for the expanded 14-case
  suite. The risky `cheap_unsafe` candidate now cuts cost by about 70% but
  drops case success to `0.142857`; the `adaptive` candidate cuts cost by about
  22%, total tokens by about 23%, and retrieved context tokens by about 28%
  while preserving all named quality gates at `1.0`.
- Ran the expanded Galileo log-stream pass after a one-case metric-profile
  smoke test:
  `agentic-rag-metric-profile-smoke-20260515T1100Z`
  (`af5c80cc-a56f-4de5-b64b-155836eaa8ab`),
  `agentic-rag-tokenomics-baseline_safe-20260515T105324Z`
  (`0f13cd38-01a7-4bcf-a1f8-77ac7720e62c`),
  `agentic-rag-tokenomics-cheap_unsafe-20260515T105348Z`
  (`66479ff0-e0fa-4129-a2bf-df73a017898f`), and
  `agentic-rag-tokenomics-adaptive-20260515T105434Z`
  (`beb56226-8525-4cb7-9038-391c49d5e263`).
- Hardened the local embedding cache against partial JSON reads and atomic
  writes after parallel fixture regeneration exposed a shared-cache race.
- Completed `GAL-106` by adding a reusable metric-profile checklist and
  template inside the Eval Engineer skill. Future tokenomics/RAG/agent work now
  has an explicit pre-optimization gate for `risk_profile`,
  `quality_dimensions`, `galileo_metrics`, expected-output contracts,
  quality/safety/performance/cost metrics, segment-level acceptance gates, and
  metric gaps.
- Recorded the RCA at
  `tests/agents/agentic-rag/galileo/reports/tokenomics-rca-2026-05-15.md` and
  notes at `notes/2026-05-15/agentic-rag-tokenomics.md`.

### Current Blocker

No blocker for the agentic RAG tokenomics loop.

### Next Move

Use the expanded agentic RAG fixture as the main demo substrate for the
tokenomics skill. Next, fetch scored Galileo metric results for the expanded
log streams when scorer jobs settle. Consider a small live-generation lane
later for final-answer prose variance.

## 2026-05-18

### Done

- Created and completed `GAL-107` for the Eval Engineer skill installer.
- Added the `eval-engineer` Python CLI with `install` and `check`
  commands, packaged through `pyproject.toml` for `uvx --from ...` usage.
- Kept `skills/eval-engineer/` as the single canonical skill source and
  packaged that folder into the installer at build time.
- Added project-scope installs for Codex at
  `.agents/skills/eval-engineer` and Claude Code at
  `.claude/skills/eval-engineer`.
- Added user-scope installs for Codex at
  `~/.agents/skills/eval-engineer` and Claude Code at
  `~/.claude/skills/eval-engineer`.
- Documented the skill-first path in `docs/installation.md`: use `uvx` now,
  then package separate Codex and Claude plugins later if marketplace,
  versioned team/community distribution, hooks, MCP servers, or app
  integrations justify it.
- Created `GAL-108` as the Backlog follow-up for separate Codex and Claude
  plugin packaging.

### Verification

- `PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 -m unittest tests.installer.test_install_cli`
- `PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 -m unittest tests.skills.test_eval_engineer_skill`
- `python3 /Users/pratik/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/eval-engineer`
- `PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 -m unittest discover -s tests/skills -p 'test_*.py'`
- `PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache python3 -m unittest discover -s tests/installer -p 'test_*.py'`
- `uvx --from /Users/pratik/Documents/github/eval-engineer eval-engineer install --target both --scope project --project-dir /tmp/eval-engineer-uvx-install.o704Of/sample-project`
- `uvx --from git+file:///tmp/eval-engineer-git-url.gCFsUu/repo eval-engineer install --target both --scope project --project-dir /tmp/eval-engineer-git-url.gCFsUu/project`

### Current Blocker

The public GitHub command is implemented and verified through local and
git-style `uvx` installs. It becomes usable from the live GitHub URL after this
branch is pushed or merged with `pyproject.toml` and the installer package.

### Next Move

Publish this branch so users can run the documented GitHub URL directly. Keep
plugin packaging as `GAL-108` unless we need marketplace installation or bundled
MCP/app/hook behavior.

### Rename Follow-Up

- Completed `GAL-109` by renaming the public skill id to `eval-engineer`
  before release.
- Updated the canonical skill source, Codex and Claude symlinks, installer
  destination names, docs, and tests.
- Kept only `eval-engineer` as the CLI command because the installer has not
  been released yet.
- Verified a `uvx --from /Users/pratik/Documents/github/eval-engineer
  eval-engineer install` run in a throwaway project.
- Verified a git-style install with
  `uvx --from git+file://<tmp-repo> eval-engineer install --target both
  --scope project --project-dir <tmp-project>`.
