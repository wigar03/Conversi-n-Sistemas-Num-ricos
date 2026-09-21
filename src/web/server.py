"""
Servidor HTTP nativo en Python estándar para la aplicación web.
Álgebra Lineal (MTM0120) - FIA UAM.

Características:
- Implementado 100% con la librería estándar de Python (http.server, socketserver, json).
- Cero dependencias externas requeridas (no necesita Flask, FastAPI ni pip).
- Provee endpoints REST para conversión algebraica de sistemas numéricos.
- Sirve los recursos estáticos (HTML5, CSS3 moderno, JavaScript Vanilla).
"""

import os
import sys
import json
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Tuple, Dict, Any

# Asegurar importación de los módulos del core
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.core.decimal_converter import decimal_to_base
from src.core.base_converter import base_to_decimal

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


class NumericalSystemsHTTPHandler(SimpleHTTPRequestHandler):
    """Manejador de peticiones HTTP para endpoints de API y archivos estáticos."""

    def __init__(self, *args, **kwargs):
        # Servir archivos estáticos desde el directorio static
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json_response(self, status_code: int, data: Dict[str, Any]) -> None:
        """Helper para emitir respuestas JSON normalizadas."""
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        """Manejo de preflight CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        """Maneja peticiones GET de la API o sirve archivos estáticos."""
        if self.path == "/api/status" or self.path == "/api/health":
            self._send_json_response(200, {
                "status": "online",
                "project": "Calculadora de Sistemas Numéricos - Álgebra Lineal",
                "institution": "Universidad Americana (UAM) - FIA",
                "version": "1.0.0"
            })
            return

        # Para la raíz o cualquier archivo estático, delegar en SimpleHTTPRequestHandler
        if self.path == "/" or self.path == "":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self) -> None:
        """Maneja peticiones POST para los endpoints de conversión."""
        content_length_str = self.headers.get("Content-Length")
        if not content_length_str:
            self._send_json_response(400, {"success": False, "error": "Cabecera Content-Length ausente."})
            return

        try:
            content_length = int(content_length_str)
            raw_body = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(raw_body)
        except Exception as e:
            self._send_json_response(400, {"success": False, "error": f"JSON inválido en la petición: {str(e)}"})
            return

        # Endpoint Módulo 1: Decimal -> Bases (Divisiones Sucesivas)
        if self.path == "/api/convert/from-decimal":
            try:
                decimal_val = body.get("decimal")
                target_base = body.get("base")

                if decimal_val is None or target_base is None:
                    raise ValueError("Se requieren los campos 'decimal' (entero) y 'base' (2, 8 o 16).")

                # Asegurar conversión a enteros
                decimal_val = int(decimal_val)
                target_base = int(target_base)

                result = decimal_to_base(decimal_val, target_base)
                self._send_json_response(200, {"success": True, "data": result})
            except Exception as e:
                self._send_json_response(400, {"success": False, "error": str(e)})
            return

        # Endpoint Módulo 2: Bases -> Decimal (Combinación Lineal)
        elif self.path == "/api/convert/to-decimal":
            try:
                num_str = body.get("value")
                source_base = body.get("base")

                if num_str is None or source_base is None:
                    raise ValueError("Se requieren los campos 'value' (cadena) y 'base' (2, 8 o 16).")

                source_base = int(source_base)
                num_str = str(num_str).strip()

                result = base_to_decimal(num_str, source_base)
                self._send_json_response(200, {"success": True, "data": result})
            except Exception as e:
                self._send_json_response(400, {"success": False, "error": str(e)})
            return

        else:
            self._send_json_response(404, {"success": False, "error": f"Ruta POST no encontrada: {self.path}"})


def find_free_port(start_port: int = 8000, max_attempts: int = 20) -> int:
    """Encuentra un puerto disponible de forma dinámica."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


def run_server(port: int = 8000, host: str = "127.0.0.1") -> Tuple[HTTPServer, int]:
    """
    Crea e inicia el servidor HTTP nativo.
    """
    actual_port = find_free_port(port)
    server_address = (host, actual_port)
    httpd = HTTPServer(server_address, NumericalSystemsHTTPHandler)
    return httpd, actual_port


if __name__ == "__main__":
    server, p = run_server()
    print(f"Servidor HTTP corriendo en: http://127.0.0.1:{p}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
        server.server_close()
