# Cross-runtime tier mapping

Portable capability tiers (`spec/capability-tiers.md`) map to runtime-specific
models via `adapters/`. This file is the only cross-runtime model mapping.

## Tier equivalence

| Portable tier | Claude Code | Cursor Claude | Codex GPT-6 | Cursor GPT-6 | Cursor Grok/Composer |
|---|---|---|---|---|---|
| **Lead** | main session | main session | main session | unused by MFC | `cursor-grok-4.5-high` (preferred) |
| **reasoning-high** | `opus` @ xhigh (fable = owner second opinion) | `claude-opus-5-thinking-xhigh` | `gpt-6-astra` @ xhigh | `lead-sequential` (no Astra slug) | — |
| **balanced** | `sonnet` | `claude-sonnet-5-thinking-high` | `gpt-6-astra` @ high | `lead-sequential` (no Astra slug) | — |
| **mechanical** | `sonnet` fallback or lead sequential | `claude-sonnet-5-thinking-high` fallback or lead sequential | `gpt-6-astra` @ medium | `lead-sequential` (no Astra slug) | `composer-2.5-fast` |

Escalation order (all runtimes): `mechanical` → `balanced` → `reasoning-high`.

Environment-specific session work types (e.g. MFC C01–C14) live in the
environment control-plane, not in this portable repo.

MFC auto-routing must not use Cursor Claude or Cursor GPT adapters. Those
families go through Claude Code CLI and Codex CLI.

## Claude profiles are distinct

- `fable` and `opus` are separate Claude Code aliases for separate models.
  Neither is an alias for the other.
- Default `reasoning-high` dispatch is Opus (`--effort xhigh` when supported).
- Fable 5.1 remains available as an owner-manual second opinion, not the auto default.
- Both satisfy the portable `reasoning-high` capability class, but the mapping
  does not claim that they are equivalent.
- Cursor Claude uses the full model slugs exposed by the Cursor catalog;
  it does not reuse Claude Code aliases. Owner-second-opinion is
  `claude-fable-5-1-thinking-high`.

## GPT-6 Astra tier and effort

Dirigent routes Codex by a single model slug. Reasoning effort is a separate
runtime control and never changes the portable capability classification.

| Codex model | Default effort | Locally exposed efforts |
|---|---|---|
| `gpt-6-astra` | `medium` | `low`, `medium`, `high`, `xhigh`, `max`, `ultra` |

Cursor GPT identifiers are treated as complete, opaque slugs. The 2026-09-05
Cursor catalog has no `gpt-6-astra` slugs. The Cursor GPT adapter therefore
dispatches `lead-sequential` and is forbidden for MFC auto-routing. Do not
invent Cursor Astra IDs.

## Verification basis

The versioned snapshot in `tests/fixtures/runtime-models.json` records the local
evidence used by the contract tests:

- Cursor `agent --list-models` on 2026-09-05;
- Claude Code `2.1.261` alias examples (`fable` → Fable 5.1);
- `~/.codex/models_cache.json` read on 2026-09-05 (client 0.153.4).

The fixture is an allowlist snapshot, not a claim that unlisted future models do
not exist. Update the fixture and adapters together after fresh local
verification.
