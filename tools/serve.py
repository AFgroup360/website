#!/usr/bin/env python3
"""Local preview server that mirrors the production .htaccess rules.

    python3 tools/serve.py        # http://localhost:8000

Resolves extensionless URLs to .html and serves 404.html for misses, so what you
see locally matches what GoDaddy serves.
"""
import functools
import http.server
import os
import pathlib
import socketserver
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        if os.path.isdir(local):
            index = os.path.join(local, "index.html")
            if os.path.exists(index):
                return index
        if not os.path.exists(local) and not local.endswith(".html"):
            candidate = local.rstrip("/") + ".html"
            if os.path.exists(candidate):
                return candidate
        return local

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = ROOT / "404.html"
            if page.exists():
                body = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(ROOT))
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Serving %s at http://localhost:%d  (Ctrl-C to stop)" % (ROOT, PORT))
        httpd.serve_forever()
