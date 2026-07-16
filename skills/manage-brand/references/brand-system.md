# Brand System Structure

## Brand kit layer

Store durable identity and visual-system fields in the brand kit:

- Name, description, website, tagline, and social links
- Primary, secondary, accent, neutral, and functional colors with roles
- Headline and body typography
- Approved logos, lockups, clear-space guidance, and misuse rules
- Imagery principles, on-image copy rules, and AI-generation guardrails

Use `api_buildBrandKit` incrementally. Send only approved sections that should change; omitted sections remain unchanged. Read the result back with `api_getBrandKit(expand="extra,website")`.

## Context layer

Use a context document for knowledge that guides decisions or generation. Canonical types include:

- `brand_voice`
- `style_guide`
- `brand_profile`
- `market_positioning`
- `icps`
- `usps`
- `features`
- `content_pillars`
- `writing_examples`
- `competitor_analysis`
- `seo_guidelines`
- `target_keywords`
- `marketing_strategy`

Check `api_getContextDocumentByType` or filter `api_listContextDocuments` before creating a canonical document. If one exists, update that document; do not create a competing source of truth.

## Minimum useful content

### Brand voice

Include voice principles, tone shifts by context, vocabulary preferences, forbidden patterns, CTA style, and paired on-brand/off-brand examples.

### ICP

Include situation, trigger, job to be done, pain, outcome, objections, decision criteria, proof needs, and channel/content behavior. Mark inferred fields.

### Positioning and USPs

Identify category/frame of reference, audience, primary value, differentiators, reasons to believe, alternatives, and claim limitations.

### Content pillars

For each pillar, define strategic purpose, audience problem, credible brand angle, recurring formats, proof sources, conversion bridge, and exclusions.

## Change control

Before modifying a mature system, compare current and proposed content. Label each change as correction, clarification, addition, deprecation, or strategic decision. Preserve source notes in the context content when they affect claim confidence.
