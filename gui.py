"""Lanzador de la interfaz gráfica de Aqua Gauss.

Atajo equivalente a ``aqua-gauss`` o ``python -m aqua_gauss``. Requiere el
paquete instalado en el entorno (``uv sync --extra qt``); ya no manipula
``sys.path``.

    uv sync --extra qt
    uv run aqua-gauss          # o:  uv run python gui.py
"""

from aqua_gauss.app import main

if __name__ == "__main__":
    main()
