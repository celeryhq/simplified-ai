---
name: campaign-review
description: Prepare Simplified social drafts for client, stakeholder, or team review and manage approval-ready revisions. Use when the user asks to package selected or all drafts for approval, create and present a social review link or review bundle, collect a campaign for client review, inspect draft status, revise selected drafts, or prepare approved content for a later publishing step.
---

# Campaign Review

Turn a group of social drafts into a clear approval package without publishing them.

## Guardrails

- A review bundle is not publishing authorization. Never schedule or queue posts from approval language alone.
- Create a shareable review bundle when the user explicitly asks to package or send drafts for review. Otherwise preview the proposed bundle first.
- For agencies or multi-client work, create one review bundle per client and
  campaign. Never combine drafts from different clients, workspaces, or teamspaces
  in the same bundle.
- Modify only drafts the user selected or changes they approved.
- Do not expose internal IDs as the primary presentation; use names, channels, dates, and short copy previews.
- Present returned review URLs as clickable links, never embedded content.
- Stop on `401` or when Simplified is not connected.

## Workflow

1. Establish the client, campaign or review scope, reviewer, desired deadline, and
   which drafts should be included. Infer scope from the active campaign only when
   unambiguous.
2. For a named client workspace or teamspace, hand off first to
   `$simplified-workspace`: call `api_getWorkspaceInfo`, resolve the exact numeric
   teamspace ID with `api_listTeamspaces` when needed, state the selected client
   context, and pass the same `space_id` on every downstream account, draft,
   update, and review-bundle call. Re-resolve context when switching clients.
3. If exact draft IDs are already known, reuse them only after verifying they belong
   to the selected client scope. Otherwise call `social_getSocialMediaAccounts`,
   select the relevant account IDs, then call `social_getSocialMediaDrafts` with
   those IDs as the required comma-separated `account_ids` string. If that
   multi-account lookup returns no rows when drafts are expected, use the read-only
   per-account fallback: query each selected account separately, merge the results,
   and deduplicate by exact draft ID. Never create replacement drafts, invent draft
   IDs, assume that every draft belongs in the bundle, or reuse IDs from another
   client scope.
   - If the user explicitly asks for **all drafts**, select every connected account
     in the resolved client scope. Retrieve every draft page for those accounts,
     using `per_page: 100` and incrementing `page` until the response is exhausted.
     Apply the per-account fallback when needed, merge the results, and deduplicate
     by exact draft ID. This covers drafts discoverable for connected accounts in the resolved client
     scope. Accountless drafts can exist, but the current listing requires account
     IDs and does not establish coverage of accountless drafts. Disclose this
     limitation rather than claiming complete workspace coverage; include separately
     supplied draft IDs only after scoped verification.
4. Present a review manifest with client/teamspace, draft, channel/account, copy
   preview, media status, planned timing, and issues requiring attention. If the
   user did not identify the drafts, let them choose from this manifest before
   creating the bundle.
5. Apply requested supported changes with `social_updateSocialMediaDraft`: its
   current schema accepts `draft_id`, `message`, `media`, `tags`, `date`, `time`,
   and `timezone`. Carry the selected `space_id`. Account reassignment and platform
   `additional` settings are not exposed by this update operation. Explain that
   limitation; create a replacement draft only when explicitly requested, retaining
   the original unless its removal is separately authorized.
6. When authorized, call `social_createSocialMediaReviewBundle` once with `title`,
   optional `description`, all selected draft IDs in `draft_ids`, and the same
   `space_id`. Use a client-identifying title such as
   `Client — Campaign — Review round`.
7. Verify which drafts were included and return the response's `linkToReview` URL
   plus a concise manifest. For an “all drafts” request, state the total discovered,
   included, excluded, and failed counts so the user can verify completeness. Keep
   a separate bundle/link record for each client.
8. For an authorized append, use `social_addDraftsToSocialMediaReviewBundle` when
   exposed, with the verified `bundle_id`, nonempty selected `draft_ids`, and the
   same `space_id`. The current operation is idempotent. Inspect the returned full
   draft list and review URL. If the deployed client lacks this tool, explain the
   limitation; do not silently recreate or replace the bundle.
9. If the user later approves publication, hand off to `$simplified-social`: show the final account/date/media matrix and obtain explicit publishing confirmation before `schedule` or `add_to_queue` unless the user already approved that unchanged concrete matrix. Review approval alone is insufficient.

## Review Checklist

- Copy: factual accuracy, brand voice, CTA, spelling, and platform length.
- Targeting: correct connected account and audience setting.
- Media: present, accessible, and valid for the selected post type.
- Timing: intended date, verified scheduling timezone, campaign order, and no past dates.
- Platform requirements: all required `additional` fields are present.
- Campaign consistency: offer, link, naming, visual identity, and legal terms agree across drafts.
- Client isolation: every draft, account, and bundle belongs to the same resolved
  workspace/teamspace; no cross-client IDs or assets are present.

## Output

Report the client/teamspace, bundle name, included and excluded drafts, unresolved
issues, and the review URL. State clearly that the content remains in review and
has not been published or scheduled.

For an explicit “create a review bundle of all drafts and present it” request,
creating the bundle is authorized: do not stop at a hypothetical preview. Complete
the scoped draft collection, create the bundle once, and present its clickable
review link and manifest.
