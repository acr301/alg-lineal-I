"""Punto de entrada de la aplicación.

Delega en el cliente por defecto (PyQt6). Cuando existan otros clientes (TUI en
#18, web en el server) tendrán sus propios entry points; este ``main`` sigue
apuntando al gráfico.
"""

from aqua_gauss.clients.qt.app import main

__all__ = ["main"]


if __name__ == "__main__":  # pragma: no cover
    main()
