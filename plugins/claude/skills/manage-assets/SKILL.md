---
name: manage-assets
description: Use when the user wants to find, list, search, upload, import, inspect, or reuse images, videos, audio, or PDFs in the Simplified Asset Library, including media for a social draft or a generation reference.
---

# Manage Simplified Assets

Find existing media before uploading another copy. Keep the permanent asset UUID for reuse; retrieve a fresh URL only when a tool or user needs it.

## Scope and tool availability

Use the connected Simplified tools, not another provider's asset library. Names here are canonical operation names; clients may add a prefix such as `mcp__simplified__`. Match the operation and its input schema in the client's available tools.

When a workspace or teamspace is named or uncertain, use `api_getWorkspaceInfo` and `api_listTeamspaces` to resolve scope. Carry the same numeric `space_id` into every asset, generation, and social call. A UUID from another workspace is not a valid reference.

Check that `api_listAssets` is exposed before promising discovery. Installing a skill does not add a missing MCP tool. If absent, refresh/reconnect the connector; if still absent, explain that its deployed profile lacks discovery and use IDs or downloadable URLs the user supplies.

## Find existing media

Call `api_listAssets`:

| Request | Arguments |
|---|---|
| Browse available media | Omit `search`; start with `page: 1` |
| Find a filename, asset name, or tag | `search: "car"` |
| Find images | `asset_type: 0` |
| Find videos | `asset_type: 2` |
| Continue results | Increment `page`, preserving search, filters, and scope |

Other numeric types include `4` giphy, `6` font, `8` audio, and `17` PDF. `page_size` requests a page size subject to server limits. Follow the returned pagination metadata; collect all pages when the user requests all matches. Deduplicate by `id` and retain the actual result names and IDs.

Search matches names and tags, not objects visible in an image. A search term includes matching media inside folders. Folder-name lookup and listing a named folder's contents are not exposed by this tool. Without search, folder contents can be excluded by the backend: do not promise a complete recursive library inventory.

For “use everything in Dynamic Auto,” explain the folder limitation and ask for an asset-name/tag search or specific IDs. Do not treat a folder name as an asset search that proves completeness.

## Inspect and reuse

Call `api_getAsset({id: "<asset UUID>"})` for details or a fresh file URL. Wait for `status: 4` before generation or relying on stored files. Stop on `2` (processing failed) or `3` (thumbnail failed); preserve the ID and report a pending state if processing remains unfinished. Use reasonable intervals and a bounded wait.

| Destination | Value to pass |
|---|---|
| Social draft `media` | Asset UUID |
| Project item `data.assets` | Asset UUID |
| Image `parameters.reference_images` | Prefer asset UUIDs; the current tool also accepts absolute HTTP(S) URLs |
| Video input slots, including `image_url` and `video_url` | Asset UUIDs, despite the `_url` suffix |
| User wants to open/download a file | Current returned URL as a clickable link |

Keep signed URL query strings intact. Stored assets have permanent IDs, but returned file/thumbnail URLs can expire. Call `api_getAsset` again to refresh them.

## Import or upload

A downloadable remote file: call `api_createAsset` with `url` and an optional `name`, save its `id`, then check readiness. A web page or login-only link is not a downloadable file. This also persists an existing temporary generated URL while it remains accessible; no regeneration is needed.

An attachment/local file: first check that this client can read the bytes and perform an HTTP PUT. If it can, follow the signed upload flow:

1. Generate a UUID and determine the original filename and MIME type.
2. Call `api_signAssetUpload` with `resource: "assets"`, `resource_id`, `filename`, and `filetype`.
3. PUT the bytes to `signed` with that MIME type and no Simplified authorization header. Keep the signed upload URL out of user-facing output.
4. Only after a successful PUT, call `api_registerAsset` with `id: resource_id`, `asset_name: filename`, and unchanged `asset_type`, `asset_key`, `asset_url`, `bucket_name`, and `thumbnail: sign.asset`.
5. Save the returned `id` and check it with `api_getAsset`.

If the client cannot read/PUT bytes, ask the user to upload in Simplified and provide the resulting ID, or supply a downloadable URL. A ChatGPT/Claude attachment is not automatically in the Simplified library. Never pass a client-local path to a hosted MCP tool or register an upload that did not happen.

## Handoff

Return the selected names, permanent IDs, readiness, and useful file links. For social work, pass the IDs to `simplified-social` and create `action: "draft"` when drafting is requested. Asset reuse or generation is not publishing authorization. For creation/editing, continue with `generate-image` or `generate-video`.
