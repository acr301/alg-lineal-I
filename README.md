# Álgebra Lineal I - Sistema de Resolución de Ecuaciones Lineales

> Sistema educativo interactivo para resolver y analizar sistemas de ecuaciones lineales Ax=b mediante eliminación de Gauss.

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install uv
uv sync

# 2. Ejecutar GUI
cd semana2/tarea1
python3 gui.py

# 3. O ejecutar consola
python3 main.py
```

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
- ✓ Generación de código LaTeX copiable
- ✓ Interfaz gráfica con PyQt6
- ✓ Interfaz de consola interactiva
- ✓ 21 tests (todos pasan)
- ✓ Sin NumPy, SymPy ni librerías de AL

## 🎓 Restricción Deliberada

**NO se usa:** NumPy, SymPy, scipy ni funciones preconstruidas de álgebra lineal.

**POR QUÉ:** El ejercicio exige comprensión profunda. Las librerías son "cajas negras".

**SE USA:** Listas, loops, aritmética básica (Python puro).

## 📊 Estado

- ✅ Feature 1: Eliminación gaussiana interactiva
- ✅ Feature 2: Verificación de soluciones
- ✅ Feature 3: Solución vectorial, rango, nulidad, LaTeX, formas
- 🔄 Chore: Migración a `uv` (en PR)

## 🧪 Tests

```bash
cd semana2/tarea1
python3 test_gauss.py    # 18 tests unitarios
python3 test_main.py     # 3 tests integración
# Salida: Ran 21 tests... OK
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
│   ├── gauss.py              # Lógica pura
│   ├── main.py               # Consola
│   ├── gui.py                # GUI PyQt6
│   └── test_*.py             # Tests
└── context/current-feature.md # Estado desarrollo
```

## 🛠️ Stack

- **Python:** 3.9+
- **PyQt6:** 6.6-7 (GUI)
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

Resultado: x = [3, 3, 0] + t[1, -2, 1]
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

**Versión:** 1.0.0 | **Última actualización:** 2026-08-31 | **Licencia:** MIT
