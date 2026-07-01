# Agent Handoff - dirigent

STATUS: LIVE - 2026-07-01 - repo handoff for Codex, Claude, and local LLM agents

## Purpose

This file records current maintenance state for `oss/dirigent`. It is
append-only for substantial sessions. Do not paste chat transcripts, secrets,
private data, generated artifacts, or local machine state.

## Current State

- `dirigent` is a Claude Code skill distribution repo.
- `SKILL.md` is the primary product surface.
- `README.md` is the public overview and install guide.
- Repo maintenance should work file-first through `AGENTS.md`,
  `PROJECT_STRUCTURE.md`, and this handoff before product files are edited.
- No repo-local MCP, plugin packaging, CI, release automation, or Codex hook
  surface is documented here yet.

## Update Rule

For substantial work, append:

- Date, tool, one-line goal
- Changed paths
- Checks run
- Open points
- Uncertain assumptions
- Alternatives rejected

## Chronological Log

### 2026-07-01 - Codex - initial agent surfaces

- **Goal:** Add file-first repo surfaces so Codex and local LLM agents can
  maintain the Claude Code skill repo without requiring Claude runtime hooks,
  SessionStart, or cloud memory.
- **Changed paths:**
  - `AGENTS.md`
  - `PROJECT_STRUCTURE.md`
  - `AGENT_HANDOFF.md`
  - `tests/agent-surface-test.sh`
- **Checks run:** See final package report in the workspace/root handoff for
  the full verification bundle.
- **Open points:** No release, publish, install, push, or user-level
  `~/.claude` write was performed.
- **Uncertain assumptions:** The repo should remain a small single-skill
  distribution unless a future package explicitly adds plugin packaging or CI.
- **Alternatives rejected:** No product doctrine rewrite, no SessionStart
  automation change, no install-flow execution, and no broad OSS repo sweep.
