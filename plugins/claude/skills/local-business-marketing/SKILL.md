---
name: local-business-marketing
description: Plan and create locally relevant social and Google Business content for location-based and service-area businesses. Use when the user asks for local marketing, neighborhood content, Google Business posts, store or restaurant promotion, appointment or booking campaigns, local events, service-area awareness, foot-traffic content, location launches, or a practical social plan for a small local business.
---

# Local Business Marketing

Turn local relevance, operational truth, community proof, and timely offers into content that drives calls, bookings, directions, visits, and qualified inquiries.

## Guardrails

Existing explicit authorization for unchanged content, accounts, timing, media, and comments is sufficient; ask only when that authorization is missing or the proposed effects change.

- Verify business name, locations or service area, hours, availability, prices, offer terms, event dates, phone/booking destination, and required disclaimers before publishing them.
- Never fabricate reviews, customer identities, local partnerships, awards, scarcity, neighborhood knowledge, or “near me” relevance.
- Treat regulated services, health claims, financial claims, age restrictions, and before/after results conservatively; surface required approvals.
- Do not publish the same generic promotional caption to every location or platform.
- Create drafts first. Obtain explicit approval of location, offer terms, CTA destination, date, account, and media before scheduling or queueing.
- Pause affected connected operations on authorization failure. If a local account is missing, continue planning or requested accountless drafts and state that publishing to that location requires its verified connected account.

## Workspace and handoff

Before connected operations, use `simplified-workspace` when the client/workspace/teamspace is named or uncertain. Resolve the exact numeric teamspace and carry its `space_id` on every related account, analytics, asset, generation, draft, tag, review, and continuation call. Re-list scoped resources after switching clients; stop on access failures rather than falling back to another space. Pass the resolved context to every delegated skill.

## Workflow

1. Establish location model: storefront, multi-location, mobile/service-area, appointment-led, event-led, or locally delivered ecommerce. Capture geography, audience, demand windows, offer, proof, conversion action, and operational constraints.
2. Call `social_getSocialMediaAccounts` once and map returned accounts to locations and channels. Do not infer that similarly named accounts represent the same branch.
3. Audit useful local inputs: FAQs, service availability, customer proof with permission, team expertise, products/menu, events, partnerships, landmarks, seasonality, weather sensitivity, inventory, and booking capacity.
4. Build a balanced plan using five jobs: be found, reduce uncertainty, prove trust, create timely reasons to act, and strengthen community relevance.
5. Choose platform roles using [references/local-channel-playbook.md](references/local-channel-playbook.md). Use Google Business for high-intent updates and actions; use social channels for discovery, familiarity, proof, and community context.
6. Write location-specific copy with a concrete local detail, customer value, proof or operational fact, and one primary CTA. Avoid keyword-stuffed city lists.
7. Plan authentic media: exterior/interior orientation, people with permission, process, product/service detail, local proof, event information, or offer creative. Upload local media through `$simplified-social` and retain permanent asset IDs.
8. Show a location/channel matrix containing date, account, post purpose, copy, media, CTA, offer terms, and verification status.
9. When authorized, create each post with `social_createSocialMediaPost` and `action: "draft"`. Apply exact Google Business and channel fields from `../simplified-social/references/platform-settings.md`.
10. Schedule or queue only after explicit approval. Measure by the intended business action where available, separating platform engagement from calls, bookings, visits, and revenue.

## Local Marketing Standard

- Lead with usefulness and specificity: what is available, for whom, where, when, why it matters, and what to do next.
- Use community content only when the relationship is real and relevant. Locality is context, not decoration.
- Balance demand capture with trust building: offers alone create promotion fatigue; lifestyle content alone may fail to drive action.
- Reflect capacity. Do not promote appointment slots, delivery coverage, inventory, or event access the business cannot fulfill.
- For multiple locations, preserve brand consistency while allowing meaningful local differences in team, proof, events, products, and CTA routes.

## Media and write results

Use `manage-assets` to find existing library media before generating copies. Resolve names/tags through exposed asset discovery, preserve pagination and scope, import accessible remote files, and require ready assets before generation or attaching media. Check byte access and HTTP PUT capability before signing a local/chat attachment upload; if unavailable, ask for a Simplified asset ID or downloadable URL. Pass permanent UUIDs into drafts. A missing required visual remains a stated production gap; do not report a media-ready post without it.

For a batch of drafts, retain each successful returned ID and report created, pending, and failed items. Continue only unfinished items; do not recreate successful drafts after a later failure. A plan or test design alone does not authorize remote writes.

## Output

Lead with the local growth objective and conversion path. Then provide the channel/location roles, content plan, verification checklist, drafts created, measurement plan, and any operational fact blocking publication.
