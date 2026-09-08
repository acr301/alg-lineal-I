"""Aqua Gauss — resuelve y analiza sistemas lineales Ax = b por eliminación de Gauss.

Estructura del paquete:

- ``aqua_gauss.core``        Model puro: álgebra lineal sin dependencias de framework.
- ``aqua_gauss.clients.qt``  Cliente gráfico (PyQt6) organizado por pantallas.
- ``aqua_gauss.app``         Punto de entrada (``aqua-gauss`` / ``python -m aqua_gauss``).

La versión "de verdad" vive en ``pyproject.toml``; se lee en runtime con
``importlib.metadata`` (ver issue #26).
"""
