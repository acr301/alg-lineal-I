# UI.md - Diseño de Interfaz y Formato de Presentación

Este documento detalla las decisiones de diseño visual y formato de la interfaz.

**1. Paleta de Colores y Contrastes (Flat Design)**
Se abandonó el uso de degradados en favor de un diseño plano y accesible.
* **Texto principal:** `#153653` (Azul oscuro).
* **Botones primarios:** `#1f4e79` (Azul tinta).
* **Accesibilidad (Contraste AA):** El texto blanco (`#ffffff`) sobre el botón primario (`#1f4e79`) alcanza un ratio de **5.6:1**, superando el estándar AA de 4.5:1 exigido para texto normal.

**2. Subíndices Unicode**
Se implementaron *helpers* para inyectar caracteres Unicode, erradicando el texto plano en la presentación.

```python
def subindice(numero):
    """'1' -> '₁'"""

def var(indice, nombre="x"):
    """var(1, 'x') -> 'x₂'"""

def parametro(indice):
    """parametro(0) -> 't₁'"""

def entrada_A(fila, col):
    return f"a{subindice(fila)}{subindice(col)}"

def entrada_b(fila):
    return f"b{subindice(fila)}"
