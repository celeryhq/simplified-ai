---
name: transcribe-media
description: Use when the user wants a transcript, timestamps, speaker-labeled text, SRT or WebVTT subtitles, or accessible speech content from an audio/video recording in Simplified. Use before content-repurposer when the source must first be transcribed.
---

# Transcribe recordings and export subtitles

Deliver the source transcript separately from summaries or rewritten content. Do not infer words, speaker identities, or timestamps that the returned recording data does not support.

## Source, language, and scope

Verify the connected tools and current schemas. Resolve a named or uncertain workspace/teamspace using `api_getWorkspaceInfo` and accessible membership from `api_listTeamspaces`; carry numeric `space_id` through transcription, source assets, exports, and any downstream draft calls.

`media_transcribeVideo.video_url` takes a reachable audio or video URL, despite the name. An uploaded asset UUID must first be resolved with `api_getAsset`; require ready `status: 4` and use its fresh file URL. A chat attachment or local path is not a hosted file. Use `manage-assets` for client-capable upload/import; otherwise request an accessible source. Do not treat a web page requiring login as the media URL.

Use the recording's known language as `language_code` in BCP-47 form. If unknown and material, ask; do not silently transcribe a non-English recording with the default `en-US`. A request to transcribe authorizes that job; a request to list options does not. Preserve the source file.

## Submit once and inspect completion

Call `media_transcribeVideo` with `video_url` and the chosen language. The raw backend submission can return only an `id`; current MCP middleware normally waits and returns a full transcription record. Do not force another polling call when the returned `job_status` is already `DONE`.

| Returned state | Action |
|---|---|
| `DONE` with `payload.phrases` | Read the transcript; export subtitles if requested |
| Only a transcription `id` | Inspect it with `media_getTranscription` |
| `FAILED` | Stop and report the failure; do not claim a transcript exists |
| `CREATED`, `PENDING`, `PROCESSING`, `RENDERING`, `UPDATED` | Continue the same `id` with `media_getTranscription` |
| Timeout/error envelope containing `id` | Retain that transcription ID and inspect it with `media_getTranscription` before retrying |

`UPDATED` is non-terminal for transcription, even though other media workflows use it differently. Poll at reasonable intervals, such as 10 seconds, with a bounded wait. The transcription `id` is not a Celery `task_id`, an asset UUID, or a repurposing-project ID; do not call `api_getTaskResult` with it. If continuation is unavailable, report the pending ID rather than submit a duplicate.

## Preserve evidence and timing

Read `payload.phrases` and its word-level data. Words can include `text`, `start`, `end`, and `confidence`; timing is in **milliseconds**, so divide by 1000 for seconds. `90000` milliseconds is 90 seconds, not 90000 seconds. Use only the timings actually returned; one timed word does not establish a whole phrase's duration.

A label such as `speaker_0` identifies an anonymous speaker, not a person's name. Attribute names only from reliable provided evidence. Mark unclear/low-confidence content, preserve qualifications, and avoid silently rewriting uncertain names, figures, or claims. A quoted business claim remains speaker testimony unless independently supported.

Keep verbatim transcript and assistant-written summary distinct. Do not claim to have reviewed visuals or non-speech content just because a recording was transcribed. For long content, retain the full transcript and label excerpt coverage.

## Export requested subtitles

Only after `job_status: "DONE"`, call `media_downloadTranscriptionFile` with the transcription `id` and `requested_format: "srt"` or `"vtt"`.

The response is raw subtitle **text**, not necessarily a file URL. Preserve its numbering, timecodes, blank lines, and encoding. Save the returned body to a `.srt`/`.vtt` file when the client can create files, or provide the text accurately. Do not invent a download link or substitute `transcription_url` for a requested subtitle export. An SRT/VTT export does not prove subtitles were burned into the video.

Return the transcript/available artifact, language, supported speaker labels and timestamps, coverage limits, and saved transcription ID. When social repurposing is requested, hand the actual transcript to `content-repurposer`; persist drafts only within the requested scope. Transcription and draft creation do not authorize publishing.
