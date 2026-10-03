# Skill Tree

The plugin ships every folder under `skills/`. The workflows documented below are
the 22 supported skills, split between Simplified platform operators and marketer
workflows.

Each top-level folder contains a canonical `SKILL.md`. Skills surfaced in Codex
also carry `agents/openai.yaml`, which adds Codex UI metadata without forking the
workflow instructions. `simplified-cli` also carries metadata for local agents, but is excluded from the
hosted ChatGPT bundle because it needs a shell. `simplified-workflows` requires
the separate automation connection and is excluded from that bundle as well.

```text
skills/
├── manage-assets/                  # find/import/upload → ready asset UUIDs
├── generate-image/                 # model discovery → reusable image asset
├── edit-image/                     # processing → verified reusable images
├── transcribe-media/               # speech → transcript and subtitle exports
├── generate-voiceover/             # locale/voice discovery → narration
├── repurpose-video/                # long recording → rendered clips and drafts
├── generate-video/                 # model discovery → reusable video asset
├── simplified-workspace/           # whoami + workspace/teamspace resolution
├── simplified-social/              # 13 platforms, auto-comments, reviews, analytics
├── manage-brand/                   # brand kit + reusable brand context
├── manage-projects/                # projects, deliverables, handoffs, exports
├── simplified-project-management/  # boards, tasks, assignees, dependencies
├── simplified-cli/                 # the `smp` command line
├── simplified-workflows/           # automation connection, step graphs and runs
├── social-content-planner/         # goals → weekly/monthly calendar
├── cross-platform-campaign/        # brief → coordinated channel rollout
├── content-repurposer/             # source → channel-native post sequence
├── evergreen-content-engine/       # durable expertise → renewable content system
├── local-business-marketing/       # local truth → visits, calls, and bookings
├── creative-testing/               # hypothesis → controlled creative learning
├── social-performance-analyst/     # metrics → evidence-backed next actions
└── campaign-review/                # drafts → stakeholder approval package
```

## Platform operators

Fourteen operators provide the platform primitives.

### `simplified-workspace`

Identify the authenticated user and workspace, read workspace defaults, resolve
accessible teamspaces to numeric IDs, and prevent cross-space resource mistakes.

### `manage-assets`

Find/list assets by name or tag, import URLs, gate local uploads on client capabilities, check readiness, and hand off permanent IDs for generation or social drafts. Named-folder listing is not implied by text search.

### `generate-image`

Discover current image models and field schemas, generate from prompts or
references, and return a permanent asset ID when the result will be reused.

### `generate-video`

Discover current video models and capabilities, generate text/image/video-guided
motion, wait for completion and continue a non-terminal variation when needed, and preserve reusable video assets.

### `edit-image`

Remove or replace backgrounds, restore/upscale, make masked or semantic edits,
and verify completed outputs before reuse.

### `transcribe-media`

Transcribe speech with supported timestamps and speaker labels; export actual
SRT/VTT text without inventing download URLs or source facts.

### `generate-voiceover`

Discover voices by exact locale, preserve approved scripts, use only supported
voice instructions, and save narration for reuse.

### `repurpose-video`

Render highlights or custom excerpts from downloadable recordings. Track project
and individual clip states, enumerate every page, preserve source timestamps,
and pass ready asset IDs to social drafts.

### `simplified-social`

Handle direct asset uploads, account discovery, platform-specific post settings,
draft/schedule/queue actions, timed auto-comments, post lifecycle, reviews, and
analytics across 13 platforms with a hard draft-before-publish boundary.

### `manage-brand`

Create and maintain brand identity, visual rules, voice, ICPs, positioning, USPs,
content pillars, writing examples, and other reusable brand context from evidence.

### `manage-projects`

Turn approved plans into projects and accountable deliverables; manage item order,
assignments, comments, assets, and partner exports without implying publishing
authorization.

### `simplified-project-management`
**Trigger:** inspect or change Simplified boards, statuses, tasks, assignees,
tags, dependencies, comments, activity, or tracked work.
**Tools:** `pm_*` plus `api_listComments` and `api_addComment` for task comments.
**Does:** discover tenant-specific identifiers, read current state, confirm
consequential changes, execute precise writes, and verify the result directly.

### `simplified-cli`
**Trigger:** scripted, CI, or terminal work rather than a conversational flow.
**Tools:** the Python `simplified-apikit` package's generated `smp` commands; this is separate from the npm `simplified` CLI.
**Does:** resolve local credentials and teamspace context, and run JSON-native
commands whose output feeds directly into pipelines.

## Marketer workflows

### `social-content-planner`

Build a chronological, goal-led weekly or monthly channel plan and optionally save
approved copy as drafts.

### `cross-platform-campaign`

Create the campaign spine, channel-native rollout, reusable media, drafts, review
handoff, and explicitly approved schedule for a launch, offer, or event.

### `content-repurposer`

Transform authoritative source material into distinct channel-native posts while
preserving facts, claims, qualifications, and attribution.

### `evergreen-content-engine`

Create durable content territories, recurring franchises, a scored content bank,
a sustainable first cycle, and explicit refresh/fatigue/retirement rules.

### `local-business-marketing`

Build verified, location-specific social and Google Business programs around local
discovery, trust, timely demand, and calls, bookings, directions, or visits.

### `creative-testing`

Turn campaign uncertainty into a falsifiable hypothesis, controlled variants,
objective-aligned metrics, a decision rule, and a reusable learning record.

### `social-performance-analyst`

Translate KPIs, trends, post results, and audience signals into a measured verdict,
limitations, three prioritized actions, and a next experiment.

### `campaign-review`

Inspect and revise selected drafts, create a stakeholder review bundle, and keep
review approval separate from scheduling or publishing authorization. Agency
workflows resolve the client teamspace first and keep one bundle per client and
campaign so drafts and IDs never cross client boundaries.

## Cross-skill flow

## Composition map

```text
brand evidence → manage-brand
                    ↓
source / goal / offer / local need / test hypothesis
                    ↓
planner / campaign / repurposer / evergreen / local / creative-testing
                    ↓
generate-image / generate-video / edit-image / generate-voiceover → permanent asset IDs
recording → repurpose-video → rendered clips → permanent asset IDs
recording → transcribe-media → source transcript → content-repurposer
                    ↓
simplified-social → drafts → campaign-review → explicit approval → publish
                    ↓
social-performance-analyst → learning → next content or creative test

approved plan → manage-projects → accountable production and handoffs
```

## Release dependency

Skills and hosted tool releases are independent. Check current tool discovery before promising a capability. The July hosted/source inventories in `evals/` remain historical snapshots. `manage-assets` uses `api_listAssets` when exposed; installing it does not deploy that operation.
