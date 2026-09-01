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
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QComboBox,
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
    generar_latex_solucion,
    rango_matriz,
    reducir_a_escalonada_reducida,
    solucion_general_vectorial,
    solucion_parametrica,
    sustitucion_regresiva,
    valor_casi_cero,
    verificar_rango_nulidad,
    verificar_solucion,
)


STYLESHEET = """
QMainWindow { background: #dff7ff; }
QWidget { color: #153653; font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 14px; }
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


def format_number(value):
    """Presenta enteros sin decimales y el resto con hasta cuatro cifras."""
    rounded = round(value)
    if valor_casi_cero(value - rounded):
        return str(int(rounded))
    return f"{value:.4f}".rstrip("0").rstrip(".")


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
        self.result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        process_layout.addWidget(self.result)

        # Sección de análisis y LaTeX
        analysis_group = QGroupBox("4 · Análisis avanzado")
        analysis_layout = QVBoxLayout(analysis_group)

        self.analysis_text = QLabel("Análisis: rango, nulidad, forma escalonada")
        self.analysis_text.setWordWrap(True)
        self.analysis_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        analysis_layout.addWidget(self.analysis_text)

        latex_label = QLabel("Código LaTeX de la solución:")
        analysis_layout.addWidget(latex_label)
        self.latex_text = QTextEdit()
        self.latex_text.setReadOnly(True)
        self.latex_text.setMaximumHeight(120)
        analysis_layout.addWidget(self.latex_text)

        latex_button_layout = QHBoxLayout()
        copy_latex = QPushButton("Copiar LaTeX")
        copy_latex.clicked.connect(self.copy_latex_to_clipboard)
        latex_button_layout.addStretch()
        latex_button_layout.addWidget(copy_latex)
        analysis_layout.addLayout(latex_button_layout)

        process_layout.addWidget(analysis_group)
        splitter.addWidget(process_group)
        splitter.setSizes([560, 560])
        page.addWidget(splitter, 1)
        layout.addWidget(scroll, 1)

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

        analysis_lines = []
        analysis_lines.append(f"Rango(A): {rango}")
        analysis_lines.append(f"Nulidad(A): {rango_nulidad['nulidad']}")
        analysis_lines.append(f"Rango + Nulidad = {rango_nulidad['suma']} (esperado: {n})")
        analysis_lines.append(f"Forma escalonada: {forma_esc}")
        self.analysis_text.setText(" | ".join(analysis_lines))

        result_lines = []
        latex_code = ""

        if kind == "incompatible":
            self.set_status("Sistema inconsistente · no tiene solución", "#ffe6e5", "#9f2520")
            result_lines.append("Una ecuación se redujo a 0 = c (con c distinto de cero).")
            self.latex_text.setPlainText("")
        elif kind == "determinado":
            solution = sustitucion_regresiva(matrix, n, pivots)
            self.set_status("Sistema consistente determinado · solución única", "#dff7e7", "#176b46")
            result_lines.append("<b>Solución única</b>")
            result_lines.extend(f"x{i + 1} = {format_number(value)}" for i, value in enumerate(solution))
            result_lines.append(self.verification_html(coefficients, terms, solution))
            self.latex_text.setPlainText("")
        else:
            self.set_status("Sistema consistente indeterminado · infinitas soluciones", "#fff3cf", "#805900")
            reducir_a_escalonada_reducida(matrix, n, pivots, registrar_paso=register)
            self.steps.append(("Forma escalonada reducida", copiar_matriz(matrix)))
            free, expressions = solucion_parametrica(matrix, n, pivots)
            result_lines.append("<b>Solución paramétrica</b>")
            for variable in range(n):
                if variable in free:
                    result_lines.append(f"x{variable + 1} = t{free.index(variable) + 1} &nbsp; (variable libre)")
                    continue
                constant, parts = expressions[variable]
                expression = format_number(constant)
                for coefficient, free_variable in parts:
                    sign = "+" if coefficient >= 0 else "−"
                    expression += f" {sign} {format_number(abs(coefficient))}·t{free.index(free_variable) + 1}"
                result_lines.append(f"x{variable + 1} = {expression}")

            # Solución vectorial y LaTeX
            solucion_vec = solucion_general_vectorial(matrix, n, pivots, free, expressions)
            result_lines.append("<b>Solución vectorial</b>")
            result_lines.append(f"xp = [{', '.join(format_number(v) for v in solucion_vec['particular'])}]")
            for k, vec in enumerate(solucion_vec["vectores_nulos"]):
                result_lines.append(f"v{k + 1} = [{', '.join(format_number(v) for v in vec)}]")

            latex_code = generar_latex_solucion(n, free, expressions,
                                                solucion_vec["particular"],
                                                solucion_vec["vectores_nulos"])
            self.latex_text.setPlainText(latex_code)

            example_solution = evaluar_solucion_parametrica(n, free, expressions, [0.0] * len(free))
            result_lines.append(self.verification_html(coefficients, terms, example_solution, "Verificación con todos los parámetros en 0"))

        self.result.setText("<br>".join(result_lines))
        self.step_slider.setRange(0, len(self.steps) - 1)
        self.step_slider.setEnabled(True)
        self.step_slider.setValue(0)
        self.show_step(0)

    def verification_html(self, coefficients, terms, solution, heading="Verificación"):
        matches = verificar_solucion(coefficients, terms, solution)
        detail = " · ".join(
            f"E{i + 1}: {format_number(actual)} {'=' if matches else '≠'} {format_number(expected)}"
            for i, (actual, expected, matches) in enumerate(matches)
        )
        return f"<br><b>{heading}</b><br>{detail}"

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
