---
name: generate-video
description: Generate AI videos with Simplified from text, reference images, first and last frames, multiple images, or source video. Use when the user asks to create an AI video, product teaser, social clip, campaign motion asset, image-to-video animation, first/last-frame transition, or reusable generated video asset, or asks which Simplified video model supports a particular format, duration, resolution, or capability.
---

# Generate Video

Create a production-appropriate video by discovering the live model contract, generating with valid parameters, and returning a reusable result.

## Guardrails

- Video generation spends credits. Proceed when generation is explicit; confirm before spending when the user is exploring options or has not approved generation.
- Call `api_getModelFields` before generation. Never rely on a memorized model list, price, duration, aspect ratio, or parameter schema.
- Use only parameters returned for the selected model and capability.
- File-typed parameters take permanent Simplified asset UUIDs, not local paths, signed URLs, or arbitrary remote URLs.
- Use `storage: "asset"` when the video will be posted, reused, or retained. Use `transient` only for an explicitly temporary result.
- Do not treat the submission `task_id` as render completion. Follow the variation status contract in [references/models-and-polling.md](references/models-and-polling.md).
- Show returned URLs as clickable links; never embed them.

## Workflow

1. Define the job: audience, objective, placement, aspect ratio, duration, visual subject, action, camera language, pacing, brand constraints, references, audio needs, and required delivery format. Infer common social dimensions only when the requested placement makes them unambiguous.
2. Call `api_getModelFields` with `type: "video"` and no model ID to discover current choices. Shortlist by supported capability, quality, speed, estimated time, and credit cost—not model fame alone.
3. Call `api_getModelFields` again with the selected `model_id` and capability to retrieve exact required fields, enums, defaults, and file-field expectations.
4. For image-to-video, multiple-image, or first/last-frame work, ensure every reference is a permanent asset UUID. Use the Simplified signed-upload asset workflow for user-supplied local files.
5. Write a motion prompt that describes subject, action over time, environment, camera behavior, composition, lighting, pacing, and exclusions. Avoid stacking contradictory movements or scene changes into a short clip.
6. Show the chosen model, capability, duration, format, credit information when available, storage mode, and prompt before generation when cost or creative direction remains ambiguous.
7. Call `api_generateVideo` with the exact nested `parameters` contract and the chosen storage mode.
8. If the call returns before terminal completion, preserve both returned IDs and call `api_getVideoVariation` until `job_status` is `DONE` or `FAILED`. Use a reasonable interval; do not busy-loop.
9. On success, report the reusable asset UUID, rendered video link, thumbnail link when available, model, format, and any material limitations. On failure, surface the provider error and suggest one targeted correction.

## Creative Standard

- Design one clear visual beat per short clip. A six-second asset needs a readable action, not a miniature screenplay.
- Match the first frame and opening motion to the social hook; assume many viewers begin muted unless generated audio is central to the concept.
- Preserve product geometry, logos, packaging, people, and claims when references are supplied. Flag visible inconsistencies instead of presenting them as final.
- For paid or conversion creative, leave intentional visual space for on-screen copy and CTA overlays.
- Treat AI-generated people, testimonials, product behavior, and locations as synthetic; never imply documentary proof.

## Output

Lead with the creative choice and generation status. Then provide the permanent asset ID, result links, intended placement, model/capability, and next useful action such as drafting a post or producing a controlled variant.
