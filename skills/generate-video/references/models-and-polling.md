# Video Models and Polling

## Model discovery

Use `api_getModelFields` in two passes:

1. `{type: "video"}` lists current engines, capabilities, estimated time, and credit metadata.
2. `{type: "video", model_id: "<id>", capability: "<capability>"}` returns the exact field descriptors.

Supported capability labels may include `prompt`, `reference_image`, `multiple_images`, `first_last_frame`, and `video_to_video`. Availability is model-specific.

Build `api_generateVideo.parameters` only from the returned field descriptors. Common names such as `prompt`, `duration`, `aspect_ratio`, `resolution`, `image_url`, `image_urls`, `first_frame_url`, `last_frame_url`, `video_url`, and `generate_audio` are examples, not a stable universal schema.

File fields accept Simplified asset UUIDs. Import or upload the source first and wait until the asset is ready.

## Completion

`api_generateVideo` returns an art ID and variation ID. Preserve both.

If generation is not already terminal, call:

- `api_getVideoVariation(art_id=<art id>, variation_id=<variation id>)`

Interpret `job_status` as follows:

- Continue: `CREATED`, `PENDING`, `PROCESSING`, `RENDERING`, `UPDATED`
- Success: `DONE`
- Failure: `FAILED`

Poll approximately every 10 seconds and allow long-form providers adequate time. Do not use `api_getTaskResult` for video completion: its submission task may finish before the provider render.

On success, resolve the rendered file and reusable asset from `payload.output`, `output`, or `asset_references` according to the returned envelope. Do not invent an asset ID if only a transient URL exists.
