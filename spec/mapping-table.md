# Cross-runtime tier mapping

Portable capability tiers (`spec/capability-tiers.md`) map to runtime-specific
models via `adapters/`. This file is the only cross-runtime model mapping.

## Tier equivalence

| Portable tier | Claude Code | Cursor Claude | Codex GPT-5.6 | Cursor GPT-5.6 |
|---|---|---|---|---|
| **Lead** | main session | main session | main session | main session |
| **reasoning-high** | `fable` (frontier/highest profile) or `opus` (high-reasoning profile) | `claude-fable-5-thinking-high` or `claude-opus-4-8-thinking-high` | `gpt-5.6-sol` | `gpt-5.6-sol-xhigh` |
| **balanced** | `sonnet` | `claude-sonnet-5-thinking-high` | `gpt-5.6-terra` | `gpt-5.6-terra-medium` |
| **mechanical** | `sonnet` fallback or lead sequentially | `claude-sonnet-5-thinking-high` fallback or lead sequentially | `gpt-5.6-luna` | `gpt-5.6-terra-medium` fallback or lead sequentially |

Escalation order (all runtimes): `mechanical` → `balanced` → `reasoning-high`.

## Claude profiles are distinct

- `fable` and `opus` are separate Claude Code aliases for separate models.
  Neither is an alias for the other.
- Fable is mapped to the frontier/highest profile.
- Opus is mapped to the high-reasoning profile.
- Both satisfy the portable `reasoning-high` capability class, but the mapping
  does not claim that they are equivalent.
- Cursor Claude uses the full model slugs exposed by the Cursor subagent schema;
  it does not reuse Claude Code aliases.

## GPT-5.6 tier and effort

Dirigent routes Codex by model tier. Reasoning effort is a separate runtime
control and never changes the portable capability classification.

| Codex model | Default effort | Locally exposed efforts |
|---|---|---|
| `gpt-5.6-sol` | `low` | `low`, `medium`, `high`, `xhigh`, `max`, `ultra` |
| `gpt-5.6-terra` | `medium` | `low`, `medium`, `high`, `xhigh`, `max`, `ultra` |
| `gpt-5.6-luna` | `medium` | `low`, `medium`, `high`, `xhigh`, `max` |

`none` is not exposed for these models in the local Codex metadata. `ultra` is
not exposed for Luna.

Cursor model identifiers are treated as complete, opaque slugs. The current
Cursor subagent schema exposes only `gpt-5.6-sol-xhigh` and
`gpt-5.6-terra-medium` from this family; no Luna slug is inferred.

## Verification basis

The versioned snapshot in `tests/fixtures/runtime-models.json` records the local
evidence used by the contract tests:

- Cursor subagent schema available on 2026-07-10;
- Claude Code `2.1.185` `--help` alias examples;
- `~/.codex/models_cache.json` read on 2026-07-10.

The fixture is an allowlist snapshot, not a claim that unlisted future models do
not exist. Update the fixture and adapters together after fresh local
verification.
