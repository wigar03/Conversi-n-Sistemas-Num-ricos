"""
Batería de Pruebas Unitarias para el Conversor de Sistemas Numéricos.
Álgebra Lineal (MTM0120) - FIA UAM.

Verifica:
1. Exactitud de las conversiones de Decimal a Binario, Octal y Hexadecimal.
2. Exactitud de las conversiones de Binario, Octal y Hexadecimal a Decimal.
3. Propiedad de consistencia bidireccional (inversa algebraica).
4. Manejo de casos límite (cero, números negativos, potencias exactas).
5. Rigor de las ecuaciones de divisiones sucesivas y combinaciones lineales.
6. Manejo correcto de excepciones ante entradas inválidas o caracteres fuera de base.
"""

import unittest
from src.core.decimal_converter import decimal_to_base
from src.core.base_converter import base_to_decimal, validate_and_clean_input


class TestDecimalToBase(unittest.TestCase):
    """Pruebas del Módulo 1: Decimal a otras bases numéricas."""

    def test_zero_conversion(self):
        """El valor 0 debe convertirse a '0' en todas las bases."""
        for base in (2, 8, 16):
            res = decimal_to_base(0, base)
            self.assertEqual(res["result_str"], "0")
            self.assertEqual(len(res["steps"]), 1)
            self.assertEqual(res["steps"][0]["remainder"], 0)

    def test_binary_conversions(self):
        """Conversión precisa a base 2 (Binario)."""
        cases = [
            (1, "1"),
            (2, "10"),
            (5, "101"),
            (22, "10110"),
            (255, "11111111"),
            (1024, "10000000000")
        ]
        for dec_val, expected in cases:
            res = decimal_to_base(dec_val, 2)
            self.assertEqual(res["result_str"], expected, f"Fallo al convertir {dec_val} a base 2")

    def test_octal_conversions(self):
        """Conversión precisa a base 8 (Octal)."""
        cases = [
            (7, "7"),
            (8, "10"),
            (255, "377"),
            (512, "1000"),
            (935, "1647")
        ]
        for dec_val, expected in cases:
            res = decimal_to_base(dec_val, 8)
            self.assertEqual(res["result_str"], expected, f"Fallo al convertir {dec_val} a base 8")

    def test_hexadecimal_conversions(self):
        """Conversión precisa a base 16 (Hexadecimal) con mapeo A-F."""
        cases = [
            (10, "A"),
            (15, "F"),
            (16, "10"),
            (255, "FF"),
            (935, "3A7"),
            (4096, "1000")
        ]
        for dec_val, expected in cases:
            res = decimal_to_base(dec_val, 16)
            self.assertEqual(res["result_str"], expected, f"Fallo al convertir {dec_val} a base 16")

    def test_negative_decimal(self):
        """Los números negativos deben conservar el signo '-'."""
        res = decimal_to_base(-42, 2)
        self.assertTrue(res["is_negative"])
        self.assertTrue(res["result_str"].startswith("-"))
        self.assertEqual(res["result_str"], "-101010")

    def test_division_algorithm_invariant(self):
        """Cada paso debe satisfacer el Teorema: dividendo = cociente * divisor + residuo."""
        test_numbers = [13, 85, 255, 935, 4097]
        for n in test_numbers:
            for b in (2, 8, 16):
                res = decimal_to_base(n, b)
                for step in res["steps"]:
                    d = step["dividend"]
                    q = step["quotient"]
                    divisor = step["divisor"]
                    r = step["remainder"]
                    self.assertEqual(d, (q * divisor) + r)
                    self.assertTrue(0 <= r < divisor)

    def test_invalid_base_rejection(self):
        """Bases distintas de 2, 8 y 16 deben rechazar la ejecución con ValueError."""
        for invalid_base in (3, 4, 10, 32, -2):
            with self.assertRaises(ValueError):
                decimal_to_base(100, invalid_base)

    def test_invalid_type_rejection(self):
        """Entradas no enteras deben generar ValueError."""
        with self.assertRaises(ValueError):
            decimal_to_base("100", 2)  # type: ignore
        with self.assertRaises(ValueError):
            decimal_to_base(12.34, 2)  # type: ignore


