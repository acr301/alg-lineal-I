"""Modelos del cliente Qt, uno por caso de uso.

- `SistemaModel`   — dimensiones, notación, matriz aumentada y resultado de Ax = b.
- `VectoresModel`  — combinación lineal, pertenencia y los ocho axiomas de R^n.

Ninguno importa `aqua_gauss.core`: el cálculo se pide a un `SolverPort`. Las
pantallas (`screen_*`, las Views) leen y escriben estos modelos y disparan sus
métodos; el `Sesion` de `state.py` sólo los agrupa.
"""

from aqua_gauss.core.formato import (
    MODO_FRACCION,
    entrada_A,
    entrada_b,
    formatear_valor,
    var,
)

EJEMPLOS = {
    "Solución única": [[1, 1, 1, 6], [0, 2, 5, -4], [2, 5, -1, 27]],
    "Infinitas soluciones": [[1, 1, 1, 6], [2, 2, 2, 12], [1, -1, 0, 0]],
    "Sistema inconsistente": [[1, 1, 2], [1, 1, 5]],
}


class SistemaModel:
    """Sistema Ax = b en edición: dimensiones, notación, celdas y resultado."""

    def __init__(self, solver):
        self._solver = solver
        self.n_eq = 3
        self.n_var = 3
        self.modo = MODO_FRACCION
        self.matriz = self._matriz_ceros(3, 3)
        self.resultado = None  # dict tras resolver(), o None
        self.origen = "manual"  # "manual" (flujo completo) | "ejemplo" (salta a proceso)

    # ---- forma --------------------------------------------------------- #

    @staticmethod
    def _matriz_ceros(n_eq, n_var):
        return [[0.0] * (n_var + 1) for _ in range(n_eq)]

    def redimensionar(self, n_eq, n_var):
        """Cambia las dimensiones conservando los valores que quepan."""
        nueva = self._matriz_ceros(n_eq, n_var)
        for i in range(min(n_eq, len(self.matriz))):
            for j in range(min(n_var + 1, len(self.matriz[i]))):
                nueva[i][j] = self.matriz[i][j]
        self.n_eq, self.n_var, self.matriz = n_eq, n_var, nueva
        self.resultado = None

    def cargar_ejemplo(self, nombre):
        datos = EJEMPLOS[nombre]
        self.n_eq = len(datos)
        self.n_var = len(datos[0]) - 1
        self.matriz = [[float(v) for v in fila] for fila in datos]
        self.resultado = None
        self.origen = "ejemplo"

    def iniciar_manual(self):
        self.origen = "manual"
        self.resultado = None

    def fmt(self, valor):
        """Formatea un número según la notación elegida (fracción o decimal)."""
        return formatear_valor(valor, self.modo)

    # ---- celdas de la matriz aumentada ------------------------------- #

    def total_celdas(self):
        return self.n_eq * (self.n_var + 1)

    def etiqueta_celda(self, indice):
        """Nombre y ayuda de la celda 'indice' (por filas): a₁₁, a₁₂, …, b₁, a₂₁…"""
        fila, col = divmod(indice, self.n_var + 1)
        if col == self.n_var:
            return (entrada_b(fila), f"término independiente de la ecuación {fila + 1}")
        return (entrada_A(fila, col), f"coeficiente de {var(col, 'x')} en la ecuación {fila + 1}")

    def set_celda(self, indice, valor):
        fila, col = divmod(indice, self.n_var + 1)
        self.matriz[fila][col] = valor
        self.resultado = None

    def get_celda(self, indice):
        fila, col = divmod(indice, self.n_var + 1)
        return self.matriz[fila][col]

    # ---- resolución -------------------------------------------------- #

    def resolver(self):
        """Pide al solver la eliminación de Gauss y cachea el resultado."""
        self.resultado = self._solver.resolver_sistema(self.matriz, self.n_var, self.modo)
        return self.resultado


