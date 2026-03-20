import http.server, socketserver, os

PORT = 8080
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header('Cache-Control','no-cache')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"\n  WORLDHATCH — port {PORT}\n  Open Webview to play!\n")
with socketserver.TCPServer(("", PORT), Handler) as s:
    s.serve_forever()
