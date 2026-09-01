# ALGORITMO.md - Explicación Técnica

Para documentación completa con playbook interactivo, ver: `DOCUMENTACION_FEATURE.md`

## Fundamentos

**Eliminación de Gauss:** Reducir matriz [A|b] a forma escalonada para resolver Ax=b.

**Fases:**
1. Reducción a forma escalonada (REF)
2. Clasificación del sistema
3. Para indeterminados: reducción a forma escalonada reducida (RREF)
4. Construcción de solución

## Algoritmo Principal: escalonar()

```
Para cada columna j = 0 hasta n-1:
  1. Encontrar pivote: fila con máx|a[i][j]| desde fila_actual
  2. Si pivote ≈ 0, ir a siguiente columna (variable libre)
  3. Intercambiar fila_pivote con fila_actual (pivoteo)
  4. Hacer ceros debajo del pivote:
     factor = a[i][j] / pivote
     a[i][k] -= factor * a[fila_actual][k] para todo k
  5. Registrar columna_pivote
```

**Resultado:** Forma escalonada + lista de columnas pivote

## Clasificación: clasificar()

```
Si existe fila [0, 0, ..., 0 | c] con c ≠ 0:
  → "incompatible" (sin solución)
Si rango(A) == n (todas las variables tienen pivote):
  → "determinado" (solución única)
Si rango(A) < n (algunas variables sin pivote):
  → "indeterminado" (infinitas soluciones)
```

## Rango y Nulidad

- **Rango:** Número de filas no nulas = número de pivotes
- **Nulidad:** n - rango = número de variables libres
- **Teorema:** Rango + Nulidad = n (siempre)

```python
rango = len(columnas_pivote)
nulidad = n - rango
assert rango + nulidad == n  # Siempre verdadero
```

## Formas Escalonadas

### REF (Forma Escalonada)

```
1 2 3 4
0 2 5 6
0 0 1 2
0 0 0 0
```

Características:
- Cada pivote está a la derecha del anterior
- Filas nulas al final
- Los pivotes pueden ser cualquier valor ≠ 0

Funciones:
- `es_forma_escalonada(matriz, n, columnas_pivote)` → bool
- `clasificar_forma_escalonada(...)` → "REF" o "ninguna"

### RREF (Forma Escalonada Reducida)

```
1 0 0 3
0 1 0 2
0 0 1 1
0 0 0 0
```

Características:
- Es REF + cada pivote es 1 + es el único en su columna
- Forma más simple de una matriz
- Solución casi lista para leer

Funciones:
- `es_forma_escalonada_reducida(matriz, n, columnas_pivote)` → bool
- Generada por `reducir_a_escalonada_reducida(matriz, ...)`

## Solución Vectorial

Para sistemas indeterminados, la solución se expresa como:

```
x = xp + t1*v1 + t2*v2 + ... + tk*vk
```

**Componentes:**
- `xp`: Solución particular (variables libres = 0)
- `vi`: Vectores del espacio nulo (k = nulidad)
- `ti`: Parámetros libres

**Construcción:**

```python
# 1. Solución particular
particular = evaluar_solucion_parametrica(
    n, libres, expresiones, [0]*len(libres)
)

# 2. Para cada variable libre
vectores_nulos = []
for k, indice_libre in enumerate(libres):
    valores = [0] * len(libres)
    valores[k] = 1
    x_temp = evaluar_solucion_parametrica(n, libres, expresiones, valores)
    vec = [x_temp[i] - particular[i] for i in range(n)]
    vectores_nulos.append(vec)
```

## Ejemplo Completo

**Sistema:**
```
x + y + z = 6
2x + 2y + 2z = 12
x - y + 0z = 0
```

**Paso 1: Escalonar**
```
[1  1  1 | 6]
[2  2  2 | 12]
[1 -1  0 | 0]
    ↓
[1  1  1 | 6]
[0  0  0 | 0]
[0 -2 -1 | -6]
```

**Paso 2: Clasificar**
- Rango = 2 (dos pivotes)
- Variables = 3
- Tipo = "indeterminado"

**Paso 3: RREF**
```
[1  0 1 | 3]
[0  1 0.5 | 3]
[0  0  0 | 0]
```

**Paso 4: Solución Vectorial**
- Variable libre: z = t
- Particular (t=0): xp = [3, 3, 0]
- Vector nulo: v1 = [-1, -0.5, 1] (aproximadamente)
- Solución general: x = [3, 3, 0] + t*[-1, -0.5, 1]

## Comprobación explícita (sustituyendo valores)

La Tarea 1 exige **demostrar** que la solución hallada satisface el sistema
*original* (antes de escalonar). No basta con escribir `6 = 6`: se muestra la
sustitución término a término.

`gauss.py:verificar_solucion_detallada(coeficientes, terminos, x)` devuelve, por
ecuación, la lista `(coef_i, x_i, coef_i·x_i)`, la suma de los productos y el
término independiente esperado. Con eso, consola y GUI imprimen:

```
Ecuación 1:
  1·(5) + 1·(3) + 1·(-2)
  = 5 + 3 - 2
  = 6 = 6 (b1)  ->  OK
```

Para el caso indeterminado se fija un valor concreto a cada parámetro libre
(`t₁ = 0, …`) y se sustituye ese vector. No aplica al caso inconsistente.

## Fracción exacta vs. decimal

El algoritmo trabaja en `float`, pero al escalonar aparecen valores como `0.3333…`
que son en realidad `1/3`. `formato.py:a_fraccion()` reconstruye la fracción exacta
por **fracción continua** (con `formato.py:mcd()` de Euclides para reducir) y
`formatear_valor()` elige entre `"1/3"` y `"0.3333"` según el modo. Se aplica a la
matriz, a cada paso, a la forma final, a los vectores `x_p` / `v_k` y a la
comprobación. Si el valor es irracional (p. ej. `√2`) se cae a decimal.

## Código LaTeX

`formato.py:generar_latex_solucion()` emite las fracciones como `\frac{a}{b}`:

```latex
\mathbf{x_p} = \begin{pmatrix} 3 \\ 3 \\ 0 \end{pmatrix}

\mathbf{v_1} = \begin{pmatrix} -\frac{1}{2} \\ -\frac{1}{2} \\ 1 \end{pmatrix}

\mathbf{x} = \mathbf{x_p} + t_1 \mathbf{v_1}
```

En la GUI, además del código copiable, la solución se muestra **renderizada** con
notación matemática (vectores columna entre corchetes, subíndices reales).

---

**Ver también:**
- `DOCUMENTACION_FEATURE.md` - Explicación detallada y playbook
- `CASOS_PRUEBA.md` - Datos listos para probar
- `test_gauss.py` - Ejemplos reales de uso
