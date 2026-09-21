"""
Interfaz de Línea de Comandos (CLI) interactiva.
Álgebra Lineal (MTM0120) - FIA UAM.

Permite al usuario interactuar con los dos módulos del programa evaluativo:
1. Decimal a Binario, Octal, Hexadecimal (con tabla de divisiones sucesivas).
2. Binario, Octal, Hexadecimal a Decimal (con desglose de la combinación lineal).
"""

import os
import sys

# Asegurar que la raíz del proyecto esté en sys.path para ejecuciones directas
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Optional
from src.core.decimal_converter import decimal_to_base, BASE_NAMES
from src.core.base_converter import base_to_decimal, validate_and_clean_input

# Códigos de color ANSI para presentación elegante en terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
RED = "\033[31m"


def print_header(title: str) -> None:
    line = "=" * 68
    print(f"\n{CYAN}{BOLD}{line}")
    print(f"  {title.center(64)}")
    print(f"{line}{RESET}\n")


def print_divider() -> None:
    print(f"{DIM}{'-' * 68}{RESET}")


def select_base(prompt_text: str) -> int:
    """Solicita al usuario seleccionar una base entre 2, 8 y 16."""
    while True:
        print(f"\n{BOLD}Seleccione la base numérica:{RESET}")
        print(f"  {CYAN}1){RESET} Base 2  (Binario)")
        print(f"  {CYAN}2){RESET} Base 8  (Octal)")
        print(f"  {CYAN}3){RESET} Base 16 (Hexadecimal)")
        choice = input(f"{YELLOW}Opción [1-3]: {RESET}").strip()

        if choice == "1" or choice.lower() in ("2", "binario", "bin"):
            return 2
        elif choice == "2" or choice.lower() in ("8", "octal", "oct"):
            return 8
        elif choice == "3" or choice.lower() in ("16", "hexadecimal", "hex"):
            return 16
        else:
            print(f"{RED}Opción inválida. Ingrese 1, 2 o 3.{RESET}")


def run_decimal_to_base_cli() -> None:
    """Ejecuta el flujo interactivo para el Módulo 1 (Decimal -> Bases)."""
    print_header("MÓDULO 1: DECIMAL A BINARIO / OCTAL / HEXADECIMAL")
    print(f"{DIM}Algoritmo: Divisiones sucesivas euclidianas y residuos invertidos.{RESET}\n")

    # Solicitar número decimal
    while True:
        raw_val = input(f"{YELLOW}Ingrese el número decimal entero a convertir: {RESET}").strip()
        try:
            decimal_val = int(raw_val)
            break
        except ValueError:
            print(f"{RED}Error: Debe ingresar un número entero válido (ej. 255, 1024, -42).{RESET}")

    target_base = select_base("Seleccione la base destino:")
    result = decimal_to_base(decimal_val, target_base)

    print("\n" + "=" * 68)
    print(f"{GREEN}{BOLD}RESULTADO: {result['decimal_input']} (base 10) = {result['result_str']} (base {result['target_base']} - {result['base_name']}){RESET}")
    print("=" * 68)

    print(f"\n{BOLD}PROCEDIMIENTO ALGEBRAICO DETALLADO:{RESET}")
    print(f"Teorema del Algoritmo de la División: Dividendo = (Cociente * Base) + Residuo\n")

    # Encabezado de la tabla de divisiones
    header = f"{'Paso':^6} | {'Dividendo':^11} | {'Divisor':^9} | {'Cociente':^10} | {'Residuo':^9} | {'Símbolo':^9}"
    print(f"{CYAN}{BOLD}{header}{RESET}")
    print_divider()

    for step in result["steps"]:
        row = (
            f"{step['step_number']:^6} | "
            f"{step['dividend']:^11} | "
            f"{step['divisor']:^9} | "
            f"{step['quotient']:^10} | "
            f"{step['remainder']:^9} | "
            f"{BOLD}{YELLOW}{step['remainder_symbol']:^9}{RESET}"
        )
        print(row)

    print_divider()
    print(f"\n{BOLD}Lectura de los Residuos (del último al primero):{RESET}")
    remainders_str = " -> ".join(result["remainders_forward"])
    reversed_str = " -> ".join(result["remainders_reversed"])
    print(f"  Residuos generados (orden normal):   {remainders_str}")
    print(f"  {GREEN}{BOLD}Residuos ordenados (orden inverso):  {reversed_str}{RESET}")
    print(f"  {BOLD}Representación final ({result['base_name']}): {result['result_str']}{RESET}\n")


