"""`SolverPort`: la única frontera entre el cliente Qt y el cálculo.

Los modelos (`models.py`) y las pantallas nunca importan `aqua_gauss.core`
directamente: piden todo a un `SolverPort`. Hoy la única implementación es
`LocalSolver`, que corre los algoritmos en el mismo proceso. Cuando exista el
servidor (#32) se añadirá un `RemoteSolver` con la misma interfaz y el cliente
no tendrá que cambiar.
"""

from __future__ import annotations

from typing import Protocol

from aqua_gauss.core.formato import (
    MODO_FRACCION,
    formatear_valor,
    generar_latex_solucion,
    latex_pmatrix,
    parametro,
)
from aqua_gauss.core.gauss import (
    clasificar,
    clasificar_forma_escalonada,
    copiar_matriz,
    crear_matriz_aumentada,
    escalonar,
    evaluar_solucion_parametrica,
    rango_matriz,
    reducir_a_escalonada_reducida,
    solucion_general_vectorial,
    solucion_parametrica,
    sustitucion_regresiva,
    verificar_rango_nulidad,
    verificar_solucion_detallada,
)
from aqua_gauss.core.vectores import (
    combinacion_lineal,
    es_combinacion_lineal,
    verificar_propiedades,
)


class SolverPort(Protocol):
    """Contrato que consume el cliente. Entra y sale sólo datos planos."""

    def resolver_sistema(self, matriz: list[list[float]], n_var: int, modo: str) -> dict: ...

    def combinacion(self, vectores: list[list[float]], pesos: list[float]) -> dict: ...

    def pertenencia(self, objetivo: list[float], vectores: list[list[float]]) -> dict: ...

    def propiedades(self, u, v, w, a, b) -> dict: ...


class LocalSolver:
    """Implementación en proceso: llama a `aqua_gauss.core`."""

    # ---- sistemas Ax = b ------------------------------------------------- #

    def resolver_sistema(self, matriz, n_var, modo=MODO_FRACCION):
        """Corre la eliminación de Gauss sobre una copia de `matriz`.

        `matriz` es la aumentada [A | b] como lista de filas. Devuelve el dict
        `datos` con tipo, rango/nulidad, forma, pasos, solución y comprobación.
        """
        n = n_var
        coeficientes = [fila[:n] for fila in matriz]
        terminos = [fila[n] for fila in matriz]
        aumentada = crear_matriz_aumentada(coeficientes, terminos)

        pasos = [("Matriz aumentada inicial", copiar_matriz(aumentada))]

        def registrar(descripcion, actual):
            pasos.append((descripcion, copiar_matriz(actual)))

        def fmt(valor):
            return formatear_valor(valor, modo)

        pivotes = escalonar(aumentada, n, registrar_paso=registrar, formato_numero=fmt)
        pasos.append(("Forma escalonada final", copiar_matriz(aumentada)))
        tipo = clasificar(aumentada, n, pivotes)

        info_rn = verificar_rango_nulidad(aumentada, n, pivotes)
        basicas = list(pivotes)
        libres = [c for c in range(n) if c not in pivotes]
        datos = {
            "tipo": tipo,
            "rango": rango_matriz(aumentada, n),
            "nulidad": info_rn["nulidad"],
            "suma": info_rn["suma"],
            "n": n,
            "pivotes": basicas,  # índices (base 0) de las columnas pivote
            "basicas": basicas,  # variables básicas = columnas pivote
            "libres_cols": libres,  # variables libres = columnas sin pivote
            "forma": clasificar_forma_escalonada(aumentada, n, pivotes),
            "solucion": None,
            "parametrica": None,  # (libres, expresiones)
            "vectorial": None,  # {particular, vectores_nulos}
            "verificacion": None,  # (encabezado, filas_detalladas)
            "latex": "",
        }

        if tipo == "determinado":
            x = sustitucion_regresiva(aumentada, n, pivotes)
            datos["solucion"] = x
            datos["latex"] = "\\mathbf{x} = " + latex_pmatrix(x, modo)
            datos["verificacion"] = (
                "Comprobación (sustituyendo en el sistema original)",
                verificar_solucion_detallada(coeficientes, terminos, x),
            )
        elif tipo == "indeterminado":
            reducir_a_escalonada_reducida(
                aumentada, n, pivotes, registrar_paso=registrar, formato_numero=fmt
            )
            pasos.append(("Forma escalonada reducida", copiar_matriz(aumentada)))
            libres, expresiones = solucion_parametrica(aumentada, n, pivotes)
            datos["parametrica"] = (libres, expresiones)
            datos["vectorial"] = solucion_general_vectorial(
                aumentada, n, pivotes, libres, expresiones
            )
            datos["latex"] = generar_latex_solucion(
                n,
                libres,
                expresiones,
                datos["vectorial"]["particular"],
                datos["vectorial"]["vectores_nulos"],
                modo,
            )
            x_ej = evaluar_solucion_parametrica(n, libres, expresiones, [0.0] * len(libres))
            etiqueta = (
                ", ".join(f"{parametro(k)} = 0" for k in range(len(libres))) or "sin parámetros"
            )
            datos["verificacion"] = (
                f"Comprobación con {etiqueta}",
                verificar_solucion_detallada(coeficientes, terminos, x_ej),
            )

        datos["pasos"] = pasos
        datos["libres"] = datos["parametrica"][0] if datos["parametrica"] else []
        return datos

    # ---- vectores de R^n ----------------------------------------------- #

    def combinacion(self, vectores, pesos):
        return {
            "tipo": "combinacion",
            "resultado": combinacion_lineal(vectores, pesos),
            "vectores": vectores,
            "pesos": pesos,
        }

    def pertenencia(self, objetivo, vectores):
        pertenece, pesos = es_combinacion_lineal(objetivo, vectores)
        return {
            "tipo": "pertenencia",
            "objetivo": objetivo,
            "vectores": vectores,
            "pertenece": pertenece,
            "pesos": pesos,
        }

    def propiedades(self, u, v, w, a, b):
        return {
            "tipo": "propiedades",
            "propiedades": verificar_propiedades(u, v, w, a, b),
        }
