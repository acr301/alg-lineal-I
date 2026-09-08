# Glosario de terminología

Términos de álgebra lineal usados en el código, los docs y los ADR, con la
forma que se prefiere en este proyecto. Objetivo: que consola, GUI, tests y
documentación digan lo mismo con las mismas palabras.

| Inglés | En el proyecto (ES) | Definición breve |
|---|---|---|
| linear combination | combinación lineal | `c1·v1 + c2·v2 + ... + cp·vp` |
| weights / coefficients | **pesos** ( = coeficientes escalares) | los `ck` de la combinación lineal. Se usa «pesos» por consistencia con Lay (ed. española) y con `combinacion_lineal(vectores, pesos)`; *coeficientes* es el equivalente estándar |
| scalar | escalar | número que multiplica a un vector; la función `escalar(c, v)` hace `c·v` |
| span | espacio / subespacio generado — `gen{v1, ..., vp}` | conjunto de **todas** las combinaciones lineales de los vectores dados |
| target vector | objetivo (`b`) | vector cuya pertenencia al generado se comprueba en `es_combinacion_lineal` |
| linearly independent | linealmente independientes | ningún vector del conjunto es combinación lineal de los otros |
| linearly dependent | linealmente dependientes | algún vector es combinación lineal de los otros (hay redundancia) |
| basis / basis vectors | base / vectores de una base | conjunto linealmente independiente que genera el (sub)espacio. En `es_combinacion_lineal`, las **columnas pivote** de `[v1 ... vp]` forman una base del subespacio que generan todos los `vk` |
| pivot column | columna pivote | columna con pivote en la RREF; aporta un vector «de la base» |
| free variable | variable libre / parámetro libre | columna **sin** pivote en la RREF. En el sistema de pesos se fija en `0` (ver `ADR-0002`) |
| REF | forma escalonada (FE) | ceros bajo cada pivote |
| RREF | forma escalonada reducida (FER) | además, cada pivote vale 1 y es el único no nulo de su columna |
| the eight axioms | los ocho axiomas | propiedades de espacio vectorial que evalúa `verificar_propiedades(u, v, w, a, b)` |
| tolerance | tolerancia `EPS = 1e-9` | umbral **absoluto** para tratar un valor como cero al comparar `float`. Fuente única: `gauss.py`; lo importan `gauss_jordan.py` y `vectores.py`. Ver `ARQUITECTURA.md` §1 |

## Notas de consistencia

- **«pesos» vs «coeficientes».** El código y los ADR usan **pesos**. En prosa
  nueva orientada a quien estudia, «coeficientes (pesos)» también es aceptable;
  no mezclar los dos términos en la misma explicación sin aclararlo.
- **«variable libre».** Usar siempre esta forma (no «parámetro» a secas ni
  «grado de libertad») para las columnas sin pivote.
- **`EPS` (1e-9) vs `ADR-0001` (1e-4).** Son decisiones distintas: `EPS`
  compara resultados de punto flotante; `ADR-0001` decide cómo se interpreta y
  se muestra lo que teclea el usuario. No citarlas como si fueran la misma.
- **`R^n` / `Rⁿ`.** En texto plano y código: `R^n`. En la GUI y LaTeX: `Rⁿ`.

## Ver también

- `docs/ADR-0001-entrada-numerica.md` — normalización de la entrada numérica.
- `docs/ADR-0002-pesos-combinacion-lineal.md` — pesos cuando la combinación no
  es única.
- `docs/ALGORITMO.md` — desarrollo matemático de cada operación.
