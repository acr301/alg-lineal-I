# ONBOARDING.md - Guía Rápida de Inicio

¿Eres nuevo aquí? Comienza aquí. Después de esto, estarás listo para trabajar.

## ⏱️ Tiempo Estimado: 10-15 minutos

## 1️⃣ Instalación (2 minutos)

```bash
# Instalar uv (si no lo tienes)
pip install uv

# Clonar el repo (si no lo has hecho)
git clone https://github.com/acr301/alg-lineal-I.git
cd alg-lineal-I

# Sincronizar dependencias (el núcleo no tiene ninguna; `qt` añade la GUI)
uv sync --extra qt
```

## 2️⃣ Exploración (5 minutos)

```bash
# Ver estructura
ls -la
cat AGENTS.md          # Punto de entrada para agentes
cat docs/PROYECTO.md   # Visión general

# Ver estado actual
cat context/current-feature.md
```

## 3️⃣ Primer Run (3 minutos)

### Interfaz Gráfica
```bash
# desde la raíz del repo
uv sync --extra qt
uv run aqua-gauss     # con `uv run` para que matplotlib renderice las fórmulas
```

La GUI es un flujo de pantallas navegable **sin ratón** (Enter avanza, Esc
retrocede, ← → recorren pasos, F1 vuelve al menú):

1. **Menú** → elige "Ejemplo rápido" → "Solución única" (salta directo al proceso).
2. **Proceso y resultado**: recorre los pasos con ← →; abajo, la solución y su
   comprobación término a término, y el análisis de rango/nulidad/forma.
3. **Solución vectorial**: la notación renderizada; el código LaTeX está detrás de
   "Ver sintaxis LaTeX".

Para crear un sistema propio: "Iniciar" → dimensiones y notación → entrada
guiada término a término.

> La consola (`main.py`) se retiró en el refactor a `core/` + `clients/`: no era
> requisito y la TUI (#18) cubrirá el terminal.

**Sistema de ejemplo** (E1: 1,1,1|6 · E2: 0,2,5|-4 · E3: 2,5,-1|27) → solución
x=5, y=3, z=-2.

## 4️⃣ Tests (2 minutos)

```bash
# Desde la raíz del repo (deben pasar):
uv run --extra dev pytest
# Salida esperada: 70 passed
```

## 5️⃣ Entender la Estructura (3 minutos)

```
src/aqua_gauss/
├── app.py                ← entry point (aqua-gauss / python -m aqua_gauss)
├── core/                 ← MODEL PURO (sin I/O, sin imports de framework)
│   ├── gauss.py              Eliminación de Gauss, rango/nulidad,
│   │                         formas escalonadas, solución vectorial
│   ├── gauss_jordan.py       RREF y solución paramétrica
│   ├── vectores.py           operaciones en R^n, combinaciones, axiomas
│   └── formato.py            PRESENTACIÓN texto (float → fracción/decimal, LaTeX, HTML)
└── clients/qt/           ← CLIENTE PyQt6 por pantallas
    ├── app.py               ventana principal (QStackedWidget) + atajos
    ├── state.py             Sesion: único punto de la GUI que llama a core/
    ├── mathrender.py        PRESENTACIÓN imagen (LaTeX → QPixmap con matplotlib)
    ├── theme.py             estilo, paleta, fuente
    ├── widgets.py           PantallaBase, MatrizGrid, navegación, ayudas
    └── screen_*.py          menú, dimensiones, entrada, proceso, resultado, vectores

tests/
├── core/   test_gauss (21) · test_gauss_jordan (6) · test_vectores (12) · test_formato (20)
└── qt/     test_mathrender (3) · test_ui (8)
```

## 🚫 Restricción Crítica

**NO uses:**
- NumPy
- SymPy
- scipy
- Cualquier "álgebra lineal externa"

**Usa:**
- Listas: `[]`
- Loops: `for`, `while`
- Aritmética: `+, -, *, /`

**Por qué:** El ejercicio requiere comprensión profunda. Las librerías son "cajas negras".

## 🎯 Primer Task (Recomendado)

Para familiarizarte, intenta **agregar un comentario a una función en gauss.py**:

```bash
# 1. Abre el archivo
vim src/aqua_gauss/core/gauss.py

# 2. Busca la función escalonar()
# 3. Lee el código

# 4. Entiende: ¿Qué hace cada loop?
# (No modifiques aún, solo lee)

# 5. Corre los tests
uv run --extra dev pytest  # Debe pasar
```

## ✅ Checklist: "Estoy Listo"

- [ ] He instalado uv y ejecutado `uv sync --extra qt`
- [ ] He ejecutado la GUI sin errores
- [ ] He visto los 3 casos de prueba ejemplo
- [ ] He corrido todos los tests (70 pass)
- [ ] He leído `docs/PROYECTO.md`
- [ ] Sé dónde está la lógica (`src/aqua_gauss/core/`)
- [ ] Entiendo la restricción: sin NumPy

## 📚 Siguiente: Profundidad

Si completaste lo anterior, lee en orden:

1. **docs/ARQUITECTURA.md** - Cómo está diseñado
2. **docs/ALGORITMO.md** - Fundamentos matemáticos
3. **docs/CASOS_PRUEBA.md** - Datos listos para probar

## 🆘 Ayuda Rápida

**"¿Cómo agrego una función?"**
1. Agrégala en `src/aqua_gauss/core/` (lógica pura, sin imports de framework)
2. Escribe test en `tests/core/test_gauss.py`
3. Verifica: `uv run --extra dev pytest` (debe pasar)
4. Si se usa en la GUI, llámala desde `clients/qt/state.py:Sesion` y
   muéstrala en la pantalla que corresponda (`clients/qt/screen_*.py`).
   Para formatear números usa `core.formato.formatear_valor` / `sesion.fmt`.

**"¿Cómo aumento los tests?"**
1. Abre `tests/core/test_gauss.py`
2. Busca la clase relevante (ej: `TestRango`)
3. Agrega método `def test_mi_caso(self):`
4. Usa `self.assertEqual()`, `self.assertTrue()`, etc.

**"¿Está mal algo?"**
1. Corre: `uv run --extra dev pytest`
2. Busca el test fallido
3. Lee el error: te dice exactamente qué está mal
4. Si es de compilación: `uv run python -m compileall src/`

## 🎓 Después del Onboarding

Una vez hayas completado esto:

1. **Abre una issue:** Describe qué quieres hacer
2. **Crea una rama:** `git checkout -b feature/tu-feature`
3. **Implementa:** Código + Tests + Docs
4. **Haz PR:** Menciona la issue
5. **Pide review:** Agrega colaboradores

---

**¿Listo?** Comienza con el paso 1️⃣
