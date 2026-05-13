# Eval Engineer

Eval Engineer is a Galileo evidence workflow for improving AI agents, RAG apps,
and future AI systems. The repo is currently proving one tight loop:

1. run a reference AI app
2. log traces and metrics to Galileo
3. fetch compact evidence
4. diagnose the failure
5. make a bounded change
6. verify the next run with local and Galileo evidence

The long-term goal is to make this loop reusable as a portable skill for Codex,
Claude Code, and similar coding agents.

## Repo Map

```text
.
|-- AGENTS.md                         # repo-local operating instructions
|-- docs/                             # plan, tasks, and progress tracking
|-- requirements.txt                  # pinned SDK/runtime dependencies
|-- .galileo/                         # current Galileo working set
|-- skills/galileo-eval-engineer/     # canonical portable skill
|-- tests/agents/tool-calling-support/ # first reference agent fixture
|-- tests/skills/                     # deterministic skill tests
|-- notes/                            # dated build notes for future writing
`-- blogs/                            # product thinking and draft narratives
```

Read these first when joining the repo:

- `AGENTS.md` for workflow rules and active Linear hygiene.
- `docs/plan.md` for product intent.
- `docs/tasks.md` for the current work breakdown.
- `docs/progress.md` for the latest evidence and next move.
- `.galileo/learnings.md` for durable Galileo debugging patterns.

## Main Areas

### `docs/`

Planning and status files live here so the repo root stays small.

- `docs/plan.md` is the product and architecture direction.
- `docs/tasks.md` is the implementation checklist and Linear issue mapping.
- `docs/progress.md` is the latest completed work, blocker, and next move.

### `.galileo/`

Repo-local Galileo working state. This is the interface between the portable
skill and the current repo. The skill reads this folder to know what evidence is
current, which files it may edit, which metrics matter, and how to verify a
change.

- `.galileo/config.yml` defines the current app type, metric set, editable
  files, blocked files, source type, and verification commands. Treat it as the
  working-set contract for an Eval Engineer run.
- `.galileo/current/` stores the active debug packet, diagnosis, fix plan, and
  verification plan. This is the default place to look before opening raw
  traces or historical sessions. Use `debug-packet.json` for the baseline or
  active packet and `verification-debug-packet.json` for the after-run packet
  used to verify a fix.
- `.galileo/sessions/` is reserved for historical Galileo evidence. Use it for
  comparisons or history, not for the first pass on a new failure.
- `.galileo/eval-dataset/` stores candidate, accepted, and rejected eval cases.
  Candidate cases should be human-reviewed before promotion.
- `.galileo/index.json` can point tools at the current session or packet.
- `.galileo/learnings.md` stores reusable repo-specific Galileo findings, such
  as metric behavior, SDK quirks, testbed patterns, and RCA patterns.

Keep `.galileo/` focused on evidence and reusable Galileo learnings. Broader
meeting notes, blog ideas, and narrative session notes belong in `notes/`.
Generated current/session evidence is ignored unless intentionally promoted.

### `skills/galileo-eval-engineer/`

The canonical skill package. This is the part intended to become reusable across
agents, RAG apps, workflows, metrics, and providers.

- `SKILL.md` is the entrypoint instruction file.
- `references/` contains durable Galileo mechanics such as experiments, debug
  packets, working sets, and RCA recipes.
- `scripts/` contains deterministic helpers such as debug-packet summarization.
- `assets/` contains diagnosis, fix-plan, and verification-plan templates.
- `agents/openai.yaml` contains Codex/OpenAI skill metadata.

Install links are kept at:

- `.agents/skills/galileo-eval-engineer`
- `.claude/skills/galileo-eval-engineer`

### `tests/agents/tool-calling-support/`

The first reference implementation. It is a frozen support-agent fixture used to
prove the Eval Engineer loop, not the product scope.

Standard shape for future reference implementations:

- `agent/` runnable implementation, prompts, policies, and tool schema
- `cases/` frozen test cases
- `eval/` local deterministic scoring and contract tests
- `galileo/` Galileo experiment runners, metric config, reports, and packets
- `runs/` generated local outputs, ignored by git

### `tests/skills/`

Deterministic tests for the portable skill and helper scripts. These keep the
skill general and prevent it from becoming hardcoded to the first support-agent
fixture.

## Setup

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create a local `.env` from `.env.example` and fill in the required variables:

```bash
cp .env.example .env
```

Required variable names:

- `GALILEO_API_KEY`
- `GALILEO_CONSOLE_URL`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `TOGETHER_API_KEY`

Do not print secret values in logs or notes.

## Common Commands

Run one local support-agent case:

```bash
python3 tests/agents/tool-calling-support/eval/evaluate.py --case TC-1
```

Run all local support-agent cases and save generated output:

```bash
python3 tests/agents/tool-calling-support/eval/evaluate.py \
  --output tests/agents/tool-calling-support/runs/latest-local-all.json
