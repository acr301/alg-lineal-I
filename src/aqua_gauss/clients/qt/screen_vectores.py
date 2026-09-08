"""Vectores y propiedades de Rⁿ — paso 1: configuración.

Mismo patrón que "1 · Dimensiones y notación": se elige la operación y las
dimensiones, y se pasa a la entrada guiada (`screen_vectores_entrada`).
"""

from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
)

from aqua_gauss.clients.qt.models import VectoresModel
from aqua_gauss.clients.qt.widgets import PantallaBase

_OPCIONES = [
    ("Calcular una combinación lineal", VectoresModel.OP_COMBINACION),
    ("¿El vector b es combinación de los demás?", VectoresModel.OP_PERTENENCIA),
    ("Verificar las 8 propiedades de Rⁿ", VectoresModel.OP_PROPIEDADES),
]


def _parsear(texto):
    texto = texto.strip().replace(",", ".")
    if not texto:
        raise ValueError("vacío")
    if "/" in texto:
        arriba, _, abajo = texto.partition("/")
        return float(arriba) / float(abajo)
    return float(texto)


class PantallaVectores(PantallaBase):
    def __init__(self, win):
        super().__init__(win)
        self.encabezado(
            "V · Vectores y propiedades de Rⁿ",
            "Elige qué hacer y con cuántos vectores. Luego se te pide cada "
            "componente, como en la creación de un sistema.",
        )

        ficha = QFrame()
        ficha.setObjectName("card")
        rej = QGridLayout(ficha)
        rej.setContentsMargins(22, 20, 22, 20)
        rej.setHorizontalSpacing(18)
        rej.setVerticalSpacing(14)

        self.operacion = QComboBox()
        for etiqueta, _clave in _OPCIONES:
            self.operacion.addItem(etiqueta)
        self.dimension = QSpinBox()
        self.dimension.setRange(1, 8)
        self.cantidad = QSpinBox()
        self.cantidad.setRange(1, 6)
        self.escalar_a = QLineEdit("2")
        self.escalar_b = QLineEdit("-1")
        for campo in (self.escalar_a, self.escalar_b):
            campo.setFixedWidth(120)

        rej.addWidget(QLabel("Operación"), 0, 0)
        rej.addWidget(self.operacion, 0, 1)
        rej.addWidget(QLabel("Dimensión n (Rⁿ)"), 1, 0)
        rej.addWidget(self.dimension, 1, 1)
        self.lbl_cantidad = QLabel("Cantidad de vectores")
        rej.addWidget(self.lbl_cantidad, 2, 0)
        rej.addWidget(self.cantidad, 2, 1)
        self.lbl_esc_a = QLabel("Escalar a")
        self.lbl_esc_b = QLabel("Escalar b")
        rej.addWidget(self.lbl_esc_a, 3, 0)
        rej.addWidget(self.escalar_a, 3, 1)
        rej.addWidget(self.lbl_esc_b, 4, 0)
        rej.addWidget(self.escalar_b, 4, 1)
        rej.setColumnStretch(2, 1)
        self.raiz.addWidget(ficha)
        self.raiz.addStretch(1)

        nota = QLabel("Enter para continuar · Esc para volver al menú")
        nota.setObjectName("hint")
        self.raiz.addWidget(nota)

        nav = self.navegacion(texto_continuar="Ingresar valores  →")
        nav.continuar.connect(self._continuar)

        self.operacion.currentIndexChanged.connect(self._ajustar_visibilidad)
        self._ajustar_visibilidad()

    # -- ciclo de vida ----------------------------------------------- #

    def al_entrar(self, **kw):
        modelo = self.sesion.vectores
        self.operacion.setCurrentIndex(
            next(i for i, (_, c) in enumerate(_OPCIONES) if c == modelo.op)
        )
        self.dimension.setValue(modelo.n)
        self.cantidad.setValue(modelo.p)
        self.escalar_a.setText(str(modelo.fmt(modelo.escalar_a)))
        self.escalar_b.setText(str(modelo.fmt(modelo.escalar_b)))
        self._ajustar_visibilidad()

    def al_atras(self):
        self.win.ir("menu")

    def widget_inicial(self):
        return self.operacion

    # -- lógica ---------------------------------------------------- #

    def _clave_operacion(self):
        return _OPCIONES[self.operacion.currentIndex()][1]

    def _ajustar_visibilidad(self):
        propiedades = self._clave_operacion() == VectoresModel.OP_PROPIEDADES
        for w in (self.lbl_cantidad, self.cantidad):
            w.setVisible(not propiedades)
        for w in (self.lbl_esc_a, self.escalar_a, self.lbl_esc_b, self.escalar_b):
            w.setVisible(propiedades)

    def _continuar(self):
        modelo = self.sesion.vectores
        modelo.op = self._clave_operacion()
        modelo.n = self.dimension.value()
        modelo.p = self.cantidad.value()
        if modelo.op == VectoresModel.OP_PROPIEDADES:
            try:
                modelo.escalar_a = _parsear(self.escalar_a.text())
                modelo.escalar_b = _parsear(self.escalar_b.text())
            except (ValueError, ZeroDivisionError):
                modelo.escalar_a, modelo.escalar_b = 2.0, -1.0
        modelo.preparar()
        self.win.ir("vectores_entrada")
