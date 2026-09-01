# ARQUITECTURA.md - Diseño Técnico

## Principios Arquitectónicos

### 1. Separación Estricta de Responsabilidades

```
gauss.py   → LÓGICA PURA (sin I/O, sin efectos secundarios, sin imports)
formato.py → PRESENTACIÓN (float → texto: fracciones, notación matemática, LaTeX)
main.py    → CONSOLA (input, print, flujo interactivo)
gui.py     → INTERFAZ GRÁFICA (PyQt6, eventos, widgets)
tests/     → VERIFICACIÓN (unittest, no parte del "ejercicio")
```

**Ventaja:** `gauss.py` puede ser usado por cualquier interfaz sin duplicar lógica,
y `formato.py` centraliza *cómo se muestran* los números (antes cada interfaz tenía
su propio `format_number` duplicado).

### 2. No Usar Librerías de Álgebra Lineal

**Prohibido:** NumPy, SymPy, scipy, cualquier "AL externa"

**Por qué:**
- El ejercicio exige comprensión profunda
- Entender cómo funciona el algoritmo es el objetivo
- Las librerías son "cajas negras"

**Consecuencia:** Implementamos TODO desde cero con listas y loops.

### 3. Pure Functions en gauss.py

```python
def escalonar(matriz, n_incognitas, registrar_paso=None):
    """Modifica matriz IN PLACE, devuelve columnas_pivote"""
    # NO hace print()
    # NO hace input()
    # NO accede a archivos
    # Operación: entrada → transformación → salida
```

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
│  └─ formato.py            [puro, sin deps]│
│     ├─ a_fraccion() (fracción continua)   │
│     ├─ formatear_valor() fracción/decimal │
│     ├─ generar_latex_solucion()           │
│     └─ helpers HTML (vector columna, …)   │
└──────────────┬────────────────────────────┘
               │ import
┌──────────────▼────────────────────────────┐
│  LÓGICA DE NEGOCIO                        │
│  └─ gauss.py                [puro]        │
│     ├─ Eliminación Gaussiana              │
│     ├─ Análisis de Rango/Nulidad          │
│     ├─ Formas Escalonadas                 │
│     ├─ Solución Vectorial                 │
│     └─ Verificación (detallada)           │
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
gauss.py:reducir_a_escalonada_reducida() → RREF
    ↓
gauss.py:solucion_parametrica() → (libres, expresiones)
    ↓
gauss.py:solucion_general_vectorial() → {particular, vectores_nulos}
    ↓
formato.py:generar_latex_solucion() → código LaTeX (con \frac)
    ↓
main.py/gui.py: mostrar resultado (GUI: notación matemática renderizada
                + diálogo aparte con análisis y LaTeX)
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

- El resultado de `gui.py` se compone con notación matemática (subíndices `x₁`,
  signo `−`, `·`, vectores columna entre corchetes vía rich-text de Qt).
- El código LaTeX y el análisis de rango/nulidad se movieron a un `QDialog`
  ("Ver análisis y LaTeX ↗") para descargar el panel "3 · Proceso y resultado".
- Enfoque deliberado: **sin dependencias nuevas**. Opciones de mayor fidelidad
  (matplotlib `mathtext`, `QWebEngineView` + KaTeX) quedan documentadas en el
  issue #15 para una iteración futura.

## Extensibilidad

### Agregar Nueva Funcionalidad

**Patrón:**

1. **Implementar en gauss.py** como función pura
2. **Agregar test en test_gauss.py** que verifique
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

Cada función en `gauss.py` es testeada porque:

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