```

Run the LangGraph + Galileo one-sample experiment:

```bash
python3 tests/agents/tool-calling-support/galileo/run_one_sample_langgraph.py \
  --case TC-1 \
  --output tests/agents/tool-calling-support/runs/latest-run-langgraph-anthropic.json \
  --metric-timeout-seconds 180
```

Try Galileo correctness on only the final answer, without sending reference
outputs:

```bash
python3 tests/agents/tool-calling-support/galileo/run_one_sample_langgraph.py \
  --case TC-1 \
  --metrics correctness \
  --dataset-shape case-id-only \
  --output-mode final-only \
  --output tests/agents/tool-calling-support/galileo/runs/tc1-correctness-no-gt.json \
  --metric-timeout-seconds 180
```

Fetch a compact Galileo debug packet for an experiment:

```bash
python3 tests/agents/tool-calling-support/galileo/fetch_debug_packet.py \
  --experiment-name <experiment-name> \
  --output tests/agents/tool-calling-support/galileo/debug-packets/<name>.json
```

Summarize a debug packet:

```bash
python3 skills/galileo-eval-engineer/scripts/summarize_debug_packet.py \
  tests/skills/fixtures/generic-rag-debug-packet.json
```

Run skill verification:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/eval-engineer-pycache \
  python3 -m unittest tests.skills.test_galileo_eval_engineer_skill

python3 /Users/pratik/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/galileo-eval-engineer
```

## Galileo Conventions

- Use Galileo experiments for reference testbeds.
- Use Galileo log streams later for production/live-traffic RCA and for
  discovering failures that should become controlled eval cases.
- Project name: `eval-engineer`.
- Experiment names should include the app name and a UTC timestamp.
- Start with non-Luna metrics unless the workspace explicitly supports Luna.
- Choose metrics by failure mode. Agent/tool metrics are only the default for
  the current tool-calling fixture, not for every Eval Engineer workflow.
- Current support-agent fixture metrics include `agentic_workflow_success`,
  `agentic_session_success`, `tool_selection_quality`, and `tool_error_rate`.
- `correctness` is available and currently surfaces as `average_factuality` in
  fetched aggregate metrics.
- For this installed SDK path, function experiments may need explicit scorer job
  triggering before non-system metrics appear.

## Generated Files

Keep generated runs, raw traces, temporary logs, and `.omc/` out of git.
Important generated evidence can be promoted deliberately into reports or compact
debug packets.

Currently ignored generated areas include:

- `.galileo/current/*`
- `.galileo/sessions/*`
- `tests/agents/**/runs/`
- `tests/agents/**/experiments/`
- `tests/agents/**/.galileo/current/`
- `tests/agents/**/.galileo/sessions/`
- `tests/agents/**/.galileo/raw/`
- `.omc/`

## Current Direction

The first tool-selection loop is working with Galileo evidence. The active next
steps are:

- refine `GAL-87` into a reference-backed or context-backed final-answer check
- add the first RAG reference implementation in `GAL-82`
- keep the skill general across agents, RAG apps, workflows, metrics, and
  providers
