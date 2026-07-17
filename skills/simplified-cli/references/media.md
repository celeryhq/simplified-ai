# `smp media` — Image & Video AI Tools Reference

AI-powered image and video processing: background removal, upscaling,
generative fill, outpainting, inpainting, format conversion, video merging,
B-roll insertion, text-to-video, script-to-video.

## Async Tasks

**Almost all media tools are asynchronous.** They return `{"task_id": "..."}`
and the toolkit middleware automatically polls `GET /api/v1/tasks/{task_id}`
until status is `SUCCESS` or `FAILURE`. You get the final result back in one
call — no manual polling.

Default polling: 15 retries × 15 seconds (~3.75 minutes). Video generation
(`text-to-video`, `script-to-video`, `add-b-rolls-video`) may exceed this — if
a task times out, the response includes the `task_id` to poll manually.

**Exception:** `blur-background` is synchronous (returns `image_url` directly).

## Image Tools

### Background removal

```bash
smp media remove-background --image-url "https://..."

# With options
smp media remove-background \
  --image-url "https://..." \
  --magic-crop true \
  --background-color "#ffffff" \
  --output-format png            # png (default, transparent) | jpeg
```

### Blur background (synchronous)

```bash
smp media blur-background --image-url "https://..." --blur-value 50   # 1-100
```

### Upscale

```bash
smp media upscale-image --image-url "https://..." --scale 4   # 2 | 4 | 8 (default 2)
```

### Restore / enhance quality

```bash
smp media restore-image --image-url "https://..." --scale 1
```

### Generative fill (prompt-guided inpaint)

Provide either `--mask-url` or `--mask-base64`. Mask = white where to fill.

```bash
smp media generative-fill \
  --image-url "https://..." \
  --mask-url "https://.../mask.png" \
  --prompt "a sunset over mountains" \
  --negative-prompt "blurry, low quality" \
  --count 4
```

### Outpainting (extend image beyond borders)

```bash
smp media image-outpainting \
  --image-url "https://..." \
  --mask-url "https://.../mask.png" \
  --prompt "ocean horizon at sunset" \
  --guidance-scale 7.5 \
  --count 4
```

### Magic inpaint (object removal/replacement)

```bash
smp media magic-inpaint \
  --image-url "https://..." \
  --prompt "remove the person, keep the background"
```

### Pix-to-pix (instruction-based transform)

```bash
smp media pix-to-pix \
  --image-url "https://..." \
  --prompt "make it winter" \
  --image-guidance-scale 1 \
  --counts 4
```

### Replace background

```bash
# replace-type: transparent | color | image
smp media replace-image-background \
  --image-url "https://..." \
  --replace-type color \
  --replace-color "#000000"

smp media replace-image-background \
  --image-url "https://..." \
  --replace-type image \
  --replace-image "https://.../bg.jpg"
```

### Scribble to image (ControlNet)

```bash
smp media sd-scribble \
  --prompt "a cat in space, oil painting" \
  --negative-prompt "blurry, low quality" \
  --image-url "https://.../scribble.png" \
  --counts 4
```

## Video Tools

All video endpoints are async — middleware polls automatically.

### Format conversion

```bash
# output-format: mp4, avi, mkv, mov, wmv, flv, webm, mpeg, mpg, 3gp, ogv,
#                ts, vob, m4v, f4v, rm, divx, asf
smp media convert-video-format --video-url "https://..." --output-format mp4
```

### Merge videos

```bash
smp media merge-videos --video-urls '["https://a.mp4", "https://b.mp4"]'   # min 2
```

### Remove audio track

```bash
smp media remove-audio --video-url "https://..."
```

### Reverse video

```bash
smp media reverse-video --video-url "https://..."
```

### Change playback speed

```bash
smp media speedup-video \
  --video-url "https://..." \
  --playbackrate 2.0          # min 0.5; 2.0 = double speed, 0.5 = half
```

### Auto-add B-roll

```bash
smp media add-b-rolls-video \
  --title "How AI is changing marketing" \
  --media-url "https://..." \
  --language-code en \
  --should-export true

# Or with an existing asset
smp media add-b-rolls-video --title "..." --asset <asset_id>
```

### Script to video

```bash
smp media script-to-video \
  --payload '{
    "title": "Why Python wins",
    "description": "A 60s explainer on Python adoption",
    "tone": "educational",
    "language_code": "en",
    "format": "youtube-shorts",
    "voice_id": "<voice_uuid>",
    "no_runs": 1
  }' \
  --should-export true
```

### Text to video

```bash
smp media text-to-video \
  --payload '{
    "title": "Sunset timelapse over the ocean",
    "tone": "calm",
    "format": "instagram-post-video"
  }' \
  --should-export true
```

## Enum Reference

**VideoTone:** `professional`, `casual`, `humorous`, `inspirational`,
`educational`, `dramatic`, `energetic`, `calm`, `friendly`, `authoritative`,
`storytelling`, `persuasive`

**VideoFormat (output aspect):** `youtube-shorts`, `youtube-video`,
`instagram-post-video`, `mp4`

**VideoOutputFormat (convert):** `mp4`, `avi`, `mkv`, `mov`, `wmv`, `flv`,
`webm`, `mpeg`, `mpg`, `3gp`, `ogv`, `ts`, `vob`, `m4v`, `f4v`, `rm`, `divx`,
`asf`

**ImageOutputFormat (remove-background):** `png` (default), `jpeg`

**Replace types (replace-image-background):** `transparent`, `color`, `image`

## Critical Gotchas

**JSON args need single quotes** — `--video-urls '["..."]'`,
`--payload '{"...":"..."}'`.

**`merge-videos` requires ≥2 URLs.** Single URL → 400.

**`replace-image-background` requires the corresponding field:**
- `--replace-type color` → must pass `--replace-color`
- `--replace-type image` → must pass `--replace-image`
- `--replace-type transparent` → neither needed

**`generative-fill` and `image-outpainting`** require a `mask_url` or
`mask_base64`. White in the mask = the region to fill/extend.

**`script-to-video` / `text-to-video` wrap their fields inside `payload`** — not
flat. Use `--payload '{"title":"...", ...}'`, not `--title ...`.

**Video generation can be slow.** `script-to-video` / `text-to-video` /
`add-b-rolls-video` may exceed the default ~3.75 min polling window. On
timeout, the response includes the `task_id` for manual polling.

**`blur-background` is the only synchronous endpoint** — returns
`{"image_url": "..."}` directly. All others are async.

## Composite Workflow Example

Remove background → upscale → overlay on new background:

```bash
# 1. Remove background → transparent PNG
SUBJECT_URL=$(smp --raw media remove-background \
  --image-url "https://input.jpg" --output-format png | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['result']['image_url'])")

# 2. Upscale the cutout 4×
UPSCALED_URL=$(smp --raw media upscale-image \
  --image-url "$SUBJECT_URL" --scale 4 | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['result']['image_url'])")

# 3. Composite onto a new background
smp media replace-image-background \
  --image-url "$UPSCALED_URL" \
  --replace-type image \
  --replace-image "https://background.jpg"
```

## Discovering Commands

```bash
smp media --help
smp media <command> --help
```
