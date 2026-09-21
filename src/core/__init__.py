"""
Módulo Core: Algoritmos algebraicos de conversión entre sistemas numéricos.
Cumple estrictamente las restricciones didácticas (sin NumPy, SciPy ni built-ins directos).
"""
from src.core.decimal_converter import decimal_to_base, BASE_NAMES, HEX_SYMBOLS
from src.core.base_converter import base_to_decimal, validate_and_clean_input, CHAR_TO_VALUE

__all__ = [
    "decimal_to_base",
    "base_to_decimal",
    "validate_and_clean_input",
    "BASE_NAMES",
    "HEX_SYMBOLS",
    "CHAR_TO_VALUE"
]
