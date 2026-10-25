from __future__ import annotations

import json
from pathlib import Path


def snapshot(url: str, out: Path, headed: bool = True, timeout_ms: int = 45000) -> dict:
    """Capture a rendered page with Playwright (headed recommended behind CloudFront)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install playwright: pip install -e '.[render]' && playwright install chromium") from exc

    out.mkdir(parents=True, exist_ok=True)
    assets = out / "assets"
    assets.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        resp = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
        html = page.content()
        title = page.title()
        browser.close()

    index = out / "index.html"
    # Stamp source for later rewrite/proxy
    stamp = f'<meta name="theja-webclone:source" content="{url}"/>'
    if "<head>" in html:
        html = html.replace("<head>", f"<head>{stamp}", 1)
    index.write_text(html, encoding="utf-8")
    meta = {
        "url": url,
        "title": title,
        "status": resp.status if resp else None,
        "bytes": len(html.encode("utf-8", errors="replace")),
        "headed": headed,
    }
    (out / "snapshot.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"ok": True, "out": str(out), **meta}
