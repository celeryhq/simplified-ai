---
name: manage-projects
description: Organize creative marketing projects and their deliverable items in Simplified, including collections, ordering, asset handoffs, assignments, and exports. Use for marketing project/item records. For Kanban boards, tasks, subtasks, statuses, and native dependencies, use simplified-project-management.
---

# Manage Projects

Translate a marketing plan into accountable, sequenced work without confusing project organization with publishing authorization.

## Guardrails

- Inspect before mutating. Reuse an existing project when it clearly matches the user's initiative.
- Use the same `resourcetype` for every operation on a project. Prefer `Project` for ordinary marketing work and `AdCreativeProject` only for specialized ad-creative projects.
- Do not invent project, item, partner, or agent IDs. Resolve them from tool results or user-provided values.
- Creating a project or item does not authorize assigning an agent, exporting content, publishing content, or deleting records.
- Resolve the exact target and consequences before soft-deleting, assigning an execution agent, or exporting. A user request that specifies the action and scope is authorization; ask only when the target, destination, or execution scope is unclear.
- Dates must be realistic and internally ordered. Surface impossible dependencies or missing owners rather than silently compressing the plan.

## Workflow

1. Define the initiative: outcome, scope, deadline, deliverables, channels, approval points, owners, dependencies, and definition of done.
2. Resolve named or uncertain workspace/teamspace scope with `simplified-workspace` and carry numeric `space_id` on every call. For Kanban boards, team task ownership, subtasks, or native dependencies, use `simplified-project-management` and its `pm_*` tools; creative project items are a different resource. Call `api_listProjects` with the chosen `resourcetype` and `search`. Reuse a verified unique match or show choices when several projects could apply. `expand: "items"` can include deliverables and avoid separate listings.
3. If creation is requested, call `api_createProject` with a clear title, concise outcome-based description, and only supported structured data. Preserve the returned project ID.
4. Inspect the returned items, or call `api_listProjectItems` on an existing project, before adding work to avoid duplicates. A newly created empty project does not need another inventory call.
5. Convert the plan into outcome-oriented items. Each item should have one deliverable, owner or owner-needed flag, status, priority, start/due date, dependencies in the description or data, and a measurable definition of done.
6. Call `api_createProjectItem` for authorized items. Use `data.assets` for known permanent asset UUIDs; never store signed URLs as durable references.
7. Revise existing work with `api_updateProject` or `api_updateProjectItem`; read first and send the complete merged `data` object when changing it. Use `api_reorderProjectItem` within the requested organization scope. Use `api_assignAgentToItem` only with a resolved agent UUID and authorized execution scope; Resolve agents through the separately configured automation/full connection when enabled; follow `simplified-workflows` for discovery and capability checks. Assignment alone does not establish completion.
8. Use `api_exportProjectItems` with the resolved numeric `partner_id` and exact `item_ids` within the authorized destination scope. There is no dedicated partner-discovery tool in the current public schema; use a known configured ID or verified supported discovery, and ask when the destination is unresolved. Report export initiation separately from completion.

Read [references/project-operations.md](references/project-operations.md) for field and lifecycle rules.

## Marketing Operations Standard

- Organize work around deliverables and approvals, not vague activity such as “work on social.”
- Separate strategy, copy, creative, channel adaptation, compliance, review, scheduling, and reporting when different owners or gates apply.
- Put the decision deadline before the publish deadline. Include contingency time for legal, customer, or executive review where relevant.
- Use priorities to express business consequence and sequencing, not urgency theater.
- Do not create a bloated project for a one-step request; perform the direct task unless the user wants tracking.

## Output

Lead with project status and the critical path. Then report created or changed items, owners, dates, dependencies, approval gates, IDs needed for follow-up, and any action awaiting confirmation.
