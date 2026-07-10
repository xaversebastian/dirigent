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

### 2026-07-10 - Cursor - GPT-5.6 portable adapters

- **Goal:** Add portable capability tiers and GPT-5.6 (Sol/Terra/Luna) runtime
  adapters for Codex and Cursor; refactor SKILL.md to reference adapters instead
  of hard-coded Claude slugs only.
- **Changed paths:**
  - `SKILL.md`
  - `README.md`
  - `PROJECT_STRUCTURE.md`
  - `spec/capability-tiers.md`
  - `spec/mapping-table.md` (new)
  - `adapters/claude.yaml` (new)
  - `adapters/codex-gpt-5.6.yaml` (new)
  - `adapters/cursor-gpt-5.6.yaml` (new)
  - `tests/adapter-test.sh` (new)
  - `tests/agent-surface-test.sh`
- **Checks run:** `bash -n tests/*.sh`; `tests/agent-surface-test.sh`;
  `tests/adapter-test.sh`
- **Open points:** `MFC/vaoa-os/engine/skills/dirigent/SKILL.md` and vendored
  copies (siljajanina) not synced — separate vendor-silja / engine sync task.
  No commit/push.
- **Uncertain assumptions:** Cursor `*-medium` slugs are composite tier+effort
  ids, not separate capability tiers; Codex canonical slugs omit the suffix.
- **Alternatives rejected:** Merging tier and reasoning effort into one routing
  dimension; putting model slugs into `spec/capability-tiers.md`.

### 2026-07-10 - Cursor - GPT-5.6 adapter + portable tier spec

- **Goal:** Add runtime-agnostic capability tiers and GPT-5.6 Sol/Terra/Luna Codex
  adapter alongside existing Claude mapping; keep tier doctrine out of model slugs.
- **Changed paths:**
  - `SKILL.md`
  - `README.md`
  - `PROJECT_STRUCTURE.md`
  - `spec/capability-tiers.md`
  - `adapters/claude.yaml`
  - `adapters/codex-gpt-5.6.yaml`
  - `tests/agent-surface-test.sh`
- **Checks run:** `bash -n tests/agent-surface-test.sh`; `tests/agent-surface-test.sh`
- **Open points:** `~/.claude/skills/dirigent` still symlinks to
  `MFC/vaoa-os/engine/skills/dirigent`, not `oss/dirigent` — engine/silja copies
  need manual re-sync after OSS publish. No commit/push performed.
- **Uncertain assumptions:** Codex dispatch slugs are `gpt-5.6-{sol,terra,luna}`
  without `-medium` suffix per `~/.codex/models_cache.json`; Cursor may use
  `-medium` aliases on the same tier.
- **Alternatives rejected:** Monolithic SKILL-only GPT section without `spec/` +
  `adapters/` split (rejected — harder to extend for future model families).

### 2026-07-10 - Cursor - Rollout sync (engine, silja, symlink)

- **Goal:** Complete portable spec rollout after OSS commit — engine copy, Claude symlink, silja vendor.
- **Changed paths:** (external) `MFC/vaoa-os/engine/skills/dirigent/**`, `engine/scripts/silja-vendor.manifest`, `MFC/siljajanina.com/.claude/skills/dirigent/**`, `~/.claude/skills/dirigent` symlink.
- **Checks run:** `tests/agent-surface-test.sh`, `tests/adapter-test.sh` (oss); `tests/adapter-test.sh` (engine); `diff` oss vs engine payload.
- **Open points:** Push still pending (`main` ahead of origin). vaoa-os + siljajanina commits separate.
- **Uncertain assumptions:** Engine `agent-surface-test.sh` expects full OSS repo root (AGENTS.md) — run surface tests from oss only.
- **Alternatives rejected:** Symlink to engine copy instead of oss (rejected — oss is publish SoT).
