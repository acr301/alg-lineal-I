"""
gauss.py

Implementación "a mano" del método de eliminación de Gauss (reducción por
filas / forma escalonada) para resolver sistemas de ecuaciones lineales
Ax = b, y de la clasificación del sistema según sus soluciones.

Restricción del ejercicio: no se usa numpy, ni ninguna librería estándar,
ni ninguna función de álgebra lineal/vectores ya dada en Python. Todo se
construye con listas, bucles y aritmética básica (los "primitivos" del
lenguaje, no una librería).

Una matriz aumentada [A | b] se representa como una lista de listas:
    matriz[i] = [a_i1, a_i2, ..., a_in, b_i]

Este módulo NO hace entrada/salida (input/print): solo contiene la lógica
del algoritmo, para que sea fácil de probar (ver test_gauss.py) y de
reutilizar desde main.py (la interfaz interactiva).
"""

# Tolerancia para considerar un número "prácticamente cero" al comparar
# resultados de aritmética con punto flotante.
EPS = 1e-9


def valor_casi_cero(valor):
    """Indica si 'valor' debe tratarse como cero dada la tolerancia EPS."""
    return -EPS < valor < EPS


def crear_matriz_aumentada(coeficientes, terminos_independientes):
    """
    Construye la matriz aumentada [A | b] a partir de:
      - coeficientes: lista de m filas, cada una con n coeficientes (A)
      - terminos_independientes: lista de m valores (b)
    """
    aumentada = []
    for i in range(len(coeficientes)):
        fila = list(coeficientes[i]) + [terminos_independientes[i]]
        aumentada.append(fila)
    return aumentada


def copiar_matriz(matriz):
    """Devuelve una copia independiente (deep copy manual) de la matriz."""
    return [list(fila) for fila in matriz]


def intercambiar_filas(matriz, i, j):
    """Intercambia dos filas de la matriz, in place."""
    matriz[i], matriz[j] = matriz[j], matriz[i]


def escalonar(matriz, n_incognitas, registrar_paso=None):
    """
    Reduce 'matriz' (aumentada, de tamaño m x (n_incognitas + 1)) a forma
    escalonada por filas, usando eliminación de Gauss con pivoteo parcial
    (se elige como pivote el mayor valor absoluto disponible en la columna,
    lo que evita divisiones por cero y mejora la estabilidad numérica).

    Modifica 'matriz' in place.

    'registrar_paso' es un callback opcional registrar_paso(descripcion,
    matriz_actual) que se invoca cada vez que se hace una operación de fila,
    para poder narrar el proceso paso a paso.

    Devuelve la lista de columnas donde se encontró un pivote, en el orden
    en que fueron procesadas (una por cada fila pivote).
    """
    m = len(matriz)
    columnas_pivote = []
    fila_actual = 0

    for col in range(n_incognitas):
        if fila_actual >= m:
            break

        # Pivoteo parcial: buscar, desde fila_actual hacia abajo, la fila
        # con mayor valor absoluto en esta columna.
        fila_max = fila_actual
        valor_max = abs(matriz[fila_actual][col])
        for r in range(fila_actual + 1, m):
            if abs(matriz[r][col]) > valor_max:
                valor_max = abs(matriz[r][col])
                fila_max = r

        if valor_casi_cero(valor_max):
            # Toda la columna (desde fila_actual hacia abajo) es cero:
            # no hay pivote aquí, esta columna será variable libre.
            continue

        if fila_max != fila_actual:
            intercambiar_filas(matriz, fila_actual, fila_max)
            if registrar_paso:
                registrar_paso(
                    f"F{fila_actual + 1} <-> F{fila_max + 1} (pivoteo parcial)",
                    matriz,
                )

        pivote = matriz[fila_actual][col]
        for r in range(fila_actual + 1, m):
            if valor_casi_cero(matriz[r][col]):
                continue
            factor = matriz[r][col] / pivote
            for c in range(col, n_incognitas + 1):
                matriz[r][c] -= factor * matriz[fila_actual][c]
            matriz[r][col] = 0.0
            if registrar_paso:
                registrar_paso(
                    f"F{r + 1} <- F{r + 1} - ({factor:.4g}) * F{fila_actual + 1}",
                    matriz,
                )

        columnas_pivote.append(col)
        fila_actual += 1

    return columnas_pivote


