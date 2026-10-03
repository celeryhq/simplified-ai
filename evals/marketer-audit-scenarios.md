# Marketer audit scenarios

These are expected behaviors from static contract review, not evidence of live execution. Run against the tools actually exposed in the client; preserve numeric `space_id` across every connected operation.

| Skill | Realistic request | Expected behavior and factual contract coverage |
|---|---|---|
| social-content-planner | Plan next month for Acme East; do not save yet. | Resolve scope if connected channel facts are needed; call account discovery once without a network filter. Return a calendar in conversation without remote writes. On later authorized drafts, resolve assets and platform settings, retain successful IDs, and report partial failures without duplication. |
| cross-platform-campaign | Prepare launch drafts using the car photos in Acme East. | Resolve teamspace before accounts/assets; asset name/tag discovery uses search and image filter with pagination. Use ready UUIDs and channel-native additional fields. Existing media does not authorize new generation; final publishing matrix needs explicit approval once. |
| content-repurposer | Turn this private webinar link into LinkedIn and Instagram drafts. | Attempt available source retrieval; if inaccessible and no transcript exists, explain the coverage gap and request source text. Do not invent the webinar. Once read and draft saving authorized, use selected scoped account IDs and valid media/settings. |
| evergreen-content-engine | Build a 90-day evergreen engine and save the first six drafts. | Return territories, proof, refresh dates, and retirement rules; save only requested draft set. Reuse ready scoped assets; preserve successes if item six fails. Describe renewal as a process, not a configured monitor or indefinite repost automation. |
| local-business-marketing | Draft an offer for our downtown Google location using this chat photo. | Verify exact location/account, offer terms, CTA and dates. Require actual byte access and PUT capability before upload signing; otherwise request uploaded asset ID/downloadable URL. Use Google STANDARD/EVENT/OFFER contract; state missing media/facts and do not publish. |
| creative-testing | Design a hook test; then save three variants with no prior baseline. | Design-only stage creates no remote drafts. Once saving requested, discover scoped connected accounts even without a baseline. Use one declared variable, valid platform settings, real asset IDs and available outcome metrics. Do not claim statistical significance from organic totals. |
| social-performance-analyst | How did Acme East perform recently? | Resolve scope; use 30 completed dates ending yesterday, concrete dates and integer analytics account IDs. Paginate post results. Pass tz only on Range/Audience, whose schemas expose it; disclose material UTC boundary limits elsewhere. Do not treat omitted metrics as zero or claim revenue from engagement. |
| campaign-review | Bundle all drafts for Acme East; later append these two and change an account. | Retrieve every discoverable connected-account draft page, scoped/deduplicated; disclose accountless-draft coverage limits. Create bundle when explicitly requested. Append through exposed addDrafts operation with bundle_id and nonempty draft_ids; do not recreate. Update permits message/media/tags/date/time/timezone, not account/additional changes; replacement requires explicit request. Review approval alone does not authorize publishing. |

## Evidence anchors

- `social_media_openapi.yaml`: unfiltered account discovery, analytics request schemas, paginated draft listing with required account_ids, CreatePostRequest allowing accountless drafts, UpdateDraftRequest supported fields, ReviewBundleAddDrafts and review URLs.
- `api_openapi.yaml`: name/tag asset search and image filter, pagination, no named-folder enumeration, sign/PUT/register upload and ready status 4.
- `middleware.py`: per-call synthetic space_id consumed into the upstream Space header.
- No scenario establishes paid generation, successful uploading, visual inspection, publication, or complete accountless enumeration without returned evidence.
