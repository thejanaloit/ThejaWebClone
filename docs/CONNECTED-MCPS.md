# Connected MCP inventory (fused into ThejaWebClone)

Snapshot of every MCP registered in `~/.cursor/mcp.json` when ThejaWebClone was extended (38 servers). Secrets are redacted.

Machine-readable copy:

- `data/connected-mcps.json`
- `src/theja_webclone/data/connected-mcps.json`

## MCP tools

| Tool | Purpose |
|------|---------|
| `twc_list_connected_mcps` | Names + roles |
| `twc_get_connected_mcp` | One server’s sanitized install details |
| `twc_export_connected_mcps` | Full JSON (`refresh_from_cursor=true` re-reads live Cursor config) |

CLI:

```powershell
py -3.11 -m theja_webclone.cli mcps
py -3.11 -m theja_webclone.cli mcps --name omniroute
py -3.11 -m theja_webclone.cli mcps --refresh
```

## Used directly in the Website cloning skills chat

| MCP | Use |
|-----|-----|
| theja-token-manager | `ttm_vault` discovery |
| omniroute | GitHub skills search |
| unbrowse | scrape namespace (auth stub) |
| cursor-ide-browser | localhost visual proof (Cursor native) |
| ThejaWebClone | this fused product |

All other listed servers were **connected in Cursor** during that work and are therefore inventoried here so agents can discover install paths/commands without guessing.
