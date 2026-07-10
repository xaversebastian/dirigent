# dirigent

A skill that turns your main session into a **conductor**: it plans a task, classifies each
piece by capability tier, dispatches workers on the cheapest tier that won't lose quality, and
reviews every result before it counts as done.

The idea is simple — most multi-step work is a mix of hard parts and mechanical parts. Running
the whole thing on your top model is wasteful; running it all on a cheap model loses quality.
`dirigent` makes the split explicit and adds a review gate so the downgrades stay safe.

## What it gives you

- A **portable capability matrix** (lead / reasoning-high / balanced / mechanical) in
  [`spec/capability-tiers.md`](spec/capability-tiers.md).
- **Runtime adapters** that map tiers to concrete model slugs — Claude
  ([`adapters/claude.yaml`](adapters/claude.yaml): opus/fable, sonnet, haiku), Codex GPT-5.6
  ([`adapters/codex-gpt-5.6.yaml`](adapters/codex-gpt-5.6.yaml): sol, terra, luna), and
  Cursor Task GPT-5.6 ([`adapters/cursor-gpt-5.6.yaml`](adapters/cursor-gpt-5.6.yaml):
  `*-medium` slugs).
- A **dispatch discipline**: explicit `model` overrides, parallel independent blocks, full
  context in every worker prompt.
- An **escalation rule** instead of blind retries (weak result → re-dispatch one tier up).
- A **review gate**: the lead session checks each worker output against the plan before
  accepting it — this is what makes routing cheaper models safe.

See [SKILL.md](SKILL.md) for the full doctrine.

## Install

```bash
git clone https://github.com/xaversebastian/dirigent.git ~/.claude/skills/dirigent
```

Then invoke it by name when you start a non-trivial task, or auto-inject it at session start
via a `SessionStart` hook in `~/.claude/settings.json` (see the "Installing" section in
[SKILL.md](SKILL.md)).

## Notes

- Capability tiers are runtime-agnostic; model slugs live in `adapters/`. See
  [`spec/mapping-table.md`](spec/mapping-table.md) for Claude ↔ GPT-5.6 equivalence.
- This is a routing layer, not an execution framework. It composes with whatever
  test/review/planning skills you already use rather than replacing them.

## License

MIT — see [LICENSE](LICENSE).
