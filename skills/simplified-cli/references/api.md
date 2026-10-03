# `smp api` reference

Use live command help for installed-version details. `resourcetype` selects a project model (`Project` or `AdCreativeProject`); `primary_type` is a free-form category, not the polymorphic selector.

## Assets and generation

```bash
smp api:list-assets --search product --asset-type 0 --page 1
smp api:get-asset --id <asset-uuid>
smp api:create-asset --url "https://example.com/product.png" --name "Product"
smp api:list-image-models
smp api:generate-image --help
smp api:generate-video --help
```

Generate with a discovered model, explicit storage, and nested JSON `--parameters`; do not pass `--prompt` at the command top level. Example template:

```bash
smp api:generate-image --model <discovered-model-id> --storage asset --parameters '{"prompt":"A studio product photo","aspect_ratio":"4:5","count":1}'
```

Image `parameters.reference_images` accepts workspace asset IDs or URLs; video input slots take asset IDs. Check readiness before reuse. Follow [manage-assets](../../manage-assets/SKILL.md) for client byte-upload capability and persistence rules, and the generation skills for completion handling.

## Brand kits and knowledge

```bash
smp api:list-brand-kits --search Acme
smp api:create-brand-kit --title Acme
smp api:get-brand-kit --brand-id <brand-uuid>
smp api:build-brand-kit --brand-id <brand-uuid> --brand '{"description":"Approved brand description","website":"https://example.com"}'
smp api:list-context-documents --brand-id <brand-uuid>
smp api:get-context-document-by-type --brand-id <brand-uuid> --context-type brand_voice
smp api:create-context-document --brand-id <brand-uuid> --doc-type brand_voice --name "Brand voice" --content "Approved voice guidance"
smp api:update-context-document --brand-id <brand-uuid> --document-link-id <link-uuid> --content "Updated approved guidance"
```

Creating a duplicate predefined context type fails; retrieve/update its existing **document-link ID** rather than assuming create is an upsert. Canonical content pillars and ICPs use structured `build-brand-kit` fields; the content-pillars context adapter is a read view, not a KnowledgeDoc write target. See [manage-brand](../../manage-brand/SKILL.md).

## Marketing projects

```bash
smp api:list-projects --resourcetype Project --search Launch
smp api:create-project --resourcetype Project --title Launch --primary-type campaign
smp api:list-project-items --resourcetype Project --parent-lookup-project-id <project-uuid>
smp api:create-project-item --resourcetype Project --parent-lookup-project-id <project-uuid> --title "Hero image" --data '{"assets":[],"flags":{}}'
smp api:reorder-project-item --resourcetype Project --parent-lookup-project-id <project-uuid> --id <item-uuid> --position 3
smp api:export-project-items --resourcetype Project --id <project-uuid> --partner-id <verified-partner-id> --item-ids '["<item-uuid>"]'
```

Keep the same model selector on list/get/create/update/delete. Read current project/item data and merge intended changes before sending a replacement data object. Export and execution-agent assignment have external consequences and need a concrete user-authorized target. See [manage-projects](../../manage-projects/SKILL.md).
