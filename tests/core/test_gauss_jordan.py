"""Pruebas directas del módulo de reducción Gauss-Jordan."""

import unittest

from aqua_gauss.core import gauss
from aqua_gauss.core.gauss_jordan import (
    evaluar_solucion_parametrica,
    reducir_a_escalonada_reducida,
    solucion_general_vectorial,
    solucion_parametrica,
)


class TestReduccionGaussJordan(unittest.TestCase):
    def test_reduce_una_forma_escalonada_a_rref(self):
        matriz = [[2.0, 1.0, 5.0], [0.0, 3.0, 6.0]]

        reducir_a_escalonada_reducida(matriz, 2, [0, 1])

        self.assertEqual(matriz, [[1.0, 0.0, 1.5], [0.0, 1.0, 2.0]])

    def test_registra_los_pasos_con_el_formato_recibido(self):
        matriz = [[2.0, 1.0, 5.0], [0.0, 3.0, 6.0]]
        pasos = []

        reducir_a_escalonada_reducida(
            matriz,
            2,
            [0, 1],
            registrar_paso=lambda descripcion, _matriz: pasos.append(descripcion),
            formato_numero=lambda valor: f"<{valor}>",
        )

        self.assertTrue(any("<3.0>" in paso for paso in pasos))


class TestSolucionesParametricas(unittest.TestCase):
    def setUp(self):
        self.matriz = [[1.0, 0.0, 2.0, 4.0], [0.0, 1.0, -1.0, 1.0]]
        self.pivotes = [0, 1]

    def test_identifica_variables_libres_y_expresiones(self):
        libres, expresiones = solucion_parametrica(self.matriz, 3, self.pivotes)

        self.assertEqual(libres, [2])
        self.assertEqual(expresiones[0], (4.0, [(-2.0, 2)]))
        self.assertEqual(expresiones[1], (1.0, [(1.0, 2)]))
        self.assertIsNone(expresiones[2])

    def test_evalua_una_eleccion_del_parametro(self):
        libres, expresiones = solucion_parametrica(self.matriz, 3, self.pivotes)

        resultado = evaluar_solucion_parametrica(3, libres, expresiones, [3.0])

        self.assertEqual(resultado, [-2.0, 4.0, 3.0])

    def test_construye_solucion_vectorial(self):
        libres, expresiones = solucion_parametrica(self.matriz, 3, self.pivotes)

        resultado = solucion_general_vectorial(self.matriz, 3, self.pivotes, libres, expresiones)

        self.assertEqual(resultado["particular"], [4.0, 1.0, 0.0])
        self.assertEqual(resultado["vectores_nulos"], [[-2.0, 1.0, 1.0]])

    def test_los_nombres_historicos_de_gauss_siguen_funcionando(self):
        libres, expresiones = gauss.solucion_parametrica(self.matriz, 3, self.pivotes)

        self.assertEqual(libres, [2])
        self.assertEqual(
            gauss.evaluar_solucion_parametrica(3, libres, expresiones, [0]),
            [4.0, 1.0, 0],
        )


if __name__ == "__main__":
    unittest.main()
