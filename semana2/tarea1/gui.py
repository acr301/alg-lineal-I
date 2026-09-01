"""Interfaz gráfica para resolver sistemas por eliminación de Gauss.

Uso:
    python3 -m pip install -r requirements.txt
    python3 gui.py

La interfaz solo coordina la entrada y la presentación. El cálculo se delega
íntegramente en ``gauss.py`` para conservar la implementación elemental del
ejercicio y la versión de consola (``main.py``).
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QColor, QPalette, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gauss import (
    clasificar,
    clasificar_forma_escalonada,
    copiar_matriz,
    crear_matriz_aumentada,
    escalonar,
    evaluar_solucion_parametrica,
    rango_matriz,
    reducir_a_escalonada_reducida,
    solucion_general_vectorial,
    solucion_parametrica,
    sustitucion_regresiva,
    valor_casi_cero,
    verificar_rango_nulidad,
    verificar_solucion_detallada,
)
from formato import (
    MENOS,
    MODO_DECIMAL,
    MODO_FRACCION,
    POR,
    formatear_valor,
    generar_latex_solucion,
    latex_pmatrix as _pmatrix_latex,
    latex_valor,
    subindice as _sub,
    var,
    vector_columna_html,
)
import mathrender


STYLESHEET = """
QMainWindow { background: #dff7ff; }
QWidget { color: #153653; font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif; font-size: 14px; }
QLabel#help { background: #0874a4; color: white; border-radius: 8px; font-weight: 800; font-size: 11px; padding: 0 5px; }
QLabel#explain { color: #5a7d92; font-size: 12px; }
QFrame#hero { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f8bd5, stop:.56 #39b9e9, stop:1 #b9f6ef); border-bottom: 2px solid #ffffff; }
QLabel#title { color: white; font-size: 28px; font-weight: 800; }
QLabel#subtitle { color: #eafcff; font-size: 14px; }
QGroupBox { background: rgba(255,255,255,0.86); border: 1px solid #a7dce9; border-radius: 16px; margin-top: 13px; padding: 14px 12px 12px; font-weight: 700; color: #0874a4; }
QGroupBox::title { subcontrol-origin: margin; left: 13px; padding: 0 5px; }
QSpinBox, QComboBox { background: white; border: 1px solid #86cde3; border-radius: 9px; padding: 7px; min-height: 20px; }
QSpinBox:focus, QTableWidget::item:selected { border: 2px solid #087fca; }
QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4bc9ef,stop:1 #0685cc); color: white; border: 1px solid #0572b2; border-radius: 10px; padding: 9px 14px; font-weight: 700; }
QPushButton:hover { background: #0695dc; }
QPushButton:pressed { background: #056da8; }
QPushButton#secondary { background: white; color: #0874a4; border: 1px solid #86cde3; }
QPushButton#secondary:hover { background: #eafaff; }
QTableWidget { background: rgba(255,255,255,0.9); alternate-background-color: #edfaff; border: 1px solid #9bd4e6; border-radius: 10px; gridline-color: #c5e9f1; selection-background-color: #9de6f2; }
QHeaderView::section { background: #d7f5fa; color: #096f99; border: 0; border-bottom: 1px solid #9bd4e6; padding: 7px; font-weight: 800; }
QLabel#hint { color: #41738c; }
QLabel#status { padding: 8px 11px; border-radius: 9px; font-weight: 800; }
QLabel#step { color: #0874a4; font-weight: 700; }
QScrollArea { border: none; background: transparent; }
QSlider::groove:horizontal { height: 7px; background: #b7e7f1; border-radius: 3px; }
QSlider::handle:horizontal { width: 19px; margin: -6px 0; border-radius: 9px; background: #0788cf; border: 2px solid white; }
"""


# Modo de presentación numérica activo (fracción exacta o decimal). Lo ajusta
# GaussWindow según el selector "Fracción ⇄ Decimal"; format_number lo consulta.
MODO_ACTIVO = MODO_FRACCION


def set_modo(modo):
    global MODO_ACTIVO
    MODO_ACTIVO = modo


def format_number(value):
    """Presenta el valor en fracción exacta o decimal, según el modo activo."""
    return formatear_valor(value, MODO_ACTIVO)


def format_display(value):
    """Como format_number pero con el signo menos tipográfico (para rich text)."""
    return format_number(value).replace("-", MENOS)


class GaussWindow(QMainWindow):
    """Ventana principal, adaptable a distintos tamaños de pantalla."""

    def __init__(self):
        super().__init__()
        self.steps = []
        self.current_solution = None
        self.setWindowTitle("Aqua Gauss · Eliminación de matrices")
        # También se aplica a la ventana: algunos backends de Qt no heredan
        # la hoja de estilo de QApplication al renderizar fuera de pantalla.
        self.setStyleSheet(STYLESHEET)
        self.setMinimumSize(840, 620)
        self.resize(1180, 760)
        self._build_ui()
        self.rebuild_input_table()
        self.load_example("Solución única")

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        hero = QFrame(objectName="hero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(28, 21, 28, 20)
        title = QLabel("Aqua Gauss")
        title.setObjectName("title")
        hero_layout.addWidget(title)
        subtitle = QLabel("Explora la eliminación por filas, un paso claro a la vez.")
        subtitle.setObjectName("subtitle")
        hero_layout.addWidget(subtitle)
        layout.addWidget(hero)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        page = QVBoxLayout(content)
        page.setContentsMargins(22, 20, 22, 24)
        page.setSpacing(16)

        controls = QGroupBox("1 · Diseña tu sistema")
        control_layout = QHBoxLayout(controls)
        control_layout.setSpacing(12)
        self.equations = QSpinBox()
        self.equations.setRange(1, 12)
        self.equations.setValue(3)
        self.variables = QSpinBox()
        self.variables.setRange(1, 12)
        self.variables.setValue(3)
        for label, spinner in (("Ecuaciones", self.equations), ("Incógnitas", self.variables)):
            column = QVBoxLayout()
            column.addWidget(QLabel(label))
            column.addWidget(spinner)
            control_layout.addLayout(column)
        self.example = QComboBox()
        self.example.addItems(["Solución única", "Variables libres", "Sistema inconsistente"])
        self.example.currentTextChanged.connect(self.load_example)
        example_column = QVBoxLayout()
        example_column.addWidget(QLabel("Ejemplo rápido"))
        example_column.addWidget(self.example)
        control_layout.addLayout(example_column)

        self.notation = QComboBox()
        self.notation.addItems(["Fracción", "Decimal"])
        self.notation.setToolTip("Fracción: recíprocos exactos como 1/2, 1/4, -8/3.\n"
                                 "Decimal: aproximación con 4 cifras.")
        self.notation.currentIndexChanged.connect(self.on_notation_changed)
        notation_column = QVBoxLayout()
        notation_column.addWidget(QLabel("Notación"))
        notation_column.addWidget(self.notation)
        control_layout.addLayout(notation_column)
        control_layout.addStretch()
        self.refresh_button = QPushButton("Actualizar matriz")
        self.refresh_button.setObjectName("secondary")
        self.refresh_button.clicked.connect(self.rebuild_input_table)
        control_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignBottom)
        page.addWidget(controls)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        entry_group = QGroupBox("2 · Matriz aumentada [A | b]")
        entry_layout = QVBoxLayout(entry_group)
        help_text = QLabel("Usa punto o coma para decimales. La última columna es el término independiente b.")
        help_text.setObjectName("hint")
        help_text.setWordWrap(True)
        entry_layout.addWidget(help_text)
        self.input_table = QTableWidget()
        self._configure_table(self.input_table)
        entry_layout.addWidget(self.input_table)
        action_row = QHBoxLayout()
        clear = QPushButton("Limpiar")
        clear.setObjectName("secondary")
        clear.clicked.connect(self.clear_table)
        solve = QPushButton("Resolver sistema  →")
        solve.clicked.connect(self.solve)
        action_row.addWidget(clear)
        action_row.addStretch()
        action_row.addWidget(solve)
        entry_layout.addLayout(action_row)
        splitter.addWidget(entry_group)

        process_group = QGroupBox("3 · Proceso y resultado")
        process_layout = QVBoxLayout(process_group)
        self.status = QLabel("Ingresa una matriz y presiona Resolver sistema.")
        self.status.setObjectName("status")
        self.set_status("listo", "#dff7e7", "#176b46")
        self.status.setWordWrap(True)
        process_layout.addWidget(self.status)
        self.step_description = QLabel("Aún no hay pasos para mostrar.")
        self.step_description.setObjectName("step")
        self.step_description.setWordWrap(True)
        process_layout.addWidget(self.step_description)
        self.step_table = QTableWidget()
        self._configure_table(self.step_table, editable=False)
        process_layout.addWidget(self.step_table)
        nav = QHBoxLayout()
        self.previous_button = QPushButton("← Anterior")
        self.previous_button.setObjectName("secondary")
        self.previous_button.clicked.connect(lambda: self.step_slider.setValue(self.step_slider.value() - 1))
        self.next_button = QPushButton("Siguiente →")
        self.next_button.setObjectName("secondary")
        self.next_button.clicked.connect(lambda: self.step_slider.setValue(self.step_slider.value() + 1))
        self.step_slider = QSlider(Qt.Orientation.Horizontal)
        self.step_slider.setEnabled(False)
        self.step_slider.valueChanged.connect(self.show_step)
        nav.addWidget(self.previous_button)
        nav.addWidget(self.step_slider, 1)
        nav.addWidget(self.next_button)
        process_layout.addLayout(nav)
        self.result = QLabel("El resultado aparecerá aquí.")
        self.result.setWordWrap(True)
        self.result.setTextFormat(Qt.TextFormat.RichText)
        self.result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        process_layout.addWidget(self.result)

        # El análisis (rango/nulidad/forma) y el LaTeX de la solución viven en una
        # ventana aparte para no recargar este panel (issue #15).
        detail_row = QHBoxLayout()
        self.analysis_button = QPushButton("Ver análisis y LaTeX  ↗")
        self.analysis_button.setObjectName("secondary")
        self.analysis_button.setToolTip("Abre una ventana con el rango/nulidad explicados, "
                                        "la solución renderizada y el código LaTeX.")
        self.analysis_button.setEnabled(False)
        self.analysis_button.clicked.connect(self.open_analysis_dialog)
        detail_row.addStretch()
        detail_row.addWidget(self.analysis_button)
        process_layout.addLayout(detail_row)

        self.analysis_dialog = None
        self._latex_code = ""
        self._build_analysis_widgets()

        splitter.addWidget(process_group)
        splitter.setSizes([560, 560])
        page.addWidget(splitter, 1)
        layout.addWidget(scroll, 1)

    # Explicaciones que aparecen al pasar el ratón por el signo "?" y como
    # subtítulo en el diálogo de análisis.
    EXPLICACIONES = {
        "rango": "Número de filas linealmente independientes de A: cuántas ecuaciones "
                 "aportan información nueva. Es el número de pivotes de la forma escalonada.",
        "nulidad": "Dimensión del conjunto de soluciones del sistema homogéneo Ax = 0. "
                   "Coincide con el número de variables libres (parámetros).",
        "suma": "Teorema del rango–nulidad: si A tiene n columnas, "
                "rango(A) + nulidad(A) = n. Sirve de comprobación.",
        "forma": "REF (escalonada): cada pivote está más a la derecha que el de la fila "
                 "de arriba y debajo de cada pivote hay ceros. "
                 "RREF (escalonada reducida): además cada pivote vale 1 y es el único "
                 "valor no nulo de su columna.",
    }

    def _build_analysis_widgets(self):
        """Crea (una sola vez) los widgets reutilizables del diálogo."""
        self.analysis_box = QWidget()
        self.analysis_layout = QVBoxLayout(self.analysis_box)
        self.analysis_layout.setContentsMargins(0, 0, 0, 0)
        self.analysis_layout.setSpacing(10)
        self.analysis_layout.addWidget(QLabel("Resuelve un sistema para ver el análisis."))

        self.solution_container = QWidget()
        self.solution_layout = QVBoxLayout(self.solution_container)
        self.solution_layout.setContentsMargins(2, 2, 2, 2)
        self.solution_layout.setSpacing(12)
        self.solution_scroll = QScrollArea()
        self.solution_scroll.setWidgetResizable(True)
        self.solution_scroll.setWidget(self.solution_container)
        self.solution_scroll.setMinimumSize(440, 220)

        self.latex_text = QTextEdit()
        self.latex_text.setReadOnly(True)
        self.latex_text.setMaximumHeight(130)

    @staticmethod
    def _help_badge(texto):
        badge = QLabel("?")
        badge.setObjectName("help")
        badge.setToolTip(texto)
        badge.setCursor(Qt.CursorShape.WhatsThisCursor)
        return badge

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout() is not None:
                GaussWindow._clear_layout(item.layout())
                item.layout().deleteLater()

    def _analysis_row(self, titulo, explicacion, clave):
        fila = QVBoxLayout()
        fila.setSpacing(1)
        cabecera = QHBoxLayout()
        etiqueta = QLabel(f"<b>{titulo}</b>")
        cabecera.addWidget(etiqueta)
        cabecera.addWidget(self._help_badge(self.EXPLICACIONES[clave]))
        cabecera.addStretch()
        fila.addLayout(cabecera)
        detalle = QLabel(explicacion)
        detalle.setObjectName("explain")
        detalle.setWordWrap(True)
        fila.addWidget(detalle)
        return fila

    def _render_analysis(self, rango, nulidad, suma, n, forma_esc):
        self._clear_layout(self.analysis_layout)
        forma_txt = {"RREF": "RREF (escalonada reducida)",
                     "REF": "REF (escalonada)",
                     "ninguna": "no escalonada"}.get(forma_esc, forma_esc)
        casa = "✓ coincide con el número de incógnitas" if suma == n else "✗ no coincide"
        for titulo, explicacion, clave in (
            (f"Rango(A) = {rango}", "Filas linealmente independientes (nº de pivotes).", "rango"),
            (f"Nulidad(A) = {nulidad}", "Número de variables libres del sistema.", "nulidad"),
            (f"Rango + Nulidad = {rango} + {nulidad} = {suma}", f"n = {n} incógnitas · {casa}.", "suma"),
            (f"Forma escalonada: {forma_txt}", "Cómo quedó la matriz tras la eliminación.", "forma"),
        ):
            self.analysis_layout.addLayout(self._analysis_row(titulo, explicacion, clave))

    def _pixmap_label(self, pixmap):
        etiqueta = QLabel()
        etiqueta.setPixmap(pixmap)
        etiqueta.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        return etiqueta

    def _math_line(self, expr):
        """QLabel con una expresión matemática renderizada (o texto si no hay matplotlib)."""
        pixmap = mathrender.latex_a_pixmap(expr) if mathrender.disponible() else None
        if pixmap is not None:
            return self._pixmap_label(pixmap)
        fallback = QLabel(expr)
        fallback.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return fallback

    def _render_solution_math(self, payload):
        """Dibuja la solución (y su comprobación) como notación matemática en el diálogo."""
        self._clear_layout(self.solution_layout)
        usar_img = mathrender.disponible()

        if payload["kind"] == "incompatible":
            self.solution_layout.addWidget(QLabel("El sistema es inconsistente: no hay solución que representar."))
            return

        fila = QHBoxLayout()
        fila.setSpacing(6)
        fila.addWidget(self._math_line(r"\mathbf{x} \;="))
        if usar_img:
            fila.addWidget(self._pixmap_label(mathrender.columna_a_pixmap(payload["particular"], MODO_ACTIVO)))
            for k, vec in enumerate(payload["vectores_nulos"]):
                fila.addWidget(self._math_line(rf"+\;\; t_{{{k + 1}}}"))
                fila.addWidget(self._pixmap_label(mathrender.columna_a_pixmap(vec, MODO_ACTIVO)))
        else:
            texto = QLabel(self._vector_solution_html(
                {"particular": payload["particular"], "vectores_nulos": payload["vectores_nulos"]}))
            texto.setTextFormat(Qt.TextFormat.RichText)
            fila.addWidget(texto)
        fila.addStretch()
        self.solution_layout.addLayout(fila)

        comp = payload.get("comprobacion")
        if comp:
            titulo = QLabel(f"<b>{comp['heading']}</b>")
            self.solution_layout.addWidget(titulo)
            for expr in comp["lineas"]:
                self.solution_layout.addWidget(self._math_line(expr))
        self.solution_layout.addStretch()

    def open_analysis_dialog(self):
        """Abre (o trae al frente) la ventana con el análisis y el LaTeX."""
        if self.analysis_dialog is None:
            dialog = QDialog(self)
            dialog.setWindowTitle("Análisis avanzado y LaTeX")
            dialog.setStyleSheet(STYLESHEET)
            dialog.setMinimumWidth(560)
            dialog.resize(640, 640)
            box = QVBoxLayout(dialog)

            rank_group = QGroupBox("Rango, nulidad y forma escalonada")
            QVBoxLayout(rank_group).addWidget(self.analysis_box)
            box.addWidget(rank_group)

            render_group = QGroupBox("Solución en notación matemática")
            QVBoxLayout(render_group).addWidget(self.solution_scroll)
            box.addWidget(render_group, 1)

            code_group = QGroupBox("Código LaTeX (para copiar / pegar en un editor)")
            code_layout = QVBoxLayout(code_group)
            code_layout.addWidget(self.latex_text)
            copy_latex = QPushButton("Copiar LaTeX")
            copy_latex.clicked.connect(self.copy_latex_to_clipboard)
            fila_copiar = QHBoxLayout()
            fila_copiar.addStretch()
            fila_copiar.addWidget(copy_latex)
            code_layout.addLayout(fila_copiar)
            box.addWidget(code_group)

            cerrar = QPushButton("Cerrar")
            cerrar.setObjectName("secondary")
            cerrar.clicked.connect(dialog.reject)
            fila_cerrar = QHBoxLayout()
            fila_cerrar.addStretch()
            fila_cerrar.addWidget(cerrar)
            box.addLayout(fila_cerrar)
            self.analysis_dialog = dialog

        self.analysis_dialog.show()
        self.analysis_dialog.raise_()
        self.analysis_dialog.activateWindow()

    def on_notation_changed(self, _index):
        """Cambia entre fracción exacta y decimal y repinta lo que haya en pantalla."""
        set_modo(MODO_DECIMAL if self.notation.currentText() == "Decimal" else MODO_FRACCION)
        if self.steps:
            self.solve()

    @staticmethod
    def _configure_table(table, editable=True):
        table.setAlternatingRowColors(True)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.verticalHeader().setDefaultSectionSize(38)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        if not editable:
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def rebuild_input_table(self):
        old_values = self._table_values(self.input_table)
        rows, columns = self.equations.value(), self.variables.value() + 1
        self.input_table.setRowCount(rows)
        self.input_table.setColumnCount(columns)
        self.input_table.setHorizontalHeaderLabels([f"x{i + 1}" for i in range(columns - 1)] + ["b"])
        self.input_table.setVerticalHeaderLabels([f"E{i + 1}" for i in range(rows)])
        for row in range(rows):
            for column in range(columns):
                value = old_values[row][column] if row < len(old_values) and column < len(old_values[row]) else "0"
                self.input_table.setItem(row, column, QTableWidgetItem(value))
        self.reset_result()

    def _table_values(self, table):
        return [[table.item(r, c).text() if table.item(r, c) else "0" for c in range(table.columnCount())] for r in range(table.rowCount())]

    def clear_table(self):
        for row in range(self.input_table.rowCount()):
            for column in range(self.input_table.columnCount()):
                self.input_table.item(row, column).setText("0")
        self.reset_result()

    def load_example(self, name):
        examples = {
            "Solución única": [[1, 1, 1, 6], [0, 2, 5, -4], [2, 5, -1, 27]],
            "Variables libres": [[1, 1, 1, 6], [2, 2, 2, 12], [1, -1, 0, 0]],
            "Sistema inconsistente": [[1, 1, 2], [1, 1, 5]],
        }
        matrix = examples[name]
        self.equations.setValue(len(matrix))
        self.variables.setValue(len(matrix[0]) - 1)
        self.rebuild_input_table()
        for row, values in enumerate(matrix):
            for column, value in enumerate(values):
                self.input_table.item(row, column).setText(str(value))

    def read_system(self):
        coefficients, terms = [], []
        for row in range(self.input_table.rowCount()):
            values = []
            for column in range(self.input_table.columnCount()):
                item = self.input_table.item(row, column)
                text = item.text().strip().replace(",", ".") if item else ""
                try:
                    values.append(float(text))
                except ValueError:
                    self.input_table.setCurrentCell(row, column)
                    raise ValueError(f"E{row + 1}, {self.input_table.horizontalHeaderItem(column).text()}: ingresa un número válido.")
            coefficients.append(values[:-1])
            terms.append(values[-1])
        return coefficients, terms

    def solve(self):
        try:
            coefficients, terms = self.read_system()
        except ValueError as error:
            QMessageBox.warning(self, "Dato inválido", str(error))
            return

        n = self.variables.value()
        matrix = crear_matriz_aumentada(coefficients, terms)
        self.steps = [("Matriz aumentada inicial", copiar_matriz(matrix))]

        def register(description, current):
            self.steps.append((description, copiar_matriz(current)))

        pivots = escalonar(matrix, n, registrar_paso=register)
        self.steps.append(("Forma escalonada final", copiar_matriz(matrix)))
        kind = clasificar(matrix, n, pivots)

        # Análisis: rango, nulidad, forma escalonada
        rango = rango_matriz(matrix, n)
        rango_nulidad = verificar_rango_nulidad(matrix, n, pivots)
        forma_esc = clasificar_forma_escalonada(matrix, n, pivots)

        self._render_analysis(rango, rango_nulidad["nulidad"], rango_nulidad["suma"], n, forma_esc)

        result_lines = []
        self._latex_code = ""
        payload = {"kind": kind, "particular": [], "vectores_nulos": [], "comprobacion": None}

        if kind == "incompatible":
            self.set_status("Sistema inconsistente · no tiene solución", "#ffe6e5", "#9f2520")
            result_lines.append("Una ecuación se redujo a <b>0 = c</b> (con c distinto de cero); "
                                "el sistema no tiene solución.")
            self.latex_text.setPlainText("")
        elif kind == "determinado":
            solution = sustitucion_regresiva(matrix, n, pivots)
            self.set_status("Sistema consistente determinado · solución única", "#dff7e7", "#176b46")
            result_lines.append("<b>Solución única</b>")
            result_lines.extend(f"{var(i)} = {format_display(value)}" for i, value in enumerate(solution))
            heading = "Comprobación (sustituyendo en el sistema original)"
            result_lines.append(self.verification_html(coefficients, terms, solution, heading))
            self._latex_code = "\\mathbf{x} = " + _pmatrix_latex(solution, MODO_ACTIVO)
            self.latex_text.setPlainText(self._latex_code)
            payload["particular"] = solution
            payload["comprobacion"] = {
                "heading": heading,
                "lineas": self._verificacion_latex(coefficients, terms, solution),
            }
        else:
            self.set_status("Sistema consistente indeterminado · infinitas soluciones", "#fff3cf", "#805900")
            reducir_a_escalonada_reducida(matrix, n, pivots, registrar_paso=register)
            self.steps.append(("Forma escalonada reducida", copiar_matriz(matrix)))
            free, expressions = solucion_parametrica(matrix, n, pivots)
            result_lines.append("<b>Solución paramétrica</b>")
            for variable in range(n):
                if variable in free:
                    result_lines.append(f"{var(variable)} = t{_sub(free.index(variable) + 1)} &nbsp; (variable libre)")
                    continue
                constant, parts = expressions[variable]
                expression = format_display(constant)
                for coefficient, free_variable in parts:
                    sign = "+" if coefficient >= 0 else MENOS
                    expression += (f" {sign} {format_display(abs(coefficient))} {POR} "
                                   f"t{_sub(free.index(free_variable) + 1)}")
                result_lines.append(f"{var(variable)} = {expression}")

            solucion_vec = solucion_general_vectorial(matrix, n, pivots, free, expressions)
            result_lines.append("<b>Solución vectorial</b> &nbsp; " + self._solucion_simbolica_html(len(free)))

            self._latex_code = generar_latex_solucion(n, free, expressions,
                                                      solucion_vec["particular"],
                                                      solucion_vec["vectores_nulos"], MODO_ACTIVO)
            self.latex_text.setPlainText(self._latex_code)

            example_solution = evaluar_solucion_parametrica(n, free, expressions, [0.0] * len(free))
            libres_cero = ", ".join(f"t{_sub(k + 1)} = 0" for k in range(len(free)))
            heading = f"Comprobación con {libres_cero}"
            result_lines.append(self.verification_html(coefficients, terms, example_solution, heading))
            payload["particular"] = solucion_vec["particular"]
            payload["vectores_nulos"] = solucion_vec["vectores_nulos"]
            payload["comprobacion"] = {
                "heading": heading,
                "lineas": self._verificacion_latex(coefficients, terms, example_solution),
            }

        self.result.setText("<br>".join(result_lines))
        self._render_solution_math(payload)
        self.analysis_button.setEnabled(True)
        self.step_slider.setRange(0, len(self.steps) - 1)
        self.step_slider.setEnabled(True)
        self.step_slider.setValue(0)
        self.show_step(0)

    def _vector_solution_html(self, solucion_vec):
        """x = x_p + t₁v₁ + … con vectores columna entre corchetes (rich text)."""
        piezas = ["<b>x</b> = ", vector_columna_html(solucion_vec["particular"], MODO_ACTIVO)]
        for k, vec in enumerate(solucion_vec["vectores_nulos"]):
            piezas.append(f" &nbsp;+&nbsp; t{_sub(k + 1)}")
            piezas.append(vector_columna_html(vec, MODO_ACTIVO))
        return "".join(piezas)

    @staticmethod
    def _solucion_simbolica_html(num_libres):
        """Forma simbólica x = x_p + t₁·v₁ + … (el detalle numérico va en el diálogo)."""
        if num_libres == 0:
            return ""
        terminos = " + ".join(f"t<sub>{k + 1}</sub>{POR}v<sub>{k + 1}</sub>"
                              for k in range(num_libres))
        return (f"<b>x</b> = <b>x</b><sub>p</sub> + {terminos} &nbsp;"
                "<span style='color:#5a7d92'>— vectores en «Ver análisis y LaTeX»</span>")

    def _verificacion_latex(self, coefficients, terms, solution):
        """Lista de expresiones LaTeX (una por ecuación) para la comprobación renderizada."""
        lineas = []
        for i, fila in enumerate(verificar_solucion_detallada(coefficients, terms, solution)):
            activos = [(c, xj, p) for (c, xj, p) in fila["terminos"]
                       if not valor_casi_cero(c)] or fila["terminos"][:1]
            partes = []
            for k, (c, xj, _p) in enumerate(activos):
                signo = "" if k == 0 else ("+ " if c >= 0 else "- ")
                coef = latex_valor(abs(c) if k else c, MODO_ACTIVO)
                partes.append(rf"{signo}{coef} \cdot ({latex_valor(xj, MODO_ACTIVO)})")
            rel = "=" if fila["coincide"] else r"\neq"
            lineas.append(
                rf"\mathrm{{E}}_{{{i + 1}}}:\;\; " + " ".join(partes)
                + rf" \;=\; {latex_valor(fila['suma'], MODO_ACTIVO)}"
                + rf" \;{rel}\; {latex_valor(fila['esperado'], MODO_ACTIVO)}"
            )
        return lineas

    def verification_html(self, coefficients, terms, solution, heading="Comprobación (sustituyendo en el sistema original)"):
        """Demostración de la comprobación término a término (issue #16)."""
        filas = verificar_solucion_detallada(coefficients, terms, solution)
        bloques = [f"<b>{heading}</b>"]
        todo = True
        for i, fila in enumerate(filas):
            activos = [(c, xj, p) for (c, xj, p) in fila["terminos"] if not valor_casi_cero(c)] or fila["terminos"][:1]
            factores = " ".join(
                (("" if k == 0 else ("+ " if c >= 0 else f"{MENOS} ")) +
                 f"{format_display(abs(c) if k else c)} {POR} ({format_display(xj)})")
                for k, (c, xj, p) in enumerate(activos)
            )
            suma = format_display(fila["suma"])
            esperado = format_display(fila["esperado"])
            simbolo = "=" if fila["coincide"] else "≠"
            if not fila["coincide"]:
                todo = False
            bloques.append(f"E{i + 1}: &nbsp; {factores} &nbsp; = &nbsp; <b>{suma}</b> {simbolo} {esperado}")
        cierre = ("✓ La solución satisface todas las ecuaciones."
                  if todo else "✗ La solución NO satisface todas las ecuaciones.")
        bloques.append(cierre)
        return "<br>".join(bloques)

    def copy_latex_to_clipboard(self):
        """Copia el contenido del campo LaTeX al portapapeles."""
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.latex_text.toPlainText())
        QMessageBox.information(self, "Copiado", "Código LaTeX copiado al portapapeles.")

    def show_step(self, index):
        if not self.steps:
            return
        index = max(0, min(index, len(self.steps) - 1))
        description, matrix = self.steps[index]
        n = self.variables.value()
        self.step_description.setText(f"Paso {index + 1} de {len(self.steps)} · {description}")
        self.populate_display_table(self.step_table, matrix, n)
        self.previous_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.steps) - 1)

    def populate_display_table(self, table, matrix, n):
        table.setRowCount(len(matrix))
        table.setColumnCount(n + 1)
        table.setHorizontalHeaderLabels([f"x{i + 1}" for i in range(n)] + ["b"])
        table.setVerticalHeaderLabels([f"E{i + 1}" for i in range(len(matrix))])
        for row, values in enumerate(matrix):
            for column, value in enumerate(values):
                item = QTableWidgetItem(format_number(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, column, item)

    def reset_result(self):
        self.steps = []
        self.step_table.clear()
        self.step_table.setRowCount(0)
        self.step_table.setColumnCount(0)
        self.step_slider.setEnabled(False)
        self.step_description.setText("Aún no hay pasos para mostrar.")
        self.result.setText("El resultado aparecerá aquí.")
        if hasattr(self, "analysis_button"):
            self.analysis_button.setEnabled(False)
            self._latex_code = ""
            self.latex_text.setPlainText("")
            self._clear_layout(self.analysis_layout)
            self.analysis_layout.addWidget(QLabel("Resuelve un sistema para ver el análisis."))
            self._clear_layout(self.solution_layout)
        self.set_status("Matriz actualizada · lista para resolver", "#dff7e7", "#176b46")

    def set_status(self, text, background, foreground):
        self.status.setText(text)
        self.status.setStyleSheet(f"background: {background}; color: {foreground};")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#dff7ff"))
    app.setPalette(palette)
    window = GaussWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
