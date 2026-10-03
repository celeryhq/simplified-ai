---
name: generate-voiceover
description: Use when the user wants spoken narration, text-to-speech, a voiceover from a script, available Simplified voices, or an existing voice resolved for a language. For recording transcription, use transcribe-media instead.
---

# Generate narration from approved text

Discover the voice and language before synthesizing. Keep approved spoken meaning intact and return reusable audio with honest timing information.

## Scope and generation intent

Use the connected Simplified tools and current schemas. Resolve a named or uncertain workspace/teamspace using `api_getWorkspaceInfo` and accessible membership from `api_listTeamspaces`; carry numeric `space_id` into voice discovery, synthesis, storage, and downstream calls.

A request to create narration authorizes the requested synthesis. “Show voices” or “what would it cost?” is discovery only: do not generate or spend credits. Clarify missing script, language, or constraints that change the result before synthesis. Do not add translations, variants, or repeated paid attempts unless requested.

## Select an actual voice

Call `api_listVoices` with the required exact `language_code`, such as `en-GB` or `en-US`. If the request only says English and no context resolves the locale, obtain or state a suitable locale choice before lookup; do not invent an all-locales call. For a saved UUID, `api_getVoice` resolves its actual details.

| Need | Behavior |
|---|---|
| Named voice | Use `voice_name` plus locale; verify the returned `voice_name` AND `language_code` before using its UUID |
| Legacy deployment ignores name filter | Inspect all returned entries; never assume `voices[0]` is the requested voice |
| No optional filter requested | Omit it or retain the documented empty-string sentinel; `0` and `false` are real filters |
| Neutral delivery | Do not infer neutral gender; gender filter `3` is only for a requested neutral-gender voice |
| Provider, premium tier, engine, gender requested | Use the actual supported filter and verify the selected entry meets it |
| Style/pace instructions | Include `instructions` only when `supports_instructions: true` |

`search` matches locale/language names, not voice names. Voice UUIDs can differ for the same name across locales; re-resolve the name after a language change. Do not fabricate a voice or silently substitute another one. If the requested name and explicit gender/provider constraints conflict, clarify the choice.

For options, show a short relevant list of names, locales, descriptions, supported instruction behavior, and returned samples. Do not promise a model or price from memory.

## Prepare the script and duration

Use the approved script verbatim unless adaptation was requested. Resolve pronunciation or ambiguous markup before spending. Plain prose uses `use_ssml: false`. Use `true` only for valid supplied/prepared SSML and an appropriately supported voice; do not wrap plain text merely to set the flag. Validate malformed markup or ask about ambiguous meaning instead of speaking broken tags as text.

The generation schema has no duration or rate field. `instructions` nudges delivery but is not an exact timing control, and unsupported voices ignore it. Word-count estimates are estimates. For “exactly 30 seconds,” resolve the requirement before a paid job: accept approximate narration or arrange separately supported measurement/editing. Do not promise exact runtime, invent `duration`, silently change approved copy, or regenerate repeatedly to chase timing.

## Synthesize and retain the result

Call `api_generateAudio` with the verified `voice_id`, `text`, `use_ssml`, and `storage: "asset"` for retained/reused narration (`"default"` only for an explicitly temporary result). Add supported `instructions` only when appropriate. There is no separate language/model/duration argument in this generation request; the voice selects the language/provider.

Inspect the actual returned payload; do not require an image/video response shape. Current middleware waits for completion. If only a pending/timeout task identifier returns, continue that exact `task_id` with `api_getTaskResult` where exposed, using reasonable intervals and a bounded wait. Stop on terminal failure, and never synthesize again merely because storage or completion metadata is missing.

Retain a returned verified audio asset UUID. If the result has only a usable URL even though persistence was requested, resolve an identifiable stored result when supported; otherwise use `api_createAsset` with the existing audio URL, then `api_getAsset` until ready `status: 4`. Keep signed query strings intact. Do not mistake a voice UUID, task ID, or arbitrary response `id` for the audio asset UUID. Follow `manage-assets` for failed/pending storage.

Return the actual voice/locale, audio link, verified asset UUID/readiness, and measured runtime when available or explicit unverified timing. Script narration does not combine audio with a video by itself. Use only exposed composition operations for that handoff, and do not claim an assembled video or published post from an audio result.
