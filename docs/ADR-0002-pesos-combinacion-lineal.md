# ADR-0002 · Pesos cuando una combinación lineal no es única

**Estado:** propuesta · **Fecha:** 2026-09-07 · **Ámbito:** `vectores.py`

## Terminología

En este proyecto **pesos** = los coeficientes escalares `c1, ..., cp` de la
combinación lineal `b = c1·v1 + ... + cp·vp`. Se mantiene la palabra «pesos»
por consistencia con la traducción española de Lay y con los nombres ya usados
en el código (`combinacion_lineal(vectores, pesos)`). El término estándar
equivalente es *coeficientes*. Ver `docs/GLOSARIO.md`.

## Contexto

Para saber si un vector objetivo `b` es combinación lineal de `v1, ..., vp`, la
aplicación resuelve el sistema cuyas columnas son esos vectores:

```text
[v1  v2  ...  vp | b]
```

El sistema puede ser compatible indeterminado. En ese caso, el objetivo sí es
combinación lineal, pero existen infinitas listas de pesos válidas. La interfaz
necesita devolver y mostrar una respuesta concreta y reproducible.

### Cuándo el sistema de pesos es indeterminado

El sistema tiene infinitas soluciones cuando la matriz `[v1 ... vp]` deja al
menos una columna sin pivote tras la reducción. Esto ocurre en dos casos:

- **Caso 1 — más vectores que dimensiones (`p > n`).** Por ejemplo, 3 vectores
  en `R^2`. Como mucho puede haber `n` columnas pivote, así que al menos
  `p - n` pesos quedan libres.
- **Caso 2 — vectores linealmente dependientes (`p ≤ n`).** Algún `vk` es
  combinación lineal de los demás, de modo que su columna no aporta un pivote
  nuevo y el peso correspondiente queda libre.

En ambos casos, las columnas sin pivote de la RREF son las variables (pesos)
libres.

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

### Qué significa fijar las libres en `0`

Las columnas **pivote** de `[v1 ... vp]` corresponden a un subconjunto
linealmente independiente que genera el mismo subespacio que todos los `vk`
juntos: una **base** de ese subespacio (ver `docs/GLOSARIO.md`). Anular los
parámetros libres equivale a decir:

> «Representa `b` usando solo los vectores asociados a columnas pivote; los
> vectores redundantes reciben peso `0`.»

Por eso no es un resultado arbitrario entre infinitos: es la combinación que
usa la base que la propia eliminación ya identificó.

## Razones

- Produce siempre la misma salida para la misma entrada.
- Reutiliza la solución paramétrica que ya calcula `gauss_jordan.py`.
- Evita pedir valores adicionales al usuario solo para escoger una solución.
- Suele producir una respuesta sencilla al anular las variables libres.
- La combinación devuelta se apoya en una base explícita (columnas pivote), no
  en una elección sin criterio.

## Precisión numérica

- La **compatibilidad** del sistema y la comparación de vectores (`iguales`)
  usan la tolerancia única del proyecto, `EPS = 1e-9`, definida en `gauss.py` e
  importada por `vectores.py`. Es la misma que emplea toda la eliminación; su
  justificación está en `docs/ARQUITECTURA.md` §1 (Decisiones Técnicas).
- La **interpretación de lo que teclea el usuario** —cuándo un decimal se
  ajusta a una fracción exacta y cuándo se deja como decimal— se rige aparte
  por `docs/ADR-0001-entrada-numerica.md` (umbral `1e-4`, denominador ≤ 64).
  `EPS` y ese umbral son decisiones distintas y no deben confundirse.

## Nota de implementación: nombres históricos en `gauss.py`

`gauss.py` conserva delegadores (`reducir_a_escalonada_reducida`,
`solucion_parametrica`, `evaluar_solucion_parametrica`,
`solucion_general_vectorial`) que reenvían a `gauss_jordan.py`. Existen porque
`main.py` y `ui/state.py` todavía importan esos nombres desde `gauss`. No hay
consumidores fuera del repositorio; cuando esos dos módulos importen
directamente de `gauss_jordan`, los delegadores pueden eliminarse. `vectores.py`
(código nuevo) ya importa de `gauss_jordan` sin pasar por el delegador.

## Consecuencias

- **+** Consola, GUI y tests reciben una lista concreta de pesos.
- **+** La combinación devuelta puede verificarse sustituyéndola en
  `combinacion_lineal`.
- **+** Los pesos devueltos corresponden a una base identificable (columnas
  pivote), lo que hace la respuesta explicable.
- **−** Pueden existir otras listas de pesos igualmente correctas.
- **−** La salida no describe por sí sola toda la familia de soluciones.

Si en una tarea futura se necesita mostrar la familia completa, puede añadirse
otra función sin cambiar el contrato actual de `es_combinacion_lineal`.
