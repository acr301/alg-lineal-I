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

## 🎓 Restricciones Deliberadas

### NO se permite:
- NumPy, SymPy, scipy
- Funciones de álgebra lineal preconstruidas
- Librerías matemáticas externas

### SÍ se permite:
- Listas y diccionarios básicos
- Loops y condicionales
- Aritmética de punto flotante
- PyQt6 (solo para GUI, no matemática)

**Razón:** El ejercicio requiere implementar desde cero para comprensión profunda.

## 📊 Estado Actual (2026-08-31)

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
- `generar_latex_solucion()` - Código LaTeX copiable
- Panel de análisis en GUI
- 18 nuevos tests
- Mergeado a main

### 🔄 En Progreso

#### Chore: Migración a `uv` para Gestión de Paquetes
- `pyproject.toml` creado
- `uv.lock` sincronizado
- Documentación actualizada (AGENTS.md, docs/*)
- Estado: PR pendiente

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
| Líneas de código | ~800 |
| Tests | 21 (100% pass) |
| Funciones en gauss.py | 20+ |
| Restricción sin librerías | ✓ Cumplida |
| Documentación | ✓ Completa |
| GUI funcional | ✓ Sí |

## 🏗️ Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────┐
│      Interfaz Gráfica (gui.py)          │
│    - Entrada de matriz (tabla)          │
│    - Visualización paso a paso          │
│    - Panel de análisis avanzado         │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│     Interfaz de Consola (main.py)       │
│    - Entrada interactiva                │
│    - Salida formateada                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Lógica Pura (gauss.py)             │
│   - Eliminación de Gauss                │
│   - Clasificación del sistema           │
│   - Análisis de rango/nulidad           │
│   - Formas escalonadas                  │
│   - Solución vectorial                  │
│   - Generación LaTeX                    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Python 3.9+ puro                 │
│    (Listas, loops, aritmética)          │
└─────────────────────────────────────────┘
```

## 🔗 Dependencias

### Runtime
- **PyQt6** >= 6.6: GUI moderna y responsiva

### Development
- **uv**: Gestor de paquetes rápido
- **pytest** (opcional): Tests avanzados

### Nulas
- ❌ NumPy
- ❌ SymPy
- ❌ scipy
- ❌ Cualquier álgebra lineal

## 🧪 Testing

- **test_gauss.py**: 18 tests unitarios
  - Sistemas determinados
  - Sistemas indeterminados
  - Sistemas inconsistentes
  - Rango y nulidad
  - Formas escalonadas
  - Solución vectorial

- **test_main.py**: 3 tests de integración
  - Flujo completo consola

**Ejecución:** `python3 test_gauss.py && python3 test_main.py`

## 👥 Colaboradores

- **Autores:** Andrés Castillo y Fátima Zogaib (Grupo 7)

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

**Última actualización:** 2026-08-31  
**Versión del proyecto:** 1.0.0  
**Estatus:** En desarrollo activo (Feature 3 mergeada, Feature 4 en progreso)
