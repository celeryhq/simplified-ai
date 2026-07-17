# Skill Tree

The plugin provides fourteen shared Codex/Claude skills in two layers: six
Simplified platform operators and eight marketer workflows. Each top-level folder
contains a canonical `SKILL.md`; `agents/openai.yaml` adds Codex UI metadata without
forking the workflow instructions.

```text
skills/
├── generate-image/                 # model discovery → reusable image asset
├── generate-video/                 # model discovery → reusable video asset
├── simplified-workspace/           # whoami + workspace/teamspace resolution
├── simplified-social/              # 13 platforms, auto-comments, reviews, analytics
├── manage-brand/                   # brand kit + reusable brand context
├── manage-projects/                # projects, deliverables, handoffs, exports
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

### `simplified-workspace`

Identify the authenticated user and workspace, read workspace defaults, resolve
accessible teamspaces to numeric IDs, and prevent cross-space resource mistakes.

### `generate-image`

Discover current image models and field schemas, generate from prompts or
references, and return a permanent asset ID when the result will be reused.

### `generate-video`

Discover current video models and capabilities, generate text/image/video-guided
motion, poll the correct variation status, and preserve reusable video assets.

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

### `simplified-project-management`
**Trigger:** inspect or change Simplified boards, statuses, tasks, assignees,
tags, dependencies, comments, activity, or tracked work.
**Tools:** `pm_*` plus `api_listComments` and `api_addComment` for task comments.
**Does:** discover tenant-specific identifiers, read current state, confirm
consequential changes, execute precise writes, and verify the result directly.

## Cross-skill flow

## Composition map

```text
brand evidence → manage-brand
                    ↓
source / goal / offer / local need / test hypothesis
                    ↓
planner / campaign / repurposer / evergreen / local / creative-testing
                    ↓
generate-image / generate-video → permanent asset IDs
                    ↓
simplified-social → drafts → campaign-review → explicit approval → publish
                    ↓
social-performance-analyst → learning → next content or creative test

approved plan → manage-projects → accountable production and handoffs
```

## Release dependency

The expanded hosted MCP profile is live. Authenticated discovery verified 105
hosted tools on July 15, 2026; the local `full` profile exposes 106. The only known
profile difference is that hosted MCP does not yet expose
`social_addDraftsToSocialMediaReviewBundle`.
