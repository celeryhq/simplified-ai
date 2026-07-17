---
name: manage-projects
description: Organize marketing work in Simplified projects and project items. Use when the user asks to create or inspect a marketing project, campaign workspace, content production board, launch checklist, editorial pipeline, or deliverable list; add, retrieve, prioritize, reorder, assign, export, or remove project items; or turn an approved content plan into trackable work.
---

# Manage Projects

Translate a marketing plan into accountable, sequenced work without confusing project organization with publishing authorization.

## Guardrails

- Inspect before mutating. Reuse an existing project when it clearly matches the user's initiative.
- Use the same `resourcetype` for every operation on a project. Prefer `Project` for ordinary marketing work and `AdCreativeProject` only for specialized ad-creative projects.
- Do not invent project, item, partner, or agent IDs. Resolve them from tool results or user-provided values.
- Creating a project or item does not authorize assigning an agent, exporting content, publishing content, or deleting records.
- Confirm the target and consequences before soft-deleting a project/item, assigning an execution agent, or exporting to a partner integration.
- Dates must be realistic and internally ordered. Surface impossible dependencies or missing owners rather than silently compressing the plan.

## Workflow

1. Define the initiative: outcome, scope, deadline, deliverables, channels, approval points, owners, dependencies, and definition of done.
2. Call `api_listProjects` with the chosen `resourcetype` and search term. Reuse a unique match or show choices when several projects could apply.
3. If creation is requested, call `api_createProject` with a clear title, concise outcome-based description, and only supported structured data. Preserve the returned project ID.
4. Call `api_listProjectItems` before adding work to understand existing deliverables and avoid duplicates.
5. Convert the plan into outcome-oriented items. Each item should have one deliverable, owner or owner-needed flag, status, priority, start/due date, dependencies in the description or data, and a measurable definition of done.
6. Call `api_createProjectItem` for authorized items. Use `data.assets` for known permanent asset UUIDs; never store signed URLs as durable references.
7. Use `api_reorderProjectItem` only when the user requests or approves a new sequence. Use `api_assignAgentToItem` only with a resolved agent ID and explicit execution scope.
8. Use `api_exportProjectItems` only after confirming the partner integration and exact item IDs. Report export initiation separately from export completion.

Read [references/project-operations.md](references/project-operations.md) for field and lifecycle rules.

## Marketing Operations Standard

- Organize work around deliverables and approvals, not vague activity such as “work on social.”
- Separate strategy, copy, creative, channel adaptation, compliance, review, scheduling, and reporting when different owners or gates apply.
- Put the decision deadline before the publish deadline. Include contingency time for legal, customer, or executive review where relevant.
- Use priorities to express business consequence and sequencing, not urgency theater.
- Do not create a bloated project for a one-step request; perform the direct task unless the user wants tracking.

## Output

Lead with project status and the critical path. Then report created or changed items, owners, dates, dependencies, approval gates, IDs needed for follow-up, and any action awaiting confirmation.
