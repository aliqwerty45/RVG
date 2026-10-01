#!/usr/bin/env python3
"""
RVG Design Playground — a tiny learn-by-doing server for the project's UI.

Why it exists
-------------
All of RVG's web UI lives in `pages.py` as big HTML strings (LOGIN_HTML,
DASHBOARD_HTML, get_public_page_html). Normally you can only see those pages by
running the whole FastAPI app and logging in. This script serves them directly,
with no backend, no auth and no database, plus live-reload: save `pages.py` and
the browser refreshes itself.

That makes `pages.py` a safe sandbox for learning web design — change a colour,
a radius, a spacing value, hit save, see it instantly.

Usage
-----
    python3 devtools/design_playground.py            # http://0.0.0.0:7100
    python3 devtools/design_playground.py --port 8080

Routes
------
    /            index with links + what to try
    /login       LOGIN_HTML
    /dashboard   DASHBOARD_HTML
    /sub         get_public_page_html("demo-uuid-0000")
    /api/*       mocked JSON so the pages' fetch() calls don't explode

Stdlib only. Never imported by the app itself — this is a dev tool.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_FILE = os.path.join(REPO_ROOT, "pages.py")

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# ── live reload ───────────────────────────────────────────────────────────────

LIVE_RELOAD_SNIPPET = """
<script>
/* RVG Design Playground — live reload (dev only) */
(function () {
  var current = null;
  async function tick() {
    try {
      var r = await fetch('/__rvg/version', { cache: 'no-store' });
      var v = (await r.json()).version;
      if (current === null) current = v;
      else if (v !== current) location.reload();
    } catch (e) { /* server restarting, ignore */ }
  }
  setInterval(tick, 1000);
  tick();
})();
</script>
"""


def pages_version() -> str:
    try:
        st = os.stat(PAGES_FILE)
        return f"{st.st_mtime_ns}-{st.st_size}"
    except OSError:
        return "missing"


def load_pages():
    """(Re)import pages.py so every request sees the file as it is on disk."""
    if "pages" in sys.modules:
        return importlib.reload(sys.modules["pages"])
    return importlib.import_module("pages")


def inject(html: str) -> str:
    if "</body>" in html:
        return html.replace("</body>", LIVE_RELOAD_SNIPPET + "</body>", 1)
    return html + LIVE_RELOAD_SNIPPET


# ── index page ────────────────────────────────────────────────────────────────

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RVG Design Playground</title>
<style>
  :root { --bg:#080B14; --card:#0D1220; --line:rgba(124,147,255,.18);
          --text:#EEF2FF; --dim:#8B96C4; --accent:#4F6BFF; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); min-height:100vh; padding:48px 20px;
         font:15px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }
  .wrap { max-width:720px; margin:0 auto; }
  h1 { font-size:26px; letter-spacing:-.02em; margin-bottom:6px; }
  .sub { color:var(--dim); margin-bottom:32px; }
  .grid { display:grid; gap:12px; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); }
  a.card { display:block; padding:18px; border:1px solid var(--line); border-radius:14px;
           background:var(--card); color:var(--text); text-decoration:none; transition:.18s; }
  a.card:hover { border-color:var(--accent); transform:translateY(-2px); }
  a.card b { display:block; font-size:16px; margin-bottom:4px; }
  a.card span { color:var(--dim); font-size:13px; }
  section { margin-top:36px; }
  h2 { font-size:15px; text-transform:uppercase; letter-spacing:.1em; color:var(--accent);
       margin-bottom:12px; }
  ol { padding-left:20px; color:var(--dim); }
  ol li { margin-bottom:8px; }
  code { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px;
         background:rgba(124,147,255,.12); padding:1px 6px; border-radius:6px; color:var(--text); }
  footer { margin-top:40px; color:var(--dim); font-size:13px; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>RVG Design Playground</h1>
    <p class="sub">Your own UI, served without the backend. Edit <code>pages.py</code>, save, and the page reloads itself.</p>

    <div class="grid">
      <a class="card" href="/login"><b>Login page</b><span>LOGIN_HTML — small, the best place to start</span></a>
      <a class="card" href="/dashboard"><b>Dashboard</b><span>DASHBOARD_HTML — layout, tables, modals</span></a>
      <a class="card" href="/sub"><b>Public sub page</b><span>get_public_page_html() — cards &amp; progress bars</span></a>
    </div>

    <section>
      <h2>Try these first</h2>
      <ol>
        <li>Open <code>pages.py</code>, find <code>:root { --accent: #4F6BFF }</code> and change it. Every button and glow follows.</li>
        <li>Change <code>--radius</code> / <code>border-radius</code> from 18px to 4px. Notice how much "personality" lives in one number.</li>
        <li>Open DevTools (F12) &rarr; device toolbar &rarr; 375px wide. Find what breaks, fix it with flex-wrap or a media query.</li>
        <li>Pick one card and double its padding. Spacing is the cheapest upgrade in design.</li>
      </ol>
    </section>

    <section>
      <h2>Notes</h2>
      <ol>
        <li>API calls are mocked, so data areas may stay empty — that is fine, you are here for layout and style.</li>
        <li>This tool is dev-only: the FastAPI app never imports it.</li>
        <li>Read <code>docs/learn-web-design.md</code> for the full roadmap and exercises.</li>
      </ol>
    </section>

    <footer>Serving from <code>pages.py</code> &middot; live reload is on.</footer>
  </div>
</body>
</html>
"""


