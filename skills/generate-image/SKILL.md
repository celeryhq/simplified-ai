---
name: generate-image
description: >-
  Generate AI images with Simplified — text-to-image, image editing, and
  reference-guided generation across Flux, Google (Gemini/Imagen), OpenAI GPT
  Image, Ideogram, Stable Diffusion, Qwen and SeeDream. Use when the user asks to
  create, generate, make, draw, or design an image, photo, picture, graphic,
  logo, poster, banner, icon, or illustration from a description.
---

# Generate AI Image

Generate an image from a text prompt using Simplified, across many leading AI
providers, and return a viewable image URL (plus an asset id you can reuse).

## What it can do

- **Text-to-image** (`capability: "prompt"`) — make an image from a description.
- **Image editing / image-to-image** (`capability: "reference_image"`) — transform
  or edit using one reference image.
- **Multi-reference composition** (`capability: "multiple_images"`) — guide with
  several reference images (supported on some models).

Good for: product shots, hero/banner images, social graphics, illustrations,
3D-style renders, icons/logo concepts, photoreal scenes, and **text rendered inside
the image** (posters, quote cards, ad headlines).

## How to use it

1. **Discover** — call `api_getModelFields(type: "image")` to get the current list of
   models (with credit costs) and, for the model you choose, the exact `parameters`
   schema. This is the source of truth; don't guess model ids or field names.
2. **Choose a capability** — `prompt`, `reference_image`, or `multiple_images`.
3. **Choose storage** — `transient` for a one-off, `asset` to reuse the image (e.g.
   post it via the `simplified-social` skill).
4. **Generate** — call `api_generateImage` with `parameters` matching the discovered
   schema. This spends credits.
5. **Present the result** — show the returned URL as a link, never embedded (see
   [Presenting the result](#presenting-the-result)).

For a quick default request you may skip step 1 and use a quick-pick model below —
but call `api_getModelFields` whenever the user names a specific model, uses a
reference image, or you're unsure of a field.

## The request

### The tools

- **`api_getModelFields`** — discover available models and the per-(model, capability)
  field schema. Read-only, spends **no credits**. Call it first.
- **`api_generateImage`** — **consumes paid AI credits**.

### Fields

Top-level fields for `api_generateImage`:

- `model` — a model id from `api_getModelFields` (e.g. `google.gemini-3.1-flash-image-preview`).
- `capability` — `prompt` | `reference_image` | `multiple_images`.
- `storage` — see [Storage](#storage) (default `transient`).
- `parameters` — a **required nested object**; never flatten its fields to the top
  level, and put the prompt text in `parameters.prompt` (not in `capability`).

The **exact keys inside `parameters` vary by model** — get them from
`api_getModelFields(type: "image", model_id, capability)`, don't assume. They differ
in real ways: most models take `aspect_ratio`, but OpenAI GPT Image uses `size` +
`quality` + `count`, Gemini adds `image_size`, Flux 2 uses `resolution`, and the
reference-image field is variously named `input_image`, `image_prompt`,
`reference_images`, `source_image`, or `style_reference_images`.

### Storage

| `storage` | Behavior |
|---|---|
| `transient` | **Default.** Temporary URL, not saved, expires. Best for one-off images. |
| `asset` | Persistent — no expiry, returns an `asset_id`. Use when you want to **reuse** the image, e.g. attach it to a post via the `simplified-social` skill (pass the `asset_id` in `media`). |
| `default` | Saved to your AiImageArt gallery. |

### Examples

**Text-to-image (default, transient):**
```json
{ "model": "google.gemini-3.1-flash-image-preview", "capability": "prompt", "storage": "transient",
  "parameters": { "prompt": "A white ceramic coffee cup on a clean white background", "aspect_ratio": "1:1" } }
```

**Keep it to reuse / post to social (asset):**
```json
{ "model": "google.gemini-3.1-flash-image-preview", "capability": "prompt", "storage": "asset",
  "parameters": { "prompt": "product hero shot of sneakers", "aspect_ratio": "4:5" } }
```

**Edit / reference-guided** — the reference field name is model-specific; take it from
`api_getModelFields` (here `input_image` for a Flux Kontext model, not a guessed name):
```json
{ "model": "flux.flux-kontext-pro", "capability": "reference_image", "storage": "asset",
  "parameters": { "prompt": "put this logo on a t-shirt", "input_image": "<asset_uuid_or_https_url>" } }
```

## Models (quick pick)

Reasonable starting points (ids and credits change — `api_getModelFields(type: "image")`
is authoritative):

- **balanced** — `google.gemini-3.1-flash-image-preview`
- **cheapest** — `openai.imgen-2` (GPT Image 2)
- **text-in-image** — `ideogram.ideogram-v3-turbo`
- **highest quality** — `google.gemini-3-pro-image-preview`

## Response

The response shape depends on `storage`:

- **`transient` (default)** — `result` is a list of **URL strings**:
  ```json
  { "status": "SUCCESS", "detail": { "result": ["https://replicate.delivery/…/out-0.webp"], "transient": true } }
  ```
  Read `detail.result[0]` (a URL string). No `asset_id` — the URL is temporary.

- **`asset`** — `result` is a list of **objects** with a reusable id:
  ```json
  { "status": "SUCCESS", "detail": { "result": [{ "asset_id": "<uuid>", "url": "https://…/image.webp?Expires=…" }], "transient": false, "storage": "asset" } }
  ```
  Read `detail.result[0].url` (the image; **signed URL — expires**) and
  `detail.result[0].asset_id` (permanent — hand off to `simplified-social`'s `media`).

Output is WebP either way.

## Presenting the result

**Never embed the returned image URL with Markdown image syntax** (`![](url)`), and
never do anything that makes the client fetch/render the image inline. Always present
the result as a **plain URL or a Markdown link** the user can click:

- ✅ `Here's your image: https://…/out-0.webp`
- ✅ `[View generated image](https://…/out-0.webp)`
- ❌ `![generated image](https://…/out-0.webp)`

Reasons: these URLs are signed and **expire**, inline rendering fails or shows a
broken image, and clients like Codex otherwise try to display the asset instead of
handing the user a usable link — poor UX. When `storage:"asset"`, also surface the
permanent `asset_id` (as text) so it can be reused with `simplified-social`.

## Gotchas

- **Discover before generating.** Call `api_getModelFields` to confirm the model id
  and `parameters` schema — it eliminates 400 errors on invalid/missing keys.
- **Generation spends credits.** If the request is ambiguous, restate what you'll
  generate and confirm once. If it's explicit, proceed.
- `429` = AI credits exhausted; tell the user plainly and don't retry.
- On error, report it; don't silently retry.

## Example prompts to try

- "A minimalist product photo of a white ceramic coffee cup on a clean white background, soft studio lighting"
- "A vibrant 3D render of a friendly robot mascot, pastel colors, studio lighting, 1:1"
- "A cinematic 16:9 landscape of snowy mountains at golden hour"
- "A flat vector app icon of a paper plane, rounded corners, blue gradient"
- "A bold quote card that says 'Ship it' in modern type" (use `ideogram.ideogram-v3-turbo` for crisp text)
