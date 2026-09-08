"""Cliente gráfico (PyQt6) organizado por pantallas.

Flujo:  Menú → Dimensiones → Entrada guiada → Proceso y resultado → Solución vectorial

- ``app.py``       ventana principal (QStackedWidget) + estado compartido
- ``state.py``     Sesion: dimensiones, notación, matriz y resultado del cálculo
- ``theme.py``     hoja de estilo, paleta y fuente (APP_INFO)
- ``widgets.py``   widgets reutilizables (matriz, botón de ayuda, barra de navegación)
- ``mathrender.py``render de LaTeX a imagen (degrada a texto si falta matplotlib)
- ``screen_*.py``  una pantalla por archivo

Toda la lógica de álgebra vive en ``aqua_gauss.core`` (Gauss, RREF, vectores) y
la conversión de números a texto/fracción en ``aqua_gauss.core.formato``.
"""

from aqua_gauss.clients.qt.app import main

__all__ = ["main"]
