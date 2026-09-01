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

# Sincronizar dependencias
uv sync
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

### Opción A: Interfaz Gráfica (recomendado)
```bash
cd semana2/tarea1
python3 gui.py
```

**Qué hacer:**
1. Haz clic en "Ejemplo rápido" → "Solución única"
2. Haz clic en "Resolver sistema"
3. Usa el slider para ver cada paso
4. Abre el panel "4 · Análisis avanzado"

### Opción B: Consola
```bash
cd semana2/tarea1
python3 main.py
```

**Qué hacer:**
1. Ingresa 3 ecuaciones, 3 incógnitas
2. Ingresa los coeficientes:
   - E1: 1, 1, 1 | 6
   - E2: 0, 2, 5 | -4
   - E3: 2, 5, -1 | 27
3. Observa la solución: x=5, y=3, z=-2

## 4️⃣ Tests (2 minutos)

```bash
cd semana2/tarea1

# Todos los tests (deben pasar)
python3 test_gauss.py
python3 test_main.py

# Salida esperada:
# Ran 21 tests... OK
```

## 5️⃣ Entender la Estructura (3 minutos)

```
semana2/tarea1/
├── gauss.py          ← LÓGICA PURA (sin I/O)
│                       - Eliminación de Gauss
│                       - Rango, nulidad
│                       - Formas escalonadas
│                       - Solución vectorial
├── main.py           ← CONSOLA (lee, escribe)
│                       - Pide entrada
│                       - Muestra resultados
├── gui.py            ← GUI PyQt6 (visual)
│                       - Tabla de entrada
│                       - Slider de pasos
│                       - Panel de análisis
├── test_gauss.py     ← TESTS (18 tests)
└── test_main.py      ← TESTS (3 tests)
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
vim semana2/tarea1/gauss.py

# 2. Busca la función escalonar()
# 3. Lee el código

# 4. Entiende: ¿Qué hace cada loop?
# (No modifiques aún, solo lee)

# 5. Corre los tests
python3 test_gauss.py  # Debe pasar
```

## ✅ Checklist: "Estoy Listo"

- [ ] He instalado uv y ejecutado `uv sync`
- [ ] He ejecutado la GUI sin errores
- [ ] He visto los 3 casos de prueba ejemplo
- [ ] He corrido todos los tests (21 pass)
- [ ] He leído `docs/PROYECTO.md`
- [ ] Sé dónde está la lógica (`gauss.py`)
- [ ] Entiendo la restricción: sin NumPy

## 📚 Siguiente: Profundidad

Si completaste lo anterior, lee en orden:

1. **docs/ARQUITECTURA.md** - Cómo está diseñado
2. **docs/ALGORITMO.md** - Fundamentos matemáticos
3. **docs/CASOS_PRUEBA.md** - Datos listos para probar

## 🆘 Ayuda Rápida

**"¿Cómo agrego una función?"**
1. Agrégala en `gauss.py` (lógica pura)
2. Escribe test en `test_gauss.py`
3. Verifica: `python3 test_gauss.py` (debe pasar)
4. Si usas en GUI/consola, integra en `main.py` o `gui.py`

**"¿Cómo aumento los tests?"**
1. Abre `test_gauss.py`
2. Busca la clase relevante (ej: `TestRango`)
3. Agrega método `def test_mi_caso(self):`
4. Usa `self.assertEqual()`, `self.assertTrue()`, etc.

**"¿Está mal algo?"**
1. Corre: `python3 test_gauss.py`
2. Busca el test fallido
3. Lee el error: te dice exactamente qué está mal
4. Si es de compilación: `python3 -m py_compile gauss.py main.py gui.py`

## 🎓 Después del Onboarding

Una vez hayas completado esto:

1. **Abre una issue:** Describe qué quieres hacer
2. **Crea una rama:** `git checkout -b feature/tu-feature`
3. **Implementa:** Código + Tests + Docs
4. **Haz PR:** Menciona la issue
5. **Pide review:** Agrega colaboradores

---

**¿Listo?** Comienza con el paso 1️⃣
