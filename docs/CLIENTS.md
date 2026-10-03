# Connect Simplified to your assistant

The hosted endpoint is `https://apikit.simplified.com/mcp`. It uses OAuth: sign in to Simplified and authorize the connection. Local CLI credentials and hosted connector authorization are different setup paths.

## Choose your client

| Client | Tool connection | Skill instructions |
|---|---|---|
| Claude Code | Install this plugin, or add the HTTP MCP server | Plugin or a compatible local skill installation |
| Codex | Install an available Simplified plugin, or add the MCP server | Plugin or local skill installation |
| ChatGPT | Simplified app when available, or a custom MCP app where permitted | Delivered app skills where supported; this repo is not automatically loaded by a custom connection |
| Claude web/desktop | Remote connector where your plan/client supports it | Client-dependent; a connector does not automatically install local skills |
| Cursor/other MCP clients | Client-specific remote HTTP MCP setup with OAuth | Local skills only if the client supports them |

Skills describe workflows. MCP exposes tools. Neither a skill ZIP nor a config file grants access to an account.

## Claude Code

For plugin installation, use the [README](../README.md). For tools without the plugin:

```bash
claude mcp add --transport http simplified https://apikit.simplified.com/mcp
```

Open `/mcp` in Claude Code and complete authentication. Use `claude mcp list` to check connection state. Choose project/user scope according to your needs; see [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp).

## Codex

For a direct CLI connection:

```bash
codex mcp add simplified --url https://apikit.simplified.com/mcp
codex mcp login simplified
codex mcp list
```

Codex uses TOML configuration, not the `mcpServers` JSON wrapper:

```toml
[mcp_servers.simplified]
url = "https://apikit.simplified.com/mcp"
```

Use the supported plugin/connector settings for your Codex desktop installation when connecting through its UI. CLI configuration and plugin installation are alternatives, not instructions to create duplicate connections. See [Codex MCP documentation](https://developers.openai.com/codex/mcp).

## ChatGPT

If Simplified is listed in your Apps interface, connect it and complete sign-in. For custom MCP apps, use the account/workspace settings available to you, enter the endpoint above, choose OAuth, and complete tool scanning/authorization. Developer mode, custom-app creation, and tool permissions depend on your plan and workspace administrator.

Use [OpenAI's current custom MCP app instructions](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) for exact UI and eligibility. Do not assume app-directory listing, custom-app access, or local-shell/file-upload capabilities simply because this repository exists.

## Claude web/desktop and other clients

Use the client's remote connector interface when supported, enter the endpoint, and authorize. A desktop client that supports only local stdio servers needs a supported remote-HTTP setup or local apikit server instead; a remote JSON entry is not universal across clients.

For clients that explicitly accept this shape (including Claude Code project configuration):

```json
{
  "mcpServers": {
    "simplified": {
      "type": "http",
      "url": "https://apikit.simplified.com/mcp"
    }
  }
}
```

Consult your client's documentation for its file location, transport name, OAuth support, and permission settings. Do not copy this JSON into Codex TOML.

## Verify before creating content

Ask the assistant to identify the Simplified workspace with `api_getWorkspaceInfo`, then list available image/video models or assets. These are read-only checks. Resolve a named teamspace with `api_listTeamspaces`; carry its numeric `space_id` into every related operation.

Tool identifiers may have a client-added prefix. Match canonical operations such as `api_listAssets` and `api_generateImage` to the actual exposed tools and read their schemas.

| Symptom | Next step |
|---|---|
| No Simplified tools | Check connector installation, enablement, and authorization |
| 401/Unauthorized | Reauthorize in the client; stop dependent calls until authorized |
| Asset discovery missing | Refresh the exposed tool list/reconnect; deployment/profile may not yet include `api_listAssets` |
| Asset not found | Check UUID and workspace/teamspace; do not substitute a different client's asset |
| Attachment cannot be uploaded | Client needs byte access and an HTTP PUT capability; otherwise upload through Simplified or provide a downloadable URL |
| New skill installed, old tool schema | Skills and server releases are independent; refreshing skills does not deploy tools |

The [media walkthrough](MEDIA.md) uses the same operations in all clients. What differs is authorization, attachment transfer, tool exposure, and how results are shown.
