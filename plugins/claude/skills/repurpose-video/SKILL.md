---
name: repurpose-video
description: Use when the user wants to turn a webinar, interview, podcast, recording, or long video into rendered short clips, Reels, Shorts, or social draft videos in Simplified, or wants a custom source-time excerpt from an existing repurposing project.
---

# Turn recordings into ready short clips

Produce playable clips and preserve source context. For rewritten posts or clip concepts, use `content-repurposer`; for a standalone transcript or subtitles, use `transcribe-media`.

## Source and setup

Discover current tools first. Require only the tools needed for the requested route: project creation and highlight retrieval, or custom excerpts from an existing project. Report missing capabilities for affected steps. Installing this skill does not deploy those tools. Resolve named or uncertain workspace/teamspace scope with `api_getWorkspaceInfo` and `api_listTeamspaces`; carry its numeric `space_id` through calls where exposed by the current schema, including assets and drafts.

The backend has download routes for direct media files, YouTube (`youtube.com`/`youtu.be`), Vimeo, and Google Drive file links. The source must be downloadable by the service; a private/login-only link or arbitrary webinar landing page is not a guaranteed source. Preserve signed URL query strings. For an asset UUID, call `api_getAsset`, require ready `status: 4`, and use its fresh file URL. Local paths and chat attachments need supported intake through `manage-assets` first.

A request to create clips authorizes the credit-consuming repurposing job; discovery alone does not. Reuse an existing project when supplied. Select `project_type: "V"` for video or `"A"` for audio/podcast. Match the source language; do not silently use `en-US` for a known other language.

Choose supported settings: `duration` is a target preset of 15, 30, 58, 180, or 300 seconds; `aspect_ratio` is `youtube-shorts`, `youtube-video`, or `instagram-post-video`; `clip_layout` is `auto`, `just_active_speaker`, or `center_fit`. State reasonable assumptions such as vertical Shorts and the 58-second preset. Use only verified brand-kit settings.

## Submit once, then follow the right resource

| Step | Tool and identifiers | Completion |
|---|---|---|
| Create source project | `media_createRepurposeProject` with `title`, `media_url`, chosen settings | Returns project `id`, not a task ID |
| Inspect project | `media_getRepurposeProject(project_id)` | `DONE`/`UPDATED` ready; `FAILED` terminal |
| Enumerate clips | `media_listRepurposeClips(project_id, page)` | Read every results page, follow `next`, deduplicate clip IDs |
| Inspect each clip | `media_getRepurposeClip(project_id, segment_id)` | `DONE`/`UPDATED` and usable `download_url` needed |

Project completion does not establish every clip's readiness. Check each selected clip, retain successes, stop failed clips, and continue pending clips with bounded waits, such as 10-second intervals. Return pending IDs if the wait ends. These project and clip UUIDs are neither Celery task IDs nor video export IDs: do not pass them to `api_getTaskResult` or `media_getVideoExport`.

There is no clip-count parameter. For “five clips,” inspect all pages and select five distinct ready highlights grounded in the source. If fewer are ready, retain them, report the shortfall and pending/failed items, and use source-grounded custom excerpts when authorized; do not invent timestamps or rerun the entire project to chase a count.

## Custom excerpts and retry recovery

For an existing project with ready transcription, “02:15–03:00” means `media_createRepurposeClip(project_id, title, start_time: 135, end_time: 180)`. Both values are absolute **whole source seconds**, 0–86399, with end later than start and within the source duration. When transcript word times are supplied in milliseconds, divide by 1000, then choose valid whole-second boundaries grounded in the requested excerpt. Custom clips inherit the project's format/layout; this tool has no aspect-ratio override.

The returned `id` is the clip UUID; poll it as `segment_id` with the same project. If submission times out with an ID, inspect that resource before retrying. If a custom clip ID is lost, reconcile all existing clip pages by `source: "CU"`, title, source range and submission context; reuse only an unambiguous match. A project timeout without its ID cannot be recovered through an exposed project-list or idempotency-key parameter. Report the uncertain submission and recover its ID from available client history rather than blindly creating another paid project.

## Preserve context and hand off usable media

Keep a ledger of source URL/title, project ID, clip ID, and the timestamp fields actually returned in `payload`. AI selection may adjust endpoints and add buffers; selection timestamps are not proof of exact final render boundaries. Verify the rendered excerpt before claiming exact boundaries. Never invent speech, speaker names, quotes, or a transcript from a clip URL alone.

Clip `id` and `story_id` are not library asset UUIDs. If a verified ready asset ID is returned, reuse it; otherwise import the completed `download_url` with `api_createAsset`, then verify the new asset with `api_getAsset` until `status: 4`. Preserve scope, names and source ranges. Do not regenerate a successful clip to get an asset ID.

For requested social drafts, hand ready asset UUIDs and grounded captions to `simplified-social` with `action: "draft"`. If no accounts are connected, accountless drafts are supported. Use `content-repurposer` for channel-specific copy and `campaign-review` for a requested review package. Clip creation and drafting do not authorize scheduling or publishing.

Return links to ready clips, source ranges with any boundary limitations, saved asset/draft IDs, and unfinished items. A failed clip must not erase successful outputs or cause duplicate drafts.
