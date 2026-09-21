"""
Módulo Core: Algoritmos algebraicos de conversión entre sistemas numéricos.
Cumple estrictamente las restricciones didácticas (sin NumPy, SciPy ni built-ins directos).
"""
from src.core.decimal_converter import decimal_to_base, BASE_NAMES, HEX_SYMBOLS

__all__ = ["decimal_to_base", "BASE_NAMES", "HEX_SYMBOLS"]
