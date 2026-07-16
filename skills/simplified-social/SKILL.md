---
name: simplified-social
description: >-
  Manage your entire social media from Codex with Simplified — post, schedule,
  queue, draft, and analyze across Facebook, Instagram, TikTok, YouTube,
  LinkedIn, Pinterest, Threads, Bluesky, X/Twitter, Google Business, Mastodon,
  Reddit, and Telegram. Triggers: social media, post to, schedule post, publish
  on, social accounts, analytics, reach, impressions, engagement, followers
  growth, content calendar, auto-comments, link in first comment, attach local
  media, upload an image or video for a social post.
---

# Simplified Social Media

Schedule, queue, and draft social media posts, add timed auto-comments, and
retrieve analytics across 13 platforms using Simplified.com.

## Connector

All tools (`social_getSocialMediaAccounts`, `social_createSocialMediaPost`,
`api_createAsset`, etc.) are provided by the **Simplified hosted MCP connector**
(`https://apikit.simplified.com/mcp`). They are not built-in tools.

The connector is **OAuth-secured** — Codex walks the OAuth flow; there is no API key to set.

## IMPORTANT: Before Any Operation

If any tool call returns a **401 / Unauthorized**, the Simplified connector is not authorized:

1. **Stop immediately** — do not retry the failed call.
2. **Inform the user** that they need to connect Simplified (authorize the connector) before social tools will work.
3. **Do not proceed** with the original request until the connector is authorized.

## Setup

