# Current Feature: LaTeX renderizado, verificación explícita y fracciones

## Status

In Progress — implementado en `fix/latex-renderizado-fracciones-verificacion`,
pendiente de PR/merge.

## Goals

- [x] **Notación matemática renderizada en la GUI (#15).** Resultado con subíndices
  `x₁`, signo `−`, `·` y vectores columna entre corchetes (rich-text de Qt, sin
  dependencias). Análisis de rango/nulidad y código LaTeX movidos a un `QDialog`
  ("Ver análisis y LaTeX ↗"); el panel "3 · Proceso y resultado" queda más limpio.
- [x] **Demostración de la comprobación sustituyendo valores (#16).**
  `verificar_solucion_detallada()` en `gauss.py` expone los términos `coef·xⱼ`;
  consola y GUI muestran `1·(5) + 1·(3) + 1·(-2) = 5 + 3 − 2 = 6 = 6`.
  `verificar_solucion()` pasa a ser vista resumida de la detallada.
- [x] **Matriz en fracción exacta en el paso a paso y tablas (#17).** `formato.py`
  con `a_fraccion()` (fracción continua) / `mcd()` (Euclides) / `formatear_valor()`,
  sin `import`. Matriz, pasos, forma final, vectores y verificación en fracción por
  defecto; toggle "Fracción ⇄ Decimal" en la GUI y `--decimal/--fraccion` en consola.
- [x] `main.py` y `gui.py` dejan de duplicar `format_number`; usan `formato.py`.
  `generar_latex_solucion()` movida de `gauss.py` a `formato.py` (usa `\frac`;
  corregido el bug que borraba los ceros de `x_p`).
- [x] Tests nuevos: `test_formato.py` (11) + `TestVerificarSolucionDetallada` en
  `test_gauss.py`. Suite: 35 tests en verde (`uv run --extra dev pytest`).
- [x] Documentación actualizada (`README.md`, `AGENTS.md`, `docs/ARQUITECTURA.md`,
  `docs/ALGORITMO.md`).
- [ ] Abrir PR y mergear a `main` (pendiente de confirmación del usuario).

## Notes

- Issues: #15 (LaTeX renderizado + declutter), #16 (verificación sustituyendo
  valores), #17 (fracciones), #18 (migración a Textual TUI — solo issue/investigación,
  no se implementa en esta rama).
- Rama: `fix/latex-renderizado-fracciones-verificacion`.
- Restricción vigente: `gauss.py` sin librerías externas ni stdlib. El helper de
  fracciones vive en `formato.py` (capa de presentación) y también evita `import`
  para mantener el espíritu del ejercicio.
- El algoritmo sigue trabajando en `float`; las fracciones son solo presentación.

## History

### Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas (semana2/tarea1)

Implementa análisis avanzado de sistemas lineales en `gauss.py` sin librerías externas:
- `rango_matriz()` calcula el rango de una matriz
- `verificar_rango_nulidad()` verifica Rango(A) + Nulidad(A) = n
- `es_forma_escalonada()` y `es_forma_escalonada_reducida()` detectan REF/RREF
- `clasificar_forma_escalonada()` clasifica la forma escalonada
- `solucion_general_vectorial()` expresa soluciones como x = xp + t1*v1 + ... + tk*vk
- `generar_latex_solucion()` genera código LaTeX copiable

Integración en `main.py`: muestra rango, nulidad, forma escalonada y solución vectorial.
Interfaz PyQt6 en `gui.py`: panel de análisis avanzado con QTextEdit para LaTeX y botón "Copiar LaTeX".
Tests exhaustivos: 18 nuevos tests en `test_gauss.py` (todos pasan).
Mergeado a `main` (rama `feature/solucion-vectorial-rango-latex-formas` eliminada).

### Verificación Explícita de la Solución (semana2/tarea1)

Agrega `verificar_solucion()` y `evaluar_solucion_parametrica()` a `gauss.py` (sin
librerías) para sustituir la solución hallada en el sistema original `[A | b]` y
comprobar la igualdad, tal como exige el enunciado de la Tarea 1. `main.py` ahora
muestra esta comprobación ecuación por ecuación tras imprimir la solución, tanto para
sistemas determinados (solución única) como indeterminados (con un valor concreto de
ejemplo para los parámetros libres). No aplica al caso inconsistente. Tests agregados en
`test_gauss.py`. Cierra el issue acr301/alg-lineal-I#3. Mergeado a `main` (rama
`feature/verificacion-explicita-solucion` eliminada).

### Eliminación Gaussiana Interactiva (semana2/tarea1)

Programa interactivo en Python (`semana2/tarea1/`) que resuelve sistemas Ax=b mediante
eliminación de Gauss con pivoteo parcial (reducción a forma escalonada), implementado sin
numpy ni ninguna función de álgebra lineal ya dada en Python (solo listas, bucles y
aritmética básica). Muestra cada paso de la reducción, clasifica el sistema (compatible
determinado / indeterminado con solución paramétrica / incompatible), e incluye tests
(`test_gauss.py`) para la lógica pura. Mergeado a `main` (rama
`feature/eliminacion-gaussiana-interactiva` eliminada). Pendiente: interfaz gráfica con
PyQt (fuera de alcance de este feature).
