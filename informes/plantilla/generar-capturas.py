"""Genera las 3 capturas de la pantalla "Proceso y resultado" para el informe.

Renderiza la GUI real (`aqua_gauss.clients.qt`) en modo offscreen, carga cada
ejemplo del menú, salta al último paso (forma escalonada final / RREF) y guarda
un PNG.

Uso (desde la raíz del repo, con el paquete instalado — `uv sync --extra qt`):

    uv run python informes/plantilla/generar-capturas.py informes/Informe_Programa_2_Grupo_7/img

Deja: caso1-unica.png · caso2-libres.png · caso3-inconsistente.png
"""

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("AQUA_GAUSS_SILENCIAR", "1")

from PyQt6.QtWidgets import QApplication, QScrollArea  # noqa: E402

from aqua_gauss.clients.qt.app import VentanaPrincipal  # noqa: E402

CASOS = [
    ("Solución única", "caso1-unica.png"),
    ("Infinitas soluciones", "caso2-libres.png"),
    ("Sistema inconsistente", "caso3-inconsistente.png"),
]


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    app = QApplication(sys.argv)

    for etiqueta, archivo in CASOS:
        win = VentanaPrincipal()
        win.resize(1100, 1400)
        win.sesion.cargar_ejemplo(etiqueta)
        win.ir("proceso")
        for _ in range(6):
            app.processEvents()

        proceso = win.pantallas["proceso"]
        if getattr(proceso, "pasos", None):
            proceso._mostrar_paso(len(proceso.pasos) - 1)
        for _ in range(4):
            app.processEvents()

        area = proceso.findChild(QScrollArea)
        objetivo = area.widget() if area is not None else proceso
        objetivo.adjustSize()
        for _ in range(3):
            app.processEvents()

        ruta = os.path.join(out, archivo)
        ok = objetivo.grab().save(ruta, "PNG")
        print(f"{'OK ' if ok else 'FALLO '} {ruta}")
        win.close()
        win.deleteLater()
        app.processEvents()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
