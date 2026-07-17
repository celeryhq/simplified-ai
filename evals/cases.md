# Canonical Eval Definitions

Machine-checkable definitions behind [openai-test-cases.md](openai-test-cases.md).
Each case has: the user prompt, the **tool sequence** we expect the model to call,
the **arguments contract**, and **assertions** (deterministic checks on tool I/O).
The eight marketer workflow skills have a separate 24-case agent suite in
[skill-cases.json](skill-cases.json).

Two layers:
- **Agent layer** — does the model pick the right tool(s) for the prompt? (eyeballed
  in Codex / OpenAI's harness; pass criteria below.)
- **I/O layer** — do the tools behave as the skills claim? (automated by
  [run_evals.py](run_evals.py); assertions below.)

Tool names: `api_generateImage`, `social_getSocialMediaAccounts`,
`social_getSocialMediaAnalyticsAggregated`, `social_createSocialMediaPost`,
`social_getSocialMediaDrafts`, `social_deleteSocialMediaDraft`.

Verified response shapes (see [results.md](results.md)):
- `api_generateImage` (transient): `{status:"SUCCESS", detail:{result:["<url str>"], transient:true}}`
- `api_generateImage` (asset): `{status:"SUCCESS", detail:{result:[{asset_id, url}], transient:false, storage:"asset"}}`
- Raw djapp generate endpoint: `202 {task_id, storage}` then poll `GET /api/v1/tasks/{id}`.

---

## C1 — Generate image (text-to-image, transient default)
- **Prompt:** "Generate an image of a white ceramic coffee cup on a clean white background…"
- **Expected tools:** `api_generateImage` (`capability:"prompt"`, `storage:"transient"` default)
- **Args contract:** `parameters` is a nested object containing `prompt` (+ optional `aspect_ratio`). Never flat.
- **Assertions:**
  - response `status == "SUCCESS"`
  - `detail.result` is a non-empty list
  - transient → `detail.result[0]` is a URL string; `detail.transient == true`
  - the URL returns HTTP 200 `image/webp`
- **Agent pass:** confirms the live catalog/schema, chooses `google.gemini-3.1-flash-image-preview` as the quality-first default when available, asks to confirm only if the request is ambiguous, otherwise generates directly, and returns the image URL.

## C2 — Generate image (text-in-image, specific model + ratio)
- **Prompt:** 'Make a 16:9 promo banner that says "Summer Sale" in bold modern type'
- **Expected tools:** `api_generateImage` (`model:"ideogram.ideogram-v3-turbo"`, `capability:"prompt"`, `parameters.aspect_ratio:"16:9"`)
- **Assertions:**
  - `status == "SUCCESS"`, `detail.result` non-empty
  - returned image is landscape 16:9 (≈1.78 ratio)
- **Agent pass:** confirms the live catalog/schema, picks `ideogram.ideogram-v3-turbo` for a typography-first banner (or Gemini Pro when dense professional layout/4K is requested), explains the choice when cost or output differs materially, and sets `aspect_ratio:"16:9"` when that is the discovered field.

## C3 — List connected social accounts (read)
- **Prompt:** "Which social media accounts do I have connected?"
- **Expected tools:** `social_getSocialMediaAccounts` (no args)
- **Assertions:**
  - response has `accounts` (list)
  - each account has integer `id`, `name`, `type`
  - tool is called **once, with no `network` arg** (don't loop per platform)
- **Agent pass:** if `accounts` empty → tells user to connect an account, does NOT call create.

## C4 — Draft a social post (no publish)
- **Prompt:** "Draft a LinkedIn post announcing our new AI image feature"
- **Expected tools:** `social_getSocialMediaAccounts` → `social_createSocialMediaPost` (`action:"draft"`)
- **Args contract:** `message` ≤ 3000 chars; `action == "draft"`; for LinkedIn, `additional.linkedin.audience`. (Drafts may be accountless.)
- **Assertions:**
  - create call uses `action == "draft"` (NOT `schedule`/`add_to_queue`)
  - create returns success; the draft appears in `social_getSocialMediaDrafts`
- **Agent pass:** shows the draft text and does not publish/schedule without explicit confirmation.

## C5 — Analytics overview (read)
- **Prompt:** "How did my Instagram account perform last month?"
- **Expected tools:** `social_getSocialMediaAccounts` → `social_getSocialMediaAnalyticsAggregated`
- **Args contract:** `account_id` is the integer id from accounts; `date_from`/`date_to` = last month; `date_to` ≤ today.
- **Assertions:**
  - response `baseLine` contains `impressions_aggregated`, `engagement_aggregated`, `followers_aggregated`, `publishing_aggregated`
  - each KPI has `value` and `prevValue`
  - `date_to` not in the future
- **Agent pass:** summarizes KPIs with period-over-period change; does not dump raw payload.

## C6 — Generate image → attach to draft post (cross-skill)
- **Prompt:** "Generate a product image of a sneaker and draft an Instagram post with it"
- **Expected tools:** `api_generateImage` (`storage:"asset"`) → `social_getSocialMediaAccounts` → `social_createSocialMediaPost` (`action:"draft"`, `media:["<asset_id>"]`)
- **Assertions:**
  - generate returns `detail.result[0].asset_id` (asset mode)
  - that exact `asset_id` is passed into `media` of the create call
  - create uses `action:"draft"` and includes `additional.instagram.{postType,channel}`
- **Agent pass:** uses `storage:"asset"` (not transient) precisely because the image must persist for the post; shows the draft; asks before publishing.

---

## Failure → fix mapping

| Failure signal | Fix |
|---|---|
| Wrong tool chosen | Tighten the skill `description` / trigger words |
| Posts/schedules without confirming | Strengthen the safety block in `simplified-social/SKILL.md` |
| "Post now" becomes a future `schedule` | Reinforce: `add_to_queue` = publish ASAP |
| Flat `parameters` → 400 | Reinforce the nested-`parameters` rule in `generate-image/SKILL.md` |
| Re-uploads instead of reusing the asset | Reinforce the asset_id → `media` handoff |
| transient used when the image must persist | Reinforce: use `storage:"asset"` when posting/reusing |
