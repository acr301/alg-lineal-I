# UI.md - Diseño de Interfaz y Formato de Presentación

Este documento detalla las decisiones de diseño visual, accesibilidad y la arquitectura de formato de texto aplicadas en la interfaz de Aqua Gauss (Tarea 3).

## 1. Paleta de Colores y Contrastes (Flat Design)

Se abandonó el uso de degradados (`qlineargradient`) en favor de un diseño plano y profesional. Esto mejora la legibilidad de las matrices complejas y mantiene una estética académica formal.

**Esquema de color principal (`ui/theme.py`):**
* **Texto principal:** `#153653` (Azul oscuro profundo).
* **Botones primarios y acentos:** `#0685cc` (Azul claro sólido) con interacciones `hover` en `#0695dc`.
* **Fondos de la ventana:** `#dff7ff`.

**Accesibilidad (Contraste AA):**
Las combinaciones elegidas garantizan el cumplimiento de los estándares de accesibilidad AA (W3C). El texto blanco (`#ffffff`) sobre los botones primarios (`#0685cc`) y el texto oscuro (`#153653`) sobre fondos claros permiten que la notación matemática renderizada sea legible sin fatiga visual.

## 2. Motor de Formato Numérico y Tipográfico

El módulo `formato.py` centraliza toda la presentación del sistema. Se independiza completamente de la lógica algebraica de `gauss.py`, operando como una capa de presentación pura.

### Subíndices Unicode

Para cumplir con la notación matemática estricta ($a_{11}$, $b_1$, $x_1$, $t_1$) sin depender exclusivamente del motor de renderizado LaTeX, se implementaron *helpers* que inyectan caracteres Unicode directamente en los strings de Python. Se erradicó por completo el texto plano quemado (ej. `x1` o `t1`).

**Funciones clave (`formato.py`):**

```python
# 1. Generador de subíndices
def subindice(numero):
    """'1' -> '₁'. Cae a dígitos ASCII si hace falta."""

# 2. Generador de variables de sistema
def var(indice, nombre="x"):
    """var(1, 'x') -> 'x₂', var(0, 'E') -> 'E₁'"""

# 3. Generador de variables libres (parámetros)
def parametro(indice):
    """parametro(0) -> 't₁'"""
