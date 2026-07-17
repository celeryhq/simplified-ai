# `smp comments` — Comments Reference

Threaded comments on any commentable Simplified resource. Currently supports
**tasks**; the surface will grow to other types (documents, projects, etc.)
as the underlying API adds support.

## Why a top-level namespace?

The API is generic by design — comments aren't PM-specific. Internally they
use Django's GenericForeignKey: every comment is addressed by

- `content_type` — the resource family (e.g. `task`)
- `object_pk` — the UUID of the resource

Putting comments under `pm` would have hidden that genericness and forced a
new wrapper for every commentable type. The top-level `smp comments`
namespace stays honest with the API shape.

## Commands

### List comments on a resource

```bash
smp comments list-comments \
  --content-type task \
  --object-pk <resource_uuid>
```

Returns paginated top-level comments. Standard `--page` / `--page-size` apply.

### Add a comment

```bash
# Top-level comment
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

## Gotchas

**`--content-type` is required even though `task` is the only supported value
today.** Pass it explicitly. The enum will grow.

**`--object-pk` is the resource UUID** — for a task, that's the task UUID
(same one you pass as `--task-id` to `smp pm` commands). The flag name
matches the API's GenericForeignKey contract, not the resource-specific
shortcut.

**`--parent` takes an integer comment ID,** not a UUID. Look it up from the
`list-comments` response.

## Discovering commands

```bash
smp comments --help
smp comments <command> --help
```
