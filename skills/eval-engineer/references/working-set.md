# Repo-Local Working Set

Eval Engineer should use a small repo-local working set so the coding agent sees
current evidence without mixing stale sessions into the diagnosis.

## Layout

```text
.galileo/
  config.yml
  learnings.md
  index.json
  current/
    debug-packet.json
    verification-debug-packet.json
    diagnosis.md
    fix-plan.md
    verification-plan.md
  sessions/
    <timestamp>_<run-id>/
      manifest.json
      debug-packet.json
      verification-debug-packet.json
      diagnosis.md
      fix-plan.md
      verification-plan.md
      raw/
        traces.json
        metrics.json
  eval-dataset/
    candidates.jsonl
    accepted.jsonl
    rejected.jsonl
    changelog.md
```

## Rules

- `.galileo/current/` is one run and one working set.
- `.galileo/current/debug-packet.json` is the baseline or active packet the
  skill should diagnose first.
- `.galileo/current/verification-debug-packet.json` is the optional after-run
  packet used to prove or reject a fix.
- `.galileo/sessions/` is append-only history.
- `.galileo/index.json` can point to the current session.
- The skill reads `config.yml`, `learnings.md`, and `current/` by default.
- The skill writes diagnosis, fix plan, verification plan, learnings, and
  candidate eval cases.
- The skill should not inspect raw historical traces unless the user asks for
  history or comparison.

## Debug Packet Naming

Use stable names inside `.galileo/current/` so agents do not need to guess:

- `debug-packet.json`: the active failure, baseline run, or packet currently
  being diagnosed.
- `verification-debug-packet.json`: the fresh packet from the verification run
  after a proposed change.

Use descriptive timestamped names outside `.galileo/current/`, for example:

```text
tests/agents/<implementation>/galileo/debug-packets/
  <case>-<provider>-<short-purpose>-<timestamp>.json
```

Examples:

- `CASE-7-provider-baseline-20260513T062239Z.json`
- `CASE-7-provider-after-routing-fix-20260513T065346Z.json`

Avoid vague names such as `debug-packet-after.json`; they do not say what role
the packet plays in the loop.

## Config Fields

Useful `config.yml` fields:

- `project`: Galileo project name.
- `agent_type`: tool-calling, RAG, workflow, chat, or other.
- `source_type`: experiment, log_stream, or mixed.
- `editable_files`: files or globs the skill may change.
- `blocked_files`: files or globs the skill must not change.
- `metrics`: primary Galileo metrics for this app or current eval. Choose these
  from the failure contract, not from the first reference fixture.
- `local_eval_command`: command for local verification.
- `galileo_eval_command`: command for Galileo verification.
- `candidate_eval_path`: where proposed eval cases should be written.

## Learnings Versus Notes

`.galileo/learnings.md` is repo/project-specific Galileo operating memory. Use
it for reusable patterns about this testbed, SDK behavior, metrics, and RCA
workflows.

Use `notes/` for the build story: decisions, surprises, blog seeds, and
developer narrative about how Eval Engineer is being built.
