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
- Before any `schedule` or `add_to_queue` call, show the final posts, accounts, dates, media, and platform settings and obtain explicit confirmation.
- Stop on `401` or an empty account list and explain how to connect Simplified.
- Present returned URLs as links, never as embedded images.

## Workflow

1. Establish the planning frame: business goal, audience, offer or topic, date range, channels, cadence, key dates, and desired call to action. Ask only for information that materially changes the plan; otherwise state reasonable assumptions.
2. Call `social_getSocialMediaAccounts` once without a network filter when connected channels matter. Use only returned account IDs.
3. If the user wants a performance-informed plan, retrieve the relevant account analytics before ideating. Use `$social-performance-analyst` for a full analysis.
4. Create three to five useful content pillars. Balance education, proof, promotion, engagement, and brand or community content rather than repeating one message.
5. Assign each post a date, channel, pillar, objective, format, hook, core message, CTA, and asset requirement. Adapt the idea to each channel instead of copying identical text everywhere.
6. Present the calendar in chronological order and flag missing source material or media.
7. If remote drafts were requested, create each with `social_createSocialMediaPost` and `action: "draft"`. Include required platform-specific `additional` fields from `../simplified-social/references/platform-settings.md`.
8. If scheduling was requested, create or show drafts first, then wait for explicit approval before scheduling.

## Planning Heuristics

- Tie every post to one primary objective: awareness, engagement, consideration, conversion, retention, or trust.
- Use realistic cadence for the available channels and source material; do not fill a calendar with low-value repetition.
- Build sequences around launches and events: setup, reveal, proof, reminder, last call, and follow-up.
- For small businesses, prioritize offers, local relevance, customer proof, FAQs, behind-the-scenes content, events, and Google Business updates where appropriate.
- Reuse a campaign idea across channels, but rewrite the hook, length, CTA, hashtags, and format for each audience context.

## Output

Summarize the strategy first, then show the calendar. End with counts by channel and pillar, unresolved inputs, and the exact next authorized action: plan only, drafts created, or awaiting scheduling approval.
