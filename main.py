#!/usr/bin/env python3
"""
Punto de Entrada Principal: Calculadora de Sistemas Numéricos.
Álgebra Lineal (MTM0120) - Facultad de Ingeniería y Arquitectura (FIA) - UAM.

Permite ejecutar:
1. Interfaz Web Moderna (por defecto): Inicia el servidor local y abre el navegador.
2. Interfaz de Consola (CLI): Con el parámetro --cli o -c.
3. Suite de Pruebas Unitarias: Con el parámetro --test o -t.
"""

import sys
import os
import argparse
import webbrowser
import threading
import time

# Asegurar que el directorio raíz del proyecto esté en sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.cli.interface import run_cli_menu
from src.web.server import run_server


def start_web_interface(port: int = 8000) -> None:
    """Inicia el servidor web nativo y abre automáticamente el navegador."""
    server, actual_port = run_server(port)
    url = f"http://127.0.0.1:{actual_port}/"

    print("\n" + "=" * 65)
    print("  CALCULADORA DE SISTEMAS NUMÉRICOS - ÁLGEBRA LINEAL (UAM)")
    print("=" * 65)
    print(f"  Servidor Web Activo en: {url}")
    print("  Abriendo navegador predeterminado...")
    print("  Presione Ctrl+C en cualquier momento para detener el servidor.")
    print("=" * 65 + "\n")

    # Intentar abrir el navegador web del sistema en un hilo secundario
    def open_browser():
        time.sleep(0.5)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido correctamente. ¡Hasta luego!")
        server.server_close()


def run_tests() -> None:
    """Ejecuta la suite de pruebas unitarias."""
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def main() -> None:
    """Función de despacho según los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Calculadora de Sistemas Numéricos - Álgebra Lineal UAM (MTM0120)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 main.py          Inicia la aplicación web moderna en el navegador (recomendado)
  python3 main.py --cli    Ejecuta el menú interactivo en la terminal
  python3 main.py --test   Ejecuta la batería de pruebas unitarias
        """
    )
    parser.add_argument(
        "-c", "--cli",
        action="store_true",
        help="Iniciar en modo interfaz de línea de comandos (CLI)"
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        help="Ejecutar la suite de pruebas unitarias automáticas"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8000,
        help="Puerto para el servidor web (por defecto: 8000)"
    )

    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.cli:
        run_cli_menu()
    else:
        start_web_interface(args.port)


if __name__ == "__main__":
    main()
