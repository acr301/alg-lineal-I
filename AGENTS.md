# AGENTS.md - Guía para Agentes IA y Colaboradores

Este archivo es la **puerta de entrada para agentes IA** (como Claude) que trabajen en este repositorio. Contiene:
- Estructura del proyecto
- Contexto crítico
- Cómo ejecutar y contribuir
- Memoria compartida del proyecto

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
│   └── CASOS_PRUEBA.md          # Playbook con datos listos
├── semana2/tarea1/
│   ├── gauss.py                 # Lógica pura (sin I/O, sin imports)
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

La GUI es un flujo de pantallas (menú → dimensiones → entrada guiada → proceso →
solución vectorial), navegable **sin ratón**: Enter avanza, Esc retrocede,
← → recorren los pasos, F1 vuelve al menú.

## 🎯 Responsabilidades del Agente

### Antes de Trabajar

- [ ] Leer `docs/PROYECTO.md` para entender el contexto
- [ ] Leer `docs/ARQUITECTURA.md` para entender decisiones técnicas
- [ ] Revisar `context/current-feature.md` para estado actual
- [ ] Ejecutar tests para verificar que todo funciona

### Durante el Trabajo

- [ ] NO usar NumPy, SymPy ni librerías de álgebra lineal (restricción del ejercicio)
- [ ] Mantener separación: `gauss.py` (lógica pura), `main.py` (consola), `gui.py` (GUI)
- [ ] NO romper tests existentes
- [ ] Commits atómicos con mensajes descriptivos

### Al Completar

- [ ] Tests verdes (44 tests deben pasar)
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
| Algoritmo | Puro | Sin NumPy/SymPy — `gauss.py` no importa nada |
| `gauss.py` / `formato.py` | Puro | Sin imports (ni `fractions`): fracción por Euclides + fracción continua |

## 🚫 Restricciones Críticas

1. **NO librerías de álgebra lineal** (NumPy, SymPy, scipy)
   - Razón: El ejercicio exige implementación desde cero
   - Usar: Listas, loops, aritmética básica
   - `matplotlib` está permitido **solo** como motor de render (LaTeX → imagen) en
     `mathrender.py`; nunca para calcular. `gauss.py` y `formato.py` siguen sin imports.

2. **NO romper funcionalidades existentes**
   - Todos los tests deben pasar
   - Si modificas `gauss.py`, actualiza tests

3. **Separación de responsabilidades**
   - `gauss.py`: Lógica pura (SIN input/print, SIN imports)
   - `formato.py`: Presentación texto (float → fracción/decimal, LaTeX, HTML)
   - `mathrender.py`: Presentación imagen (LaTeX → QPixmap con matplotlib)
   - `main.py`: UI de consola
   - `ui/`: UI PyQt6 por pantallas; `ui/state.py:Sesion` es el ÚNICO sitio de la
     GUI que llama a `gauss.py`. Cada pantalla es un `ui/screen_*.py`.
   - No dupliques formateo de números: usa `formato.formatear_valor(v, modo)` o
     `sesion.fmt(v)`.

## 📊 Métricas Actuales

- **Líneas de código:** ~1000 (gauss.py, formato.py, gui.py, main.py)
- **Tests:** 44 (todos pasan) — test_gauss (21), test_formato (14), test_mathrender (3), test_main (3), test_ui (3)
- **Cobertura:** Lógica principal y capa de formato cubiertas
- **Estado:** Feature completada y mergeada

## 🤖 Memoria para Agentes

### Contexto Compartido

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
R: NO. Es una restricción deliberada del ejercicio. Usa listas y loops.

**P: ¿Cómo agrego una nueva función?**  
R: 1) Agregar en `gauss.py`, 2) Agregar tests en `test_gauss.py`, 3) Integrar en `main.py` o `gui.py`

**P: ¿Los tests deben pasar?**  
R: SÍ. Siempre. Si algo falla, es un bloqueador.

**P: ¿Rompo algo si edito `gauss.py`?**  
R: Posiblemente. Verifica: `python3 test_gauss.py && python3 test_main.py`

**P: ¿Dónde está la documentación matemática?**  
R: En `docs/ALGORITMO.md` (completa) y `docs/CASOS_PRUEBA.md` (práctica)

---

**Última actualización:** 2026-08-31  
**Versión:** 1.0.0  
**Estado del Repo:** rama `fix/latex-renderizado-fracciones-verificacion` en curso (issues #15/#16/#17); issue #18 (Textual TUI) abierto
