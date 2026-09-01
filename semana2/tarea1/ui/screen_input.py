"""Segunda pantalla: entrada guiada de la matriz aumentada, término a término."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from ui.widgets import MatrizGrid, PantallaBase


def _parsear(texto):
    """Acepta '3', '3.5', '3,5' y también '1/2'. Devuelve float o lanza ValueError."""
    texto = texto.strip().replace(",", ".")
    if not texto:
        raise ValueError("vacío")
    if "/" in texto:
        arriba, _, abajo = texto.partition("/")
        return float(arriba) / float(abajo)
    return float(texto)


def _num_editable(valor):
    if valor == int(valor):
        return str(int(valor))
    return f"{valor:g}"


class PantallaEntrada(PantallaBase):
    def __init__(self, win):
        super().__init__(win)
        self.encabezado("2 · Matriz aumentada [A | b]",
                        "Se te pide cada término de izquierda a derecha y de arriba "
                        "abajo, como se lee. La matriz se va rellenando abajo.")

        self.prompt = QLabel("—")
        self.prompt.setObjectName("prompt")
        self.prompt.setWordWrap(True)
        self.raiz.addWidget(self.prompt)

        fila_entrada = QHBoxLayout()
        self.anterior = QPushButton("◀  Anterior")
        self.anterior.setObjectName("secondary")
        self.anterior.clicked.connect(lambda: self._ir_a(self.indice - 1))
        self.campo = QLineEdit()
        self.campo.setObjectName("cell")
        self.campo.setPlaceholderText("número  (admite . , y también 1/2)")
        self.campo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.campo.returnPressed.connect(self._confirmar)
        self.siguiente = QPushButton("Siguiente  ▶")
        self.siguiente.setObjectName("secondary")
        self.siguiente.clicked.connect(lambda: self._ir_a(self.indice + 1))
        fila_entrada.addWidget(self.anterior)
        fila_entrada.addWidget(self.campo, 1)
        fila_entrada.addWidget(self.siguiente)
        self.raiz.addLayout(fila_entrada)

        self.error = QLabel("")
        self.error.setStyleSheet("color:#9f2520; font-weight:700;")
        self.raiz.addWidget(self.error)

        self.grid = MatrizGrid()
        self.raiz.addWidget(self.grid, 0)
        self.raiz.addStretch(1)

        pista = QLabel("Enter: guardar y pasar al siguiente · Retroceso en campo vacío: "
                       "término anterior · Esc: volver")
        pista.setObjectName("hint")
        self.raiz.addWidget(pista)

        nav = self.navegacion(texto_continuar="Aceptar matriz  →")
        nav.continuar.connect(lambda: self.win.ir("proceso"))

        self.indice = 0
        self._visitadas = set()

    # -- ciclo de vida -------------------------------------------------- #

    def al_entrar(self, **kw):
        total = self.sesion.total_celdas()
        # Si la matriz viene de un ejemplo (algo distinto de cero), damos todas
        # las celdas por revisadas para permitir continuar de inmediato.
        if any(v != 0 for fila in self.sesion.matriz for v in fila):
            self._visitadas = set(range(total))
        else:
            self._visitadas = set()
        self._ir_a(0)

    def al_atras(self):
        self.win.ir("dimensiones")

    def widget_inicial(self):
        return self.campo

    # -- navegación entre celdas -------------------------------------- #

    def _ir_a(self, indice):
        total = self.sesion.total_celdas()
        self.indice = max(0, min(indice, total - 1))
        self.error.setText("")
        etiqueta, descripcion = self.sesion.etiqueta_celda(self.indice)
        fila = self.indice // (self.sesion.n_var + 1) + 1
        self.prompt.setText(f"Ecuación {fila} · <b>{etiqueta}</b> — {descripcion} "
                            f"&nbsp; ({self.indice + 1}/{total})")
        self.campo.setText(_num_editable(self.sesion.get_celda(self.indice)))
        self.campo.selectAll()
        self.campo.setFocus()
        self.anterior.setEnabled(self.indice > 0)
        self.siguiente.setEnabled(self.indice < total - 1)
        self.grid.poblar(self.sesion, resaltar=self.indice)
        self._actualizar_continuar()

    def _confirmar(self):
        try:
            valor = _parsear(self.campo.text())
        except (ValueError, ZeroDivisionError):
            self.error.setText("Ingresa un número válido (ej. 3, -2.5, 1/2).")
            self.campo.selectAll()
            return
        self.sesion.set_celda(self.indice, valor)
        self._visitadas.add(self.indice)
        total = self.sesion.total_celdas()
        if self.indice < total - 1:
            self._ir_a(self.indice + 1)
        else:
            self.grid.poblar(self.sesion, resaltar=None)
            self.prompt.setText("Matriz aumentada completa. Revísala y pulsa "
                                "<b>Aceptar matriz</b>, o corrige cualquier término.")
            self._actualizar_continuar()
            if self.nav.boton_continuar.isEnabled():
                self.nav.boton_continuar.setFocus()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key.Key_Backspace and not self.campo.text()
                and self.indice > 0):
            self._ir_a(self.indice - 1)
            return
        super().keyPressEvent(event)

    def _actualizar_continuar(self):
        completo = len(self._visitadas) >= self.sesion.total_celdas()
        self.nav.set_continuar_habilitado(completo)
