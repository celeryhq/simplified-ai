# Attached Media and Assets

Use this workflow when a user supplies a local image, video, audio file, or PDF
that must become persistent Simplified media.

## Ingest an attachment

1. Determine the original filename and MIME type, and create a UUID for the asset.
2. Call `api_signAssetUpload` with `filename`, `filetype`, `resource: "assets"`,
   and `resource_id: "<uuid>"`.
3. From the MCP client, PUT the local file bytes directly to the returned `signed`
   URL with `Content-Type` set to the same MIME type. Do not send Simplified auth.
4. After a successful PUT, call `api_registerAsset` with:
   - `id`: the original `resource_id`.
   - `asset_type`, `asset_key`, `asset_url`, `thumbnail` (the sign response's
     `asset` field), and `bucket_name`: carry unchanged from the sign response.
   - `asset_name`: original filename.
   - `payload.title`: optional human-readable title.
5. Capture the returned `id` as the permanent asset UUID.
6. Poll `api_getAsset({id: "<uuid>"})` until `status=4` before scheduling or
   publishing. Stop and report any explicit failure state.
7. Pass the exact UUID into `social_createSocialMediaPost.media`.

```text
api_signAssetUpload({
  filename: "campaign.png",
  filetype: "image/png",
  resource: "assets",
  resource_id: "a1b2c3..."
}) -> {signed, asset, asset_url, asset_key, asset_type, bucket_name}

PUT campaign.png bytes directly to signed with Content-Type: image/png

api_registerAsset({
  id: "a1b2c3...",
  asset_type: "<sign.asset_type>",
  asset_key: "<sign.asset_key>",
  asset_name: "campaign.png",
  asset_url: "<sign.asset_url>",
  thumbnail: "<sign.asset>",
  bucket_name: "<sign.bucket_name>",
  payload: {title: "Campaign"}
}) -> {id: "a1b2c3..."}

api_getAsset({id: "a1b2c3..."}) -> poll until status=4

social_createSocialMediaPost({
  message: "Campaign day is here.",
  account_ids: [123],
  action: "draft",
  media: ["a1b2c3..."],
  additional: {
    instagram: {
      postType: {value: "post"},
      channel: {value: "direct"}
    }
  }
})
```

## Import a public URL

Call `api_createAsset` with `url` when the media already has a permanent public
URL. Do not download and upload it unnecessarily.

## Safety and failure handling

- Never pass a client-local `path` to the hosted connector; it would refer to the
  remote server's filesystem.
- Treat `signed` as a temporary secret: never print, summarize, or present it to
  the user.
- Never attach the Simplified OAuth/API authorization header to the storage PUT.
- Do not call `api_registerAsset` until the direct PUT succeeds.
- Do not create a social post if upload, registration, or processing fails.
- Asset creation is not publishing authorization. Continue to require explicit
  approval before `schedule` or `add_to_queue`.
