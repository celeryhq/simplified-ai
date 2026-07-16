---
name: cross-platform-campaign
description: Turn a launch, promotion, event, announcement, or marketing brief into a coordinated campaign of channel-native social posts. Use when the user asks to launch or promote something across multiple platforms, create a campaign sequence, coordinate social messaging, generate campaign visuals, prepare drafts, or schedule a multi-channel rollout.
---

# Cross-Platform Campaign

Build one coherent campaign while respecting how each social channel works. Compose the `generate-image` and `simplified-social` capabilities when campaign visuals are needed.

## Guardrails

- Do not publish or schedule without explicit approval of the final campaign matrix.
- Create safe previews with `action: "draft"` when the user asks to prepare the campaign.
- Image generation spends credits. Proceed when the image request is explicit; confirm first when visual generation is ambiguous.
- Carry a generated image's permanent `asset_id` into social `media`; never rely on its expiring signed URL.
- Stop on authorization failure or when no target accounts are connected.
- Present all returned URLs as clickable links, never inline images.

## Workflow

1. Distill the brief into audience, objective, offer, proof, CTA, dates, channels, tone, constraints, and success metric. State sensible assumptions instead of requesting a long questionnaire.
2. Call `social_getSocialMediaAccounts` once and map requested channels to returned account IDs.
3. Define the campaign spine: one promise, supporting proof, CTA, and a sequence such as tease, launch, proof, reminder, and last call.
4. Create channel-native variants. Change hook, length, CTA, format, and platform settings; do not paste the same caption everywhere.
5. Plan media by post. If generation is requested, follow `$generate-image`, discover the current model schema, and use `storage: "asset"` for anything that will be attached to a post.
   For a user-supplied local file, follow `$simplified-social` through signed
   upload and `api_registerAsset`, wait for `api_getAsset`, and carry the UUID.
6. Show a campaign matrix containing phase, date, account, copy, media, objective, and CTA.
7. When drafts are authorized, call `social_createSocialMediaPost` with `action: "draft"` for each post. Pass generated asset UUIDs in `media` and use `../simplified-social/references/platform-settings.md` for `additional` fields.
8. Offer a stakeholder review package via `$campaign-review` when several drafts need approval.
9. Schedule or queue only after the user explicitly approves the final matrix. `add_to_queue` means publish as soon as possible.

## Quality Bar

- Keep the promise and visual identity consistent across the campaign.
- Make each post useful on its own while advancing the sequence.
- Match media to platform format requirements; never attach an image to a reel or short that requires video.
- Do not invent product claims, prices, deadlines, testimonials, or availability.
- Surface missing landing-page URLs, legal copy, offer terms, or media before publishing.

## Output

Lead with the campaign idea and rollout. Then show the channel matrix, asset plan, drafts created, and any items blocking approval or scheduling.