def clasificar(matriz, n_incognitas, columnas_pivote):
    """
    Clasifica el sistema ya reducido a forma escalonada:
      - "incompatible": existe una fila del tipo 0 = c, con c != 0.
      - "determinado": rango(A) == número de incognitas -> solución única.
      - "indeterminado": rango(A) < número de incognitas -> infinitas
        soluciones (hay al menos una variable libre).
    """
    for fila in matriz:
        coeficientes_cero = all(
            valor_casi_cero(v) for v in fila[:n_incognitas]
        )
        termino_no_cero = not valor_casi_cero(fila[n_incognitas])
        if coeficientes_cero and termino_no_cero:
            return "incompatible"

    rango = len(columnas_pivote)
    if rango == n_incognitas:
        return "determinado"
    return "indeterminado"


def sustitucion_regresiva(matriz, n_incognitas, columnas_pivote):
    """
    Calcula la solución única x = [x1, ..., xn] por sustitución hacia atrás.
    Solo válido cuando el sistema es "determinado" (columnas_pivote cubre
    todas las incognitas, es decir columnas_pivote == [0, 1, ..., n-1]).
    """
    x = [0.0] * n_incognitas
    for i in range(len(columnas_pivote) - 1, -1, -1):
        col = columnas_pivote[i]
        suma = matriz[i][n_incognitas]
        for j in range(col + 1, n_incognitas):
            suma -= matriz[i][j] * x[j]
        x[col] = suma / matriz[i][col]
    return x


def reducir_a_escalonada_reducida(matriz, n_incognitas, columnas_pivote,
                                   registrar_paso=None):
    """
    A partir de una matriz ya en forma escalonada, continúa el proceso
    (estilo Gauss-Jordan) hasta la forma escalonada reducida: cada pivote
    vale 1 y es el único valor no nulo en su columna. Modifica in place.
    """
    for i in range(len(columnas_pivote) - 1, -1, -1):
        col = columnas_pivote[i]
        pivote = matriz[i][col]
        if not valor_casi_cero(pivote - 1.0):
            for c in range(col, n_incognitas + 1):
                matriz[i][c] /= pivote
            if registrar_paso:
                registrar_paso(f"F{i + 1} <- F{i + 1} / {pivote:.4g}", matriz)

        for r in range(i):
            factor = matriz[r][col]
            if valor_casi_cero(factor):
                continue
            for c in range(col, n_incognitas + 1):
                matriz[r][c] -= factor * matriz[i][c]
            matriz[r][col] = 0.0
            if registrar_paso:
                registrar_paso(
                    f"F{r + 1} <- F{r + 1} - ({factor:.4g}) * F{i + 1}",
                    matriz,
                )


def solucion_parametrica(matriz, n_incognitas, columnas_pivote):
    """
    A partir de la matriz en forma escalonada REDUCIDA, construye la
    descripción de la solución para un sistema indeterminado.

    Devuelve (libres, expresiones):
      - libres: lista de índices de variables libres (parámetros).
      - expresiones: lista de tamaño n_incognitas; para cada índice de
        variable pivote v, expresiones[v] = (termino_independiente, partes)
        donde partes es una lista de (coeficiente, indice_variable_libre)
        tal que x_v = termino_independiente + suma(coeficiente * x_libre).
        Para variables libres, expresiones[v] es None.
    """
    libres = [v for v in range(n_incognitas) if v not in columnas_pivote]
    expresiones = [None] * n_incognitas

    for i, col in enumerate(columnas_pivote):
        termino_independiente = matriz[i][n_incognitas]
        partes = []
        for v in libres:
            coef = matriz[i][v]
            if not valor_casi_cero(coef):
                partes.append((-coef, v))
        expresiones[col] = (termino_independiente, partes)

    return libres, expresiones


def evaluar_solucion_parametrica(n_incognitas, libres, expresiones, valores_libres):
    """
    Construye una solucion concreta x = [x1, ..., xn] a partir de la solucion
    parametrica devuelta por solucion_parametrica(), asignando un valor
    numerico a cada variable libre.

    'valores_libres' es una lista alineada con 'libres': valores_libres[k] es
    el valor que se le asigna a la variable libre libres[k].

    Util para construir un ejemplo concreto (p. ej. con parametros = 0 o 1)
    y poder verificar que satisface el sistema original.
    """
    x = [0.0] * n_incognitas
    for indice_libre, valor in zip(libres, valores_libres):
        x[indice_libre] = valor

    for v in range(n_incognitas):
        if expresiones[v] is None:
            continue
        termino_independiente, partes = expresiones[v]
        valor = termino_independiente
        for coef, indice_libre in partes:
            valor += coef * x[indice_libre]
        x[v] = valor

    return x


