# Calculadora de Sistemas Numéricos — Álgebra Lineal (MTM0120)

> **Universidad Americana (UAM)**  
> **Facultad de Ingeniería y Arquitectura (FIA)**  
> **Asignatura:** Álgebra Lineal (`MTM0120`)  
> **Proyecto Integrador:** Módulo de Conversión de Sistemas Numéricos (Primer Corte Evaluativo)
> 
> Integrantes (Grupo 10):

    William Antonio García García

    Andrés Sebastián González Maradiaga

    Rafael Hernández Sánchez

    Caleb Jordan Tardencilla Alvarado

---

## 1. Descripción de la Actividad

El presente software constituye un módulo interactivo de conversión bidireccional entre números decimales (base 10) y los sistemas numéricos **Binario (base 2)**, **Octal (base 8)** y **Hexadecimal (base 16)**.

El desarrollo se enfoca en el **rigor algebraico**, exponiendo paso a paso los teoremas y procedimientos matemáticos correspondientes:
- **Módulo 1 (Decimal a Otras Bases):** Algoritmo de divisiones sucesivas euclidianas, registrando dividendo, divisor, cociente y residuos invertidos.
- **Módulo 2 (Otras Bases a Decimal):** Descomposición formal en **combinación lineal** de coordenadas escalares sobre la base canónica polinomial de ponderaciones.

---

## 2. Fundamentación en Álgebra Lineal

### 2.1. Representación Vectorial y Combinación Lineal (Módulo 2)
En el Álgebra Lineal, un sistema numérico posicional en base $b \in \{2, 8, 16\}$ modela cualquier entero $N$ como una **combinación lineal** de los elementos de una base ortogonal de ponderaciones monomias:

$$\mathcal{B} = \{ b^n, b^{n-1}, \dots, b^1, b^0 \}$$

Donde:
- Cada número se interpreta como un vector de coordenadas escalares:
  $$\vec{d} = (d_n, d_{n-1}, \dots, d_1, d_0), \quad \text{con } d_i \in \{0, 1, \dots, b-1\}$$
- La magnitud escalar en base decimal corresponde al producto punto formal entre el vector de coordenadas y la base canónica:
  $$N_{10} = \sum_{i=0}^n d_i \cdot b^i = d_n \cdot b^n + d_{n-1} \cdot b^{n-1} + \dots + d_1 \cdot b^1 + d_0 \cdot b^0$$

#### Ejemplo Algebraico:
Para el número hexadecimal $(3A7)_{16}$:
$$N = (3 \cdot 16^2) + (10 \cdot 16^1) + (7 \cdot 16^0) = (3 \cdot 256) + (10 \cdot 16) + (7 \cdot 1) = 768 + 160 + 7 = 935_{10}$$

### 2.2. Teorema de la División Euclidiana (Módulo 1)
Para transformar un número decimal $N \ge 0$ a una base $b > 1$, se aplica iterativamente el Teorema del Algoritmo de la División:

$$D_k = q_k \cdot b + r_k, \quad \text{donde } 0 \le r_k < b$$

El cociente $q_k$ se transforma en el dividendo de la iteración subsiguiente hasta que $q_k = 0$. Por el principio de ordenamiento posicional, el último residuo obtenido representa el escalar más significativo ($d_n$), mientras que el primero corresponde al menos significativo ($d_0$):

$$(N)_{10} = (r_n \, r_{n-1} \, \dots \, r_1 \, r_0)_b$$

---

## 3. Cumplimiento Estricto de Normas Técnicas

Conforme a las directrices didácticas de la asignatura:
- **Cero librerías externas:** No se utilizan `NumPy`, `SciPy`, ni funciones complejas de `math`.
- **Cero atajos built-in:** No se emplean funciones automáticas de conversión de Python como `bin()`, `oct()`, `hex()` o `int(cadena, base)` para saltarse la lógica algorítmica.
- **Python estándar:** Todas las operaciones están fundamentadas en estructuras de datos nativas (`listas`, `bucles for/while`, `condicionales` y `funciones`).
- **Comentarios en código:** Cada función está documentada explicando detalladamente la equivalencia matemática y el algoritmo implementado.

---

## 4. Estructura del Proyecto

```
Conversión Sistemas Numéricos/
├── README.md                 # Documentación técnica y académica completa
├── main.py                   # Lanzador universal (Servidor Web y modo CLI)
├── .gitignore                # Reglas de exclusión para control de versiones
├── src/
│   ├── __init__.py           # Paquete raíz
│   ├── core/                 # Algoritmos algebraicos puros
│   │   ├── __init__.py
│   │   ├── decimal_converter.py  # Módulo 1: Divisiones sucesivas
│   │   └── base_converter.py     # Módulo 2: Combinaciones lineales
│   ├── cli/                  # Interfaz de consola interactiva
│   │   ├── __init__.py
│   │   └── interface.py      # Menús y tablas formateadas para terminal
│   └── web/                  # Servidor local nativo e interfaz gráfica moderna
│       ├── __init__.py
│       ├── server.py         # HTTP Server nativo en Python (sin dependencias)
│       └── static/           # SPA interactiva (HTML5, CSS3 Glassmorphism, JS)
│           ├── index.html
│           ├── style.css
│           └── app.js
└── tests/                    # Batería de pruebas unitarias
    ├── __init__.py
    └── test_conversions.py   # Validación de rigor matemático y casos límite
```

---

## 5. Instrucciones de Ejecución

El programa no requiere la instalación de librerías mediante `pip` ni configuraciones complejas. Solo requiere **Python 3** estándar.

### 5.1. Ejecutar la Aplicación Gráfica Web (Recomendado)
Inicia el servidor local y abre automáticamente la interfaz en el navegador web predeterminado:

```bash
python3 main.py
```
*Si el navegador no se abre de forma automática, acceder a la URL indicada en la consola (por ejemplo: `http://127.0.0.1:8000/`).*

### 5.2. Ejecutar la Interfaz de Línea de Comandos (CLI)
Para evaluar el software directamente desde la consola con tablas ASCII y explicaciones paso a paso:

```bash
python3 main.py --cli
```

### 5.3. Ejecutar las Pruebas Unitarias
Para verificar el rigor matemático y la cobertura de pruebas de ambos módulos:

```bash
python3 -m unittest discover tests -v
```

---

## 6. Características de la Interfaz

- **Estética Glassmorphism:** Paleta refinada de colores, modo oscuro/claro con persistencia, tipografías modernas y contrastes armónicos.
- **Visualizador de Divisiones:** Tabla paso a paso con residuo destacado, comprobación euclidiana ($D = q \cdot b + r$) y flujo animado de residuos en orden inverso.
- **Visualizador de Combinación Lineal:** Cuadrícula de ponderación posicional para cada dígito, visualizador del producto escalar vectorial y desglose algebraico polinomial completo.
- **Validaciones en Tiempo Real:** Detección de caracteres no válidos de acuerdo a la base seleccionada (ej. rechazo de '2' en binario o '8' en octal).
- **Controles Stepper Intuitivos (+ / −):** Desactivación del scroll nativo involuntario y spinners del navegador en inputs numéricos, reemplazados por controles interactivos con soporte para pulsación simple y continua (press & hold).
- **Iconografía Minimalista Open Source:** Interfaz limpia sin emojis, estandarizada con iconos vectoriales SVG de Lucide Icons (MIT) adaptables a modo claro y oscuro.

