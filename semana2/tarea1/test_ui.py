"""
test_ui.py

Pruebas de humo de la GUI (paquete ui/). Se saltan si PyQt6 no está disponible.
Cubren en particular el bug del doble clic en el menú (issue de regresión):
un gesto que repuebla la lista no debe volver a invocar el handler con un item
ya borrado.
"""

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("AQUA_GAUSS_SILENCIAR", "1")

try:
    from PyQt6.QtWidgets import QApplication

    _APP = QApplication.instance() or QApplication([])
    from ui.app import VentanaPrincipal

    _LISTO = True
except Exception:  # pragma: no cover - depende del entorno
    _LISTO = False


@unittest.skipUnless(_LISTO, "PyQt6 no disponible")
class TestMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = VentanaPrincipal()

    @classmethod
    def tearDownClass(cls):
        cls.win.close()

    def setUp(self):
        self.win.ir("menu")

    def test_doble_gesto_en_ejemplo_rapido_no_revienta(self):
        menu = self.win.pantallas["menu"]
        menu._poblar_principal()
        item = next(
            menu.lista.item(i)
            for i in range(menu.lista.count())
            if menu.lista.item(i).text().startswith("Ejemplo")
        )
        # Simula el doble disparo (itemActivated + itemDoubleClicked): el 1er
        # _activar repuebla la lista, el 2º recibiría un item ya borrado.
        menu._activar(item)
        menu._activar(item)          # con el fix: no-op / repoblar, sin crash
        menu._activar(None)          # gesto sobre lista ya cambiada
        self.assertEqual(menu._modo, "ejemplos")

    def test_elegir_ejemplo_salta_a_proceso(self):
        menu = self.win.pantallas["menu"]
        menu._poblar_ejemplos()
        for i in range(menu.lista.count()):
            if menu.lista.item(i).text() == "Variables libres":
                menu._activar(menu.lista.item(i))
                break
        self.assertIs(self.win.stack.currentWidget(), self.win.pantallas["proceso"])
        self.assertEqual(self.win.sesion.origen, "ejemplo")

    def test_iniciar_va_a_dimensiones(self):
        menu = self.win.pantallas["menu"]
        menu._poblar_principal()
        menu._activar(menu.lista.item(0))  # "Iniciar"
        self.assertIs(self.win.stack.currentWidget(), self.win.pantallas["dimensiones"])
        self.assertEqual(self.win.sesion.origen, "manual")

    def test_vectores_abre_su_pantalla(self):
        menu = self.win.pantallas["menu"]
        item = next(
            menu.lista.item(i)
            for i in range(menu.lista.count())
            if menu.lista.item(i).text().startswith("Vectores")
        )

        menu._activar(item)

        self.assertIs(self.win.stack.currentWidget(), self.win.pantallas["vectores"])

    def test_pantalla_calcula_una_combinacion(self):
        self.win.ir("vectores")
        pantalla = self.win.pantallas["vectores"]
        pantalla.dimension.setValue(2)
        pantalla.cantidad.setValue(2)
        pantalla.operacion.setCurrentText("Calcular combinación lineal")
        valores = ((0, 0, "2"), (1, 0, "1"), (2, 0, "2"),
                   (0, 1, "-1"), (1, 1, "3"), (2, 1, "-1"))
        for fila, columna, valor in valores:
            pantalla.tabla.item(fila, columna).setText(valor)

        datos = pantalla._calcular()

        self.assertEqual(datos["resultado"], [-1, 5])

    def test_estado_verifica_propiedades(self):
        datos = self.win.sesion.comprobar_propiedades(
            [1, 2], [3, -1], [0, 4], 2, -3
        )

        self.assertEqual(len(datos["propiedades"]), 8)
        self.assertTrue(all(p["cumple"] for p in datos["propiedades"].values()))


@unittest.skipUnless(_LISTO, "PyQt6 no disponible")
class TestNotacionSubindices(unittest.TestCase):
    """Fija la notación con subíndices Unicode en la matriz y sus etiquetas."""

    def test_etiqueta_celda_usa_doble_subindice(self):
        from ui.state import Sesion

        sesion = Sesion()  # 3x3 por defecto
        self.assertEqual(sesion.etiqueta_celda(0)[0], "a₁₁")
        self.assertEqual(sesion.etiqueta_celda(3)[0], "b₁")
        self.assertEqual(sesion.etiqueta_celda(4)[0], "a₂₁")
        self.assertIn("x₁", sesion.etiqueta_celda(0)[1])

    def test_matrizgrid_encabeza_con_subindices(self):
        from ui.state import Sesion
        from ui.widgets import MatrizGrid

        grid = MatrizGrid()
        grid.poblar(Sesion())
        encabezados = {
            grid._grid.itemAtPosition(0, 2 + j).widget().text() for j in range(3)
        }
        self.assertEqual(encabezados, {"x₁", "x₂", "x₃"})
        self.assertEqual(grid._grid.itemAtPosition(1, 0).widget().text(), "E₁")


if __name__ == "__main__":
    unittest.main()
