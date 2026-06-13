---
name: dirigent
description: Use when starting ANY non-trivial task — multi-step, multi-file, build, research, review, migration, content. The lead session plans in detail, dispatches workers on the cheapest model that won't lose quality (opus/sonnet/haiku matrix), and reviews every result. Skip only for trivial one-file edits or direct questions.
---

# Dirigent — the lead session conducts, the model matrix executes

Maximum quality is the default. You only economise where no quality loss is expected —
and the lead-session review gate catches the rest.

## Role

Your **lead session** (the model running your main Claude Code conversation) is the conductor:

1. **Plan** — decompose the task in detail. (Plan mode and plan-writing skills stay
   compatible; this skill does not change HOW you plan, only WHO executes.)
2. **Classify** — rank each block against the routing matrix below.
3. **Dispatch** — start workers via the Agent/Task tool with an explicit `model` override.
   Run independent blocks in parallel (several Agent calls in one message).
4. **Review** — check every worker output yourself against the plan and the gates before
   it counts as done. This review is the guarantee that makes the downgrades safe.
5. **Synthesise** — summarise the result, deviations, and open points in the lead session.

## Trivial exception

No orchestration overhead for: a one-file edit, a direct question, or a task under
~15 minutes. The lead session just does it, no dispatch.

## Routing matrix

| Tier | `model` | For |
|---|---|---|
| **Lead** | – (itself) | Detailed planning, decomposition, architecture decisions, review/synthesis of all worker outputs, delicate or user-facing text, security-critical judgements |
| **Opus** | `opus` | Complex implementation with design latitude, hard debugging, ambiguous specs, demanding one-off writing |
| **Sonnet** | `sonnet` | Standard implementation with a clear spec, tests, docs, refactoring along an existing pattern, exploration/research |
| **Haiku** | `haiku` | Mechanical sweeps, file inventories, format/lint fixes, simple status checks, log analysis |

## Default rules

- **When in doubt, go one tier up.** Quality beats savings — downgrade only with a clear
  spec and a clear pattern.
- **The override is mandatory.** Without a `model` parameter, subagents inherit the lead
  model — expensive and unnecessary for mechanical work.
- **Escalate, don't retry.** Worker blocked or result weak → re-dispatch one tier up with a
  sharpened context. Never an identical retry, never patch it yourself (context pollution).
- **Workers get full context.** Task text, paths, gates, expected output format go into the
  prompt — workers shouldn't have to hunt for the plan.

## Mechanics

- Agent/Task tool: `model: "opus" | "sonnet" | "haiku"` per dispatch.
- Workflow orchestration tool (if available): `agent(prompt, {model: "..."})` — only on
  explicit user opt-in for multi-agent orchestration.
- Persistent subagents (`.claude/agents/*.md`): set the `model:` field in the frontmatter so
  the agent is pinned to a tier.
- Explore/Plan agents in plan mode: pass the override too (`model: "sonnet"` is usually enough
  for exploration).

## Traps

- **Worktree + symlink trap:** in a monorepo whose shared directories are symlinks, never
  dispatch a block that writes through one of those symlinks with `isolation: worktree` — the
  worker commits through the symlink into the main tree. Only self-contained repos isolate
  cleanly.
- **Go-gates unchanged:** push/deploy/migration still follow your normal confirmation rules —
  the conductor presents finished, reviewed changes for the human to ship.

## Installing

Drop this directory into your skills folder so it's available in every session:

```bash
git clone https://github.com/xaversebastian/dirigent.git ~/.claude/skills/dirigent
```

To make the doctrine apply automatically, inject `SKILL.md` at session start via a
`SessionStart` hook in `~/.claude/settings.json`, and optionally re-state it per prompt with a
`UserPromptSubmit` hook. (Both are optional — invoking the skill by name works on its own.)

## Scope

This skill is the **routing layer**: who does what, with which model. Execution discipline
stays with your other skills — test-driven development, review loops, plan writing. It points
at them; it doesn't duplicate them.
