# CASOS_PRUEBA.md - Playbook de Testing

**Nota:** Playbook completo con datos listos y capturas en: `DOCUMENTACION_FEATURE.md`

## Tres Casos Fundamentales

### 🟢 CASO 1: Solución Única (3×3)

**Sistema:**
```
x + y + z = 6
0x + 2y + 5z = -4
2x + 5y - z = 27
```

**Entrada en GUI o Consola:**
```
Ecuaciones: 3, Incógnitas: 3
E1: [1, 1, 1] | 6
E2: [0, 2, 5] | -4
E3: [2, 5, -1] | 27
```

**Resultado esperado:**
- x = 5, y = 3, z = -2
- Rango(A) = 3, Nulidad = 0
- Forma = RREF
- Tipo = "determinado"

**En GUI:**
1. Menú → "Ejemplo rápido" → "Solución única" (salta al proceso).
2. Pantalla "3 · Proceso y resultado": recorre los pasos con ← →.
3. Debajo: solución `x₁=5, x₂=3, x₃=-2` y la comprobación término a término.
4. "Ver solución vectorial →" muestra `x = [5, 3, -2]` renderizado.

---

### 🟡 CASO 2: Infinitas Soluciones (3×3)

**Sistema:**
```
x + y + z = 6
2x + 2y + 2z = 12
x - y + 0z = 0
```

**Entrada:**
```
Ecuaciones: 3, Incógnitas: 3
E1: [1, 1, 1] | 6
E2: [2, 2, 2] | 12
E3: [1, -1, 0] | 0
```

**Resultado esperado:**
- Rango(A) = 2, Nulidad = 1
- Variable libre: x₃ = t₁
- Solución: x = [3, 3, 0] + t₁·[-1/2, -1/2, 1]
- Forma = RREF
- Tipo = "indeterminado"

**En GUI - Lo Especial:**
1. Menú → "Ejemplo rápido" → "Variables libres".
2. Pantalla "3 · Proceso y resultado":
   - solución paramétrica `x₁ = 3 − 1/2·t₁`, `x₂ = 3 − 1/2·t₁`, `x₃ = t₁`;
   - análisis: Rango 2, Nulidad 1, Rango+Nulidad = 3 = n, Forma RREF (con ayudas `?`).
3. "Ver solución vectorial →": `x = [3,3,0] + t₁[-1/2,-1/2,1]` renderizado; el
   código LaTeX está detrás de "Ver sintaxis LaTeX" (con botón "Copiar LaTeX").

**LaTeX generado (con `\frac`):**
```latex
\mathbf{x_p} = \begin{pmatrix} 3 \\ 3 \\ 0 \end{pmatrix}
\mathbf{v_{1}} = \begin{pmatrix} -\frac{1}{2} \\ -\frac{1}{2} \\ 1 \end{pmatrix}
\mathbf{x} = \mathbf{x_p} + t_{1} \mathbf{v_{1}}
```

---

### 🔴 CASO 3: Sin Solución (2×2)

**Sistema:**
```
x + y = 2
x + y = 5
```

**Entrada:**
```
Ecuaciones: 2, Incógnitas: 2
E1: [1, 1] | 2
E2: [1, 1] | 5
```

**Resultado esperado:**
- Contradicción: 0 = 3
- Rango(A) = 1, Rango([A|b]) = 2
- Tipo = "incompatible"
- Sin solución

**En GUI:**
1. Menú → "Ejemplo rápido" → "Sistema inconsistente".
2. En los pasos aparece la fila `[0, 0 | 3]`.
3. Estado rojo: "Sistema inconsistente · no tiene solución"; el bloque de solución
   explica "Una ecuación se redujo a 0 = c...".

---

## Verificación Manual (Consola)

```bash
cd semana2/tarea1
uv run python main.py

# Ingresa los datos del Caso 1
# Verás cada paso (multiplicadores como fracción: F3 <- F3 - (1/2) * F1)
# Resultado: x=5, y=3, z=-2
# Comprobación: 1·(5) + 1·(3) + 1·(-2) = 6 = 6 ✓
```

---

## Tests Automáticos

Todos los casos están cubiertos por tests:

```bash
uv run --extra dev pytest

# Salida:
# test_solucion_unica_3x3 ... ok
# test_infinitas_soluciones ... ok
# test_sin_solucion ... ok
# ...
# 44 passed
# OK
```

---

## Variantes (Opcional)

### Sistema Rectangular 2×4 (más incógnitas)

```
x + 2y + 3z + 4w = 10
2x + 4y + 6z + 8w = 20
```

**Esperado:** Sistema indeterminado con 3 variables libres

### Sistema Rectangular 3×2 (más ecuaciones)

```
x + y = 3
2x + 2y = 6
x - y = 1
```

**Esperado:** Sistema indeterminado (las dos primeras son iguales)

---

## Checklist para Documentación Visual

- [ ] Captura: Caso 1 - Matriz inicial
- [ ] Captura: Caso 1 - Pasos de eliminación
- [ ] Captura: Caso 1 - Resultado (x=5, y=3, z=-2)
- [ ] Captura: Caso 1 - Panel análisis
- [ ] Captura: Caso 2 - Matriz inicial
- [ ] Captura: Caso 2 - RREF final
- [ ] Captura: Caso 2 - Solución vectorial
- [ ] Captura: Caso 2 - Panel LaTeX
- [ ] Captura: Caso 3 - Contradicción [0 0 | 3]
- [ ] Captura: Caso 3 - Estado inconsistente

---

**Más detalles en:** `DOCUMENTACION_FEATURE.md`
