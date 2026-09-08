"""
main.py

Programa interactivo que resuelve sistemas de ecuaciones lineales Ax = b
usando el método de eliminación de Gauss (reducción por filas), muestra
cada paso del proceso y clasifica el sistema según sus soluciones:

  - Consistente determinado   -> solución única.
  - Consistente indeterminado -> infinitas soluciones (solución paramétrica).
  - Inconsistente             -> sin solución.

Toda la lógica del algoritmo vive en gauss.py (sin input/print). Este
archivo solo se encarga de la interacción con el usuario por consola.

Uso:
    python3 main.py                 # valores como fracción exacta (por defecto)
    python3 main.py --decimal       # valores en decimal
"""

import sys

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
    MODO_DECIMAL,
    MODO_FRACCION,
    entrada_b,
    formatear_valor,
    generar_latex_solucion,
    latex_combinacion_lineal,
    parametro,
    subindice,
    texto_combinacion_lineal,
    var,
)
from vectores import (
    combinacion_lineal,
    es_combinacion_lineal,
    verificar_propiedades,
)

# Modo de presentación numérica; se ajusta según los argumentos de línea de
# comandos en main(). Fracción exacta por defecto (más legible para álgebra).
MODO = MODO_FRACCION


def pedir_entero(mensaje, minimo=1):
    """Pide un entero >= minimo por consola, repitiendo hasta que sea válido."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  Por favor ingresa un número entero válido.")
            continue
        if valor < minimo:
            print(f"  Debe ser un entero mayor o igual a {minimo}.")
            continue
        return valor


def pedir_flotante(mensaje):
    """Pide un número (entero o decimal) por consola, repitiendo hasta que sea válido."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("  Por favor ingresa un número válido (usa punto decimal, ej: 3.5).")


def leer_sistema():
    """Lee interactivamente el número de ecuaciones/incógnitas y la matriz aumentada."""
    print("=== Resolución de sistemas de ecuaciones lineales Ax = b ===")
    print("Método: eliminación de Gauss (reducción a forma escalonada)\n")

    m = pedir_entero("Número de ecuaciones (filas): ")
    n = pedir_entero("Número de incógnitas (columnas de A): ")

    coeficientes = []
    terminos = []
    print("\nIngresa los coeficientes de cada ecuación y su término independiente.")
    for i in range(m):
        print(f"\n-- Ecuación {i + 1} --")
        fila = []
        for j in range(n):
            fila.append(pedir_flotante(f"  Coeficiente de {var(j)}: "))
        b = pedir_flotante(f"  Término independiente ({entrada_b(i)}): ")
        coeficientes.append(fila)
        terminos.append(b)

    return coeficientes, terminos, m, n


def leer_vector(n, nombre):
    """Lee las ``n`` componentes de un vector por consola."""
    print(f"\n-- Vector {nombre} de R^{n} --")
    return [pedir_flotante(f"  Componente {i + 1}: ") for i in range(n)]


def resolver_combinacion_vectorial(vectores, pesos):
    """Calcula y presenta una combinación lineal en consola."""
    resultado = combinacion_lineal(vectores, pesos)
    print("\n--- Resultado de la combinación lineal ---")
    print(texto_combinacion_lineal(resultado, vectores, pesos, MODO))
    print("\nCódigo LaTeX:")
    print(latex_combinacion_lineal(resultado, vectores, pesos, MODO))
    return resultado


def comprobar_combinacion_vectorial(objetivo, vectores):
    """Explica en consola si un objetivo pertenece al generado."""
    pertenece, pesos = es_combinacion_lineal(objetivo, vectores)
    print("\n--- ¿Es combinación lineal? ---")
    if not pertenece:
        print("El vector objetivo NO es combinación lineal de los vectores dados.")
        return pertenece, pesos
    print("El vector objetivo SÍ es combinación lineal.")
    print("Pesos encontrados:")
    for i, peso in enumerate(pesos):
        print(f"  c{i + 1} = {formatear_numero(peso)}")
    print(latex_combinacion_lineal(objetivo, vectores, pesos, MODO))
    return pertenece, pesos


