"""ThejaWebClone MCP server — stdio.

Exposes fused tools from the Website cloning skills chat.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import __version__
from .lessons import as_text
from .mirror import mirror, website_downloader_available
from .rewrite import rewrite_root
from .snapshot import snapshot


def _build():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit(
            "Install MCP extra: py -3.11 -m pip install -e '.[mcp]'"
        ) from exc

    mcp = FastMCP("ThejaWebClone")

    @mcp.tool()
    def twc_status() -> str:
        """Report ThejaWebClone version and whether mirror/snapshot backends are installed."""
        try:
            import playwright  # noqa: F401

            pw = True
        except Exception:
            pw = False
        return json.dumps(
            {
                "version": __version__,
                "website_downloader": website_downloader_available(),
                "playwright": pw,
            }
        )

    @mcp.tool()
    def twc_chat_lessons() -> str:
        """Return frozen lessons and prompt insights from the source Cursor chat."""
        return as_text()

    @mcp.tool()
    def twc_mirror(
        url: str,
        out_dir: str,
        max_pages: int = 200,
        render_js: bool = True,
    ) -> str:
        """Recursively mirror a site into out_dir (uses website-downloader when installed)."""
        result = mirror(url, Path(out_dir), max_pages=max_pages, render_js=render_js)
        return json.dumps(result)

    @mcp.tool()
    def twc_snapshot(url: str, out_dir: str, headed: bool = True) -> str:
        """Playwright-render one page into out_dir (use headed=True behind CloudFront)."""
        result = snapshot(url, Path(out_dir), headed=headed)
        return json.dumps(result)

    @mcp.tool()
    def twc_rewrite(root_dir: str, hosts_csv: str, inject_css: str = "") -> str:
        """Rewrite absolute CDN URLs under root_dir to local cdn/ paths."""
        hosts = [h.strip() for h in hosts_csv.split(",") if h.strip()]
        n = rewrite_root(Path(root_dir), hosts, inject_css=inject_css or None)
        return json.dumps({"changed": n, "root": root_dir})

    @mcp.tool()
    def twc_serve_hint(root_dir: str, port: int = 8770, origin: str = "") -> str:
        """Return the exact CLI command to serve a clone (MCP cannot block on serve_forever)."""
        cmd = f'py -3.11 -m theja_webclone.cli serve --root "{root_dir}" --port {port}'
        if origin:
            cmd += f' --origin "{origin}"'
        return json.dumps(
            {
                "message": "Run this command in a terminal (long-running).",
                "command": cmd,
                "open": f"http://127.0.0.1:{port}/",
            }
        )

    return mcp


def main() -> None:
    mcp = _build()
    mcp.run()


if __name__ == "__main__":
    main()
