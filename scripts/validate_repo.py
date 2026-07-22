#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_IMPLICIT = {"ep-chinese-writing", "ep-code-change"}
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def validate_manifest() -> None:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    required = {
        "name": "easypower",
        "skills": "./skills/",
        "license": "MIT",
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            fail(f".codex-plugin/plugin.json: {key} must be {expected!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(manifest.get("version", ""))):
        fail(".codex-plugin/plugin.json: version must be SemVer")
    if not manifest.get("author", {}).get("name"):
        fail(".codex-plugin/plugin.json: author.name is required")
    interface = manifest.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not interface.get(key):
            fail(f".codex-plugin/plugin.json: interface.{key} is required")

    marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = [entry for entry in marketplace.get("plugins", []) if entry.get("name") == "easypower"]
    if len(entries) != 1:
        fail(".agents/plugins/marketplace.json: expected one easypower entry")
    elif entries[0].get("source") != {"source": "local", "path": "./"}:
        fail(".agents/plugins/marketplace.json: easypower must point to plugin root")


def validate_skills() -> set[str]:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    names = {path.name for path in skill_dirs}
    if not names:
        fail("skills/: no skills found")
        return names

    for directory in skill_dirs:
        skill_path = directory / "SKILL.md"
        metadata_path = directory / "agents" / "openai.yaml"
        scenario_path = ROOT / "tests" / directory.name / "scenarios.md"
        for path in (skill_path, metadata_path, scenario_path):
            if not path.is_file():
                fail(f"{path.relative_to(ROOT)}: required file is missing")
        if not skill_path.is_file() or not metadata_path.is_file():
            continue

        values = frontmatter(skill_path)
        if values.get("name") != directory.name:
            fail(f"{skill_path.relative_to(ROOT)}: name must match directory")
        if not values.get("description"):
            fail(f"{skill_path.relative_to(ROOT)}: description is required")

        metadata = metadata_path.read_text(encoding="utf-8")
        if f"${directory.name}" not in metadata:
            fail(f"{metadata_path.relative_to(ROOT)}: default_prompt must mention ${directory.name}")
        policy_match = re.search(r"allow_implicit_invocation:\s*(true|false)", metadata)
        expected = directory.name in EXPECTED_IMPLICIT
        if not policy_match or (policy_match.group(1) == "true") != expected:
            fail(f"{metadata_path.relative_to(ROOT)}: implicit policy must be {str(expected).lower()}")
    return names


def published_markdown() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "SKILL-MAP.md", ROOT / "SKILL-WORKFLOW.md"]
    files.extend(path for base in (ROOT / "skills", ROOT / "tests") for path in base.rglob("*.md"))
    files.extend((ROOT / "CONTRIBUTING.md", ROOT / "SECURITY.md", ROOT / "THIRD_PARTY_NOTICES.md"))
    return [path for path in files if path.is_file()]


def validate_text(names: set[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    skill_pattern = re.compile(r"\$(ep-[a-z0-9-]+)")
    placeholder_pattern = re.compile(r"\[TODO:|\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b|待补充")

    for path in published_markdown():
        text = path.read_text(encoding="utf-8")
        if placeholder_pattern.search(text):
            fail(f"{path.relative_to(ROOT)}: contains a placeholder")
        for referenced in skill_pattern.findall(text):
            if referenced not in names:
                fail(f"{path.relative_to(ROOT)}: references undefined skill ${referenced}")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().strip("<>")
            if re.match(r"^(?:https?://|mailto:|codex://|#)", target):
                continue
            local_part = unquote(target.split("#", 1)[0])
            if local_part and not (path.parent / local_part).exists():
                fail(f"{path.relative_to(ROOT)}: broken link {raw_target}")


def validate_evals(names: set[str]) -> None:
    cases = load_json(ROOT / "tests" / "routing-evals.json")
    if not isinstance(cases, list):
        fail("tests/routing-evals.json: root must be an array")
        return
    seen: set[str] = set()
    entries: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not case_id or case_id in seen:
            fail("tests/routing-evals.json: case ids must be present and unique")
        seen.add(case_id)
        entry = case.get("entry")
        route = case.get("expected_route")
        entries.add(entry)
        if entry not in names or route not in names:
            fail(f"tests/routing-evals.json: {case_id} uses an undefined skill")
        if not case.get("prompt") or not isinstance(case.get("must_not"), list):
            fail(f"tests/routing-evals.json: {case_id} is missing prompt or must_not")
    if not {"ep-use-easypower", "ep-code-change"}.issubset(entries):
        fail("tests/routing-evals.json: both routing entries need coverage")


def main() -> int:
    validate_manifest()
    names = validate_skills()
    validate_text(names)
    validate_evals(names)
    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"Validation failed with {len(ERRORS)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated Easypower plugin with {len(names)} skills and no repository errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
