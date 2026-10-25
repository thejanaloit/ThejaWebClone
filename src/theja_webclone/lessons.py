"""Frozen lessons from the Website cloning skills chat."""

CHAT_ID = "782d09ea-95b5-4772-83f7-702400140b32"
CHAT_TITLE = "Website cloning skills"

LESSONS = [
    "Judge clone tools by what the code does, not the repository name.",
    "Highest GitHub stars is not the same as best SPA mirror; Playwright crawlers beat wget on JS sites.",
    "webclone-skill and website-downloader are CLI/skills until wrapped as MCP.",
    "Python 3.14 may fail package installs; use 3.11 for website-downloader on Windows.",
    "CloudFront often returns 403 to plain HTTP/headless; use headed Playwright / --render-js.",
    "Sitemap may also be 403 — seed URLs from already-mirrored HTML.",
    "After mirror, rewrite absolute CDN URLs to local cdn/ or the page paints blank.",
    "Edge/Chrome can show a blank tab from cache even when the server returns 200 — hard refresh.",
    "Local http.server dies when the session ends — document restart command.",
    "Proxy servers must guard writeHead after timeout (ERR_HTTP_HEADERS_SENT).",
    "All product pages is not the same as core features 1:1. Features need live API proxy or a rebuilt backend.",
    "Perfect offline 1:1 of a commercial API-backed site is not achievable as static files alone.",
]


def as_text() -> str:
    lines = [f"Chat: {CHAT_TITLE} ({CHAT_ID})", "", "Lessons:"]
    lines.extend(f"- {x}" for x in LESSONS)
    return "\n".join(lines)
