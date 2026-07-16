---
name: campaign-review
description: Prepare Simplified social drafts for client, stakeholder, or team review and manage approval-ready revisions. Use when the user asks to package drafts for approval, create a social review link or review bundle, collect a campaign for client review, inspect draft status, revise selected drafts, or prepare approved content for a later publishing step.
---

# Campaign Review

Turn a group of social drafts into a clear approval package without publishing them.

## Guardrails

- A review bundle is not publishing authorization. Never schedule or queue posts from approval language alone.
- Create a shareable review bundle when the user explicitly asks to package or send drafts for review. Otherwise preview the proposed bundle first.
- Modify only drafts the user selected or changes they approved.
- Do not expose internal IDs as the primary presentation; use names, channels, dates, and short copy previews.
- Present returned review URLs as clickable links, never embedded content.
- Stop on `401` or when Simplified is not connected.

## Workflow

1. Establish the campaign or review scope, reviewer, desired deadline, and which drafts should be included. Infer scope from the active campaign when unambiguous.
2. If exact draft IDs are already known, reuse them verbatim. Otherwise call `social_getSocialMediaAccounts`, select the relevant account IDs, then call `social_getSocialMediaDrafts` with those IDs as the required comma-separated `account_ids` string. If that multi-account lookup returns no rows when drafts are expected, use the read-only per-account fallback: query each selected account separately, merge the results, and deduplicate by exact draft ID. Never create replacement drafts, invent draft IDs, or assume that every draft belongs in the bundle.
3. Present a review manifest with draft, channel/account, copy preview, media status, planned timing, and issues requiring attention. If the user did not identify the drafts, let them choose from this manifest before creating the bundle.
4. Apply requested copy, media, account, or settings changes with `social_updateSocialMediaDraft`, following the connector's current tool schema.
5. When authorized, call `social_createSocialMediaReviewBundle` once with `title`, optional `description`, and all selected draft IDs in `draft_ids`.
6. Verify which drafts were included and return the response's `linkToReview` URL plus a concise manifest.
7. The hosted connector currently does not expose a separate append-to-existing-bundle tool. If the user asks to append drafts, explain the limitation; do not silently recreate or replace the bundle.
8. If the user later approves publication, hand off to `$simplified-social`: show the final account/date/media matrix and obtain explicit publishing confirmation before `schedule` or `add_to_queue`.

## Review Checklist

- Copy: factual accuracy, brand voice, CTA, spelling, and platform length.
- Targeting: correct connected account and audience setting.
- Media: present, accessible, and valid for the selected post type.
- Timing: intended date, account timezone, campaign order, and no past dates.
- Platform requirements: all required `additional` fields are present.
- Campaign consistency: offer, link, naming, visual identity, and legal terms agree across drafts.

## Output

Report the bundle name, included and excluded drafts, unresolved issues, and the review URL. State clearly that the content remains in review and has not been published or scheduled.
