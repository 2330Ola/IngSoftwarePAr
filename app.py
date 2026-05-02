"""
Servidor web en Python estándar que sirve HTML, CSS y estáticos.
Ejecutar: python app.py
Abrir: http://127.0.0.1:8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote
import mimetypes

BASE_DIR = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        raw = unquote(self.path.split("?", 1)[0])
        if raw in ("/", "/index.html"):
            file_path = BASE_DIR / "index.html"
        elif raw.startswith("/static/"):
            candidate = (BASE_DIR / raw.lstrip("/")).resolve()
            try:
                candidate.relative_to(BASE_DIR)
            except ValueError:
                self.send_error(403)
                return
            file_path = candidate
        else:
            self.send_error(404)
            return

        if not file_path.is_file():
            self.send_error(404)
            return

        body = file_path.read_bytes()
        ctype, _ = mimetypes.guess_type(str(file_path))
        if ctype is None:
            ctype = "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {args[0]}")


if __name__ == "__main__":
    host, port = "127.0.0.1", 8000
    print(f"Servidor en http://{host}:{port}  (Ctrl+C para detener)")
    HTTPServer((host, port), Handler).serve_forever()
