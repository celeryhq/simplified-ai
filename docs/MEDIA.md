# Use assets, images, and videos

Connect Simplified first using [your client's setup](CLIENTS.md). Start with existing media when you have it; generate only when you need new content.

## Find uploaded images

Ask: “Find images with ‘car’ in their name or tags and create drafts using the matches.”

The assistant calls `api_listAssets` with `search: "car"`, `asset_type: 0`, and `page: 1`, carrying `space_id` when a teamspace was selected. It continues pagination when you ask for all matches, checks media readiness, and uses returned `id` values in drafts.

Search matches names and tags, not visual contents or folder names. Searching “Dynamic Auto” does not mean “everything in the Dynamic Auto folder.” Named-folder contents are not exposed by the current tool. Listing without search can omit folder contents; the assistant must not claim it found your complete recursive library.

If discovery is missing from your connector, refresh/reconnect. Until it is deployed in that profile, provide IDs or downloadable media URLs.

## Bring in a file

A downloadable URL can be imported with `api_createAsset`. Keep the returned asset UUID and wait until `api_getAsset` reports `status: 4`.

A local file or chat attachment needs a real upload: sign, transfer bytes directly to storage, then register. The assistant can do this only if its client can read the file and perform the HTTP PUT. If not, upload in Simplified yourself and provide the resulting UUID. An attachment name is not an asset ID and cannot be sent to the hosted connector as a local path.

## Create an image

Ask: “Create a vertical product photo and save it for reuse.”

The assistant chooses a currently compatible model and sends `api_generateImage` with `storage: "asset"` and nested `parameters`. For example, `prompt`, `aspect_ratio: "4:5"`, and `count: 1` belong inside `parameters`.

To edit/reuse an existing image, ask: “Use this asset ID as the reference and change the background to blue.” The current image tool takes `parameters.reference_images` containing workspace asset UUIDs or HTTP(S) URLs. Several references guide one composition; `count` controls the number of outputs.

Generation spends credits. A clear generation request authorizes that job; exploring model choices does not. The assistant should clarify changes that materially affect cost, quantity, or direction.

## Create a video

Ask: “Animate this product image with a slow camera push and save the video.”

The assistant checks the selected model's capabilities and uses a ready image asset UUID in `parameters.image_url`. Video slots require IDs despite their names: `image_url`, `image_urls`, `first_frame_url`, `last_frame_url`, `video_url`, and supported audio inputs do not accept arbitrary URLs. Remote references must be imported first.

Current generation tools wait for completion. A pending/timeout response does not mean the video is ready or that it should be generated again. The assistant retains returned job identifiers and continues the existing variation where supported. A submission task ID alone cannot establish video render completion.

## Save and reuse the result

| Storage | What to expect |
|---|---|
| `asset` | A saved Asset Library item and reusable UUID when creation succeeds |
| `transient` | Temporary file URL; no guaranteed asset UUID |
| `default` | Gallery entry; do not assume it is a standalone asset |

An asset ID is permanent; a returned signed file URL can expire. Retrieve the asset again for a fresh link. To reuse an already generated temporary image/video, import the URL while it is accessible rather than generating another copy.

For social work, pass the real asset UUID into `media` and create a draft. Show the draft before publishing; request explicit scheduling/queueing authorization. Generation alone does not grant it.

## What a useful result includes

The assistant should return the status, file link, asset UUID when present, and a clear pending/failure explanation when unfinished. It should state whether it could inspect the output, rather than claim visual quality from a URL alone. Never report a saved asset, completed upload, or complete folder selection without evidence from the tools.
