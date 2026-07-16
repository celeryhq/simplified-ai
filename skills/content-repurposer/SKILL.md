---
name: content-repurposer
description: Transform one source asset into multiple channel-native social posts and a reusable content sequence. Use when the user asks to repurpose a blog post, video, transcript, webinar, newsletter, announcement, product page, testimonial, case study, podcast, or existing social post into content for LinkedIn, Instagram, Facebook, TikTok, YouTube, Threads, Bluesky, Pinterest, or Google Business.
---

# Content Repurposer

Extract the strongest ideas from supplied source material and reshape them for the intended channels without inventing facts.

## Guardrails

- Treat the source as authoritative. Preserve names, numbers, claims, qualifications, links, and offer terms.
- Clearly label any interpretation that is not directly supported by the source.
- Return copy in conversation unless the user asks to save drafts.
- Create remote content with `action: "draft"`; require explicit approval before scheduling or queueing.
- Stop on MCP authorization failure or when required accounts are not connected.
- Present returned URLs as links, never as embedded media.

## Workflow

1. Read the complete source material available to the user. If only a link is provided, retrieve it with an available browsing or connector tool before writing; do not guess its contents.
2. Build a source ledger: central thesis, useful facts, proof points, quotes that may be paraphrased, stories, objections, CTA, and prohibited or unsupported claims.
3. Identify reusable angles such as insight, checklist, contrarian point, customer proof, behind-the-scenes detail, FAQ, short tip, and offer.
4. Select an output sequence that matches the source depth. Prefer fewer distinct posts over padded variations.
5. Adapt each post to the channel's audience behavior, length, hook, CTA, and media format. Do not merely shorten the same caption.
6. Call `social_getSocialMediaAccounts` once when the user wants connected-channel drafts.
7. Show the proposed set with its source angle and intended channel. If asked to save it, call `social_createSocialMediaPost` with `action: "draft"` and the required settings from `../simplified-social/references/platform-settings.md`.
8. If new supporting visuals are explicitly requested, use `$generate-image` with `storage: "asset"` and pass each returned `asset_id` into social `media`.
   If the user supplies a local visual, follow `$simplified-social` through
   signed upload and `api_registerAsset`, then reuse the returned UUID.
9. Wait for explicit approval before any scheduling or queueing operation.

## Transformation Patterns

- Long-form article: insight post, checklist, myth-versus-fact, quote card concept, and discussion prompt.
- Webinar or transcript: key lesson, clip concept, speaker insight, FAQ, and follow-up CTA.
- Case study or testimonial: challenge, turning point, outcome, lesson, and proof-led offer. Preserve exact attribution requirements.
- Product announcement: problem, benefit, differentiator, demonstration, objection response, and launch CTA.
- Event or promotion: announce, explain value, social proof, reminder, last call, and recap.

## Output

State what was extracted from the source, then present each channel-ready post with its angle, copy, CTA, and media suggestion. Report whether the result is copy only, saved drafts, or awaiting publishing approval.
