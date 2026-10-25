# Architecture

## Modes

### 1. Archive (`mirror`)

Recursive public-page download. Prefer installed `website-downloader` (proven on TyreDekho with `--render-js`). Falls back to a thin Playwright single-start crawl if missing.

Failure modes handled:

- HTTP **403** without browser → enable `--render-js` / headed Chromium
- Sitemap **403** → seed from already-mirrored HTML links
- Missing CDN CSS → run `rewrite`

### 2. Snapshot (`snapshot`)

One (or few) page captures for SPA shells. Headed Chromium bypasses some CloudFront bot blocks (learned when headless got 923-byte error HTML).

### 3. Rewrite (`rewrite`)

Replace `https://cdn-host/...` with `cdn/cdn-host/...` across HTML so offline CSS/JS load. Inject main stylesheet link early to avoid blank paint while deferred JS runs.

### 4. Feature proxy (`serve`)

Serve local UI; forward missing paths to `--origin`. This is the **core features** path: search/compare/dealers can work while online.

Hardening from chat:

- Proxy timeout must not call `writeHead` after headers sent (fixed in TyreDekho `server.js` and mirrored here)

## What “1:1” means here

| Claim | Supported? |
|-------|------------|
| Visual shell of key pages | Yes (snapshot/mirror + rewrite) |
| Offline browsing of saved pages | Yes (archive) |
| Search / live filters / dealers without internet | No |
| Core features while online via proxy | Best-effort yes |
| Perfect offline twin of entire commercial site | No |

## Ports used in the chat

- `8765` — static archive of TyreDekho
- `8770` — feature snapshot + live proxy
