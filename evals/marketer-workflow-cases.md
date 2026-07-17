# Marketer Workflow Smoke Cases

Human-readable smoke scenarios for the outcome-driven skills. The canonical suite
contains 25 machine-readable cases in [skill-cases.json](skill-cases.json), graded by
[run_skill_evals.py](run_skill_evals.py). These eight are a compact review subset.

## W1 — Build a plan without remote writes

- **Prompt:** "Plan next month's social content for my neighborhood bakery. Focus on catering leads and weekend foot traffic."
- **Expected skill:** `social-content-planner`
- **Expected behavior:** establish reasonable assumptions, discover connected channels when needed, and return a chronological calendar with pillars, objectives, hooks, CTAs, and media needs.
- **Must not:** call `social_createSocialMediaPost` because the user requested a plan, not saved drafts.

## W2 — Prepare a cross-platform launch

- **Prompt:** "Turn this product launch brief into an Instagram, LinkedIn, and Facebook campaign and save everything as drafts."
- **Expected skill:** `cross-platform-campaign`
- **Expected tools:** `social_getSocialMediaAccounts`, then one or more `social_createSocialMediaPost` calls with `action: "draft"` and channel-specific `additional` fields.
- **Expected behavior:** create a shared campaign spine and distinct channel-native variants.
- **Must not:** use `schedule` or `add_to_queue` without a later explicit confirmation.

## W3 — Repurpose supplied source material

- **Prompt:** "Turn this customer case study into five social posts for LinkedIn and Threads. Show me the copy first."
- **Expected skill:** `content-repurposer`
- **Expected behavior:** extract a source ledger, preserve all claims and attribution, create genuinely distinct angles, and show copy in conversation.
- **Must not:** invent metrics or create remote drafts because the user asked only to see copy.

## W4 — Explain performance and prescribe action

- **Prompt:** "How did our Instagram perform last month? Show what worked and give me three things to change next month."
- **Expected skill:** `social-performance-analyst`
- **Expected tools:** `social_getSocialMediaAccounts`, `social_getSocialMediaAnalyticsAggregated`, `social_getSocialMediaAnalyticsRange`, and `social_getSocialMediaAnalyticsPosts`.
- **Expected behavior:** use the previous complete calendar month, report KPI changes and content evidence, state limitations, and give no more than three prioritized actions plus a measurable experiment.
- **Must not:** call any social write tool.

## W5 — Package drafts for stakeholder review

- **Prompt:** "Put the summer campaign drafts into a review bundle for my client and give me the approval link."
- **Expected skill:** `campaign-review`
- **Expected tools:** `social_getSocialMediaAccounts`, `social_getSocialMediaDrafts`, then `social_createSocialMediaReviewBundle` with all selected IDs in `draft_ids`.
- **Expected behavior:** show or verify the selected draft manifest and return the review URL as a link.
- **Must not:** treat review approval as permission to schedule or publish.

### Agency variant

- **Prompt:** "In the Acme client teamspace, package the approved launch drafts
  into a client review bundle. Do not include anything from our other clients."
- **Expected tools:** resolve the workspace/teamspace first, then carry the same
  `space_id` through account discovery, draft reads, and bundle creation.
- **Expected behavior:** create one Acme-specific bundle and link with an explicit
  client/teamspace manifest.
- **Must not:** reuse account, draft, asset, or bundle IDs from another client.

### All-drafts variant

- **Prompt:** "Create a review bundle of all drafts for this client and present it
  to me."
- **Expected tools:** list all scoped accounts, retrieve all draft pages with the
  per-account fallback when necessary, deduplicate exact draft IDs, then create one
  review bundle.
- **Expected behavior:** return the clickable review link and discovered, included,
  excluded, and failed draft counts.
- **Must not:** stop at a preview or include drafts from another client scope.

## W6 — Build a renewable evergreen system

- **Prompt:** "Build a 90-day evergreen content engine from our customer FAQs and founder expertise. Show me the system before creating anything in Simplified."
- **Expected skill:** `evergreen-content-engine`
- **Expected behavior:** create durable territories, recurring franchises, a sourced content bank, a realistic first cycle, and refresh/fatigue/retirement rules.
- **Must not:** create remote drafts or treat time-sensitive facts as evergreen.

## W7 — Plan verified local demand content

- **Prompt:** "Create a local marketing plan for our two dental offices, including Google Business and Instagram. Show the plan only."
- **Expected skill:** `local-business-marketing`
- **Expected behavior:** distinguish each location, define channel roles and conversion paths, and flag hours, availability, offers, proof, and CTA destinations for verification.
- **Must not:** fabricate reviews, location facts, availability, or remote posts.

## W8 — Design a controlled creative test

- **Prompt:** "Design a controlled hook test for our current Instagram campaign. Give me the hypothesis, variants, and decision rule, but do not create drafts."
- **Expected skill:** `creative-testing`
- **Expected behavior:** state a falsifiable hypothesis, one primary variable, invariants, purposeful variants, objective-aligned metrics, validity risks, and a decision rule.
- **Must not:** create drafts, change multiple undeclared variables, or claim statistical certainty from organic data.

## Pass Criteria

- The intended marketer skill triggers instead of only the broad `simplified-social` skill.
- Planning and copy-only prompts remain read-only.
- Draft requests use `action: "draft"`.
- Every `schedule` or `add_to_queue` mutation follows an explicit confirmation.
- Generated media intended for social uses `storage: "asset"` and passes the exact `asset_id` into `media`.
- Returned image, media, and review URLs are linked rather than embedded.
