# ARQUITECTURA.md - Diseño Técnico

## Principios Arquitectónicos

### 1. Separación Estricta de Responsabilidades

```
gauss.py     → GAUSS / REF (lógica pura; compatibilidad con nombres históricos)
gauss_jordan.py → GAUSS-JORDAN / RREF y soluciones paramétricas
vectores.py  → OPERACIONES Y PROPIEDADES DE R^n
formato.py   → PRESENTACIÓN texto (float → fracción/decimal, LaTeX, HTML) — sin deps
mathrender.py→ PRESENTACIÓN imagen (LaTeX → QPixmap con matplotlib mathtext)
main.py      → CONSOLA (input, print, flujo interactivo)
gui.py       → punto de entrada de la GUI (shim delgado hacia ui/)
ui/          → INTERFAZ GRÁFICA PyQt6 por pantallas (ver "Flujo de la GUI")
tests/       → VERIFICACIÓN (unittest, no parte del "ejercicio")
```

**Ventaja:** cada algoritmo puede probarse por separado. `gauss.py` conserva
funciones de compatibilidad para consumidores antiguos, `vectores.py` reutiliza
Gauss/Gauss-Jordan y `formato.py` centraliza *cómo se muestran* los números.

### 2. No Usar Librerías de Álgebra Lineal

**Prohibido:** NumPy, SymPy, scipy, cualquier "AL externa"

**Por qué:**
- El ejercicio exige comprensión profunda
- Entender cómo funciona el algoritmo es el objetivo
- Las librerías son "cajas negras"

**Consecuencia:** Implementamos TODO desde cero con listas y loops.

### 3. Funciones puras en los módulos de cálculo

```python
def escalonar(matriz, n_incognitas, registrar_paso=None):
    """Modifica matriz IN PLACE, devuelve columnas_pivote"""
    # NO hace print()
    # NO hace input()
    # NO accede a archivos
    # Operación: entrada → transformación → salida
```

La misma regla se aplica a `gauss_jordan.py` y `vectores.py`: no hacen
`input()`, `print()`, acceso a archivos ni llamadas a la GUI.

## Arquitectura de Capas

```
┌─────────────────────────────────────────────┐
│  INTERFAZ DE USUARIO                        │
│  ├─ gui.py (PyQt6)        [visual]         │
│  └─ main.py (consola)     [interactivo]    │
└──────────────┬────────────────────────────┘
               │ import
┌──────────────▼────────────────────────────┐
│  PRESENTACIÓN                             │
│  ├─ formato.py           [puro, sin deps] │
│  │   ├─ a_fraccion() (fracción continua)  │
│  │   ├─ formatear_valor() fracción/decimal│
│  │   ├─ generar_latex_solucion()          │
│  │   └─ helpers HTML (vector columna, …)  │
│  └─ mathrender.py     [matplotlib mathtext]│
│      ├─ latex_a_pixmap()  (LaTeX → QPixmap)│
│      └─ columna_a_pixmap() (vector dibujado)│
└──────────────┬────────────────────────────┘
               │ import
┌──────────────▼────────────────────────────┐
│  LÓGICA DE NEGOCIO                        │
│  ├─ gauss.py         [Gauss / REF]        │
│  ├─ gauss_jordan.py  [RREF / parámetros]  │
│  └─ vectores.py      [operaciones de R^n] │
└──────────────┬────────────────────────────┘
               │
┌──────────────▼────────────────────────────┐
│  DATOS & ALGORITMO                        │
│  ├─ Estructuras: listas de listas         │
│  ├─ Operaciones: loops y aritmética       │
│  └─ Tolerancia numérica: EPS = 1e-9       │
└─────────────────────────────────────────┘
```

## Flujo de Datos

### Sistema Determinado (Solución Única)

```
Usuario Input
    ↓
main.py:leer_sistema() → (coeficientes, terminos)
    ↓
gauss.py:crear_matriz_aumentada() → matriz aumentada
    ↓
gauss.py:escalonar() → forma escalonada + columnas_pivote
    ↓
gauss.py:clasificar() → "determinado"
    ↓
gauss.py:sustitucion_regresiva() → solución x
    ↓
gauss.py:verificar_solucion_detallada() → términos coef·x_j, suma, esperado
    ↓
formato.py:formatear_valor() → fracción exacta o decimal
    ↓
main.py:imprimir_verificacion() / gui.py:verification_html()
    → demostración término a término al usuario
```

### Sistema Indeterminado (Infinitas Soluciones)

