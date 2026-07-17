# `smp pm` — Project Manager Reference

Boards, statuses, tasks, subtasks, assignees, tags, dependencies, comments,
and activity.

## Core Concepts

- **Board** — a Kanban project. Has statuses (columns) and tasks.
- **Status** — a column within a board (e.g. "To Do", "In Progress"). Tasks live
  inside statuses, not boards directly.
- **Task** — always belongs to a status. To create a task you need a `status_id`,
  not just a `board_id`.
- **Composite fields** — `pm create-task` and `pm update-task` accept assignees
  and tags inline; the toolkit makes the sub-resource calls automatically.

## Memory Pattern (per-board cache)

If memory tools are available, treat memory as an L1 cache for PM identity
lookups. Board UUIDs, status IDs, user IDs and tag IDs are stable across runs —
re-fetching them on every call is wasteful.

### Memory schema

```
pm/board:<board_id>/meta       → {id, title, slug}
pm/board:<board_id>/statuses   → {status_id: status_title}
pm/workspace/users             → {user_id: "First Last (email)"}
pm/workspace/tags              → {tag_id: tag_name}
```

`statuses` is per-board (each board has its own columns). `users` and `tags` are
workspace-scoped (one table per workspace).

### On first contact with a board

If `pm/board:<board_id>/meta` is not in memory, seed the cache cheaply before
doing any work:

```bash
smp pm get-board --board-id <id>                # → meta
smp pm list-statuses --board-id <id>            # → statuses table
smp pm list-workspace-members --page-size 100   # → users table (write once per workspace)
```

Three small calls, persist all three to memory, then proceed with the user's
actual request. The user shouldn't notice the seeding.

### Lookup discipline

**Before any CLI call that resolves a name to an ID, check memory first.**

- "Move task X to In Progress" → look up `In Progress` in
  `pm/board:<board_id>/statuses` before calling `pm list-statuses`.
- "Assign to Saurabh" → look up `Saurabh` in `pm/workspace/users` before calling
  `pm list-workspace-members --search`.
- If memory has it: use the cached ID directly, no CLI call.
- If memory misses: fall through to the CLI, then **write the result to memory**
  before using it.

### Post-job introspection

When you finish a task, before replying to the user, ask: *what did this job
teach me that future runs would benefit from?* Examples:

- A board ID the user mentioned that wasn't in memory → seed it now.
- A new user resolved via `--search` → add to the users table now.
- A new status created during this task → add to that board's statuses table.
- An auto-created tag from `pm create-task` → add to the tags table.

### What NOT to cache

- **Task content** (title, description, status, assignees, due dates) — changes
  constantly. Always fetch fresh with `pm get-task`.
- **Task lists / search results** — same reason.
- **Anything with `last_modified` semantics**.

Memory is for **identity** (IDs, names, slugs), never **state**.

## Key Workflows

### Find a board and its statuses

```bash
smp pm list-boards                              # default page_size=10
smp pm list-boards --page-size 50               # more results
smp pm list-statuses --board-id <board_uuid>
```

### Create a task

Assignees and tags can be set inline at create time:

```bash
# Minimal
smp pm create-task --status <status_uuid> --title "Fix login bug"

# With assignees and tags in one shot
smp pm create-task \
  --status <status_uuid> \
  --title "Fix login bug" \
  --priority 2 \
  --tags '["bug", "auth"]' \
  --assignees '[196, 200]'
```

`--tags` takes an array of tag name strings (auto-created if unknown).
`--assignees` takes integer user IDs (from `pm list-workspace-members`).

**Note:** Assignees are NOT in the createTask response. Verify with
`smp pm get-task --task-id <id> --expand assignees`.

### Update a task

```bash
smp pm update-task \
  --task-id <task_uuid> \
  --title "New title" \
  --assignees-add '[196]' \
  --assignees-remove '[200]' \
  --tags-add '["urgent"]' \
  --tags-remove '["bug"]'
```

All fields are optional. Mix and match.

### Find user IDs

```bash
smp pm list-workspace-members
# → {"options": [{"value": 196, "label": "Arun Mittal (email@example.com)"}]}

smp pm list-workspace-members --search "arun"
```

