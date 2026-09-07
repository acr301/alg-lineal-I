# Current Feature

## Status

Ready for review — rama publicada, PR pendiente

## Goals

- Implementar el issue #23: propiedades algebraicas de `R^n`.
- Separar Gauss-Jordan sin romper las llamadas existentes.
- Integrar combinaciones lineales con vectores columna y LaTeX.
- Ofrecer los cálculos desde consola y GUI.
- Mantener los algoritmos libres de librerías externas de álgebra lineal.

## Notes

- Rama local: `feature/propiedades-algebraicas-rn`.
- Responsable: Andrés Castillo.
- Verificación actual: 71 tests aprobados.
- Guía de revisión: `docs/FEATURE_PROPIEDADES_RN.md`.
- Rama publicada en `origin/feature/propiedades-algebraicas-rn`; `main` no fue
  modificado y todavía no se creó el PR.
- Fuera de alcance para evitar conflictos: subíndices globales, cambios de
  paleta/degradados y housekeeping de metadatos, versionado y changelog.

## History

### Propiedades algebraicas de R^n y combinaciones lineales (semana2/tarea1)

Implementación local del issue #23 en la rama `feature/propiedades-algebraicas-rn`.
Agrega `vectores.py` con operaciones puras, pertenencia a un espacio generado y
verificación de los ocho axiomas; separa la reducción RREF en `gauss_jordan.py`
manteniendo compatibilidad desde `gauss.py`; integra notación LaTeX con vectores
columna, consola y una pantalla de GUI. No usa NumPy, SymPy ni rutinas externas
de álgebra lineal. Incluye pruebas de algoritmo, formato, consola y GUI. Estado:
listo para revisión local, con 71 tests aprobados. Documentación detallada en
`docs/FEATURE_PROPIEDADES_RN.md`.

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

### Migración a uv (raíz del repo)

`pyproject.toml` + `uv.lock` versionados; documentación agnóstica de herramienta.
Cierra acr301/alg-lineal-I#13. Mergeado a `main` vía PR #14 (`67ae726`), rama
`chore/docs-y-migracion-a-uv` eliminada.

### Notación matemática renderizada y rediseño de la GUI por pantallas (semana2/tarea1)

- **Presentación** (`formato.py`, sin imports): `a_fraccion()` (fracción continua +
  Euclides), `formatear_valor(v, modo)` (fracción vs decimal, tope de denominador 64),
  `normalizar_entrada()` (ADR-0001: lo tecleado se ajusta a fracción tidy o a 4
  decimales), `generar_latex_solucion()` (con `\frac`), `texto/latex_verificacion()`,
  helpers HTML.
- **`gauss.py`**: `verificar_solucion_detallada()` (términos `coef·xⱼ` para la
  comprobación; `verificar_solucion()` queda como vista resumida). `escalonar` y
  `reducir_a_escalonada_reducida` aceptan `formato_numero` → el multiplicador de cada
  paso sale como fracción (`F2 ← F2 − (1/2)·F1`).
- **`mathrender.py`**: LaTeX → `QPixmap` con matplotlib mathtext (`latex_a_pixmap`,
  `columna_a_pixmap`, `matriz_a_pixmap`); degrada a texto/HTML si falta matplotlib
  (nunca muestra LaTeX crudo). `matplotlib` en `pyproject.toml` solo como render.
- **GUI reescrita en `ui/`** (paquete, una pantalla por archivo, `QStackedWidget`):
  menú → dimensiones y notación → entrada guiada término a término → proceso y
  resultado (pasos protagonistas + solución + comprobación + análisis) → solución
  vectorial (código LaTeX oculto tras "Ver sintaxis LaTeX"). Navegable sin ratón
  (Enter/Esc/←→/F1). Contenido en columna centrada; info de la app en un pie.
  `gui.py` es un shim → `ui.app.main`. `ui/state.py:Sesion` es el único punto de la
  GUI que llama a `gauss.py`.
- **ADR-0001** en `docs/ADR-0001-entrada-numerica.md`.
- Bugs de UI: `qt.qpa.fonts` "Segoe UI" (fuente elegida por código), tooltips
  (`QToolButton`), y #22 (crash al doble clic en "Ejemplo rápido" del menú →
  `ui/widgets.ListaOpciones` + guarda en `_activar`).
- Autores: **Andrés Castillo y Fátima Zogaib (Grupo 7)**.
- Tests: `test_formato.py`, `test_mathrender.py`, `test_ui.py` nuevos; 44 en verde.
- Mergeado a `main` vía PR #21 (`be2d169`). Cierra #15, #16, #17, #19, #20, #22.
  Ramas `feature/gui-multipantalla-y-notacion-matematica` y
  `fix/latex-renderizado-fracciones-verificacion` eliminadas.
- Cerrados como stale (resueltos en PR #12 mergeado): #9, #10, #11.
- Pendiente (fuera de alcance): #18 (migración de la consola a Textual TUI), #4.
