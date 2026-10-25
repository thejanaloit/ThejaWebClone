# MCP / tool fusion map

Everything this chat actually used (or researched as clone capability), fused into ThejaWebClone.

## Connected / called in-session

| Namespace / tool | Role in chat | Fused into ThejaWebClone as |
|------------------|--------------|-----------------------------|
| `user-theja-token-manager` → `ttm_vault` | Search stashed MCP tools for clone | Documented; vault was empty for clone tools |
| `cursor` → `WebSearch` / `WebFetch` | Find HTTrack MCP, star rankings, latest skills | Research method in docs; not required at runtime |
| `user-omniroute` → `omniroute_github_skills_search` | Skill repo search (rate-limited) | Optional discovery path |
| `cursor-ide-browser` → navigate / CDP / screenshots | Prove localhost clone visually | Agents still use browser MCP separately; TWC serves URLs |
| `cursor` → `SearchConversations` | Re-find this chat for productization | Provenance only |
| Shell + `gh` | Clone repos, stars, create/push this project | Dev workflow |

## External engines researched / installed locally

| Engine | Stars / freshness (at research time) | Role |
|--------|--------------------------------------|------|
| `pskill9/website-downloader` | Highest-star **MCP** wget mirror (~157★) | Reference for MCP-shaped mirror API |
| `PKHarsimran/website-downloader` | Newer CLI; Playwright optional | Primary **mirror** backend when installed |
| `chentianxiong123/webclone-skill` | Newest AI snapshot → codegen skill | Primary **snapshot** inspiration |
| `TechVentures-Studio/httrack-mcp` | Newest HTTrack MCP (0★) | Reference for `mirror_site` job pattern |
| `ajmaluk/site-mirror-skill` | Static + dynamic multi-page skill | Multi-page dynamic pattern |

## Fusion design

```
                    ┌─────────────────────┐
  Agent / Cursor ──►│  ThejaWebClone MCP  │
                    │  twc_* tools        │
                    └──────────┬──────────┘
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
     twc_mirror          twc_snapshot         twc_serve
  (website-downloader    (Playwright headed    (static + reverse
   or internal crawl)     page capture)         proxy to origin)
           │                   │                   │
           └────────► twc_rewrite ◄────────────────┘
                 (CDN absolute → local cdn/)
```

## Skills installed during the chat

- `~/.cursor/skills/webclone-skill`
- `~/.cursor/skills/website-downloader`
- New fused skill: `skills/theja-webclone` in this repo

## Runtime paths used on the machine

- `C:\Users\ThejanaD\tools\webclone-skill`
- `C:\Users\ThejanaD\tools\website-downloader`
- `C:\Users\ThejanaD\tools\clones\tyres-cardekho` (static archive)
- `C:\Users\ThejanaD\tools\clones\tyres-features\home2` (feature + proxy)
