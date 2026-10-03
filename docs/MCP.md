# Simplified MCP reference

The hosted connector provides tools; this repository provides instructions for using them. Start with [client setup](CLIENTS.md) or [the media walkthrough](MEDIA.md).

## Connection and tool discovery

The declared endpoint is `https://apikit.simplified.com/mcp`, authenticated through OAuth. Tools exposed there depend on the deployed release/profile and client permissions. Inspect the current client's tools and schemas before making calls. Inventory JSON files under `evals/` are dated captures, not promises that today's server matches them.

Client prefixes differ, but canonical names such as `api_listAssets`, `api_generateImage`, and `social_createSocialMediaPost` identify the operations. Local `smp` commands are generated from the same OpenAPI operations.

## Assets and generation

| Operation | Purpose |
|---|---|
| `api_listAssets` | List assets or search names/tags; optional `search`, `asset_type`, `page`, `page_size` |
| `api_getAsset` | Inspect a known UUID, processing state, and fresh URLs |
| `api_createAsset` | Import a downloadable URL into the workspace |
| `api_signAssetUpload` → client PUT → `api_registerAsset` | Upload local bytes through a capable client |
| `api_listImageModels`, `api_getImageModelFields` | Discover image models/options where exposed |
| `api_listVideoModels`, `api_getVideoModelFields` | Discover video models/options where exposed |
| `api_getModelFields` | Alternative discovery operation for model/capability metadata |
| `api_generateImage` | Create/edit using nested `parameters`, normalized `reference_images`, explicit storage |
| `api_generateVideo` | Generate motion with normalized slots containing asset UUIDs |
| `api_getVideoVariation` | Continue a returned non-terminal variation when required |

Use the generation tool schema for public input names. Catalogs help choose model support/options; provider-specific descriptors do not override normalized inputs. Image references accept workspace UUIDs or HTTP(S) URLs; video input slots take workspace UUIDs.

Asset search is not semantic/visual search or folder-name search. It cannot enumerate a named folder. Listing without search can omit assets inside folders. Continue pages with unchanged filters/scope for all matching results.

## Workspace and teamspace

`api_getWorkspaceInfo` identifies the credential-bound workspace. Resolve accessible teamspaces through `api_listTeamspaces`. Use the exact numeric `space_id` on every downstream read, generation, draft, continuation, and follow-up for that scoped task. Omitting it returns to the credential's default context. Never mix IDs between clients/workspaces.

## Local toolkit and profiles

Install `simplified-apikit` using your Python package tooling. `smp --help` and individual command help describe the installed version. Local auth uses its configured token/workspace; it is separate from hosted OAuth.

```bash
smp api:list-assets --search car --asset-type 0 --page 1
smp api:get-asset --id <asset-uuid>
smp api:generate-image --help
smp api:generate-video --help
smp serve --profile public
```

Current source profiles:

| Profile | Intended surface |
|---|---|
| `public` | Workspace/assets/generation, projects/tasks, social, media, notifications |
| `social` | Curated social operations plus identity, assets, credits, and brand lookup |
| `automation` | Workflow/agent-building namespaces and generic passthrough |
| `full` | All registered namespaces; default for local toolkit |

When multiple profiles are mounted by the toolkit, `public` owns `/mcp`; others use `/social/mcp`, `/automation/mcp`, and `/full/mcp`. This describes source routing, not proof that every path is deployed publicly. Use the declared connector for this plugin. Automation-only skills require their own compatible connection; the ChatGPT bundle excludes them.

The older `mcp` local profile and July tool counts in historical eval captures are not the current source profile definition.

## Completion, errors, and result links

Current apikit waits for image tasks and video variation completion. Do not poll while the generation call is active. If it returns non-terminal or times out, inspect the returned identifiers and use the documented continuation tool. Video submission `task_id` tracks dispatch, not render completion; never use it to establish a completed video. See [video completion](../skills/generate-video/references/models-and-polling.md).

Keep permanent asset IDs for reuse. File links can expire; call `api_getAsset` for fresh ones. On failure, preserve the actual tool/provider message. A timed-out paid job may still be running; do not silently submit another one. Reauthorize a failed OAuth connection before resuming dependent calls.

Creating/importing assets and drafting posts are separate from publishing authorization. Use `action: "draft"` for draft requests; scheduling and queueing require explicit approval.

## Contributor verification

Run [contract/bundle checks](../evals/README.md). Validate examples against the current apikit OpenAPI specs. Keep historical hosted snapshots intact and record their date; update live inventory only from authenticated discovery. A local spec comparison, mock request, or agent reading exercise is not a live integration test.
