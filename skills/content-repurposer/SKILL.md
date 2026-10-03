---
name: content-repurposer
description: Transform one source asset into multiple channel-native social posts and a reusable content sequence. Use when the user asks to repurpose a blog post, video, transcript, webinar, newsletter, announcement, product page, testimonial, case study, podcast, or existing social post into content for LinkedIn, Instagram, Facebook, TikTok, YouTube, Threads, Bluesky, Pinterest, or Google Business.
---

# Content Repurposer

For rendered video highlights, Reels, Shorts, or source-time excerpts, use `repurpose-video`; this skill handles source-grounded channel copy. Use `transcribe-media` first when a recording needs an actual transcript or subtitle export. Never call written clip concepts completed video files.

Extract the strongest ideas from supplied source material and reshape them for the intended channels without inventing facts.

## Guardrails

- Treat the source as authoritative. Preserve names, numbers, claims, qualifications, links, and offer terms.
- Clearly label any interpretation that is not directly supported by the source.
- Return copy in conversation unless the user asks to save drafts.
- Create remote content with `action: "draft"`; require explicit approval before scheduling or queueing.
- Stop on MCP authorization failure or when required accounts are not connected.
- Present returned URLs as links, never as embedded media.

## Workspace and handoff

Before connected operations, use `simplified-workspace` when the client/workspace/teamspace is named or uncertain. Resolve the exact numeric teamspace and carry its `space_id` on every related account, analytics, asset, generation, draft, tag, review, and continuation call. Re-list scoped resources after switching clients; stop on access failures rather than falling back to another space. Pass the resolved context to every delegated skill.

## Workflow

1. Read the complete source material available to the user. If only a link is provided, retrieve it with an available browsing or connector tool before writing; do not guess its contents. If retrieval, transcription, or attachment access is unavailable, state which material was actually read and request the missing text/transcript; do not imply a complete review.
2. Build a source ledger: central thesis, useful facts, proof points, quotes that may be paraphrased, stories, objections, CTA, and prohibited or unsupported claims.
3. Identify reusable angles such as insight, checklist, contrarian point, customer proof, behind-the-scenes detail, FAQ, short tip, and offer.
4. Select an output sequence that matches the source depth. Prefer fewer distinct posts over padded variations.
5. Adapt each post to the channel's audience behavior, length, hook, CTA, and media format. Do not merely shorten the same caption.
6. Call `social_getSocialMediaAccounts` once when the user wants connected-channel drafts.
7. Show the proposed set with its source angle and intended channel. If asked to save it, call `social_createSocialMediaPost` with `action: "draft"` and the required settings from `../simplified-social/references/platform-settings.md`.
8. If new supporting visuals are explicitly requested, use `$generate-image` with `storage: "asset"` and pass each returned `asset_id` into social `media`.
   If the user supplies a local visual, follow `$simplified-social` through
   signed upload and `api_registerAsset`, then reuse the returned UUID.
9. Obtain explicit approval of the concrete final posts, accounts, timing, media, and settings before scheduling or queueing; preserve existing approval if that matrix is unchanged.

## Transformation Patterns

- Long-form article: insight post, checklist, myth-versus-fact, quote card concept, and discussion prompt.
- Webinar or transcript: key lesson, clip concept, speaker insight, FAQ, and follow-up CTA.
- Case study or testimonial: challenge, turning point, outcome, lesson, and proof-led offer. Preserve exact attribution requirements.
- Product announcement: problem, benefit, differentiator, demonstration, objection response, and launch CTA.
- Event or promotion: announce, explain value, social proof, reminder, last call, and recap.

## Media and write results

Use `manage-assets` to find existing library media before generating copies. Resolve names/tags through exposed asset discovery, preserve pagination and scope, import accessible remote files, and require ready assets before generation or attaching media. Check byte access and HTTP PUT capability before signing a local/chat attachment upload; if unavailable, ask for a Simplified asset ID or downloadable URL. Pass permanent UUIDs into drafts. A missing required visual remains a stated production gap; do not report a media-ready post without it.

For a batch of drafts, retain each successful returned ID and report created, pending, and failed items. Continue only unfinished items; do not recreate successful drafts after a later failure. A plan or test design alone does not authorize remote writes.

## Output

State what was extracted from the source, then present each channel-ready post with its angle, copy, CTA, and media suggestion. Report whether the result is copy only, saved drafts, or awaiting publishing approval.
