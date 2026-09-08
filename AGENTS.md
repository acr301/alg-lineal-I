# AGENTS.md - Guía para Agentes IA y Colaboradores

Este archivo es la **puerta de entrada para agentes IA** (como Claude) que trabajen en este repositorio. Contiene:
- Estructura del proyecto
- Contexto crítico
- Cómo ejecutar y contribuir
- Memoria compartida del proyecto

> **Hacia dónde va el repo:** ver [`docs/RUMBO.md`](docs/RUMBO.md) — arquitectura
> objetivo (MVC, `core/` + `clients/` + `server/`), roadmap por fases y el mapa
> de issues (#26–#43). La restricción "sin librerías de álgebra lineal" es una
> **fase actual**, no permanente: se irá levantando con el contenido del curso.

## 📁 Estructura del Repositorio

```
alg-lineal-I/
├── AGENTS.md                     # ← TÚ ESTÁS AQUÍ (guía para agentes)
├── pyproject.toml                # Configuración moderna con uv
├── uv.lock                       # Lock file (versionar para reproducibilidad)
├── docs/                         # Documentación completa
│   ├── PROYECTO.md              # Visión, objetivos, estado
│   ├── ARQUITECTURA.md          # Diseño técnico y decisiones
│   ├── ONBOARDING.md            # Guía rápida de inicio
│   ├── ALGORITMO.md             # Explicación matemática detallada
│   ├── CASOS_PRUEBA.md          # Playbook con datos listos
│   ├── FEATURE_PROPIEDADES_RN.md # Recorrido del issue #23
│   ├── GLOSARIO.md              # Terminología unificada
│   ├── ADR-0001-entrada-numerica.md
│   └── ADR-0002-pesos-combinacion-lineal.md
├── semana2/tarea1/
│   ├── gauss.py                 # Gauss / REF + API histórica compatible
│   ├── gauss_jordan.py          # RREF y soluciones paramétricas
│   ├── vectores.py              # Operaciones y propiedades de R^n
│   ├── formato.py               # Presentación: fracciones, LaTeX (texto), helpers HTML
│   ├── mathrender.py            # LaTeX -> imagen (matplotlib mathtext) para la GUI
│   ├── main.py                  # Interfaz de consola (--decimal / --fraccion)
│   ├── gui.py                   # Punto de entrada de la GUI (shim -> ui/)
│   ├── ui/                      # GUI PyQt6 por pantallas
│   │   ├── app.py               #   ventana principal (QStackedWidget) + atajos
│   │   ├── state.py             #   Sesion: único sitio que llama a gauss desde la GUI
│   │   ├── theme.py             #   hoja de estilo, paleta, fuente
│   │   ├── widgets.py           #   PantallaBase, MatrizGrid, barra de navegación, ayuda
│   │   └── screen_*.py          #   menú, dimensiones, entrada guiada, proceso, resultado
│   ├── test_gauss.py            # Tests de la lógica pura
│   ├── test_gauss_jordan.py     # Tests directos de RREF y parámetros
│   ├── test_vectores.py         # Tests de operaciones y ocho axiomas
│   ├── test_formato.py          # Tests de fracciones / formato
│   ├── test_mathrender.py       # Tests del render de LaTeX (se salta si falta matplotlib)
│   ├── test_main.py             # Tests de integración de consola
│   └── requirements.txt          # Legacy (generado desde pyproject.toml)
└── context/
    └── current-feature.md       # Estado actual del desarrollo
```

## 🚀 Inicio Rápido (para Agentes)

### 1. Entender el Proyecto

```bash
# Leer primero (en orden):
1. docs/PROYECTO.md           # ¿Qué es? ¿Por qué?
2. docs/ARQUITECTURA.md       # Cómo está hecho
3. docs/ONBOARDING.md         # Cómo trabajar aquí
```

### 2. Configurar Entorno

```bash
# Instalar uv (una sola vez)
pip install uv

# Desde la raíz del proyecto
uv sync
```

### 3. Ejecutar

```bash
cd semana2/tarea1

# GUI: ejecútala DENTRO del entorno de uv para que matplotlib renderice las
# fórmulas. Con `python3 gui.py` a secas puede faltar matplotlib y la notación
# se verá como texto.
uv run python gui.py

# Consola (fracción exacta por defecto; --decimal para decimales)
uv run python main.py

# Tests
uv run --extra dev pytest        # desde la raíz del repo
```

La GUI mantiene el flujo de sistemas (menú → dimensiones → entrada guiada →
proceso → solución vectorial) y agrega desde el menú una pantalla independiente
de vectores y propiedades de `R^n`. Es navegable **sin ratón**: Enter avanza,
Esc retrocede, ← → recorren los pasos, F1 vuelve al menú.

## 🎯 Responsabilidades del Agente

### Antes de Trabajar

- [ ] Leer `docs/PROYECTO.md` para entender el contexto
- [ ] Leer `docs/ARQUITECTURA.md` para entender decisiones técnicas
- [ ] Revisar `context/current-feature.md` para estado actual
- [ ] Ejecutar tests para verificar que todo funciona

### Durante el Trabajo

- [ ] NO usar NumPy, SymPy ni librerías de álgebra lineal (restricción del ejercicio)
- [ ] Mantener separación: `gauss.py` (REF), `gauss_jordan.py` (RREF),
      `vectores.py` (R^n), `main.py` (consola) y `ui/` (GUI)
- [ ] NO romper tests existentes
- [ ] Commits atómicos con mensajes descriptivos

### Al Completar

- [ ] Tests verdes (78 tests en `main`)
- [ ] Actualizar `context/current-feature.md`
- [ ] Commits lógicos (no squash a menos que se pida)
- [ ] Crear PR mencionando issues relacionados
- [ ] Agregar colaboradores como reviewers

## 📚 Documentación Completa

### docs/PROYECTO.md
- Visión del proyecto
- Objetivos a corto y largo plazo
- Restricciones del ejercicio
- Estado del desarrollo

### docs/ARQUITECTURA.md
- Diseño de módulos
- Flujo de datos
- Decisiones técnicas (por qué sin librerías externas)
- Guía de extensión

### docs/ONBOARDING.md
- Primeros pasos
- Estructura de carpetas
- Cómo agregar funcionalidad
- Cómo ejecutar tests

### docs/ALGORITMO.md
- Fundamentos matemáticos
- Fases del algoritmo
- Explicación de rango/nulidad
- Detección de formas escalonadas
- Solución vectorial
- Comprobación explícita (sustitución término a término)
- Fracción exacta vs. decimal (`formato.a_fraccion`)

### docs/ADR-0001-entrada-numerica.md
- Cómo se normaliza lo que teclea el usuario (fracción tidy ≤ 64 o 4 decimales)
- `formato.normalizar_entrada`, `MAX_DEN_DISPLAY`, `DECIMALES_ENTRADA`

### docs/ADR-0002-pesos-combinacion-lineal.md
- Convención determinista para una combinación lineal con infinitos pesos
- Los parámetros libres se fijan en cero para devolver una solución concreta

### docs/FEATURE_PROPIEDADES_RN.md
- Alcance del issue #23, ejemplos manuales y mapa de archivos
- Separación de Gauss/Gauss-Jordan, vectores columna y pruebas agregadas

### docs/GLOSARIO.md
- Terminología unificada: base, span, pesos/coeficientes, variable libre, EPS
- Reglas de consistencia (`pesos` en código y ADR; `EPS` ≠ umbral de ADR-0001)

### docs/CASOS_PRUEBA.md
- 3 casos de prueba principales
- Datos listos para copiar/pegar
- Salidas esperadas
- Playbook para documentación

## 🛠️ Tecnología Stack

| Componente | Versión | Razón |
|-----------|---------|-------|
| Python | 3.9+ | Soportado por PyQt6 |
| PyQt6 | 6.6-7 | GUI moderna |
| matplotlib | 3.9+ | SOLO render de notación matemática (mathtext) en la GUI; arrastra NumPy como dep. suya |
| uv | 0.10+ | Gestor de paquetes rápido |
| unittest | stdlib | Tests sin dependencias |
| Algoritmo | Puro | `gauss.py`, `gauss_jordan.py` y `vectores.py` sin librerías de AL |
| `formato.py` | Puro | Sin imports (ni `fractions`): fracción por Euclides + fracción continua |

## 🚫 Restricciones Críticas

1. **NO librerías de álgebra lineal** (NumPy, SymPy, scipy)
   - Razón: El ejercicio exige implementación desde cero
   - Usar: Listas, loops, aritmética básica
   - `matplotlib` está permitido **solo** como motor de render (LaTeX → imagen) en
     `mathrender.py`; nunca para calcular. Los módulos algorítmicos solo usan
     Python y, cuando corresponde, imports de otros módulos propios.

2. **NO romper funcionalidades existentes**
   - Todos los tests deben pasar
   - Si modificas `gauss.py`, actualiza tests

3. **Separación de responsabilidades**
   - `gauss.py`: eliminación hacia adelante, clasificación y compatibilidad
   - `gauss_jordan.py`: RREF y solución paramétrica/vectorial
   - `vectores.py`: operaciones, combinaciones y propiedades de `R^n`
   - Los tres módulos son lógica pura (sin input/print y sin librerías de AL)
   - `formato.py`: Presentación texto (float → fracción/decimal, LaTeX, HTML)
   - `mathrender.py`: Presentación imagen (LaTeX → QPixmap con matplotlib)
   - `main.py`: UI de consola
   - `ui/`: UI PyQt6 por pantallas; `ui/state.py:Sesion` es el ÚNICO sitio de la
     GUI que llama a los módulos de cálculo. Cada pantalla es un `ui/screen_*.py`.
   - No dupliques formateo de números: usa `formato.formatear_valor(v, modo)` o
     `sesion.fmt(v)`.

## 📊 Métricas Actuales

- **Tests:** 78 (todos pasan en `main`) — `uv run --extra dev pytest`
- **Suites:** `test_gauss`, `test_gauss_jordan`, `test_vectores`, `test_formato`,
  `test_mathrender`, `test_main`, `test_ui`
- **Cobertura:** Lógica principal y capa de formato cubiertas
- **Estado:** Tareas 1–3 en `main`. Próximo trabajo estructural en #28 (ver `docs/RUMBO.md`)

## 🤖 Memoria para Agentes

### Contexto Compartido

**Tarea 3 — propiedades de Rⁿ (#29 → `806dc24`, mergeado):**
- `gauss_jordan.py` separa RREF y soluciones paramétricas; `gauss.py` mantiene
  delegadores compatibles para `main.py` y `ui/state.py` (ver ADR-0002).
- `vectores.py` implementa operaciones, combinación lineal, pertenencia y los
  ocho axiomas de `R^n` sin librerías externas de álgebra lineal.
- `formato.py`, consola y `ui/screen_vectores.py` muestran vectores columna y LaTeX.
- Convención de pesos no únicos en ADR-0002; terminología en `docs/GLOSARIO.md`.

**Subíndices + rediseño plano (#30 → `00ba185`, mergeado):**
- `formato.subindice/var/parametro/entrada_A/entrada_b` para notación Unicode;
  `ui/theme.py` sin degradados (flat design, contraste AA).

**Rumbo:** `main.py` (consola) se **deprecará** en #28 — la app va puro GUI +
una TUI Textual (#18). No agregues features nuevas a `main.py`.

**Última feature (rama `fix/latex-renderizado-fracciones-verificacion`):**
LaTeX renderizado, comprobación explícita y fracciones. Issues #15, #16, #17.
- `formato.py` (`a_fraccion`, `formatear_valor`, `generar_latex_solucion`,
  `texto/latex_verificacion`, helpers HTML) + `mathrender.py` (LaTeX → QPixmap con
  matplotlib mathtext: `latex_a_pixmap`, `columna_a_pixmap`, `matriz_a_pixmap`;
  degrada a texto/HTML si falta matplotlib).
- `gauss.py`: `verificar_solucion_detallada()`; y `escalonar` /
  `reducir_a_escalonada_reducida` aceptan `formato_numero` para que el
  multiplicador de cada paso salga como fracción ('F2 <- F2 - (1/2) * F1').
- **GUI reescrita en el paquete `ui/`**: flujo de 5 pantallas navegable con teclado
  (menú con info de la app → dimensiones+notación → entrada guiada término a término
  → proceso con los pasos como protagonista + solución y comprobación → solución
  vectorial renderizada con el código LaTeX oculto tras "Ver sintaxis LaTeX").
  `gui.py` es un shim que llama a `ui.app.main`.
- Tooltips con `QToolButton` (funcionan también con teclado); fuente elegida por
  código (sin warning de "Segoe UI").
- Issue #18 (migrar consola a Textual TUI): abierto como investigación, no implementado.

**Feature previa:** Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas
(mergeada a main 2026-08-31).

**Migración a `uv`:** `pyproject.toml` + `uv.lock` en su sitio; documentación actualizada.

### Decisiones Tomales Anteriormente

1. **Sin librerías externas** - Exigencia del ejercicio educativo
2. **Solución vectorial explícita** - Para entendimiento matemático
3. **PyQt6 para GUI** - Moderno y bien mantenido
4. **uv en lugar de pip** - 10-100x más rápido

### Temas Futuros (Out of Scope Ahora)

- Migrar la consola a **Textual TUI** (issue #18)
- LaTeX de alta fidelidad en la GUI: matplotlib `mathtext` o `QWebEngineView` + KaTeX (issue #15)
- Método de Cramer
- Factorización LU
- Descomposición QR
- Valores y vectores propios
- Interfaz web (Django/FastAPI)

## 📝 Cómo Contribuir

### 1. Crear Issue Primero
```bash
gh issue create --title "Descripción" --body "Contexto y motivación"
```

### 2. Crear Rama
```bash
git checkout -b feature/nombre-descriptivo
# O: chore/docs, fix/bug-name
```

### 3. Implementar
```bash
# Actualizar código
# Agregar tests
# Actualizar docs
# Verificar: python3 test_gauss.py
```

### 4. Crear PR
```bash
gh pr create --title "..." --body "..." --reviewer @colega
```

## ❓ FAQ para Agentes

**P: ¿Debo usar NumPy para esto?**  
R: NO por ahora. Es una restricción de la fase actual (comprensión profunda) y
vive en `core/` — se irá levantando con el contenido del curso. Ver `docs/RUMBO.md`.

**P: ¿Cómo agrego una nueva función?**  
R: 1) Elegir `gauss.py`, `gauss_jordan.py` o `vectores.py`, 2) agregar el test
correspondiente, 3) integrar mediante `ui/state.py` + una pantalla. **No** en
`main.py` (se deprecará en #28).

**P: ¿Los tests deben pasar?**  
R: SÍ. Siempre. Si algo falla, es un bloqueador.

**P: ¿Rompo algo si edito `gauss.py`?**  
R: Posiblemente. Verifica: `uv run --extra dev pytest`

**P: ¿Dónde está la documentación matemática?**  
R: En `docs/ALGORITMO.md` (completa) y `docs/CASOS_PRUEBA.md` (práctica)

---

**Última actualización:** 2026-09-08

**Estado del Repo:** Tareas 1–3 en `main` (`v3.0.0` = #29 `806dc24`; #30
`00ba185`). 78 tests. Trabajo estructural planificado en #28 → #26 → #27; épicos
#31 (glosario), #32 (server), #33 (Manim), spike #34 (Lean). Mapa completo en
[`docs/RUMBO.md`](docs/RUMBO.md).
