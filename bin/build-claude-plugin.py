#!/usr/bin/env python3
"""Build the plugin submitted to the Claude directory into plugins/claude/.

The directory's Software Directory Policy 4(B) disallows AI image, video and
audio generation, so the listed plugin is a separate, narrower build of this
repo's skills. It connects only to the `claude` profile of the hosted connector,
which serves an explicit allowlist with no generation tools. The directory reads
from GitHub, so the output is committed; `--check` fails when it has drifted
from the skills it is built from.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
OUT = ROOT / "plugins" / "claude"

NAME = "simplified"
VERSION = "1.0.0"
CONNECTOR_URL = "https://apikit.simplified.com/claude/mcp"
FULL_PLUGIN_INSTALL = "/plugin marketplace add celeryhq/simplified-ai"

# Explicit allowlist: a skill added to this repo stays out of the listed plugin
# until it is named here and its tools are on the claude profile.
INCLUDED = (
    "campaign-review",
    "evergreen-content-engine",
    "local-business-marketing",
    "manage-assets",
    "manage-brand",
    "manage-projects",
    "repurpose-video",
    "simplified-project-management",
    "simplified-social",
    "simplified-workspace",
    "social-content-planner",
    "social-performance-analyst",
    "transcribe-media",
)

# The AI media tools the claude profile withholds. A skill that names one
# instructs the model to call a tool the listed connector does not serve.
AI_MEDIA_TOOLS = frozenset(
    {
        "api_generateImage",
        "api_generateVideo",
        "api_generateAudio",
        "media_textToVideo",
        "media_scriptToVideo",
        "media_addBRollsVideo",
        "media_generativeFill",
        "media_magicInpaint",
        "media_imageOutpainting",
        "media_sdScribble",
        "media_replaceImageBackground",
        "media_restoreImage",
        "media_upscaleImage",
        "media_blurBackground",
        "media_removeBackground",
        "media_removeVideoBackground",
    }
)

# Namespaces the claude profile serves. A tool-looking name outside these is a
# call the listed connector cannot answer.
SERVED_NAMESPACES = ("api_", "media_", "pm_", "social_")

# Tool names are `namespace_camelCaseOperation`; the uppercase letter separates
# them from the snake_case parameter names that fill the skill documents.
TOOL_CALL_RE = re.compile(r"\b([a-z][a-z0-9]*)_([a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*)\b")
KNOWN_NAMESPACES = ("agents_", "api_", "flows_", "media_", "notify_", "pm_", "smp_", "social_")


class ClaudePluginBuild:
    """Checks the included skills and writes the plugin tree."""

    @staticmethod
    def tool_calls(skill: Path) -> set[str]:
        found: set[str] = set()
        for md in skill.rglob("*.md"):
            found.update(f"{ns}_{op}" for ns, op in TOOL_CALL_RE.findall(md.read_text()))
        return {tool for tool in found if tool.startswith(KNOWN_NAMESPACES)}

    @staticmethod
    def problems(skill: Path) -> list[str]:
        if not (skill / "SKILL.md").is_file():
            return ["missing SKILL.md"]
        tools = ClaudePluginBuild.tool_calls(skill)
        problems: list[str] = []
        media = sorted(tools & AI_MEDIA_TOOLS)
        if media:
            problems.append(f"names AI media tools: {', '.join(media)}")
        unserved = sorted(t for t in tools if not t.startswith(SERVED_NAMESPACES))
        if unserved:
            problems.append(f"calls tools outside the claude profile: {', '.join(unserved)}")
        return problems

    @staticmethod
    def manifest() -> str:
        manifest = {
            "name": NAME,
            "version": VERSION,
            "description": (
                "Draft, schedule and review social posts, manage brand context, "
                "assets, projects and tasks, and read analytics in Simplified."
            ),
            "author": {"name": "Simplified", "url": "https://simplified.com"},
            "homepage": "https://simplified.com",
            "repository": "https://github.com/celeryhq/simplified-ai",
            "license": "MIT",
            "keywords": [
                "social-media",
                "social-media-scheduling",
                "social-media-analytics",
                "content-calendar",
                "brand-management",
                "project-management",
                "simplified",
            ],
        }
        return f"{json.dumps(manifest, indent=2)}\n"

    @staticmethod
    def mcp_config() -> str:
        config = {"mcpServers": {"simplified": {"type": "http", "url": CONNECTOR_URL}}}
        return f"{json.dumps(config, indent=2)}\n"

    @staticmethod
    def readme() -> str:
        return f"""\
# Simplified

Skills for working with [Simplified](https://simplified.com) from Claude. They
cover drafting, scheduling and reviewing social posts, planning content
calendars, reading performance analytics, managing brand context, assets and
projects, tracking tasks on project boards, and turning recordings into
transcripts and short clips.

The skills need the Simplified connector, which this plugin configures at
`{CONNECTOR_URL}`. Sign in with your Simplified account when Claude asks, then
ask "Which Simplified workspace am I connected to?" to confirm the scope.

Posts are saved as drafts first. Nothing is scheduled or published without your
explicit go-ahead.

A version that also generates images, video and audio is available separately:
`{FULL_PLUGIN_INSTALL}`.

Source and licence: https://github.com/celeryhq/simplified-ai (MIT).
"""

    @staticmethod
    def write(out: Path) -> None:
        if out.exists():
            shutil.rmtree(out)
        (out / ".claude-plugin").mkdir(parents=True)
        (out / ".claude-plugin" / "plugin.json").write_text(ClaudePluginBuild.manifest())
        (out / ".mcp.json").write_text(ClaudePluginBuild.mcp_config())
        (out / "README.md").write_text(ClaudePluginBuild.readme())
        shutil.copy(ROOT / "LICENSE", out / "LICENSE")
        for name in INCLUDED:
            shutil.copytree(
                SKILLS_DIR / name,
                out / "skills" / name,
                ignore=shutil.ignore_patterns("agents", ".DS_Store"),
            )

    @staticmethod
    def differences(left: Path, right: Path) -> list[str]:
        diff = filecmp.dircmp(left, right)
        found = [f"only in built: {n}" for n in diff.left_only]
        found += [f"only in committed: {n}" for n in diff.right_only]
        found += [f"differs: {n}" for n in diff.diff_files]
        for sub in diff.common_dirs:
            found += [f"{sub}/{d}" for d in ClaudePluginBuild.differences(left / sub, right / sub)]
        return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="build to a temp directory and fail if plugins/claude differs",
    )
    args = parser.parse_args()

    failures = {n: ClaudePluginBuild.problems(SKILLS_DIR / n) for n in INCLUDED}
    failures = {n: p for n, p in failures.items() if p}
    for name, problems in failures.items():
        for problem in problems:
            print(f"{name}: {problem}", file=sys.stderr)
    if failures:
        return 1

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            built = Path(tmp) / "claude"
            ClaudePluginBuild.write(built)
            if not OUT.is_dir():
                print(f"{OUT.relative_to(ROOT)} is missing; run bin/build-claude-plugin.py", file=sys.stderr)
                return 1
            drift = ClaudePluginBuild.differences(built, OUT)
        if drift:
            print("plugins/claude is stale; run bin/build-claude-plugin.py", file=sys.stderr)
            print("\n".join(f"  {line}" for line in drift), file=sys.stderr)
            return 1
        print("plugins/claude is current")
        return 0

    ClaudePluginBuild.write(OUT)
    print(f"Wrote {len(INCLUDED)} skills to {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
