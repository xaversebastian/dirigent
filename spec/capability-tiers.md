# Capability tiers (portable)

Runtime-agnostic routing tiers for dirigent. This file defines what capability
each task block needs, independently of concrete execution surfaces.

## Lead (conductor)

The main session itself. Never dispatched as a worker.

- Research of task context, constraints, and current state
- Detailed planning and task decomposition
- Architecture decisions and trade-off judgements
- Sequential execution when no compatible worker is available
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
2. Resolve the tier through an adapter that matches the available worker
   surface.
3. Use an explicit override only when the surface supports it and the adapter
   lists the value as available.
4. If no compatible worker or override is available, keep the same block and
   execute it sequentially in the lead session.

Capability tier and reasoning effort are separate decisions. A tier describes
the capability required by the task; effort is an optional runtime control and
must not change the tier classification.
