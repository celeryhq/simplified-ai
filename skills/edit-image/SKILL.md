---
name: edit-image
description: Use when the user wants to remove, blur, or replace an image background, remove an object, fill a masked region, extend a canvas, restore a photo, upscale, or convert an existing image in Simplified. For a new image or broad reference-guided transformation, use generate-image.
---

# Edit an existing image

Choose the smallest supported operation that achieves the requested edit. Preserve the source and create a new result; do not regenerate the product or change approved copy to solve a file-processing task.

## Resolve the source and scope

Use the connected Simplified tools and their current schemas. Canonical names below may have a client prefix. A missing tool is a capability limit, not a reason to silently switch providers.

For a named or uncertain workspace/teamspace, resolve it with `api_getWorkspaceInfo` and accessible membership from `api_listTeamspaces`. Carry the numeric `space_id` on every related call. Use `manage-assets` to search names/tags or handle intake; a folder name does not establish its contents.

For an asset UUID, call `api_getAsset`, require ready `status: 4`, and use its fresh full file URL. The image editing tools below take `image_url`, not an asset UUID or a client-local path. An attachment must first be made accessible using a supported import/upload flow. Preserve signed URL query strings and refresh expired source URLs.

## Choose the operation

| Requested change | Operation and inputs |
|---|---|
| Transparent cutout | `media_removeBackground`: `image_url`, `output_format: "png"`; omit `background_color`; avoid `magic_crop: true` when framing must remain |
| Background blur | `media_blurBackground`: `image_url`, required `blur_value` from 1–100 |
| Background color/image/transparency | `media_replaceImageBackground`: `replace_type`; color needs `replace_color`, image needs `replace_image` URL |
| Resolution | `media_upscaleImage`: `scale` 2, 4, or 8, according to request |
| Denoising/artifact repair | `media_restoreImage`; use its supported strength fields |
| Specific masked region | `media_generativeFill`: prompt and `mask_url` or `mask_base64`; white marks the fill area |
| Object described in words, no mask | `media_magicInpaint`: prompt describing removal/replacement |
| Extend beyond existing borders | `media_imageOutpainting`: prompt and required `mask_url` defining the extension |
| File format only | `media_convertImageFormat`: current format field and supported value |

For an exact-region request without a mask, obtain or create a usable mask only if the client can do so accurately. Semantic inpainting is an alternative only when the user accepts model-selected boundaries. Neither a prompt nor a mask guarantees pixel-perfect preservation: verify the result, and do not promise unchanged pixels outside a region without comparison.

Use PNG for transparency; JPEG cannot retain alpha. Do not promise that later upscaling or conversion retains transparency or source framing without inspecting it. If visual inspection is unavailable, report that limit. Masked generation can default to multiple variations: set `count: 1` unless more were requested. Explicit edits authorize the requested work; clarify materially ambiguous changes or added variants before spending credits.

## Complete each step before chaining

`media_blurBackground` can return an `image_url` synchronously. Other tools may be async at the backend while middleware waits for completion. Inspect the actual completed output; a `task_id` alone is not an image.

For a pending/timeout envelope, retain the exact task ID and call `api_getTaskResult` where exposed. Poll with reasonable intervals and a bounded wait. `SUCCESS` requires usable output; `FAILURE` or `REVOKED` stops the chain. A timeout with `error: true` is incomplete, not proof of terminal failure. Do not resubmit the paid edit or run the next step on the original as if the previous edit succeeded. If no continuation tool is exposed, report the saved task ID and unfinished steps.

For remove-background → upscale, the upscale input is the completed cutout URL. For a batch, preserve successes and report each failure; retry only unresolved work when its state and authorization are clear.

## Save and hand off

If the edit returns a verified permanent asset UUID, reuse it rather than importing a duplicate. If it returns only a usable temporary URL and the result should be retained, call `api_createAsset` with that URL and a useful name, then `api_getAsset` until ready. Never regenerate just to obtain storage. The original asset remains separate.

Return the edit performed, actual result link, verified asset UUID/readiness, and any unverified transparency/framing detail. Show links in the form supported by the client. For requested social drafts, pass the ready result UUID to `simplified-social` with `action: "draft"`; editing does not authorize publication.
