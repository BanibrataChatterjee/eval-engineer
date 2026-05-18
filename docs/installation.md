# Installing Eval Engineer Skills

Eval Engineer is distributed as a portable skill first. The canonical source is
`skills/eval-engineer/`; installers and future plugins should package
that folder instead of maintaining separate copies.

## Recommended Quick Install

Install into the current project for both Codex and Claude Code:

```bash
uvx --from git+https://github.com/Galileo-Agent-Labs/eval-engineer.git \
  eval-engineer install --target both --scope project --project-dir .
```

That creates:

- `.agents/skills/eval-engineer` for Codex.
- `.claude/skills/eval-engineer` for Claude Code.

Validate the install:

```bash
uvx --from git+https://github.com/Galileo-Agent-Labs/eval-engineer.git \
  eval-engineer check --target both --scope project --project-dir .
```

Use a user-scope install only when the skill should be available across all
projects:

```bash
uvx --from git+https://github.com/Galileo-Agent-Labs/eval-engineer.git \
  eval-engineer install --target both --scope user
```

User-scope installs write to `~/.agents/skills/eval-engineer` for Codex
and `~/.claude/skills/eval-engineer` for Claude Code.

Use `--force` when intentionally replacing an existing install. Use a tagged Git
ref once releases exist if the install must be reproducible. The install itself
does not require Galileo credentials; credentials are only needed later when a
skill run reads or writes Galileo evidence.

## Why This Is Skill-First

Claude Code treats standalone `.claude/skills` as the right path for quick
iteration and project-specific workflows, then recommends plugins when sharing,
versioned releases, or marketplace distribution become important.

Codex uses skills as the authoring format for reusable workflows and plugins as
the installable distribution unit for skills, apps, and MCP integrations.

For Eval Engineer, the reusable object today is one skill folder with
references, scripts, and assets. A `uvx` installer is the lowest-friction path
that works for both Claude Code and Codex without forking the skill.

## Plugin Direction

Plugin packaging should come after the skill installer works well.

Do not create two independent skill copies for plugins. Keep
`skills/eval-engineer/` canonical and generate or package it into:

- a Codex plugin when we need Codex marketplace installation, bundled app
  integrations, MCP servers, or plugin metadata
- a Claude Code plugin when we need namespaced team/community distribution,
  plugin agents, hooks, MCP servers, or versioned marketplace-style releases

Because Claude and Codex plugin manifests differ, publish separate plugins if we
go that route. They should share the same canonical skill source.
