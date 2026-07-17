# `smp social` — Social Media Reference

Connected accounts, posts (publish/draft/schedule), tags, and analytics.

## Capabilities at a Glance

- **Accounts** — `get-social-media-accounts`
- **Posts** — create, update, delete (published)
- **Drafts** — get, update, delete (unpublished)
- **Tags** — list, create
- **Analytics** — range (time series), posts, aggregated, audience

## Posting

```bash
# 1. Find the connected accounts
smp social get-social-media-accounts

# 2. Publish, schedule, or draft a post
smp social create-social-media-post \
  --message "Big launch tomorrow!" \
  --account-ids '["<account_uuid>"]' \
  --action publish                          # publish | schedule | draft
```

### Action types

- `publish` — go out immediately
- `schedule` — publish at `--date "YYYY-MM-DD HH:MM"`
- `draft` — save as a draft (no publish)

### Media

`--media` accepts a JSON array. Each entry is either:
- A **Simplified asset UUID** (resolved server-side to a fresh permanent URL).
  Use this when the media was produced by `smp api generate-image` with
  `storage: "asset"`.
- A **fully qualified URL** (passed through as-is). Use only for media at a
  permanent public location.

```bash
smp social create-social-media-post \
  --message "..." \
  --account-ids '["<account>"]' \
  --action publish \
  --media '["<asset_uuid>"]'
```

### Scheduling

```bash
smp social create-social-media-post \
  --message "Live in 24h" \
  --account-ids '["<account>"]' \
  --action schedule \
  --date "2026-06-15 09:00"
```

### Tags

Tags are user-facing labels used to filter the Drafts/Publishing views.

```bash
smp social list-social-media-tags
smp social create-social-media-tag --name "Q2-launch"

smp social create-social-media-post \
  --message "..." \
  --account-ids '["<account>"]' \
  --action draft \
  --tags '["<tag_id>"]'
```

## Updating and Deleting

```bash
# Published post
smp social update-social-media-post --post-id <uuid> --message "..."
smp social delete-social-media-post --post-id <uuid>

# Draft (addressed by group id, not post id)
smp social update-social-media-draft --group-id <uuid> --message "..."
smp social delete-social-media-draft --group-id <uuid>
```

## Reading

```bash
smp social get-social-media-posts                # published
smp social get-social-media-drafts               # unpublished
```

## Analytics

```bash
# Aggregated metrics (followers, engagement, reach)
smp social get-social-media-analytics-aggregated --account-id <id>

# Per-post breakdown
smp social get-social-media-analytics-posts --account-id <id>

# Time series
smp social get-social-media-analytics-range \
  --account-id <id> \
  --start-date "2026-04-01" \
  --end-date "2026-05-01"

# Audience demographics (follower breakdown by age/gender/geo)
smp social get-social-media-analytics-audience --account-id <id>
```

## Gotchas

**Drafts are addressed by `group-id`, not `post-id`.** Use
`update-social-media-draft` / `delete-social-media-draft` for drafts, and
`update-social-media-post` / `delete-social-media-post` for published posts.

**`--account-ids` is a JSON array** — `'["<uuid>"]'`, not `<uuid>`.

**Media UUIDs vs URLs.** Prefer asset UUIDs over URLs whenever the media is in
Simplified — the server resolves to a fresh signed URL at publish time,
avoiding link-rot.

## Discovering Commands

```bash
smp social --help
smp social <command> --help
```
