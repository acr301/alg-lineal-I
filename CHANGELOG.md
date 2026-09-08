# Changelog

Todos los cambios notables de este proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
versionado, [Semantic Versioning](https://semver.org/lang/es/) con la regla del
curso **una Tarea/Programa = un *major*** (ver [`docs/VERSIONADO.md`](docs/VERSIONADO.md)).

## [Unreleased]

### Changed

- Refactor a paquete instalable `aqua-gauss` con separación **core / clients**
  (#28): el cálculo puro vive en `aqua_gauss.core` y el cliente PyQt6 en
  `aqua_gauss.clients.qt`, que consume `core` a través de un `SolverPort`
  (`LocalSolver`). `gui.py` es un shim sin `sys.path`; entry point `aqua-gauss`.
- Migración de `black` + `isort` a `ruff` (lint + formato) (#26).
- `APP_INFO["version"]` se lee de `importlib.metadata`; `pyproject.toml` es la
  única fuente de la versión (#26).
- `context/current-feature.md` deja de versionarse; se versiona su plantilla
  `context/current-feature.md.template` (#26).

### Removed

- Interfaz de consola (`main.py`, `test_main.py`): no era requisito del curso; el
  terminal lo cubrirá la TUI (#18) (#28).

### Added

- `docs/VERSIONADO.md`, `CHANGELOG.md`, `.editorconfig` (#26).

## [3.0.0] — 2026-09-07

Tarea 3 — Propiedades algebraicas de `R^n` y combinación lineal (#29).

### Added

- `vectores.py`: operaciones puras en `R^n`, pertenencia a un espacio generado y
  verificación de los ocho axiomas de espacio vectorial.
- Notación LaTeX con vectores columna para combinaciones lineales; pantalla de
  GUI "Vectores y propiedades de R^n".
- `docs/GLOSARIO.md` con la terminología unificada; `docs/ADR-0002` (convención
  para pesos no únicos).
- Subíndices Unicode consistentes y rediseño visual plano con contraste AA
  (#24, #25, #30).

### Changed

- La reducción a forma escalonada reducida (RREF) se separa en `gauss_jordan.py`,
  manteniendo `gauss.py` como API histórica compatible.

## [2.0.0] — 2026-09-01

Rework de la presentación: notación matemática renderizada y GUI multipantalla
(#21), más el análisis avanzado de sistemas y la migración de tooling que se
entregaron entre la Tarea 1 y ésta.

### Added

- GUI PyQt6 reescrita por pantallas (`ui/`), navegable con teclado: menú →
  dimensiones y notación → entrada guiada → proceso y resultado → solución
  vectorial (#21).
- `formato.py`: `float` → fracción exacta (Euclides + fracción continua) o
  decimal, sin `fractions`; normalización de la entrada del usuario
  (`docs/ADR-0001`).
- `mathrender.py`: LaTeX → `QPixmap` con matplotlib mathtext; degrada a
  texto/HTML si falta matplotlib.
- Análisis de sistemas en `gauss.py`: rango y nulidad
  (`Rango(A) + Nulidad(A) = n`), detección de formas escalonadas (REF/RREF),
  solución general vectorial `x = xₚ + t₁v₁ + … + tₖvₖ` y generación de LaTeX
  copiable (#12).
- Verificación explícita de la solución: sustitución término a término en el
  sistema original (#3).

### Changed

- Multiplicador de cada paso mostrado como fracción (`F2 ← F2 − (1/2)·F1`).
- Migración del gestor de dependencias a `uv`; `pyproject.toml` + `uv.lock`
  versionados (#14).

## [1.0.0] — 2026-08-24

Tarea 1 — Solución de sistemas `Ax = b` por eliminación por filas.

### Added

- Programa interactivo de consola (`main.py`) que resuelve `Ax = b` por
  eliminación de Gauss con pivoteo parcial, mostrando cada paso.
- `gauss.py`: lógica pura (sin `input`/`print` ni librerías de álgebra lineal);
  clasificación del sistema (determinado / indeterminado con solución
  paramétrica / incompatible).
- `test_gauss.py`: pruebas de la lógica pura.

[Unreleased]: https://github.com/acr301/alg-lineal-I/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/acr301/alg-lineal-I/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/acr301/alg-lineal-I/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/acr301/alg-lineal-I/releases/tag/v1.0.0
