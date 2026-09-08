# Álgebra Lineal I - Sistema de Resolución de Ecuaciones Lineales

> Sistema educativo interactivo para resolver y analizar sistemas de ecuaciones lineales Ax=b mediante eliminación de Gauss.

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias (desde la raíz del repo)
pip install uv
uv sync --extra qt        # el núcleo no tiene dependencias; `qt` añade PyQt6 + matplotlib

# 2. Ejecutar la GUI  (dentro del entorno de uv, para que se rendericen las fórmulas)
uv run aqua-gauss         # equivalente:  uv run python -m aqua_gauss   /   uv run python gui.py
```

> La consola (`main.py`) se retiró: no era requisito del curso y la TUI (issue
> #18) cubrirá el terminal. Toda la lógica vive ahora en el paquete instalable
> `aqua_gauss` (`core/` de cálculo + `clients/qt/` de interfaz).

> La GUI es un flujo de pantallas navegable **sin ratón**: Enter avanza, Esc
> retrocede, ← → recorren los pasos, F1 vuelve al menú.

## 📖 Documentación

**¿Eres agente IA?** → Lee [AGENTS.md](AGENTS.md) primero.

**¿Eres humano nuevo?** → Lee [docs/ONBOARDING.md](docs/ONBOARDING.md).

**¿Quieres entender todo?** → Explora:
- [docs/RUMBO.md](docs/RUMBO.md) - Arquitectura objetivo y roadmap por fases
- [docs/PROYECTO.md](docs/PROYECTO.md) - Visión y estado
- [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) - Diseño técnico
- [docs/ALGORITMO.md](docs/ALGORITMO.md) - Explicación matemática
- [docs/CASOS_PRUEBA.md](docs/CASOS_PRUEBA.md) - Playbook con datos
- [docs/FEATURE_PROPIEDADES_RN.md](docs/FEATURE_PROPIEDADES_RN.md) - Tarea 3: vectores y combinaciones
- [docs/ADR-0002-pesos-combinacion-lineal.md](docs/ADR-0002-pesos-combinacion-lineal.md) - Convención para pesos no únicos
- [docs/GLOSARIO.md](docs/GLOSARIO.md) - Terminología (base, span, pesos/coeficientes, tolerancia)

## ✨ Características

- ✓ Eliminación de Gauss con pivoteo parcial
- ✓ Análisis de rango y nulidad
- ✓ Detección de formas escalonadas (REF/RREF)
- ✓ Solución general vectorial: x = xp + t₁v₁ + ... + tₖvₖ
- ✓ **Valores en fracción exacta** (`1/3`, `-8/3`) o decimal, con toggle en la GUI
- ✓ **Comprobación explícita** sustituyendo valores término a término
- ✓ Multiplicador de cada paso como fracción: `F2 ← F2 − (1/2)·F1`
- ✓ Notación matemática **renderizada** en la GUI (matplotlib mathtext → imagen):
  matrices y vectores con corchetes, fracciones apiladas; código LaTeX oculto tras un botón
- ✓ GUI por pantallas (menú → dimensiones → entrada guiada → proceso → vector), teclado-first
- ✓ Análisis de rango/nulidad/forma en lista con explicaciones y ayudas `?`
- ✓ Operaciones, combinaciones lineales y ocho propiedades algebraicas de `R^n`
- ✓ Gauss-Jordan/RREF separado en `gauss_jordan.py`, con API histórica compatible
- ✓ Pantalla gráfica de vectores y propiedades
- ✓ Subíndices Unicode consistentes y rediseño visual plano (contraste AA)
- ✓ Paquete instalable `aqua-gauss` con separación `core/` + `clients/qt/` (#28)
- ✓ 70 tests (todos pasan)
- ✓ El **algoritmo** no usa NumPy/SymPy (fase actual, ver `docs/RUMBO.md`); matplotlib
  se usa solo para dibujar la notación matemática, nunca para calcular

## 🎓 Restricción Deliberada

**NO se usa** NumPy, SymPy, scipy ni funciones preconstruidas de álgebra lineal
**para calcular**. `gauss.py`, `gauss_jordan.py` y `vectores.py` solo usan
Python y módulos propios del proyecto; `formato.py` continúa sin dependencias.

**POR QUÉ:** El ejercicio exige comprensión profunda. Las librerías son "cajas negras".
Es una **fase**: se irá levantando con el contenido del curso (ver [`docs/RUMBO.md`](docs/RUMBO.md)).

**SE USA:** Listas, loops, aritmética básica (Python puro). `matplotlib` aparece
solo en `mathrender.py` para convertir LaTeX en imágenes bonitas en la GUI (su
motor `mathtext`); arrastra NumPy como dependencia suya, que tampoco se usa.

## 📊 Estado

**Entregado (en `main`):**

- ✅ Tarea 1: eliminación gaussiana interactiva (`v1.0.0`)
- ✅ Verificación de soluciones · solución vectorial, rango, nulidad, LaTeX, formas
- ✅ Migración a `uv`
- ✅ Notación matemática renderizada + rediseño de la GUI por pantallas (PR #21, `v2.0.0`)
- ✅ Tarea 3: propiedades algebraicas de `R^n` y combinación lineal (#29, `v3.0.0`)
- ✅ Subíndices Unicode consistentes + rediseño visual plano (#30)
- ✅ #28: `core/` + `clients/qt` (MVC), paquete instalable `aqua-gauss`, baja de la consola

**Planificado** — ver [`docs/RUMBO.md`](docs/RUMBO.md):

- 🔄 #26 / #27: housekeeping + versionado → CI + release
- 📋 #31: glosario como fuente única + tooltips didácticos
- 📋 #18: cliente de terminal con Textual
- 📋 #32: API FastAPI sobre `core/`
- 📋 #33: animaciones Manim en la app
- 📋 #34: spike Lean 4 para los axiomas

## 🧪 Tests

```bash
# Desde la raíz del repo:
uv run --extra dev pytest        # 70 tests
```

- `tests/core/test_gauss.py` — lógica pura (21)
- `tests/core/test_gauss_jordan.py` — RREF y soluciones paramétricas (6)
- `tests/core/test_vectores.py` — operaciones, combinaciones y propiedades (12)
- `tests/core/test_formato.py` — fracciones, normalización de entrada, LaTeX (20)
- `tests/qt/test_mathrender.py` — render de LaTeX a imagen (3)
- `tests/qt/test_ui.py` — humo de la GUI / regresión del menú (8)

## 📁 Estructura

```
├── AGENTS.md                  # Punto de entrada para agentes IA
├── docs/                      # Documentación completa
│   ├── PROYECTO.md
│   ├── ARQUITECTURA.md
│   ├── ONBOARDING.md
│   ├── ALGORITMO.md
│   ├── CASOS_PRUEBA.md
│   ├── FEATURE_PROPIEDADES_RN.md
│   ├── GLOSARIO.md
│   ├── ADR-0001-entrada-numerica.md
│   └── ADR-0002-pesos-combinacion-lineal.md
├── pyproject.toml             # Paquete `aqua-gauss`; entry point + extras qt/dev
├── gui.py                     # Lanzador de la GUI (shim -> aqua_gauss.app:main)
├── src/aqua_gauss/
│   ├── app.py                # Punto de entrada (aqua-gauss / python -m aqua_gauss)
│   ├── core/                 # Model puro: SIN dependencias de framework
│   │   ├── gauss.py          # Gauss / REF + compatibilidad
│   │   ├── gauss_jordan.py   # Gauss-Jordan / RREF y parámetros
│   │   ├── vectores.py       # Operaciones y propiedades de R^n
│   │   └── formato.py        # Presentación: fracciones, LaTeX (texto), HTML
│   └── clients/qt/           # Cliente PyQt6 por pantallas
│       ├── app.py            # Ventana principal (QStackedWidget)
│       ├── state.py          # Sesion: dimensiones, notación, matriz, resultado
│       ├── mathrender.py     # LaTeX -> imagen (matplotlib mathtext)
│       └── screen_*.py       # una pantalla por archivo (incl. screen_vectores.py)
├── tests/
│   ├── core/                 # tests del núcleo (algoritmos, formato)
│   └── qt/                   # tests del cliente (mathrender, humo de GUI)
└── context/current-feature.md # Estado desarrollo (local, ver #26)
```

## 🛠️ Stack

- **Python:** 3.9+
- **PyQt6:** 6.6-7 (GUI)
- **matplotlib:** 3.9+ (render de notación matemática en la GUI; opcional en runtime)
- **uv:** Gestor de paquetes rápido
- **unittest:** Tests

## 📝 Ejemplos

### Solución Única

```
x + y + z = 6
0x + 2y + 5z = -4
2x + 5y - z = 27

