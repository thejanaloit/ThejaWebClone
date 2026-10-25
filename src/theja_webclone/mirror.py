from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def website_downloader_available() -> bool:
    try:
        import website_downloader  # noqa: F401

        return True
    except Exception:
        return shutil.which("website-downloader") is not None


def mirror(
    url: str,
    out: Path,
    max_pages: int = 200,
    render_js: bool = True,
    download_external: bool = True,
    url_file: Path | None = None,
) -> dict:
    """Run PKHarsimran website-downloader when available; else raise with install hint."""
    out.mkdir(parents=True, exist_ok=True)
    if not website_downloader_available():
        raise RuntimeError(
            "website-downloader not installed. "
            "pip install -e path/to/website-downloader  "
            "(see README). For a single page use: theja-webclone snapshot"
        )
    cmd = [
        sys.executable,
        "-m",
        "website_downloader",
        "--url",
        url,
        "--destination",
        str(out),
        "--max-pages",
        str(max_pages),
    ]
    if render_js:
        cmd.append("--render-js")
    if download_external:
        cmd.append("--download-external-assets")
    if url_file and url_file.is_file():
        cmd.extend(["--url-file", str(url_file)])
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "code": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-2000:],
        "stderr_tail": (proc.stderr or "")[-2000:],
        "out": str(out),
        "cmd": cmd,
    }
