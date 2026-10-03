---
name: simplified-social
description: Create, retrieve, revise, schedule, or queue Simplified social posts and drafts; manage auto-comments and review bundles; retrieve account analytics. Use for direct social operations. For a content calendar, campaign strategy, or performance interpretation, use social-content-planner, cross-platform-campaign, or social-performance-analyst.
---

# Simplified Social Media

Schedule, queue, and draft social media posts, add timed auto-comments, and
retrieve analytics across 13 platforms using Simplified.com.

## Connector

All tools (`social_getSocialMediaAccounts`, `social_createSocialMediaPost`,
`api_createAsset`, etc.) are provided by the **Simplified hosted MCP connector**
(`https://apikit.simplified.com/mcp`). They are not built-in tools.

The connector is **OAuth-secured** — the connected client walks the OAuth flow; there is no API key to set.

## IMPORTANT: Before Any Operation

If any tool call returns a **401 / Unauthorized**, the Simplified connector is not authorized:

1. **Stop immediately** — do not retry the failed call.
2. **Inform the user** that they need to connect Simplified (authorize the connector) before social tools will work.
3. **Do not proceed** with the original request until the connector is authorized.

## Setup

1. Sign up at [simplified.com](https://simplified.com).
2. Connect your social media accounts in the Simplified dashboard.
3. Enable the Simplified connector in your client and complete the OAuth authorization.

## Core Workflow

For publishing, follow **Discover → Select → Compose → Confirm → Publish**.
For drafts, resolve workspace/teamspace scope and compose; a connected account is optional.
Carry an explicitly selected `space_id` through every related read, write, and poll.

### Step 1: Discover Accounts

Call `social_getSocialMediaAccounts` once without `network` to list connected accounts.
The `network` filter is deprecated; filter returned accounts client-side.

```
social_getSocialMediaAccounts({})
```

Returns `{ accounts: [...] }` where each account has `id` (integer), `name`, and `type` (see type values below).

If publishing or account-specific analytics requires an account and the list is empty,
explain that an account must be connected. For a requested draft, continue with
`action: "draft"` and omit `account_ids`; do not block accountless drafting.
For account-dependent operations, explain which account needs connecting in [Simplified](https://app.simplified.com).

### Step 2: Select Target Accounts

Pick one or more account IDs from the results and serialize them as strings for
posting, e.g. `account_ids: ["123"]`. Analytics `account_id` remains an integer;
draft/post listing `account_ids` is a comma-separated string. You can post to
multiple accounts in a single call.

### Step 3: Compose the Post

Build the post payload:
- `message` (required) — the post text, max 5000 chars at the connector boundary
  (tighter per-platform limits apply)
- `account_ids` (required for publishing actions) — array of stringified target account IDs
- `action` (required) — `schedule`, `add_to_queue`, or `draft`
- `date` — required for `schedule`, format: `YYYY-MM-DD HH:MM`
- `media` — array (max 10) of **Simplified asset UUIDs**, public media URLs, or `{url, thumbUrl}` objects for video with an explicit poster
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

Publishing is outward-facing. For `schedule` / `add_to_queue`, show the composed
post, target accounts, timing, and auto-comments for approval. Existing explicit
authorization covering that exact content, targets, and timing is sufficient;
ask only when authorization is missing or the proposed publication changed.
An internal `action:"draft"` preview is useful when content still needs review.
Then call `social_createSocialMediaPost`.

If the post includes auto-comments, the authorized publication plan must cover each comment's text
and post-relative delay. For “link in first comment after X minutes,” convert
nonnegative minutes to an integer number of seconds with `delay = X * 60`.
`delay` is measured in seconds after the post publishes, not after the previous
comment. Comments execute in array order. Do not move the comment text into the
main post.

**Media presentation.** Use a native media preview when the client supports it and the user wants to review the result. Otherwise show a usable link. Refresh expired asset URLs; do not download remote media merely to bypass client display restrictions. Review bundles and other web pages remain links.

## Choosing the Right Analytics Tool

| User asks about... | Tool to call |
|---|---|
| Trends over time, charts, metric growth/decline | `social_getSocialMediaAnalyticsRange` |
| Specific posts, best/worst performing content | `social_getSocialMediaAnalyticsPosts` |
| Account overview, KPIs, period summary | `social_getSocialMediaAnalyticsAggregated` |
| Demographics, follower origins, age/gender breakdown | `social_getSocialMediaAnalyticsAudience` |
| "Show me analytics" with no further context | `social_getSocialMediaAnalyticsAggregated` + `social_getSocialMediaAnalyticsRange` with key metrics |

## Read details for the current operation

- Accounts, draft listing/revisions, review bundles, and action selection: [references/operations.md](references/operations.md). Accountless drafts can be created, but the current draft listing requires connected account IDs; retain actual create-response IDs and disclose that listing limitation.
- Platform-specific `additional` fields, supported media, and enums: [references/platform-settings.md](references/platform-settings.md). Read only the relevant platform before writing. Mastodon and Telegram have no dedicated additional-settings branch; Reddit requires `additional.reddit.post.targets`.
- Analytics metrics, periods, status fields, and response shapes: [references/analytics.md](references/analytics.md). Missing/unsupported metrics are not zero; paginate comprehensive reports.
- Local media intake and readiness: [references/assets.md](references/assets.md).
- Concrete queue, scheduled-video, generated-image, Reddit, and auto-comment payloads: [references/examples.md](references/examples.md).

## Timing and completion

For scheduling, resolve workspace settings and selected account metadata. The create tool has no timezone argument. Convert a user-specified timezone only after establishing the service's interpretation; retain a draft if a material conflict remains unresolved. Send `date` as `YYYY-MM-DD HH:MM`, with no seconds or timezone suffix.

“Post now” requests `add_to_queue`; actual timing is service-determined and immediate delivery is not guaranteed. Report returned status/timing. “Save” or “draft” requests `action: "draft"`.

For batches, retain each successful typed draft/group ID and continue only unfinished items. A successful call must still be inspected for actual output; do not invent IDs or duplicate successful drafts after a later failure. Publication and review-bundle approval remain separate.
