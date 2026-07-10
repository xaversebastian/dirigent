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
require_text "spec/mapping-table.md" "gpt-5\\.6-sol"
require_text "spec/mapping-table.md" "opus"

# Runtime adapters
require_file "adapters/claude.yaml"
require_file "adapters/codex-gpt-5.6.yaml"
require_file "adapters/cursor-gpt-5.6.yaml"

require_text "adapters/claude.yaml" "dispatch: opus"
require_text "adapters/claude.yaml" "dispatch: sonnet"
require_text "adapters/claude.yaml" "dispatch: haiku"

require_text "adapters/codex-gpt-5.6.yaml" "dispatch: gpt-5\\.6-sol"
require_text "adapters/codex-gpt-5.6.yaml" "dispatch: gpt-5\\.6-terra"
require_text "adapters/codex-gpt-5.6.yaml" "dispatch: gpt-5\\.6-luna"

require_text "adapters/cursor-gpt-5.6.yaml" "dispatch: gpt-5\\.6-sol-medium"
require_text "adapters/cursor-gpt-5.6.yaml" "dispatch: gpt-5\\.6-terra-medium"
require_text "adapters/cursor-gpt-5.6.yaml" "dispatch: gpt-5\\.6-luna-medium"

# SKILL.md must reference portable tiers, not hard-code only Claude slugs
require_text "SKILL.md" "reasoning-high"
require_text "SKILL.md" "adapters/"
require_text "SKILL.md" "codex-gpt-5\\.6\\.yaml"

printf 'OK dirigent adapters + spec\n'
