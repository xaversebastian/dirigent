# AGENTS.md - dirigent

This file is the tool-agnostic maintenance contract for this repo. The product
itself is a portable runtime-neutral skill, so repo work must not require any
single tool runtime.

## Session Start

1. Read this file.
2. Read `PROJECT_STRUCTURE.md`.
3. Read `AGENT_HANDOFF.md`.
4. Read `README.md` and `SKILL.md` before changing product behavior.
5. Check `git status --short --branch` before edits and do not touch foreign
   dirty changes.

## Scope

- `SKILL.md` is the distributed skill doctrine and primary product surface.
- `README.md` is the public repo overview and install guide.
- `AGENT_HANDOFF.md` records current maintenance state.
- `tests/agent-surface-test.sh` guards this repo's file-first agent surface.

## Agent Roles

- Codex is the default coding agent for complete, clearly scoped reversible
  repo tasks; task size alone does not require another tool.
- Claude is an optional adapter for reviewing or using the portable skill.
- A local LLM must be able to work from files in this order:
  `AGENTS.md` -> `PROJECT_STRUCTURE.md` -> `AGENT_HANDOFF.md` -> `README.md`
  -> `SKILL.md`.

## Safety Rules

- Do not assume `SessionStart`, Claude memory, Claude hooks, subagents, MCP, or
  cloud memory are available for repo maintenance.
- Do not write to `~/.claude`, install the skill there, or publish releases
  without explicit user approval. Confirmed `non_prod` pushes are allowed;
  classify unknown push effects first and withhold auto-production pushes.
- Keep changes scoped and atomic. Preserve the distinction between product
  guidance in `SKILL.md` and maintenance guidance in this file.
- Do not add generated artifacts, credentials, private data, or local runtime
  state.

## Checks

Run the focused surface check after maintenance changes:

```bash
tests/agent-surface-test.sh
```

For shell edits, also run `bash -n` on changed shell scripts.

## Handoff Updates

Append only for durable cross-session state, open gates, or a real handoff:

- Date, tool, one-line goal
- Changed paths
- Checks run
- Open points
- Uncertain assumptions
- Alternatives rejected
