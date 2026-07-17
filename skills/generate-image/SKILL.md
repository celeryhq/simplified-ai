---
name: generate-image
description: >-
  Generate AI images with Simplified — text-to-image, image editing, and
  reference-guided generation across Flux, Google (Gemini/Imagen), OpenAI GPT
  Image, Ideogram, Stable Diffusion, Qwen and Seedream. Use when the user asks to
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
   models, capabilities, and credit costs. Filter out models that cannot satisfy the
   requested capability; don't choose on model name alone.
2. **Choose the model** — use [Model selection](#model-selection). For the selected
   model, call `api_getModelFields(type: "image", model_id, capability)` and use its
   exact `parameters` schema. This is the source of truth; don't guess model ids,
   capabilities, field names, or costs.
3. **Choose storage** — `transient` for a one-off, `asset` to reuse the image (e.g.
   post it via the `simplified-social` skill).
4. **Explain the choice when it matters** — before a costly or ambiguous request,
   name the selected model, why it fits, and the discovered credit cost. If the user
   explicitly chose a model, honor it when it supports the requested capability.
5. **Generate** — call `api_generateImage` with `parameters` matching the discovered
   schema. This spends credits.
6. **Present the result** — show the returned URL as a link, never embedded (see
   [Presenting the result](#presenting-the-result)).

For an ordinary prompt-only request, use the quality-first default below after
confirming it is still available. Always inspect live fields for reference-image,
multi-image, exact-size, quality, or resolution requests.

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

### Resolving Simplified asset references

Treat a Simplified `asset_id` as the canonical reference, but follow the live model
schema at the generation boundary. When a model field is a URL or URL list (for
example Gemini `reference_images`):

1. Call `api_getAsset` with the permanent asset UUID.
2. Require `status: 4` (`DONE`) and the expected `asset_type` before generating.
3. Pass the current `file_url` returned by `api_getAsset` into the model-specific
   reference field. If the URL is signed, preserve its complete query string and use
   it before expiry.
4. Do not trust a cached URL copied from a brand-kit record when an `asset_id` is
   available. Brand records can contain stale or malformed derived URLs; resolve the
   ID immediately before generation instead.

In short: **IDs at rest, URLs at the model boundary, IDs downstream.** Do not pass a
client-local path to the hosted connector.

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

## Model selection

Choose for the requested outcome, not provider popularity. These routes are maintained
defaults, but model availability, capabilities, parameters, and credits can change;
`api_getModelFields(type: "image")` remains authoritative.

| User need | Preferred model | Why / tradeoff |
|---|---|---|
| Normal social image, product shot, illustration, character continuity, or general edit | `google.gemini-3.1-flash-image-preview` | **Quality-first default.** Strong all-around prompt following and reference fidelity. Do not interpret “Flash” as the cheapest option. |
| Complex professional design, dense typography/layout, menu, invitation, high-fidelity product mockup, factual visualization, or explicit 4K | `google.gemini-3-pro-image-preview` | Premium quality and instruction handling; slower and typically costs more. Use only when the request benefits from it. |
| Budget-sensitive generation or explicit GPT Image request | `openai.imgen-2` | The catalog's `credits_per_image` is a **baseline**, not the final charge. Cost varies with `size`, `quality`, and `count`. Use the live API field `quality: "auto"` (the operational “effort auto” setting) unless the user requests a different quality. It uses `size` rather than `aspect_ratio`. |
| Short headline or typography-first poster/banner | `ideogram.ideogram-v3-turbo` | Specialized text rendering. Prefer Gemini Pro when the design also requires a dense or complex professional layout. |
| Targeted edit with a single source image | `google.gemini-3.1-flash-image-preview`; `flux.flux-kontext-pro` when explicitly requested or better suited by live metadata | Default to Gemini for fidelity. Flux Kontext is a specialized alternative; inspect its `input_image` contract first. |
| Many reference images or exact reference limits | Best compatible model returned live | Filter by `multiple_images` and the discovered reference limit. Never assume every model accepts the same number or field name. |
| User names Flux, Seedream, Qwen, Stable Diffusion, or another available model | The requested model, if compatible | Respect an explicit preference. Otherwise do not automatically route to an unvalidated specialist merely because it is available or cheaper. |

### Routing rules

1. Infer the hard constraints: capability, reference count, aspect ratio/size,
   resolution, text/layout complexity, budget, and any explicit provider choice.
2. Filter the live catalog by those constraints.
3. Use Gemini 3.1 Flash when no stronger constraint applies. Upgrade to Gemini 3 Pro
   only for the professional-design cases above. Consider GPT Image 2 when minimizing
   credits is explicit or as the first fallback, but state that its live catalog rate
   is only a baseline and the final charge varies with `size`, `quality`, and `count`.
   Default to `size: "auto"`, `quality: "auto"`, and `count: 1` unless the request
   requires different values.
4. For a typography-first graphic, choose Ideogram Turbo; for dense layout or 4K,
   choose Gemini Pro instead.
5. Never silently change models after an error. Report the failure and proposed
   fallback with its live credit cost, then regenerate only when the user's existing
   intent clearly authorizes the additional spend.

When a request is ambiguous and the choice materially changes cost or output, offer
the most relevant two choices, leading with the recommended model. Do not dump the
entire catalog on the user.

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

Output format varies by model and provider. Inspect the returned asset or response
metadata instead of assuming WebP; for example, Gemini may return JPEG.

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
  and `parameters` schema — it eliminates 400 errors on invalid/missing keys and
  prevents routing from stale model or credit assumptions.
- **Resolve asset-backed references before generating.** Use `api_getAsset`, require
  `status: 4`, and pass its current `file_url` when the live model field expects a
  URL. Keep the source `asset_id` for future runs.
- **Generation spends credits.** If the request is ambiguous, restate what you'll
  generate and confirm once. If it's explicit, proceed.
- **Do not overstate GPT Image 2 pricing.** Treat `credits_per_image` as baseline
  metadata. Final usage varies with `size`, `quality`, and `count`. The live API calls
  the effort control `quality`; use `quality: "auto"` for the usual “effort auto”
  behavior and never describe the baseline as the guaranteed charge.
- `429` = AI credits exhausted; tell the user plainly and don't retry.
- On error, report it; don't silently retry.

## Example prompts to try

- "A minimalist product photo of a white ceramic coffee cup on a clean white background, soft studio lighting"
- "A vibrant 3D render of a friendly robot mascot, pastel colors, studio lighting, 1:1"
- "A cinematic 16:9 landscape of snowy mountains at golden hour"
- "A flat vector app icon of a paper plane, rounded corners, blue gradient"
- "A bold quote card that says 'Ship it' in modern type" (use `ideogram.ideogram-v3-turbo` for crisp text)
