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

Bring your **Simplified** marketing workspace into your AI assistant. Generate AI
images and run your whole social presence — draft, schedule, publish, and analyze
across 10 platforms — straight from a conversation in Claude, ChatGPT, Codex, or
Cursor.

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
| **Best for** | Chat-driven image + social with guardrails ("draft before publish", "carry the asset id") | Power users, automations, and clients that don't use Skills |
| **Setup** | One-line install (Claude Code / Codex) | Add one URL to your MCP config |
| **Tools exposed** | The 2 published skills → image generation + the full social suite | Hosted connector: same curated set. Full toolkit: ~100 tools (see below) |
| **Auth** | OAuth via the connector | OAuth via the connector |

Both run on the **same hosted connector** — `https://apikit.simplified.com/mcp`.
The plugin just adds the workflow knowledge on top.

---

## What you can do

**🎨 Generate images** — text-to-image and image-to-image across Flux, Google
(Gemini / Imagen), OpenAI GPT Image, Ideogram, Recraft, Stable Diffusion, Qwen, and
SeeDream. Saved as a reusable **asset** you can drop straight into a post.

**📣 Run social** — draft, schedule, queue, publish, update, and delete posts across
**Facebook, Instagram, TikTok, YouTube, LinkedIn, Pinterest, Threads, Bluesky, and
Google Business**. Manage drafts and tags, bundle drafts into a shareable **review
link**, and pull **analytics** (time-series, per-post, aggregated KPIs, and audience
demographics).

The two compose: generate an image → get an `asset_id` → attach it to a post.

> **More than images + social.** The hosted connector ships a curated set focused on
> the two published skills. The complete Simplified platform — **project management,
> brand kits, projects, AI video & audio, image editing, transcription, long-form
> documents** — is exposed by the full toolkit. Jump to
> [The full platform](#the-full-platform--simplified-apikit).

---

## Install

### Claude Code
```
/plugin marketplace add celeryhq/simplified-ai
/plugin install simplified-ai@simplified-ai
```

### Any agent (via [skills.sh](https://skills.sh))
```
npx skills add celeryhq/simplified-ai
```
Add a single skill with `--skill generate-image` or `--skill simplified-social`.

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
- **Curated tool set.** Ships the tools behind the two published skills: the full
  **social** suite plus **image generation** — focused, and small enough to fit
  app-directory review forms.
- This is what the **plugin**, the **ChatGPT App**, and **Claude.ai Custom
  Connectors** all talk to.

### The full platform — `simplified-apikit`

The hosted connector is a deliberately curated slice. The complete platform lives in
the **`simplified-apikit`** toolkit, which is *three things in one package*:

- **`smp`** — a CLI that drives Simplified from your terminal
- **`smp serve`** — a local MCP server (stdio or HTTP) for Claude Desktop, Cursor,
  Cline, or any MCP host
- the agent toolkit powering Simplified's own assistants

In its default (`full`) profile it exposes **~100 tools across 5 namespaces** — the
capabilities the curated connector leaves out:

| Namespace | Tools | What it adds beyond the plugin |
|---|---:|---|
| **`pm`** | 29 | **Project management** — boards, statuses, tasks, subtasks, dependencies, assignees, tags, custom fields, search |
| **`api`** | 36 | **Brand kits** (V2 build + context documents), **projects & items**, **AI image + video** generation, **text-to-speech**, **assets**, **long-form documents**, comments |
| **`social`** | 16 | The full social + analytics suite (same as the connector) |
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
set. On a `401` the client refreshes its token automatically (the server emits the
standard `WWW-Authenticate` challenge).

---

## Key behavior (see [AGENTS.md](AGENTS.md))

- **Confirm before spending credits** (image generation) or **publishing** (social).
- **Draft → confirm → publish** for social posts; never publish without confirmation.
- **"Post now" → `add_to_queue`** — the `action` enum is `schedule | add_to_queue | draft`.
- **Carry the `asset_id`, not the URL** — generated-image URLs are signed and expire;
  the asset id is permanent and is what the social `media` field accepts.
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
├── .agents/plugins/             ← Codex marketplace catalog
├── .mcp.json                    ← hosted MCP connector (OAuth) — shared by all clients
├── AGENTS.md                    ← agent behavior & safety conventions
├── SKILL_TREE.md                ← index of skills
├── docs/
│   └── MCP.md                   ← full MCP reference (toolkit, profiles, tool catalog)
├── skills/
│   ├── generate-image/          ← text-to-image workflow  (api_generateImage)
│   └── simplified-social/       ← post / schedule / draft / analyze  (social_*)
├── assets/                      ← brand icon + logo
├── evals/                       ← contributor QA harness (not installed)
├── submission/                  ← app-directory submission artifacts
└── LICENSE
```

---

## Status

- [x] Hosted connector live: `apikit.simplified.com/mcp` (OAuth + token refresh).
- [x] Works as a Claude.ai / Desktop **Custom Connector**.
- [x] Claude Code plugin verified end-to-end (marketplace + plugin + MCP).
- [x] `action` semantics verified against backend (`add_to_queue` = publish ASAP).
- [x] Codex marketplace config complete (`.codex-plugin/` + `.agents/plugins/marketplace.json`).
- [x] Claude Connectors Directory submission prepared (`submission/claude-directory.md`).
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