def imprimir_propiedades_vectoriales(u, v, w, a, b):
    """Muestra el resultado de los ocho axiomas evaluados."""
    propiedades = verificar_propiedades(u, v, w, a, b)
    print("\n--- Propiedades algebraicas de R^n ---")
    for datos in propiedades.values():
        estado = "OK" if datos["cumple"] else "NO cumple"
        izquierdo = [formatear_numero(x) for x in datos["lado_izquierdo"]]
        derecho = [formatear_numero(x) for x in datos["lado_derecho"]]
        print(f"  {datos['propiedad']}: {izquierdo} = {derecho} -> {estado}")
    return propiedades


def flujo_vectores():
    """Flujo interactivo de la Tarea 3 para consola."""
    print("\n=== Vectores y propiedades algebraicas de R^n ===")
    print("1. Calcular una combinación lineal")
    print("2. Comprobar si un objetivo es combinación lineal")
    print("3. Verificar las ocho propiedades algebraicas")
    opcion = pedir_entero("Opción: ")
    while opcion not in (1, 2, 3):
        print("  Elige 1, 2 o 3.")
        opcion = pedir_entero("Opción: ")

    n = pedir_entero("Dimensión n de los vectores: ")
    if opcion in (1, 2):
        p = pedir_entero("Cantidad p de vectores: ")
        vectores = [leer_vector(n, f"v{i + 1}") for i in range(p)]
        if opcion == 1:
            pesos = [pedir_flotante(f"Peso c{i + 1}: ") for i in range(p)]
            resolver_combinacion_vectorial(vectores, pesos)
        else:
            objetivo = leer_vector(n, "objetivo b")
            comprobar_combinacion_vectorial(objetivo, vectores)
        return

    u = leer_vector(n, "u")
    v = leer_vector(n, "v")
    w = leer_vector(n, "w")
    a = pedir_flotante("Escalar a: ")
    b = pedir_flotante("Escalar b: ")
    imprimir_propiedades_vectoriales(u, v, w, a, b)


def formatear_numero(valor):
    """Formatea un valor según el MODO activo (fracción exacta o decimal)."""
    return formatear_valor(valor, MODO)


def imprimir_matriz(matriz, n_incognitas, titulo=None):
    """Imprime la matriz aumentada [A | b] de forma legible."""
    if titulo:
        print(titulo)
    for fila in matriz:
        coeficientes_str = "  ".join(
            f"{formatear_numero(v):>8}" for v in fila[:n_incognitas]
        )
        termino_str = formatear_numero(fila[n_incognitas])
        print(f"[ {coeficientes_str}  |  {termino_str:>8} ]")


def _con_signo(texto, es_primero):
    """Antepone ' + ' / ' - ' a un valor ya formateado, para encadenar términos."""
    negativo = texto.startswith("-")
    cuerpo = texto[1:] if negativo else texto
    if es_primero:
        return f"-{cuerpo}" if negativo else cuerpo
    return f" - {cuerpo}" if negativo else f" + {cuerpo}"


def _linea_sustitucion(terminos):
    """
    A partir de [(coef, x_j, producto), ...] arma las dos partes de la
    demostración:  '2·(5) + 1·(-3)'   y   '10 - 3'.
    Omite los términos con coeficiente 0 (no aportan nada a la suma).
    """
    activos = [(c, xj, p) for (c, xj, p) in terminos if not valor_casi_cero(c)]
    if not activos:
        activos = terminos[:1]  # todos los coeficientes eran 0: mostrar 0·(x)
    factores = ""
    productos = ""
    for indice, (coef, xj, producto) in enumerate(activos):
        primero = indice == 0
        factores += _con_signo(f"{formatear_numero(coef)}·({formatear_numero(xj)})", primero)
        productos += _con_signo(formatear_numero(producto), primero)
    return factores, productos


