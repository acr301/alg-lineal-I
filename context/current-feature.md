# Current Feature: Verificación Explícita de la Solución (semana2/tarea1)

## Status

In Progress

## Goals

- Agregar en `gauss.py` una función pura (sin imports) que sustituya una solución `x` en
  la matriz de coeficientes original `A` y el vector `b`, y devuelva por cada ecuación el
  valor calculado (lado izquierdo) vs. el término independiente esperado (`b_i`), y si
  coinciden dentro de la tolerancia `EPS`.
- En `main.py`, mostrar esa verificación al usuario justo después de imprimir la
  solución, en los 3 casos:
  - Determinado: sustituir la solución única.
  - Indeterminado: sustituir con al menos un valor concreto del/los parámetro(s) libres
    (p. ej. t=0 o t=1) para demostrar que la solución paramétrica satisface el sistema.
  - Inconsistente: no aplica (no hay solución que verificar); no mostrar este paso.
- Agregar tests en `test_gauss.py` para la nueva función de verificación.

## Notes

- Fuente: enunciado oficial de la Tarea 1 (sección "Salida y Verificación"), que exige
  "comprobar automáticamente la solución sustituyendo los valores obtenidos en el sistema
  original para verificar la igualdad".
- Issue de referencia: https://github.com/acr301/alg-lineal-I/issues/3
- No modificar la lógica de eliminación/clasificación existente (`escalonar`, `clasificar`,
  `sustitucion_regresiva`, `solucion_parametrica`), solo agregar la verificación como paso
  adicional.
- Restricción vigente: sin numpy/scipy/math ni funciones de álgebra lineal ya dadas en
  Python. Solo listas, bucles, condicionales y aritmética básica.
- Flujo git acordado: crear rama de feature, implementar, merge local a main, y hacer push
  a origin (repo `acr301/alg-lineal-I`, usar `git config core.sshCommand` con la llave
  `~/.ssh/gh_macbook_Auth` ya configurada en este repo).

## History

### Eliminación Gaussiana Interactiva (semana2/tarea1)

Programa interactivo en Python (`semana2/tarea1/`) que resuelve sistemas Ax=b mediante
eliminación de Gauss con pivoteo parcial (reducción a forma escalonada), implementado sin
numpy ni ninguna función de álgebra lineal ya dada en Python (solo listas, bucles y
aritmética básica). Muestra cada paso de la reducción, clasifica el sistema (compatible
determinado / indeterminado con solución paramétrica / incompatible), e incluye tests
(`test_gauss.py`) para la lógica pura. Mergeado a `main` (rama
`feature/eliminacion-gaussiana-interactiva` eliminada). Pendiente: interfaz gráfica con
PyQt (fuera de alcance de este feature).
