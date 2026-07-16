# Workspace and teamspace context

## Scope hierarchy

```text
authenticated user
└── one workspace bound to the credential
    ├── default workspace context
    └── zero or more accessible teamspaces (Spaces)
```

`api_getWorkspaceInfo` is the primary identity call. It returns the current user, workspace, workspace settings, and active teamspaces. `api_listTeamspaces` supports focused search and pagination. `api_getWorkspace` reads richer metadata for the known workspace integer ID.

## CLI versus hosted MCP

The Simplified CLI can persist an active teamspace locally and sends its numeric ID as the `Space` header. Its precedence is one-off command flag, environment override, saved local context, then default workspace.

Hosted MCP serves many independent users and requests. Server-side mutable teamspace session memory would risk leaking scope between requests, so the connector remains stateless. Every tool accepts optional `space_id`; middleware forwards it upstream as Simplified's canonical `Space` header for that operation, including polls and follow-ups, then clears it.

## Safe resolution

1. Read `api_getWorkspaceInfo`.
2. Match the requested teamspace against returned name and slug. Use `api_listTeamspaces(search=...)` when necessary.
3. If zero matches, report that it is not accessible. If multiple matches remain, ask the user which one; include names and numeric IDs.
4. Preserve the exact numeric ID in the handoff.
5. Pass `space_id: <id>` on every downstream Simplified call in the task. Do not pass it only on the first call.

Never infer that the default workspace is the user's intended teamspace. Never substitute another accessible teamspace after a `403`.

## Resource boundaries

Assume these identifiers are context-bound unless the API explicitly proves otherwise:

- connected social account IDs;
- asset IDs and upload registrations;
- brand kit and context-document IDs;
- project and project-item IDs;
- draft, post, tag, and review-bundle IDs.

After a context change, re-list resources with the new `space_id` instead of carrying IDs from the previous context.

## Marketing defaults

Workspace timezone, language, and start-of-week can guide calendar presentation and planning. For live social scheduling, use the selected connected account's timezone and surface any conflict with the workspace default. Brand memory belongs in approved brand-kit context documents, not unverified conversational assumptions.
