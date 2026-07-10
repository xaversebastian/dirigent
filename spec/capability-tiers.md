# Capability tiers (portable)

Runtime-agnostic routing tiers for dirigent. Model names live only in
`adapters/` — this file defines *what* each tier is for, not *which* slug to
dispatch.

## Lead (conductor)

The main session itself. Never dispatched as a worker.

- Detailed planning and task decomposition
- Architecture decisions and trade-off judgements
- Review and synthesis of every worker output
- Delicate or user-facing copy, security-critical calls

## Worker tiers

Classify each block into exactly one worker tier before dispatch. Escalate one
tier up when in doubt or when a worker result is weak.

| Tier | Id | For |
|---|---|---|
| **Reasoning-high** | `reasoning-high` | Complex implementation with design latitude, hard debugging, ambiguous specs, demanding one-off writing, deep review |
| **Balanced** | `balanced` | Standard implementation with a clear spec, tests, docs, refactoring along an existing pattern, exploration/research |
| **Mechanical** | `mechanical` | Mechanical sweeps, file inventories, format/lint fixes, simple status checks, log analysis |

## Escalation order

`mechanical` → `balanced` → `reasoning-high`

Never retry identically at the same tier. Re-dispatch one tier up with
sharpened context.

## Dispatch rule

1. Pick the capability tier for the block (table above).
2. Resolve the tier to a runtime-specific model via the adapter for your
   environment (`adapters/claude.yaml`, `adapters/codex-gpt-5.6.yaml`,
   `adapters/cursor-gpt-5.6.yaml`, …). See `spec/mapping-table.md` for the
   cross-runtime equivalence table.
3. Pass the adapter's `dispatch` value as an explicit `model` override on every
   worker call.

Without an override, workers inherit the lead model — expensive and unnecessary
for mechanical work.
