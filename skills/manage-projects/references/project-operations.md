# Project Operations

## Resource types

- `Project`: default for campaigns, editorial programs, content operations, and general marketing work.
- `AdCreativeProject`: use only when the user is explicitly working with the specialized ad-creative model.

Pass the same `resourcetype` to list, create, get, delete, item, reorder, assignment, comment, and export operations.

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

## High-consequence operations

- `api_deleteProject` and `api_deleteProjectItem` are soft deletes but still require a verified target.
- `api_assignAgentToItem` may trigger downstream execution. Confirm the agent and scope.
- `api_exportProjectItems` sends selected items to a partner integration. Confirm `partner_id`, exact item IDs, and destination intent.
- `api_reorderProjectItem` changes execution sequence. Preserve dependency order.

## Campaign project template

Typical gates are strategy approved, claims/source verified, copy approved, creative approved, platform adaptation complete, final review complete, scheduled, and performance review due. Use only the gates that materially apply.
