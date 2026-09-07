# ADR-0002 · Pesos cuando una combinación lineal no es única

**Estado:** propuesta · **Fecha:** 2026-09-07 · **Ámbito:** `vectores.py`

## Contexto

Para saber si un vector objetivo `b` es combinación lineal de
`v1, ..., vp`, la aplicación resuelve el sistema cuyas columnas son esos
vectores:

```text
[v1  v2  ...  vp | b]
```

El sistema puede ser compatible indeterminado. En ese caso, el objetivo sí es
combinación lineal, pero existen infinitas listas de pesos válidas. La interfaz
necesita devolver y mostrar una respuesta concreta y reproducible.

## Decisión propuesta

Cuando el sistema de pesos sea indeterminado:

1. Gauss-Jordan obtiene las variables libres y sus expresiones paramétricas.
2. Se asigna `0` a cada parámetro libre.
3. Se evalúan las expresiones y se devuelve ese conjunto particular de pesos.

El resultado público continúa siendo:

```python
(True, pesos)
```

La respuesta indica que el objetivo pertenece al espacio generado; no afirma
que los pesos encontrados sean únicos.

## Razones

- Produce siempre la misma salida para la misma entrada.
- Reutiliza la solución paramétrica que ya calcula `gauss_jordan.py`.
- Evita pedir valores adicionales al usuario solo para escoger una solución.
- Suele producir una respuesta sencilla al anular las variables libres.

## Consecuencias

- **+** Consola, GUI y tests reciben una lista concreta de pesos.
- **+** La combinación devuelta puede verificarse sustituyéndola en
  `combinacion_lineal`.
- **−** Pueden existir otras listas de pesos igualmente correctas.
- **−** La salida no describe por sí sola toda la familia de soluciones.

Si en una tarea futura se necesita mostrar la familia completa, puede añadirse
otra función sin cambiar el contrato actual de `es_combinacion_lineal`.
