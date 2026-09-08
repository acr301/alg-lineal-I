"""`Sesion`: agrupa los modelos del cliente y su `SolverPort`.

Ya no contiene lógica — sólo une `SistemaModel` y `VectoresModel` y deja
proxies planos (`sesion.n_var`, `sesion.resolver()`, …) para que las pantallas
y los widgets sigan hablando con un objeto único. El cálculo entra por
`self.solver` (un `LocalSolver` salvo que se inyecte otro, p. ej. en tests o,
más adelante, un `RemoteSolver`).
"""

from aqua_gauss.clients.qt.models import EJEMPLOS, SistemaModel, VectoresModel
from aqua_gauss.clients.qt.solver import LocalSolver

__all__ = ["Sesion", "EJEMPLOS"]


class Sesion:
    def __init__(self, solver=None):
        self.solver = solver or LocalSolver()
        self.sistema = SistemaModel(self.solver)
        self.vectores = VectoresModel(self.solver)

    # ---- proxies al SistemaModel (atributos mutables) ------------------ #

    @property
    def n_eq(self):
        return self.sistema.n_eq

    @n_eq.setter
    def n_eq(self, valor):
        self.sistema.n_eq = valor

    @property
    def n_var(self):
        return self.sistema.n_var

    @n_var.setter
    def n_var(self, valor):
        self.sistema.n_var = valor

    @property
    def modo(self):
        return self.sistema.modo

    @modo.setter
    def modo(self, valor):
        self.sistema.modo = valor

    @property
    def matriz(self):
        return self.sistema.matriz

    @matriz.setter
    def matriz(self, valor):
        self.sistema.matriz = valor

    @property
    def origen(self):
        return self.sistema.origen

    @origen.setter
    def origen(self, valor):
        self.sistema.origen = valor

    @property
    def resultado(self):
        return self.sistema.resultado

    @resultado.setter
    def resultado(self, valor):
        self.sistema.resultado = valor

    @property
    def resultado_vectores(self):
        return self.vectores.resultado

    # ---- proxies al SistemaModel (métodos) --------------------------- #

    def redimensionar(self, n_eq, n_var):
        return self.sistema.redimensionar(n_eq, n_var)

    def cargar_ejemplo(self, nombre):
        return self.sistema.cargar_ejemplo(nombre)

    def iniciar_manual(self):
        return self.sistema.iniciar_manual()

    def fmt(self, valor):
        return self.sistema.fmt(valor)

    def total_celdas(self):
        return self.sistema.total_celdas()

    def etiqueta_celda(self, indice):
        return self.sistema.etiqueta_celda(indice)

    def set_celda(self, indice, valor):
        return self.sistema.set_celda(indice, valor)

    def get_celda(self, indice):
        return self.sistema.get_celda(indice)

    def resolver(self):
        return self.sistema.resolver()

    # ---- proxies al VectoresModel ----------------------------------- #

    def calcular_combinacion(self, vectores, pesos):
        return self.vectores.calcular_combinacion(vectores, pesos)

    def comprobar_combinacion(self, objetivo, vectores):
        return self.vectores.comprobar_combinacion(objetivo, vectores)

    def comprobar_propiedades(self, u, v, w, a, b):
        return self.vectores.comprobar_propiedades(u, v, w, a, b)
