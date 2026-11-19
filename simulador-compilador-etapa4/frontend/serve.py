import http.server
import urllib.request
import urllib.error

BACKEND = "http://127.0.0.1:8000"

class Handler(http.server.SimpleHTTPRequestHandler):
    def proxy(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(tamanho) if tamanho else None
        req = urllib.request.Request(
            BACKEND + self.path,
            data=corpo,
            method=self.command,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
        )
        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.HTTPError as erro:
            resp = erro
        dados = resp.read()
        self.send_response(resp.getcode())
        self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path.startswith("/api"):
            return self.proxy()
        super().do_GET()

    def do_POST(self):
        self.proxy()

http.server.ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
