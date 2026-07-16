---
name: evergreen-content-engine
description: Build a renewable, long-lived content system that repeatedly turns durable brand expertise, customer questions, proof, and offers into channel-native social content. Use when the user asks for an evergreen strategy, always-on content engine, recurring content series, 60- or 90-day program, content bank, sustainable posting system, content recycling plan, or a way to keep publishing without chasing daily trends.
---

# Evergreen Content Engine

Design a compounding content program in which durable ideas become repeatable franchises, varied executions, and measurable learning—not a calendar filled with generic tips.

## Guardrails

- Do not label time-sensitive offers, statistics, platform features, event dates, seasonal advice, or changing regulations as evergreen.
- Treat brand claims, customer proof, prices, outcomes, and quotations as source-dependent. Never manufacture authority or testimonials.
- Separate planning, remote draft creation, scheduling, and publishing authorization.
- Create remote posts only with `action: "draft"` unless the user explicitly approves a final schedule or queue action.
- Do not automate indefinite recycling. Every reusable asset needs a review date, fatigue signal, and retirement rule.
- Stop when Simplified is unauthorized or required accounts are not connected.

## Workflow

1. Define the business objective, audience segments, buying questions, offers, expertise, proof library, content capacity, channels, cadence, and measurement horizon. State assumptions rather than forcing a long intake.
2. Call `social_getSocialMediaAccounts` once when connected-channel planning or drafting is requested.
3. If the user wants an evidence-led engine, inspect recent aggregated, trend, and post analytics. Use `$social-performance-analyst` for a full diagnosis.
4. Build a durable source map: customer questions, misconceptions, decision criteria, demonstrations, processes, founder/operator insight, customer evidence, and objection handling. Distinguish owned expertise from borrowed opinion.
5. Define three to five content territories with a strategic job, audience problem, credible point of view, proof sources, conversion bridge, and exclusions.
6. Turn territories into recurring franchises such as teardown, checklist, FAQ, myth, before/after process, decision guide, customer lesson, or behind-the-scenes operating principle.
7. Create a content bank with atomic ideas. Score each for relevance, distinctiveness, evidence strength, reuse potential, production effort, and shelf life using [references/content-system.md](references/content-system.md).
8. Build a 60- or 90-day sequence that balances discovery, trust, consideration, proof, and conversion. Rewrite ideas for each channel instead of duplicating captions.
9. When drafts are requested, call `social_createSocialMediaPost` with `action: "draft"`, permanent asset IDs, and platform settings from `../simplified-social/references/platform-settings.md`.
10. Define the renewal loop: review results, retain winners, vary one meaningful element, refresh changed claims, pause fatigued concepts, and feed learning back into the bank.

## Marketing Standard

- Start from audience decisions and recurring problems, not arbitrary posting categories.
- Give each territory a defensible brand angle. “Educational content” is not a territory until it has a subject, viewpoint, and audience consequence.
- Build memory through recognizable recurring formats while changing examples, hooks, proof, and creative treatment.
- Maintain an intentional conversion bridge. Evergreen does not mean every post sells, but the program should make the next step obvious over time.
- Protect production sustainability. A viable engine respects access to experts, customer proof, design/video capacity, approval time, and channel cadence.
- Use performance as directional evidence; do not let one outlier post rewrite the entire strategy.

## Output

Lead with the evergreen thesis and audience value. Then provide territories, franchises, source requirements, content-bank priorities, cadence, a dated first cycle, refresh/retirement rules, success measures, and the exact authorized state: plan, drafts, or awaiting scheduling approval.