1. Sign up at [simplified.com](https://simplified.com).
2. Connect your social media accounts in the Simplified dashboard.
3. Enable the Simplified connector in Codex and complete the OAuth authorization.

## Core Workflow

Always follow this sequence: **Discover → Select → Compose → Confirm → Publish**

### Step 1: Discover Accounts

Call `social_getSocialMediaAccounts` to list connected accounts. Optionally filter by network.

```
social_getSocialMediaAccounts({ network: "instagram" })
```

Returns `{ accounts: [...] }` where each account has `id` (integer), `name`, and `type` (see type values below).

If `social_getSocialMediaAccounts` returns an empty list, stop and inform the user with this message:

> **No social media accounts connected yet.**
>
> You're one step away from managing your entire social media presence without leaving your editor. Connect your accounts in the [Simplified dashboard](https://app.simplified.com) and you'll be able to:
>
> - 📅 Schedule and publish posts to Facebook, Instagram, TikTok, YouTube, LinkedIn, Pinterest, Threads, Bluesky, X/Twitter, Google Business, Mastodon, Reddit, and Telegram — with a single command
> - 📊 Pull analytics, track reach, engagement and follower growth across all platforms
> - 🤖 Let your AI agent run full social media campaigns autonomously
>
> Takes 2 minutes to connect. No code required.

### Step 2: Select Target Accounts

Pick one or more `account_ids` from the results. You can post to multiple accounts in a single call.

### Step 3: Compose the Post

Build the post payload:
- `message` (required) — the post text, max 5000 chars at the connector boundary
  (tighter per-platform limits apply)
- `account_ids` (required for publishing actions) — array of target account IDs
- `action` (required) — `schedule`, `add_to_queue`, or `draft`
- `date` — required for `schedule`, format: `YYYY-MM-DD HH:MM`
- `media` — array (max 10) of **Simplified asset UUIDs** or public media URLs
- `comments` — ordered auto-comments, each with `message` and a nonnegative
  `delay` in seconds after the post publishes; comments cannot include media
- `additional` — platform-specific settings (see below)

**Attaching a generated image:** `media` accepts Simplified **asset UUIDs**, resolved server-side to fresh permanent URLs at publish time — exactly what the **generate-image** skill returns with `storage:"asset"`. Pass that `asset_id` straight into `media`.

**Attaching a local file:** never pass a client-local path to the hosted server.
Read [references/assets.md](references/assets.md), then follow the UI-equivalent
flow: `api_signAssetUpload` → direct client PUT to signed storage →
`api_registerAsset`. Poll `api_getAsset` until `status=4`, then pass that exact UUID
into `media`. Never expose the signed upload URL or attach Simplified auth to the
storage PUT.

### Step 4: Confirm, then Publish

Publishing is outward-facing. For `schedule` / `add_to_queue`, **show the composed post to the user and get explicit confirmation first** (drafting first with `action:"draft"` is a good way to preview). Then call `social_createSocialMediaPost`.

If the post includes auto-comments, the confirmation must show each comment's text
and post-relative delay. For “link in first comment after X minutes,” convert
nonnegative minutes to an integer number of seconds with `delay = X * 60`.
`delay` is measured in seconds after the post publishes, not after the previous
comment. Comments execute in array order. Do not move the comment text into the
main post.

**Show returned URLs as links, never embed them.** Any URL these tools return
(review-bundle links, published-post URLs, media URLs) must be presented as a plain
URL or Markdown link — **never** Markdown image syntax (`![](url)`) and never
inline-rendered. The user clicks the link; the agent does not render it.

## Choosing the Right Analytics Tool

| User asks about... | Tool to call |
|---|---|
| Trends over time, charts, metric growth/decline | `social_getSocialMediaAnalyticsRange` |
| Specific posts, best/worst performing content | `social_getSocialMediaAnalyticsPosts` |
| Account overview, KPIs, period summary | `social_getSocialMediaAnalyticsAggregated` |
| Demographics, follower origins, age/gender breakdown | `social_getSocialMediaAnalyticsAudience` |
| "Show me analytics" with no further context | `social_getSocialMediaAnalyticsAggregated` + `social_getSocialMediaAnalyticsRange` with key metrics |

## Tool Reference

### `social_getSocialMediaAccounts`

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| `network` | string | No       | Filter by platform (see networks)    |

**Networks (filter parameter):** `facebook`, `instagram`, `linkedin`, `tiktok`,
`tiktokBusiness`, `youtube`, `pinterest`, `threads`, `google`, `bluesky`,
`mastodon`, `reddit`, `telegram`

Returns `{ accounts: [...] }`. Each account object:

| Field  | Type    | Description |
|--------|---------|-------------|
| `id`   | integer | Account ID — use for all analytics calls and for `account_ids` in `social_createSocialMediaPost` |
| `name` | string  | Account display name |
| `type` | string  | Account type — see values below |

**`type` values and their meaning:**

| `type` value | Platform | Notes |
|---|---|---|
| `Facebook page` | Facebook | — |
| `Instagram business` / `Instagram profile` | Instagram | — |
| `Youtube account` | YouTube | — |
| `TikTok profile` | TikTok Personal | use `tiktok` metrics set |
| `TikTok profile (business)` | TikTok Business | use `tiktokBusiness` metrics set |
| `LinkedIn company` | LinkedIn | use LinkedIn Company metrics set |
| `LinkedIn profile` | LinkedIn | use LinkedIn Personal metrics set |
| `Pinterest board` | Pinterest | — |
| `Threads account` | Threads | — |
| `Bluesky account` | Bluesky | — |
| `Google Profile` | Google Business | — |
| `Reddit account` | Reddit | `additional.reddit.post.targets` is required |

### `social_createSocialMediaPost`

| Parameter     | Type     | Required | Description                              |
|---------------|----------|----------|------------------------------------------|
| `message`     | string   | Yes      | Post text (connector max 5000 chars; tighter platform limits apply) |
| `account_ids` | int[]    | For publish | Target account IDs from `social_getSocialMediaAccounts`; omit/empty for an accountless `draft` |
| `action`      | string   | Yes      | `schedule`, `add_to_queue`, or `draft`   |
| `date`        | string   | For `schedule` | Schedule datetime: `YYYY-MM-DD HH:MM` (not in the past) |
| `media`       | string[] | No       | Asset UUIDs or public media URLs (max 10) |
| `tags`        | int[]    | No       | Tag IDs |
| `comments`    | object[] | No       | Ordered auto-comments: `{message, delay}`; `delay` is seconds after publish and must be ≥ 0 |
| `additional`  | object   | Per platform | Platform-specific settings |

### `social_getSocialMediaDrafts`

Lists unpublished drafts for selected accounts. `account_ids` is required and must
be a comma-separated string of numeric IDs returned by
`social_getSocialMediaAccounts`, for example `"123,456"`. If a multi-account lookup
returns no rows when drafts are expected, retry once per account ID, merge the
results, and deduplicate by exact draft ID. This per-account fallback is read-only
and must not create replacement drafts. Optional filters are `page`, `per_page`,
`search`, `tz`, `order_by`, and `order` (`asc` or `desc`). Omit ordering by default;
if the connector rejects an optional filter, retry without that filter rather than
treating the drafts as absent.

### `social_updateSocialMediaDraft`

Updates one draft. `draft_id` is required. Optional fields are `message`, `media`,
`tags`, `date`, `time`, and `timezone`. Only pass fields the user asked to change.

### `social_createSocialMediaReviewBundle`

Creates a shareable stakeholder-review package. `title` is required; `description`
and `draft_ids` are optional. Prefer one call containing all selected draft IDs.
Draft IDs must come from `social_getSocialMediaDrafts`; never fabricate them. The
response includes `linkToReview`, which must be shown as a link and never embedded.

The hosted connector currently does not expose a separate tool for appending drafts
to an existing bundle. Do not recreate an existing bundle unless the user explicitly
asks for a replacement.

### `social_getSocialMediaAnalyticsRange`

Retrieves time-series data for selected metrics within a date range.

| Parameter    | Type     | Required | Description                                                  |
|--------------|----------|----------|--------------------------------------------------------------|
| `account_id` | integer  | Yes      | Social media account ID (from `social_getSocialMediaAccounts`) |
| `metrics`    | string[] | Yes      | List of metrics to retrieve (see `references/analytics.md`)  |
| `date_from`  | string   | Yes      | Start date: `YYYY-MM-DD`                                     |
| `date_to`    | string   | Yes      | End date: `YYYY-MM-DD` (never in the future)                 |
| `tz`         | string   | No       | Timezone, e.g. `UTC`, `Europe/Warsaw` (default: `UTC`)       |

Returns `data` (per-day series), `baseLine` (period totals with `prevValue`), and `additional` (windowed extras). See `references/analytics.md` for the full metric list, default metrics per network, and response examples.

### `social_getSocialMediaAnalyticsPosts`

Retrieves analytics for individual posts within a date range.

| Parameter    | Type    | Required | Description                                             |
|--------------|---------|----------|---------------------------------------------------------|
| `account_id` | integer | Yes      | Social media account ID                                 |
| `date_from`  | string  | Yes      | Start date: `YYYY-MM-DD`                                |
| `date_to`    | string  | Yes      | End date: `YYYY-MM-DD`                                  |
| `page`       | integer | No       | Page number (default: 1, minimum: 1)                    |
| `per_page`   | integer | No       | Posts per page (default: 10, max: 100)                  |

Returns paginated posts with per-post metrics. **Pagination:** use `per_page: 100`, start at `page: 1`, increment until `current_page >= pages_count` or `posts` is empty.

### `social_getSocialMediaAnalyticsAggregated`

Retrieves aggregated analytics (totals and averages) for an account within a date range.

| Parameter    | Type    | Required | Description             |
|--------------|---------|----------|-------------------------|
| `account_id` | integer | Yes      | Social media account ID |
| `date_from`  | string  | Yes      | Start date: `YYYY-MM-DD` |
| `date_to`    | string  | Yes      | End date: `YYYY-MM-DD`  |

Returns `data` plus `baseLine` with four KPIs: `impressions_aggregated`, `engagement_aggregated`, `followers_aggregated`, `publishing_aggregated` (each with `value` and `prevValue`).

### `social_getSocialMediaAnalyticsAudience`

Retrieves audience demographics and follower data for an account.

| Parameter    | Type    | Required | Description                          |
|--------------|---------|----------|--------------------------------------|
| `account_id` | integer | Yes      | Social media account ID              |
| `date_from`  | string  | Yes      | Start date: `YYYY-MM-DD`             |
| `date_to`    | string  | Yes      | End date: `YYYY-MM-DD`              |
| `tz`         | string  | No       | Timezone, e.g. `UTC`, `Europe/Warsaw` |

Returns `audience_page_fans_gender_age`, `audience_page_fans_country`, `audience_page_fans_city`. Not all fields are available for every network.

## Action Types

| Action         | When to Use                                          | `date` Required? |
|----------------|------------------------------------------------------|-------------------|
| `schedule`     | Post at a specific date/time                         | Yes               |
| `add_to_queue` | Publish as soon as possible (optimal-time queue)     | No                |
| `draft`        | Save for later editing in the Simplified dashboard   | No                |

**Default:** When the user doesn't specify timing (or says "post now"), use `add_to_queue` — it publishes ASAP; there is no separate immediate-publish action. When they give a date/time, use `schedule`. When they say "save" or "draft", use `draft`.

## Platform Settings Quick Reference

All platform settings go inside the `additional` object, grouped by platform name. **Bold** = required. For full details see [references/platform-settings.md](references/platform-settings.md).

| Platform       | Required additionals              | Optional additionals               |
|----------------|-----------------------------------|------------------------------------|
| Facebook       | **`postType`**                    | —                                  |
| Instagram      | **`postType`**, **`channel`**     | `postReel` (reel only)             |
| TikTok         | **`postType`**, **`channel`**, **`post`** | `postPhoto` (photo only)  |
| TikTok Biz     | **`postType`**, **`post`**        | `postPhoto` (photo only)           |
| YouTube        | **`postType`**, **`post`**        | —                                  |
| LinkedIn       | **`audience`**                    | —                                  |
| Pinterest      | **`post`**                        | —                                  |
| Threads        | **`channel`**                     | —                                  |
| Google         | **`post`**                        | —                                  |
| Bluesky        | —                                 | —                                  |
| Mastodon       | —                                 | —                                  |
| Reddit         | **`post.targets`**                | target flair, NSFW flag, link URL  |
| Telegram       | —                                 | —                                  |

Key enum values:

| Platform   | Field              | Values                              |
|------------|--------------------|-------------------------------------|
| Facebook   | `postType.value`   | `post`\*, `reel`, `story`           |
| Instagram  | `postType.value`   | `post`\*, `reel`, `story`           |
| Instagram  | `channel.value`    | `direct`\*, `reminder`              |
| TikTok     | `postType.value`   | `video`\*, `photo`                  |
| TikTok     | `channel.value`    | `direct`\*, `reminder`              |
| TikTok     | `post.privacyStatus` | `PUBLIC_TO_EVERYONE`\*, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| YouTube    | `postType.value`   | `video`\*, `short`                  |
| YouTube    | `post.privacyStatus` | `""`, `public`, `private`, `unlisted` |
| LinkedIn   | `audience.value`   | `PUBLIC`\*, `CONNECTIONS`, `LOGGED_IN` |
| Threads    | `channel.value`    | `direct`\*, `reminder`              |
| Google     | `post.topicType`   | `STANDARD`\*, `EVENT`, `OFFER`      |
| Reddit     | `post.targets[].type` | `self`, `link`                    |

\* = default

## Example Workflows

### Simple Queue Post

```
1. social_getSocialMediaAccounts({ network: "instagram" })
2. social_createSocialMediaPost({
     message: "Check out our new feature! 🚀",
     account_ids: [123],
     action: "add_to_queue",
     media: ["https://cdn.example.com/image.jpg"],
     additional: {
       instagram: { postType: { value: "post" }, channel: { value: "direct" } }
     }
   })
```

### Scheduled YouTube Short

```
1. social_getSocialMediaAccounts({ network: "youtube" })
2. social_createSocialMediaPost({
     message: "Quick tip: how to use our API",
     account_ids: [456],
     action: "schedule",
     date: "2026-06-10 14:00",
     media: ["https://cdn.example.com/video.mp4"],
     additional: {
       youtube: { postType: { value: "short" },
         post: { title: "API Quick Tip", privacyStatus: "public", selfDeclaredMadeForKids: "no" } }
     }
   })
```

### Post a freshly generated image

```
1. (generate-image skill) → asset_id "a1b2c3…"
2. social_getSocialMediaAccounts({ network: "instagram" })
3. social_createSocialMediaPost({
     message: "Meet the new drop 👟",
     account_ids: [123],
     action: "draft",
     media: ["a1b2c3…"],                       // asset UUID from generate-image
     additional: { instagram: { postType: { value: "post" }, channel: { value: "direct" } } }
   })
```

### Reddit draft

```
1. social_getSocialMediaAccounts({ network: "reddit" })
2. social_createSocialMediaPost({
     message: "What we learned from shipping our new workflow",
     account_ids: [789],
     action: "draft",
     additional: {
       reddit: {
         post: {
           targets: [{
             subreddit: "devtestsmp",
             title: "What we learned from shipping our new workflow",
             type: "self",
             flairId: null,
             flairText: null,
             nsfw: false,
             url: null
           }]
         }
       }
     }
   })
```

### Link in the first comment after 5 minutes

```
1. Preview and confirm both the main post and:
   first comment: "Read the full guide: https://example.com/guide"
   delay: 5 minutes after the post publishes
2. social_createSocialMediaPost({
     message: "We published a practical guide to better campaign reviews.",
     account_ids: [123],
     action: "schedule",
     date: "2026-06-10 14:00",
     comments: [{
       message: "Read the full guide: https://example.com/guide",
       delay: 300
     }]
   })
```

### Analytics: Account Overview

```
1. social_getSocialMediaAccounts({ network: "facebook" })
2. social_getSocialMediaAnalyticsAggregated({ account_id: 789, date_from: "2026-05-01", date_to: "2026-05-31" })
```

## Gotchas

- **Analytics `account_id` is an integer** — use the numeric `id` from `social_getSocialMediaAccounts`.
- **Analytics date format** is `YYYY-MM-DD` (no time component, unlike post scheduling); never set `date_to` in the future.
- **Unknown metrics are silently ignored** by `social_getSocialMediaAnalyticsRange` — check `references/analytics.md` for per-network availability.
- **Audience data availability varies** — `social_getSocialMediaAnalyticsAudience` may return partial or empty data depending on the network.
- **Post `date` format** must be `YYYY-MM-DD HH:MM` (24-hour, no seconds, no timezone — uses account timezone).
- **Media** must be a Simplified asset UUID (from `generate-image` with `storage:"asset"`) or a publicly accessible URL — localhost does not work.
- **Local media** uses `api_signAssetUpload` → direct storage PUT →
  `api_registerAsset`; never send a local path to the hosted connector.
- **`date` is required** when `action` is `schedule` — omit it for `add_to_queue` and `draft`.
- **Platform character limits** — see `references/platform-settings.md`.
- **Auto-comments** — `comments[].delay` is measured in seconds after the post
  publishes. For X minutes use `X * 60`; the delay is not relative to the previous
  comment, and comments do not support media.
- **Reddit targets are required** — include at least one entry in
  `additional.reddit.post.targets`; omit the `r/` prefix from `subreddit`.
- **Instagram always requires `channel`** — include `channel: { value: "direct" }` for every Instagram post.
- **TikTok `postType`** values are `video` and `photo` (not `image`); **channel** values are `direct` and `reminder` (not `business`).
- **LinkedIn audience** value is `LOGGED_IN` (not `LOGGED_IN_MEMBERS`).
- **Google `topicType`** only has `STANDARD`, `EVENT`, `OFFER` (no `PRODUCT`).
- **Instagram story** — message must be empty (`""`), max 1 photo.
- **Reels and Shorts require video** — Instagram reel, Facebook reel, YouTube short all require a video file in `media`; images are not allowed.
- **YouTube always requires `post.title`** — include `additional.youtube.post` with a `title` for every YouTube video or short.
