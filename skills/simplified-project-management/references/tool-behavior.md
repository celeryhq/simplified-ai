# PM Tool Behavior

Read this reference when troubleshooting a PM operation.

## Search is eventually consistent

`pm_searchTasks` is backed by a search index. Newly created or updated tasks may
not appear immediately. Do not use search to verify a write; use `pm_getTask`
with the returned UUID or slug.

Full-text search covers title, description, tags, and comments. Scope searches
by board and status, then inspect title and description when relevance matters.

Search results may omit exact creation timestamps and expanded relationships.
Read candidate tasks directly when those fields matter.

## Avoid duplicate writes

A transient request error does not prove that a write failed. Never retry a
create blindly. If the response included a resource ID, read it directly. If it
did not, describe the uncertain outcome and ask before another create.

## Lean responses need expansion

Default task responses may omit status details, board, assignees, tags,
attachments, or subtasks. Use comma-separated `expand` fields such as:

```text
status_details,assignees,tags,board
```

Verify composite assignee and tag writes with an expanded direct task read.

## Rich descriptions

Task descriptions are stored as Quill Delta data. Send plain text through the
`description` field and let the connector create `rich_description`. When a
response contains a Delta, read the text from its `ops[*].insert` values.

## Dates and pagination

- Send task `start_date` and `due_date` as ISO 8601 date-time strings.
- Search date filters use `YYYY-MM-DD` dates.
- Keep `page_size <= 100` and paginate larger result sets.

## Board-specific identifiers

Status UUIDs belong to one board. Resolve statuses from the target board before
creating or moving tasks. Member IDs and tags also belong to the authenticated
workspace; discover them rather than carrying IDs across users or workspaces.

When agent memory is available, cache these mappings under the authenticated
workspace and teamspace. Revalidate a cached mapping after a workspace switch,
authentication change, stale/failed lookup, or server-side rename/delete. Do not
use durable memory for changing task state or task content.

## Authentication

On `401`, `Unauthorized`, `Needs authentication`, or a disconnected MCP, stop
and ask the user to reconnect Simplified. Do not repeat the failed write until
authentication is restored and the prior outcome has been checked.
