---
name: generate-video
description: Use when the user asks Simplified to generate an AI video, animate an image, create a product teaser, guide motion with several images, make a first/last-frame transition, transform a source video, or check supported video models, duration, resolution, or audio options.
---

# Generate Video

Create one clear motion asset using a compatible model, ready workspace references, and the current tool's nested parameters.

## Workflow

1. Resolve scope with `simplified-workspace` when a workspace/teamspace is named or uncertain. Carry `space_id` into every related call.
2. Define the subject, action, placement, aspect ratio, duration, camera behavior, and audio needs. Infer ordinary choices from the user's brief; ask only for missing constraints that change the result or cost.
3. Discover current models with `api_listVideoModels` or `api_getModelFields(type: "video")`, depending on the exposed tools. Inspect `api_getVideoModelFields` or the available model-fields tool for model-specific durations, resolutions, and capabilities. Do not guess model IDs, costs, or supported values.
4. Use `manage-assets` to find/import/upload references and check readiness with `api_getAsset`. Every video input slot takes a Simplified asset UUID from the same workspace, not a local path or remote URL.
5. Choose `storage: "asset"` for a reusable video. Generation spends credits; proceed for an explicit request, and clarify material ambiguity in scope/cost before submitting.
6. Call `api_generateVideo` once. Current apikit waits for the rendered result; wait for this call before using any continuation tool.
7. Inspect the actual terminal status and return the rendered video link plus its real asset ID when present. Handle pending/timeout/older deployments as described in [references/models-and-polling.md](references/models-and-polling.md).

## Current input contract

Top-level: `model`, `parameters`, and chosen `storage`; optional `capability` and `space_id`. All generation controls belong inside `parameters`.

| Mode | Nested input |
|---|---|
| Text-to-video | `prompt` |
| Animate one image | `image_url: "<asset UUID>"` and optional motion prompt |
| Multiple image guidance | `image_urls: ["<asset UUID>", "<asset UUID>"]` |
| First/last-frame transition | `first_frame_url` and `last_frame_url`, both asset UUIDs |
| Source video transformation | `video_url: "<video asset UUID>"` |
| Supported lipsync/audio modes | `audio_url` or `reference_audio_urls`, containing audio asset UUIDs |

Despite `_url` in the names, these slots take **asset UUIDs**. Use the same public slot names across models. Choose only controls the selected model supports, such as `duration`, `resolution`, `aspect_ratio`, or `generate_audio`. Image-driven modes may derive their ratio from the reference; do not force an unsupported ratio. Omit `capability` to let the current tool infer it from inputs, or use an explicitly supported mode.

```json
{
  "model": "<discovered image-to-video model ID>",
  "storage": "asset",
  "parameters": {
    "image_url": "<ready image asset UUID>",
    "prompt": "A slow push toward the product, soft light moving across its packaging"
  }
}
```

Replace placeholders before calling. Do not assume every model supports every slot, duration, or audio option.

## Creative quality

Use one readable visual beat for a short clip. Preserve product geometry, packaging, logos, and identity in references; avoid contradictory camera moves. Leave space for overlays when needed. If the client can inspect the output, check it; otherwise state that visual quality has not been inspected. Synthetic people/scenes are not documentary evidence.

## Handoff

Use a clickable video link; preserve any thumbnail link and permanent asset UUID. Signed URLs can expire. `default` gallery storage is not a guarantee of a standalone reusable asset; `transient` may supply only a temporary URL. If no asset ID exists and the user wants reuse, import the downloadable output using `api_createAsset`. Never invent an asset ID from an art or variation ID.

Pass confirmed assets to `simplified-social` for drafts when requested. Generating a video does not authorize publishing. Report failures directly and avoid duplicate paid submissions after a timeout.
