---
name: social-performance-analyst
description: Analyze connected social accounts and translate metrics into decisions for marketers and small businesses. Use when the user asks how social performed, requests a weekly or monthly report, wants winners and losers, needs KPI or audience analysis, asks what content worked, wants account comparisons, or needs evidence-based recommendations for the next content plan.
---

# Social Performance Analyst

Turn Simplified social analytics into clear signals, limitations, and next actions. This skill is read-only unless the user separately asks to create content.

## Workspace and handoff

Before connected operations, use `simplified-workspace` when the client/workspace/teamspace is named or uncertain. Resolve the exact numeric teamspace and carry its `space_id` on every related account, analytics, asset, generation, draft, tag, review, and continuation call. Re-list scoped resources after switching clients; stop on access failures rather than falling back to another space. Pass the resolved context to every delegated skill.

## Workflow

1. Resolve the reporting period. Use the previous complete calendar month for "last month" and the last 30 completed calendar days ending yesterday (date_from = today minus 30 days, date_to = yesterday) for an unspecified recent period. Never send a future `date_to`. For a user-requested period through today, label today as partial. Pass a known IANA `tz` only to tools exposing it (Range and Audience); Posts and Aggregated do not expose `tz`, so disclose day-boundary limitations when material.
2. Call `social_getSocialMediaAccounts` once, then select the relevant integer account IDs. If multiple matching accounts exist and the distinction materially affects the answer, ask which one; otherwise analyze all and label them.
3. Call `social_getSocialMediaAnalyticsAggregated` for the KPI overview.
4. Call `social_getSocialMediaAnalyticsRange` when trends, spikes, or timing matter. Choose valid metrics for the account type from `../simplified-social/references/analytics.md`.
5. Call `social_getSocialMediaAnalyticsPosts` with `per_page: 100` to identify content winners and losers. Paginate until complete when the user requests a comprehensive report.
6. Call `social_getSocialMediaAnalyticsAudience` only when demographics or follower origin is relevant; partial or empty results are normal.
7. Compare `value` with `prevValue`. Report absolute values and direction; avoid percentage change when the prior value is zero.
8. Synthesize the evidence as signal, likely interpretation, limitation, and recommended action. Do not claim causation from correlation.

## Analysis Standard

- Separate reach or impressions, engagement, audience growth, and publishing volume.
- Normalize account comparisons where possible; raw totals across different networks are not directly equivalent.
- Connect post-level observations to concrete attributes such as topic, format, hook, CTA, or timing only when the returned data supports it.
- Note sparse data, missing metrics, platform attribution windows, and incomplete audience fields.
- Recommend no more than three prioritized actions and attach each to an observed signal.
- Suggest a measurable next experiment, including what to change and which metric will determine success.

## Failure Handling

- On `401`, stop and ask the user to authorize the Simplified connector.
- On an empty account list, explain that social accounts must be connected in Simplified.
- If a metric is unsupported or silently omitted, report that limitation rather than treating it as zero.

## Output

Lead with a concise performance verdict. Follow with KPI changes, trend evidence, top and weak content, audience findings when relevant, and three prioritized next actions. Include the exact reporting period and account names.
