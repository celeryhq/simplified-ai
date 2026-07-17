# Project Management Workflows

Use this reference when selecting tools or coordinating a multi-step PM change.

## Operation map

| Goal | Preferred tools |
|---|---|
| Find or inspect boards | `pm_listBoards`, `pm_getBoard` |
| Create, edit, clone, or delete a board | `pm_createBoard`, `pm_updateBoard`, `pm_cloneBoard`, `pm_deleteBoard` |
| Resolve or manage columns | `pm_listStatuses`, `pm_getStatus`, `pm_createStatus`, `pm_updateStatus`, `pm_deleteStatus` |
| Drain and retire statuses | `pm_moveStatus` |
| Find tasks | `pm_searchTasks`, `pm_searchRecentTasks` |
| Create, inspect, edit, clone, or delete a task | `pm_createTask`, `pm_getTask`, `pm_updateTask`, `pm_cloneTask`, `pm_deleteTask` |
| Manage assignees or tags | `pm_listWorkspaceMembers`, `pm_updateTaskAssignees`, `pm_updateTaskTags` |
| Manage attachments or custom fields | `pm_updateTaskAttachments`, `pm_updateTaskCustomFields` |
| Manage subtasks | `pm_createTask` with `parent`, `pm_listSubtasks` |
| Review task history | `pm_getTaskActivity` |
| Manage dependencies | `pm_getTaskDependencies`, `pm_addTaskDependency`, `pm_removeTaskDependency` |
| Manage task comments | `api_listComments`, `api_addComment` |

## Create a task

1. Resolve the board with `pm_listBoards`.
2. Resolve the target status with `pm_listStatuses`.
3. Resolve assignees with `pm_listWorkspaceMembers` when names were supplied.
4. Call `pm_createTask` with the status UUID. The board is inferred from the
   status.
5. Pass tag names and integer assignee IDs when requested.
6. Verify with `pm_getTask` and
   `expand=status_details,assignees,tags,board`.

If the requested status does not exist, ask before creating a new status. Do not
silently place the task into another column.

## Update or move a task

1. Resolve the task by ID/slug or scoped search.
2. Read the current task and relevant expanded fields.
3. Resolve the new status or assignee dynamically.
4. Apply only the requested fields with `pm_updateTask` or the focused
   assignee/tag tool.
5. Read the task again with the changed fields expanded.

To fully reassign a task, add the new member and remove the old member. Do not
assume adding one assignee replaces existing assignees.

## Complete a task

1. Read the task and call `pm_getTaskDependencies`.
2. If `is_blocked` or incomplete blockers are present, explain the blockers and
   do not force completion.
3. Resolve the workspace's completed status if the user asked to move the task.
4. Apply the requested completion field and/or status change.
5. Verify the final task state directly.

Do not assume every board uses a column named `Completed`; use the live status
list and ask when several completion-like columns exist.

## Dependencies

Read the dependency graph first to avoid duplicates. For
`pm_addTaskDependency`, pass the source task as `task_id`, the counterpart task
as `target_task_id`, and one uppercase relation:

- `BLOCKS`: the source task blocks the target task.
- `RELATES_TO`: the tasks are related without ordering.
- `DUPLICATES`: the source task duplicates the target task.

Remove a relationship only with the `relationship_id` returned by
`pm_getTaskDependencies`, and confirm immediately before removal.

## Comments

Comments are generic API tools, not `pm_*` tools:

```text
api_listComments({content_type: "task", object_pk: "<task-uuid>"})
api_addComment({content_type: "task", object_pk: "<task-uuid>", comment: "..."})
```

For a threaded reply, read comments first and pass the integer comment ID as
`parent`.

## Boards and statuses

- Use `pm_updateStatus(order=...)` to reorder a status.
- Use `pm_moveStatus` to migrate every task from source statuses into a target
  status and retire the sources. Confirm because this is a bulk change.
- Confirm before `pm_deleteStatus`; the status must be empty.
- Confirm before `pm_cloneBoard`; cloning can create many resources.
- Confirm before board, status, and task deletion.

## Search across a board

1. Resolve the board.
2. List its statuses.
3. Call `pm_searchTasks` once per relevant status with both `board` and `status`.
4. Continue pages until exhausted, keeping `page_size <= 100`.
5. Deduplicate by task ID and filter title/description client-side when a broad
   full-text term matched comments or tags.
