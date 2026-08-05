# Cross-runtime tier mapping

Portable capability tiers (`spec/capability-tiers.md`) map to runtime-specific
models via `adapters/`. This file is the only cross-runtime model mapping.

## Tier equivalence

| Portable tier | Claude Code | Cursor Claude | Codex GPT-5.6 | Cursor GPT-5.6 | Cursor Grok/Composer |
|---|---|---|---|---|---|
| **Lead** | main session | main session | main session | main session | `cursor-grok-4.5-high` (preferred) |
| **reasoning-high** | `opus` @ xhigh (fable = owner second opinion) | `claude-opus-5-thinking-xhigh` | `gpt-5.6-sol` | `gpt-5.6-sol-xhigh` | — |
| **balanced** | `sonnet` | `claude-sonnet-5-thinking-high` | `gpt-5.6-terra` | `gpt-5.6-terra-medium` | — |
| **mechanical** | `sonnet` fallback or lead sequential | `claude-sonnet-5-thinking-high` fallback or lead sequential | `gpt-5.6-luna` | `gpt-5.6-luna-medium` | `composer-2.5-fast` |

Escalation order (all runtimes): `mechanical` → `balanced` → `reasoning-high`.

Environment-specific session work types (e.g. MFC C01–C14) live in the
environment control-plane, not in this portable repo.

## Claude profiles are distinct

- `fable` and `opus` are separate Claude Code aliases for separate models.
  Neither is an alias for the other.
- Default `reasoning-high` dispatch is Opus (`--effort xhigh` when supported).
- Fable remains available as an owner-manual second opinion, not the auto default.
- Both satisfy the portable `reasoning-high` capability class, but the mapping
  does not claim that they are equivalent.
- Cursor Claude uses the full model slugs exposed by the Cursor catalog;
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

Cursor model identifiers are treated as complete, opaque slugs (often including
effort suffixes such as `-xhigh` or `-medium`).

## Verification basis

The versioned snapshot in `tests/fixtures/runtime-models.json` records the local
evidence used by the contract tests:

- Cursor `agent --list-models` on 2026-08-05;
- Claude Code `2.1.220` `--help` alias examples;
- `~/.codex/models_cache.json` read on 2026-08-05.

The fixture is an allowlist snapshot, not a claim that unlisted future models do
not exist. Update the fixture and adapters together after fresh local
verification.
