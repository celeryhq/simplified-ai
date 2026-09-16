#!/usr/bin/env python3
"""Build the curated skill bundle uploaded to the ChatGPT Apps submission form.

The plugin manifest ships `skills/` by glob, so Claude Code and skills.sh receive
every folder. The ChatGPT Apps submission is a separate surface with a narrower
audience: it runs against the hosted connector only, with no shell. This script
produces the subset appropriate to that surface.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

# Skills deliberately withheld from the ChatGPT Apps bundle, with the reason each
# one is withheld. A skill is excluded here rather than deleted because it stays
# valid for other surfaces.
EXCLUDED: dict[str, str] = {
    "simplified-cli": (
        "drives the `smp` shell command, not the hosted connector; there is no "
        "shell in the ChatGPT app surface"
    ),
    "simplified-workflows": (
        "calls flows_* tools served by the /automation/mcp mount, which this "
        "plugin does not declare; unusable against apikit.simplified.com/mcp"
    ),
}

# Tool namespaces served by https://apikit.simplified.com/mcp. A skill in the
# bundle that calls anything outside these cannot work for a reviewer.
CONNECTOR_NAMESPACES = ("api_", "media_", "notify_", "pm_", "social_")

# Tool names are `namespace_camelCaseOperation`, so the operation half always
# carries an uppercase letter. Requiring one is what separates a tool call from
# the snake_case parameter names that fill these documents (`asset_id`,
# `per_page`, `rich_description`).
TOOL_CALL_RE = re.compile(r"\b([a-z][a-z0-9]*)_([a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*)\b")


class CodexSkillBundle:
    """Selects, checks, and packages the skills for the submission form."""

    @staticmethod
    def select() -> list[Path]:
        skills = sorted(p for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())
        return [p for p in skills if p.name not in EXCLUDED]

    @staticmethod
    def unknown_tool_namespaces(skill: Path) -> set[str]:
        """Tool-looking identifiers whose namespace the connector does not serve.

        This is the guard for the failure that reached a release: a skill calling
        a namespace that exists in the wider platform but not on the endpoint the
        plugin ships.
        """
        found: set[str] = set()
        for md in skill.rglob("*.md"):
            for namespace, operation in TOOL_CALL_RE.findall(md.read_text()):
                tool = f"{namespace}_{operation}"
                if not tool.startswith(CONNECTOR_NAMESPACES):
                    found.add(tool)
        return found

    @staticmethod
    def check(skill: Path) -> list[str]:
        problems: list[str] = []
        if not (skill / "agents" / "openai.yaml").is_file():
            problems.append("missing agents/openai.yaml (no Codex UI metadata)")
        if not (skill / "SKILL.md").read_text().startswith("---"):
            problems.append("SKILL.md has no frontmatter")
        unknown = CodexSkillBundle.unknown_tool_namespaces(skill)
        if unknown:
            problems.append(f"calls tools outside the connector: {', '.join(sorted(unknown))}")
        return problems

    @staticmethod
    def write_zip(target: Path, files: list[tuple[Path, str]]) -> None:
        """Write a deterministic zip so rebuilds are byte-identical."""
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            for source, arcname in sorted(files, key=lambda pair: pair[1]):
                info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                zf.writestr(info, source.read_bytes())

    @staticmethod
    def skill_files(skill: Path) -> list[tuple[Path, str]]:
        return [
            (f, str(f.relative_to(skill.parent)))
            for f in sorted(skill.rglob("*"))
            if f.is_file() and not f.name.startswith(".")
        ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "dist" / "codex",
        help="output directory (default: dist/codex)",
    )
    parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="package anyway when a skill fails its checks",
    )
    args = parser.parse_args()

    selected = CodexSkillBundle.select()
    if not selected:
        print("No skills selected — check EXCLUDED and skills/.", file=sys.stderr)
        return 1

    print(f"Excluded {len(EXCLUDED)}:")
    for name, reason in sorted(EXCLUDED.items()):
        print(f"  - {name}: {reason}")

    print(f"\nIncluded {len(selected)}:")
    failures: dict[str, list[str]] = {}
    for skill in selected:
        problems = CodexSkillBundle.check(skill)
        marker = "ok " if not problems else "FAIL"
        print(f"  [{marker}] {skill.name}")
        for problem in problems:
            print(f"         {problem}")
        if problems:
            failures[skill.name] = problems

    if failures and not args.allow_warnings:
        print(
            f"\n{len(failures)} skill(s) failed. Fix them, exclude them, "
            "or re-run with --allow-warnings.",
            file=sys.stderr,
        )
        return 1

    if args.out.exists():
        shutil.rmtree(args.out)
    per_skill = args.out / "per-skill"
    tree = args.out / "skills"

    combined: list[tuple[Path, str]] = []
    for skill in selected:
        files = CodexSkillBundle.skill_files(skill)
        combined.extend(files)
        CodexSkillBundle.write_zip(per_skill / f"{skill.name}.zip", files)
        shutil.copytree(skill, tree / skill.name)

    bundle = args.out / "simplified-ai-skills.zip"
    CodexSkillBundle.write_zip(bundle, combined)

    manifest = args.out / "MANIFEST.txt"
    manifest.write_text(
        "Curated skill bundle for the ChatGPT Apps submission form.\n"
        f"Included ({len(selected)}): {', '.join(s.name for s in selected)}\n\n"
        "Excluded:\n"
        + "".join(f"  {name}: {reason}\n" for name, reason in sorted(EXCLUDED.items()))
        + "\nUpload one of:\n"
        f"  {bundle.relative_to(ROOT)}         all skills in one zip\n"
        f"  {per_skill.relative_to(ROOT)}/<skill>.zip   one skill at a time\n"
        f"  {tree.relative_to(ROOT)}/          drop as a folder\n"
    )

    print(f"\nWrote {len(selected)} skills to {args.out.relative_to(ROOT)}/")
    print(f"  simplified-ai-skills.zip   all {len(selected)} in one zip")
    print(f"  per-skill/<skill>.zip      {len(selected)} individual zips")
    print("  skills/                    plain folder")
    print("  MANIFEST.txt               what is in, what is out, and why")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
