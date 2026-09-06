"""Operaciones y propiedades algebraicas de vectores de R^n.

Los vectores se representan mediante listas. Este módulo no usa NumPy, SymPy,
``fractions`` ni librerías externas de álgebra lineal; solo reutiliza los
algoritmos propios de Gauss y Gauss-Jordan del proyecto.
"""

from gauss import (
    clasificar,
    crear_matriz_aumentada,
    escalonar,
    sustitucion_regresiva,
)
from gauss_jordan import (
    evaluar_solucion_parametrica,
    reducir_a_escalonada_reducida,
    solucion_parametrica,
)

EPS = 1e-9


def _validar_vector(vector):
    if not isinstance(vector, (list, tuple)) or not vector:
        raise ValueError("Un vector debe contener al menos una componente.")
    for componente in vector:
        if not isinstance(componente, (int, float)):
            raise ValueError("Todas las componentes deben ser números.")
    return len(vector)


def _validar_misma_dimension(vectores):
    if not isinstance(vectores, (list, tuple)) or not vectores:
        raise ValueError("Debe proporcionarse al menos un vector.")
    dimension = _validar_vector(vectores[0])
    for vector in vectores[1:]:
        if _validar_vector(vector) != dimension:
            raise ValueError("Todos los vectores deben pertenecer al mismo R^n.")
    return dimension


def suma(u, v):
    """Calcula ``u + v`` componente por componente."""
    dimension = _validar_misma_dimension([u, v])
    return [u[i] + v[i] for i in range(dimension)]


def escalar(c, vector):
    """Calcula ``c·vector`` componente por componente."""
    if not isinstance(c, (int, float)):
        raise ValueError("El escalar debe ser un número.")
    dimension = _validar_vector(vector)
    return [c * vector[i] for i in range(dimension)]


def cero(n):
    """Construye el vector cero de R^n."""
    if not isinstance(n, int) or n < 1:
        raise ValueError("La dimensión debe ser un entero positivo.")
    return [0.0] * n


def opuesto(vector):
    """Devuelve el inverso aditivo ``-vector``."""
    return escalar(-1, vector)


def iguales(u, v, eps=EPS):
    """Compara vectores con tolerancia para errores de punto flotante."""
    try:
        dimension = _validar_misma_dimension([u, v])
    except ValueError:
        return False
    for i in range(dimension):
        if abs(u[i] - v[i]) > eps:
            return False
    return True


def combinacion_lineal(vectores, pesos):
    """Calcula ``c₁v₁ + ... + cₚvₚ`` y valida dimensiones y cantidades."""
    dimension = _validar_misma_dimension(vectores)
    if not isinstance(pesos, (list, tuple)) or len(vectores) != len(pesos):
        raise ValueError("Debe existir exactamente un peso por cada vector.")

    resultado = cero(dimension)
    for k in range(len(vectores)):
        if not isinstance(pesos[k], (int, float)):
            raise ValueError("Todos los pesos deben ser números.")
        for i in range(dimension):
            resultado[i] += pesos[k] * vectores[k][i]
    return resultado


def es_combinacion_lineal(objetivo, vectores):
    """Determina si ``objetivo`` pertenece al generado por ``vectores``.

    Las columnas de la matriz de coeficientes son los vectores recibidos. Si
    el sistema es compatible, devuelve ``(True, pesos)``; de lo contrario,
    devuelve ``(False, None)``. Cuando hay infinitas respuestas se elige la
    solución concreta que asigna cero a los parámetros libres.
    """
    dimension = _validar_misma_dimension(vectores)
    if _validar_vector(objetivo) != dimension:
        raise ValueError("El objetivo y los vectores deben pertenecer al mismo R^n.")

    cantidad = len(vectores)
    coeficientes = []
    for i in range(dimension):
        coeficientes.append([vectores[k][i] for k in range(cantidad)])
    matriz = crear_matriz_aumentada(coeficientes, objetivo)
    pivotes = escalonar(matriz, cantidad)
    tipo = clasificar(matriz, cantidad, pivotes)

    if tipo == "incompatible":
        return False, None
    if tipo == "determinado":
        return True, sustitucion_regresiva(matriz, cantidad, pivotes)

    reducir_a_escalonada_reducida(matriz, cantidad, pivotes)
    libres, expresiones = solucion_parametrica(matriz, cantidad, pivotes)
    pesos = evaluar_solucion_parametrica(
        cantidad, libres, expresiones, [0.0] * len(libres)
    )
    return True, pesos


def _igualdad(nombre, lado_izquierdo, lado_derecho):
    return {
        "propiedad": nombre,
        "lado_izquierdo": lado_izquierdo,
        "lado_derecho": lado_derecho,
        "cumple": iguales(lado_izquierdo, lado_derecho),
    }


def verificar_propiedades(u, v, w, a, b):
    """Evalúa los ocho axiomas pedidos para valores concretos de R^n."""
    dimension = _validar_misma_dimension([u, v, w])
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("a y b deben ser escalares numéricos.")
    vector_nulo = cero(dimension)

    return {
        "conmutatividad_suma": _igualdad(
            "Conmutatividad de la suma", suma(u, v), suma(v, u)
        ),
        "asociatividad_suma": _igualdad(
            "Asociatividad de la suma",
            suma(suma(u, v), w),
            suma(u, suma(v, w)),
        ),
        "neutro_aditivo": _igualdad(
            "Elemento neutro aditivo", suma(u, vector_nulo), list(u)
        ),
        "inverso_aditivo": _igualdad(
            "Inverso aditivo", suma(u, opuesto(u)), vector_nulo
        ),
        "identidad_escalar": _igualdad(
            "Identidad escalar", escalar(1, u), list(u)
        ),
        "asociatividad_escalar": _igualdad(
            "Asociatividad del producto por escalares",
            escalar(a, escalar(b, u)),
            escalar(a * b, u),
        ),
        "distributividad_vectores": _igualdad(
            "Distributividad respecto de la suma de vectores",
            escalar(a, suma(u, v)),
            suma(escalar(a, u), escalar(a, v)),
        ),
        "distributividad_escalares": _igualdad(
            "Distributividad respecto de la suma de escalares",
            escalar(a + b, u),
            suma(escalar(a, u), escalar(b, u)),
        ),
    }


__all__ = [
    "EPS",
    "cero",
    "combinacion_lineal",
    "es_combinacion_lineal",
    "escalar",
    "iguales",
    "opuesto",
    "suma",
    "verificar_propiedades",
]
