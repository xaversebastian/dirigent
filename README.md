# dirigent

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill that turns your main
session into a **conductor**: it plans a task, classifies each piece, dispatches workers on the
cheapest model that won't lose quality (an opus/sonnet/haiku matrix), and reviews every result
before it counts as done.

The idea is simple — most multi-step work is a mix of hard parts and mechanical parts. Running
the whole thing on your top model is wasteful; running it all on a cheap model loses quality.
`dirigent` makes the split explicit and adds a review gate so the downgrades stay safe.

## What it gives you

- A **routing matrix** (lead / opus / sonnet / haiku) with a one-line rule for each tier.
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

- The `opus`/`sonnet`/`haiku` tiers are Claude model families; adapt the names if your setup
  exposes different model ids.
- This is a routing layer, not an execution framework. It composes with whatever
  test/review/planning skills you already use rather than replacing them.

## License

MIT — see [LICENSE](LICENSE).
