# Eval Results & Golden Outputs

Live captures from production (`https://api.simplified.com`) and the hosted MCP
connector (`https://apikit.simplified.com/mcp`). Image generation, stateless OAuth,
workspace/brand/project operators, social reads, analytics, draft creation, and an
image-to-draft flow were verified end to end.

Last live connector run: 2026-07-15. Last skill-contract run: 2026-07-16.

## Marketer skill evals

`python3 evals/run_skill_evals.py` validates six platform operator contracts,
eight marketer workflow contracts, 26 marketer routing cases, and 12
source-profile platform routing cases without credentials or network access.

| Suite | Cases/checks | Status | Last run |
|---|---:|---|---|
| Catalog IDs and schema | 2 | ✅ pass | 2026-07-14 |
| Per-workflow scenario coverage | 26 cases, at least 3 per workflow | ✅ pass | 2026-07-16 |
| New platform routing coverage | 12 cases, 3 per new operator | ✅ pass | 2026-07-15 |
| Skill contracts and metadata | 14 | ✅ pass | 2026-07-16 |
| Hosted tool inventory compatibility | 105 live tools | ✅ pass | 2026-07-15 |
| Source profile inventory compatibility | 49 source tools | ✅ pass | 2026-07-15 |
| Sample agent trace + asset handoff | 1 | ✅ pass | 2026-07-14 |
| Live installed-plugin routing smoke | 5 prompts | ✅ 5/5 | 2026-07-14 |

The sample trace verifies model-field discovery → asset-backed image generation →
account discovery → safe social draft, including the exact generated `asset_id`
being passed into `media`. Full model-run traces remain environment-dependent and
can be graded with `--traces`.

The platform contracts validate workspace identity/teamspace boundaries,
image/video model discovery, asset ingestion, brand-kit/context change control,
and project mutation safety. The
`simplified-social` contract specifically verifies the attached-file
workflow: `api_signAssetUpload` → direct storage PUT → `api_registerAsset` →
`api_getAsset` readiness → permanent asset UUID handoff, while prohibiting
client-local paths and Simplified auth headers on the storage request.

## Hosted MCP inventory verification

Authenticated Codex MCP initialization on 2026-07-15 exposed **105 tools** across
the `pm`, `api`, `social`, `media`, and `notify` namespaces. The exact names and
critical schemas are captured in
[hosted-tool-inventory.json](hosted-tool-inventory.json).

The hosted deployment is broader than the compact 49-tool local `mcp` source
profile. It currently matches the 106-tool local `full` catalog except for
`social_addDraftsToSocialMediaReviewBundle`. Review workflows therefore pass all
selected IDs directly to `social_createSocialMediaReviewBundle.draft_ids`.

The stateless OAuth backend fix was tested with three concurrent fresh Codex
sessions. All initialized successfully and no `SessionExpired404` was observed.
Live read-only operator smoke tests passed for workspace/teamspace identity, model
fields, credit balance, brand kits, projects, social accounts, and analytics.

A live social E2E created one four-account draft, generated one reusable image asset,
and attached it to the matching LinkedIn, Facebook, Google Business, and X/Twitter
drafts. Per-account reads verified exactly one photo on every draft. Nothing was
scheduled, queued, or published.

One connector compatibility behavior was also captured: a comma-separated
multi-account `social_getSocialMediaDrafts` lookup returned no rows while equivalent
per-account queries returned the expected drafts. The social and campaign-review
skills now require a read-only per-account fallback and exact-ID deduplication.

The installed pre-1.1 Codex marketplace also reports an upgrade identity mismatch:
the configured marketplace/plugin is `simplified-for-ai`, while the current
repository correctly declares the canonical `simplified-ai` identity. Existing
legacy installations need a one-time remove/reinstall migration; the repository
should not revert its name to accommodate the old identity.

## Installed-plugin routing smoke

The local `simplified-ai@simplified-ai` 1.1.0 build was installed into Codex and
tested with five marketer prompts. It selected `social-content-planner`,
`cross-platform-campaign`, `content-repurposer`, `social-performance-analyst`, and
`campaign-review` correctly (5/5). The capture is in
[fixtures/live-routing-smoke-2026-07-14.json](fixtures/live-routing-smoke-2026-07-14.json).

## Status summary

| Case | Layer | Status | Note |
|---|---|---|---|
| OAuth pipeline (DCR → PKCE → token) | infra | ✅ verified | client registered, token minted (3600s, full scopes) |
| C1 — image, transient | I/O | ✅ verified live | real 1024×1024 WebP |
| C2 — image, 16:9 text | I/O | ⏳ not run | image path proven by C1; run with `--with-image` |
| C3 — list accounts | I/O | ✅ verified live | connected accounts returned successfully |
| C4 — draft post | I/O | ✅ verified live | four-account draft created without publishing |
| C5 — analytics aggregated | I/O | ✅ verified live | connected-account analytics returned successfully |
| C6 — image→draft (cross-skill) | I/O | ✅ verified live | one generated asset attached to four matching drafts |

## Golden outputs (captured live)

### api_generateImage — raw endpoint is async (202 → poll)
`POST /api/v1/ai/image/ai-generate-image-v2`:
```json
{ "task_id": "24797bd9-3591-4f19-89cd-9fd935d4839f", "storage": "asset" }   // HTTP 202
```

### api_generateImage — transient (default), via MCP tool
```json
{ "status": "SUCCESS",
  "detail": { "result": ["https://replicate.delivery/…/out-0.webp"], "transient": true } }
```
`detail.result[0]` is a **URL string**. Fetched → HTTP 200 `image/webp`, 1024×1024. ✅

### api_generateImage — asset, via MCP tool
```json
{ "status": "SUCCESS",
  "detail": { "result": [{ "asset_id": "e3441f49-c118-49a0-9a37-5b73f11f2aed",
                           "url": "https://djcdnpt.simplified.com/…/image.webp?Expires=…&Signature=…&Key-Pair-Id=…" }],
              "transient": false, "storage": "asset" } }
```
`detail.result[0]` is an **object** `{asset_id, url}`. Fetched → HTTP 200 `image/webp`,
1024×1024. ✅ The raw task-poll also returns an identical `info` key; the MCP tool
returns only `detail`. The `url` is a **signed CloudFront URL that expires** — carry
the `asset_id` downstream.

### api_getModelFields({type:"image"})
The live hosted MCP returned **16 models** on 2026-07-16 (Flux, Recraft, Ideogram,
Google Gemini, OpenAI GPT Image, Qwen, and ByteDance). ✅ Model capabilities and
catalog credit metadata are dynamic; query the selected model and capability again
before generation. OpenAI `imgen*` models use `size` rather than `aspect_ratio`, and
their catalog `credits_per_image` is a baseline rather than a guaranteed final charge.

## Social output contracts

### social_getSocialMediaAccounts → `{ "accounts": [{ "id": <int>, "name": "...", "type": "..." }] }`
### social_getSocialMediaAnalyticsAggregated → `{ "data": [...], "baseLine": { "impressions_aggregated": {value,prevValue}, "engagement_aggregated": {...}, "followers_aggregated": {...}, "publishing_aggregated": {...} } }`
### social_createSocialMediaPost (action:"draft") → success; draft then visible in `social_getSocialMediaDrafts`.

## Rerun the deterministic live harness
```bash
export SMP_ACCESS_TOKEN=<fresh token>   # see README.md
python3 evals/run_evals.py --with-image
```
Use `--keep-drafts` only when the created test drafts should remain available for
manual inspection. Otherwise the harness cleans them up.
