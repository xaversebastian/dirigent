# dirigent

A portable orchestration skill that turns the main session into a
**conductor**. Non-trivial work follows:

**Research → Plan → Act → Review**

The lead researches the real state, decomposes the goal into evidence-bearing
task blocks, routes eligible work by capability, and reviews every result before
it counts as done.

## What it gives you

- A **portable capability matrix** (lead / reasoning-high / balanced / mechanical) in
  [`spec/capability-tiers.md`](spec/capability-tiers.md).
- **Separate runtime adapters** for each execution surface. Concrete mappings
  and their local verification basis live only in `adapters/` and
  [`spec/mapping-table.md`](spec/mapping-table.md).
- A **dispatch discipline**: supported overrides only, complete worker context,
  and parallel execution only for disjoint write scopes or read-only blocks.
- A **sequential fallback**: if no compatible worker or override is available,
  the lead executes the same plan without fabricating worker results.
- An **escalation rule** instead of blind retries (weak result → re-dispatch one tier up).
- An **operational review gate**: every block has acceptance criteria and a done
  criterion; the lead checks tests, logs, paths, scope, side effects, and risks.

See [SKILL.md](SKILL.md) for the full doctrine.

## Install

Install the repository in the skill directory documented by the target runtime.
For Claude Code:

```bash
git clone https://github.com/xaversebastian/dirigent.git ~/.claude/skills/dirigent
```

Then invoke it by name when you start a non-trivial task, or auto-inject it at session start
via a `SessionStart` hook in `~/.claude/settings.json` (see the "Installing" section in
[SKILL.md](SKILL.md)). Other runtimes should use their own skill location and
invocation mechanism; an adapter does not imply hook support.

## Notes

- Capability tiers and workflow rules are runtime-neutral. Concrete model names
  are isolated to adapters and the explicit mapping document.
- Adapter availability is checked against the versioned local-evidence fixture
  in `tests/fixtures/runtime-models.json`.
- The distributed surface test works both in this OSS repo and in payload-only
  mirrors that intentionally omit maintenance files.
- This is a routing layer, not an execution framework. It composes with whatever
  test/review/planning skills you already use rather than replacing them.

## License

MIT — see [LICENSE](LICENSE).
