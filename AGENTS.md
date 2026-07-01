# AGENTS.md - dirigent

This file is the tool-agnostic maintenance contract for this repo. The product
itself is a Claude Code skill, but repo work must not require Claude runtime
features.

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

- Codex is the default coding agent for small, reviewable repo changes.
- Claude is optional for reviewing, using, or evolving the Claude Code skill
  itself.
- A local LLM must be able to work from files in this order:
  `AGENTS.md` -> `PROJECT_STRUCTURE.md` -> `AGENT_HANDOFF.md` -> `README.md`
  -> `SKILL.md`.

## Safety Rules

- Do not assume `SessionStart`, Claude memory, Claude hooks, subagents, MCP, or
  cloud memory are available for repo maintenance.
- Do not write to `~/.claude`, install the skill, publish releases, or push
  without explicit user approval.
- Keep changes small and targeted. Preserve the distinction between product
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

For substantial work, append to `AGENT_HANDOFF.md` with:

- Date, tool, one-line goal
- Changed paths
- Checks run
- Open points
- Uncertain assumptions
- Alternatives rejected
