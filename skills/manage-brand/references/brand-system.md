# Brand System Structure

## Brand kit layer

Store durable identity and visual-system fields in the brand kit:

- `brand.name`, `brand.description`, `brand.website`, and top-level `social_links`; store taglines in suitable messaging context rather than inventing a top-level build field
- `style.colors.primary`, `secondary`, `accent`, and `neutral`, each a list of tokens with `hex` and/or `name` and an optional `role`; preserve a supplied color name without inventing its hex code
- Headline and body typography
- Approved logos, lockups, clear-space guidance, and misuse rules
- Imagery principles, on-image copy rules, and AI-generation guardrails

Use `api_buildBrandKit` incrementally. Send only authorized sections that should change; omitted top-level sections remain unchanged. For an existing style or identity section, read the current value and merge the intended changes before sending it; do not assume a partial nested object preserves every sibling. Read the result back with `api_getBrandKit(expand="extra,website")`.

## Structured ICPs and content pillars

Canonical writes use `api_buildBrandKit` with `brand_id` and the relevant array:

- `icps`: 1–5 objects requiring `title` (1–200 characters) and `description` (20–10000). Optional fields are `is_primary`, `segment_name`, `industry`, `job_role`, and `company_size`. Titles must be unique; at most one entry is primary.
- `content_pillars`: 1–5 objects requiring `name` (1–200 characters) and `description` (20–4000). Optional fields are `tags`, `priority` (`high`, `medium`, `low`), and `preferred_channels`.

Objects reject unknown fields. Put richer strategic detail into the description or separate supporting context. Entries merge by case-insensitive title/name; omitted entries are preserved. Omit an array to leave it unchanged. An empty array is not a deletion operation. Rename/removal requires the relevant Brand Kit UI or a verified dedicated CRUD endpoint; changing a name may create an additional record.

Build is synchronous. Read back through context adapters with `api_getContextDocumentByType(brand_id=..., context_type="icps" or "content_pillars")`; the kit GET omits these write-only arrays. The `content_pillars` adapter returns `{doc_type, content}`, not a KnowledgeDoc ID, and may return 404 when no structured pillars exist even if a legacy context document does. Inventory legacy links separately; do not interpret that 404 as permission to create a competing pillar document.

## Context layer

Use a context document for knowledge that guides decisions or generation. Canonical types include:

- `brand_voice`
- `style_guide`
- `brand_profile`
- `market_positioning`
- `usps`
- `features`
- `writing_examples`
- `competitor_analysis`
- `seo_guidelines`
- `target_keywords`
- `marketing_strategy`

Check `api_getContextDocumentByType` with `context_type`, or filter `api_listContextDocuments` with `canonical_key`, before creating an ordinary canonical document. If one exists, read it and update it using `document_link_id`. This identifier can be the link UUID or the underlying KnowledgeDoc UUID. Do not create a competing source of truth. The structured ICP/pillar write paths above take precedence over legacy context-document storage for those records.

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
