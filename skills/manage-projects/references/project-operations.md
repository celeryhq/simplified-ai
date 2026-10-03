# Project Operations

## Resource types

- `Project`: default for campaigns, editorial programs, content operations, and general marketing work.
- `AdCreativeProject`: use only when the user is explicitly working with the specialized ad-creative model.

Pass the same `resourcetype` to project/item CRUD, reorder, assignment, and export operations. Comments use `api_listComments`/`api_addComment` with `object_pk` and `content_type: "task"`; they do not accept `resourcetype`. Read the live schema before commenting.

## Safe sequence

1. `api_listProjects`
2. `api_getProject` when a likely match needs verification
3. `api_listProjectItems`
4. Mutate only the approved project/items
5. Read back the affected project or item when correctness matters

For creation, retain the returned project ID and item IDs. Do not infer IDs from titles.

## Item design

Use `api_createProjectItem` with a concise deliverable title and enough context to execute without reopening the entire campaign brief. Useful fields include description, primary type, start date, due date, status, priority, and flexible `data`.

When assets are attached in `data.assets`, store permanent Simplified asset UUIDs. Keep source links and approval references distinct from media assets.

## Update and call contracts

- Project get/update/delete/export uses `id` for the project.
- Item list/create uses `parent_lookup_project_id`; item get/update/delete/reorder/assign additionally uses `id` for the item. All take the matching `resourcetype` and selected `space_id`.
- Read with `api_getProject` or `api_getProjectItem`, then update with `api_updateProject` or `api_updateProjectItem`. When changing `data`, send the complete merged object, preserving unrelated campaign state.
- Dates are ISO date-time strings. Item status is at most 16 characters; priority is an integer. Native owner/dependency fields are not declared here: record metadata in `data`/description, or route actual team task management to `pm_*`.
- `primary_type` is a category, separate from routing `resourcetype`; list filters accept one case-sensitive category of at most 24 characters.
- Reorder takes integer `position`; assignment takes `agent_id` (UUID); export takes numeric `partner_id` and UUID `item_ids`. No public partner-discovery operation is declared. Resolve the integration before exporting, and never invent an endpoint or ID.
- Agent discovery requires a separately configured automation/full connection with the discovery operation exposed; follow `simplified-workflows` for the supported operation. Public projects plus automation agents may require two connected surfaces; installation does not grant those tools automatically.

## High-consequence operations

- `api_deleteProject` and `api_deleteProjectItem` are soft deletes but still require a verified target.
- `api_assignAgentToItem` may trigger downstream execution. Resolve the agent and authorized scope; ask only if unclear.
- `api_exportProjectItems` sends selected items to a partner integration. Resolve `partner_id`, exact item IDs, and authorized destination intent; do not ask again when the user has specified them.
- `api_reorderProjectItem` changes execution sequence. Preserve dependency order.

## Campaign project template

Typical gates are strategy approved, claims/source verified, copy approved, creative approved, platform adaptation complete, final review complete, scheduled, and performance review due. Use only the gates that materially apply.
