#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  printf 'FAIL %s\n' "$*" >&2
  exit 1
}

require_file() {
  local path="$1"
  [[ -f "$repo_root/$path" ]] || fail "missing $path"
}

require_absent() {
  local path="$1"
  [[ ! -e "$repo_root/$path" ]] || fail "unexpected legacy path $path"
}

require_text() {
  local path="$1"
  local pattern="$2"
  grep -Eq "$pattern" "$repo_root/$path" || fail "$path missing pattern: $pattern"
}

# Portable spec
require_file "spec/capability-tiers.md"
require_file "spec/mapping-table.md"
require_text "spec/capability-tiers.md" "reasoning-high"
require_text "spec/capability-tiers.md" "balanced"
require_text "spec/capability-tiers.md" "mechanical"
require_text "spec/mapping-table.md" "gpt-5\\.6-sol-xhigh"
require_text "spec/mapping-table.md" "fable.*opus.*separate"

# Runtime adapters
require_file "adapters/claude-code.yaml"
require_file "adapters/cursor-claude.yaml"
require_file "adapters/codex-gpt-5.6.yaml"
require_file "adapters/cursor-gpt-5.6.yaml"
require_absent "adapters/claude.yaml"

require_text "adapters/claude-code.yaml" "^[[:space:]]+dispatch: fable$"
require_text "adapters/claude-code.yaml" "^[[:space:]]+high-reasoning: opus$"
require_text "adapters/claude-code.yaml" "^[[:space:]]+dispatch: sonnet$"

require_text "adapters/cursor-claude.yaml" "^[[:space:]]+dispatch: claude-fable-5-thinking-high$"
require_text "adapters/cursor-claude.yaml" "^[[:space:]]+high-reasoning: claude-opus-4-8-thinking-high$"
require_text "adapters/cursor-claude.yaml" "^[[:space:]]+dispatch: claude-sonnet-5-thinking-high$"

require_text "adapters/codex-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-sol$"
require_text "adapters/codex-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-terra$"
require_text "adapters/codex-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-luna$"
require_text "adapters/codex-gpt-5.6.yaml" "independent_from_tier: true"

require_text "adapters/cursor-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-sol-xhigh$"
require_text "adapters/cursor-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-terra-medium$"
require_text "adapters/cursor-gpt-5.6.yaml" "^[[:space:]]+dispatch: gpt-5\\.6-luna-medium$"
require_text "adapters/cursor-gpt-5.6.yaml" "fallback: lead-sequential"

require_file "adapters/cursor-grok-composer.yaml"
require_text "adapters/cursor-grok-composer.yaml" "^[[:space:]]+dispatch: cursor-grok-4\\.5-high$"
require_text "adapters/cursor-grok-composer.yaml" "^[[:space:]]+dispatch: composer-2\\.5-fast$"


# Portable core and executable contract
require_text "SKILL.md" "reasoning-high"
require_text "SKILL.md" "adapters/"
require_text "SKILL.md" "Research"
require_text "SKILL.md" "Plan"
require_text "SKILL.md" "Act"
require_text "SKILL.md" "Review"
require_file "tests/fixtures/runtime-models.json"
require_file "tests/contract-test.py"

python3 "$repo_root/tests/contract-test.py"

printf 'OK dirigent adapters + spec\n'