def run_base_to_decimal_cli() -> None:
    """Ejecuta el flujo interactivo para el Módulo 2 (Bases -> Decimal)."""
    print_header("MÓDULO 2: BASE A DECIMAL (COMBINACIÓN LINEAL)")
    print(f"{DIM}Algoritmo: Combinación lineal posicional N = sum(d_i * b^i).{RESET}\n")

    source_base = select_base("Seleccione la base de origen:")
    base_name = BASE_NAMES[source_base]

    while True:
        raw_val = input(f"{YELLOW}Ingrese el número en base {source_base} ({base_name}): {RESET}").strip()
        try:
            result = base_to_decimal(raw_val, source_base)
            break
        except ValueError as e:
            print(f"{RED}Error de validación: {e}{RESET}")

    print("\n" + "=" * 68)
    print(f"{GREEN}{BOLD}RESULTADO: {result['raw_input']} (base {result['source_base']} - {result['base_name']}) = {result['decimal_result']} (base 10){RESET}")
    print("=" * 68)

    print(f"\n{BOLD}DESGLOSE DE TÉRMINOS VECTORIALES (Ponderación canónica):{RESET}")
    header = f"{'Pos (i)':^8} | {'Dígito':^8} | {'Escalar (d_i)':^14} | {'Base^i':^10} | {'Ponderación':^13} | {'Producto (d_i*b^i)':^18}"
    print(f"{CYAN}{BOLD}{header}{RESET}")
    print_divider()

    for term in result["terms"]:
        base_exp = f"{term['base']}^{term['exponent']}"
        row = (
            f"{term['exponent']:^8} | "
            f"{term['char']:^8} | "
            f"{term['scalar_value']:^14} | "
            f"{base_exp:^10} | "
            f"{term['weight']:^13} | "
            f"{BOLD}{YELLOW}{term['product']:^18}{RESET}"
        )
        print(row)

    print_divider()
    print(f"\n{BOLD}DEMOSTRACIÓN DE LA COMBINACIÓN LINEAL:{RESET}")
    print(f"  En el espacio vectorial de números enteros bajo la base canónica {{b^n, ..., b^0}}:")
    print(f"\n  N = {result['linear_combination_formula']}")
    print(f"    = {result['linear_combination_eval']}")
    print(f"    = {result['linear_combination_products']}")
    print(f"  {GREEN}{BOLD}  = {result['decimal_result']} (decimal){RESET}\n")


def run_cli_menu() -> None:
    """Bucle principal de la interfaz de consola."""
    while True:
        print_header("SISTEMAS NUMÉRICOS - ÁLGEBRA LINEAL (UAM)")
        print(f"{BOLD}Seleccione una opción:{RESET}")
        print(f"  {CYAN}1){RESET} Módulo 1: Convertir Decimal -> Binario, Octal, Hexadecimal (Divisiones sucesivas)")
        print(f"  {CYAN}2){RESET} Módulo 2: Convertir Binario, Octal, Hexadecimal -> Decimal (Combinación lineal)")
        print(f"  {CYAN}3){RESET} Salir")
        print_divider()

        choice = input(f"{YELLOW}Opción [1-3]: {RESET}").strip()

        if choice == "1":
            run_decimal_to_base_cli()
            input(f"\n{DIM}Presione Enter para volver al menú principal...{RESET}")
        elif choice == "2":
            run_base_to_decimal_cli()
            input(f"\n{DIM}Presione Enter para volver al menú principal...{RESET}")
        elif choice in ("3", "q", "exit", "salir"):
            print(f"\n{GREEN}Gracias por utilizar el Conversor de Sistemas Numéricos. ¡Éxitos en la defensa!{RESET}\n")
            sys.exit(0)
        else:
            print(f"{RED}Opción no válida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    run_cli_menu()
