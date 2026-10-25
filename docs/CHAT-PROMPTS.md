# Chat prompt analysis — Website cloning skills

Source conversation: local Cursor chat **Website cloning skills**  
id: `782d09ea-95b5-4772-83f7-702400140b32`  
Window: 2026-10-23 → 2026-10-25

## Prompt timeline (intent → outcome)

| # | User prompt (condensed) | Intent class | What we did | Lesson locked into ThejaWebClone |
|---|-------------------------|--------------|-------------|----------------------------------|
| 1 | Deep research for skill/MCP with full exact site cloning | Discovery | Searched installed skills, TTM vault, MCP catalog, GitHub, web | Prefer **behavior inside code**, not repo title |
| 2 | Show highest-star MCP/skill | Ranking | Live `gh api` star counts | Highest-star MCP was `pskill9/website-downloader` (~157★); not the newest |
| 3 | Latest update; AI can copy entire web; find from **inside** the work | Discovery (anti-name-bias) | Inspected READMEs/`SKILL.md`/crawler modules | Chose `webclone-skill` (AI rebuild) + `PKHarsimran/website-downloader` (full crawl) |
| 4 | Install those two “MCPs” | Install | Cloned + built; clarified they are **CLI/skill**, not MCP | ThejaWebClone **adds** a real MCP wrapper |
| 5 | Are those working? | Verify | Smoke-tested `example.com` | Always smoke-test before a big target |
| 6 | 100% clone `tyres.cardekho.com` on localhost | Execute | Playwright mirror (plain HTTP 403), serve `:8765` | CloudFront/bot walls need headed/render-js |
| 7 | Show what you did | Recap | Summary of research → install → clone | Keep provenance docs |
| 8 | (blank / refused-to-connect screenshots) | Recover | Restart server; rewrite CDN URLs; Ctrl+F5 | Offline CSS must be **local**; Edge caches blanks |
| 9 | Larger crawl / full entire clone | Scale | Seeds from HTML + up to 5000 pages | Sitemap can be 403; seed from discovered links |
| 10 | Will all pages appear? | Expectation | Honest: up to cap, not every live URL | Document caps in CLI help |
| 11 | Perfect 1:1 copy? | Expectation | No — APIs/backend can’t be mirrored as files | Split **archive** vs **feature-proxy** modes |
| 12 | Products not needed; core features 1:1 | Pivot | Stopped product crawl; snapshot + live API proxy `:8770` | `serve-proxy` is the feature path |
| 13 | Fuse chat MCPs + prompts into ThejaWebClone and push GitHub | Productize | This repository | Single fused toolkit + MCP + skill |

## Intent clusters

1. **Find** — discover real clone capability (stars, recency, code truth).
2. **Install / verify** — make tools run on Windows (Python 3.11, not 3.14).
3. **Execute** — mirror a hard target and show localhost.
4. **Recover** — server down, blank page, CDN paths.
5. **Scale vs reality** — “all pages” vs “core features”.
6. **Productize** — fuse into ThejaWebClone and publish.

## Prompt patterns ThejaWebClone agents should recognize

- “full exact clone / 100% / perfect 1:1” → ask: **archive** or **features**?
- “show on localhost” → serve after rewrite; give hard-refresh instructions.
- “highest stars” ≠ “best for SPAs” (wget MCP vs Playwright crawler).
- “install as MCP” when repo is only a skill/CLI → wrap with MCP (this project).
