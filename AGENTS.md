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
│   ├── gauss.py                 # Lógica pura (sin I/O, sin librerías externas)
│   ├── main.py                  # Interfaz de consola
│   ├── gui.py                   # Interfaz PyQt6
│   ├── test_gauss.py            # 18 tests unitarios
│   ├── test_main.py             # 3 tests de integración
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
# GUI (interfaz gráfica)
cd semana2/tarea1
python3 gui.py

# O consola
python3 main.py

# O tests
python3 test_gauss.py
```

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

- [ ] Tests verdes (21 tests deben pasar)
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
| uv | 0.10+ | Gestor de paquetes rápido |
| unittest | stdlib | Tests sin dependencias |
| Algoritmo | Puro | Sin NumPy/SymPy |

## 🚫 Restricciones Críticas

1. **NO librerías de álgebra lineal** (NumPy, SymPy, scipy)
   - Razón: El ejercicio exige implementación desde cero
   - Usar: Listas, loops, aritmética básica

2. **NO romper funcionalidades existentes**
   - Todos los tests deben pasar
   - Si modificas `gauss.py`, actualiza tests

3. **Separación de responsabilidades**
   - `gauss.py`: Lógica pura (SIN input/print)
   - `main.py`: UI de consola
   - `gui.py`: UI PyQt6

## 📊 Métricas Actuales

- **Líneas de código:** ~800 (gauss.py: 560, GUI: 400, main: 150)
- **Tests:** 21 (todos pasan)
- **Cobertura:** Lógica principal cubierta
- **Estado:** Feature completada y mergeada

## 🤖 Memoria para Agentes

### Contexto Compartido

**Última feature completada:** Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas
- 6 funciones nuevas en `gauss.py`
- Panel de análisis en GUI
- 18 nuevos tests
- Generación de código LaTeX
- Mergeado a main: 2026-08-31

**Migración en curso:** Cambio a `uv` para gestión de paquetes
- `pyproject.toml` creado
- `uv.lock` sincronizado
- Documentación actualizada
- Estado: PR pendiente

### Decisiones Tomales Anteriormente

1. **Sin librerías externas** - Exigencia del ejercicio educativo
2. **Solución vectorial explícita** - Para entendimiento matemático
3. **PyQt6 para GUI** - Moderno y bien mantenido
4. **uv en lugar de pip** - 10-100x más rápido

### Temas Futuros (Out of Scope Ahora)

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
**Estado del Repo:** Feature feature/solucion-vectorial mergeada, migration a uv en progreso
