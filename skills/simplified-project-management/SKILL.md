---
name: simplified-project-management
description: >-
  Manage Simplified project-management boards, statuses, tasks, assignees,
  tags, dependencies, comments, activity, and searches through the Simplified
  hosted MCP connector. Use when the user explicitly asks to inspect or change
  Simplified PM data, create or triage tasks, update assignments or status,
  manage boards and columns, review dependencies, or complete tracked work. Do
  not invoke for generic coding or debugging unless the request also involves
  updating Simplified project-management records.
---

# Simplified Project Management

Operate each user's own Simplified PM workspace through the hosted connector.
Discover identifiers from live tools and optionally cache stable mappings in
agent memory; never ship or assume tenant-specific IDs.

## Connector

Use the Simplified hosted MCP connector at `https://apikit.simplified.com/mcp`.
Use logical `pm_*` tool names for PM resources and `api_listComments` /
`api_addComment` for task comments.

If a call returns `401`, `Unauthorized`, `Needs authentication`, or a connection
error, stop and ask the user to reconnect Simplified. Do not retry writes while
authentication is unresolved.

## Core Workflow

Follow: **Discover -> Read -> Confirm -> Write -> Verify**.

### 1. Discover context

1. Call `pm_listBoards` and match the user's board by title or slug.
2. If multiple boards match, ask the user which board they mean.
3. Call `pm_listStatuses` for the selected board before resolving a status name.
4. Call `pm_listWorkspaceMembers` before assigning by a person's name or email.
5. Use IDs returned by the connector only. Do not retain tenant-specific IDs in
   the skill or infer IDs from names.

For teamspace-scoped work, pass `space_id` when the user selected a teamspace.
Otherwise omit workspace and teamspace arguments and use the authenticated
default context.

### Optional memory cache

Use agent memory when the client provides it, but keep the workflow functional
without memory.

- Cache stable board, status, member, and tag mappings after live discovery.
- Namespace every entry by connector, authenticated workspace, and teamspace so
  IDs can never leak across accounts or tenants.
- Store the resource type, ID, display name, parent board ID when relevant, and
  `last_verified_at`. Store a user's preferred board/teamspace only when they
  explicitly chose it or asked for that preference to persist.
- Treat same-session values as fresh. On the first cross-session use, after a
  meaningful age, or before a consequential bulk action, validate the mapping
  with the appropriate live list/get tool.
- Refresh memory after a successful create, rename, move, or delete. Invalidate
  it on `404`, name/parent mismatch, workspace switch, or authentication change.
- Never store access tokens, authorization headers, private task descriptions,
  comments, attachments, or search-result bodies in memory.

Memory reduces repetitive discovery calls; it does not replace direct reads for
current task state or post-write verification.

### 2. Read before writing

- Read a task with `pm_getTask` before changing, deleting, cloning, completing,
  or linking it.
- Use `expand=status_details,assignees,tags,board` when those fields affect the
  decision or must be verified.
- Read dependencies with `pm_getTaskDependencies` before adding a relationship
  or marking a blocked task complete.
- Read comments with `api_listComments` before replying to a thread.

### 3. Confirm consequential actions

Proceed without an extra confirmation when the user explicitly requested an
ordinary create or edit and the target is unambiguous.

Get explicit confirmation immediately before:

- deleting a board, status, or task;
- removing a task dependency;
- draining a status with `pm_moveStatus`;
- cloning a board with its statuses and tasks;
- performing a bulk or ambiguous change.

State the exact resource and effect in the confirmation. Do not treat a request
to inspect or plan a change as permission to execute it.

### 4. Write precisely

- Pass plain text in task `description`; do not construct `rich_description`.
- Use ISO 8601 date-time values for `start_date` and `due_date`.
- Use `pm_updateTaskAssignees` or `assignees_add` / `assignees_remove` for
  assignment changes. Resolve integer member IDs first.
- Use `pm_updateTaskTags` or `tags_add` / `tags_remove` for tag changes.
- Use uppercase `BLOCKS`, `RELATES_TO`, or `DUPLICATES` for dependencies.
- Use `api_addComment` with `content_type: "task"` and the task UUID as
  `object_pk`. Use an integer comment ID as `parent` for a reply.
- Use `pm_updateStatus(order=...)` to reorder a column. Use `pm_moveStatus` only
  to move all tasks out of one or more statuses and retire those statuses.

### 5. Verify the result

- Verify task writes with `pm_getTask`, not immediate search results.
- Expand the fields changed by the write.
- Verify dependency changes with `pm_getTaskDependencies`.
- Verify board and status changes with their direct get or list tools.
- Report the resulting task/board title, status, assignees, and identifier.

If a write returns a transient or ambiguous error, do not retry blindly. A write
may have committed. Use a returned ID for a direct read; if no reliable ID was
returned, explain the uncertainty and ask before attempting another create.

## Search and Listing

Scope `pm_searchTasks` by board and status whenever possible. For a whole-board
search, list statuses and query each column, paginate, and deduplicate task IDs.
Keep `page_size` at or below 100. Treat search as eventually consistent after a
write; use direct `get` tools for verification.

Use `pm_searchRecentTasks` for recently modified cross-board work. Use
`pm_getTask` on candidates when exact creation timestamps or expanded relations
matter.

## References

- Read [references/workflows.md](references/workflows.md) for operation routing,
  board/status management, subtasks, dependencies, comments, and completion.
- Read [references/tool-behavior.md](references/tool-behavior.md) after a search,
  write, pagination, expansion, or rich-description issue.