def imprimir_verificacion(coeficientes, terminos, x, titulo="Verificación (sustituyendo en el sistema original)"):
    """
    Sustituye 'x' en el sistema original [coeficientes | terminos] y muestra,
    ecuación por ecuación, la DEMOSTRACIÓN completa: los factores coef·(x_j),
    la suma de los productos y la comparación con el término independiente.
    """
    print(f"\n--- {titulo} ---")
    resultados = verificar_solucion_detallada(coeficientes, terminos, x)
    todo_coincide = True
    for i, resultado in enumerate(resultados):
        factores, productos = _linea_sustitucion(resultado["terminos"])
        suma = formatear_numero(resultado["suma"])
        esperado = formatear_numero(resultado["esperado"])
        coincide = resultado["coincide"]
        if not coincide:
            todo_coincide = False
        simbolo = "=" if coincide else "≠"
        estado = "OK" if coincide else "NO coincide"
        print(f"  Ecuación {i + 1}:")
        print(f"    {factores}")
        if productos != suma:
            print(f"    = {productos}")
        print(f"    = {suma} {simbolo} {esperado} ({entrada_b(i)})  ->  {estado}")
    if todo_coincide:
        print("La solución satisface todas las ecuaciones del sistema original.")
    else:
        print("ADVERTENCIA: la solución NO satisface todas las ecuaciones.")