def verificar_solucion(coeficientes, terminos_independientes, x):
    """
    Sustituye la solucion 'x' en el sistema ORIGINAL (antes de escalonar) y
    comprueba, ecuacion por ecuacion, que A*x sea igual a b.

    Devuelve una lista de tuplas (valor_calculado, valor_esperado, coincide):
      - valor_calculado: resultado de evaluar la fila i de A contra x.
      - valor_esperado: terminos_independientes[i] (b_i).
      - coincide: True si valor_calculado es (casi) igual a valor_esperado.
    """
    resultados = []
    for fila, b_i in zip(coeficientes, terminos_independientes):
        valor_calculado = 0.0
        for coef, xj in zip(fila, x):
            valor_calculado += coef * xj
        coincide = valor_casi_cero(valor_calculado - b_i)
        resultados.append((valor_calculado, b_i, coincide))
    return resultados


def rango_matriz(matriz, n_incognitas):
    """
    Calcula el rango de una matriz (número de filas no nulas o número de
    pivotes). La matriz debe estar en forma escalonada.
    """
    rango = 0
    for fila in matriz:
        tiene_pivote = any(not valor_casi_cero(fila[col]) for col in range(n_incognitas))
        if tiene_pivote:
            rango += 1
    return rango


def verificar_rango_nulidad(matriz, n_incognitas, columnas_pivote):
    """
    Verifica el teorema del rango-nulidad: Rango(A) + Nulidad(A) = n.

    Devuelve un diccionario con:
      - rango: número de pivotes
      - nulidad: número de variables libres
      - suma: rango + nulidad
      - es_valido: True si suma == n_incognitas
    """
    rango = len(columnas_pivote)
    nulidad = n_incognitas - rango
    suma = rango + nulidad

    return {
        "rango": rango,
        "nulidad": nulidad,
        "suma": suma,
        "es_valido": suma == n_incognitas
    }


def es_forma_escalonada(matriz, n_incognitas, columnas_pivote):
    """
    Verifica si una matriz está en forma escalonada por filas (REF).
    Condiciones:
      1. Las filas nulas están al final.
      2. En cada fila no nula, el pivote está a la derecha del pivote de la fila anterior.
      3. Los pivotes no tienen que ser 1, ni ser los únicos valores no nulos en su columna.
    """
    if not columnas_pivote:
        # Sin pivotes: todas las filas deben ser nulas
        return all(all(valor_casi_cero(v) for v in fila[:n_incognitas])
                   for fila in matriz)

    # Verificar que hay exactamente len(columnas_pivote) filas no nulas
    num_filas_nulas = 0
    for fila in matriz:
        if all(valor_casi_cero(v) for v in fila[:n_incognitas]):
            num_filas_nulas += 1

    num_filas_no_nulas = len(matriz) - num_filas_nulas

    # Si hay distinto número de filas no nulas que pivotes, algo está mal
    if num_filas_no_nulas != len(columnas_pivote):
        return False

    # Verificar que las filas nulas están al final
    primera_fila_nula = -1
    for i, fila in enumerate(matriz):
        es_nula = all(valor_casi_cero(v) for v in fila[:n_incognitas])
        if es_nula and primera_fila_nula == -1:
            primera_fila_nula = i
        elif not es_nula and primera_fila_nula != -1:
            return False

    # Verificar que los pivotes están en orden (columna creciente)
    # y que cada pivote realmente existe en su posición
    for i in range(len(columnas_pivote)):
        if i > 0 and columnas_pivote[i] <= columnas_pivote[i - 1]:
            return False
        # Verificar que la fila i tiene un pivote no nulo en columnas_pivote[i]
        if valor_casi_cero(matriz[i][columnas_pivote[i]]):
            return False

    return True


def es_forma_escalonada_reducida(matriz, n_incognitas, columnas_pivote):
    """
    Verifica si una matriz está en forma escalonada reducida por filas (RREF).
    Condiciones (además de REF):
      1. Cada pivote es 1.
      2. Cada pivote es el único valor no nulo en su columna.
    """
    if not es_forma_escalonada(matriz, n_incognitas, columnas_pivote):
        return False

    for i, col in enumerate(columnas_pivote):
        # Verificar que el pivote es 1
        if not valor_casi_cero(matriz[i][col] - 1.0):
            return False

        # Verificar que es el único valor no nulo en su columna
        for j in range(len(matriz)):
            if i != j and not valor_casi_cero(matriz[j][col]):
                return False

    return True


