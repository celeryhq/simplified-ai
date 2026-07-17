---
name: simplified-cli
description: >
  Entry point for the Simplified CLI (`smp MODULE COMMAND`) — covers Project Manager,
  Media (image/video AI), Assets API (brand kits, projects, assets), Social Media,
  and the MCP server (`smp serve`). Trigger on any request to use the `smp` CLI,
  manage Simplified PM boards/tasks, generate or process images/videos, manage
  brand kits or assets, schedule social media posts, or expose Simplified as MCP
  tools to Claude Desktop / Cursor / Cline.
---

# Simplified CLI (`smp`) — Module Index

`smp` is the unified CLI for the Simplified API, distributed as the
`simplified-apikit` pip/pipx package. It exposes 4 functional modules plus an
MCP server, all auto-generated from OpenAPI specs.

## Installation

```bash
pipx install simplified-apikit \
  --index-url "https://gitlab.com/api/v4/projects/70495826/packages/pypi/simple" \
  --pip-args="--extra-index-url https://pypi.org/simple"
```

## Authentication

Auth is read from environment variables — set once, use everywhere:

```bash
export SMP_TOKEN=your_api_token             # API key (sQL00kSs.xxx) or DRF token
export SMP_WORKSPACE=270                    # required for DRF tokens; inferred for API keys
export SMP_SPACE=42                         # optional, for space-scoped resources
export SMP_URL=https://api.simplified.com   # default; omit for prod
```

Or pass per-call: `smp --token xxx --workspace 270 pm list-boards`

## Command Syntax

Subcommands use **space separation**: `smp pm list-boards`. The legacy colon form
(`smp pm:list-boards`) also works for back-compat.

## Modules

The CLI is organised by module. Pick the right one for the task:

### `smp pm` — Project Manager
Boards, statuses, tasks, subtasks, assignees, tags, dependencies, comments, activity.
The most stateful module — has a memory-cache discipline for board/status/user IDs.

→ See [references/pm.md](references/pm.md) for full guide.

```bash
smp pm list-boards
smp pm create-task --status <uuid> --title "Fix login" --assignees '[196]'
smp pm search-tasks --board <id> --status <id> --search "login"
smp pm add-task-dependency --task-id <a> --target-task-id <b> --relation-type BLOCKS
```

### `smp media` — Image & Video AI Tools
Background removal, upscaling, generative fill, outpainting, inpainting, format
conversion, video merging, B-roll, text/script to video. Mostly async — middleware
auto-polls for results.

→ See [references/media.md](references/media.md) for full guide.

```bash
smp media remove-background --image-url "https://..."
smp media upscale-image --image-url "https://..." --scale 4
smp media merge-videos --video-urls '["https://a.mp4","https://b.mp4"]'
smp media text-to-video --payload '{"title":"Sunset timelapse","tone":"calm"}'
```

### `smp api` — Assets API
Workspaces, brand kits (V2), projects and project items, AI image generation,
assets, context documents, brand books, agents.

→ See [references/api.md](references/api.md) for full guide.

```bash
smp api get-workspace
smp api list-brand-kits
smp api generate-image --prompt "sunset over mountains"
smp api create-project --primary-type ASSET --title "Q1 launch"
```

### `smp social` — Social Media
Connected accounts, posts (publish/draft/schedule), tags, and analytics
(range, posts, aggregated, audience).

→ See [references/social.md](references/social.md) for full guide.

```bash
smp social get-social-media-accounts
smp social create-social-media-post --payload '{"caption":"Hello","accounts":[...]}'
smp social get-social-media-analytics-aggregated --account-id <id>
```

### `smp comments` — Comments
Threaded comments on any commentable Simplified resource. Currently supports
tasks; will grow to other types. Generic by design — addressed by
`content_type` + `object_pk` rather than a resource-specific shortcut.

→ See [references/comments.md](references/comments.md) for full guide.

```bash
smp comments list-comments --content-type task --object-pk <task_uuid>
smp comments add-comment --content-type task --object-pk <task_uuid> --comment "LGTM"
```

### `smp serve` — MCP Server
Exposes every module command above as an MCP tool. Use from Claude Desktop,
Cursor, Cline, or any MCP host.

```bash
smp serve                              # stdio (default — for Claude Desktop/Cursor)
smp serve --transport http --port 9000 # HTTP transport
```

The middleware handles pre/post hooks (e.g. inline assignees on `pm create-task`,
auto Quill-Delta description conversion), response normalization, and async task
polling — so MCP clients get the same ergonomic interface as the CLI.

## Discovering Commands

Don't rely on a static table. The CLI is auto-generated from OpenAPI specs and
`--help` is always current:

```bash
smp --help                          # list modules
smp pm --help                       # list pm commands
smp pm create-task --help           # full options for a single command
```

## Output

By default `smp` pretty-prints JSON. Pass `--raw` for unformatted output (useful
when piping into `jq` / `python3 -c`):

```bash
smp --raw pm list-boards | jq '.results[].id'
```

## Cross-cutting Patterns

**Async tasks.** Several endpoints (`media/*`, `api generate-image`, some video ops)
return a `task_id`. The middleware polls `GET /api/v1/tasks/{task_id}` automatically
and returns the final result. Default polling is ~3.75 min — video generation may
need longer. If it times out you'll get the `task_id` to poll manually.

**Composite fields.** `pm create-task` / `pm update-task` accept assignees and tags
inline; the toolkit makes follow-up sub-resource calls automatically.

**JSON args.** Array/object options need single quotes around JSON:
`--assignees '[196, 200]'`, `--payload '{"title":"..."}'`.

**Pagination.** List endpoints default to `page_size=10`. Add `--page-size 100` to
get more.
