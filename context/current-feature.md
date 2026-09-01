# Current Feature: Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas

## Status

Complete

## Goals

- Implementar `solucion_general_vectorial()` en gauss.py para expresar soluciones como x = xp + t1*v1 + ... + tk*vk
- Implementar `rango_matriz()` para calcular el rango de una matriz
- Implementar `verificar_rango_nulidad()` para verificar que Rango(A) + Nulidad(A) = n
- Implementar `es_forma_escalonada()` para detectar forma escalonada por filas
- Implementar `es_forma_escalonada_reducida()` para detectar forma escalonada reducida
- Implementar `clasificar_forma_escalonada()` para clasificar como REF, RREF o ninguna
- Generar código LaTeX copiable de la solución vectorial
- Agregar interfaz en GUI: QTextEdit para LaTeX + botón "Copiar LaTeX"
- Mostrar en GUI: Rango(A), n - Rango(A), verificación rango-nulidad, solución vectorial, LaTeX, clasificación
- Escribir tests exhaustivos para determinado, indeterminado, incompatible, rango, variables libres, rango-nulidad, solución vectorial, REF, RREF, etc.

## Notes

- Respeta separación: gauss.py = lógica pura, main.py = consola, gui.py = PyQt6
- Prohibido: NumPy, SymPy, librerías de álgebra lineal externas
- No romper funcionalidades existentes
- Tests en test_gauss.py y test_main.py
- Rama: feature/solucion-vectorial-rango-latex-formas

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
