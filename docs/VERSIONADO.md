# Versionado

## Criterio: una tarea del curso = un *major*

El proyecto sigue [SemVer](https://semver.org/lang/es/) con una regla propia para
el eje *major*: **cada "Programa N" / Tarea del curso entregado sube la versión a
`N.0.0`**. Entre tareas, los cambios se numeran así:

| Cambio | Bump | Ejemplo |
|--------|------|---------|
| Nueva Tarea/Programa del curso entregado | **major** | `2.x.y` → `3.0.0` |
| Funcionalidad nueva dentro de la tarea vigente (feature, pantalla, análisis) | **minor** | `3.0.0` → `3.1.0` |
| Corrección de bug, refactor sin cambio de comportamiento, docs, infra | **patch** | `3.1.0` → `3.1.1` |

Un refactor grande sin comportamiento nuevo (p. ej. #28, el paso a
`core/` + `clients/`) es **patch**: no cambia lo que el usuario puede hacer.

## Fuente de verdad

`pyproject.toml` → `[project].version`. En runtime, `APP_INFO["version"]`
(`aqua_gauss.clients.qt.theme`) lo lee con
`importlib.metadata.version("aqua-gauss")`; no se hardcodea en dos sitios.

Al preparar una entrega:

1. Subir `version` en `pyproject.toml` según la tabla.
2. Añadir la sección correspondiente en `CHANGELOG.md`.
3. `git tag vX.Y.Z` sobre el commit de la entrega y `git push --tags`.
4. Crear el GitHub Release con el cuerpo de esa sección del changelog
   (a partir de #27 lo hace el workflow `release.yml` al detectar el tag).

El workflow de release valida que `git describe --tags` coincida con
`pyproject.version`: el tag y la versión no pueden divergir.

## Historial de entregas

| Versión | Entrega | Commit / PR |
|---------|---------|-------------|
| `v1.0.0` | Tarea 1 — eliminación gaussiana interactiva (consola) | rama `feature/eliminacion-gaussiana-interactiva` |
| `v2.0.0` | Notación matemática renderizada + GUI multipantalla | PR #21 (`be2d169`) |
| `v3.0.0` | Tarea 3 — propiedades algebraicas de `R^n` y combinación lineal | PR #29 (`806dc24`) |

Las versiones intermedias (verificación de la solución, rango/nulidad, solución
vectorial, migración a `uv`) se entregaron entre `v1` y `v2` sin tag propio; se
listan en el `CHANGELOG.md` bajo `v2.0.0`.
