# PROYECTO.md - Visión y Estado del Proyecto

## 🎯 ¿Qué es este proyecto?

**alg-lineal-I** es un sistema educativo interactivo para resolver y analizar sistemas de ecuaciones lineales Ax=b mediante eliminación de Gauss, con énfasis en:

- Comprensión matemática profunda
- Visualización paso a paso
- Análisis avanzado (rango, nulidad, forma escalonada)
- Sin "cajas negras" (sin librerías de álgebra lineal)

## 📚 Contexto Educativo

Este proyecto es parte del curso **Álgebra Lineal I** y busca que estudiantes comprendan:

1. Cómo funciona realmente la eliminación de Gauss
2. Qué son el rango y la nulidad de una matriz
3. Diferencia entre forma escalonada (REF) y forma escalonada reducida (RREF)
4. Expresión de soluciones vectoriales: x = xp + t₁v₁ + ... + tₖvₖ
5. Codificación de conceptos matemáticos en software

## 🎓 Restricción Deliberada (fase actual)

En `aqua_gauss.core` **no** se usan NumPy, SymPy, scipy ni funciones de álgebra
lineal preconstruidas: solo listas, bucles y aritmética. **Es una fase**, no una
prohibición permanente: se irá levantando a medida que avance el contenido del
curso, y se levantará en `core/` sin tocar los clientes (ver
[`docs/RUMBO.md`](RUMBO.md)).

`PyQt6` y `matplotlib` sí se usan, pero solo en `aqua_gauss.clients.qt` (interfaz
y render de LaTeX a imagen), nunca para calcular.

**Razón:** el ejercicio requiere implementar desde cero para comprensión profunda.

## 📊 Estado Actual (2026-09-08)

### ✅ Completado

#### Feature 1: Eliminación Gaussiana Interactiva
- Pivoteo parcial
- Reducción a forma escalonada
- Clasificación del sistema (determinado/indeterminado/inconsistente)
- Mergeado a main

#### Feature 2: Verificación Explícita de Solución
- `verificar_solucion()` - Sustituye en el sistema original
- `evaluar_solucion_parametrica()` - Construye soluciones concretas
- Mergeado a main

#### Feature 3: Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas
- `rango_matriz()` - Calcula rango
- `verificar_rango_nulidad()` - Verifica Rango + Nulidad = n
- `es_forma_escalonada()` y `es_forma_escalonada_reducida()` - Detectan REF/RREF
- `clasificar_forma_escalonada()` - Clasifica la forma
- `solucion_general_vectorial()` - Expresión vectorial
- `generar_latex_solucion()` - Código LaTeX (movido luego a `formato.py`)
- Cierra issues #9, #10, #11 · Mergeado a main (PR #12)

### 🔄 En Progreso

#### Chore: Migración a `uv` (PR #14, abierto)
- `pyproject.toml` + `uv.lock`; documentación agnóstica de herramienta.

#### Feature: Notación matemática y rediseño de la GUI (PR pendiente)
- `formato.py` (fracciones, `normalizar_entrada`, LaTeX, HTML) y `mathrender.py`
  (LaTeX → imagen con matplotlib mathtext).
- `gauss.verificar_solucion_detallada()` (comprobación término a término) y
  `formato_numero` en `escalonar` (multiplicador de cada paso como fracción).
- GUI reescrita en `ui/` como flujo de 5 pantallas navegable con teclado.
- ADR-0001: normalización de la entrada numérica.
- PR #21. Cierra #15, #16, #17, #19 (rework), #20 (ADR), #22 (bug doble clic). 44 tests.

### 📋 Planificado (Futura)

- [ ] Método de Cramer (determinantes)
- [ ] Factorización LU
- [ ] Descomposición QR
- [ ] Valores y vectores propios
- [ ] Interfaz web (Django/FastAPI)
- [ ] Visualización 3D de espacios
- [ ] Exportación a PDF

## 📈 Métricas

