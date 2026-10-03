# Social accounts, drafts, and reviews

### `social_getSocialMediaAccounts`

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| `network` | string | No       | Deprecated; omit and filter returned accounts client-side |

**Historical filter values:** `facebook`, `instagram`, `linkedin`, `tiktok`,
`tiktokBusiness`, `youtube`, `pinterest`, `threads`, `google`, `bluesky`.
Discover actual connected platforms from the unfiltered response.

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
| `account_ids` | string[]    | For publish | Target account IDs from `social_getSocialMediaAccounts`; omit/empty for an accountless `draft` |
| `action`      | string   | Yes      | `schedule`, `add_to_queue`, or `draft`   |
| `date`        | string   | For `schedule` | Schedule datetime: `YYYY-MM-DD HH:MM` (not in the past) |
| `media`       | array | No       | Asset UUIDs, public media URLs, or `{url, thumbUrl}` objects (max 10) |
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

### `social_addDraftsToSocialMediaReviewBundle`

Append drafts to an existing bundle using required `bundle_id` (string) and
`draft_ids` (non-empty string array). Use the exact existing bundle ID and
discovered draft IDs. The operation is idempotent: existing drafts are skipped.
It returns the updated bundle and review link. Preserve the existing bundle
unless the user explicitly requests a replacement.


## Action Types

| Action         | When to Use                                          | `date` Required? |
|----------------|------------------------------------------------------|-------------------|
| `schedule`     | Post at a specific date/time                         | Yes               |
| `add_to_queue` | Queue for publishing; actual timing is service-determined     | No                |
| `draft`        | Save for later editing in the Simplified dashboard   | No                |

**Default:** When the user doesn't specify timing (or says "post now"), use `add_to_queue`; actual timing is service-determined and immediate delivery
is not guaranteed. There is no separate immediate-publish action.
Report the returned scheduling/status information instead of promising an exact time. When they give a date/time, use `schedule`. When they say "save" or "draft", use `draft`.

