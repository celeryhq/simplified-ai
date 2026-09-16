# Release notes

## v1.4.0

Simplified for AI 1.4.0 is the first release since v1. It takes the plugin from
two skills — image generation and social posting — to sixteen, adding video,
brand, projects, task management, and the command line, plus eight
outcome-driven marketer workflows built on top of them.

### New — creative

- `generate-video` — model-aware AI video generation with capability discovery,
  text-, image-, and video-guided motion, and correct render polling.

### New — workspace and brand

- `simplified-workspace` — authenticated identity, workspace defaults, and
  teamspace resolution, so scoped work never crosses a client boundary.
- `manage-brand` — evidence-led brand kits and reusable brand context: identity,
  voice, audiences, positioning, proof, content pillars, and visual rules.

### New — operations

- `manage-projects` — approved plans into projects, deliverables, assignments,
  review gates, and controlled exports.
- `simplified-project-management` — boards, tasks, subtasks, dependencies,
  assignees, tags, custom fields, and comments.
- `simplified-cli` — the `smp` command line across project management, media,
  assets, social, and `smp serve`.

### New — marketer workflows

Eight outcome-driven workflows compose the platform operators above:
`social-content-planner`, `cross-platform-campaign`, `content-repurposer`,
`evergreen-content-engine`, `local-business-marketing`, `creative-testing`,
`social-performance-analyst`, and `campaign-review`.

### Improved — social

- Coverage across 13 platforms: Facebook, Instagram, TikTok, YouTube, LinkedIn,
  Pinterest, Threads, Bluesky, X/Twitter, Google Business, Mastodon, Reddit, and
  Telegram.
- Timed auto-comments, for patterns such as "link in first comment."
- Shareable review bundles for stakeholder and client approval.
- Analytics: time-series, per-post, aggregated KPIs, and audience demographics.
- Direct asset upload, with permanent asset IDs carried into posts in place of
  signed URLs that expire.

### Improved — image generation

- Capability-first model discovery across Flux, Google Gemini and Imagen, OpenAI
  GPT Image, Ideogram, Recraft, Stable Diffusion, Qwen, and Seedream.
- Quality and cost tradeoffs, model-specific parameter handling, and brand assets
  resolved by permanent asset ID before generation.

### Compatibility

- The hosted MCP endpoint (`https://apikit.simplified.com/mcp`) and its OAuth
  setup are unchanged from v1. No reinstall or reauthorization is required.
- One exception: installations still registered under the earlier
  `simplified-for-ai` marketplace identity need a one-time remove and reinstall
  to move to `simplified-ai`.
- Everything v1 could do, it still does.