def resolver_sistema(coeficientes, terminos, n):
    """Ejecuta el flujo completo (escalonar, clasificar, mostrar) para un sistema dado."""
    matriz = crear_matriz_aumentada(coeficientes, terminos)
    imprimir_matriz(matriz, n, "\nMatriz aumentada [A | b] inicial:")

    pasos = []

    def registrar(descripcion, matriz_actual):
        pasos.append((descripcion, copiar_matriz(matriz_actual)))

    print("\n--- Proceso de eliminación (reducción por filas) ---")
    columnas_pivote = escalonar(matriz, n, registrar_paso=registrar,
                                formato_numero=formatear_numero)

    if not pasos:
        print("(La matriz ya estaba en forma escalonada, no hizo falta ninguna operación.)")
    for descripcion, matriz_paso in pasos:
        imprimir_matriz(matriz_paso, n, f"\nPaso: {descripcion}")

    imprimir_matriz(matriz, n, "\nForma escalonada final:")

    tipo = clasificar(matriz, n, columnas_pivote)

    # Información sobre rango, nulidad y forma escalonada
    rango = rango_matriz(matriz, n)
    info_rango_nulidad = verificar_rango_nulidad(matriz, n, columnas_pivote)
    forma_esc = clasificar_forma_escalonada(matriz, n, columnas_pivote)

    print("\n--- Análisis de la matriz ---")
    print(f"Rango(A): {rango}")
    print(f"Nulidad(A) (variables libres): {info_rango_nulidad['nulidad']}")
    print(f"Verificación rango-nulidad: {rango} + {info_rango_nulidad['nulidad']} = {info_rango_nulidad['suma']} (esperado: {n})")
    print(f"Forma escalonada: {forma_esc}")

    print("\n--- Clasificación del sistema ---")
    if tipo == "incompatible":
        print("Sistema INCONSISTENTE: no tiene solución.")
        print("(Una fila quedó de la forma 0 = c, con c distinto de 0.)")

    elif tipo == "determinado":
        print("Sistema CONSISTENTE DETERMINADO: tiene solución única.")
        x = sustitucion_regresiva(matriz, n, columnas_pivote)
        print("\nSolución:")
        for j in range(n):
            print(f"  {var(j)} = {formatear_numero(x[j])}")

        imprimir_verificacion(coeficientes, terminos, x)

    else:
        print("Sistema CONSISTENTE INDETERMINADO: tiene infinitas soluciones.")

        pasos_rref = []

        def registrar_rref(descripcion, matriz_actual):
            pasos_rref.append((descripcion, copiar_matriz(matriz_actual)))

        print("\n--- Reducción adicional a forma escalonada reducida ---")
        print("(para expresar la solución en función de las variables libres)")
        reducir_a_escalonada_reducida(matriz, n, columnas_pivote,
                                      registrar_paso=registrar_rref,
                                      formato_numero=formatear_numero)
        for descripcion, matriz_paso in pasos_rref:
            imprimir_matriz(matriz_paso, n, f"\nPaso: {descripcion}")

        libres, expresiones = solucion_parametrica(matriz, n, columnas_pivote)

        nombres_libres = [var(v) for v in libres]
        print("\nVariables libres (parámetros):", ", ".join(nombres_libres))

        print("\nSolución paramétrica:")
        for v in range(n):
            if v in libres:
                print(f"  {var(v)} = {parametro(libres.index(v))}   (variable libre)")
            else:
                termino, partes = expresiones[v]
                texto = formatear_numero(termino)
                for coef, indice_libre in partes:
                    signo = "+" if coef >= 0 else "-"
                    texto += f" {signo} {formatear_numero(abs(coef))}*{parametro(libres.index(indice_libre))}"
                print(f"  {var(v)} = {texto}")

        # Solución vectorial
        print("\n--- Solución general vectorial ---")
        solucion_vec = solucion_general_vectorial(matriz, n, columnas_pivote, libres, expresiones)

        ecuacion_vec = "x = xp"
        if libres:
            ecuacion_vec += " + " + " + ".join(f"{parametro(k)}*v{subindice(k+1)}" for k in range(len(libres)))
        print(ecuacion_vec)

        print("\nDonde:")
        print("xp (solución particular) =", [f"{formatear_numero(v)}" for v in solucion_vec["particular"]])
        for k, vec in enumerate(solucion_vec["vectores_nulos"]):
            print(f"v{subindice(k + 1)} =", [f"{formatear_numero(v)}" for v in vec])

        # LaTeX de la solución
        print("\n--- Código LaTeX (para copiar) ---")
        latex_code = generar_latex_solucion(n, libres, expresiones,
                                            solucion_vec["particular"],
                                            solucion_vec["vectores_nulos"], MODO)
        print(latex_code)

        valores_ejemplo = [0.0] * len(libres)
        x_ejemplo = evaluar_solucion_parametrica(n, libres, expresiones, valores_ejemplo)
        asignaciones = ", ".join(
            f"{parametro(k)} = {formatear_numero(v)}" for k, v in enumerate(valores_ejemplo)
        )
        titulo = f"Verificación con un ejemplo concreto ({asignaciones})"
        imprimir_verificacion(coeficientes, terminos, x_ejemplo, titulo)


def main():
    global MODO
    if "--decimal" in sys.argv:
        MODO = MODO_DECIMAL
    elif "--fraccion" in sys.argv:
        MODO = MODO_FRACCION
    etiqueta = "decimal" if MODO == MODO_DECIMAL else "fracción exacta"
    print(f"(Los valores se muestran en {etiqueta}; usa --decimal o --fraccion para cambiar.)\n")

    while True:
        print("¿Qué quieres estudiar?")
        print("1. Sistemas de ecuaciones lineales")
        print("2. Vectores y propiedades de R^n")
        opcion = pedir_entero("Opción: ")
        while opcion not in (1, 2):
            print("  Elige 1 o 2.")
            opcion = pedir_entero("Opción: ")
        if opcion == 1:
            coeficientes, terminos, _m, n = leer_sistema()
            resolver_sistema(coeficientes, terminos, n)
        else:
            flujo_vectores()

        respuesta = input("\n¿Deseas realizar otra operación? (s/n): ").strip().lower()
        if respuesta != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
