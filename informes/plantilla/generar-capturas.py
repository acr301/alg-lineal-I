"""Capturas de la app para el informe, fieles a lo que se ve en pantalla.

Lanza la GUI (`aqua_gauss.clients.qt`) con el backend **nativo** de macOS (no
"offscreen"), aplica el tema real y fotografía cada ventana con
``QWidget.grab()``: los mismos píxeles que pinta la app —tipografía del sistema,
degradado del encabezado, matrices renderizadas con matplotlib— sin la barra de
título del sistema (que no es contenido de la app).

Se prefiere ``grab()`` a ``screencapture`` de macOS porque no depende del orden
de ventanas ni de permisos de *Grabación de pantalla*: es determinista.

Uso (desde la raíz del repo, con el paquete instalado — ``uv sync --extra qt``):

    uv run python informes/plantilla/generar-capturas.py informes/Informe_Programa_2_Grupo_7/img

Deja, por cada caso (única / infinitas / inconsistente):
    casoN-proceso.png     pantalla "Proceso y resultado" en el último paso (RREF)
    casoN-vectorial.png   pantalla "Solución en notación vectorial"
"""

import os
import sys
import time

os.environ.pop("QT_QPA_PLATFORM", None)  # backend nativo (cocoa), no "offscreen"
os.environ.setdefault("AQUA_GAUSS_SILENCIAR", "1")

from PyQt6.QtWidgets import QApplication  # noqa: E402

from aqua_gauss.clients.qt.app import VentanaPrincipal  # noqa: E402
from aqua_gauss.clients.qt.theme import aplicar_tema  # noqa: E402

CASOS = [
    ("Solución única", "caso1"),
    ("Infinitas soluciones", "caso2"),
    ("Sistema inconsistente", "caso3"),
]
TAM = (1040, 760)  # tamaño por defecto de la ventana de la app


def _asentar(app, veces=25):
    for _ in range(veces):
        app.processEvents()
        time.sleep(0.04)
    time.sleep(0.5)
    app.processEvents()


def _foto(win, ruta):
    win.grab().save(ruta, "PNG")
    print(f"OK  {ruta}")


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)

    app = QApplication(sys.argv)
    aplicar_tema(app)

    for etiqueta, base in CASOS:
        win = VentanaPrincipal()
        win.setFixedSize(*TAM)
        win.sesion.cargar_ejemplo(etiqueta)

        win.ir("proceso")
        proceso = win.pantallas["proceso"]
        if getattr(proceso, "pasos", None):
            proceso._mostrar_paso(len(proceso.pasos) - 1)  # último paso: RREF / escalonada final
        win.show()
        _asentar(app)
        _foto(win, os.path.join(out, f"{base}-proceso.png"))

        win.ir("resultado")  # pantalla "4 · Solución en notación vectorial"
        _asentar(app, veces=15)
        _foto(win, os.path.join(out, f"{base}-vectorial.png"))

        win.close()
        win.deleteLater()
        app.processEvents()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
