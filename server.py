"""
server.py — WORLDHATCH Web Server
══════════════════════════════════
Serves the browser game on Replit's webview port.

Run:
  python server.py

Then open the Replit webview tab — the game loads automatically.
"""

import http.server
import socketserver
import os

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve world.html as the root page
        if self.path == '/' or self.path == '/index.html':
            self.path = '/world.html'
        return super().do_GET()

    def log_message(self, format, *args):
        # Suppress noisy access logs
        pass

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"""
╔══════════════════════════════════════════════╗
  WORLDHATCH Web Server starting on port {PORT}
  Open the Replit Webview tab to play!
  Press Ctrl+C to stop.
╚══════════════════════════════════════════════╝
""")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
