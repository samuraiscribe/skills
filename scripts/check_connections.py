#!/usr/bin/env python3
"""Check that every connection's server still answers the way the app signs in.

    python3 scripts/check_connections.py [--register] [id ...]

`validate.py` checks the files; this asks the services themselves, so it needs
the network and runs on pull requests that touch `connections/` and once a
week. Services move their MCP servers (Asana retired its first one in 2026),
and a preset that points at an address nobody answers any more shows the user
a Connect button that cannot work.

For each connection:

- the address answers an unauthenticated request with 401 and an OAuth
  challenge naming its protected-resource metadata (the MCP authorization
  spec), or — for `api_key` — with 401 at all;
- that metadata names an authorization server whose own metadata has an
  authorization endpoint;
- the app can register there by itself (`registration_endpoint`), unless the
  connection names its own `client_id`;
- with `--register`, the service accepts that registration for the address
  the app's sign-in returns to, `http://127.0.0.1:<port>/…` — a loopback
  address over plain http, as every desktop sign-in is. Calendly advertises
  registration and then refuses any redirect that is not https, which only
  this catches. It leaves a registered client at the service, so it runs on
  pull requests that change a connection, not every week.

Exits non-zero with one line per problem. Standard library only.
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONNECTIONS = ROOT / "connections"
TIMEOUT = 15
USER_AGENT = "samuraiscribe-skills-check/1"
RESOURCE_METADATA = re.compile(r'resource_metadata="([^"]+)"')
# Where the app's sign-in returns: `handlers/connections.rs` in the app.
APP_REDIRECT = "http://127.0.0.1:8000/api/connections/oauth/callback"


def context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL = context()


def request(url: str, method: str = "GET", body: bytes | None = None) -> tuple[int, dict[str, str], bytes]:
    headers = {"user-agent": USER_AGENT, "accept": "application/json, text/event-stream"}
    if body is not None:
        headers["content-type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read()


def json_at(url: str) -> dict | None:
    try:
        status, _, body = request(url)
    except (OSError, ValueError):
        return None
    if status != 200:
        return None
    try:
        value = json.loads(body)
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def server_metadata(issuer: str) -> dict | None:
    """RFC 8414 metadata, at the places servers actually put it: the path
    inserted after the well-known prefix, the bare host, then OpenID's."""
    u = urllib.parse.urlparse(issuer)
    host, path = f"{u.scheme}://{u.netloc}", u.path.rstrip("/")
    for well_known in ("/.well-known/oauth-authorization-server", "/.well-known/openid-configuration"):
        for url in (host + well_known + path, host + well_known, issuer.rstrip("/") + well_known):
            meta = json_at(url)
            if meta and "authorization_endpoint" in meta:
                return meta
    return None


def try_registering(endpoint: str) -> str | None:
    """Register as the app does (rmcp: a public client with PKCE); None when
    accepted, else the service's answer."""
    body = json.dumps({
        "client_name": "Samurai Scribe connection check",
        "redirect_uris": [APP_REDIRECT],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }).encode()
    try:
        status, _, answer = request(endpoint, "POST", body)
    except (OSError, ValueError) as e:
        return str(e)
    if 200 <= status < 300:
        return None
    return f"{status} {answer[:300].decode('utf-8', 'replace')}"


def check(c: dict, register: bool = False) -> list[str]:
    where = f"connections/{c.get('id')}"
    url = c.get("url", "")
    if not url.startswith("https://"):
        return [f"{where}: {url} is not https"]
    initialize = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": USER_AGENT, "version": "1"}}}
    ).encode()
    try:
        status, headers, _ = request(url, "POST", initialize)
    except (OSError, ValueError) as e:
        return [f"{where}: {url} could not be reached ({e})"]
    if status != 401:
        return [f"{where}: {url} answered {status} without sign-in, not 401"]
    if c.get("auth") != "oauth":
        return []
    challenge = headers.get("www-authenticate", "")
    found = RESOURCE_METADATA.search(challenge)
    resource = json_at(found.group(1)) if found else None
    if resource is None:
        # Older servers skip the challenge; the spec's fallback is the
        # well-known address at the server's root.
        u = urllib.parse.urlparse(url)
        resource = json_at(f"{u.scheme}://{u.netloc}/.well-known/oauth-protected-resource{u.path.rstrip('/')}") or json_at(
            f"{u.scheme}://{u.netloc}/.well-known/oauth-protected-resource"
        )
    if resource is None:
        return [f"{where}: {url} names no protected-resource metadata, so a sign-in cannot start"]
    servers = resource.get("authorization_servers") or []
    if not servers:
        return [f"{where}: the protected-resource metadata names no authorization server"]
    meta = server_metadata(servers[0])
    if meta is None:
        return [f"{where}: no metadata for the authorization server {servers[0]}"]
    if not meta.get("registration_endpoint") and not c.get("client_id"):
        return [f"{where}: {servers[0]} does not let apps register themselves, and the connection names no client_id"]
    if register and not c.get("client_id"):
        refused = try_registering(meta["registration_endpoint"])
        if refused:
            return [f"{where}: {servers[0]} refused the app's registration for {APP_REDIRECT}: {refused}"]
    return []


def main(argv: list[str]) -> int:
    register = "--register" in argv
    argv = [a for a in argv if a != "--register"]
    folders = sorted(p for p in CONNECTIONS.iterdir() if (p / "connection.json").is_file()) if CONNECTIONS.is_dir() else []
    if argv:
        folders = [f for f in folders if f.name in argv]
    problems: list[str] = []
    for folder in folders:
        c = json.loads((folder / "connection.json").read_text(encoding="utf-8"))
        found = check(c, register)
        print(f"{folder.name}: {'ok' if not found else 'PROBLEM'}")
        problems += found
    for p in problems:
        print(p)
    print(f"{len(folders)} connections: {'ok' if not problems else f'{len(problems)} problems'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
