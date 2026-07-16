# AGENTS.md — Simplified for AI

Operational guidance for AI coding assistants (Codex, Claude Code, Cursor) using
this plugin.

## Project overview

Simplified for AI lets agents operate Simplified's **image/video generation,
assets, brand context, marketing projects, and social media**, then compose those
platform primitives into marketer workflows — through:

- **Skills** ([skills/](skills/)) — `SKILL.md` workflow files that teach the agent
  sequencing, terminology, and safety behavior.
- **A hosted MCP connector** — the tools the skills drive, served at
  `https://apikit.simplified.com/mcp` (OAuth-secured). Declared in
  [.mcp.json](.mcp.json).

## Plugin structure

```
simplified-ai/
├── .mcp.json                 # hosted MCP connector (OAuth) — shared by all clients
├── .claude-plugin/plugin.json   # Claude Code manifest
├── .codex-plugin/plugin.json    # Codex / ChatGPT Apps manifest
├── skills/                   # SKILL.md workflows (Agent Skills spec)
│   ├── generate-image/
│   ├── generate-video/
│   ├── simplified-workspace/
│   ├── simplified-social/
│   ├── manage-brand/
│   ├── manage-projects/
│   ├── social-content-planner/
│   ├── cross-platform-campaign/
│   ├── content-repurposer/
│   ├── evergreen-content-engine/
│   ├── local-business-marketing/
│   ├── creative-testing/
│   ├── social-performance-analyst/
│   └── campaign-review/
├── assets/                   # brand icon + logo
└── evals/                    # test cases + runnable I/O harness
```

## Skills

| Skill | Purpose | Tools |
|---|---|---|
| [generate-image](skills/generate-image/SKILL.md) | Text-to-image generation (Flux, Gemini/Imagen, GPT Image, Ideogram, …); saves as a reusable asset | `api_generateImage` |
| [generate-video](skills/generate-video/SKILL.md) | Model-aware AI video generation and render polling | `api_getModelFields`, `api_generateVideo`, `api_getVideoVariation` |
| [simplified-workspace](skills/simplified-workspace/SKILL.md) | Authenticated identity, workspace settings, and safe teamspace discovery | workspace and teamspace tools |
| [simplified-social](skills/simplified-social/SKILL.md) | Draft / schedule / queue posts + analytics across 10 platforms | `social_*` |
| [manage-brand](skills/manage-brand/SKILL.md) | Evidence-led brand kits and reusable brand context | brand-kit and context-document tools |
| [manage-projects](skills/manage-projects/SKILL.md) | Marketing projects, deliverables, assignments, and exports | project and item tools |
| [social-content-planner](skills/social-content-planner/SKILL.md) | Goal-led weekly and monthly content calendars | accounts, analytics, drafts, scheduling |
| [cross-platform-campaign](skills/cross-platform-campaign/SKILL.md) | Coordinated channel-native campaign rollouts | image generation + social |
| [content-repurposer](skills/content-repurposer/SKILL.md) | Source content into channel-native post sequences | drafts + optional image generation |
| [evergreen-content-engine](skills/evergreen-content-engine/SKILL.md) | Durable content territories, franchises, content bank, and renewal loop | accounts, analytics, drafts |
| [local-business-marketing](skills/local-business-marketing/SKILL.md) | Verified local and Google Business programs | accounts, assets, drafts, platform settings |
| [creative-testing](skills/creative-testing/SKILL.md) | Controlled creative experiments and reusable learning | analytics, generation, drafts |
| [social-performance-analyst](skills/social-performance-analyst/SKILL.md) | KPI, trend, post, and audience analysis with next actions | social analytics |
| [campaign-review](skills/campaign-review/SKILL.md) | Draft QA, revisions, and stakeholder review bundles | drafts + review bundles |

The outcome-driven skills compose the six platform operators. Workspace identity
establishes the scope for every other operator. Image and video
generation return permanent **asset IDs** for `simplified-social.media`; brand and
project skills provide reusable context and operational handoffs. Workflow skills
orchestrate those primitives around marketer jobs without duplicating API mechanics.

## MCP server

Same connector for every client, configured in [.mcp.json](.mcp.json):

```json
{ "mcpServers": { "simplified": { "type": "http", "url": "https://apikit.simplified.com/mcp" } } }
```

OAuth-secured — the client walks the OAuth flow; no API key to set. On a 401, the
client refreshes its token automatically (server emits the standard challenge).

## Key conventions (agent behavior)

- **Confirm before spending credits.** Image/video generation and social publishing
  consume credits / post to live accounts — confirm when intent is ambiguous.
- **Resolve scope before scoped work.** Use `api_getWorkspaceInfo` as `whoami` when
  workspace/teamspace context is named or uncertain. Resolve names to exact numeric
  IDs, then pass `space_id` on every downstream tool call in that scoped task.
- **Draft before publish.** For social posts, create a `draft` and show it before
  scheduling/queuing. Never publish without explicit user confirmation.
- **"Post now" → `add_to_queue`** (publishes ASAP). There is no separate immediate
  publish action; the `action` enum is `schedule | add_to_queue | draft`.
- **Carry the `asset_id`, not the URL.** Generated-image URLs are signed and expire;
  the `asset_id` is permanent and is what `simplified-social.media` accepts.
- **Show returned URLs as links — never embed them.** Any URL a tool or skill
  returns (image results, asset URLs, review-bundle links, exports) must be shown as
  a plain URL or a Markdown link — **never** Markdown image syntax (`![alt](url)`)
  and never anything that makes the client fetch/render the asset inline. The user
  clicks the link; the agent does not render it. Inline rendering breaks on signed/
  expiring URLs and produces poor UX (e.g. Codex trying to display the image instead
  of showing a clickable URL).
- **Stop if not connected.** If `social_getSocialMediaAccounts` is empty, tell the
  user to connect an account — don't attempt to post.

## Commit attribution

When an AI agent commits to this repo, include a `Co-Authored-By:` line with the
agent model's name.
