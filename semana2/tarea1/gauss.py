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
