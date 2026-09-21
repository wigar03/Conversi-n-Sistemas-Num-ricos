"""
Módulo de Conversión: Decimal a Sistemas Numéricos (Binario, Octal, Hexadecimal).
Álgebra Lineal (MTM0120) - FIA UAM.

Fundamentación Algebraica:
--------------------------
De acuerdo con el Teorema del Algoritmo de la División Euclidiana en los números enteros,
para cualquier entero decimal N >= 0 y una base entera b in {2, 8, 16}, existen enteros
únicos q_i (cocientes) y r_i (residuos) que satisfacen:

    N = q_0 * b + r_0,         donde 0 <= r_0 < b
    q_0 = q_1 * b + r_1,       donde 0 <= r_1 < b
    q_1 = q_2 * b + r_2,       donde 0 <= r_2 < b
    ...
    q_{n-1} = 0 * b + r_n,     donde 0 <= r_n < b

Sustituyendo recursivamente los cocientes:
    N = r_n * b^n + r_{n-1} * b^{n-1} + ... + r_1 * b^1 + r_0 * b^0

Por consiguiente, la representación del número N en la base b se obtiene disponiendo
los residuos resultantes en orden inverso al que fueron generados:
    (N)_10 = (r_n r_{n-1} ... r_1 r_0)_b

Restricciones didácticas cumplidas:
- Sin NumPy ni SciPy ni funciones de math.
- Sin funciones built-in de conversión (bin(), oct(), hex(), int(x, base)).
- Implementación pura mediante bucles while, operadores aritméticos fundamentales (//, %) y listas.
"""

from typing import Dict, Any, List

# Diccionario canónico de correspondencia posicional para residuos mayores o iguales a 10
HEX_SYMBOLS: List[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

BASE_NAMES: Dict[int, str] = {
    2: "Binario",
    8: "Octal",
    16: "Hexadecimal"
}

def decimal_to_base(decimal_number: int, target_base: int) -> Dict[str, Any]:
    """
    Convierte un número decimal entero a una base destino (2, 8 o 16)
    empleando el algoritmo de divisiones sucesivas.

    Procedimiento algebraico:
    1. Se calcula el residuo mediante r = dividendo % base.
    2. Se calcula el nuevo cociente mediante q = dividendo // base.
    3. Se mapea el residuo a su símbolo equivalente (especialmente para base 16: 10->A, 11->B, etc.).
    4. El proceso se itera mientras el cociente sea estrictamente mayor que 0.
    5. Los residuos se concatenan en orden cronológicamente inverso (del último residuo obtenido al primero).

    Args:
        decimal_number (int): Número decimal a convertir (admite positivos, negativos y cero).
        target_base (int): Base de destino requerida (2 para binario, 8 para octal, 16 para hexadecimal).

    Returns:
        Dict[str, Any]: Diccionario con la representación final, pasos algebraicos y metadatos.

    Raises:
        ValueError: Si la base no es 2, 8 o 16, o si el número no es entero.
    """
    if not isinstance(decimal_number, int):
        raise ValueError("El número a convertir debe ser un número entero.")

    if target_base not in (2, 8, 16):
        raise ValueError(f"Base no soportada: {target_base}. Las bases permitidas son 2 (Binario), 8 (Octal) y 16 (Hexadecimal).")

    is_negative: bool = decimal_number < 0
    current_dividend: int = -decimal_number if is_negative else decimal_number

    steps: List[Dict[str, Any]] = []
    remainders: List[str] = []

    # Caso particular: el número es 0
    if current_dividend == 0:
        steps.append({
            "step_number": 1,
            "dividend": 0,
            "divisor": target_base,
            "quotient": 0,
            "remainder": 0,
            "remainder_symbol": "0",
            "equation": f"0 = 0 * {target_base} + 0"
        })
        return {
            "decimal_input": decimal_number,
            "target_base": target_base,
            "base_name": BASE_NAMES[target_base],
            "result_str": "0",
            "is_negative": is_negative,
            "steps": steps,
            "remainders_forward": ["0"],
            "remainders_reversed": ["0"],
            "algebraic_proof": f"0_{{10}} = 0_{{{target_base}}}"
        }

    step_counter: int = 1
    # Bucle de divisiones sucesivas hasta agotar el cociente a cero
    while current_dividend > 0:
        # Cociente entero: q = dividendo // divisor
        quotient: int = current_dividend // target_base
        # Residuo algebraico: r = dividendo - (cociente * divisor) equivalente a dividendo % divisor
        remainder: int = current_dividend - (quotient * target_base)
        symbol: str = HEX_SYMBOLS[remainder]

        remainders.append(symbol)

        steps.append({
            "step_number": step_counter,
            "dividend": current_dividend,
            "divisor": target_base,
            "quotient": quotient,
            "remainder": remainder,
            "remainder_symbol": symbol,
            "equation": f"{current_dividend} = ({quotient} * {target_base}) + {remainder}"
        })

        # El cociente se convierte en el dividendo de la siguiente iteración
        current_dividend = quotient
        step_counter += 1

    # Invertir la lista de residuos manualmente respetando la norma algorítmica
    # (El residuo de la última división es el dígito más significativo)
    reversed_remainders: List[str] = []
    for i in range(len(remainders) - 1, -1, -1):
        reversed_remainders.append(remainders[i])

    result_digits: str = "".join(reversed_remainders)
    result_str: str = f"-{result_digits}" if is_negative else result_digits

    # Demostración algebraica para retroalimentación
    algebraic_proof = f"({decimal_number})_{{10}} = ({result_str})_{{{target_base}}}"

    return {
        "decimal_input": decimal_number,
        "target_base": target_base,
        "base_name": BASE_NAMES[target_base],
        "result_str": result_str,
        "is_negative": is_negative,
        "steps": steps,
        "remainders_forward": remainders,
        "remainders_reversed": reversed_remainders,
        "algebraic_proof": algebraic_proof
    }
