"""
Paquete de interfaz gráfica (PyQt6) organizado por pantallas.

Flujo:  Menú → Dimensiones → Entrada guiada → Proceso y resultado → Solución vectorial

- ``app.py``            ventana principal (QStackedWidget) + estado compartido
- ``state.py``          Sesion: dimensiones, notación, matriz y resultado del cálculo
- ``theme.py``          hoja de estilo, paleta y fuente
- ``widgets.py``        widgets reutilizables (matriz, botón de ayuda, barra de navegación)
- ``screen_*.py``       una pantalla por archivo

Toda la lógica de álgebra sigue en ``gauss.py`` (sin cambios). La conversión de
números a texto/fracción vive en ``formato.py`` y el render de LaTeX en
``mathrender.py``.
"""

from ui.app import main

__all__ = ["main"]
