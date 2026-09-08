"""Pantalla de combinaciones lineales y propiedades algebraicas de R^n."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QWidget,
)

from aqua_gauss.clients.qt.widgets import PantallaBase
from aqua_gauss.core.formato import (
    latex_combinacion_lineal,
    normalizar_entrada,
    texto_combinacion_lineal,
    vector_columna_html,
)


def _parsear(texto):
    texto = texto.strip().replace(",", ".")
    if not texto:
        raise ValueError("vacío")
    if "/" in texto:
        numerador, _, denominador = texto.partition("/")
        return normalizar_entrada(float(numerador) / float(denominador))
    return normalizar_entrada(float(texto))


class PantallaVectores(PantallaBase):
    """Integra los tres usos vectoriales del issue en una sola pantalla."""

    OPERACIONES = (
        "Calcular combinación lineal",
        "¿Es combinación lineal?",
        "Verificar propiedades de Rⁿ",
    )

    def __init__(self, win):
        super().__init__(win)
        self.encabezado(
            "Vectores y propiedades de Rⁿ",
            "Trabaja con vectores columna usando los algoritmos propios del proyecto.",
        )

        configuracion = QFrame()
        configuracion.setObjectName("card")
        rejilla = QGridLayout(configuracion)
        self.operacion = QComboBox()
        self.operacion.addItems(self.OPERACIONES)
        self.dimension = QSpinBox()
        self.dimension.setRange(1, 8)
        self.dimension.setValue(3)
        self.cantidad = QSpinBox()
        self.cantidad.setRange(1, 6)
        self.cantidad.setValue(2)
        rejilla.addWidget(QLabel("Operación"), 0, 0)
        rejilla.addWidget(self.operacion, 0, 1)
        rejilla.addWidget(QLabel("Dimensión n"), 1, 0)
        rejilla.addWidget(self.dimension, 1, 1)
        rejilla.addWidget(QLabel("Cantidad p de vectores"), 2, 0)
        rejilla.addWidget(self.cantidad, 2, 1)
        self.raiz.addWidget(configuracion)

        self.tabla = QTableWidget()
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setMinimumHeight(180)
        self.tabla.setMaximumHeight(245)
        self.raiz.addWidget(self.tabla)

        self.caja_escalares = QWidget()
        fila_escalares = QHBoxLayout(self.caja_escalares)
        fila_escalares.setContentsMargins(0, 0, 0, 0)
        fila_escalares.addStretch()
        fila_escalares.addWidget(QLabel("Escalar a:"))
        self.escalar_a = QLineEdit("2")
        self.escalar_a.setFixedWidth(100)
        fila_escalares.addWidget(self.escalar_a)
        fila_escalares.addWidget(QLabel("Escalar b:"))
        self.escalar_b = QLineEdit("-1")
        self.escalar_b.setFixedWidth(100)
        fila_escalares.addWidget(self.escalar_b)
        fila_escalares.addStretch()
        self.raiz.addWidget(self.caja_escalares)

        fila_accion = QHBoxLayout()
        self.error = QLabel("")
        self.error.setStyleSheet("color:#9f2520; font-weight:700;")
        self.calcular = QPushButton("Calcular")
        self.calcular.clicked.connect(self._calcular)
        fila_accion.addWidget(self.error, 1)
        fila_accion.addWidget(self.calcular)
        self.raiz.addLayout(fila_accion)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setPlaceholderText("Aquí aparecerá el resultado y su explicación.")
        self.raiz.addWidget(self.resultado, 1)

        self.latex = QTextEdit()
        self.latex.setReadOnly(True)
        self.latex.setMaximumHeight(85)
        self.latex.setPlaceholderText("LaTeX de la combinación lineal")
        self.raiz.addWidget(self.latex)

        nota = QLabel("Puedes ingresar enteros, decimales o fracciones como 1/2 · Esc: menú")
        nota.setObjectName("hint")
        self.raiz.addWidget(nota)
        nav = self.navegacion(texto_continuar="Menú principal")
        nav.continuar.connect(lambda: self.win.ir("menu"))

        self.operacion.currentIndexChanged.connect(self._reconstruir)
        self.dimension.valueChanged.connect(self._reconstruir)
        self.cantidad.valueChanged.connect(self._reconstruir)
        self._reconstruir()

    def al_entrar(self, **kw):
        self.error.setText("")
        self._reconstruir()

    def al_atras(self):
        self.win.ir("menu")

    def widget_inicial(self):
        return self.operacion

    def _reconstruir(self):
        if not hasattr(self, "tabla"):
            return
        n = self.dimension.value()
        operacion = self.operacion.currentText()
        propiedades = operacion == self.OPERACIONES[2]
        pertenencia = operacion == self.OPERACIONES[1]
        cantidad = 3 if propiedades else self.cantidad.value()
        self.cantidad.setEnabled(not propiedades)
        self.caja_escalares.setVisible(propiedades)
        self.latex.setVisible(not propiedades)

        columnas = cantidad + (1 if pertenencia else 0)
        self.tabla.setRowCount(n + (1 if operacion == self.OPERACIONES[0] else 0))
        self.tabla.setColumnCount(columnas)
        if propiedades:
            encabezados = ["u", "v", "w"]
        else:
            encabezados = [f"v{i + 1}" for i in range(cantidad)]
        if pertenencia:
            encabezados.append("objetivo b")
        self.tabla.setHorizontalHeaderLabels(encabezados)
        filas = [f"Componente {i + 1}" for i in range(n)]
        if operacion == self.OPERACIONES[0]:
            filas = ["Peso"] + filas
        self.tabla.setVerticalHeaderLabels(filas)
        for fila in range(self.tabla.rowCount()):
            for columna in range(columnas):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla.setItem(fila, columna, item)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.resultado.clear()
        self.latex.clear()
        self.error.setText("")

    def _valor(self, fila, columna):
        item = self.tabla.item(fila, columna)
        return _parsear(item.text() if item else "")

    def _leer_vector(self, columna, fila_inicial=0):
        return [self._valor(fila_inicial + i, columna) for i in range(self.dimension.value())]

    def _calcular(self):
        try:
            operacion = self.operacion.currentText()
            if operacion == self.OPERACIONES[0]:
                datos = self._calcular_combinacion()
            elif operacion == self.OPERACIONES[1]:
                datos = self._comprobar_pertenencia()
            else:
                datos = self._comprobar_propiedades()
        except (ValueError, ZeroDivisionError):
            self.error.setText("Revisa los datos: usa números válidos y dimensiones compatibles.")
            return
        self.error.setText("")
        return datos

    def _calcular_combinacion(self):
        p = self.cantidad.value()
        pesos = [self._valor(0, i) for i in range(p)]
        vectores = [self._leer_vector(i, 1) for i in range(p)]
        datos = self.sesion.calcular_combinacion(vectores, pesos)
        objetivo = datos["resultado"]
        self.resultado.setHtml(
            "<b>Vector resultante:</b><br>"
            + vector_columna_html(objetivo, self.sesion.modo)
            + "<p>"
            + texto_combinacion_lineal(objetivo, vectores, pesos, self.sesion.modo)
            + "</p>"
        )
        self.latex.setPlainText(
            latex_combinacion_lineal(objetivo, vectores, pesos, self.sesion.modo)
        )
        return datos

    def _comprobar_pertenencia(self):
        p = self.cantidad.value()
        vectores = [self._leer_vector(i) for i in range(p)]
        objetivo = self._leer_vector(p)
        datos = self.sesion.comprobar_combinacion(objetivo, vectores)
        if datos["pertenece"]:
            pesos = ", ".join(self.sesion.fmt(peso) for peso in datos["pesos"])
            mensaje = f"<b>Sí pertenece.</b><p>Pesos encontrados: [{pesos}]</p>"
            self.latex.setPlainText(
                latex_combinacion_lineal(objetivo, vectores, datos["pesos"], self.sesion.modo)
            )
        else:
            mensaje = "<b>No pertenece.</b><p>El sistema asociado es inconsistente.</p>"
            self.latex.clear()
        self.resultado.setHtml(
            mensaje + "<p>Vector objetivo:</p>" + vector_columna_html(objetivo, self.sesion.modo)
        )
        return datos

    def _comprobar_propiedades(self):
        vectores = [self._leer_vector(i) for i in range(3)]
        a = _parsear(self.escalar_a.text())
        b = _parsear(self.escalar_b.text())
        datos = self.sesion.comprobar_propiedades(*vectores, a, b)
        lineas = []
        for propiedad in datos["propiedades"].values():
            marca = "✓" if propiedad["cumple"] else "✗"
            lineas.append(f"<li>{marca} {propiedad['propiedad']}</li>")
        self.resultado.setHtml(
            f"<b>{len(lineas)} propiedades verificadas:</b><ul>{''.join(lineas)}</ul>"
        )
        self.latex.clear()
        return datos
