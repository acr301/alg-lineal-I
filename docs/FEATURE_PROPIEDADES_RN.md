# Feature: Propiedades algebraicas de R^n

## Resumen

Esta rama implementa el issue #23 como trabajo de **Andrés Castillo**. Agrega
operaciones con vectores de `R^n`, combinaciones lineales y la verificación de
los ocho axiomas de espacio vectorial. Los vectores se presentan como columnas
y la notación copiable se integra con el LaTeX que ya tenía la aplicación.

La implementación se hizo sobre la arquitectura existente y sin librerías de
álgebra lineal. Los cálculos usan listas, ciclos, aritmética básica y los
algoritmos de Gauss/Gauss-Jordan del proyecto.

## Alcance implementado

### Operaciones en `vectores.py`

- `suma(u, v)`
- `producto_escalar(c, v)`
- `vector_cero(n)`
- `opuesto(v)`
- `iguales(u, v)`
- `combinacion_lineal(vectores, pesos)`
- `es_combinacion_lineal(objetivo, vectores)`
- `verificar_propiedades(u, v, w, a, b)`

`es_combinacion_lineal` coloca los vectores `v1, ..., vp` como columnas de la
matriz de coeficientes y resuelve el sistema asociado. Devuelve si el vector
objetivo pertenece al espacio generado y, cuando pertenece, un conjunto de
pesos que reproduce el objetivo.

Cuando hay infinitas respuestas, se elige la solución que asigna cero a los
parámetros libres. Esta convención se propone formalmente en
`docs/ADR-0002-pesos-combinacion-lineal.md`.

### Ocho propiedades verificadas

1. Conmutatividad de la suma.
2. Asociatividad de la suma.
3. Elemento neutro aditivo.
4. Inverso aditivo.
5. Identidad escalar.
6. Asociatividad del producto por escalares.
7. Distributividad respecto de la suma de vectores.
8. Distributividad respecto de la suma de escalares.

### Separación de algoritmos

La reducción RREF y la construcción de soluciones paramétricas viven ahora en
`gauss_jordan.py`. `gauss.py` conserva funciones de compatibilidad, por lo que
el código que ya usaban la consola, la GUI y los tests sigue funcionando sin
cambiar sus llamadas.

### Presentación e interfaces

- `formato.py` genera texto y LaTeX con vectores columna.
- `main.py` ofrece un menú de consola para las tres operaciones vectoriales.
- `ui/screen_vectores.py` agrega una pantalla gráfica para calcular una
  combinación, comprobar pertenencia o revisar las ocho propiedades.
- `ui/state.py` mantiene el mismo patrón existente: la pantalla no llama
  directamente a los algoritmos.

## Notación usada

Para una combinación lineal se mantiene la convención

```text
b = c1 v1 + c2 v2 + ... + cp vp
```

En LaTeX, `b` y cada `vk` se escriben con `bmatrix`, por lo que aparecen como
vectores columna. Los pesos se escriben como `c_1, ..., c_p` y los vectores como
`v_1, ..., v_p`.

## Cómo probarlo

Desde la raíz del repositorio:

```bash
uv sync
uv run --extra dev pytest
```

Para probar la interfaz gráfica:

```bash
cd semana2/tarea1
uv run python gui.py
```

Luego elegir **Vectores y propiedades de R^n** en el menú principal.

Caso corto para combinación lineal en `R^2`:

```text
v1 = [1, 2]    c1 = 2
v2 = [3, -1]   c2 = -1
resultado esperado = [-1, 5]
```

Para comprobar pertenencia, usar los mismos vectores y el objetivo `[-1, 5]`.
La aplicación debe responder que sí pertenece y mostrar pesos válidos.

## Pruebas agregadas

- `test_gauss_jordan.py`: reducción, clasificación y solución paramétrica.
- `test_vectores.py`: operaciones, pertenencia, casos incompatibles y axiomas.
- `test_formato.py`: LaTeX y texto de combinaciones con vectores columna.
- `test_main.py`: integración del flujo de consola.
- `test_ui.py`: apertura de pantalla, cálculo y verificación de propiedades.

Resultado local al cerrar la rama: **71 tests aprobados**.

## Historial previo al cierre documental

Los cambios se separaron por responsabilidad para facilitar la revisión:

1. `3a348b0` — separa la lógica de Gauss-Jordan.
2. `5bcfa3b` — agrega pruebas directas de Gauss-Jordan.
3. `6996b2a` — implementa vectores, combinaciones y propiedades.
4. `726cd53` — agrega presentación con vectores columna y LaTeX.
5. `e3b13ea` — integra el flujo de consola.
6. `6f9086c` — integra la pantalla gráfica.
7. `f7a2203` — agrega la guía inicial y actualiza el estado compartido.

## Límites respetados

Esta rama no modifica la configuración de dependencias, la paleta general ni
la notación global de subíndices. La documentación general solo recibe las
secciones necesarias para explicar el issue #23; el versionado, changelog y
demás housekeeping permanecen en su issue correspondiente.