| Métrica | Valor |
|---------|-------|
| Paquete | `aqua-gauss` (instalable, layout `src/`) |
| Tests | 70 (100% pass) |
| Restricción sin librerías (`core/`) | ✓ Cumplida (fase actual) |
| Lint + formato | `ruff` (`uv run ruff check . && ruff format --check .`) |
| GUI funcional | ✓ Sí (flujo de pantallas, teclado-first) |

## 🏗️ Arquitectura de Alto Nivel

```
┌───────────────────────────────────────────────┐
│  aqua_gauss.clients.qt   — cliente PyQt6       │
│  Views = screen_*  ·  Controllers = handlers   │
│  Models = SistemaModel / VectoresModel         │
│  Menú → Dimensiones → Entrada → Proceso → Vec. │
└───────────────┬───────────────────────────────┘
                │  SolverPort  (LocalSolver hoy; RemoteSolver con el server #32)
┌───────────────▼───────────────────────────────┐
│  aqua_gauss.core   — MODEL puro, sin framework │
│  gauss.py (REF) · gauss_jordan.py (RREF)       │
│  vectores.py (R^n) · formato.py (presentación) │
└───────────────┬───────────────────────────────┘
                │
┌───────────────▼───────────────────────────────┐
│        Python 3.9+ puro                        │
│   (listas, bucles, aritmética; sin AL externa)│
└───────────────────────────────────────────────┘
```

`gui.py` es un shim a `aqua_gauss.app:main`. La consola (`main.py`) se retiró en
#28; el terminal lo cubrirá la TUI (#18).

## 🔗 Dependencias

- **Núcleo (`core/`):** ninguna — solo la stdlib de Python.
- **Extra `qt`:** `PyQt6` >= 6.6 (GUI) y `matplotlib` >= 3.9 (solo render de
  notación; arrastra NumPy como dep. suya, que no se usa para calcular).
- **Extra `dev`:** `pytest`, `pytest-cov`, `ruff`.
- **Tooling:** `uv` (gestor de paquetes y entorno).

## 🧪 Testing

- **tests/core/test_gauss.py** (21): lógica pura — determinado/indeterminado/
  inconsistente, rango y nulidad, formas escalonadas, solución vectorial.
- **tests/core/test_gauss_jordan.py** (6): RREF y soluciones paramétricas.
- **tests/core/test_vectores.py** (12): operaciones, combinaciones y 8 axiomas.
- **tests/core/test_formato.py** (20): fracciones, `normalizar_entrada`
  (ADR-0001), LaTeX.
- **tests/qt/test_mathrender.py** (3): render de LaTeX a imagen (se salta sin
  matplotlib).
- **tests/qt/test_ui.py** (8): humo de la GUI + regresión del menú (se salta sin
  PyQt6).

**Ejecución:** `uv run --extra dev pytest` (70 passed)

## 👥 Colaboradores

- **Autores (Grupo 7):** Andrés Castillo, Fátima Zogaib, Roberto Macías, Reynaldo Molina.

## 📝 Cómo Contribuir

1. **Leer primero:** `AGENTS.md` → `docs/ONBOARDING.md`
2. **Entender la restricción:** Sin NumPy ni librerías de AL
3. **Crear issue:** Describir qué y por qué
4. **Implementar:** Código + Tests + Docs
5. **PR:** Mencionar issue, pedir reviewers

## 🔒 Valores del Proyecto

- ✓ **Claridad sobre mágica:** Todo implementado, nada oculto
- ✓ **Educación sobre eficiencia:** Comprensión primero
- ✓ **Testing riguroso:** Confianza en corrección
- ✓ **Documentación excelente:** Para agentes y humanos

## 🌐 Recursos Externos

- **Teoría:** "Linear Algebra Done Right" (Axler)
- **Método:** "Numerical Linear Algebra" (Trefethen & Bau)
- **PyQt6:** https://doc.qt.io/qtforpython-6/
- **uv:** https://docs.astral.sh/uv/

---

**Última actualización:** 2026-09-01  
**Versión del proyecto:** 1.0.0  
**Estatus:** En desarrollo activo (PR #14 uv y PR #21 notación/GUI en revisión)
