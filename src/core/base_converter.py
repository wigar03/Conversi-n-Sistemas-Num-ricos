"""
Módulo de Conversión: Sistemas Numéricos (Binario, Octal, Hexadecimal) a Decimal.
Álgebra Lineal (MTM0120) - FIA UAM.

Fundamentación Algebraica y Enfoque en Álgebra Lineal:
------------------------------------------------------
En el Álgebra Lineal, cualquier número expresado en un sistema posicional con base b
puede modelarse formalmente como una COMBINACIÓN LINEAL de los vectores base de ponderación
monomial {b^n, b^{n-1}, ..., b^1, b^0} con escalares d_i pertenecientes al conjunto
finito de coordenadas {0, 1, ..., b-1}:

    N_10 = sum_{i=0}^{n} ( d_i * b^i )
         = d_n * b^n + d_{n-1} * b^{n-1} + ... + d_1 * b^1 + d_0 * b^0

Donde:
- b in {2, 8, 16} representa la base numérica (el factor multiplicativo del espacio vectorial).
- d_i representa el escalar o coordenada en la posición i.
- b^i representa la ponderación canónica del grado i.
- d_i * b^i representa la contribución de la proyección escalar a la magnitud decimal total.

Restricciones didácticas cumplidas:
- Sin NumPy ni SciPy ni math.pow / int(s, base).
- Sin atajos built-in.
- Cálculo de potencias y productos implementado mediante bucles estándar y aritmética básica.
"""

from typing import Dict, Any, List, Tuple
from src.core.decimal_converter import BASE_NAMES

# Tabla de valores canónicos para dígitos posicionales en bases hasta 16
CHAR_TO_VALUE: Dict[str, int] = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15
}

VALID_DIGITS_BY_BASE: Dict[int, str] = {
    2: "0, 1",
    8: "0, 1, 2, 3, 4, 5, 6, 7",
    16: "0-9, A-F (sin distinción de mayúsculas/minúsculas)"
}

def validate_and_clean_input(number_str: str, base: int) -> Tuple[str, bool]:
    """
    Valida y limpia una cadena numérica según las reglas estrictas de la base dada.

    Args:
        number_str (str): Cadena a verificar.
        base (int): Base esperada (2, 8, 16).

    Returns:
        Tuple[str, bool]: (Cadena limpia en mayúsculas sin signo, bandera is_negative).

    Raises:
        ValueError: Si la cadena contiene caracteres no válidos para la base o está vacía.
    """
    if not isinstance(number_str, str):
        raise ValueError("La entrada debe ser una cadena de texto representativa del número.")

    cleaned: str = number_str.strip()
    if not cleaned:
        raise ValueError("La entrada no puede estar vacía.")

    is_negative: bool = False
    if cleaned[0] == "-":
        is_negative = True
        cleaned = cleaned[1:].strip()
    elif cleaned[0] == "+":
        cleaned = cleaned[1:].strip()

    if not cleaned:
        raise ValueError("Debe ingresar dígitos después del signo.")

    cleaned_upper: str = cleaned.upper()

    for char in cleaned_upper:
        if char not in CHAR_TO_VALUE:
            raise ValueError(
                f"Carácter inválido '{char}'. Dígitos permitidos para base {base} ({BASE_NAMES.get(base, 'Desconocida')}): {VALID_DIGITS_BY_BASE.get(base)}"
            )
        val = CHAR_TO_VALUE[char]
        if val >= base:
            raise ValueError(
                f"El dígito '{char}' (valor {val}) no pertenece a la base {base}. "
                f"En base {base}, cada dígito debe ser estrictamente menor que {base} (permitidos: {VALID_DIGITS_BY_BASE.get(base)})."
            )

    return cleaned_upper, is_negative


