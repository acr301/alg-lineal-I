"""Reducción Gauss-Jordan y soluciones paramétricas a partir de RREF.

Este módulo contiene lógica pura del proyecto. No realiza entrada/salida ni
usa librerías de álgebra lineal: trabaja únicamente con listas, ciclos y
aritmética básica.
"""

from gauss import _formato_por_defecto, valor_casi_cero


def reducir_a_escalonada_reducida(
    matriz,
    n_incognitas,
    columnas_pivote,
    registrar_paso=None,
    formato_numero=None,
):
    """Continúa desde una matriz REF hasta su forma reducida RREF."""
    fmt = formato_numero or _formato_por_defecto
    for i in range(len(columnas_pivote) - 1, -1, -1):
        col = columnas_pivote[i]
        pivote = matriz[i][col]
        if not valor_casi_cero(pivote - 1.0):
            for c in range(col, n_incognitas + 1):
                matriz[i][c] /= pivote
            if registrar_paso:
                registrar_paso(f"F{i + 1} <- F{i + 1} / {fmt(pivote)}", matriz)

        for r in range(i):
            factor = matriz[r][col]
            if valor_casi_cero(factor):
                continue
            for c in range(col, n_incognitas + 1):
                matriz[r][c] -= factor * matriz[i][c]
            matriz[r][col] = 0.0
            if registrar_paso:
                registrar_paso(
                    f"F{r + 1} <- F{r + 1} - ({fmt(factor)}) * F{i + 1}",
                    matriz,
                )


def solucion_parametrica(matriz, n_incognitas, columnas_pivote):
    """Construye variables libres y expresiones desde una matriz RREF."""
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


def evaluar_solucion_parametrica(
    n_incognitas, libres, expresiones, valores_libres
):
    """Evalúa una solución paramétrica para valores concretos."""
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


def solucion_general_vectorial(
    matriz, n_incognitas, columnas_pivote, libres, expresiones
):
    """Construye una solución particular y una base del espacio nulo."""
    particular = evaluar_solucion_parametrica(
        n_incognitas, libres, expresiones, [0] * len(libres)
    )

    vectores_nulos = []
    for k, indice_libre in enumerate(libres):
        valores_libres = [0.0] * len(libres)
        valores_libres[k] = 1.0
        x_temporal = evaluar_solucion_parametrica(
            n_incognitas, libres, expresiones, valores_libres
        )
        vector = [0.0] * n_incognitas
        vector[indice_libre] = 1.0
        for i in range(n_incognitas):
            vector[i] = x_temporal[i] - particular[i]
        vectores_nulos.append(vector)

    return {
        "particular": particular,
        "vectores_nulos": vectores_nulos,
        "variables_libres": libres,
        "expresion_str": _construir_expresion_string(
            particular, vectores_nulos, libres
        ),
    }


def _construir_expresion_string(particular, vectores_nulos, variables_libres):
    """Construye la descripción textual conservada por compatibilidad."""
    if not variables_libres:
        return f"x = {particular}"

    partes = [f"x = {particular}"]
    for k, vector in enumerate(vectores_nulos):
        partes.append(f" + t{k + 1} * {vector}")
    return "".join(partes)


__all__ = [
    "evaluar_solucion_parametrica",
    "reducir_a_escalonada_reducida",
    "solucion_general_vectorial",
    "solucion_parametrica",
]
