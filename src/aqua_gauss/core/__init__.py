"""Núcleo de cálculo: álgebra lineal pura, sin dependencias de framework.

Módulos:

- ``gauss``         eliminación de Gauss, clasificación y análisis de sistemas Ax = b
- ``gauss_jordan``  reducción a forma escalonada reducida (RREF) y solución paramétrica
- ``vectores``      operaciones en R^n, combinaciones lineales y los ocho axiomas
- ``formato``       conversión de números a texto/fracción y notación LaTeX

Restricción de la fase actual: estos módulos no importan ``fractions``, NumPy,
SymPy ni ninguna rutina externa de álgebra lineal; solo listas, bucles y
aritmética básica. Se irá levantando a medida que avance el contenido, y se
levantará aquí sin tocar los clientes.
"""
