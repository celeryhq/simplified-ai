# Social, PM, and workspace contract scenarios

These scenarios verify skill behavior without live writes. Fixture identifiers
must be replaced by exact values discovered in the selected context. Account
IDs below are illustrative; all UUID fixtures must be valid UUIDs.

| Scenario | Expected behavior |
|---|---|
| Account listing returns numeric `id:123`; user requests draft | Posting payload uses `account_ids:["123"]`; analytics uses integer `account_id:123`; listing drafts uses CSV `account_ids:"123"`. Numeric posting arrays fail connector schema validation. |
| No connected accounts; user requests text draft | Save `action:"draft"` with omitted/empty `account_ids`; do not stop or demand connecting an account. A publish or account-analytics request still requires a connected account. |
| User asks for all accounts or one platform | One unfiltered `social_getSocialMediaAccounts` call; filter returned rows client-side. Do not fan out deprecated `network` calls. |
| User explicitly authorized exact publication content, accounts, and timing | Proceed under existing authorization; do not request duplicate permission. If material content/targets/timing remain unknown or change, show the concrete proposal before publishing. |
| User says post now; queue timing differs across sources | Use `add_to_queue` only with publishing authorization. Describe service-determined queue timing, make no immediate-delivery guarantee, and report actual returned timing/status. |
| Workspace, account, and explicitly requested scheduling timezones differ | Read workspace/account context. Create schema exposes `date` and no timezone field. Resolve service timezone interpretation before conversion; disclose unresolved conflict and retain a draft if exact requested timing cannot be satisfied. |
| Attach a local image | Sign with valid UUID, PUT bytes without Simplified auth, register only after PUT succeeds, carry integer `asset_type` unchanged, poll same scoped asset to `status:4`, use UUID in social media. Never expose signed upload URL. |
| Attach video with explicit poster | Accept `media:[{url:"https://example.test/video.mp4",thumbUrl:"https://example.test/cover.jpg"}]`; do not reduce the supported array to strings only. |
| LinkedIn PDF carousel | Wait for PDF asset readiness, get fresh PDF `file_url`, use `additional.linkedin.document:{url:<pdf-url>,title:<optional-title>}` with `media:[]` and usual audience. Do not put asset UUID in document `url`. |
| Add discovered drafts to an existing bundle | Call `social_addDraftsToSocialMediaReviewBundle` with exact string `bundle_id` and non-empty string `draft_ids`; retain bundle identity; existing drafts are skipped idempotently. |
| Whoami contains visible space absent from membership list | Do not claim membership from whoami. Resolve accessible IDs using paginated `api_listTeamspaces`; never substitute another teamspace after access denial. |
| User selects teamspace 42 and requests asset/post workflow | Carry integer `space_id:42` through every related list, read, write, and poll. Do not rely on persisted hosted session or reuse resources discovered in another scope. |
| Scoped payload returns 400 for an invalid field | Inspect/correct actual field error in the same scope; do not infer teamspace invalidity or retry another space. |
| Analytics returns `account_active:false` | Explain reconnect requirement before consuming/charting metrics; do not report null data as zero. |
| Analytics status is `NO_PERMISSION`, `DISABLED`, `ERROR`, or `NOT_SUPPORTED` | Explain availability state; do not fabricate zero metrics. Treat `PROCESSING` as pending. |
| Aggregating accounts 123 and 456, one disabled | Use `account_ids:"123,456"` with dates; inspect `accounts_status`, disclose excluded account and partial aggregate coverage. Singular `account_id` takes precedence if both selectors are supplied. |
| Unknown Range metric versus known enum unsupported on network | Arbitrary unknown metric fails connector enum validation; a valid enum metric unsupported by selected network may be ignored upstream. Use listed metrics relevant to actual account type. |
| User knows timezone and requests analytics | Supply `tz` only to Range/Audience; Posts/Aggregated do not expose `tz`. |
| Last 7 days including 2026-10-02 | Query `date_from:"2026-09-26"`, `date_to:"2026-10-02"`; exactly seven inclusive dates. Seven completed days end 2026-10-01. Week boundaries honor workspace `start_of_week`. |
| Search expected subtask across a board | Resolve board/statuses, query each relevant status with `include_subtasks:true`, paginate and deduplicate; direct-get a known UUID/slug before declaring it absent. |
| Resolve assignee by name | Use integer user ID from `pm_listWorkspaceMembers.options[].value`; do not invent `member_id` or use membership-record ID. Focused assignee mutation uses `add`/`remove`. |
| Add/remove task tags | Pass tag names in `add`/`remove` or composite `tags_add`/`tags_remove`; do not confuse social numeric label IDs with PM tag names. Verify expanded direct task read. |
| Dependency A blocks B | Read both tasks/graph and use `task_id:A`, `target_task_id:B`, `relation_type:"BLOCKS"`; remove only discovered relationship ID under explicit authorization. |
| Mark task complete but blockers or running timer remain | Inspect dependencies and task state; completion uses `complete:true`, and server may reject blockers/running timer. Explain cause and do not force completion. Moving to a completed-looking column alone is not assumed to set `complete`. |
| Drain PM source column into destination | `pm_moveStatus` migrates one source's tasks; source remains. Verify empty and delete separately only when source deletion was authorized. |
| Task composite assignee/tag write succeeds | Verify using expanded `pm_getTask`, because initial result may omit post-hook changes and search is eventually consistent. |
