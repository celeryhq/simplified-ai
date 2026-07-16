#!/usr/bin/env python3
"""Validate marketer skill contracts and optionally grade agent traces.

The default run is deterministic and needs no network access. It validates the
scenario catalog plus the platform and marketer SKILL.md contracts. Pass --traces to grade
captured agent runs against expected skill routing, tool order, arguments, and
publishing safety.

Trace JSON can be a list, {"traces": [...]}, or JSONL. Each trace has:
  {"id": "P1", "skill": "social-content-planner",
   "tools": [{"name": "social_getSocialMediaAccounts", "arguments": {}}],
   "output": "..."}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = Path(__file__).with_name("skill-cases.json")
DEFAULT_INVENTORY = Path(__file__).with_name("hosted-tool-inventory.json")
DEFAULT_SOURCE_INVENTORY = Path(__file__).with_name("source-profile-tool-inventory.json")

CONTRACT_TERMS = {
    "social-content-planner": [
        "social_getsocialmediaaccounts",
        'action: "draft"',
        "explicit confirmation",
        "planning, drafting, and publishing",
    ],
    "cross-platform-campaign": [
        "social_getsocialmediaaccounts",
        'storage: "asset"',
        "permanent `asset_id`",
        "explicit approval",
        'action: "draft"',
    ],
    "content-repurposer": [
        "treat the source as authoritative",
        'action: "draft"',
        "explicit approval",
        "do not merely shorten",
    ],
    "social-performance-analyst": [
        "social_getsocialmediaanalyticsaggregated",
        "social_getsocialmediaanalyticsrange",
        "social_getsocialmediaanalyticsposts",
        "social_getsocialmediaanalyticsaudience",
        "read-only",
    ],
    "campaign-review": [
        "social_getsocialmediaaccounts",
        "social_getsocialmediadrafts",
        "social_createsocialmediareviewbundle",
        "comma-separated",
        "per-account fallback",
        "`draft_ids`",
        "not publishing authorization",
    ],
    "evergreen-content-engine": [
        "content territories",
        "content bank",
        'action: "draft"',
        "review date",
        "retirement rule",
    ],
    "local-business-marketing": [
        "google business",
        "service area",
        'action: "draft"',
        "verify",
        "never fabricate reviews",
    ],
    "creative-testing": [
        "falsifiable hypothesis",
        "one primary variable",
        "control",
        "decision metric",
        'action: "draft"',
    ],
}

PLATFORM_CONTRACT_TERMS = {
    "generate-image": [
        "api_getmodelfields",
        "api_generateimage",
        '"storage": "asset"',
        "credits",
    ],
    "simplified-social": [
        "api_signassetupload",
        "direct client put",
        "api_registerasset",
        "api_getasset",
        "never pass a client-local path",
        "never attach the simplified oauth/api authorization header",
        "mastodon",
        "additional.reddit.post.targets",
        "telegram",
        "auto-comments",
        "`delay` is measured in",
        "`delay = x * 60`",
    ],
    "generate-video": [
        "api_getmodelfields",
        "api_generatevideo",
        "api_getvideovariation",
        'storage: "asset"',
        "spends credits",
    ],
    "manage-brand": [
        "api_listbrandkits",
        "api_getbrandkit",
        "api_buildbrandkit",
        "api_getcontextdocumentbytype",
        "api_updatecontextdocument",
        "fabricated certainty",
    ],
    "manage-projects": [
        "api_listprojects",
        "api_createprojectitem",
        "api_assignagenttoitem",
        "api_exportprojectitems",
        "confirm",
    ],
    "simplified-workspace": [
        "api_getworkspaceinfo",
        "api_listteamspaces",
        "api_getworkspace",
        "authoritative `whoami`",
        "space_id",
        "every downstream",
        "stateless",
    ],
}

REQUIRED_REFERENCES = {
    "simplified-social": ["references/assets.md"],
    "generate-video": ["references/models-and-polling.md"],
    "manage-brand": ["references/brand-system.md"],
    "manage-projects": ["references/project-operations.md"],
    "simplified-workspace": ["references/teamspace-context.md"],
    "evergreen-content-engine": ["references/content-system.md"],
    "local-business-marketing": ["references/local-channel-playbook.md"],
    "creative-testing": ["references/experiment-design.md"],
}

SOURCE_PROFILE_CASE_SKILLS = {
    "generate-video",
    "manage-brand",
    "manage-projects",
    "simplified-workspace",
}
ROUTING_SKILLS = set(CONTRACT_TERMS) | SOURCE_PROFILE_CASE_SKILLS


@dataclass
class Check:
    name: str
    passed: bool
    message: str


def load_json_or_jsonl(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = load_json_or_jsonl(path)
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("case file must be an object containing a cases list")
    return data["cases"]


def validate_contracts(
    cases: list[dict[str, Any]],
    inventory: dict[str, Any],
    source_inventory: dict[str, Any],
) -> list[Check]:
    checks: list[Check] = []
    ids = [case.get("id") for case in cases]
    duplicates = sorted(k for k, count in Counter(ids).items() if count > 1)
    checks.append(Check("catalog IDs", not duplicates, f"duplicates={duplicates}" if duplicates else f"{len(ids)} unique"))

    counts = Counter(case.get("skill") for case in cases)
    missing_coverage = {skill: counts.get(skill, 0) for skill in ROUTING_SKILLS if counts.get(skill, 0) < 3}
    checks.append(Check("skill coverage", not missing_coverage,
                        f"needs >=3 cases: {missing_coverage}" if missing_coverage else str(dict(counts))))

    catalog_errors: list[str] = []
    for case in cases:
        cid = case.get("id", "<missing>")
        expected = case.get("expected")
        if not isinstance(cid, str) or not cid:
            catalog_errors.append("case missing string id")
        if case.get("skill") not in ROUTING_SKILLS:
            catalog_errors.append(f"{cid}: unknown skill")
        if case.get("tool_profile", "live") not in ("live", "source"):
            catalog_errors.append(f"{cid}: invalid tool_profile")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            catalog_errors.append(f"{cid}: missing prompt")
        if not isinstance(expected, dict):
            catalog_errors.append(f"{cid}: missing expected object")
            continue
        required = set(expected.get("required_tools", []))
        forbidden = set(expected.get("forbidden_tools", []))
        if required & forbidden:
            catalog_errors.append(f"{cid}: tools both required and forbidden: {sorted(required & forbidden)}")
        for rule in expected.get("required_args", []):
            if not all(field in rule for field in ("tool", "path")) or not ({"equals", "nonempty"} & set(rule)):
                catalog_errors.append(f"{cid}: malformed required_args rule")
        for rule in expected.get("forbidden_args", []):
            if not all(field in rule for field in ("tool", "path", "equals")):
                catalog_errors.append(f"{cid}: malformed forbidden_args rule")
        for rule in expected.get("handoffs", []):
            required_fields = ("from_tool", "from_path", "to_tool", "to_path")
            if not all(field in rule for field in required_fields):
                catalog_errors.append(f"{cid}: malformed handoff rule")
        for group in expected.get("required_output_any", []):
            if not isinstance(group, list) or not group or not all(isinstance(term, str) for term in group):
                catalog_errors.append(f"{cid}: malformed required_output_any group")
    checks.append(Check("catalog schema", not catalog_errors,
                        "; ".join(catalog_errors) if catalog_errors else "valid"))

    def referenced_tools(selected_cases: list[dict[str, Any]]) -> set[str]:
        referenced: set[str] = set()
        for case in selected_cases:
            expected = case["expected"]
            for key in ("required_tools", "forbidden_tools", "ordered_tools"):
                referenced.update(expected.get(key, []))
            for key in ("required_args", "forbidden_args"):
                referenced.update(rule["tool"] for rule in expected.get(key, []))
            for rule in expected.get("handoffs", []):
                referenced.update((rule["from_tool"], rule["to_tool"]))
        return referenced

    def inventory_check(
        label: str, selected_cases: list[dict[str, Any]], selected_inventory: dict[str, Any]
    ) -> Check:
        names = selected_inventory.get("names", [])
        errors: list[str] = []
        if selected_inventory.get("total") != len(names) or len(set(names)) != len(names):
            errors.append("inventory count or uniqueness mismatch")
        unknown = sorted(referenced_tools(selected_cases) - set(names))
        if unknown:
            errors.append(f"evals reference tools absent from inventory: {unknown}")
        return Check(
            label,
            not errors,
            "; ".join(errors) if errors else f"{len(names)} tools",
        )

    live_cases = [case for case in cases if case.get("tool_profile", "live") == "live"]
    source_cases = [case for case in cases if case.get("tool_profile") == "source"]
    checks.append(inventory_check("hosted tool inventory", live_cases, inventory))
    checks.append(inventory_check("source profile inventory", source_cases, source_inventory))

    manifest_errors: list[str] = []
    prompts: list[Any] = []
    try:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        prompts = manifest.get("interface", {}).get("defaultPrompt", [])
        if not isinstance(prompts, list) or len(prompts) > 3:
            manifest_errors.append("interface.defaultPrompt must contain at most 3 prompts")
        elif any(not isinstance(prompt, str) or len(prompt) > 128 for prompt in prompts):
            manifest_errors.append("each default prompt must be a string of at most 128 characters")
    except (OSError, json.JSONDecodeError) as exc:
        manifest_errors.append(str(exc))
    checks.append(Check("Codex prompt manifest", not manifest_errors,
                        "; ".join(manifest_errors) if manifest_errors else f"{len(prompts)} valid prompts"))

    for skill, terms in {**CONTRACT_TERMS, **PLATFORM_CONTRACT_TERMS}.items():
        folder = ROOT / "skills" / skill
        skill_file = folder / "SKILL.md"
        metadata_file = folder / "agents" / "openai.yaml"
        errors: list[str] = []
        if not skill_file.exists():
            errors.append("SKILL.md missing")
        else:
            content = skill_file.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not match or not re.search(rf"^name:\s*{re.escape(skill)}\s*$", match.group(1), re.MULTILINE):
                errors.append("frontmatter name mismatch")
            for reference in REQUIRED_REFERENCES.get(skill, []):
                if reference not in content:
                    errors.append(f"SKILL.md does not route to {reference}")
                    continue
                reference_file = folder / reference
                if not reference_file.exists():
                    errors.append(f"{reference} missing")
                else:
                    content += "\n" + reference_file.read_text(encoding="utf-8")
            lower = content.lower()
            missing_terms = [term for term in terms if term.lower() not in lower]
            if missing_terms:
                errors.append(f"missing contract terms {missing_terms}")
        if not metadata_file.exists():
            errors.append("agents/openai.yaml missing")
        elif f"${skill}" not in metadata_file.read_text(encoding="utf-8"):
            errors.append("default prompt does not name skill")
        checks.append(Check(f"contract {skill}", not errors, "; ".join(errors) if errors else "valid"))
    return checks


def normalize_traces(data: Any) -> dict[str, dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("traces"), list):
        data = data["traces"]
    if not isinstance(data, list):
        raise ValueError("trace file must be a list, a traces object, or JSONL")
    traces: dict[str, dict[str, Any]] = {}
    for trace in data:
        if not isinstance(trace, dict) or not isinstance(trace.get("id"), str):
            raise ValueError("every trace must be an object with a string id")
        if trace["id"] in traces:
            raise ValueError(f"duplicate trace id {trace['id']}")
        traces[trace["id"]] = trace
    return traces


def tool_calls(trace: dict[str, Any]) -> list[dict[str, Any]]:
    calls = []
    for item in trace.get("tools", []):
        if isinstance(item, str):
            calls.append({"name": item, "arguments": {}, "result": None})
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            calls.append({"name": item["name"], "arguments": item.get("arguments") or {},
                          "result": item.get("result")})
    return calls


def get_path(value: Any, path: str) -> Any:
    current = value
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None
    return current


def is_subsequence(expected: list[str], actual: list[str]) -> bool:
    cursor = iter(actual)
    return all(any(item == wanted for item in cursor) for wanted in expected)


def rule_matches(call: dict[str, Any], rule: dict[str, Any]) -> bool:
    if call["name"] != rule["tool"]:
        return False
    value = get_path(call["arguments"], rule["path"])
    if rule.get("nonempty") is True:
        return bool(value)
    return value == rule.get("equals")


def grade_trace(case: dict[str, Any], trace: dict[str, Any]) -> Check:
    expected = case["expected"]
    errors: list[str] = []
    selected = trace.get("skills", trace.get("skill", []))
    if isinstance(selected, str):
        selected = [selected]
    if case["skill"] not in selected:
        errors.append(f"expected skill {case['skill']}, got {selected}")

    calls = tool_calls(trace)
    names = [call["name"] for call in calls]
    missing = [name for name in expected.get("required_tools", []) if name not in names]
    forbidden = [name for name in expected.get("forbidden_tools", []) if name in names]
    if missing:
        errors.append(f"missing tools {missing}")
    if forbidden:
        errors.append(f"forbidden tools {forbidden}")
    ordered = expected.get("ordered_tools", [])
    if ordered and not is_subsequence(ordered, names):
        errors.append(f"tool order expected {ordered}, got {names}")

    for rule in expected.get("required_args", []):
        matching_tool_calls = [call for call in calls if call["name"] == rule["tool"]]
        mode = rule.get("match", "any")
        matches = [rule_matches(call, rule) for call in matching_tool_calls]
        valid = bool(matches) and (all(matches) if mode == "all" else any(matches))
        if not valid:
            requirement = "nonempty" if rule.get("nonempty") else repr(rule.get("equals"))
            errors.append(f"required arg {rule['tool']} {rule['path']}={requirement} ({mode})")
    for rule in expected.get("forbidden_args", []):
        if any(rule_matches(call, rule) for call in calls):
            errors.append(f"forbidden arg {rule['tool']} {rule['path']}={rule['equals']!r}")
    for rule in expected.get("handoffs", []):
        sources = [get_path(call, rule["from_path"]) for call in calls if call["name"] == rule["from_tool"]]
        sources = [value for value in sources if value is not None]
        targets = [get_path(call, rule["to_path"]) for call in calls if call["name"] == rule["to_tool"]]
        handed_off = any(
            source == target or (isinstance(target, list) and source in target)
            for source in sources for target in targets
        )
        if not handed_off:
            errors.append(
                f"missing handoff {rule['from_tool']}:{rule['from_path']} -> "
                f"{rule['to_tool']}:{rule['to_path']}"
            )

    output = str(trace.get("output", "")).lower()
    missing_output = [term for term in expected.get("required_output_terms", []) if term.lower() not in output]
    if missing_output:
        errors.append(f"output missing {missing_output}")
    for group in expected.get("required_output_any", []):
        if not any(term.lower() in output for term in group):
            errors.append(f"output needs one of {group}")
    return Check(case["id"], not errors, "; ".join(errors) if errors else "trace passed")


def print_checks(title: str, checks: list[Check]) -> int:
    print(f"\n{title}\n" + "-" * 72)
    failures = 0
    for check in checks:
        tag = "PASS" if check.passed else "FAIL"
        failures += 0 if check.passed else 1
        print(f"[{tag}] {check.name:34} {check.message}")
    print("-" * 72)
    print(f"{len(checks) - failures} passed, {failures} failed")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES, help="scenario catalog JSON")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY, help="verified hosted tool inventory JSON")
    parser.add_argument(
        "--source-inventory",
        type=Path,
        default=DEFAULT_SOURCE_INVENTORY,
        help="verified simplified-apikit source profile inventory JSON",
    )
    parser.add_argument("--traces", type=Path, help="agent traces as JSON or JSONL")
    parser.add_argument("--allow-missing", action="store_true", help="skip catalog cases absent from traces")
    args = parser.parse_args()

    try:
        cases = load_cases(args.cases)
        inventory = load_json_or_jsonl(args.inventory)
        if not isinstance(inventory, dict):
            raise ValueError("inventory must be a JSON object")
        source_inventory = load_json_or_jsonl(args.source_inventory)
        if not isinstance(source_inventory, dict):
            raise ValueError("source inventory must be a JSON object")
        failures = print_checks(
            "Skill contracts and eval catalog",
            validate_contracts(cases, inventory, source_inventory),
        )
        if args.traces:
            traces = normalize_traces(load_json_or_jsonl(args.traces))
            trace_checks: list[Check] = []
            for case in cases:
                trace = traces.get(case["id"])
                if trace is None:
                    if not args.allow_missing:
                        trace_checks.append(Check(case["id"], False, "trace missing"))
                    continue
                trace_checks.append(grade_trace(case, trace))
            failures += print_checks("Agent trace grading", trace_checks)
        return 1 if failures else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
