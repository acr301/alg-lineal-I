# RUMBO.md — Hacia dónde va el repo

Estado y plan de evolución. El detalle vive en los issues; esto es el mapa.

## Dónde estamos (2026-09-08)

- Tareas 1–3 entregadas y en `main`.
  - `v1.0.0` → Tarea 1 (eliminación gaussiana interactiva).
  - `v2.0.0` → PR #21 (rework GUI multipantalla + notación matemática).
  - `v3.0.0` → `806dc24` (#29, propiedades algebraicas de Rⁿ y combinación lineal).
  - #30 (`00ba185`): subíndices Unicode consistentes + rediseño visual plano.
- **70 tests** en verde (`uv run --extra dev pytest`).
- Código en `semana2/tarea1/` (se consolida en #28).

## La restricción "sin librerías" es una fase, no un dogma

Hoy `gauss.py` / `gauss_jordan.py` / `vectores.py` se implementan desde cero
(sin NumPy/SymPy) porque el objetivo es comprensión profunda. **Esa restricción
se irá levantando** a medida que el curso avance en contenidos. Por eso el
cálculo se aísla en `core/` (#28): el día que se levante, se levanta ahí sin
tocar clientes ni servidor.

## Arquitectura objetivo — MVC, cliente/servidor

```
core/            # Model puro: gauss.py gauss_jordan.py vectores.py formato.py
shared/          # DTOs (pydantic) + shared/glosario.py — reusados por server y clientes
server/          # FastAPI fino sobre core/ (opcional; los clientes también resuelven local)
clients/
  qt/            # PyQt6 MVC (Views = pantallas, Controllers por pantalla, Models ≈ DTOs)
  tui/           # Textual (#18)
animaciones/     # escenas Manim (.py; extra `viz`)
formal/          # Lean 4 (spike #34)
```

- **`SolverPort`**: los clientes hablan con una interfaz con dos
  implementaciones — `LocalSolver` (importa `core`, offline) y `RemoteSolver`
  (llama al API). El servidor es **aditivo**, nunca está en el camino crítico de
  resolver.
- **Sin rama `staging`**: no hay stakes ni clientes reales. Se prueba en `main`;
  `main` no es prod, es solo despliegue. El deploy sale de `main` y de los tags.

## Roadmap por fases (se puede parar en cualquiera)

| Fase | Qué | Issues |
|---|---|---|
| **0** ✅ | Tarea 3 + rediseño en `main`; tags retro pendientes | #29, #30 |
| **1** | `core/` + `clients/qt/` MVC, paquete instalable, sin `sys.path`, borrar `main.py` | #28 |
| **2** | Housekeeping (pyproject, `[tool.ruff]`, versionado, `CHANGELOG`, sacar `current-feature.md`) → CI + `release.yml` | #26, #27 |
| **3** | Glosario como fuente única + tooltips didácticos con check en CI; spike Lean 4 | #31 (#35–#37), #34 |
| **4** | Cliente TUI (Textual) sobre `SolverPort` | #18 |
| **5** | Server FastAPI sobre `core/`; `RemoteSolver`; deploy desde `main` | #32 (#38–#40) |
| **6** | Animaciones Manim: escenas + streaming desde el server + pantalla en el cliente | #33 (#41–#43) |

Tras Fase 2/3 el repo ya está limpio, testeado y con CI. Server (Fase 5) y
Manim (Fase 6) son opcionales.

## Versionado

Criterio: **cada Tarea = bump major** (se documenta en `docs/VERSIONADO.md`, #26).
`pyproject.toml` es la fuente de verdad de la versión; `APP_INFO["version"]`
pasará a leerla con `importlib.metadata`. Un tag `vX.Y.Z` sobre el commit
correcto + GitHub Release por entrega.
