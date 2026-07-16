<p align="center">
  <img src="assets/simplified-logo.png" alt="Simplified" width="120" />
</p>

<h1 align="center">Simplified for AI</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT" />
  <img src="https://img.shields.io/badge/clients-Claude%20Code%20%7C%20Codex-7C3AED.svg" alt="Clients: Claude Code | Codex" />
  <img src="https://img.shields.io/badge/MCP-hosted%20connector-FFAD00.svg" alt="MCP: hosted connector" />
  <img src="https://img.shields.io/badge/auth-OAuth-brightgreen.svg" alt="Auth: OAuth" />
</p>

Bring your **Simplified** marketing workspace into your AI assistant. Manage brand
context and content operations, generate reusable image and video assets, and run
your social presence across 13 platforms—through shared skills for Claude, ChatGPT,
Codex, and Cursor.

Under the hood it's a **Model Context Protocol (MCP)** connector. This repo ships
the **plugin** — a curated, safety-railed front-end over that connector — but the
same hosted MCP can be wired into any MCP-capable client directly, and the wider
Simplified platform (project management, brand kits, video & audio tools,
transcription, documents) is available through the full toolkit.

> **TL;DR** — Want a guided experience? Install the **plugin** (below). Want raw
> tools in your own client? Point it at `https://apikit.simplified.com/mcp`. Want
> the entire Simplified platform (PM, brand kits, media editing)? See
> [the full MCP toolkit](#the-full-platform--simplified-apikit) and
> [docs/MCP.md](docs/MCP.md).

---

## Two ways in

| | **Plugin (this repo)** | **MCP connector (direct)** |
|---|---|---|
| **What it is** | Curated [Skills](https://docs.claude.com/en/docs/agents-and-tools) that teach the assistant *how* to use the tools — sequencing, terminology, safety rails | The raw tool surface, callable by any MCP client |
| **Best for** | Marketer workflows: plan, create, repurpose, review, publish, and improve—with guardrails | Power users, automations, and clients that don't use Skills |
| **Setup** | One-line install (Claude Code / Codex) | Add one URL to your MCP config |
| **Guided workflows** | 14 skills: 6 platform operators + 8 marketer workflows | Hosted connector: 105 live tools verified July 15, 2026. Full local toolkit: 106 tools |
| **Auth** | OAuth via the connector | OAuth via the connector |

Both run on the **same hosted connector** — `https://apikit.simplified.com/mcp`.
The plugin just adds the workflow knowledge on top.

---

## What you can do

**🎨 Generate images** — text-to-image and image-to-image across Flux, Google
(Gemini / Imagen), OpenAI GPT Image, Ideogram, Recraft, Stable Diffusion, Qwen, and
SeeDream. Saved as a reusable **asset** you can drop straight into a post.

**🎬 Generate videos** — discover current model capabilities, create text- or
reference-guided motion, poll real render completion, and retain reusable assets.

**🧭 Manage brand context** — structure approved identity, voice, audiences,
positioning, proof, content pillars, and visual rules as reusable brand knowledge.

**✅ Run content operations** — turn approved plans into projects, accountable
deliverables, review gates, comments, assignments, and controlled exports.

**📣 Run social** — draft, schedule, queue, publish, update, and delete posts across
**Facebook, Instagram, TikTok, YouTube, LinkedIn, Pinterest, Threads, Bluesky,
X/Twitter, Google Business, Mastodon, Reddit, and Telegram**. Add timed
auto-comments for patterns such as “link in first comment,” manage drafts and tags,
bundle drafts into a shareable **review link**, and pull **analytics** (time-series,
per-post, aggregated KPIs, and audience demographics).

**🗓️ Plan content** — turn goals, audiences, offers, and key dates into practical
weekly or monthly calendars with channel-aware content pillars and cadence.

**🚀 Run campaigns** — adapt one launch or promotion across channels, generate
reusable campaign assets, create drafts, and package them for stakeholder review.

**♻️ Repurpose content** — turn articles, announcements, transcripts, case studies,
and events into distinct channel-native posts without inventing claims.

**🌱 Build evergreen programs** — create durable territories, recurring franchises,
a content bank, and explicit refresh and retirement rules.

**📍 Grow local businesses** — coordinate verified location content and Google
Business drafts around visits, calls, bookings, directions, and timely demand.

**🧪 Test creative** — design controlled hook, proof, format, visual, and CTA tests
with decision metrics and reusable learning—not random variations.

**📊 Improve performance** — combine account KPIs, trends, post-level results, and
audience data into prioritized actions and measurable next experiments.

The workflows compose: plan or repurpose content → generate reusable assets → create
channel-native drafts → review → confirm → schedule or queue → analyze results.

> **Live verification.** On July 15, 2026, an authenticated Codex initialization
> exposed 105 hosted tools. Workspace/teamspace discovery, model discovery, credits,
> brand kits, projects, social accounts, analytics, image generation, and social
> draft updates all passed live smoke tests. A complete draft-to-image flow was also
> verified across Simplified's LinkedIn, Facebook, Google Business, and X/Twitter
> accounts without publishing. The local `full` profile exposes 106 tools; the
> hosted profile is currently one operation smaller.

---

## Install

### Claude Code
```
/plugin marketplace add celeryhq/simplified-ai
/plugin install simplified-ai@simplified-ai
```

### Any agent (via [skills.sh](https://skills.sh))

Install from the repository and let the CLI detect your available agents:

```
npx skills add celeryhq/simplified-ai
```

Useful installation variants:

```bash
# Preview the available skills without installing
npx skills add celeryhq/simplified-ai --list

# Install selected skills
npx skills add celeryhq/simplified-ai \
  --skill generate-image \
  --skill simplified-social

# Install every skill for Codex and Claude Code
npx skills add celeryhq/simplified-ai \
  --skill '*' \
  --agent codex \
  --agent claude-code

# Install globally so the skills are available in every project
npx skills add celeryhq/simplified-ai --all --global
```

See [SKILL_TREE.md](SKILL_TREE.md) for the complete marketer-focused catalog.

#### Update an existing skills.sh installation

The CLI records the source and can refresh installed skills when this repository
changes:

```bash
# Update all installed project or global skills (interactive scope selection)
npx skills update

# Update only project-scoped or global skills
npx skills update --project
npx skills update --global

# Update one or more Simplified skills by name
npx skills update generate-image simplified-social

# Non-interactive update; project scope inside a project, otherwise global
npx skills update --yes

# Confirm what is installed afterward
npx skills list
```

Project installs are the default and can be committed with the project. Use
`--global` when the skills should be available across projects. The skills.sh CLI
supports Codex, Claude Code, Cursor, and other compatible agents; use repeated
`--agent <name>` flags to target specific clients.

### ChatGPT (Apps)
Enable the **Simplified** app — it's backed by the hosted MCP connector, so there's
nothing to install. *(Submission in progress — see [Status](#status).)*

### Claude.ai / Claude Desktop (Custom Connector)
Add a Custom Connector pointing at `https://apikit.simplified.com/mcp` and complete
the OAuth flow. No API key.

### Codex / Cursor / any MCP client
Add the connector to your client's MCP config:

```json
{
  "mcpServers": {
    "simplified": { "type": "http", "url": "https://apikit.simplified.com/mcp" }
  }
}
```

On first use the client walks the OAuth flow; tokens refresh automatically. (Codex
also supports a plugin install — see [Status](#status) for verification state.)

---

## The MCP behind the plugin

Everything in this repo is a front-end over one hosted MCP server.

### Hosted connector — `apikit.simplified.com/mcp`

- **Public, OAuth-secured, zero-install.** OAuth 2.0 Authorization Code + PKCE with
  Dynamic Client Registration; no API key to manage, tokens refresh on expiry.
- **Expanded hosted tool set.** An authenticated Codex initialization on July 15,
  2026 exposed **105 tools**, including workspace/teamspace discovery, assets, AI
  image and video generation, brand kits and context documents, marketing projects,
  social publishing and review, and analytics. See [docs/MCP.md](docs/MCP.md) for the
  namespace and profile breakdown.
- This is what the **plugin**, the **ChatGPT App**, and **Claude.ai Custom
  Connectors** all talk to.

### The full platform — `simplified-apikit`

The hosted connector is the public, zero-install path to a near-complete Simplified
tool surface. The distributable platform toolkit lives in **`simplified-apikit`**,
which is *three things in one package*:

- **`smp`** — a CLI that drives Simplified from your terminal
- **`smp serve`** — a local MCP server (stdio or HTTP) for Claude Desktop, Cursor,
  Cline, or any MCP host
- the agent toolkit powering Simplified's own assistants

Its default (`full`) profile exposes **106 tools across 5 namespaces**:

| Namespace | Tools | What it covers |
|---|---:|---|
| **`pm`** | 29 | **Project management** — boards, statuses, tasks, subtasks, dependencies, assignees, tags, custom fields, search |
| **`api`** | 39 | **Brand kits** (V2 build + context documents), **projects & items**, **AI image + video** generation, **credits**, **text-to-speech**, **assets**, **long-form documents**, comments |
| **`social`** | 16 | The full social + analytics suite; the local full profile currently has one additional operation beyond the hosted profile |
| **`media`** | 21 | **Image editing** (bg removal, upscale, outpaint, inpaint, restore, convert), **video editing** (merge, trim, speed, reverse, B-roll, text/script-to-video), **transcription** |
| **`notify`** | 1 | Agent notifications |

The `full` toolkit (the `simplified-apikit` CLI) is distributed to Simplified
workspaces. The hosted connector above is the public, zero-install path. Profiles,
the per-namespace tool catalog, and connect-from-any-client instructions are in
**[docs/MCP.md](docs/MCP.md)**.

---

## Connector & auth

The connector is declared in [`.mcp.json`](.mcp.json):

```json
{ "mcpServers": { "simplified": { "type": "http", "url": "https://apikit.simplified.com/mcp" } } }
```

OAuth-secured — the client walks the OAuth flow on first use; there's no API key to
set. The server uses stateless OAuth validation and emits the standard
`WWW-Authenticate` challenge when a token must be refreshed. Fresh and concurrent
Codex sessions were verified successfully on July 15, 2026.

---

## Key behavior (see [AGENTS.md](AGENTS.md))

- **Confirm before spending credits** (image/video generation) or **publishing** (social).
- **Draft → confirm → publish** for social posts; never publish without confirmation.
- **"Post now" → `add_to_queue`** — the `action` enum is `schedule | add_to_queue | draft`.
- **First comments use post-relative delays** — convert “after X minutes” to
  `comments[0].delay = X * 60` seconds and preview the text and delay before publishing.
- **Carry the `asset_id`, not the URL** — generated-image URLs are signed and expire;
  the asset id is permanent and is what the social `media` field accepts.
- **Resolve workspace scope first** — when a workspace or teamspace is named or
  uncertain, resolve its exact ID and carry that scope through downstream calls.
- **Show returned URLs as links, never embeds** — signed asset and review URLs should
  remain clickable instead of being fetched inline by the client.
- **Stop if not connected** — if no social accounts are returned, ask the user to
  connect one rather than attempting to post.

---

## Repo layout

```
simplified-ai/
├── .claude-plugin/
│   ├── marketplace.json         ← Claude Code marketplace catalog
│   └── plugin.json              ← Claude Code plugin manifest
├── .codex-plugin/plugin.json    ← Codex / ChatGPT Apps manifest
├── .codex/config.toml           ← Codex workspace MCP configuration
├── .agents/plugins/             ← Codex marketplace catalog
├── .github/workflows/evals.yml  ← deterministic contract and fixture checks
├── .mcp.json                    ← hosted MCP connector (OAuth) — shared by all clients
├── AGENTS.md                    ← agent behavior & safety conventions
├── SKILL_TREE.md                ← index of skills
├── docs/
│   └── MCP.md                   ← full MCP reference (toolkit, profiles, tool catalog)
├── skills/
│   ├── generate-image/          ← text-to-image workflow  (api_generateImage)
│   ├── generate-video/          ← model-aware AI video generation
│   ├── simplified-workspace/    ← whoami + workspace/teamspace resolution
│   ├── simplified-social/       ← social operations + platform rules  (social_*)
│   ├── manage-brand/            ← brand kits + reusable context
│   ├── manage-projects/         ← projects + content operations
│   ├── social-content-planner/  ← goal-led calendars and draft plans
│   ├── cross-platform-campaign/ ← coordinated multi-channel rollouts
│   ├── content-repurposer/      ← source content → channel-native posts
│   ├── evergreen-content-engine/ ← durable content program + renewal loop
│   ├── local-business-marketing/ ← local and Google Business workflows
│   ├── creative-testing/        ← controlled creative experiments
│   ├── social-performance-analyst/ ← metrics → decisions and experiments
│   └── campaign-review/         ← stakeholder review bundles and revisions
├── assets/                      ← brand icon + logo
├── evals/                       ← contributor QA harness (not installed)
└── LICENSE
```

---

## Status

- [x] Hosted connector live: `apikit.simplified.com/mcp` (OAuth + token refresh).
- [x] Stateless OAuth verified across fresh and concurrent Codex sessions; no
  `SessionExpired404` observed after the backend fix.
- [x] Expanded hosted profile live: 105 tools observed in authenticated discovery.
- [x] Live operator smoke tests passed for workspace/teamspaces, model fields,
  credits, brand kits, projects, social accounts, and analytics.
- [x] End-to-end image-to-social flow verified on four Simplified main accounts;
  drafts were updated with media and nothing was published.
- [x] Works as a Claude.ai / Desktop **Custom Connector**.
- [x] Claude Code plugin verified end-to-end (marketplace + plugin + MCP).
- [x] `action` semantics verified against backend (`add_to_queue` = publish ASAP).
- [x] Codex marketplace config complete (`.codex-plugin/` + `.agents/plugins/marketplace.json`).
- [ ] Codex legacy migration: existing `simplified-for-ai` installations need a
  one-time remove/reinstall path to move to the canonical `simplified-ai` identity.
- [ ] ChatGPT App submission (pending business verification).
- [ ] Claude Connectors Directory listing live (pending Anthropic review).
- [ ] Cursor plugin install.

---

## Contributing

Skills follow the [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools)
spec — a `SKILL.md` per directory plus optional `agents/openai.yaml` (Codex metadata)
and `references/` for deep detail. The [`evals/`](evals/) harness holds test cases and
a runnable I/O check (not shipped with the plugin).

When an AI agent commits to this repo, include a `Co-Authored-By:` line naming the
model.

## License

See [LICENSE](LICENSE).
