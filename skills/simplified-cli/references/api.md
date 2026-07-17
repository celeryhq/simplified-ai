# `smp api` — Assets API Reference

Workspaces, brand kits (V2), projects and project items, AI image generation,
assets, context documents, brand books, and agents.

## Capabilities at a Glance

- **Workspace** — `get-workspace`
- **Brand Kits** — list, create, build (canonical doc), get-V2, get-brand-book,
  import modules
- **Projects** — list, create, get, update, delete (soft), assign-agent-to-item
- **Project Items** — create, get, list, reorder, delete (soft), export
- **Context Documents** — list, create, update, delete, get-by-type
- **Documents** — `create-document` (long-form rendered)
- **AI Image Generation** — `generate-image`
- **Image Conversion** — `convert-image-format`
- **Assets** — `create-asset` (persistent workspace asset)
- **Async Task Results** — `get-task-result`

## Common Patterns

### Workspace info

```bash
smp api get-workspace
```

### Brand kits

```bash
smp api list-brand-kits
smp api create-brand-kit --title "Acme" --website "https://acme.com"
smp api get-brand-kit-v2 --brand-kit-id <uuid>            # canonical V2 document
smp api get-brand-book --brand-kit-id <uuid>              # rendered brand book
```

The `build-brand-kit` endpoint accepts a canonical BrandKitDocument body — the
same shape `get-brand-kit-v2` returns.

### Projects and project items

```bash
smp api create-project --primary-type ASSET --title "Q1 launch"
smp api list-projects --primary-type ASSET
smp api list-project-items --project-id <uuid>
smp api reorder-project-item --project-item-id <uuid> --order 3
smp api export-project-items --payload '{"project_item_ids": ["..."]}'
```

`primary-type` discriminates project polymorphism (e.g. `ASSET`, `DOCUMENT`).

### Context documents

Context documents are typed knowledge attached to a brand kit (e.g.
`brand_voice`, `icps`, `usps`, `content_pillars`, `marketing_strategy`,
`competitor_analysis`).

```bash
smp api list-context-documents --brand-kit-id <uuid>
smp api get-context-document-by-type \
  --brand-kit-id <uuid> --canonical-key brand_voice
smp api create-context-document \
  --brand-kit-id <uuid> --canonical-key brand_voice --content "..."
smp api update-context-document --context-document-id <uuid> --content "..."
```

Each canonical key is a singleton per brand kit — creating a second one with
the same key updates the existing record (and bumps its version).

### AI image generation

```bash
smp api generate-image --prompt "sunset over mountains, oil painting"
```

This returns a `task_id`; the middleware auto-polls until the result is ready.

### Task results

```bash
smp api get-task-result --task-id <task_uuid>
```

Used when manual polling is necessary (e.g. after a timeout). The middleware
already calls this for you on most async endpoints, so direct use is rare.

## Gotchas

**`primary-type` is required on project create/list** — use the same value on
both create and list so you don't get an empty page.

**Soft delete** — `delete-project` and `delete-project-item` are soft deletes,
not hard. The records remain queryable with the right flags.

**Context document singleton** — one document per `canonical_key` per brand kit.
A second create against the same key updates the existing one.

## Discovering Commands

```bash
smp api --help
smp api <command> --help
```
