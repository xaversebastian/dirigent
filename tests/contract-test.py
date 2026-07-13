#!/usr/bin/env python3
"""Dependency-free contract checks for the distributed dirigent payload."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/runtime-models.json"
ADAPTERS = {
    "claude_code": ROOT / "adapters/claude-code.yaml",
    "cursor_claude": ROOT / "adapters/cursor-claude.yaml",
    "codex": ROOT / "adapters/codex-gpt-5.6.yaml",
    "cursor_gpt": ROOT / "adapters/cursor-gpt-5.6.yaml",
}


class ContractError(RuntimeError):
    """Raised when a payload contract is violated."""


def fail(message: str) -> None:
    raise ContractError(message)


def parse_scalar(value: str, path: Path, line_number: int) -> Any:
    if not value:
        fail(f"{path}:{line_number}: empty scalar")
    if value in {"true", "false"}:
        return value == "true"
    if value[0] in "[{|>":
        fail(f"{path}:{line_number}: unsupported YAML scalar syntax")
    return value


def parse_yaml_subset(path: Path) -> dict[str, Any]:
    """Parse the strict mapping/list YAML subset used by the adapters."""

    records: list[tuple[int, str, int]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "\t" in raw:
            fail(f"{path}:{line_number}: tabs are not allowed")
        stripped = raw.lstrip(" ")
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(stripped)
        if indent % 2:
            fail(f"{path}:{line_number}: indentation must use two-space steps")
        records.append((indent, stripped, line_number))

    if not records:
        fail(f"{path}: empty YAML")

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(records) or records[index][0] != indent:
            fail(f"{path}: expected content at indentation {indent}")

        list_mode = records[index][1].startswith("- ")
        container: Any = [] if list_mode else {}

        while index < len(records):
            current_indent, text, line_number = records[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                fail(f"{path}:{line_number}: unexpected indentation")

            if list_mode:
                if not text.startswith("- "):
                    fail(f"{path}:{line_number}: mixed list and mapping")
                container.append(parse_scalar(text[2:].strip(), path, line_number))
                index += 1
                continue

            if text.startswith("- "):
                fail(f"{path}:{line_number}: mixed mapping and list")
            match = re.fullmatch(r"([A-Za-z0-9_.-]+):(.*)", text)
            if not match:
                fail(f"{path}:{line_number}: invalid mapping entry")
            key, raw_value = match.group(1), match.group(2).strip()
            if key in container:
                fail(f"{path}:{line_number}: duplicate key {key}")

            index += 1
            if raw_value:
                container[key] = parse_scalar(raw_value, path, line_number)
                continue

            if index >= len(records) or records[index][0] != indent + 2:
                fail(f"{path}:{line_number}: key {key} requires a nested block")
            container[key], index = parse_block(index, indent + 2)

        return container, index

    parsed, final_index = parse_block(0, records[0][0])
    if final_index != len(records) or not isinstance(parsed, dict):
        fail(f"{path}: incomplete or non-mapping document")
    return parsed


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, got {actual!r}")


def validate_adapters() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    parsed = {name: parse_yaml_subset(path) for name, path in ADAPTERS.items()}

    legacy = ROOT / "adapters/claude.yaml"
    if legacy.exists():
        fail("mixed Claude adapter still exists: adapters/claude.yaml")

    for name, adapter in parsed.items():
        allowed = set(adapter["dispatch"]["allowed"])
        for tier, config in adapter["tiers"].items():
            if config["dispatch"] not in allowed:
                fail(f"{name} {tier} dispatch is outside its allowlist")
            for profile, model in config.get("alternatives", {}).items():
                if model not in allowed:
                    fail(f"{name} {tier} alternative {profile} is outside its allowlist")

    require_equal(
        parsed["claude_code"]["dispatch"]["allowed"],
        fixture["claude_code"]["aliases"],
        "Claude Code allowlist",
    )
    require_equal(
        parsed["cursor_claude"]["dispatch"]["allowed"],
        fixture["cursor"]["claude"],
        "Cursor Claude allowlist",
    )
    require_equal(
        parsed["cursor_gpt"]["dispatch"]["allowed"],
        fixture["cursor"]["gpt_5_6"],
        "Cursor GPT allowlist",
    )
    require_equal(
        parsed["codex"]["dispatch"]["allowed"],
        list(fixture["codex"]["models"]),
        "Codex allowlist",
    )

    claude_high = parsed["claude_code"]["tiers"]["reasoning-high"]
    require_equal(claude_high["dispatch"], "fable", "Claude Code frontier profile")
    require_equal(
        claude_high["alternatives"]["high-reasoning"],
        "opus",
        "Claude Code high-reasoning profile",
    )
    if claude_high["dispatch"] == claude_high["alternatives"]["high-reasoning"]:
        fail("Fable and Opus must remain distinct models")

    cursor_high = parsed["cursor_claude"]["tiers"]["reasoning-high"]
    if cursor_high["dispatch"] == cursor_high["alternatives"]["high-reasoning"]:
        fail("Cursor Fable and Opus must remain distinct models")

    cursor_mechanical = parsed["cursor_gpt"]["tiers"]["mechanical"]
    require_equal(
        cursor_mechanical["dispatch"],
        "gpt-5.6-terra-medium",
        "Cursor mechanical fallback model",
    )
    require_equal(
        cursor_mechanical["fallback"],
        "lead-sequential",
        "Cursor mechanical sequential fallback",
    )
    if "gpt-5.6-luna" in ADAPTERS["cursor_gpt"].read_text(encoding="utf-8").lower():
        fail("Cursor adapter must not invent a Luna slug")

    effort = parsed["codex"]["reasoning_effort"]
    require_equal(effort["independent_from_tier"], True, "Codex tier/effort split")
    for model, expected in fixture["codex"]["models"].items():
        actual = effort["models"][model]
        require_equal(actual["default"], expected["default_effort"], f"{model} default effort")
        require_equal(actual["allowed"], expected["efforts"], f"{model} effort allowlist")

    ruby = shutil.which("ruby")
    if ruby:
        subprocess.run(
            [
                ruby,
                "-e",
                "require 'yaml'; ARGV.each { |path| YAML.load_file(path) }",
                *(str(path) for path in ADAPTERS.values()),
            ],
            check=True,
            capture_output=True,
            text=True,
        )


def validate_portable_core() -> None:
    core_paths = [ROOT / "SKILL.md", ROOT / "spec/capability-tiers.md"]
    forbidden = re.compile(
        r"\b(?:claude|cursor|codex|gpt|fable|opus|sonnet|haiku|sol|terra|luna)\b",
        re.IGNORECASE,
    )
    for path in core_paths:
        match = forbidden.search(path.read_text(encoding="utf-8"))
        if match:
            fail(f"{path}: runtime/model leak: {match.group(0)}")


def validate_skill_workflow() -> None:
    path = ROOT / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) >= 500:
        fail(f"SKILL.md must stay below 500 lines; got {len(lines)}")

    frontmatter = text.split("---", 2)[1]
    body = text.split("---", 2)[2]
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not description_match or not description_match.group(1).startswith("Coordinates "):
        fail("SKILL.md description must be specific and third-person")

    if "**Research → Plan → Act → Review**" not in body:
        fail("SKILL.md must name the complete workflow")
    stage_patterns = (
        r"^1\. \*\*Research\*\*",
        r"^2\. \*\*Plan\*\*",
        r"^3\. \*\*Act\*\*",
        r"^4\. \*\*Review\*\*",
    )
    positions = [
        match.start() if (match := re.search(pattern, body, re.MULTILINE)) else -1
        for pattern in stage_patterns
    ]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        fail("SKILL.md must define Research -> Plan -> Act -> Review in order")

    required_phrases = [
        "acceptance criteria",
        "done criterion",
        "concrete evidence",
        "tests",
        "command logs",
        "owned paths",
        "unintended side effects",
        "risks",
        "executes the unchanged plan sequentially",
        "never fabricates",
        "exactly one writer per canonical worktree",
        "read/owned/forbidden paths",
        "disjoint foreign dirt",
        "read-only",
    ]
    lower = " ".join(text.lower().split())
    for phrase in required_phrases:
        if phrase.lower() not in lower:
            fail(f"SKILL.md missing workflow contract phrase: {phrase}")


def main() -> int:
    try:
        validate_adapters()
        validate_portable_core()
        validate_skill_workflow()
    except (ContractError, KeyError, TypeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("OK dirigent runtime + workflow contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