### Search tasks

**Always scope search with `--board` and `--status`.** Without scoping, results
span the entire workspace (hundreds of tasks with no relevance ranking).

```bash
# Correct: one column at a time
smp pm search-tasks \
  --board <board_uuid> \
  --status <status_uuid> \
  --search "login bug"

# Search across all columns of a board
for status_id in $(smp pm list-statuses --board-id <board_id> | \
  python3 -c "import json,sys; [print(s['id']) for s in json.load(sys.stdin)['results']]"); do
  smp pm search-tasks --board <board_id> --status $status_id --search "login"
done
```

Filter options: `--assignees 196`, `--priority 2`, `--complete true`.

Recently modified tasks (Elasticsearch-backed, no scoping needed):

```bash
smp pm search-recent-tasks --search "login bug"
```

### Task dependencies

```bash
# Add: task A blocks task B
smp pm add-task-dependency \
  --task-id <task_a_uuid> \
  --target-task-id <task_b_uuid> \
  --relation-type BLOCKS                   # UPPERCASE required

# relation_type options: BLOCKS, RELATES_TO, DUPLICATES

# Get all dependencies
smp pm get-task-dependencies --task-id <task_uuid>
# → {"blocks": [...], "blocked_by": [...], "related": [...], "is_blocked": false}

# Remove
smp pm remove-task-dependency \
  --task-id <task_uuid> \
  --relationship-id <relationship_uuid>
```

### Activity

```bash
smp pm get-task-activity --task-id <task_uuid>
```

### Comments

Comments are not PM-specific — they live under their own namespace because
the underlying API is generic across commentable resources. See
[comments.md](comments.md). For tasks specifically:

```bash
# List comments on a task
smp comments list-comments --content-type task --object-pk <task_uuid>

# Add a comment to a task
smp comments add-comment \
  --content-type task \
  --object-pk <task_uuid> \
  --comment "LGTM — merging."

# Threaded reply
smp comments add-comment \
  --content-type task \
  --object-pk <task_uuid> \
  --comment "+1" \
  --parent <parent_comment_id>
```

### Subtasks

```bash
# Create as a child of an existing task
smp pm create-task \
  --status <status_uuid> \
  --title "Write tests" \
  --parent <parent_task_uuid>

smp pm list-subtasks --task-id <parent_task_uuid>
```

### Clone

```bash
smp pm clone-board --board-id <board_uuid>     # deep clone (statuses + tasks)
smp pm clone-task --task-id <task_uuid>
```

## Critical Gotchas

**`relation_type` must be UPPERCASE** — `BLOCKS`, `RELATES_TO`, `DUPLICATES`.
Lowercase → 400.

**`pm search-tasks` without scoping returns workspace-wide results** — always pass
`--board` + `--status` together. The UI always does this, fetching one column at
a time.

**JSON arrays need single quotes** — `--assignees '[196, 200]'`,
`--tags-add '["bug"]'`.

**`pm list-boards` vs `pm search-boards`** — use `pm list-boards` (reliable).
`pm search-boards` hits an Elasticsearch index that may be stale and return
`count:0` even when boards exist.

**Verify tag/assignee changes** — confirm with
`smp pm get-task --task-id <id> --expand assignees,tags`.

**Assignees not in createTask response** — always verify with
`pm get-task --expand assignees`.

## Full Example

```bash
# 1. Find a board
BOARD=$(smp --raw pm list-boards | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['results'][0]['id'])")

# 2. Get the "To Do" status
STATUS=$(smp --raw pm list-statuses --board-id $BOARD | python3 -c "
import json,sys
results = json.load(sys.stdin)['results']
todo = next(s for s in results if 'do' in s['title'].lower())
print(todo['id'])")

# 3. Find the user to assign
USER_ID=$(smp --raw pm list-workspace-members --search "arun" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['options'][0]['value'])")

# 4. Create the task with assignees and tags in one shot
smp pm create-task \
  --status $STATUS \
  --title "Implement OAuth2" \
  --priority 2 \
  --assignees "[$USER_ID]" \
  --tags '["auth", "backend"]'
```

## Discovering Commands

```bash
smp pm --help
smp pm <command> --help
```