class TestBaseToDecimal(unittest.TestCase):
    """Pruebas del Módulo 2: Bases numéricas a Decimal mediante Combinación Lineal."""

    def test_binary_to_decimal(self):
        """Conversión de binario a decimal mediante sum(d_i * 2^i)."""
        cases = [
            ("0", 0),
            ("1", 1),
            ("10", 2),
            ("10110", 22),
            ("11111111", 255),
            ("10000000000", 1024)
        ]
        for bin_str, expected in cases:
            res = base_to_decimal(bin_str, 2)
            self.assertEqual(res["decimal_result"], expected)

    def test_octal_to_decimal(self):
        """Conversión de octal a decimal mediante sum(d_i * 8^i)."""
        cases = [
            ("0", 0),
            ("7", 7),
            ("10", 8),
            ("377", 255),
            ("1647", 935)
        ]
        for oct_str, expected in cases:
            res = base_to_decimal(oct_str, 8)
            self.assertEqual(res["decimal_result"], expected)

    def test_hexadecimal_to_decimal(self):
        """Conversión de hexadecimal a decimal mediante sum(d_i * 16^i)."""
        cases = [
            ("0", 0),
            ("A", 10),
            ("f", 15),       # Minúscula válida
            ("FF", 255),
            ("3A7", 935),
            ("3a7", 935),     # Case-insensitive
            ("1000", 4096)
        ]
        for hex_str, expected in cases:
            res = base_to_decimal(hex_str, 16)
            self.assertEqual(res["decimal_result"], expected)

    def test_linear_combination_terms(self):
        """La suma explícita de los términos escalares debe ser igual al decimal resultante."""
        res = base_to_decimal("3A7", 16)
        terms_sum = sum(term["product"] for term in res["terms"])
        self.assertEqual(terms_sum, res["decimal_result"])
        self.assertEqual(res["decimal_result"], 935)

    def test_negative_base_number(self):
        """Debe procesar números negativos preservando el signo algebraico."""
        res = base_to_decimal("-10110", 2)
        self.assertEqual(res["decimal_result"], -22)
        self.assertTrue(res["is_negative"])

    def test_invalid_digits_rejection(self):
        """Rechazar dígitos prohibidos según la base."""
        # En base 2: '2', '8', 'A' son inválidos
        with self.assertRaises(ValueError):
            base_to_decimal("102", 2)
        with self.assertRaises(ValueError):
            base_to_decimal("10A", 2)

        # En base 8: '8', '9', 'B' son inválidos
        with self.assertRaises(ValueError):
            base_to_decimal("387", 8)
        with self.assertRaises(ValueError):
            base_to_decimal("19", 8)

        # En base 16: 'G', 'Z', '#' son inválidos
        with self.assertRaises(ValueError):
            base_to_decimal("3G7", 16)
        with self.assertRaises(ValueError):
            base_to_decimal("Z1", 16)


class TestBidirectionalConsistency(unittest.TestCase):
    """Prueba de consistencia: (N_10 -> N_b -> N_10) == N_10 para cualquier número y base."""

    def test_roundtrip_all_bases(self):
        test_values = [0, 1, 2, 7, 8, 15, 16, 22, 42, 100, 255, 935, 1024, 65535]
        for val in test_values:
            for base in (2, 8, 16):
                converted = decimal_to_base(val, base)
                restored = base_to_decimal(converted["result_str"], base)
                self.assertEqual(
                    restored["decimal_result"],
                    val,
                    f"Fallo de consistencia bidireccional para {val} en base {base}"
                )


if __name__ == "__main__":
    unittest.main()
