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
|-- SKILL.md                  # Distributed skill doctrine (entry point)
|-- adapters/
|   |-- claude.yaml              # Claude Code: opus / sonnet / haiku
|   |-- codex-gpt-5.6.yaml       # Codex: gpt-5.6-sol / terra / luna
|   `-- cursor-gpt-5.6.yaml    # Cursor Task: gpt-5.6-*-medium slugs
|-- spec/
|   |-- capability-tiers.md    # Portable capability tier definitions
|   `-- mapping-table.md       # Cross-runtime tier equivalence
`-- tests/
    |-- agent-surface-test.sh  # Verifies required agent surfaces
    `-- adapter-test.sh        # Verifies adapter + spec structure
```

## Ownership Boundaries

- Product behavior lives in `SKILL.md`, with portable tier definitions in `spec/` and
  runtime model slugs in `adapters/`.
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

Focused checks:

```bash
tests/agent-surface-test.sh
tests/adapter-test.sh
```

If shell scripts are added or edited, run `bash -n` on the changed scripts.
