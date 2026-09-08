"""Ventana principal: un QStackedWidget que va mostrando cada pantalla."""

import os
import sys

from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from aqua_gauss.clients.qt import mathrender
from aqua_gauss.clients.qt.theme import APP_INFO, aplicar_tema

_ORDEN = (
    "menu",
    "dimensiones",
    "entrada",
    "proceso",
    "resultado",
    "vectores",
    "vectores_entrada",
)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        from aqua_gauss.clients.qt.state import Sesion  # import perezoso: evita ciclos al arrancar

        self.sesion = Sesion()
        self.setWindowTitle(f"{APP_INFO['nombre']} · Sistemas lineales y vectores de Rⁿ")
        self.resize(1040, 760)
        self.setMinimumSize(820, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        from aqua_gauss.clients.qt.screen_dimensions import PantallaDimensiones
        from aqua_gauss.clients.qt.screen_input import PantallaEntrada
        from aqua_gauss.clients.qt.screen_menu import PantallaMenu
        from aqua_gauss.clients.qt.screen_process import PantallaProceso
        from aqua_gauss.clients.qt.screen_result import PantallaResultado
        from aqua_gauss.clients.qt.screen_vectores import PantallaVectores
        from aqua_gauss.clients.qt.screen_vectores_entrada import PantallaVectoresEntrada

        clases = {
            "menu": PantallaMenu,
            "dimensiones": PantallaDimensiones,
            "entrada": PantallaEntrada,
            "proceso": PantallaProceso,
            "resultado": PantallaResultado,
            "vectores": PantallaVectores,
            "vectores_entrada": PantallaVectoresEntrada,
        }
        self.pantallas = {}
        for nombre in _ORDEN:
            pantalla = clases[nombre](self)
            self.pantallas[nombre] = pantalla
            self.stack.addWidget(pantalla)

        QShortcut(QKeySequence("Escape"), self, activated=self._atras_global)
        QShortcut(QKeySequence("F1"), self, activated=lambda: self.ir("menu"))

        self.ir("menu")

    def ir(self, nombre, **kw):
        pantalla = self.pantallas[nombre]
        pantalla.al_entrar(**kw)
        self.stack.setCurrentWidget(pantalla)
        inicial = pantalla.widget_inicial()
        if inicial is not None:
            inicial.setFocus()

    def _atras_global(self):
        self.stack.currentWidget().al_atras()


def main():
    app = QApplication(sys.argv)
    aplicar_tema(app)

    ventana = VentanaPrincipal()
    ventana.show()

    if not mathrender.disponible() and os.environ.get("AQUA_GAUSS_SILENCIAR") != "1":
        QMessageBox.information(
            ventana,
            "Notación matemática como texto",
            "No se encontró <b>matplotlib</b>, así que la notación se mostrará como "
            "texto en vez de renderizada.<br><br>"
            "Para verla bonita, cierra la app y ejecútala dentro del entorno de uv:"
            "<br><code>uv sync --extra qt</code><br><code>uv run aqua-gauss</code>",
        )

    sys.exit(app.exec())
