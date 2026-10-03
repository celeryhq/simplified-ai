# `smp pm` reference

Read [simplified-project-management](../../simplified-project-management/SKILL.md) for operation behavior and verification. Boards contain status columns; tasks are created in a resolved status UUID. PM membership IDs are integers; they are not social account IDs.

## Discovery and ordinary writes

```bash
smp pm:list-boards
smp pm:list-statuses --board-id <board-uuid>
smp pm:list-workspace-members --search "Alex"
smp pm:create-task --status <status-uuid> --title "Prepare launch" --description "Deliver approved launch copy"
smp pm:create-task --status <status-uuid> --title "Write tests" --parent <task-uuid>
smp pm:get-task --task-id <task-uuid> --expand assignees,tags
```

Do not choose the first result in a script when the user has named a board/person. Resolve an unambiguous match or ask. Optional memory entries must be scoped by connector, workspace, teamspace, resource, and parent where relevant, and refreshed on a scope/auth change or stale read. Never cache credentials or task content.

## Assignments, dependencies, and search

```bash
smp pm:update-task --task-id <task-uuid> --assignees-add '[123]' --tags-add '["launch"]'
smp pm:get-task-dependencies --task-id <task-uuid>
smp pm:add-task-dependency --task-id <blocking-task-uuid> --target-task-id <blocked-task-uuid> --relation-type BLOCKS
smp pm:search-tasks --board <board-uuid> --status <status-uuid> --search launch
smp pm:search-recent-tasks --search launch
```

Replace sample member IDs with discovered IDs. `BLOCKS`, `RELATES_TO`, and `DUPLICATES` are uppercase. Use plain task descriptions; middleware constructs rich-description data. Verify assignments/tags with a direct expanded get, since create responses can omit hook-applied relations.

Scope searches to the requested board/status, paginate, and deduplicate. Direct gets are authoritative for post-write verification. Read dependencies before completing a blocked task. Bulk changes/deletion require an exact user-authorized target; report partial successes without repeating writes.

Comments use the `api` namespace; see [comments](comments.md). Inspect help before cloning boards or draining statuses—these are different effects from changing a task's status.
