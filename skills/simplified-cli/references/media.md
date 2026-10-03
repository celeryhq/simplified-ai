# `smp media` reference

Media editing tools are separate from `api:generate-image` and `api:generate-video`. Choose the operation the user requested and inspect current help: parameters and accepted input formats differ between tools.

## Common edits

```bash
smp media:remove-background --image-url "https://example.com/product.png"
smp media:upscale-image --image-url "https://example.com/product.png" --scale 4
smp media:convert-image-format --help
smp media:generative-fill --help
smp media:image-outpainting --help
smp media:magic-inpaint --help
smp media:replace-image-background --help
smp media:merge-videos --help
smp media:convert-video-format --help
smp media:transcribe-video --help
```

Use an accessible source URL only for operations whose schema asks for one. UUID-only AI-video generation inputs follow [generate-video](../../generate-video/SKILL.md), not these editing examples. Resolve asset file URLs immediately before a URL-based edit; keep signed query strings intact.

`pix-to-pix` was removed and must not be called. For generative editing, use the current image-generation reference contract or a supported editing tool. Inpaint/outpaint masks and conditional background fields must satisfy the selected operation's schema; inspect help before building the request.

## Script/text video tools

```bash
smp media:script-to-video --help
smp media:text-to-video --help
smp media:add-b-rolls-video --help
```

These composition/editing operations are distinct from model-based `api:generate-video`. Use their actual nested `payload` fields, voice/format choices, and supported inputs. Do not route a request to animate an image to a script composition tool just because both produce videos.

## Completion and reuse

Middleware waits for many async operations, but not every endpoint has the same response shape or wait budget. Inspect the returned status and continuation contract before using output. On timeout, preserve identifiers and check the existing job; avoid duplicate credit spend.

Read the actual result envelope before using a JSON extraction path in a pipeline. Stop a chain if an earlier edit fails; never assume `result.image_url` exists universally. If an output is only a temporary URL and must be reused, import it with `api:create-asset`, retain the UUID, and check readiness. Show the file link and state whether output quality was inspected.
