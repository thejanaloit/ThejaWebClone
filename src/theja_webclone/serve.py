from __future__ import annotations

import json
import mimetypes
import socketserver
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def write_proxy_config(root: Path, origin: str, enabled: bool = True) -> None:
    (root / "proxy-config.json").write_text(
        json.dumps({"originUrl": origin, "proxyEnabled": enabled}, indent=2),
        encoding="utf-8",
    )


def _make_handler(root: Path, origin: str):
    root = root.resolve()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:  # noqa: A003
            print("[%s] %s" % (self.log_date_time_string(), fmt % args))

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self.send_header("access-control-allow-origin", "*")
            self.send_header("access-control-allow-methods", "GET, POST, OPTIONS")
            self.send_header("access-control-allow-headers", "*")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            self._serve_or_proxy()

        def do_POST(self) -> None:  # noqa: N802
            self._proxy()

        def _local_file(self) -> Path | None:
            rel = self.path.split("?", 1)[0].lstrip("/")
            if not rel or rel.endswith("/"):
                rel = f"{rel}index.html" if rel else "index.html"
            candidate = (root / rel).resolve()
            if str(candidate).startswith(str(root)) and candidate.is_file():
                return candidate
            return None

        def _serve_or_proxy(self) -> None:
            local = self._local_file()
            if local is not None:
                data = local.read_bytes()
                ctype = mimetypes.guess_type(str(local))[0] or "application/octet-stream"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            self._proxy()

        def _proxy(self) -> None:
            if not origin:
                self.send_error(404, "Not found (proxy disabled)")
                return
            parsed = urlparse(origin)
            target = f"{parsed.scheme}://{parsed.netloc}{self.path}"
            length = int(self.headers.get("Content-Length", "0") or 0)
            body = self.rfile.read(length) if length else None
            req = Request(target, data=body, method=self.command)
            req.add_header("User-Agent", self.headers.get("User-Agent", "ThejaWebClone/0.1"))
            req.add_header("Host", parsed.netloc)
            try:
                with urlopen(req, timeout=30) as resp:  # noqa: S310
                    data = resp.read()
                    self.send_response(resp.status)
                    self.send_header("access-control-allow-origin", "*")
                    self.send_header(
                        "Content-Type",
                        resp.headers.get("Content-Type", "application/octet-stream"),
                    )
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as exc:  # noqa: BLE001
                if not self.wfile.closed:
                    try:
                        self.send_error(502, f"Proxy error: {exc}")
                    except Exception:  # noqa: BLE001
                        pass

    return Handler


def serve(root: Path, port: int, origin: str | None = None) -> None:
    root = root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    if origin:
        write_proxy_config(root, origin, True)
    handler = _make_handler(root, origin or "")
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"ThejaWebClone serving {root} at http://127.0.0.1:{port}")
    if origin:
        print(f"Proxy origin: {origin}")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("stopped")
    finally:
        httpd.server_close()
