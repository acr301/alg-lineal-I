"""Vectores y propiedades de Rⁿ — paso 2: entrada guiada + resultado.

Mismo patrón que "2 · Matriz aumentada [A | b]": se pide cada valor término a
término, la rejilla de la derecha se va rellenando y al final se calcula y se
muestra el resultado en una tarjeta.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from aqua_gauss.clients.qt import mathrender
from aqua_gauss.clients.qt.models import VectoresModel
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
        arriba, _, abajo = texto.partition("/")
        return float(arriba) / float(abajo)
    return float(texto)


class RejillaValores(QFrame):
    """La tabla de vectores como rejilla con corchetes y encabezados con subíndices."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        cont = QHBoxLayout(self)
        cont.setContentsMargins(10, 12, 10, 12)
        self._grid = QGridLayout()
        self._grid.setHorizontalSpacing(14)
        self._grid.setVerticalSpacing(8)
        cont.addStretch()
        cont.addLayout(self._grid)
        cont.addStretch()

    def poblar(self, modelo, resaltar=None):
        while self._grid.count():
            w = self._grid.takeAt(0).widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        nombres = modelo.nombres_columnas()
        ncols = len(nombres)
        nfilas = modelo._n_filas()
        pesos = modelo.hay_fila_pesos()

        for j, nom in enumerate(nombres):
            enc = QLabel(nom)
            enc.setObjectName("hint")
            enc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._grid.addWidget(enc, 0, 1 + j)

        izq = QLabel()
        izq.setStyleSheet(
            "border:3px solid #153653; border-right:none;"
            " border-top-left-radius:3px; border-bottom-left-radius:3px;"
        )
        izq.setFixedWidth(9)
        der = QLabel()
        der.setStyleSheet(
            "border:3px solid #153653; border-left:none;"
            " border-top-right-radius:3px; border-bottom-right-radius:3px;"
        )
        der.setFixedWidth(9)
        self._grid.addWidget(izq, 1, 0, nfilas, 1)
        self._grid.addWidget(der, 1, 1 + ncols, nfilas, 1)

        for i in range(nfilas):
            if pesos and i == 0:
                et = QLabel("pesos →")
            else:
                et = QLabel(f"fila {i - (1 if pesos else 0) + 1}")
            et.setObjectName("hint")
            self._grid.addWidget(et, i + 1, ncols + 2)
            for j in range(ncols):
                idx = i * ncols + j
                celda = QLabel(modelo.fmt(modelo.tabla[i][j]))
                celda.setAlignment(Qt.AlignmentFlag.AlignCenter)
                celda.setMinimumWidth(46)
                if resaltar is not None and idx == resaltar:
                    celda.setStyleSheet(
                        "background:#fff3cf; border:2px solid #e0a400;"
                        " border-radius:6px; padding:2px 8px; font-weight:800;"
                    )
                else:
                    celda.setStyleSheet("padding:2px 8px;")
                self._grid.addWidget(celda, i + 1, 1 + j)