ERROR_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Playground error</title>
<style>body{{background:#140A0E;color:#FFD9E0;font:14px/1.6 ui-monospace,monospace;padding:32px}}
h1{{font-size:18px;color:#FB7185;margin-bottom:12px}} pre{{white-space:pre-wrap}}</style></head>
<body><h1>pages.py could not be rendered</h1><pre>{detail}</pre>
<p style="margin-top:16px;color:#8B96C4">Fix the error and save — this page reloads automatically.</p>
{snippet}</body></html>
"""


# ── mocked API ────────────────────────────────────────────────────────────────

MOCK_API = {
    "/api/me": {"authenticated": True},
    "/api/login": {"ok": True},
    "/api/logout": {"ok": True},
    "/api/update-log": {"ok": True, "log": "playground — no updater running"},
}


class Handler(BaseHTTPRequestHandler):
    server_version = "RVGDesignPlayground"

    # ── helpers ──
    def _send(self, body: bytes, status: int = 200, ctype: str = "text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _html(self, html: str, status: int = 200):
        self._send(html.encode("utf-8"), status)

    def _json(self, payload, status: int = 200):
        self._send(json.dumps(payload).encode("utf-8"), status, "application/json; charset=utf-8")

    def _render(self, which: str):
        try:
            pages = load_pages()
            if which == "login":
                html = pages.LOGIN_HTML
            elif which == "dashboard":
                html = pages.DASHBOARD_HTML
            else:
                html = pages.get_public_page_html("demo-uuid-0000")
            self._html(inject(html))
        except Exception:
            detail = traceback.format_exc()
            self._html(
                ERROR_TEMPLATE.format(
                    detail=detail.replace("&", "&amp;").replace("<", "&lt;"),
                    snippet=LIVE_RELOAD_SNIPPET,
                ),
                status=500,
            )

    # ── routing ──
    def do_GET(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"

        if path == "/":
            return self._html(inject(INDEX_HTML))
        if path == "/__rvg/version":
            return self._json({"version": pages_version()})
        if path in ("/login", "/dashboard"):
            return self._render(path.lstrip("/"))
        if path == "/sub" or path.startswith("/api/public/sub"):
            return self._render("sub")
        if path.startswith("/api/"):
            return self._json(MOCK_API.get(path, {"ok": True, "items": [], "data": {}}))
        return self._json({"ok": False, "error": "not found", "path": path}, status=404)

    do_HEAD = do_GET

    def do_POST(self):
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        if path.startswith("/api/"):
            return self._json(MOCK_API.get(path, {"ok": True}))
        return self._json({"ok": False, "error": "not found", "path": path}, status=404)

    def log_message(self, fmt, *args):  # quieter console
        if "__rvg/version" in (args[0] if args else ""):
            return
        sys.stderr.write("  %s\n" % (fmt % args))


def main() -> int:
    ap = argparse.ArgumentParser(description="Serve RVG's pages.py UI with live reload.")
    ap.add_argument("--port", type=int, default=7100)
    ap.add_argument("--host", default="0.0.0.0")
    args = ap.parse_args()

    if not os.path.exists(PAGES_FILE):
        print(f"pages.py not found at {PAGES_FILE}", file=sys.stderr)
        return 1

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"RVG Design Playground  →  http://{args.host}:{args.port}")
    print("  /login  /dashboard  /sub      (live reload on pages.py)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
