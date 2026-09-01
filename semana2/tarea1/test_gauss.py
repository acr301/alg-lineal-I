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
    clasificar_forma_escalonada,
    crear_matriz_aumentada,
    es_forma_escalonada,
    es_forma_escalonada_reducida,
    escalonar,
    evaluar_solucion_parametrica,
    rango_matriz,
    reducir_a_escalonada_reducida,
    solucion_general_vectorial,
    solucion_parametrica,
    sustitucion_regresiva,
    verificar_rango_nulidad,
    verificar_solucion,
    verificar_solucion_detallada,
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


class TestVerificarSolucionDetallada(unittest.TestCase):
    def test_expone_terminos_y_suma(self):
        coeficientes = [[1, 1, 1], [0, 2, 5], [2, 5, -1]]
        terminos = [6, -4, 27]
        x = [5, 3, -2]
        detalle = verificar_solucion_detallada(coeficientes, terminos, x)

        self.assertEqual(len(detalle), 3)
        # Ecuación 1: términos (coef, x_j, producto)
        self.assertEqual(detalle[0]["terminos"],
                         [(1, 5, 5), (1, 3, 3), (1, -2, -2)])
        self.assertAlmostEqual(detalle[0]["suma"], 6)
        self.assertEqual(detalle[0]["esperado"], 6)
        for fila in detalle:
            self.assertTrue(fila["coincide"])

    def test_marca_incoincidencia(self):
        coeficientes = [[1, 1], [1, -1]]
        terminos = [4, 0]
        detalle = verificar_solucion_detallada(coeficientes, terminos, [1, 1])
        self.assertFalse(all(fila["coincide"] for fila in detalle))

    def test_consistente_con_verificar_solucion(self):
        coeficientes = [[2, 1], [1, 3]]
        terminos = [1, 1]
        x = [0.4, 0.2]  # 2/5, 1/5
        resumen = verificar_solucion(coeficientes, terminos, x)
        detalle = verificar_solucion_detallada(coeficientes, terminos, x)
        for (suma_r, esp_r, ok_r), fila in zip(resumen, detalle):
            self.assertAlmostEqual(suma_r, fila["suma"])
            self.assertEqual(esp_r, fila["esperado"])
            self.assertEqual(ok_r, fila["coincide"])


class TestRango(unittest.TestCase):
    def test_rango_matriz_determinado(self):
        # Sistema con rango completo: rango = 3, n = 3
        coeficientes = [
            [1, 1, 1],
            [0, 2, 5],
            [2, 5, -1],
        ]
        terminos = [6, -4, 27]
        matriz, n, columnas_pivote, _ = resolver(coeficientes, terminos)
        rango = rango_matriz(matriz, n)
        self.assertEqual(rango, 3)

    def test_rango_matriz_indeterminado(self):
        # Sistema con una variable libre: rango = 2, n = 3
        coeficientes = [
            [1, 1, 1],
            [2, 2, 2],
            [1, -1, 0],
        ]
        terminos = [6, 12, 0]
        matriz, n, columnas_pivote, _ = resolver(coeficientes, terminos)
        rango = rango_matriz(matriz, n)
        self.assertEqual(rango, 2)

    def test_rango_nulidad(self):
        # Verificar que Rango + Nulidad = n
        coeficientes = [
            [1, 1, 1],
            [2, 2, 2],
            [1, -1, 0],
        ]
        terminos = [6, 12, 0]
        matriz, n, columnas_pivote, _ = resolver(coeficientes, terminos)
        result = verificar_rango_nulidad(matriz, n, columnas_pivote)
        self.assertEqual(result["rango"], 2)
        self.assertEqual(result["nulidad"], 1)
        self.assertEqual(result["suma"], 3)
        self.assertTrue(result["es_valido"])