```
Usuario Input
    ↓
gauss.py:escalonar() → REF + columnas_pivote
    ↓
gauss.py:clasificar() → "indeterminado"
    ↓
gauss_jordan.py:reducir_a_escalonada_reducida() → RREF
    ↓
gauss_jordan.py:solucion_parametrica() → (libres, expresiones)
    ↓
gauss_jordan.py:solucion_general_vectorial() → {particular, vectores_nulos}
    ↓
formato.py:generar_latex_solucion() → código LaTeX (con \frac)
    ↓
main.py/gui.py: mostrar resultado (GUI: notación matemática renderizada
                + diálogo aparte con análisis y LaTeX)
```

Los mismos nombres continúan disponibles desde `gauss.py` como delegados de
compatibilidad.

### Combinación lineal de vectores

```
Usuario ingresa v1 ... vp, pesos c1 ... cp y, si aplica, objetivo b
    ↓
ui/screen_vectores.py o main.py valida la entrada
    ↓
ui/state.py:Sesion (solo GUI) llama a vectores.py
    ↓
vectores.py:combinacion_lineal() → suma componente a componente
    o
vectores.py:es_combinacion_lineal() → [v1 ... vp | b]
    ↓
gauss.py + gauss_jordan.py → compatibilidad y pesos
    ↓
formato.py:latex_combinacion_lineal() → vectores columna
    ↓
Consola o pantalla de vectores muestra resultado y LaTeX
```

## Decisiones Técnicas y Justificación

### 1. Tolerancia Numérica: EPS = 1e-9

```python
EPS = 1e-9

def valor_casi_cero(valor):
    return -EPS < valor < EPS
```

**Razón:** Punto flotante no es exacto. 0.0000000001 es efectivamente cero.

**Consecuencia:** Comparaciones siempre con `valor_casi_cero()`, nunca con `== 0`

**Fuente única:** `EPS` se define en `gauss.py`. `gauss_jordan.py` y `vectores.py`
lo importan de ahí (p. ej. `iguales()` y la compatibilidad del sistema de pesos
en `es_combinacion_lineal`). No confundir con `ADR-0001`, que fija un umbral
distinto (`1e-4`, denominador ≤ 64) para interpretar y mostrar lo que teclea el
usuario.

### 2. Pivoteo Parcial en Eliminación

```python
# Elegir el elemento con mayor |valor| en la columna
fila_max = argmax(abs(matriz[i:][col]))
intercambiar(fila_max, fila_actual)
```

**Razón:**
- Evita división por cero
- Mejora estabilidad numérica
- Reduce errores de redondeo

**Consecuencia:** Orden de filas puede cambiar (pero la solución es la misma)

### 3. Módulos Separados (no una clase)

```python
# ✗ MALO: Encapsulación excesiva
class GaussEliminador:
    def __init__(self, matriz):
        self.matriz = matriz
    def escalonar(self):
        ...

# ✓ BUENO: Funciones puras
def escalonar(matriz, n_incognitas):
    ...
```

**Razón:** Ejercicio de procedimiento, no OOP. Más claro y testeable.

### 4. Sin Excepciones Innecesarias

```python
# ✗ NO: Lanzar excepciones por comportamiento esperado
if matriz_vacia:
    raise EmptyMatrixError()

# ✓ SÍ: Devolver datos que indiquen el estado
clasificacion = clasificar(matriz, n, columnas_pivote)
if clasificacion == "incompatible":
    # Manejar
```

**Razón:** El usuario podría dar una matriz vacía. No es un error del programa.

### 5. Capa de presentación aparte: `formato.py`

```python
# gauss.py trabaja SIEMPRE en float (el algoritmo no cambia).
# formato.py decide cómo se ve ese float:
formatear_valor(1/3, MODO_FRACCION)  # -> "1/3"
formatear_valor(1/3, MODO_DECIMAL)   # -> "0.3333"
```

