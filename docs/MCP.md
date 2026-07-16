# Simplified MCP — full reference

This document covers the MCP connector behind **Simplified for AI** in depth: the
hosted connector, the full `simplified-apikit` toolkit, tool **profiles**, the
complete per-namespace tool catalog, authentication, and how to connect from any
MCP client.

If you just want the guided plugin, start at the [README](../README.md). This page
is for power users, automation, and anyone who needs more than image generation +
social.

---

## The two surfaces

There is **one toolkit codebase** (`simplified-apikit`, built on
[FastMCP](https://gofastmcp.com)) exposed through two surfaces. The hosted deployment
uses a curated allowlist; `smp serve` uses a local profile:

| Surface | URL / entry | Profile | Tools | Install |
|---|---|---|---|---|
| **Hosted connector** | `https://apikit.simplified.com/mcp` | deployed allowlist | 105 verified live | none — OAuth |
| **Full toolkit** | `smp serve` (local stdio/HTTP) | `full` | 106 (all namespaces) | `pipx install simplified-apikit` |

Both auto-generate tool schemas from OpenAPI specs. Because the hosted allowlist is
deployed independently, keep its inventory under test; the verified snapshot lives
in [`evals/hosted-tool-inventory.json`](../evals/hosted-tool-inventory.json).

---

## Profiles

The server selects a **tool profile** via the `SMP_PROFILE` env var (or
`--profile` on `smp serve`):

| Profile | Tools | Purpose |
|---|---|---|
| `mcp` | 49 tools: workspace identity, teamspace discovery, social, image/video generation, assets, brand context, and marketing projects | A compact local profile for marketer workflows. |
| `full` | everything (106) | Default for the CLI and `smp serve`. The entire platform. |

```bash
smp serve --profile full          # all tools (default)
smp serve --profile mcp           # run the local curated profile
SMP_PROFILE=mcp smp serve         # same, via env
```

### Hosted inventory snapshot

Verified through authenticated Codex MCP initialization on 2026-07-15, the hosted
connector exposes **105 tools**. It covers all five namespaces documented below:
project management, workspace and brand operations, AI image/video/audio generation,
assets and documents, social operations and analytics, media editing and
transcription, and notifications.

The hosted social surface supports creating a review bundle with all selected IDs
in `social_createSocialMediaReviewBundle.draft_ids`. It does **not** currently
expose `social_addDraftsToSocialMediaReviewBundle`; that append operation remains
available in the full toolkit.

The local `mcp` source profile remains a compact 49-tool subset for marketer
workflows. It includes authenticated `whoami`, workspace details, teamspace
discovery, all 16 social operations, image/video generation, direct asset ingestion,
brand context, and marketing projects. The hosted deployment is broader than that
local profile and currently matches the 106-tool `full` catalog except for
`social_addDraftsToSocialMediaReviewBundle`.

Attached files follow the same flow as the Simplified UI: authenticated signing,
direct client-to-storage PUT, then asset registration. The hosted server never
attempts to read a client-local path or proxy file bytes.

The source inventory is captured separately in
[`evals/source-profile-tool-inventory.json`](../evals/source-profile-tool-inventory.json).
The live hosted snapshot is captured independently because hosted deployment and
local profile definitions can change on different release schedules.

### Workspace and teamspace context

`api_getWorkspaceInfo` is the hosted connector's authoritative `whoami`: it returns
the authenticated user, the credential-bound workspace, workspace defaults, and
active teamspaces. `api_listTeamspaces` resolves names to numeric IDs, and
`api_getWorkspace` reads richer workspace metadata.

The CLI can persist an active teamspace and send its numeric ID as the `Space`
header. Hosted MCP remains stateless: every generated tool accepts optional
`space_id`, which middleware forwards as `Space` for that call, its asynchronous
polls, and hook follow-ups. Agents resolve a teamspace once and pass the same
`space_id` on every related call; omitting it returns to the credential's default
workspace context.

---

## The full toolkit — `simplified-apikit`

`simplified-apikit` is *three things in one package*:

- **`smp`** — a CLI to drive Simplified from your terminal
- **`smp serve`** — a local MCP server (stdio or HTTP) for Claude Desktop, Cursor,
  Cline, or any MCP host
- the agent toolkit powering Simplified's own assistants

> **Distribution.** The hosted connector at `https://apikit.simplified.com/mcp` is
> the public, zero-install path and exposes the 105-tool hosted profile. The
> `simplified-apikit` CLI/toolkit (the `full` profile) is distributed to Simplified
> workspaces — see your workspace settings or contact Simplified for the install
> command. The sections below document what it does once installed.

### Install

Install once, globally, with `pipx` (index URL provided with your workspace access):

```bash
pipx install simplified-apikit
```

Upgrade with `pipx upgrade simplified-apikit`.

### Authenticate

Auth is read from environment variables — set once, use everywhere:

```bash
export SMP_TOKEN=your_api_token             # API key (sQL00kSs.xxx) or DRF token
export SMP_WORKSPACE=270                    # required for DRF tokens; inferred for API keys
export SMP_SPACE=42                         # optional, for space-scoped resources
export SMP_URL=https://api.simplified.com   # default; omit for prod
```

Or pass per-call: `smp --token xxx --workspace 270 pm list-boards`.

### Serve as a local MCP

```bash
smp serve                                   # stdio (Claude Desktop / Cursor)
smp serve --transport http --port 9000      # HTTP transport
```

The middleware handles pre/post hooks (inline assignees on `pm create-task`, Quill-
Delta description conversion), response normalization, and async task polling — so
MCP clients get the same ergonomic interface as the CLI.

---

## Tool catalog

`full` profile, by namespace. Tool ids are `<namespace>_<operationId>`.

### `pm` — Project Manager (29)

Boards, statuses, tasks, and everything around them.

- **Boards** — `listBoards`, `createBoard`, `getBoard`, `updateBoard`,
  `deleteBoard`, `cloneBoard`
- **Statuses** (board columns) — `listStatuses`, `createStatus`, `getStatus`,
  `updateStatus`, `deleteStatus`, `moveStatus`
- **Tasks** — `createTask`, `getTask`, `updateTask`, `deleteTask`, `cloneTask`,
  `listSubtasks`, `getTaskActivity`, `searchTasks`, `searchRecentTasks`
- **Task sub-resources** — `updateTaskAssignees`, `updateTaskTags`,
  `updateTaskAttachments`, `updateTaskCustomFields`, `getTaskDependencies`,
  `addTaskDependency`, `removeTaskDependency`
- **Workspace** — `listWorkspaceMembers`

### `api` — Assets, brand kits, generation, documents (39)

- **Workspace context** — `listTeamspaces`, `getWorkspace`, `getWorkspaceInfo`
- **Brand kits (V2)** — `listBrandKits`, `createBrandKit`, `getBrandKit`,
  `buildBrandKit`
- **Context documents** — `listContextDocuments`, `createContextDocument`,
  `getContextDocument`, `getContextDocumentByType`, `updateContextDocument`,
  `deleteContextDocument`
- **Projects & items** — `listProjects`, `createProject`, `getProject`,
  `deleteProject`, `exportProjectItems`, `listProjectItems`, `createProjectItem`,
  `getProjectItem`, `deleteProjectItem`, `assignAgentToItem`, `reorderProjectItem`
- **AI image** — `generateImage`, `getModelFields`
- **AI video** — `generateVideo`, `getVideoVariation`
- **Text-to-speech** — `listVoices`, `generateAudio`
- **Assets** — `createAsset`, `getAsset`
- **Documents** — `createDocument`
- **Tasks** — `getTaskResult` (poll an async job)
- **Comments** — `listComments`, `addComment`

### `social` — Social media (16)

The full toolkit includes one operation beyond the current hosted connector:
appending drafts to an existing review bundle.

- **Accounts** — `getSocialMediaAccounts`
- **Posts** — `createSocialMediaPost`, `getSocialMediaPosts`,
  `updateSocialMediaPost`, `deleteSocialMediaPost`
- **Drafts** — `getSocialMediaDrafts`, `updateSocialMediaDraft`,
  `deleteSocialMediaDraft`
- **Tags** — `listSocialMediaTags`, `createSocialMediaTag`
- **Analytics** — `getSocialMediaAnalyticsRange`, `getSocialMediaAnalyticsPosts`,
  `getSocialMediaAnalyticsAggregated`, `getSocialMediaAnalyticsAudience`
- **Review bundles** — `createSocialMediaReviewBundle`,
  `addDraftsToSocialMediaReviewBundle`

### `media` — Image / video / audio editing (21)

- **Image** — `blurBackground`, `removeBackground`, `upscaleImage`,
  `generativeFill`, `imageOutpainting`, `magicInpaint`, `replaceImageBackground`,
  `restoreImage`, `sdScribble`, `convertImageFormat`
- **Video** — `convertVideoFormat`, `mergeVideos`, `removeAudio`, `reverseVideo`,
  `speedupVideo`, `addBRollsVideo`, `scriptToVideo`, `textToVideo`
- **Transcription** — `transcribeVideo`, `getTranscription`,
  `downloadTranscriptionFile`

### `notify` — Agent notifications (1)

- `notify` — send an agent notification.

---

## Async tasks

Several tools (image/video generation, most `media/*` ops) are async on the
backend. The toolkit middleware **polls for you** and returns the finished result —
you rarely call `getTaskResult` directly. Default auto-poll is ~3.75 min; long jobs
(video) may return a `task_id` to poll manually if they exceed the window.

For video specifically, poll `getVideoVariation` (step 3 of the
discover → submit → poll flow) rather than `getTaskResult`.

---

## Connect from any MCP client

### Hosted connector (recommended)

```json
{
  "mcpServers": {
    "simplified": { "type": "http", "url": "https://apikit.simplified.com/mcp" }
  }
}
```

OAuth on first use; tokens refresh automatically. Works in Claude Code, Claude.ai /
Desktop Custom Connectors, Cursor, Codex, and any spec-compliant MCP host.

### Codex CLI (OAuth-gated remote MCP)

Add the connector to Codex configuration:

```toml
[mcp_servers.simplified]
url = "https://apikit.simplified.com/mcp"
```

Then run `codex mcp login simplified` to complete OAuth. The hosted connector uses
stateless token validation; fresh and concurrent Codex sessions were verified on
2026-07-15 without `SessionExpired404`.

### Local full toolkit (stdio)

```json
{
  "mcpServers": {
    "simplified": {
      "command": "smp",
      "args": ["serve"],
      "env": { "SMP_TOKEN": "your_token", "SMP_WORKSPACE": "270" }
    }
  }
}
```

This gives you the **`full`** profile — every namespace above.

---

## CLI quick reference

The same tools are available as CLI subcommands (`smp <module> <command>`):

```bash
smp pm list-boards
smp pm create-task --status <uuid> --title "Fix login" --assignees '[196]'
smp api generate-image --prompt "sunset over mountains"
smp api list-brand-kits
smp social get-social-media-accounts
smp social create-social-media-post --payload '{"message":"Hello","action":"draft"}'
smp media upscale-image --image-url "https://..." --scale 4
smp media text-to-video --payload '{"title":"Sunset timelapse","tone":"calm"}'
```

`--help` is always current (auto-generated from the OpenAPI specs):

```bash
smp --help                  # list modules
smp pm --help               # list pm commands
smp pm create-task --help   # full options for one command
```

---

## See also

- [README](../README.md) — the plugin and quick start
- [AGENTS.md](../AGENTS.md) — agent behavior & safety conventions
- [SKILL_TREE.md](../SKILL_TREE.md) — index of the published skills
