# Current Feature

## Status

Not Started

## Goals

<!-- goals go here -->

## Notes

<!-- notes go here -->

## History

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
