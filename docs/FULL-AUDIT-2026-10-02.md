# Full skill audit — October 2, 2026

Reviewed all 18 skills, all supporting Markdown references and agent metadata. Compared tool names, fields, IDs, lifecycle behavior, model/asset handoffs, profiles/resources, scoping, and examples against the current local `simplified-apikit` specs, middleware/hooks, generated tool/CLI schemas, and selected backend code. Each domain was read by its assigned reviewer; root reviewed findings, edits, and cross-skill consistency.

## Coverage

| Skill | Audited behavior |
|---|---|
| `manage-assets` | Listing/search, pagination, attachment capability, readiness, asset handoff |
| `generate-image` | Normalized references, current model discovery, storage and result envelopes |
| `generate-video` | UUID inputs, middleware completion, failure/timeout continuation |
| `simplified-workspace` | Membership authority, stateless scope, timezone/error interpretation |
| `simplified-social` | Account ID types, accountless drafting, lifecycle IDs, PDF/video media, reviews |
| `manage-brand` | Structured ICP/pillar writes, singleton context/link IDs, evidence and asset handoff |
| `manage-projects` | CRUD argument routing, merged data updates, PM distinction, export/execution scope |
| `simplified-project-management` | Status migration vs deletion, subtasks, assignee/tag IDs, direct verification |
| `simplified-cli` | All five references checked; corrected command groups/flags/actions and removed unsafe selection scripts |
| `simplified-workflows` | Automation connection, resource scope, graph preservation, approval/restart/input contracts |
| `social-content-planner` | Scope, authorized drafts, asset sourcing, partial-batch recovery |
| `cross-platform-campaign` | Scope, asset reuse/intake, channel adaptation, partial-batch recovery |
| `content-repurposer` | Source-access limits, grounded claims, scope, attachment and draft handoffs |
| `evergreen-content-engine` | Scope, reusable assets, durable content quality, monitoring vs saved plans |
| `local-business-marketing` | Location scope, verified operations, media intake and platform contracts |
| `creative-testing` | Account discovery for drafts, explicit save intent, controlled variables and measurement limits |
| `social-performance-analyst` | Completed-day windows, coverage/status, timezone, scoped analytics and interpretation |
| `campaign-review` | Append operation, supported edit fields, accountless coverage, explicit publication handoff |

## Material corrections

- Social posting uses string account IDs under strict request validation; analytics uses numeric single-account IDs, and listing endpoints can use CSV. Asset IDs are UUIDs and must not be conflated with any account or draft identifier.
- Empty connected-account results no longer block accountless drafts. Scheduling/queueing still needs accounts and user-authorized publishing intent.
- Review append is supported when exposed; draft update does not support reassignment or arbitrary platform-settings changes. “All drafts” is qualified where listing cannot establish accountless coverage.
- Teamspace resolution uses accessible membership discovery, not whoami visibility. Scope is carried on every downstream call, including media and review handoffs.
- PM status migration does not itself delete the source status; subtasks need explicit search inclusion. User IDs and tag names use their actual write shapes.
- Canonical pillars and ICPs use structured brand-build arrays. A rendered pillar context view has no editable KnowledgeDoc UUID.
- Project updates preserve complete merged data and correct model/parent/item routing; marketing metadata is not native PM ownership/dependencies.
- Workflow resources cannot carry a per-call space ID. Scoped tool alternatives, automation connection requirements, approval field mapping, restart/input semantics, and duplicate-run risks are explicit.
- CLI references no longer advertise removed commands, a comments namespace, top-level image prompt, publish action, wrong brand/context/project flags, or selecting arbitrary first results. The new checker guards documented tool names and literal command contracts against current source.

## Verification and limits

Ran the existing document/catalog checks, the new source-contract checker, skill/metadata YAML and local-link checks, and ChatGPT bundle packaging. All 18 skills have valid frontmatter and Codex metadata. Corrected a private submission-file link and bundle output-path handling, then verified packaging both inside and outside the repository. Negative checker probes rejected unknown tools, wrong flags, missing required arguments, and an invalid `publish` action. Earlier baseline CLI checking exposed 25 genuine name/flag errors plus a checker false positive on `--help`, which was corrected.

Domain scenario documents capture expected behavior for realistic requests. Reviews and scenario reasoning were read-only/static; they are not empirical assistant traces or authenticated end-to-end connector tests. No customer records were read, credits spent, social content published, or external messages sent. Historical inventory snapshots remain dated evidence and were not relabeled as live verification.

## Initial source conflicts

The initial audit identified these upstream issues. The follow-up section below records the fixes and the runtime checks that remain; this list preserves the original findings:

1. Apikit's social publish guide says queue timing is the next slot; backend serializer documentation says ASAP. Skills report service-determined timing and avoid an immediate-delivery promise. Scheduling timezone prose also conflicts across references; resolve actual interpretation before publishing at a promised wall-clock time.
2. `workflow-run-control.md` suggests restarting for corrected input, but restart preserves original input. Skills use a new start for corrected input, and `useLatestDefinitions: true` when restarting against a fixed definition.
3. `mcp_prompts.py` contains pre-build approval and an automatic live-test step; skills preserve existing user authorization and do not run an unsolicited test with external effects.
4. Workflow save and publish descriptions disagree about validation timing. Skills inspect errors from both instead of assuming save cannot validate.
5. Brand-build prose omits `icps` and overstates GET/POST identity despite write-only structured inputs. Skills follow the actual schema.
6. The legacy raw-image I/O eval harness still needs a separate current-route/MCP update. Its old golden outputs cannot establish today's integration behavior.

Client setup distinguishes skills from tools and follows official client documentation. A skill update cannot grant permissions, deploy a tool, or prove app-directory availability. Hosted tool exposure and paid/live behavior still need authenticated release verification.

## Follow-up fixes — October 2, 2026

The apikit source branch `codex/skill-audit-source-fixes` now aligns workflow restart/input and approval-field guidance with the schemas, distinguishes save-shape validation from publish compilation, adds ICP/write-only brand semantics, and removes automatic test execution and repeated build-approval requirements from MCP prompts. Social guidance no longer promises a queue slot or assumes workspace timezone is the creation parser's timezone. The publishing service's actual queue/timezone behavior still needs service-level confirmation.

Replaced the legacy raw HTTP eval harness with canonical MCP calls. Defaults are read-only; drafts and credit-consuming generation are explicit options. Generation reuses returned completed/pending jobs, fields are discovered for the explicitly selected model, completed-month analytics dates are inclusive, and cleanup uses typed draft/group IDs with visible errors. Generated assets are retained and identified. Nine offline regressions cover these failure modes.

Read-only checks through the connected Simplified app succeeded for image model discovery, image field discovery, video model discovery, video field discovery, and an empty asset search with the expected pagination envelope. These are separate from harness execution: its shell OAuth token was not configured. No generation credits were spent, drafts created, or posts published during these checks. Paid generation, attachment upload, and cross-client end-to-end traces remain release-verification work, not claimed results.

Final verification: 269 apikit tests passed; 9 offline MCP-harness regressions passed; 21 skill/catalog checks and the sample-trace grader passed; 64 CLI examples matched current source; the 16-skill hosted bundle built successfully. The sample trace is a fixture, not a new live agent run. Five live read-only connector checks passed.
