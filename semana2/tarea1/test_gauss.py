"""
test_gauss.py

Pruebas para la lógica pura de gauss.py (no prueban la interfaz interactiva
de main.py). Se usan asserts simples y unittest (infraestructura de
pruebas, no forma parte del "procedimiento de resolución" que el ejercicio
pide implementar de forma elemental).

Ejecutar con:
    python3 test_gauss.py
"""

import unittest

from gauss import (
    clasificar,
    crear_matriz_aumentada,
    escalonar,
    evaluar_solucion_parametrica,
    reducir_a_escalonada_reducida,
    solucion_parametrica,
    sustitucion_regresiva,
    verificar_solucion,
)


def resolver(coeficientes, terminos):
    """Helper: corre escalonar + clasificar sobre un sistema dado."""
    n = len(coeficientes[0])
    matriz = crear_matriz_aumentada(coeficientes, terminos)
    columnas_pivote = escalonar(matriz, n)
    tipo = clasificar(matriz, n, columnas_pivote)
    return matriz, n, columnas_pivote, tipo


class TestSistemaDeterminado(unittest.TestCase):
    def test_solucion_unica_3x3(self):
        # x + y + z = 6 ; 2y + 5z = -4 ; 2x + 5y - z = 27
        # Solución conocida: x=5, y=3, z=-2
        coeficientes = [
            [1, 1, 1],
            [0, 2, 5],
            [2, 5, -1],
        ]
        terminos = [6, -4, 27]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "determinado")
        x = sustitucion_regresiva(matriz, n, columnas_pivote)
        self.assertAlmostEqual(x[0], 5)
        self.assertAlmostEqual(x[1], 3)
        self.assertAlmostEqual(x[2], -2)

    def test_requiere_pivoteo_por_cero_inicial(self):
        # La primera ecuación tiene coeficiente 0 en x, obliga a intercambiar filas.
        # 0x + 2y = 4 ; 3x + 1y = 5  -> y=2, x=1
        coeficientes = [
            [0, 2],
            [3, 1],
        ]
        terminos = [4, 5]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "determinado")
        x = sustitucion_regresiva(matriz, n, columnas_pivote)
        self.assertAlmostEqual(x[0], 1)
        self.assertAlmostEqual(x[1], 2)


class TestSistemaIndeterminado(unittest.TestCase):
    def test_infinitas_soluciones(self):
        # x + y + z = 6 ; 2x + 2y + 2z = 12 (fila dependiente) ; x - y = 0
        coeficientes = [
            [1, 1, 1],
            [2, 2, 2],
            [1, -1, 0],
        ]
        terminos = [6, 12, 0]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "indeterminado")
        reducir_a_escalonada_reducida(matriz, n, columnas_pivote)
        libres, expresiones = solucion_parametrica(matriz, n, columnas_pivote)

        # z (índice 2) debe ser la variable libre
        self.assertEqual(libres, [2])
        # Verificar que, para un valor arbitrario del parámetro t = z, la
        # solución generada satisface las ecuaciones originales.
        for t in (0, 1, -3.5):
            x = evaluar_solucion_parametrica(n, libres, expresiones, [t])
            resultados = verificar_solucion(coeficientes, terminos, x)
            for _, _, coincide in resultados:
                self.assertTrue(coincide)


class TestSistemaIncompatible(unittest.TestCase):
    def test_sin_solucion(self):
        # x + y = 2 ; x + y = 5  (contradiccion)
        coeficientes = [
            [1, 1],
            [1, 1],
        ]
        terminos = [2, 5]
        _, _, _, tipo = resolver(coeficientes, terminos)
        self.assertEqual(tipo, "incompatible")

    def test_sin_solucion_3x3(self):
        coeficientes = [
            [1, -1, 1],
            [2, -2, 2],
            [1, 1, 1],
        ]
        terminos = [3, 5, 4]  # 2*fila1 debe dar 6, no 5 -> incompatible
        _, _, _, tipo = resolver(coeficientes, terminos)
        self.assertEqual(tipo, "incompatible")


class TestVerificarSolucion(unittest.TestCase):
    def test_solucion_correcta(self):
        coeficientes = [[1, 1, 1], [0, 2, 5], [2, 5, -1]]
        terminos = [6, -4, 27]
        x = [5, 3, -2]
        resultados = verificar_solucion(coeficientes, terminos, x)
        self.assertEqual(len(resultados), 3)
        for valor_calculado, valor_esperado, coincide in resultados:
            self.assertTrue(coincide)
            self.assertAlmostEqual(valor_calculado, valor_esperado)

    def test_solucion_incorrecta_no_coincide(self):
        coeficientes = [[1, 1], [1, -1]]
        terminos = [4, 0]
        x = [1, 1]  # solución real es x=2, y=2
        resultados = verificar_solucion(coeficientes, terminos, x)
        coincidencias = [coincide for _, _, coincide in resultados]
        self.assertFalse(all(coincidencias))


if __name__ == "__main__":
    unittest.main()
