---
name: local-business-marketing
description: Plan and create locally relevant social and Google Business content for location-based and service-area businesses. Use when the user asks for local marketing, neighborhood content, Google Business posts, store or restaurant promotion, appointment or booking campaigns, local events, service-area awareness, foot-traffic content, location launches, or a practical social plan for a small local business.
---

# Local Business Marketing

Turn local relevance, operational truth, community proof, and timely offers into content that drives calls, bookings, directions, visits, and qualified inquiries.

## Guardrails

- Verify business name, locations or service area, hours, availability, prices, offer terms, event dates, phone/booking destination, and required disclaimers before publishing them.
- Never fabricate reviews, customer identities, local partnerships, awards, scarcity, neighborhood knowledge, or “near me” relevance.
- Treat regulated services, health claims, financial claims, age restrictions, and before/after results conservatively; surface required approvals.
- Do not publish the same generic promotional caption to every location or platform.
- Create drafts first. Obtain explicit approval of location, offer terms, CTA destination, date, account, and media before scheduling or queueing.
- Stop on authorization failure or when the requested local account is not connected.

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

## Output

Lead with the local growth objective and conversion path. Then provide the channel/location roles, content plan, verification checklist, drafts created, measurement plan, and any operational fact blocking publication.
