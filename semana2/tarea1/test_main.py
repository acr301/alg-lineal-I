"""Pruebas de los textos de clasificación mostrados por la interfaz de consola."""

import io
import unittest
from contextlib import redirect_stdout

from main import (
    comprobar_combinacion_vectorial,
    imprimir_propiedades_vectoriales,
    resolver_combinacion_vectorial,
    resolver_sistema,
)


class TestClasificacionVisible(unittest.TestCase):
    def salida_de(self, coeficientes, terminos):
        salida = io.StringIO()
        with redirect_stdout(salida):
            resolver_sistema(coeficientes, terminos, len(coeficientes[0]))
        return salida.getvalue()

    def test_sistema_consistente_determinado(self):
        salida = self.salida_de([[1, 1], [1, -1]], [4, 0])
        self.assertIn("Sistema CONSISTENTE DETERMINADO", salida)
        self.assertNotIn("Sistema COMPATIBLE", salida)

    def test_sistema_consistente_indeterminado(self):
        salida = self.salida_de([[1, 1], [2, 2]], [2, 4])
        self.assertIn("Sistema CONSISTENTE INDETERMINADO", salida)
        self.assertNotIn("Sistema COMPATIBLE", salida)

    def test_sistema_inconsistente(self):
        salida = self.salida_de([[1, 1], [1, 1]], [2, 5])
        self.assertIn("Sistema INCONSISTENTE", salida)
        self.assertNotIn("Sistema INCOMPATIBLE", salida)

    def test_solucion_unica_usa_subindices(self):
        salida = self.salida_de([[1, 1], [1, -1]], [4, 0])
        self.assertIn("x₁ = ", salida)
        self.assertNotIn("x1 = ", salida)

    def test_solucion_parametrica_usa_subindices(self):
        salida = self.salida_de([[1, 1], [2, 2]], [2, 4])
        self.assertIn("t₁", salida)
        self.assertNotIn(" t1", salida)
        self.assertNotIn("*t1", salida)


class TestVectoresEnConsola(unittest.TestCase):
    def test_muestra_combinacion_y_latex(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            resultado = resolver_combinacion_vectorial(
                [[1, 2], [3, -1]], [2, -1]
            )

        self.assertEqual(resultado, [-1, 5])
        self.assertIn("b = 2·v1 − 1·v2 = [−1, 5]ᵀ", salida.getvalue())
        self.assertIn(r"\begin{pmatrix}", salida.getvalue())

    def test_informa_cuando_el_objetivo_no_pertenece(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            pertenece, pesos = comprobar_combinacion_vectorial(
                [1, 0], [[1, 1]]
            )

        self.assertFalse(pertenece)
        self.assertIsNone(pesos)
        self.assertIn("NO es combinación lineal", salida.getvalue())

    def test_muestra_los_ocho_axiomas(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            propiedades = imprimir_propiedades_vectoriales(
                [1, 2], [3, -1], [0, 4], 2, -3
            )

        self.assertEqual(len(propiedades), 8)
        self.assertEqual(salida.getvalue().count("-> OK"), 8)


if __name__ == "__main__":
    unittest.main()
