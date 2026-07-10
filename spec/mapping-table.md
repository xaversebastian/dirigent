# Cross-runtime tier mapping

Portable capability tiers (`spec/capability-tiers.md`) map to runtime-specific
model slugs via `adapters/`. Model names never appear in the portable spec.

## Tier equivalence

| Portable tier | Claude (`adapters/claude.yaml`) | GPT-5.6 Codex (`adapters/codex-gpt-5.6.yaml`) | GPT-5.6 Cursor (`adapters/cursor-gpt-5.6.yaml`) |
|---|---|---|---|
| **Lead** (conductor) | main session | main session | main session |
| **reasoning-high** | `opus` (alias: `fable`) | `gpt-5.6-sol` | `gpt-5.6-sol-medium` |
| **balanced** | `sonnet` | `gpt-5.6-terra` | `gpt-5.6-terra-medium` |
| **mechanical** | `haiku` | `gpt-5.6-luna` | `gpt-5.6-luna-medium` |

Escalation order (all runtimes): `mechanical` → `balanced` → `reasoning-high`.

## What GPT-5.6 tiers mean

OpenAI launched GPT-5.6 on 2026-07-09 as a three-tier model family:

- **Sol** — flagship; frontier agentic coding, long-horizon work, max/ultra reasoning.
- **Terra** — balanced everyday tier; competitive with GPT-5.5 at lower cost.
- **Luna** — fastest, most affordable; volume/mechanical workloads.

The number (5.6) is the generation. Sol/Terra/Luna are durable capability tiers
that can advance independently. Sources: [OpenAI announcement](https://openai.com/index/gpt-5-6/),
[OpenAI API model guidance](https://developers.openai.com/api/docs/guides/latest-model).

## Tier vs reasoning effort (GPT-5.6 only)

GPT-5.6 separates **model tier** (sol/terra/luna) from **reasoning effort**
(`none`, `low`, `medium`, `high`, `xhigh`, `max`, `ultra`). Dirigent routes by
tier; effort stays at runtime defaults unless the lead session explicitly raises
it for a hard block.

Cursor's `*-medium` slugs are composite model ids (tier + default effort preset),
not a separate tier.

## Claude tier notes

- `fable` is an extended-thinking alias at the reasoning-high tier (analogous
  role to sol + high reasoning).
- `opus` / `sonnet` / `haiku` are the default Claude Code dispatch overrides.
