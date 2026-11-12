---
name: social-content-planner
description: Build goal-led weekly or monthly social content calendars for marketers, social media managers, and small businesses. Use when the user asks for a content plan, posting calendar, campaign calendar, content pillars, posting cadence, ideas to fill calendar gaps, or a set of social drafts organized across dates and channels.
---

# Social Content Planner

Turn business goals into a practical, channel-aware content calendar. Use the Simplified hosted MCP connector for account discovery, analytics, drafts, tags, and scheduling.

## Guardrails

- Treat planning, drafting, and publishing as separate levels of authorization.
- Return a plan in conversation when the user asks only for a plan. Do not create remote drafts unless requested.
- Use `action: "draft"` when the user asks to create or save the planned content.
- Before `schedule` or `add_to_queue`, verify that explicit authorization covers the final posts, accounts, dates, media, settings, and comments. Reuse unchanged existing authorization; show the concrete plan and ask only for missing approval.
- On `401`, pause affected connected operations and explain how to authorize Simplified. An empty account list does not block planning or requested accountless drafts; omit `account_ids`. Scheduling, queueing, and account analytics require suitable connected accounts.
- Use a native media preview when the client supports it and the user wants to review the result. Otherwise show a usable link. Refresh expired asset URLs; do not download remote media merely to bypass client display restrictions. Review bundles and other web pages remain links.

## Workspace and handoff

Before connected operations, use `simplified-workspace` when the client/workspace/teamspace is named or uncertain. Resolve the exact numeric teamspace and carry its `space_id` on every related account, analytics, asset, generation, draft, tag, review, and continuation call. Re-list scoped resources after switching clients; stop on access failures rather than falling back to another space. Pass the resolved context to every delegated skill.

## Workflow

1. Establish the planning frame: business goal, audience, offer or topic, date range, channels, cadence, key dates, and desired call to action. Ask only for information that materially changes the plan; otherwise state reasonable assumptions.
2. Call `social_getSocialMediaAccounts` once without a network filter when connected channels matter. Use only returned account IDs.
3. If the user wants a performance-informed plan, retrieve the relevant account analytics before ideating. Use `$social-performance-analyst` for a full analysis.
4. Create three to five useful content pillars. Balance education, proof, promotion, engagement, and brand or community content rather than repeating one message.
5. Assign each post a date, channel, pillar, objective, format, hook, core message, CTA, and asset requirement. Adapt the idea to each channel instead of copying identical text everywhere.
6. Present the calendar in chronological order and flag missing source material or media.
7. If remote drafts were requested, create each with `social_createSocialMediaPost` and `action: "draft"`. Include required platform-specific `additional` fields from `../simplified-social/references/platform-settings.md`.
8. If scheduling was requested, create or show drafts first, then obtain explicit approval of the final account/date/media matrix before scheduling. Existing approval of that unchanged concrete matrix is sufficient.

## Planning Heuristics

- Tie every post to one primary objective: awareness, engagement, consideration, conversion, retention, or trust.
- Use realistic cadence for the available channels and source material; do not fill a calendar with low-value repetition.
- Build sequences around launches and events: setup, reveal, proof, reminder, last call, and follow-up.
- For small businesses, prioritize offers, local relevance, customer proof, FAQs, behind-the-scenes content, events, and Google Business updates where appropriate.
- Reuse a campaign idea across channels, but rewrite the hook, length, CTA, hashtags, and format for each audience context.

## Media and write results

Use `manage-assets` to find existing library media before generating copies. Resolve names/tags through exposed asset discovery, preserve pagination and scope, import accessible remote files, and require ready assets before generation or attaching media. Check byte access and HTTP PUT capability before signing a local/chat attachment upload; if unavailable, ask for a Simplified asset ID or downloadable URL. Pass permanent UUIDs into drafts. A missing required visual remains a stated production gap; do not report a media-ready post without it.

For a batch of drafts, retain each successful returned ID and report created, pending, and failed items. Continue only unfinished items; do not recreate successful drafts after a later failure. A plan or test design alone does not authorize remote writes.

## Output

Summarize the strategy first, then show the calendar. End with counts by channel and pillar, unresolved inputs, and the exact next authorized action: plan only, drafts created, or awaiting scheduling approval.
