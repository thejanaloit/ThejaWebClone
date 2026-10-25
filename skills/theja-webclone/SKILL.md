---
name: theja-webclone
description: Fuse archive mirroring, Playwright snapshot, CDN URL rewrite, and live API proxy for website cloning. Use when the user wants offline copies, localhost serve, or core-feature proxy clones. Distilled from Theja Website cloning skills chat.
---

# ThejaWebClone

Installed package: `theja-webclone` (`py -3.11 -m theja_webclone.cli`).

## Decide mode first

1. **Archive** (many public pages offline) → `mirror` then `rewrite` then `serve` without origin.
2. **Core features 1:1 while online** → `snapshot --headed` then `serve --origin https://live-site/`.
3. Never promise perfect offline twin of API-backed commercial sites.

## Commands

```powershell
py -3.11 -m theja_webclone.cli status
py -3.11 -m theja_webclone.cli lessons
py -3.11 -m theja_webclone.cli mirror --url <URL> --out .\out\site --max-pages 200 --render-js
py -3.11 -m theja_webclone.cli snapshot --url <URL> --out .\out\snap --headed
py -3.11 -m theja_webclone.cli rewrite --root .\out\site --hosts cdn.example.com,static.example.com
py -3.11 -m theja_webclone.cli serve --root .\out\snap --port 8770 --origin https://example.com/
```

## Hard lessons

- Plain HTTP / headless may get **403** — use `--render-js` / headed.
- Blank browser + 200 status → hard refresh; check CDN rewrite.
- Proxy timeout must not double-write headers.
- Products optional; features need proxy or a rebuilt backend.

See repo `docs/CHAT-PROMPTS.md` and `docs/MCP-FUSION.md`.
