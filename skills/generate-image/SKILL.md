---
name: generate-image
description: Use when the user asks to create, generate, draw, design, or edit an image with Simplified, including product photos, social graphics, logos, posters, banners, illustrations, or compositions guided by one or more reference images.
---

# Generate Image

Create or edit an image with Simplified and retain an asset ID when the result will be reused. Use the current generation tool schema as the request contract; model catalogs describe availability and limits, not a reason to substitute provider-specific field names.

## Workflow

1. Resolve workspace/teamspace scope when needed using `simplified-workspace`. Carry its `space_id` into related calls.
2. Resolve existing references with `manage-assets`: search names/tags with `api_listAssets` if available, or use supplied IDs/URLs. Check asset readiness with `api_getAsset` before generating.
3. Select a compatible model from `api_listImageModels`, or `api_getModelFields(type: "image")` if that is the discovery tool exposed in this client. Inspect `api_getImageModelFields` or the available model-fields tool for limits/options when the request requires a particular resolution, quality, reference count, or provider. Honor explicit model choices when supported. Model IDs and credit costs can change; do not guess them.
4. Build the nested request below. Use `storage: "asset"` for reusable outputs; use `transient` only for an explicitly temporary result. The current schema recommends/defaults to asset storage; pass the choice explicitly.
5. Call `api_generateImage` when the user requests generation. Generation spends credits: clarify once when cost, quantity, or intent is ambiguous. Do not add a confirmation when the user already authorized that generation.
6. Wait for the tool's response, inspect its actual status, and report the result. Current apikit waits for completion; do not start a second job or manually poll while the call is still active.

## Current request contract

```json
{
  "model": "<model ID returned by discovery>",
  "storage": "asset",
  "parameters": {
    "prompt": "A studio product photo with space for a headline",
    "aspect_ratio": "4:5",
    "count": 1
  }
}
```

This is a template: substitute a discovered model ID before calling it. `model`, `storage`, and `parameters` are top-level. `prompt`, `aspect_ratio`, `count`, and `reference_images` belong inside `parameters`.

For editing, add `parameters.reference_images: ["<ready asset UUID>"]`. For composition, supply several references in that array; supported counts depend on the model. Prefer workspace asset UUIDs. The image tool also accepts absolute HTTP(S) image URLs; preserve the full signed query string if using one. Local paths, filenames, and another workspace's UUIDs are invalid.

`capability` is optional: no references selects `prompt`, one selects `reference_image`, and several select `multiple_images`. Several references compose one output; use `count` for several generated outputs. If setting a capability explicitly, confirm the model supports it.

Use the normalized public field `reference_images` for every model. Do not replace it with provider fields such as `input_image` or `source_image`, even if a catalog describes internal provider fields. Add optional model-specific controls only when the generation schema/live contract accepts them.

## Choose for the outcome

For ordinary social graphics, select a currently available general model; for dense text/layout or higher resolution, inspect compatible models and limits. For continuity/editing, filter by reference support. When the user specifies a provider, use that family's currently recommended compatible ID. For a budget-sensitive request, inspect available credit metadata and generate only the requested count. Treat credit rates as estimates unless the tool explicitly guarantees the charge; size, quality, and count can affect usage.

## Storage and results

| Mode | Use |
|---|---|
| `asset` | Save in the Asset Library and retain a reusable UUID |
| `transient` | Temporary output URL without a permanent asset ID |
| `default` | Save in the image gallery; do not assume this supplies an Asset Library UUID |

Read the returned envelope rather than assuming all clients return identical wrappers. Common successful image results are in `detail.result`; entries can be URL strings (transient) or objects containing `asset_id` and `url` (asset). Keep every returned output when generating multiple images.

Show the result as a clickable link and include the permanent `asset_id` when present. Signed file URLs may expire even for saved assets. Refresh them with `api_getAsset`. If the user later wants to reuse a transient image, import its accessible URL with `api_createAsset` instead of generating again.

For social drafts, hand off actual IDs to `simplified-social.media`; generation is not permission to publish.

## Errors and incomplete jobs

An accepted request is not proof of a finished image. On timeout/pending status, retain the returned job identifiers and use only the continuation operation the response/tool schema specifies. Never blindly repeat a paid generation. Report provider errors and use the supported-value list for a targeted correction. A 429 may indicate quota or rate limits: report its actual message rather than assuming credits are always exhausted.

Examples users can ask: “Make a vertical product photo and save it”; “Find my uploaded logo and use it in a poster”; “Edit this asset to use a blue background”; “Create three variations for review.”
