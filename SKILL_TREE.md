# Skill Tree

Index of skills in this plugin. Each is a directory under [skills/](skills/) with a
`SKILL.md` (Agent Skills spec) plus an optional `agents/openai.yaml` (Codex metadata)
and `references/` for deep detail.

```
skills/
├── generate-image/
│   ├── SKILL.md                 # text-to-image generation workflow
│   └── agents/openai.yaml       # Codex UI metadata + MCP dependency
├── simplified-project-management/
│   ├── SKILL.md                 # boards / statuses / tasks / dependencies
│   ├── agents/openai.yaml
│   └── references/
│       ├── workflows.md         # operation routing and multi-step workflows
│       └── tool-behavior.md     # search, write, expansion, and date behavior
└── simplified-social/
    ├── SKILL.md                 # post / schedule / draft / analyze workflow
    ├── agents/openai.yaml
    └── references/
        ├── platform-settings.md # per-platform `additional` settings + limits
        └── analytics.md         # metrics, default sets, response shapes
```

## Skills

### generate-image
**Trigger:** create / generate / make / design an image, photo, graphic, logo, banner.
**Tool:** `api_generateImage`.
**Does:** text-to-image across Flux, Google (Gemini/Imagen), OpenAI GPT Image,
Ideogram, Stable Diffusion, Qwen, SeeDream. Returns a viewable URL; with
`storage:"asset"` also a reusable `asset_id` for the social skill.

### simplified-social
**Trigger:** post / schedule / publish to social; social accounts; analytics, reach,
engagement, followers.
**Tools:** `social_getSocialMediaAccounts`, `social_createSocialMediaPost`,
`social_getSocialMediaAnalytics{Range,Posts,Aggregated,Audience}`, plus drafts/tags.
**Does:** draft → confirm → schedule/queue posts, and pull analytics, across 10
platforms. Accepts a `generate-image` `asset_id` in `media` to post a generated image.

### simplified-project-management
**Trigger:** inspect or change Simplified boards, statuses, tasks, assignees,
tags, dependencies, comments, activity, or tracked work.
**Tools:** `pm_*` plus `api_listComments` and `api_addComment` for task comments.
**Does:** discover tenant-specific identifiers, read current state, confirm
consequential changes, execute precise writes, and verify the result directly.

## Cross-skill flow

`generate-image` (`storage:"asset"`) → `asset_id` → `simplified-social`
(`media:["<asset_id>"]`) → draft post → confirm → publish.
