# Calculadora de Sistemas Numéricos: Álgebra Lineal (MTM0120)

```text
================================================================================
                    UNIVERSIDAD AMERICANA (UAM)
               Facultad de Ingeniería y Arquitectura (FIA)
                    Álgebra Lineal (MTM0120)
                  Primer Corte Evaluativo (30 Puntos)
================================================================================
  Docente:     Carlos Iván Argüello
  Grupo:       Grupo 10
  Modalidad:   Grupal con defensa/exposición individual
  Proyecto:    Módulo de Conversión de Sistemas Numéricos:
               Divisiones Sucesivas Euclidianas y Combinación Lineal
================================================================================
  Integrantes:
    • William Antonio García García
    • Caleb Jordan Tardencilla Alvarado
    • Rafael Hernández Sánchez
    • Andrés Sebastián González Maradiaga
================================================================================
```

---

## 1. Descripción de la Actividad

El presente software constituye un módulo interactivo de conversión bidireccional entre números decimales (base 10) y los sistemas numéricos **Binario (base 2)**, **Octal (base 8)** y **Hexadecimal (base 16)**.

El desarrollo se enfoca en el **rigor algebraico**, exponiendo paso a paso los teoremas y procedimientos matemáticos correspondientes:
- **Módulo 1 (Decimal a Otras Bases):** Algoritmo de divisiones sucesivas euclidianas, registrando dividendo, divisor, cociente y residuos invertidos.
- **Módulo 2 (Otras Bases a Decimal):** Descomposición formal en **combinación lineal** de coordenadas escalares sobre la base canónica polinomial de ponderaciones.

---

## 2. Fundamentación en Álgebra Lineal

### 2.1. Representación Vectorial y Combinación Lineal (Módulo 2)

En Álgebra Lineal, un sistema numérico posicional en base $b \in \{2, 8, 16\}$ modela cualquier entero no negativo $N$ como una **combinación lineal** de los elementos de una base ortogonal de ponderaciones monomias:

$$
\mathcal{B} = \{ b^n, b^{n-1}, \dots, b^1, b^0 \}
$$

Cada número se representa mediante un vector de coordenadas escalares:

$$
\vec{d} = (d_n, d_{n-1}, \dots, d_1, d_0), \quad \text{con } d_i \in \{0, 1, \dots, b-1\}
$$

La magnitud escalar en base decimal corresponde al producto escalar formal entre el vector de coordenadas y los vectores de la base de potencias:

$$
N_{10} = \sum_{i=0}^n d_i \cdot b^i = d_n \cdot b^n + d_{n-1} \cdot b^{n-1} + \dots + d_1 \cdot b^1 + d_0 \cdot b^0
$$

#### Ejemplo Algebraico
Para el número hexadecimal $(3A7)_{16}$, con coordenadas $\vec{d} = (3, 10, 7)$ en base $b = 16$:

$$
N = (3 \cdot 16^2) + (10 \cdot 16^1) + (7 \cdot 16^0)
$$

$$
N = (3 \cdot 256) + (10 \cdot 16) + (7 \cdot 1) = 768 + 160 + 7 = 935_{10}
$$

### 2.2. Teorema de la División Euclidiana (Módulo 1)

Para transformar un número decimal $N \ge 0$ a una base de destino $b > 1$, se aplica recursiva o iterativamente el Teorema del Algoritmo de la División:

$$
D_k = q_k \cdot b + r_k, \quad \text{con } 0 \le r_k < b
$$

El cociente $q_k$ se establece como el dividendo de la iteración subsiguiente hasta que $q_k = 0$. Por el principio de ordenamiento posicional, el último residuo obtenido representa el coeficiente más significativo $d_n$, mientras que el primero corresponde al menos significativo $d_0$:

$$
(N)_{10} = (r_n \, r_{n-1} \, \dots \, r_1 \, r_0)_b
$$

---

## 3. Cumplimiento Estricto de Normas Técnicas

Conforme a las directrices didácticas de la asignatura:
- **Cero librerías externas:** No se utilizan `NumPy`, `SciPy`, ni funciones complejas de `math`.
- **Cero atajos built-in:** No se emplean funciones automáticas de conversión de Python como `bin()`, `oct()`, `hex()` o `int(cadena, base)` para saltarse la lógica algorítmica.
- **Python estándar:** Todas las operaciones están fundamentadas en estructuras de datos nativas (`listas`, bucles `for` / `while`, condicionales `if` / `else` y funciones modulares).
- **Comentarios en código:** Cada función está documentada explicando detalladamente la equivalencia matemática y el algoritmo implementado.

---

## 4. Estructura del Proyecto

```text
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
│           ├── index.html    # Estructura semántica accesible con iconografía SVG
│           ├── style.css     # Estilos modernos con modo claro/oscuro y glassmorphism
│           └── app.js        # Lógica cliente y controladores interactivos
└── tests/                    # Batería completa de pruebas unitarias
    ├── __init__.py
    └── test_conversions.py   # Validación de rigor matemático y casos límite
```