**Razón:**
- La forma fraccionaria exacta (`1/3`, `-8/3`) es mucho más legible que `0.3333`
  para material educativo de álgebra lineal (issue #17).
- `main.py` y `gui.py` tenían cada uno su propio `format_number` duplicado.
- La conversión float → fracción se hace **a mano** (fracción continua + Euclides),
  sin importar `fractions`, para respetar la restricción del ejercicio.
- `generar_latex_solucion()` (presentación pura) se movió aquí desde `gauss.py`.

**Consecuencia:** cualquier interfaz nueva (p. ej. la TUI de Textual, issue #18)
reutiliza `formatear_valor` / los helpers HTML sin reimplementar nada.

### 6. GUI: notación matemática renderizada, no código LaTeX crudo (issue #15)

- `mathrender.py` convierte el LaTeX a imagen con el motor **mathtext de
  matplotlib** (no necesita una instalación de LaTeX del sistema). Matrices y
  vectores se dibujan a mano (`matriz_a_pixmap`, `columna_a_pixmap`) porque
  mathtext no soporta los entornos `pmatrix` / `array`.
- `mathrender.disponible()` degrada con elegancia: sin matplotlib, la GUI usa los
  helpers de texto/HTML de `formato.py` (nunca muestra LaTeX crudo). Por eso la
  GUI debe ejecutarse dentro del entorno de uv (`uv run python gui.py`).
- El código LaTeX no se muestra por defecto: está detrás de "Ver sintaxis LaTeX"
  en la última pantalla.
- Descartado por peso: `QWebEngineView` + KaTeX (+150 MB).

### 7. Flujo de la GUI: pantallas, no un único panel (paquete `ui/`)

`gui.py` es un shim; la GUI vive en `ui/` con una pantalla por archivo y un
`QStackedWidget` que las intercambia (`ui/app.py`):

```
Menú  →  Dimensiones y notación  →  Entrada guiada  →  Proceso y resultado  →  Solución vectorial
(info)   (n_eq, n_var, fracción)   (término a término)  (pasos + solución +      (render + LaTeX
                                                         comprobación + análisis) oculto)
```

Desde el menú existe además una ruta independiente a
`ui/screen_vectores.py`, que reúne combinación lineal, pertenencia y
verificación de propiedades sin alterar el flujo de sistemas `Ax = b`.

- Estado compartido en `ui/state.py:Sesion`; es el **único** punto de la GUI que
  llama a los módulos de cálculo. `Sesion.resolver()` produce un dict con pasos, tipo,
  rango/nulidad, solución, vectorial, verificación y LaTeX.
- Navegación **sin ratón**: Enter avanza (botón por defecto), Esc retrocede
  (atajo de ventana → `pantalla.al_atras()`), ← → recorren los pasos, F1 al menú.
- Widgets reutilizables en `ui/widgets.py`: `PantallaBase` (encabezado + barra de
  navegación), `MatrizGrid` (rejilla con corchetes y celda resaltable para la
  entrada), `boton_ayuda` (`QToolButton` con tooltip que también responde al
  teclado), `FilaAnalisis`.

### 8. Separación Gauss / Gauss-Jordan / vectores (issue #23)

- `gauss.py` conserva la eliminación hacia adelante, clasificación,
  sustitución regresiva, rango y verificaciones.
- `gauss_jordan.py` contiene RREF y las soluciones paramétricas/vectoriales.
- `vectores.py` contiene operaciones de `R^n` y solo importa módulos propios del
  proyecto para resolver pertenencia.
- Los nombres históricos movidos siguen accesibles desde `gauss.py`; sus imports
  locales evitan un ciclo durante la carga de los módulos.
- Cuando una combinación admite infinitos pesos, se elige la solución con
  parámetros libres iguales a cero. La decisión está en ADR-0002.

## Extensibilidad

### Agregar Nueva Funcionalidad

**Patrón:**

1. **Elegir el módulo puro correcto**: `gauss.py`, `gauss_jordan.py` o
   `vectores.py`.
2. **Agregar el test correspondiente** (`test_gauss.py`,
   `test_gauss_jordan.py` o `test_vectores.py`).
3. **Integrar en main.py o gui.py** según corresponda

**Ejemplo: Agregar método de Cramer**

```python
# 1. gauss.py
def determinante_2x2(a, b, c, d):
    return a*d - b*c

def determinante_nxn(matriz):
    # Implementación con cofactores
    ...

def cramer(coeficientes, terminos):
    # Usa determinantes
    ...

# 2. test_gauss.py
class TestCramer(unittest.TestCase):
    def test_determinante_2x2(self):
        assert determinante_2x2(1, 2, 3, 4) == -2

# 3. main.py
def resolver_sistema(coeficientes, terminos, n):
    # ... código Gauss existente ...
    # Agregar opción: usar Cramer para sistemas pequeños
```

## Testsabilidad

Las funciones de `gauss.py`, `gauss_jordan.py` y `vectores.py` son fáciles de
probar porque:

1. **Entrada simple:** Datos básicos (listas)
2. **Salida predecible:** Valores determinísticos
3. **Sin estado global:** No depende de nada afuera
4. **Sin I/O:** No lee ni escribe archivos

```python
# Fácil de testear
def rango_matriz(matriz, n):
    rango = 0
    for fila in matriz:
        if any(not valor_casi_cero(v) for v in fila[:n]):
            rango += 1
    return rango

# Test trivial
assert rango_matriz([[1, 2, 3], [0, 0, 0]], 3) == 1
```

## Performance

**No optimizado intencionalmente** (educativo):

- O(n³) para escalonar (aceptable para matrices pequeñas)
- Pivoteo linear O(n) por columna
- Copia full de matriz para pasos (registrar_paso)

**No usar para:**
- Matrices > 100×100
- Aplicaciones tiempo real
- Sistemas de precisión crítica

**Sí usar para:**
- Aprendizaje
- Enseñanza
- Demostración
- Matrices pequeñas (<20×20)

---

**Filosofía de diseño:** Claridad > Eficiencia > Elegancia
