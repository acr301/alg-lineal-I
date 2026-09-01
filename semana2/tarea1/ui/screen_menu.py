"""Pantalla de menú: información de la app y punto de entrada al flujo."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from ui.state import EJEMPLOS
from ui.theme import APP_INFO
from ui.widgets import PantallaBase

_PRINCIPAL = "principal"
_EJEMPLOS = "ejemplos"


class PantallaMenu(PantallaBase):
    def __init__(self, win):
        super().__init__(win)
        self.encabezado(f"{APP_INFO['nombre']}  ·  v{APP_INFO['version']}",
                        APP_INFO["resumen"])

        ficha = QFrame()
        ficha.setObjectName("card")
        fv = QVBoxLayout(ficha)
        fv.setContentsMargins(18, 14, 18, 14)
        for linea in (
            f"<b>Autores:</b> {APP_INFO['autores']}",
            f"<b>Licencia:</b> {APP_INFO['licencia']}",
            f"<b>Repositorio:</b> {APP_INFO['repo']}",
            "<b>Método:</b> eliminación de Gauss (sin NumPy/SymPy).",
        ):
            et = QLabel(linea)
            et.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            fv.addWidget(et)
        self.raiz.addWidget(ficha)

        self.titulo_lista = QLabel("¿Qué quieres hacer?")
        self.titulo_lista.setObjectName("h1")
        self.raiz.addWidget(self.titulo_lista)

        self.lista = QListWidget()
        self.lista.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lista.itemActivated.connect(self._activar)
        self.raiz.addWidget(self.lista, 1)

        ayuda = QLabel("Teclado: ↑ ↓ para moverte · Enter para elegir · Esc para volver")
        ayuda.setObjectName("hint")
        self.raiz.addWidget(ayuda)

        self._modo = _PRINCIPAL
        self._poblar_principal()

    # -- poblado de la lista ------------------------------------------------ #

    def _poblar_principal(self):
        self._modo = _PRINCIPAL
        self.titulo_lista.setText("¿Qué quieres hacer?")
        self.lista.clear()
        for texto in ("Iniciar  →  crear un sistema nuevo",
                      "Ejemplo rápido  →  cargar un caso de muestra",
                      "Salir"):
            self.lista.addItem(QListWidgetItem(texto))
        self.lista.setCurrentRow(0)

    def _poblar_ejemplos(self):
        self._modo = _EJEMPLOS
        self.titulo_lista.setText("¿Qué tipo de ejemplo?")
        self.lista.clear()
        for nombre in EJEMPLOS:
            self.lista.addItem(QListWidgetItem(nombre))
        self.lista.addItem(QListWidgetItem("←  Volver"))
        self.lista.setCurrentRow(0)

    # -- eventos ---------------------------------------------------------- #

    def _activar(self, item):
        texto = item.text()
        if self._modo == _PRINCIPAL:
            if texto.startswith("Iniciar"):
                self.win.ir("dimensiones")
            elif texto.startswith("Ejemplo"):
                self._poblar_ejemplos()
            else:
                QApplication.instance().quit()
        else:
            if texto.startswith("←"):
                self._poblar_principal()
            else:
                self.sesion.cargar_ejemplo(texto)
                self.win.ir("dimensiones")

    def al_entrar(self, **kw):
        self._poblar_principal()

    def al_atras(self):
        if self._modo == _EJEMPLOS:
            self._poblar_principal()

    def widget_inicial(self):
        return self.lista