---

## 5. Instrucciones de Ejecución

El programa no requiere la instalación de paquetes externos mediante `pip` ni configuraciones adicionales. Funciona al 100% con **Python 3** estándar.

### 5.1. Ejecutar la Aplicación Gráfica Web (Recomendado)
Inicia el servidor local y abre automáticamente la interfaz en el navegador web predeterminado:

```bash
python3 main.py
```
*Si el navegador no se abre de forma automática, acceder a la URL indicada en la consola (por ejemplo: `http://127.0.0.1:8000/`).*

Opciones adicionales:
```bash
python3 main.py --port 9000      # Cambiar el puerto
python3 main.py --no-browser     # Iniciar servidor sin abrir navegador automáticamente
```

### 5.2. Ejecutar la Interfaz de Línea de Comandos (CLI)
Para evaluar el software directamente desde la consola con tablas ASCII y explicaciones paso a paso:

```bash
python3 main.py --cli
```

### 5.3. Ejecutar las Pruebas Unitarias
El proyecto incluye una suite de **15 pruebas unitarias automatizadas** que validan la exactitud de cada algoritmo de conversión y sus casos límite:

```bash
python3 -m unittest discover tests -v
```

---

## 6. Características de la Interfaz

- **Estética Glassmorphism:** Paleta refinada de colores, modo oscuro/claro con persistencia, tipografías modernas y contrastes armónicos.
- **Visualizador de Divisiones:** Tabla paso a paso con residuo destacado, comprobación euclidiana $D = q \cdot b + r$ y flujo animado de residuos en orden inverso.
- **Visualizador de Combinación Lineal:** Cuadrícula de ponderación posicional para cada dígito, visualizador del producto escalar vectorial y desglose algebraico polinomial completo.
- **Validaciones en Tiempo Real:** Detección de caracteres no válidos de acuerdo a la base seleccionada (ej. rechazo de '2' en binario o '8' en octal).
- **Controles Stepper Intuitivos (+ / −):** Desactivación del scroll nativo involuntario y spinners del navegador en inputs numéricos, reemplazados por controles interactivos con soporte para pulsación simple y continua (press & hold).
- **Iconografía Minimalista Open Source:** Interfaz limpia sin emojis, estandarizada con iconos vectoriales SVG de Lucide Icons (MIT) adaptables a modo claro y oscuro.

---

## 7. Registro de Commits del Desarrollo

El desarrollo del proyecto se estructuró e integró cronológicamente mediante **commits semánticos** siguiendo el estándar *Conventional Commits*:

1. `2376ab2` - `first commit`: Inicialización del repositorio Git.
2. `4fe488d` - `chore: inicializar estructura del proyecto y arquitectura base`: Configuración de paquetes modulares `core`, `cli`, `web` y `tests`.
3. `c8dd007` - `feat(core): implementar conversion de decimal a otras bases mediante divisiones sucesivas`: Algoritmo euclidiano de divisiones sucesivas con registro detallado de pasos.
4. `bdf8f56` - `feat(core): implementar conversion de bases a decimal mediante combinacion lineal`: Descomposición formal en base canónica monomia y producto escalar.
5. `3123caf` - `feat(cli): crear interfaz de linea de comandos interactiva con procedimientos detallados`: Modo interactivo CLI para terminal con tablas y desgloses algebraicos.
6. `8c91a72` - `test: agregar suite de pruebas unitarias para algoritmos de conversion y casos limite`: Suite de 15 pruebas unitarias automatizadas con cobertura de casos límite y bidireccionalidad.
7. `86eceae` - `feat(server): implementar servidor http nativo y api rest en python estandar`: Servidor HTTP nativo en Python estándar sin dependencias de terceros.
8. `9820ba9` - `feat(web): disenar interfaz web moderna con soporte para temas y diseno responsivo`: Interfaz web SPA interactiva con modo claro/oscuro y diseño responsivo.
9. `0adc9d1` - `feat(web): integrar visualizadores interactivos para divisiones y combinaciones lineales`: Tablas dinámicas de división y cuadrículas posicionales vectoriales.
10. `f873fcb` - `docs: documentar fundamentos de algebra lineal y guia de uso en readme`: Documentación técnica de fundamentos matemáticos y manual de ejecución.
11. `f1b8208` - `refactor: consolidar lanzador principal, validaciones y pulido de experiencia de usuario`: Flags universales de ejecución (`--cli`, `--port`, `--no-browser`) y validaciones robustas.
12. `23438b9` - `Update README with team member names`: Inclusión formal de los integrantes del Grupo 10.
13. `67d2e89` - `feat(web): reemplazar scroll con stepper +/- y migrar interfaz a iconos minimalistas open source`: Controles stepper táctiles sin scroll numérico nativo e iconografía minimalista Lucide.