class VectoresModel:
    """Operaciones de R^n: combinación lineal, pertenencia y axiomas."""

    OP_COMBINACION = "combinacion"
    OP_PERTENENCIA = "pertenencia"
    OP_PROPIEDADES = "propiedades"

    def __init__(self, solver):
        self._solver = solver
        self.resultado = None  # dict del último cálculo, o None
        # --- estado de edición (flujo guiado tipo "Iniciar") -------------- #
        self.op = self.OP_COMBINACION
        self.n = 3  # dimensión del espacio
        self.p = 2  # nº de vectores
        self.escalar_a = 2.0  # solo para OP_PROPIEDADES
        self.escalar_b = -1.0
        self.tabla = self._tabla_ceros()

    # ---- forma de la tabla ------------------------------------------- #
    #  combinación: fila 0 = pesos c₁…c_p ; filas 1…n = componentes de v₁…v_p
    #  pertenencia: filas 0…n-1 = componentes ; columnas v₁…v_p y luego b
    #  propiedades: filas 0…n-1 = componentes ; columnas u, v, w  (p se ignora)

    def _n_filas(self):
        return self.n + (1 if self.op == self.OP_COMBINACION else 0)

    def _n_cols(self):
        if self.op == self.OP_PROPIEDADES:
            return 3
        return self.p + (1 if self.op == self.OP_PERTENENCIA else 0)

    def _tabla_ceros(self):
        return [[0.0] * self._n_cols() for _ in range(self._n_filas())]

    def nombres_columnas(self):
        if self.op == self.OP_PROPIEDADES:
            return ["u", "v", "w"]
        nombres = [var(j, "v") for j in range(self.p)]
        if self.op == self.OP_PERTENENCIA:
            nombres.append("b")
        return nombres

    def hay_fila_pesos(self):
        return self.op == self.OP_COMBINACION

    def preparar(self):
        """Rehace la tabla con la forma actual, conservando lo que quepa."""
        vieja, nueva = self.tabla, self._tabla_ceros()
        for i in range(min(len(nueva), len(vieja))):
            for j in range(min(len(nueva[i]), len(vieja[i]))):
                nueva[i][j] = vieja[i][j]
        self.tabla = nueva
        self.resultado = None

    def fmt(self, valor):
        return formatear_valor(valor, MODO_FRACCION)

    # ---- entrada guiada (recorrido por filas) ----------------------- #

    def total_celdas(self):
        return self._n_filas() * self._n_cols()

    def _rc(self, indice):
        return divmod(indice, self._n_cols())

    def etiqueta_celda(self, indice):
        fila, col = self._rc(indice)
        if self.hay_fila_pesos() and fila == 0:
            c = var(col, "c")
            return (c, f"peso que multiplica al vector {var(col, 'v')}")
        base = 1 if self.hay_fila_pesos() else 0
        nom = self.nombres_columnas()[col]
        comp = fila - base + 1
        etiqueta = "b" if nom == "b" else f"{nom}"
        return (f"{etiqueta} · componente {comp}", f"el {comp}º número del vector {nom}")

    def set_celda(self, indice, valor):
        fila, col = self._rc(indice)
        self.tabla[fila][col] = valor
        self.resultado = None

    def get_celda(self, indice):
        fila, col = self._rc(indice)
        return self.tabla[fila][col]

    # ---- cálculo --------------------------------------------------- #

    def _leer_vectores(self):
        base = 1 if self.hay_fila_pesos() else 0
        ncols = 3 if self.op == self.OP_PROPIEDADES else self.p
        return [[self.tabla[base + i][j] for i in range(self.n)] for j in range(ncols)]

    def calcular(self):
        if self.op == self.OP_COMBINACION:
            pesos = [self.tabla[0][j] for j in range(self.p)]
            return self.calcular_combinacion(self._leer_vectores(), pesos)
        if self.op == self.OP_PERTENENCIA:
            objetivo = [self.tabla[i][self.p] for i in range(self.n)]
            return self.comprobar_combinacion(objetivo, self._leer_vectores())
        u, v, w = self._leer_vectores()
        return self.comprobar_propiedades(u, v, w, self.escalar_a, self.escalar_b)

    def calcular_combinacion(self, vectores, pesos):
        self.resultado = self._solver.combinacion(vectores, pesos)
        return self.resultado

    def comprobar_combinacion(self, objetivo, vectores):
        self.resultado = self._solver.pertenencia(objetivo, vectores)
        return self.resultado

    def comprobar_propiedades(self, u, v, w, a, b):
        self.resultado = self._solver.propiedades(u, v, w, a, b)
        return self.resultado
