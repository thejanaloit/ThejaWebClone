from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .lessons import as_text
from .mirror import mirror
from .rewrite import rewrite_root
from .serve import serve
from .snapshot import snapshot


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="theja-webclone", description="ThejaWebClone fused website clone toolkit")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("mirror", help="Recursive offline archive")
    m.add_argument("--url", required=True)
    m.add_argument("--out", required=True, type=Path)
    m.add_argument("--max-pages", type=int, default=200)
    m.add_argument("--render-js", action="store_true", default=True)
    m.add_argument("--no-render-js", action="store_true")
    m.add_argument("--url-file", type=Path)

    s = sub.add_parser("snapshot", help="Playwright page snapshot")
    s.add_argument("--url", required=True)
    s.add_argument("--out", required=True, type=Path)
    s.add_argument("--headed", action="store_true", default=True)
    s.add_argument("--headless", action="store_true")

    r = sub.add_parser("rewrite", help="Rewrite CDN URLs to local cdn/")
    r.add_argument("--root", required=True, type=Path)
    r.add_argument("--hosts", required=True, help="Comma-separated CDN hosts")
    r.add_argument("--inject-css", default=None)

    v = sub.add_parser("serve", help="Serve local root with optional origin proxy")
    v.add_argument("--root", required=True, type=Path)
    v.add_argument("--port", type=int, default=8770)
    v.add_argument("--origin", default=None)

    sub.add_parser("lessons", help="Print lessons from the source chat")
    sub.add_parser("status", help="Show install status")

    args = p.parse_args(argv)

    if args.cmd == "mirror":
        result = mirror(
            args.url,
            args.out,
            max_pages=args.max_pages,
            render_js=not args.no_render_js,
            url_file=args.url_file,
        )
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1

    if args.cmd == "snapshot":
        result = snapshot(args.url, args.out, headed=not args.headless)
        print(json.dumps(result, indent=2))
        return 0

    if args.cmd == "rewrite":
        hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
        n = rewrite_root(args.root, hosts, inject_css=args.inject_css)
        print(json.dumps({"changed": n, "root": str(args.root)}))
        return 0

    if args.cmd == "serve":
        serve(args.root, args.port, args.origin)
        return 0

    if args.cmd == "lessons":
        print(as_text())
        return 0

    if args.cmd == "status":
        from .mirror import website_downloader_available

        try:
            import playwright  # noqa: F401

            pw = True
        except Exception:
            pw = False
        print(
            json.dumps(
                {
                    "version": __version__,
                    "website_downloader": website_downloader_available(),
                    "playwright": pw,
                },
                indent=2,
            )
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
