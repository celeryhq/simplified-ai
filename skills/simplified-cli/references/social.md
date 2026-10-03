# `smp social` reference

Use [simplified-social](../../simplified-social/SKILL.md) and its platform/analytics references for current behavioral rules. Use command help for exact installed flags.

## Accounts and drafts

```bash
smp social:get-social-media-accounts
smp social:create-social-media-post --message "Product launch preview" --action draft --account-ids '["<resolved-account-id>"]' --media '["<ready-asset-uuid>"]'
smp social:update-social-media-draft --draft-id <draft-id> --message "Updated approved copy"
smp social:create-social-media-post --message "An accountless draft" --action draft
```

Post `account_ids` entries are strings under the current request schema. Use the exact discovered account identifier, serialized as a string; do not invent an account UUID. Asset UUIDs are a different resource. Drafts can be accountless; publication cannot.

Actions are `draft`, `schedule`, and `add_to_queue`; there is no `publish` action. Scheduling/queueing requires concrete authorization and connected accounts. Read the current queue and timezone contract rather than promise immediate timing from the action name.

## Lifecycle identifiers

Draft updates take `draft_id`. Published deletion uses `group_id` and/or `post_schedule_id` according to the requested target; draft deletion accepts `group_id` or `draft_ids`. Inspect returned identifiers instead of assuming every operation takes a common post UUID.

```bash
smp social:delete-social-media-post --help
smp social:delete-social-media-draft --help
smp social:update-social-media-post --help
```

`media` accepts asset UUIDs, supported URLs, or URL/thumbnail objects. Prefer permanent asset UUIDs for Simplified files. Draft update supports copy, timing, media, and tags; it does not change destination accounts or platform-specific settings.

## Reviews and analytics

```bash
smp social:create-social-media-review-bundle --help
smp social:add-drafts-to-social-media-review-bundle --help
smp social:get-social-media-analytics-range --help
smp social:get-social-media-analytics-aggregated --help
smp social:get-social-media-analytics-posts --help
smp social:get-social-media-analytics-audience --help
```

Range uses `date_from`, `date_to`, and required `metrics`, not `start_date`/`end_date`. Timezone parameters vary by operation; pass only fields its schema exposes. Use comparable completed-day windows and disclose partial current-day data. Follow pagination and distinguish unavailable metrics from zero.