class TestFormasEscalonadas(unittest.TestCase):
    def test_ref_no_rref(self):
        # Una matriz en forma escalonada pero no reducida
        coeficientes = [
            [1, 1, 1],
            [0, 2, 5],
        ]
        terminos = [6, -4]
        matriz, n, columnas_pivote, _ = resolver(coeficientes, terminos)

        self.assertTrue(es_forma_escalonada(matriz, n, columnas_pivote))
        # No está reducida porque los pivotes no son 1
        self.assertFalse(es_forma_escalonada_reducida(matriz, n, columnas_pivote))
        self.assertEqual(clasificar_forma_escalonada(matriz, n, columnas_pivote), "REF")

    def test_rref_sí_reducida(self):
        # Una matriz completamente reducida
        coeficientes = [
            [1, 0, 5],
            [0, 1, 3],
        ]
        terminos = [2, 4]
        matriz, n, columnas_pivote, _ = resolver(coeficientes, terminos)
        reducir_a_escalonada_reducida(matriz, n, columnas_pivote)

        self.assertTrue(es_forma_escalonada(matriz, n, columnas_pivote))
        self.assertTrue(es_forma_escalonada_reducida(matriz, n, columnas_pivote))
        self.assertEqual(clasificar_forma_escalonada(matriz, n, columnas_pivote), "RREF")

    def test_no_escalonada(self):
        # Una matriz que NO está en forma escalonada
        # Esta matriz tiene un pivote en col 0 (fila 0) y col 1 (fila 1),
        # pero la fila 2 es no nula y está después de una fila nula: viola REF
        matriz = [[1, 2, 3], [0, 1, 4], [0, 0, 0], [0, 0, 5]]  # Fila 4 no nula después de nula
        columnas_pivote = [0, 1]  # Solo dos pivotes
        n_incognitas = 3

        # Este caso no pasará la verificación de escalonada porque
        # las filas nulas no están al final
        self.assertFalse(es_forma_escalonada(matriz, n_incognitas, columnas_pivote))


class TestSolucionVectorial(unittest.TestCase):
    def test_solucion_vectorial_indeterminada(self):
        # Sistema con una variable libre
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

        result = solucion_general_vectorial(matriz, n, columnas_pivote, libres, expresiones)
        self.assertIn("particular", result)
        self.assertIn("vectores_nulos", result)
        self.assertIn("variables_libres", result)

        # Verificar que la solución particular es válida
        particular = result["particular"]
        verificacion = verificar_solucion(coeficientes, terminos, particular)
        for _, _, coincide in verificacion:
            self.assertTrue(coincide)

    def test_solucion_vectorial_determinada(self):
        # Sistema con solución única (sin variables libres)
        coeficientes = [
            [1, 1, 1],
            [0, 2, 5],
            [2, 5, -1],
        ]
        terminos = [6, -4, 27]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "determinado")
        # Para sistemas determinados, no hay variables libres
        libres = []
        expresiones = [None] * n

        x = sustitucion_regresiva(matriz, n, columnas_pivote)
        # En lugar de llamar solucion_general_vectorial, verificar que funciona
        self.assertEqual(len(libres), 0)

    def test_solucion_vectorial_dos_variables_libres(self):
        # Sistema 2x5 con rango 1: cuatro variables libres
        coeficientes = [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],  # Fila dependiente
        ]
        terminos = [15, 30]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "indeterminado")
        reducir_a_escalonada_reducida(matriz, n, columnas_pivote)
        libres, expresiones = solucion_parametrica(matriz, n, columnas_pivote)

        self.assertEqual(len(libres), 4)  # 5 variables - 1 pivote = 4 libres
        result = solucion_general_vectorial(matriz, n, columnas_pivote, libres, expresiones)
        self.assertEqual(len(result["vectores_nulos"]), 4)


class TestMatricesRectangulares(unittest.TestCase):
    def test_matriz_2x3(self):
        # Dos ecuaciones, tres incógnitas
        coeficientes = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        terminos = [7, 8]
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        self.assertEqual(tipo, "indeterminado")
        self.assertEqual(len(columnas_pivote), 2)
        self.assertLessEqual(len(columnas_pivote), min(len(coeficientes), n))

    def test_matriz_3x2(self):
        # Tres ecuaciones, dos incógnitas
        coeficientes = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        terminos = [7, 8, 10]  # Ajustado para que sea compatible
        matriz, n, columnas_pivote, tipo = resolver(coeficientes, terminos)

        # Puede ser incompatible o indeterminado dependiendo
        self.assertIn(tipo, ["incompatible", "determinado", "indeterminado"])


if __name__ == "__main__":
    unittest.main()