class PantallaVectoresEntrada(PantallaBase):
    def __init__(self, win):
        super().__init__(win)
        self.encabezado(
            "V · Ingresar los vectores",
            "Cada valor de izquierda a derecha y de arriba abajo. La tabla se va rellenando abajo.",
        )

        self.prompt = QLabel("—")
        self.prompt.setObjectName("prompt")
        self.prompt.setWordWrap(True)
        self.prompt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.raiz.addWidget(self.prompt)

        fila = QHBoxLayout()
        self.anterior = QPushButton("◀")
        self.anterior.setObjectName("secondary")
        self.anterior.setFixedWidth(46)
        self.anterior.clicked.connect(lambda: self._ir_a(self.indice - 1))
        self.campo = QLineEdit()
        self.campo.setObjectName("cell")
        self.campo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.campo.setFixedWidth(180)
        self.campo.returnPressed.connect(self._confirmar)
        self.siguiente = QPushButton("▶")
        self.siguiente.setObjectName("secondary")
        self.siguiente.setFixedWidth(46)
        self.siguiente.clicked.connect(lambda: self._ir_a(self.indice + 1))
        fila.addStretch(1)
        fila.addWidget(self.anterior)
        fila.addWidget(self.campo)
        fila.addWidget(self.siguiente)
        fila.addStretch(1)
        self.raiz.addLayout(fila)

        self.error = QLabel("")
        self.error.setStyleSheet("color:#9f2520; font-weight:700;")
        self.error.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.raiz.addWidget(self.error)

        self.rejilla = RejillaValores()
        self.raiz.addWidget(self.rejilla)

        self.tarjeta = QFrame()
        self.tarjeta.setObjectName("card")
        self.tarjeta_layout = QVBoxLayout(self.tarjeta)
        self.tarjeta_layout.setContentsMargins(16, 14, 16, 14)
        self.tarjeta_layout.setSpacing(6)
        self.tarjeta.setVisible(False)
        self.raiz.addWidget(self.tarjeta, 1)

        self.raiz.addStretch(1)
        pista = QLabel(
            "Enter: guardar y avanzar · Retroceso en campo vacío: valor anterior · Esc: volver"
        )
        pista.setObjectName("hint")
        self.raiz.addWidget(pista)

        nav = self.navegacion(texto_continuar="Calcular  →")
        nav.continuar.connect(self._al_continuar)

        self.indice = 0
        self._visitadas = set()
        self._calculado = False

    # -- ciclo de vida ------------------------------------------------ #

    def al_entrar(self, **kw):
        self._calculado = False
        self.tarjeta.setVisible(False)
        self.nav.set_texto_continuar("Calcular  →")
        total = self.sesion.vectores.total_celdas()
        self._visitadas = set(range(total)) if kw.get("revisitar") else set()
        self._ir_a(0)

    def al_atras(self):
        self.win.ir("vectores")

    def widget_inicial(self):
        return self.campo

    # -- navegación entre celdas ------------------------------------ #

    def _ir_a(self, indice):
        modelo = self.sesion.vectores
        total = modelo.total_celdas()
        self.indice = max(0, min(indice, total - 1))
        self.error.setText("")
        etiqueta, descripcion = modelo.etiqueta_celda(self.indice)
        self.prompt.setText(f"<b>{etiqueta}</b> — {descripcion} &nbsp; ({self.indice + 1}/{total})")
        self.campo.setText(modelo.fmt(modelo.get_celda(self.indice)))
        self.campo.selectAll()
        self.campo.setFocus()
        self.anterior.setEnabled(self.indice > 0)
        self.siguiente.setEnabled(self.indice < total - 1)
        self.rejilla.poblar(modelo, resaltar=self.indice)
        self._actualizar_continuar()

    def _confirmar(self):
        try:
            valor = normalizar_entrada(_parsear(self.campo.text()))
        except (ValueError, ZeroDivisionError):
            self.error.setText("Ingresa un número válido (ej. 3, -2.5, 1/2).")
            self.campo.selectAll()
            return
        modelo = self.sesion.vectores
        modelo.set_celda(self.indice, valor)
        self._visitadas.add(self.indice)
        if self.indice < modelo.total_celdas() - 1:
            self._ir_a(self.indice + 1)
        else:
            self.rejilla.poblar(modelo, resaltar=None)
            self.prompt.setText("Valores completos. Pulsa <b>Calcular</b> o corrige cualquiera.")
            self._actualizar_continuar()
            if self.nav.boton_continuar.isEnabled():
                self.nav.boton_continuar.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Backspace and not self.campo.text() and self.indice > 0:
            self._ir_a(self.indice - 1)
            return
        super().keyPressEvent(event)

    def _actualizar_continuar(self):
        completo = len(self._visitadas) >= self.sesion.vectores.total_celdas()
        self.nav.set_continuar_habilitado(completo or self._calculado)

    # -- calcular y mostrar -------------------------------------- #

    def _al_continuar(self):
        if self._calculado:
            self.win.ir("menu")
            return
        modelo = self.sesion.vectores
        try:
            datos = modelo.calcular()
        except (ValueError, ZeroDivisionError, IndexError):
            self.error.setText("Revisa los datos: usa números válidos.")
            return
        self.error.setText("")
        self._pintar_resultado(modelo, datos)
        self._calculado = True
        self.nav.set_texto_continuar("Menú principal")
        self.nav.set_continuar_habilitado(True)

    def _limpiar_tarjeta(self):
        while self.tarjeta_layout.count():
            w = self.tarjeta_layout.takeAt(0).widget()
            if w:
                w.setParent(None)
                w.deleteLater()

    def _titulo(self, texto):
        t = QLabel(texto)
        t.setObjectName("h1")
        self.tarjeta_layout.addWidget(t)

    def _pintar_resultado(self, modelo, datos):
        self._limpiar_tarjeta()
        self.tarjeta.setVisible(True)
        modo = self.sesion.modo
        op = modelo.op

        if op == VectoresModel.OP_COMBINACION:
            objetivo = datos["resultado"]
            self._titulo("Vector resultante")
            self._agregar_columna(objetivo, modo)
            self.tarjeta_layout.addWidget(
                QLabel(texto_combinacion_lineal(objetivo, datos["vectores"], datos["pesos"], modo))
            )
            self._agregar_latex(
                latex_combinacion_lineal(objetivo, datos["vectores"], datos["pesos"], modo)
            )
        elif op == VectoresModel.OP_PERTENENCIA:
            if datos["pertenece"]:
                pesos = ", ".join(modelo.fmt(p) for p in datos["pesos"])
                self._titulo("Sí es combinación lineal")
                self.tarjeta_layout.addWidget(QLabel(f"Pesos encontrados: [{pesos}]"))
                self._agregar_latex(
                    latex_combinacion_lineal(
                        datos["objetivo"], datos["vectores"], datos["pesos"], modo
                    )
                )
            else:
                self._titulo("No es combinación lineal")
                self.tarjeta_layout.addWidget(QLabel("El sistema [v₁ … v_p | b] es inconsistente."))
        else:  # propiedades
            props = datos["propiedades"]
            ok = sum(1 for p in props.values() if p["cumple"])
            self._titulo(f"{ok} de {len(props)} propiedades se cumplen")
            for p in props.values():
                marca = "✓" if p["cumple"] else "✗"
                fila = QLabel(f"{marca}  {p['propiedad']}")
                fila.setWordWrap(True)
                fila.setStyleSheet("color:%s;" % ("#176b46" if p["cumple"] else "#9f2520"))
                self.tarjeta_layout.addWidget(fila)

    def _agregar_columna(self, componentes, modo):
        pix = mathrender.columna_a_pixmap(componentes, modo, fontsize=17)
        if pix is not None:
            lbl = QLabel()
            lbl.setPixmap(pix)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tarjeta_layout.addWidget(lbl)
        else:
            html = QLabel(vector_columna_html(componentes, modo))
            self.tarjeta_layout.addWidget(html)

    def _agregar_latex(self, codigo):
        toggle = QPushButton("▸  Ver sintaxis LaTeX")
        toggle.setObjectName("ghost")
        caja = QLabel(codigo)
        caja.setWordWrap(True)
        caja.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        caja.setStyleSheet(
            "background:#f2fbff; border:1px solid #86cde3; border-radius:8px; padding:8px;"
        )
        caja.setVisible(False)

        def alternar():
            caja.setVisible(not caja.isVisible())
            toggle.setText(("▾  Ocultar" if caja.isVisible() else "▸  Ver sintaxis") + " LaTeX")

        toggle.clicked.connect(alternar)
        self.tarjeta_layout.addWidget(toggle)
        self.tarjeta_layout.addWidget(caja)
