# Current Feature: Consolidación core/ + clients/ (MVC), CI/Release y housekeeping (#28, #27, #26)

## Status

In Progress — **#28 completo** (pasos 1, 2 y 3) en **PR #45**, rama
`refactor/core-clients-mvc` (merge de `origin/main` tras PR #44 ya resuelto).
Siguiente: #26 (rama `chore/housekeeping-pyproject-docs-versionado`, se ramifica
de `refactor/core-clients-mvc` mientras PR #45 no esté en `main`).

### Avance de #28 (PR #45)

- [x] Paso 1 · Mover (mecánico): `git mv` de `semana2/tarea1/` → `src/aqua_gauss/`
  (`core/` puro + `clients/qt/`), tests a `tests/core` y `tests/qt`. Historial
  preservado (renames detectados por git).
- [x] Paquete instalable `aqua-gauss` (hatchling, layout src); entry point
  `aqua-gauss = "aqua_gauss.app:main"`; `python -m aqua_gauss`; extras `qt` /
  `dev`. `core/` sin dependencias.
- [x] `gui.py` movido a la raíz como shim a `aqua_gauss.app:main`, sin
  `sys.path.insert`.
- [x] Paso 3 · Borrada la consola: `main.py`, `test_main.py`, `requirements.txt`.
- [x] Docs/README con rutas y comandos nuevos (README, ONBOARDING, AGENTS
  quickstart, CASOS_PRUEBA, FEATURE_PROPIEDADES_RN); sección "Layout del paquete"
  en `docs/ARQUITECTURA.md`.
- [x] Autores: Roberto Macías (@roberto7503) y Reynaldo Molina (@ReynaldoZr)
  añadidos en `README.md`, `clients/qt/theme.py:APP_INFO` y `pyproject.toml`.
- [x] 70 tests en verde (`uv run --extra dev pytest` desde la raíz). Bajó de 78
  a 70 al eliminar los 8 tests de consola de `test_main.py`.
- [x] **Paso 2 · MVC en `clients/qt/`:** nuevo `solver.py` (`SolverPort` +
  `LocalSolver`) como única frontera con los algoritmos de `core`; `state.Sesion`
  deja de tener lógica y pasa a agrupar `SistemaModel` + `VectoresModel`
  (`models.py`) y su solver, con proxies planos para no tocar pantallas/tests.
  Cada `screen_*` es la View y su handler hace de controller. `core.gauss` /
  `core.vectores` ya sólo se importan desde `solver.py`. `docs/ARQUITECTURA.md`
  con el patrón y el flujo de una resolución.
- [x] Merge de `origin/main` (PR #44: `RUMBO.md` + rename "Variables libres" →
  "Infinitas soluciones") resuelto en la rama; el rename de #44 cubre lo que
  pedía #26 para el menú.
- [x] Autores reformateados: cada uno separado con ` · `, sin "(Grupo 7)", con
  enlace a su perfil (README) y handle (APP_INFO). `pyproject.toml` con 4
  entradas `{name=…}`.
- [ ] Reconciliación fina del resto de `docs/ARQUITECTURA.md` (diagramas de flujo
  antiguos) y de prosa suelta en `AGENTS.md` → se hace en #26.
- [ ] `semana2/tarea1/` queda con `Informe_Programa 1_Grupo 1.md` (sin versionar,
  archivo del alumno) y `.DS_Store`; git ya no rastrea nada ahí.

## Goals

### #28 — refactor: `core/` + `clients/` (MVC) y paquete instalable

- `git mv` de `semana2/tarea1/` → `core/` (`gauss.py`, `gauss_jordan.py`,
  `vectores.py`, `formato.py`, `mathrender.py`, tests) + `clients/qt/` (`ui/`,
  tests de GUI), preservando historial (`git log --follow`).
- Quitar `sys.path.insert` de `gui.py`; `pyproject.toml` coherente; borrar
  `semana2/` si queda vacío.
- Paquete instalable; entry point `aqua-gauss = "<pkg>.app:main"`; extras
  `qt` / `dev`. `uv run --extra dev pytest` en verde desde la raíz.
- `core/` sin imports de framework (Qt, FastAPI); solo Python + módulos propios.
- MVC en `clients/qt/`: `Sesion` deja de ser god-object; Models por caso,
  Controllers por pantalla, Views (`screen_*`); `SolverPort` con `LocalSolver`
  como única implementación. Documentar en `docs/ARQUITECTURA.md`.
- Borrar la consola: eliminar `main.py` y `test_main.py`; asserts útiles pasan a
  `core/tests/` y tests de cliente.
- Rama: `refactor/core-clients-mvc`.

### #26 — chore: housekeeping (pyproject, versionado, docs)

- `pyproject.toml`: alinear nombre y versión con `APP_INFO` (fuente de verdad =
  `pyproject.toml`); `APP_INFO["version"]` pasa a leer
  `importlib.metadata.version(<pkg>)` en runtime.
- `authors` de `pyproject.toml`: añadir a `ReynaldoZr` (Reynaldo Molina) y
  `roberto7503` (Roberto Macías).
- Migrar `[tool.black]` + `[tool.isort]` → `[tool.ruff]` (lint + format).
- `docs/VERSIONADO.md`: criterio **Tarea → bump major**.
- Tags retroactivos + GitHub Releases: `v1.0.0` (Tarea 1), `v2.0.0` (PR #21),
  `v3.0.0` (`806dc24`, Tarea 3).
- `CHANGELOG.md` en la raíz, formato *Keep a Changelog*.
- Sacar `context/current-feature.md` del VC: `git rm --cached`, `.gitignore`,
  versionar `context/current-feature.md.template`, aclarar en `AGENTS.md` que es
  local.
- `.editorconfig` en la raíz (`end_of_line = lf`, etc.).
- Docs: arreglar enlace roto a `DOCUMENTACION_FEATURE.md` en `README.md`; conteo
  de tests al día (**78**); reflejar split `gauss.py`/`gauss_jordan.py`/
  `vectores.py` y layout `core/`+`clients/`; encuadrar "sin librerías" como fase
  actual; typos de `AGENTS.md`.
- `ui/state.py:EJEMPLOS`: `"Variables libres"` → `"Variables libres (infinitas soluciones)"`.
- Rama: `chore/housekeeping-pyproject-docs-versionado`.

### #27 — infra: CI y release

- `.github/workflows/ci.yml` en `push` + `pull_request`: `setup-uv` +
  `uv sync --extra dev`; `ruff check .` y `ruff format --check .`; guard de fin
  de línea (falla ante `w/crlf` en `git ls-files --eol`); `uv run --extra dev
  pytest`; job GUI headless con `QT_QPA_PLATFORM=offscreen`; matriz Python
  3.9 y 3.13 en `ubuntu-latest` (+ `windows-latest` si se puede).
- `.github/workflows/release.yml` en tags `v*`: re-corre tests, guard
  `git describe --tags` ≡ `pyproject.version`, crea GitHub Release con la
  sección del `CHANGELOG.md`.
- Badge de CI en `README.md`; documentar en `docs/ONBOARDING.md`.
- Rama: `infra/ci-y-release`.

### Petición explícita del usuario — autoría de Roberto Macías y Reynaldo Molina

- Añadir a **Roberto Macías** y **Reynaldo Molina** como autores/colaboradores en:
  - `README.md` (línea de **Autores:** en el pie).
  - `semana2/tarea1/ui/theme.py` → `APP_INFO["autores"]` (o su ubicación tras el
    `git mv` de #28: `clients/qt/ui/theme.py`).
- Si #26/#28 mueven `APP_INFO` o lo vuelven dinámico (`importlib.metadata`), el
  campo `autores` sigue siendo texto en `APP_INFO`: mantenerlo ahí con los cinco
  nombres. Coherente con el `authors` de `pyproject.toml` que pide #26.

## Notes

- Estado hoy: `APP_INFO` (`semana2/tarea1/ui/theme.py:5`) dice `"Aqua Gauss"`
  `2.0.0`, autores `"Andrés Castillo y Fátima Zogaib (Grupo 7)"`. `pyproject.toml`
  dice `1.0.0`. `README.md:181` repite los mismos autores.
- Orden recomendado de implementación: **#28 → #26 → #27**.
  - #27 necesita `[tool.ruff]` en `pyproject.toml` → después de #26.
  - #26 (`APP_INFO` vía `importlib.metadata`, layout `core/`+`clients/` en docs)
    encaja mejor después de #28.
  - #27 es por lo demás independiente de #28 (el workflow se adapta a la ruta).
- Cada issue tiene su propia rama y se mergea por PR separado (#28 son 3 PRs).
- Precedentes ya mergeados: #23/#24/#25 (`806dc24`, `00ba185`), #30.
- Restricción "sin librerías de álgebra lineal": vive en `core/`; se levantará
  ahí cuando avance el contenido, sin tocar el resto.

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
