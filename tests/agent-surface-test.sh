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

# The maintenance surface exists only in the OSS repo. Distributed payloads
# contain none of these four files; a partial maintenance surface is invalid.
maintenance_files=(AGENTS.md PROJECT_STRUCTURE.md AGENT_HANDOFF.md README.md)
maintenance_count=0
for path in "${maintenance_files[@]}"; do
  [[ -f "$repo_root/$path" ]] && maintenance_count=$((maintenance_count + 1))
done

maintenance_expected=0
[[ -e "$repo_root/.git" ]] && maintenance_expected=${#maintenance_files[@]}
if (( maintenance_count != maintenance_expected )); then
  fail "maintenance surface count $maintenance_count, expected $maintenance_expected"
fi

require_file "SKILL.md"
require_file "tests/agent-surface-test.sh"
require_file "tests/adapter-test.sh"
require_file "tests/contract-test.py"
require_file "tests/fixtures/runtime-models.json"
require_file "spec/capability-tiers.md"
require_file "spec/mapping-table.md"
require_file "adapters/claude-code.yaml"
require_file "adapters/cursor-claude.yaml"
require_file "adapters/codex-gpt-5.6.yaml"
require_file "adapters/cursor-gpt-5.6.yaml"

require_text "SKILL.md" "reasoning-high"
require_text "SKILL.md" "adapters/"
require_text "SKILL.md" "Research"
require_text "SKILL.md" "Plan"
require_text "SKILL.md" "Act"
require_text "SKILL.md" "Review"

if (( maintenance_expected == ${#maintenance_files[@]} )); then
  require_text "AGENTS.md" "Codex"
  require_text "AGENTS.md" "Claude"
  require_text "AGENTS.md" "local LLM"
  require_text "AGENTS.md" "SKILL.md"
  require_text "AGENTS.md" "SessionStart"

  require_text "PROJECT_STRUCTURE.md" "README.md"
  require_text "PROJECT_STRUCTURE.md" "SKILL.md"
  require_text "PROJECT_STRUCTURE.md" "AGENT_HANDOFF.md"
  require_text "PROJECT_STRUCTURE.md" "adapters/"
  require_text "PROJECT_STRUCTURE.md" "capability-tiers.md"
  require_text "PROJECT_STRUCTURE.md" "tests/agent-surface-test.sh"

  require_text "AGENT_HANDOFF.md" "STATUS:"
  require_text "AGENT_HANDOFF.md" "Changed paths"
  require_text "AGENT_HANDOFF.md" "Checks run"
  require_text "AGENT_HANDOFF.md" "Open points"
fi

printf 'OK dirigent agent surfaces\n'
