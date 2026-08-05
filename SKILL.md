---
name: dirigent
description: Coordinates non-trivial, decomposable work through Research, Plan, Act, and Review; routes independent task blocks by capability; and requires evidence-based acceptance. Use for multi-step or multi-file implementation, research, migration, or review. Skip direct questions and small single-file edits.
---

# Dirigent — the lead session conducts, the capability matrix executes

Maximum quality is the default. Economise only where no quality loss is expected,
and accept no block without concrete review evidence.

## Required workflow

Every non-trivial task follows **Research → Plan → Act → Review**:

1. **Research** — inspect the relevant source files, constraints, current state,
   and available execution capabilities before choosing an approach. Research
   comes before planning; do not plan non-trivial work from assumptions.
2. **Plan** — decompose the goal into task blocks. Every block must state:
   - its goal and owned paths or read-only scope;
   - dependencies and whether parallel execution is safe;
   - acceptance criteria;
   - a concrete done criterion and required evidence;
   - its portable capability tier.
3. **Act** — execute the plan. Dispatch eligible blocks through the matching
   runtime adapter, or execute the same blocks sequentially in the lead session
   when dispatch is unavailable.
4. **Review** — the lead session independently verifies each block against its
   acceptance criteria and done criterion before accepting it.

After Review, synthesise the outcome, deviations, and open risks.

## Trivial exception

No orchestration overhead for a direct question or a small single-file edit. The
lead session acts and verifies directly.

## Environment session routing

Some environments (e.g. MFC control-plane) define a **session work-type layer**
above these tiers. When that binding exists, classify the session there first,
then map each stage onto the portable tiers below and resolve models via the
environment binding + `adapters/`. Dirigent itself does not own environment-
specific categories or write-authority profiles.

## Routing matrix (portable)

Full tier definitions live in `spec/capability-tiers.md`. Concrete runtime
mappings live in `adapters/` and are summarised in `spec/mapping-table.md`.

| Tier | Id | For |
|---|---|---|
| **Lead** | – (itself) | Detailed planning, decomposition, architecture decisions, review/synthesis of all worker outputs, delicate or user-facing text, security-critical judgements |
| **Reasoning-high** | `reasoning-high` | Complex implementation with design latitude, hard debugging, ambiguous specs, demanding one-off writing |
| **Balanced** | `balanced` | Standard implementation with a clear spec, tests, docs, refactoring along an existing pattern, exploration/research |
| **Mechanical** | `mechanical` | Mechanical sweeps, file inventories, format/lint fixes, simple status checks, log analysis |

## Dispatch rules

- Resolve the block's tier through the adapter that matches the actual worker
  surface. Use only values listed as available by that adapter.
- An explicit model override is required only when the worker surface supports
  overrides. Never invent an override or assume an unavailable worker exists.
- Give every worker the task goal, owned paths, constraints, acceptance
  criteria, done criterion, and expected evidence.
- When in doubt, route one tier up. Quality beats savings.
- If a worker is blocked or its result is weak, sharpen the context and
  escalate one tier when possible; do not retry identically.

### Parallel safety

Independent native blocks may run in parallel in different repos or separate
worktrees, with exactly one writer per canonical worktree. Assign explicit
read/owned/forbidden paths and a single integration owner. Shared files,
overlapping paths, handoffs, indexes, and integration steps are serialized by
that owner; disjoint foreign dirt is preserved by digest.

### No-worker fallback

If no worker tool, compatible model, or supported override is available, the
orchestrator executes the unchanged plan sequentially. It records its own
evidence and never fabricates worker calls, worker findings, or unavailable
model results.

## Review gate

A task block counts as done only when the assigned verifier or orchestrator
checks:

1. every acceptance criterion against concrete evidence such as tests,
   command logs, changed paths, generated artefacts, or cited source lines;
2. the declared scope against the actual diff or output;
3. unintended side effects and integration impact;
4. unresolved assumptions, risks, and follow-up work;
5. the block's explicit done criterion.

Missing or contradictory evidence keeps the block open. Review is not delegated
to the worker that produced the result.

## Traps

- **Worktree + symlink trap:** in a monorepo whose shared directories are symlinks, never
  dispatch a block that writes through one of those symlinks with `isolation: worktree` — the
  worker commits through the symlink into the main tree. Only self-contained repos isolate
  cleanly.
- **Risk-based external effects:** confirmed `non_prod` pushes and local
  migration tests may be completed by the assigned native worker. Classify
  unknown push effects first; withhold auto-production pushes, production
  migrations, provider writes and other irreversible effects for approval.

## Installing

Install this directory in the skill location documented by the target runtime.
Automatic injection is optional; direct skill invocation must remain sufficient.

## Scope

This skill is the routing and evidence-gate layer. It composes with planning,
test-driven development, and repository-specific safety rules rather than
replacing them.
