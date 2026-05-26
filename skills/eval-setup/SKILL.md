---
name: eval-setup
description: Use when the user asks to set up Eval Engineer, check .galileo readiness, create workspace scaffolding, or configure editable files, verification commands, app type, or evidence paths.
---

# Eval Setup

Use this skill to make a repo ready for Eval Engineer without pretending it is
ready for RCA. Setup is operational: create or review workspace files, identify
missing configuration, and tell the user what evidence is still needed.

## Do

- Ensure `.galileo/config.yml`, `.galileo/current/`, `.galileo/eval-dataset/`,
  `.galileo/sessions/`, and `.galileo/learnings.md` exist.
- Preserve existing files. Do not overwrite user configuration or evidence.
- Help fill in app type, editable files, blocked files, and verification
  commands when the user knows them.
- Explain which evidence is needed next: trace, session, log stream,
  experiment, metric profile, or verification packet.

## Do Not

- Do not guess metrics, providers, app type, or production safety requirements.
- Do not fetch Galileo evidence unless the user provides a URL/ID or asks for
  `/eval-fetch`.
- Do not diagnose or fix application behavior during setup.

## Validation Loop

Before reporting ready, confirm `.galileo/config.yml`, `.galileo/current/`,
`.galileo/eval-dataset/`, `.galileo/sessions/`, and `.galileo/learnings.md`
exist, then list missing config values without guessing them.

## Output

End with:

```text
Workspace: ready/needs changes
Missing before RCA:
- ...
Next command: /eval-fetch, /eval-measure, /eval-diagnose, /eval-cost, or /eval-engineer
```

If `.galileo/current/debug-packet.json` and `.galileo/config.yml` are already
usable, route to `/eval-diagnose` for failure RCA or `/eval-cost` for
tokenomics work instead of sending the user back to `/eval-engineer`.
