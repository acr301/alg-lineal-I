"""VectoresModel: forma de la tabla y etiquetas del flujo guiado.

No necesita PyQt6 (el modelo y el solver no importan framework).
"""

import unittest

from aqua_gauss.clients.qt.models import VectoresModel
from aqua_gauss.clients.qt.solver import LocalSolver


def _modelo():
    return VectoresModel(LocalSolver())


class TestFormaDeLaTabla(unittest.TestCase):
    def test_combinacion_tiene_fila_de_pesos(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_COMBINACION, 3, 2
        m.preparar()
        self.assertEqual(len(m.tabla), 4)  # pesos + 3 componentes
        self.assertEqual(len(m.tabla[0]), 2)  # 2 vectores
        self.assertTrue(m.hay_fila_pesos())

    def test_pertenencia_agrega_columna_b(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_PERTENENCIA, 3, 2
        m.preparar()
        self.assertEqual((len(m.tabla), len(m.tabla[0])), (3, 3))  # 3 comp x (v1 v2 b)
        self.assertEqual(m.nombres_columnas(), ["v₁", "v₂", "b"])

    def test_propiedades_fija_u_v_w(self):
        m = _modelo()
        m.op, m.n = m.OP_PROPIEDADES, 2
        m.preparar()
        self.assertEqual((len(m.tabla), len(m.tabla[0])), (2, 3))
        self.assertEqual(m.nombres_columnas(), ["u", "v", "w"])

    def test_preparar_conserva_lo_que_cabe(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_COMBINACION, 2, 2
        m.preparar()
        m.tabla = [[9.0, 8.0], [1.0, 2.0], [3.0, 4.0]]
        m.p = 3  # una columna más
        m.preparar()
        self.assertEqual(m.tabla[0][:2], [9.0, 8.0])
        self.assertEqual(m.tabla[0][2], 0.0)


class TestEtiquetasGuiadas(unittest.TestCase):
    def test_pesos_y_componentes_con_subindices(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_COMBINACION, 2, 2
        m.preparar()
        self.assertEqual(m.etiqueta_celda(0)[0], "c₁")
        self.assertEqual(m.etiqueta_celda(1)[0], "c₂")
        self.assertEqual(m.etiqueta_celda(2)[0], "v₁ · componente 1")
        self.assertEqual(m.etiqueta_celda(5)[0], "v₂ · componente 2")

    def test_total_celdas(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_PERTENENCIA, 3, 2
        m.preparar()
        self.assertEqual(m.total_celdas(), 3 * 3)


class TestCalcular(unittest.TestCase):
    def test_combinacion_desde_la_tabla(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_COMBINACION, 2, 2
        m.preparar()
        # pesos [2, -1]; v1 = [1, 2], v2 = [3, -1]
        m.tabla = [[2.0, -1.0], [1.0, 3.0], [2.0, -1.0]]
        datos = m.calcular()
        self.assertEqual(datos["resultado"], [-1, 5])

    def test_pertenencia_desde_la_tabla(self):
        m = _modelo()
        m.op, m.n, m.p = m.OP_PERTENENCIA, 2, 2
        m.preparar()
        # v1 = [1, 0], v2 = [0, 1], b = [3, 4]  -> pertenece con pesos [3, 4]
        m.tabla = [[1.0, 0.0, 3.0], [0.0, 1.0, 4.0]]
        datos = m.calcular()
        self.assertTrue(datos["pertenece"])


if __name__ == "__main__":
    unittest.main()