def clasificar_forma_escalonada(matriz, n_incognitas, columnas_pivote):
    """
    Clasifica la forma de una matriz ya en forma escalonada.

    Devuelve:
      - "RREF": forma escalonada reducida por filas
      - "REF": forma escalonada por filas (pero no reducida)
      - "ninguna": no está en ninguna forma escalonada
    """
    if es_forma_escalonada_reducida(matriz, n_incognitas, columnas_pivote):
        return "RREF"
    elif es_forma_escalonada(matriz, n_incognitas, columnas_pivote):
        return "REF"
    else:
        return "ninguna"


def solucion_general_vectorial(matriz, n_incognitas, columnas_pivote, libres, expresiones):
    """
    Construye la solución general vectorial en la forma:
    x = xp + t1*v1 + t2*v2 + ... + tk*vk

    donde:
      - xp es una solución particular (con variables libres = 0)
      - v1, v2, ..., vk son los vectores de espacio nulo (k = número de variables libres)
      - t1, t2, ..., tk son los parámetros libres

    Devuelve un diccionario:
      - particular: vector solución particular
      - vectores_nulos: lista de vectores del espacio nulo
      - variables_libres: lista de índices de variables libres
      - expresion_str: descripción en forma string de la solución
    """
    # Solución particular: asignar 0 a todas las variables libres
    particular = evaluar_solucion_parametrica(n_incognitas, libres, expresiones, [0] * len(libres))

    # Vectores del espacio nulo
    vectores_nulos = []
    for k, indice_libre in enumerate(libres):
        # Vector correspondiente a la variable libre k-ésima
        vec = [0.0] * n_incognitas
        vec[indice_libre] = 1.0  # Este parámetro vale 1

        # Asignar valores a las otras variables libres (todos 0 excepto este)
        valores_libres_temp = [0.0] * len(libres)
        valores_libres_temp[k] = 1.0
        x_temp = evaluar_solucion_parametrica(n_incognitas, libres, expresiones, valores_libres_temp)

        # El vector es x_temp - particular
        for i in range(n_incognitas):
            vec[i] = x_temp[i] - particular[i]

        vectores_nulos.append(vec)

    return {
        "particular": particular,
        "vectores_nulos": vectores_nulos,
        "variables_libres": libres,
        "expresion_str": _construir_expresion_string(particular, vectores_nulos, libres)
    }


def _construir_expresion_string(particular, vectores_nulos, variables_libres):
    """Helper para construir una descripción textual de la solución vectorial."""
    if not variables_libres:
        # Solución única
        return f"x = {particular}"

    parts = [f"x = {particular}"]
    for k, (vec, var_idx) in enumerate(zip(vectores_nulos, variables_libres)):
        parts.append(f" + t{k + 1} * {vec}")

    return "".join(parts)


def generar_latex_solucion(n_incognitas, libres, expresiones, particular, vectores_nulos):
    """
    Genera código LaTeX para la solución general vectorial.

    Devuelve un string con código LaTeX que puede copiarse.
    """
    lines = []

    # Solución particular
    lines.append("\\text{Solución particular (variables libres } = 0\\text{):}")
    lines.append("\\\\")
    x_p_components = []
    for val in particular:
        x_p_components.append(f"{val:.6g}".rstrip('0').rstrip('.'))
    lines.append(f"\\mathbf{{x_p}} = \\begin{{pmatrix}} {' \\\\ '.join(x_p_components)} \\end{{pmatrix}}")
    lines.append("\\\\")
    lines.append("\\\\")

    # Vectores del espacio nulo
    if vectores_nulos:
        lines.append("\\text{Vectores del espacio nulo (base):}")
        lines.append("\\\\")
        for k, vec in enumerate(vectores_nulos):
            v_components = []
            for val in vec:
                v_components.append(f"{val:.6g}".rstrip('0').rstrip('.'))
            lines.append(f"\\mathbf{{v_{k + 1}}} = \\begin{{pmatrix}} {' \\\\ '.join(v_components)} \\end{{pmatrix}}")
            if k < len(vectores_nulos) - 1:
                lines.append(", \\quad ")
            lines.append("\\\\")
        lines.append("\\\\")

        # Solución general
        lines.append("\\text{Solución general:}")
        lines.append("\\\\")
        params = " + ".join([f"t_{k + 1} \\mathbf{{v_{k + 1}}}" for k in range(len(vectores_nulos))])
        lines.append(f"\\mathbf{{x}} = \\mathbf{{x_p}} + {params}")

    return "".join(lines)
