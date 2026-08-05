# PROJECT_STRUCTURE.md - dirigent

`dirigent` is a small OSS repo for a portable orchestration skill. The skill
routes non-trivial work across capability tiers, while this repo's maintenance
surface remains file-first and usable across agent runtimes.

## Start Here

1. `AGENTS.md` - repo maintenance rules.
2. `PROJECT_STRUCTURE.md` - this file index.
3. `AGENT_HANDOFF.md` - current status and open points.
4. `README.md` - public overview and install notes.
5. `SKILL.md` - distributed portable skill doctrine.

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
|   |-- claude-code.yaml       # Claude Code aliases only
|   |-- cursor-claude.yaml     # Cursor-exposed Claude slugs only
|   |-- codex-gpt-5.6.yaml     # Codex model + independent effort mapping
|   |-- cursor-gpt-5.6.yaml    # Exact Cursor GPT slugs + fallback
|   `-- cursor-grok-composer.yaml # Preferred lead Grok + Composer mechanical
|-- spec/
|   |-- capability-tiers.md    # Portable capability tier definitions
|   `-- mapping-table.md       # Cross-runtime tier equivalence
`-- tests/
    |-- agent-surface-test.sh  # Verifies OSS or payload-only surfaces
    |-- adapter-test.sh        # Shell entrypoint for adapter checks
    |-- contract-test.py       # Parses adapters + workflow contracts
    `-- fixtures/
        `-- runtime-models.json # Versioned local availability allowlist
```

## Ownership Boundaries

- Product behavior lives in `SKILL.md`, with portable tier definitions in `spec/` and
  runtime model slugs in `adapters/`.
- Environment-specific session routers (e.g. MFC C01–C14) live in that
  environment's control-plane, not here.
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
python3 tests/contract-test.py
```

If shell scripts are added or edited, run `bash -n` on the changed scripts.
