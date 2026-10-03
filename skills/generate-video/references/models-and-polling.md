# Video Models and Completion

## Model discovery

Use the discovery operations available in the connected client: `api_listVideoModels` and `api_getVideoModelFields`, or `api_getModelFields(type: "video")` followed by its model/capability lookup. Consult the tool schema for accepted capabilities; discovery endpoints can expose fewer modes than generation. Use the current generation schema for normalized input slots, and discovery for model support and option values.

Input slots (`image_url`, `image_urls`, `first_frame_url`, `last_frame_url`, `video_url`, and supported audio slots) take workspace asset UUIDs. Upload/import URLs first. Model availability, costs, and render time are live metadata, not fixed promises.

## Completion

Current `api_generateVideo` middleware polls the variation record and returns a terminal result. Do not call a separate polling tool while it is running. The backend submission `task_id` only tracks dispatch; it is not render completion and must not be passed to `api_getTaskResult` to check the video.

If an older deployment or timeout returns a non-terminal job with identifiers, preserve the actual values. The initial record commonly uses `id` (art) and `art_variation_id` (variation). Map these to the continuation tool's arguments:

`api_getVideoVariation(art_id: "<returned id>", variation_id: "<returned art_variation_id>")`

Use continuation only when those identifiers and the tool are available. If missing, report the pending state and preserve what was returned; do not resubmit the generation.

Read both response shapes:

- A completed variation uses `job_status: "DONE"` or `job_status: "FAILED"`.
- Middleware failure can use `error: true`, `status: "FAILED"`, and `payload` plus job identifiers; this is terminal even when `job_status` is absent.
- Middleware timeout uses `error: true`, `timed_out: true`, `status: "PENDING"`, and job identifiers; preserve them and continue the existing job where possible. This is not a terminal provider failure.

Variation statuses: `DONE` is success, `FAILED` is failure; `CREATED`, `PENDING`, `PROCESSING`, `RENDERING`, and `UPDATED` are non-terminal. Use spaced, bounded checks (for example 10–30 seconds), respecting the client's wait capability. A timeout means incomplete, not proof the provider failed.

On success, inspect `payload.output`, `output`, or `asset_references` according to the actual envelope. Identify a permanent asset UUID explicitly; art and variation IDs are not asset IDs. Preserve error details on failure.
