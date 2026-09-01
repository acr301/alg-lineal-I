# Álgebra Lineal I - Sistema de Resolución de Ecuaciones Lineales

> Sistema educativo interactivo para resolver y analizar sistemas de ecuaciones lineales Ax=b mediante eliminación de Gauss.

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install uv
uv sync

# 2. Ejecutar GUI  (dentro del entorno de uv, para que se rendericen las fórmulas)
cd semana2/tarea1
uv run python gui.py

# 3. O ejecutar consola
uv run python main.py
```

> La GUI es un flujo de pantallas navegable **sin ratón**: Enter avanza, Esc
> retrocede, ← → recorren los pasos, F1 vuelve al menú.

## 📖 Documentación

**¿Eres agente IA?** → Lee [AGENTS.md](AGENTS.md) primero.

**¿Eres humano nuevo?** → Lee [docs/ONBOARDING.md](docs/ONBOARDING.md).

**¿Quieres entender todo?** → Explora:
- [docs/PROYECTO.md](docs/PROYECTO.md) - Visión y estado
- [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) - Diseño técnico
- [docs/ALGORITMO.md](docs/ALGORITMO.md) - Explicación matemática
- [docs/CASOS_PRUEBA.md](docs/CASOS_PRUEBA.md) - Playbook con datos
- [DOCUMENTACION_FEATURE.md](DOCUMENTACION_FEATURE.md) - Detalles completos

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
- ✓ Interfaz de consola interactiva (`--decimal` / `--fraccion`)
- ✓ 38 tests (todos pasan)
- ✓ El **algoritmo** no usa NumPy/SymPy (`gauss.py` no importa nada); matplotlib
  se usa solo para dibujar la notación matemática, nunca para calcular

## 🎓 Restricción Deliberada

**NO se usa** NumPy, SymPy, scipy ni funciones preconstruidas de álgebra lineal
**para calcular**. `gauss.py` (el algoritmo) y `formato.py` no importan nada.

**POR QUÉ:** El ejercicio exige comprensión profunda. Las librerías son "cajas negras".

**SE USA:** Listas, loops, aritmética básica (Python puro). `matplotlib` aparece
solo en `mathrender.py` para convertir LaTeX en imágenes bonitas en la GUI (su
motor `mathtext`); arrastra NumPy como dependencia suya, que tampoco se usa.

## 📊 Estado

- ✅ Feature 1: Eliminación gaussiana interactiva
- ✅ Feature 2: Verificación de soluciones
- ✅ Feature 3: Solución vectorial, rango, nulidad, LaTeX, formas
- ✅ Chore: Migración a `uv`
- 🔄 Fix: LaTeX renderizado, comprobación explícita y fracciones (issues #15/#16/#17)
- 📋 Issue #18: migración de la consola a Textual TUI (propuesta)

## 🧪 Tests

```bash
cd semana2/tarea1
python3 test_gauss.py     # 21 tests de la lógica pura
python3 test_formato.py   # 11 tests de fracciones / formato
python3 test_main.py      # 3 tests de integración de consola
# Total: 38 tests (test_mathrender se salta si falta matplotlib). O bien: uv run --extra dev pytest
```

## 📁 Estructura

```
├── AGENTS.md                  # Punto de entrada para agentes IA
├── docs/                      # Documentación completa
│   ├── PROYECTO.md
│   ├── ARQUITECTURA.md
│   ├── ONBOARDING.md
│   ├── ALGORITMO.md
│   └── CASOS_PRUEBA.md
├── DOCUMENTACION_FEATURE.md   # Detalles extensos
├── semana2/tarea1/
│   ├── gauss.py              # Lógica pura (sin imports)
│   ├── formato.py            # Presentación: fracciones, LaTeX (texto), HTML
│   ├── mathrender.py         # LaTeX -> imagen (matplotlib mathtext) para la GUI
│   ├── main.py               # Consola
│   ├── gui.py                # Punto de entrada de la GUI (shim)
│   ├── ui/                   # GUI PyQt6 por pantallas (app, state, theme, widgets, screen_*)
│   └── test_*.py             # Tests (gauss / formato / mathrender / main)
└── context/current-feature.md # Estado desarrollo
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

## 👥 Contribuir

1. Lee [AGENTS.md](AGENTS.md)
2. Sigue [docs/ONBOARDING.md](docs/ONBOARDING.md)
3. Crea issue, rama, tests, PR

---

**Autores:** Andrés Castillo y Fátima Zogaib (Grupo 7) | **Última actualización:** 2026-09-01 | **Licencia:** MIT

Ver también [docs/ADR-0001-entrada-numerica.md](docs/ADR-0001-entrada-numerica.md) — cómo la calculadora normaliza los números que teclea el usuario.
