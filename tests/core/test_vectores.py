"""Pruebas de operaciones, propiedades y combinaciones lineales en R^n."""

import unittest

from aqua_gauss.core.vectores import (
    cero,
    combinacion_lineal,
    es_combinacion_lineal,
    escalar,
    iguales,
    opuesto,
    suma,
    verificar_propiedades,
)


class TestOperacionesVectoriales(unittest.TestCase):
    def test_suma_componente_a_componente(self):
        self.assertEqual(suma([1, 2, 3], [4, -2, 1]), [5, 0, 4])

    def test_producto_por_escalar(self):
        self.assertEqual(escalar(-2, [1, -3, 0.5]), [-2, 6, -1])

    def test_cero_y_opuesto(self):
        u = [3, -4, 2]
        self.assertEqual(suma(u, opuesto(u)), cero(3))

    def test_igualdad_tolera_error_decimal(self):
        self.assertTrue(iguales([0.1 + 0.2], [0.3]))

    def test_rechaza_dimensiones_distintas(self):
        with self.assertRaises(ValueError):
            suma([1, 2], [1, 2, 3])


class TestCombinacionesLineales(unittest.TestCase):
    def test_calcula_una_combinacion(self):
        vectores = [[1, 2, 0], [0, -1, 3], [2, 0, 1]]

        resultado = combinacion_lineal(vectores, [2, -1, 3])

        self.assertEqual(resultado, [8, 5, 0])

    def test_rechaza_cantidad_incorrecta_de_pesos(self):
        with self.assertRaises(ValueError):
            combinacion_lineal([[1, 2], [3, 4]], [2])

    def test_encuentra_pesos_de_una_base(self):
        pertenece, pesos = es_combinacion_lineal([3, -2], [[1, 0], [0, 1]])

        self.assertTrue(pertenece)
        self.assertEqual(pesos, [3.0, -2.0])

    def test_encuentra_una_solucion_si_hay_infinitas(self):
        vectores = [[1, 2], [2, 4]]

        pertenece, pesos = es_combinacion_lineal([2, 4], vectores)

        self.assertTrue(pertenece)
        self.assertTrue(iguales(combinacion_lineal(vectores, pesos), [2, 4]))

    def test_detecta_objetivo_fuera_del_generado(self):
        pertenece, pesos = es_combinacion_lineal([1, 0], [[1, 1]])

        self.assertFalse(pertenece)
        self.assertIsNone(pesos)


class TestPropiedadesAlgebraicas(unittest.TestCase):
    def test_verifica_los_ocho_axiomas(self):
        propiedades = verificar_propiedades(
            [1, 2, -1], [3, -2, 4], [0, 5, 2], 2, -4
        )

        self.assertEqual(len(propiedades), 8)
        self.assertTrue(all(datos["cumple"] for datos in propiedades.values()))
        for datos in propiedades.values():
            self.assertIn("lado_izquierdo", datos)
            self.assertIn("lado_derecho", datos)

    def test_rechaza_vectores_de_dimensiones_distintas(self):
        with self.assertRaises(ValueError):
            verificar_propiedades([1, 2], [1, 2], [1, 2, 3], 2, 3)


if __name__ == "__main__":
    unittest.main()
