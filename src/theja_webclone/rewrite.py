from __future__ import annotations

import re
from pathlib import Path


def rewrite_root(root: Path, hosts: list[str], inject_css: str | None = None) -> int:
    """Rewrite absolute https://host/... URLs to relative cdn/host/... under root."""
    if not hosts:
        raise ValueError("hosts required")
    host_alt = "|".join(re.escape(h.strip()) for h in hosts if h.strip())
    pattern = re.compile(
        rf"""(?P<prefix>["'(=]|url\()(?P<url>https?://(?P<host>{host_alt})(?P<path>/[^"'\)\s]*))""",
        re.I,
    )
    changed = 0
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root)
        depth = len(rel.parts) - 1
        prefix = "../" * depth

        def repl(m: re.Match[str]) -> str:
            host = m.group("host")
            pth = m.group("path").lstrip("/").split("?", 1)[0]
            return f"{m.group('prefix')}{prefix}cdn/{host}/{pth}"

        out = pattern.sub(repl, text)
        if inject_css and inject_css not in out and "</title>" in out:
            css_href = prefix + inject_css if not inject_css.startswith(("http", "/")) else inject_css
            out = out.replace("</title>", f'</title>\n<link rel="stylesheet" href="{css_href}"/>', 1)
        if out != text:
            path.write_text(out, encoding="utf-8")
            changed += 1
    return changed
