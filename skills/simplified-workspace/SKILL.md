---
name: simplified-workspace
description: Identify the authenticated Simplified user and workspace, inspect workspace settings, and discover or resolve accessible teamspaces safely. Use when the user asks "who am I," which Simplified workspace or teamspace is connected, what teamspaces they can access, which timezone or language applies, or asks to work in a named teamspace before using assets, brands, projects, social accounts, drafts, or other workspace-scoped resources.
---

# Simplified Workspace

Establish the correct Simplified identity and workspace context before operating on scoped resources. This operator resolves a teamspace once, then scopes every downstream MCP call explicitly.

## Workflow

1. Call `api_getWorkspaceInfo` for the authenticated user's identity, current workspace, workspace settings, and active teamspace membership.
2. If the user asks which teamspaces are available, return the teamspace names and numeric IDs. Use `api_listTeamspaces` when search, pagination, or expanded settings are needed.
3. If the user names a teamspace, search with `api_listTeamspaces`. Resolve to one exact numeric ID; do not guess when names or slugs are ambiguous.
4. If deeper workspace metadata is material, call `api_getWorkspace` with the workspace integer ID returned by `api_getWorkspaceInfo`.
5. When the user says “use,” “push this to,” “create in,” or “switch to” a teamspace, remember the resolved ID for the current task and pass `space_id: <numeric_id>` on every downstream Simplified tool call.
6. State the applied context before the downstream workflow: user, workspace, teamspace name and ID, and settings that affect the work.
7. Follow [references/teamspace-context.md](references/teamspace-context.md) before handing off to another Simplified skill.

## Identity and memory model

- Treat `api_getWorkspaceInfo` as Simplified's authoritative `whoami`; never infer identity from conversation memory.
- A credential belongs to one workspace. Teamspaces are sub-spaces inside that workspace, not alternate workspaces.
- Brand kits and their context documents are durable Simplified marketing memory. Workspace identity decides where that memory is read or written; this skill does not replace `manage-brand`.
- Conversation memory is not proof that a remote workspace, teamspace, account, asset, brand kit, project, or draft still exists or remains accessible. Re-read context when the user changes client, workspace, or teamspace, or before a consequential write when context is uncertain.
- Workspace settings such as timezone, language, and start of week are useful defaults. A connected social account's own timezone remains authoritative for scheduling that account.

## Teamspace safety

- Teamspace IDs are integers. Never pass a name, slug, alias, or fabricated value where a numeric ID is required.
- Hosted MCP scoping is stateless: `space_id` applies to one tool call. Carry the same resolved ID into every related read, write, poll, and follow-up call for the current task.
- It is fine to tell the user “Using Acme East (42)” after resolution, but do not imply the server persisted a global `teamspace:use` session.
- Do not reuse IDs for accounts, assets, brand kits, projects, items, drafts, or posts across teamspaces without re-listing them in the correctly scoped context.
- Never omit `space_id` midway through a scoped workflow. An omitted value uses the credential's default workspace context.
- Stop on `403`: the credential lacks access to that teamspace. Stop on `400`: the teamspace ID or scope is invalid. Never retry against a different space without the user's direction.

## Handoff contract

When another skill will continue the work, provide a compact context block:

- authenticated user;
- workspace name and integer ID;
- requested teamspace name and integer ID, or `default workspace context`;
- workspace timezone/language/start-of-week when relevant;
- the `space_id` that every downstream Simplified call must carry.

Do not treat context resolution as permission to generate credits, edit brand memory, mutate projects, schedule, queue, or publish.
