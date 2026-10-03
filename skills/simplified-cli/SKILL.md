---
name: simplified-cli
description: Use when the user explicitly wants the smp command line, shell scripts, JSON pipelines, local Simplified API automation, or a local smp serve MCP server. For conversational tasks through a hosted connector, use the relevant platform skill instead.
---

# Simplified CLI

`smp` is supplied by the Python `simplified-apikit` package. It generates commands from the same OpenAPI specs and runs them through MCP middleware, so request validation and hooks apply across CLI and connector calls. It is different from the npm `simplified` CLI; do not mix their commands or credentials.

## Setup and scope

Use your team's supported package source to install `simplified-apikit`. Confirm `smp --version` and command help before scripting. Local CLI calls require configured credentials; hosted app OAuth does not automatically populate local CLI environment variables.

```bash
smp --version
smp --help
smp api --help
```

Set `SMP_TOKEN` privately in the environment. API keys use their bound workspace; DRF tokens also require numeric `SMP_WORKSPACE`. Set numeric `SMP_SPACE` only after resolving the user's chosen teamspace. Omit `SMP_URL` for production; use overrides only for an explicitly selected environment. Never print credentials or put them into user-facing commands/logs.

Root options such as `--space`, `--workspace`, and `--raw` precede the namespace. Both `smp api list-assets` and `smp api:list-assets` work. JSON options take a single shell-quoted JSON value.

```bash
smp --raw api:list-assets --search car --asset-type 0 --page 1
smp api:get-workspace-info
smp api:list-teamspaces
```

Use the same resolved scope throughout. Do not guess tenant IDs or select the first board/account/member just to make a script run.

## Choose the namespace

| Namespace | Use | Reference |
|---|---|---|
| `api` | Workspace, brand context, assets, AI generation, marketing projects, comments | [API](references/api.md) |
| `pm` | Boards, statuses, tasks, dependencies, assignments | [PM](references/pm.md) |
| `social` | Accounts, drafts, scheduling, reviews, analytics | [Social](references/social.md) |
| `media` | Image/video editing and transcription | [Media](references/media.md) |
| `flows`, `agents` | Workflow and agent automation | Current namespace help and the matching automation skill |
| `notify` | Requested notifications | Current command help |

Comments are `smp api:list-comments` / `smp api:add-comment`, not a separate comments namespace. See [comments](references/comments.md).

## Execute and verify

Read the target state, resolve IDs, then execute the user-authorized operation. Use `--help` for the exact required flags. Keep returned IDs for follow-up; verify writes using direct reads. For partial batches, report successful IDs and failed steps without repeating successful creates.

Current image/video generation waits for completion. Pending/timeout responses require continuation using the actual job identifiers, not a duplicate paid request. Video submission task IDs do not establish render completion. Other tools may have different task-result contracts.

Default output is formatted JSON; root `--raw` makes it suitable for JSON parsers. Read the actual envelope before writing a jq/path expression. Pagination limits and defaults vary by endpoint; retain filters/scope and follow returned pagination metadata.

Generation consumes credits and social scheduling/queueing can publish content. Preserve explicit authorization already given for the concrete operation. Planning is not permission to run it.

## Local MCP server

```bash
smp serve
smp serve --profile public
smp serve --transport http --port 9000 --profile social
```

`full` is the default local profile. Hosted connector tools/profile are deployed separately; local full access does not prove a hosted client has the same tools. `flows`, `agents`, and the generic passthrough require an automation/full surface. See [client setup](../../docs/CLIENTS.md).
