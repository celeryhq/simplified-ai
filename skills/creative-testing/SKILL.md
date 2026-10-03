---
name: creative-testing
description: Design, produce, and evaluate disciplined social creative tests for marketers. Use when the user asks for A/B tests, hook tests, creative variants, message experiments, format tests, offer or CTA tests, an experimentation roadmap, ways to improve a campaign systematically, or draft variants whose results can produce a reusable marketing learning.
---

# Creative Testing

Create tests that isolate a meaningful decision and produce learning the team can reuse—not a pile of unrelated variants.

## Guardrails

- Do not claim statistical significance from ordinary organic social comparisons, small samples, unequal delivery, or platform-reported totals without a valid experiment design.
- Hold audience, offer, placement, timing, and CTA constant when testing a creative variable unless one of those is the declared variable.
- Preserve factual claims and required disclaimers across variants. Never make a test “stronger” by inventing proof or urgency.
- Image or video generation spends credits. Confirm ambiguous generation and avoid generating variants that do not test a defined hypothesis.
- Create variants as drafts and require explicit approval before scheduling or queueing.
- Do not automatically declare a winner from the highest raw engagement count; match the decision metric to the objective.

## Workspace and handoff

Before connected operations, use `simplified-workspace` when the client/workspace/teamspace is named or uncertain. Resolve the exact numeric teamspace and carry its `space_id` on every related account, analytics, asset, generation, draft, tag, review, and continuation call. Re-list scoped resources after switching clients; stop on access failures rather than falling back to another space. Pass the resolved context to every delegated skill.

## Workflow

1. Define the business decision: what choice will change if this test succeeds? Resolve objective, audience, offer, channel/placement, conversion path, current control, constraints, and available volume.
2. Call `social_getSocialMediaAccounts` once when a connected baseline or connected-account drafts are needed. When a baseline exists, retrieve relevant aggregated, range, and post analytics. Distinguish observed patterns from hypotheses.
3. Write one falsifiable hypothesis: changing **X** for **Y audience/context** should improve **Z metric** because **reason**.
4. Select one primary variable: hook, promise framing, proof type, visual treatment, opening frame, format, CTA language, creator/brand voice, or offer framing. Use [references/experiment-design.md](references/experiment-design.md) to control confounds.
5. Define the control and two to four purposeful variants. Each variant must express a distinct strategic alternative, not superficial synonym changes.
6. Choose a primary decision metric and guardrails before production. Examples: qualified reach/video hold for attention, saves or substantive engagement for utility, clicks/leads/bookings for response, and negative feedback for audience cost.
7. Produce a test matrix with invariant elements, variable, hypothesis, assets, account/placement, run window, minimum practical evidence, and decision rule.
8. If new creative is authorized, use `$generate-image` or `$generate-video` with reusable asset storage. Keep composition, product, and brand constants unless visual treatment is the tested variable.
9. When the user requests saving/creating drafts, create each execution with `social_createSocialMediaPost` and `action: "draft"`, using required platform settings from `../simplified-social/references/platform-settings.md`. Never publish one variant early and call it a fair comparison.
10. After the run, use `$social-performance-analyst` to compare results. Record result, confidence/limitations, learning, next decision, and follow-up test. Retain a control until a challenger wins under a credible comparison.

## Experimentation Standard

- Prioritize high-leverage uncertainty. Test the promise or proof before button color, emoji, or trivial copy edits.
- Separate exploration from validation. Early tests can identify promising territories; later tests should isolate and confirm the driver.
- Build variants from different audience tensions or persuasion mechanisms, not random creativity.
- Evaluate platform delivery effects, audience overlap, spend, timing, and sample imbalance before attributing performance to creative.
- Stop tests that create brand, legal, reputational, or customer-experience risk regardless of short-term metrics.
- Turn each result into a reusable rule with scope: what worked, for whom, where, under what conditions, and what remains unknown.

## Media and write results

Use `manage-assets` to find existing library media before generating copies. Resolve names/tags through exposed asset discovery, preserve pagination and scope, import accessible remote files, and require ready assets before generation or attaching media. Check byte access and HTTP PUT capability before signing a local/chat attachment upload; if unavailable, ask for a Simplified asset ID or downloadable URL. Pass permanent UUIDs into drafts. A missing required visual remains a stated production gap; do not report a media-ready post without it.

For a batch of drafts, retain each successful returned ID and report created, pending, and failed items. Continue only unfinished items; do not recreate successful drafts after a later failure. A plan or test design alone does not authorize remote writes.

## Output

Lead with the decision and hypothesis. Then show the controlled matrix, draft/asset status, measurement and stopping rules, validity risks, and the learning record the team should complete after results arrive.