Resultado: x=5, y=3, z=-2
```

### Infinitas Soluciones

```
x + y + z = 6
2x + 2y + 2z = 12
x - y + 0z = 0

Resultado: x = [3, 3, 0] + t·[-1/2, -1/2, 1]
```

### Sin Solución

```
x + y = 2
x + y = 5

Resultado: Inconsistente (contradicción)
```

### Combinación lineal en R²

```text
v₁ = [1, 2]ᵀ, v₂ = [3, -1]ᵀ, c₁ = 2, c₂ = -1

Resultado: 2v₁ - v₂ = [-1, 5]ᵀ
```

## 👥 Contribuir

1. Lee [AGENTS.md](AGENTS.md)
2. Sigue [docs/ONBOARDING.md](docs/ONBOARDING.md)
3. Crea issue, rama, tests, PR

---

**Autores:** Andrés Castillo ([@acr301](https://github.com/acr301)) · Fátima Zogaib ([@fmariezgg](https://github.com/fmariezgg)) · Roberto Macías ([@roberto7503](https://github.com/roberto7503)) · Reynaldo Molina ([@ReynaldoZr](https://github.com/ReynaldoZr)) | **Última actualización:** 2026-09-08 | **Licencia:** MIT

Ver también [docs/ADR-0001-entrada-numerica.md](docs/ADR-0001-entrada-numerica.md) — cómo la calculadora normaliza los números que teclea el usuario.

La convención para combinaciones con pesos no únicos está en
[docs/ADR-0002-pesos-combinacion-lineal.md](docs/ADR-0002-pesos-combinacion-lineal.md).
