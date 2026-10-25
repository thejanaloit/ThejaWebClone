from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

# Prefer packaged data, then repo data/, then live Cursor mcp.json
_REPO_DATA = Path(__file__).resolve().parents[2] / "data" / "connected-mcps.json"
_CURSOR_MCP = Path.home() / ".cursor" / "mcp.json"


def _load_packaged() -> dict | None:
    candidates = [
        Path(__file__).resolve().parent / "data" / "connected-mcps.json",
        Path(__file__).resolve().parents[2] / "data" / "connected-mcps.json",
    ]
    for p in candidates:
        try:
            if p.is_file():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return None


def load_inventory(refresh_from_cursor: bool = False) -> dict:
    if refresh_from_cursor and _CURSOR_MCP.is_file():
        return snapshot_from_cursor_mcp(_CURSOR_MCP)
    data = _load_packaged()
    if data:
        return data
    if _CURSOR_MCP.is_file():
        return snapshot_from_cursor_mcp(_CURSOR_MCP)
    return {"count": 0, "servers": {}, "error": "no inventory found"}


def snapshot_from_cursor_mcp(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    servers_in = raw.get("mcpServers", {})
    servers = {}
    for name, cfg in sorted(servers_in.items()):
        env = {}
        for k, v in (cfg.get("env") or {}).items():
            kl = k.lower()
            if any(x in kl for x in ("token", "key", "secret", "password", "passwd", "credential")):
                env[k] = "<redacted>"
            elif isinstance(v, str) and len(v) > 40 and " " not in v and not (
                v.startswith("C:") or v.startswith("/") or "\\" in v
            ):
                env[k] = "<redacted>"
            else:
                env[k] = v
        entry = {
            "command": cfg.get("command"),
            "args": cfg.get("args"),
            "url": cfg.get("url"),
            "type": cfg.get("type"),
            "clone_chat_role": "connected in Cursor; available during ThejaWebClone sessions",
        }
        if env:
            entry["env"] = env
        servers[name] = {k: v for k, v in entry.items() if v is not None}
    return {
        "source": str(path),
        "chat_id": "782d09ea-95b5-4772-83f7-702400140b32",
        "chat_title": "Website cloning skills",
        "count": len(servers),
        "servers": servers,
    }


def list_names() -> list[str]:
    return sorted(load_inventory().get("servers", {}).keys())


def get_server(name: str) -> dict | None:
    servers = load_inventory().get("servers", {})
    if name in servers:
        return servers[name]
    # case-insensitive
    for k, v in servers.items():
        if k.lower() == name.lower():
            return v
    return None
