# PROJECT_STRUCTURE.md - dirigent

`dirigent` is a small OSS repo for a Claude Code skill. The skill routes
non-trivial work across model tiers, while this repo's maintenance surface must
remain file-first and usable by Codex or local LLM agents.

## Start Here

1. `AGENTS.md` - repo maintenance rules.
2. `PROJECT_STRUCTURE.md` - this file index.
3. `AGENT_HANDOFF.md` - current status and open points.
4. `README.md` - public overview and install notes.
5. `SKILL.md` - distributed Claude Code skill doctrine.

## Tree

```text
dirigent/
|-- AGENTS.md                 # Tool-agnostic repo maintenance rules
|-- AGENT_HANDOFF.md          # Append-only repo handoff
|-- LICENSE                   # MIT license
|-- PROJECT_STRUCTURE.md      # This file-first index
|-- README.md                 # Public overview and install guide
|-- SKILL.md                  # Distributed Claude Code skill content
`-- tests/
    `-- agent-surface-test.sh # Verifies required agent surfaces
```

## Ownership Boundaries

- Product behavior lives in `SKILL.md`.
- Public positioning and install instructions live in `README.md`.
- Agent maintenance rules live in `AGENTS.md`.
- Current repo state lives in `AGENT_HANDOFF.md`.

Keep these surfaces separate: do not turn always-on instructions into a
changelog, and do not hide product changes in maintenance-only docs.

## Exclusions

Do not content-audit or ingest:

- `.git/`
- `.env*` files or credentials
- `node_modules/`
- `.venv/`, `__pycache__/`
- `dist/`, `build/`, generated outputs
- archives or worktrees

Allowed checks for excluded paths: existence, counts, sizes, and classification.

## Verification

Focused check:

```bash
tests/agent-surface-test.sh
```

If shell scripts are added or edited, run `bash -n` on the changed scripts.