def base_to_decimal(number_str: str, source_base: int) -> Dict[str, Any]:
    """
    Convierte una representación numérica en base 2, 8 o 16 a su equivalente decimal
    demostrando detalladamente la combinación lineal de sus ponderaciones canónicas.

    Procedimiento algebraico:
    1. Se analiza la longitud n del número; los exponentes van desde (n-1) hasta 0.
    2. Para cada dígito d_i en la posición i con exponente exp = (n - 1 - índice):
       - Escalar d_i = valor numérico del símbolo (ej. 'B' -> 11).
       - Ponderación canónica W_i = base^exp (calculada por multiplicación iterativa).
       - Producto escalar = d_i * W_i.
    3. La suma de los productos escalares genera el número decimal final.

    Args:
        number_str (str): Cadena del número en base origen.
        source_base (int): Base numérica de origen (2, 8 o 16).

    Returns:
        Dict[str, Any]: Desglose de la combinación lineal, términos algebraicos y valor decimal.
    """
    if source_base not in (2, 8, 16):
        raise ValueError(f"Base no soportada: {source_base}. Las bases permitidas son 2, 8 y 16.")

    clean_str, is_negative = validate_and_clean_input(number_str, source_base)
    length: int = len(clean_str)

    terms: List[Dict[str, Any]] = []
    total_decimal: int = 0
    polynomial_formula_parts: List[str] = []
    evaluation_parts: List[str] = []
    products_parts: List[str] = []

    # Procesar de izquierda a derecha (desde el dígito más significativo)
    for idx in range(length):
        char = clean_str[idx]
        exponent = length - 1 - idx
        scalar = CHAR_TO_VALUE[char]

        # Cálculo manual de la potencia base^exponent sin librerías externas
        weight = 1
        for _ in range(exponent):
            weight = weight * source_base

        product = scalar * weight
        total_decimal += product

        # Construcción de representaciones textuales para la fórmula algebraica
        if source_base == 16 and char in "ABCDEF":
            term_str = f"({char}[={scalar}] * {source_base}^{exponent})"
        else:
            term_str = f"({scalar} * {source_base}^{exponent})"

        eval_str = f"({scalar} * {weight})"
        prod_str = str(product)

        polynomial_formula_parts.append(term_str)
        evaluation_parts.append(eval_str)
        products_parts.append(prod_str)

        terms.append({
            "index_from_left": idx,
            "exponent": exponent,
            "char": char,
            "scalar_value": scalar,
            "base": source_base,
            "weight": weight,
            "product": product,
            "term_algebraic": f"{scalar} * {source_base}^{exponent}",
            "term_evaluated": f"{scalar} * {weight} = {product}"
        })

    final_decimal = -total_decimal if is_negative else total_decimal

    # Expresión completa de la combinación lineal
    formula_joined = " + ".join(polynomial_formula_parts)
    eval_joined = " + ".join(evaluation_parts)
    prods_joined = " + ".join(products_parts)

    linear_combination_expansion = (
        f"Combinación Lineal:\n"
        f"  N = {formula_joined}\n"
        f"    = {eval_joined}\n"
        f"    = {prods_joined}\n"
        f"    = {total_decimal}"
    )

    vector_scalars = [CHAR_TO_VALUE[c] for c in clean_str]
    vector_weights = [terms[i]["weight"] for i in range(length)]

    algebraic_proof = f"({number_str.strip()})_{{{source_base}}} = ({final_decimal})_{{10}}"

    return {
        "raw_input": number_str,
        "clean_input": clean_str,
        "source_base": source_base,
        "base_name": BASE_NAMES[source_base],
        "decimal_result": final_decimal,
        "is_negative": is_negative,
        "terms": terms,
        "vector_scalars": vector_scalars,
        "vector_weights": vector_weights,
        "linear_combination_formula": formula_joined,
        "linear_combination_eval": eval_joined,
        "linear_combination_products": prods_joined,
        "linear_combination_expansion": linear_combination_expansion,
        "algebraic_proof": algebraic_proof
    }
