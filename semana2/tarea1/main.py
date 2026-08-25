"""
main.py

Programa interactivo que resuelve sistemas de ecuaciones lineales Ax = b
usando el método de eliminación de Gauss (reducción por filas), muestra
cada paso del proceso y clasifica el sistema según sus soluciones:

  - Compatible determinado   -> solución única.
  - Compatible indeterminado -> infinitas soluciones (solución paramétrica).
  - Incompatible             -> sin solución.

Toda la lógica del algoritmo vive en gauss.py (sin input/print). Este
archivo solo se encarga de la interacción con el usuario por consola.

Uso:
    python3 main.py
"""

from gauss import (
    clasificar,
    copiar_matriz,
    crear_matriz_aumentada,
    escalonar,
    evaluar_solucion_parametrica,
    reducir_a_escalonada_reducida,
    solucion_parametrica,
    sustitucion_regresiva,
    valor_casi_cero,
    verificar_solucion,
)


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
            fila.append(pedir_flotante(f"  Coeficiente de x{j + 1}: "))
        b = pedir_flotante(f"  Término independiente (b{i + 1}): ")
        coeficientes.append(fila)
        terminos.append(b)

    return coeficientes, terminos, m, n


def formatear_numero(valor):
    """Formatea un flotante como entero si es (casi) un entero, o con 4 decimales."""
    redondeado = round(valor)
    if valor_casi_cero(valor - redondeado):
        return str(int(redondeado))
    return f"{valor:.4f}"


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


def imprimir_verificacion(coeficientes, terminos, x, titulo="Verificación (sustituyendo en el sistema original)"):
    """
    Sustituye 'x' en el sistema original [coeficientes | terminos] y muestra,
    ecuación por ecuación, el valor calculado vs. el esperado, y si coinciden.
    """
    print(f"\n--- {titulo} ---")
    resultados = verificar_solucion(coeficientes, terminos, x)
    todo_coincide = True
    for i, (valor_calculado, valor_esperado, coincide) in enumerate(resultados):
        estado = "OK" if coincide else "NO coincide"
        if not coincide:
            todo_coincide = False
        print(
            f"  Ecuación {i + 1}: {formatear_numero(valor_calculado)} "
            f"(esperado {formatear_numero(valor_esperado)})  ->  {estado}"
        )
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
    columnas_pivote = escalonar(matriz, n, registrar_paso=registrar)

    if not pasos:
        print("(La matriz ya estaba en forma escalonada, no hizo falta ninguna operación.)")
    for descripcion, matriz_paso in pasos:
        imprimir_matriz(matriz_paso, n, f"\nPaso: {descripcion}")

    imprimir_matriz(matriz, n, "\nForma escalonada final:")

    tipo = clasificar(matriz, n, columnas_pivote)

    print("\n--- Clasificación del sistema ---")
    if tipo == "incompatible":
        print("Sistema INCOMPATIBLE: no tiene solución.")
        print("(Una fila quedó de la forma 0 = c, con c distinto de 0.)")

    elif tipo == "determinado":
        print("Sistema COMPATIBLE DETERMINADO: tiene solución única.")
        x = sustitucion_regresiva(matriz, n, columnas_pivote)
        print("\nSolución:")
        for j in range(n):
            print(f"  x{j + 1} = {formatear_numero(x[j])}")

        imprimir_verificacion(coeficientes, terminos, x)

    else:
        print("Sistema COMPATIBLE INDETERMINADO: tiene infinitas soluciones.")

        pasos_rref = []

        def registrar_rref(descripcion, matriz_actual):
            pasos_rref.append((descripcion, copiar_matriz(matriz_actual)))

        print("\n--- Reducción adicional a forma escalonada reducida ---")
        print("(para expresar la solución en función de las variables libres)")
        reducir_a_escalonada_reducida(matriz, n, columnas_pivote, registrar_paso=registrar_rref)
        for descripcion, matriz_paso in pasos_rref:
            imprimir_matriz(matriz_paso, n, f"\nPaso: {descripcion}")

        libres, expresiones = solucion_parametrica(matriz, n, columnas_pivote)

        nombres_libres = [f"x{v + 1}" for v in libres]
        print("\nVariables libres (parámetros):", ", ".join(nombres_libres))

        print("\nSolución paramétrica:")
        for v in range(n):
            if v in libres:
                indice_parametro = libres.index(v) + 1
                print(f"  x{v + 1} = t{indice_parametro}   (variable libre)")
            else:
                termino, partes = expresiones[v]
                texto = formatear_numero(termino)
                for coef, indice_libre in partes:
                    signo = "+" if coef >= 0 else "-"
                    indice_parametro = libres.index(indice_libre) + 1
                    texto += f" {signo} {formatear_numero(abs(coef))}*t{indice_parametro}"
                print(f"  x{v + 1} = {texto}")

        valores_ejemplo = [0.0] * len(libres)
        x_ejemplo = evaluar_solucion_parametrica(n, libres, expresiones, valores_ejemplo)
        asignaciones = ", ".join(
            f"t{k + 1} = {formatear_numero(v)}" for k, v in enumerate(valores_ejemplo)
        )
        titulo = f"Verificación con un ejemplo concreto ({asignaciones})"
        imprimir_verificacion(coeficientes, terminos, x_ejemplo, titulo)


def main():
    while True:
        coeficientes, terminos, m, n = leer_sistema()
        resolver_sistema(coeficientes, terminos, n)

        respuesta = input("\n¿Deseas resolver otro sistema? (s/n): ").strip().lower()
        if respuesta != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
