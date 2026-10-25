# ThejaWebClone

Fused website-clone toolkit distilled from the Cursor chat **Website cloning skills** (Oct 2026).

It combines research findings, installed tools, MCPs used in that session, and the prompts that drove the work into one product:

| Mode | Purpose |
|------|---------|
| **mirror** | Recursive offline archive of public pages (Playwright-capable) |
| **snapshot** | AI-friendly page snapshot (assets + optional serve files) |
| **rewrite** | Rewrite CDN absolute URLs to local `cdn/` paths |
| **serve-proxy** | Serve local UI and reverse-proxy unknown routes to the live origin (core features while online) |
| **MCP** | Agent tools for all of the above |

> Honest limit from that chat: a commercial site with live APIs cannot be a perfect standalone 1:1 offline twin. Product pages can be archived; search/compare/dealers need either live proxy or a rebuilt backend. ThejaWebClone makes both paths explicit.

## Install

```powershell
cd C:\Users\ThejanaD\Projects\ThejaWebClone
py -3.11 -m pip install -e ".[render,mcp]"
py -3.11 -m playwright install chromium
```

Optional (full recursive mirror engine already used in the chat):

```powershell
py -3.11 -m pip install -e "C:\Users\ThejanaD\tools\website-downloader"
```

## CLI

```powershell
# Offline archive (wraps website-downloader if installed)
theja-webclone mirror --url https://example.com --out .\out\example --max-pages 200 --render-js

# Headed snapshot for SPA / CloudFront-protected homes
theja-webclone snapshot --url https://example.com --out .\out\snap --headed

# Fix absolute CDN links after a mirror
theja-webclone rewrite --root .\out\example --hosts trstatic.example.com,cdn.example.com

# Serve local UI + proxy APIs to origin
theja-webclone serve --root .\out\snap --port 8770 --origin https://example.com/
```

## Cursor MCP

Add to `~/.cursor/mcp.json`:

```json
"ThejaWebClone": {
  "command": "py",
  "args": ["-3.11", "-m", "theja_webclone.mcp_server"],
  "env": {
    "PYTHONIOENCODING": "utf-8",
    "THEJA_WEBCLONE_ROOT": "C:/Users/ThejanaD/Projects/ThejaWebClone"
  }
}
```

Tools: `twc_mirror`, `twc_snapshot`, `twc_rewrite`, `twc_serve`, `twc_status`, `twc_chat_lessons`.

## Cursor skill

Copy `skills/theja-webclone` to `~/.cursor/skills/theja-webclone`.

## Docs from the source chat

- [docs/CHAT-PROMPTS.md](docs/CHAT-PROMPTS.md) — every user prompt analysed
- [docs/MCP-FUSION.md](docs/MCP-FUSION.md) — MCPs/tools used and how they fuse
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — modes and failure modes (403, blank Edge, proxy timeout)

## Provenance

Built from chat id `782d09ea-95b5-4772-83f7-702400140b32` (“Website cloning skills”), GitHub user `thejanaloit`, targeting the TyreDekho learning case `https://tyres.cardekho.com/`.

License: MIT
