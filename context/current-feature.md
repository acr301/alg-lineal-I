# Current Feature: LaTeX renderizado, verificación explícita y fracciones

## Status

In Progress — implementado en `fix/latex-renderizado-fracciones-verificacion`,
pendiente de PR/merge.

## Goals

- [x] **Notación matemática renderizada en la GUI (#15).** Resultado con subíndices
  `x₁`, signo `−`, `·` y vectores columna entre corchetes (rich-text de Qt, sin
  dependencias). Análisis de rango/nulidad y código LaTeX movidos a un `QDialog`
  ("Ver análisis y LaTeX ↗"); el panel "3 · Proceso y resultado" queda más limpio.
- [x] **Demostración de la comprobación sustituyendo valores (#16).**
  `verificar_solucion_detallada()` en `gauss.py` expone los términos `coef·xⱼ`;
  consola y GUI muestran `1·(5) + 1·(3) + 1·(-2) = 5 + 3 − 2 = 6 = 6`.
  `verificar_solucion()` pasa a ser vista resumida de la detallada.
- [x] **Matriz en fracción exacta en el paso a paso y tablas (#17).** `formato.py`
  con `a_fraccion()` (fracción continua) / `mcd()` (Euclides) / `formatear_valor()`,
  sin `import`. Matriz, pasos, forma final, vectores y verificación en fracción por
  defecto; toggle "Fracción ⇄ Decimal" en la GUI y `--decimal/--fraccion` en consola.
- [x] `main.py` y `gui.py` dejan de duplicar `format_number`; usan `formato.py`.
  `generar_latex_solucion()` movida de `gauss.py` a `formato.py` (usa `\frac`;
  corregido el bug que borraba los ceros de `x_p`).
- [x] Tests nuevos: `test_formato.py` (11) + `TestVerificarSolucionDetallada` en
  `test_gauss.py`. Suite: 35 tests en verde (`uv run --extra dev pytest`).
- [x] Documentación actualizada (`README.md`, `AGENTS.md`, `docs/ARQUITECTURA.md`,
  `docs/ALGORITMO.md`).
- [x] **2ª iteración (feedback):** render real de LaTeX con `mathrender.py`
  (matplotlib mathtext → `QPixmap`); el diálogo "Ver análisis y LaTeX" ahora
  muestra la solución y la comprobación como imágenes matemáticas. Rango/nulidad/
  forma en lista con signos `?` (tooltips explicativos). Botón "Cerrar". Fuente sin
  "Segoe UI" (quitaba el warning de Qt en macOS). `matplotlib` añadido a
  `pyproject.toml` (solo render; `gauss.py`/`formato.py` siguen sin imports).
  Degradación elegante si matplotlib no está (`mathrender.disponible()`).
- [x] **3ª iteración (feedback):**
  - GUI reescrita como paquete `ui/` con flujo de 5 pantallas (menú, dimensiones,
    entrada guiada término a término, proceso, solución vectorial), navegable con
    teclado (Enter/Esc/←→/F1). `gui.py` queda como shim.
  - El multiplicador de cada paso se muestra como fracción: `gauss.escalonar` /
    `reducir_a_escalonada_reducida` aceptan `formato_numero`; lo usan `ui/state.py`
    y `main.py`.
  - `mathrender.matriz_a_pixmap()` para render de matrices; los pasos y la
    solución vectorial se ven renderizados. Sin matplotlib no se muestra LaTeX
    crudo (cae a texto/HTML); aviso al arrancar + docs piden `uv run python gui.py`.
  - Tooltips con `QToolButton` (funcionan con ratón y teclado). Fuente elegida por
    código → sin warning "missing font family".
  - Código LaTeX oculto tras "Ver sintaxis LaTeX" en la última pantalla; la
    comprobación ya no se repite ahí (está en "Proceso y resultado").
- [x] **4ª iteración (feedback):**
  - Rama renombrada a `feature/gui-multipantalla-y-notacion-matematica`.
  - Contenido de todas las pantallas en una columna centrada (máx. 820 px), no de
    borde a borde; encabezados centrados.
  - Menú: la info (autores/licencia/repo/método) baja a un pie pequeño.
    **Autores: Andrés Castillo y Fátima Zogaib (Grupo 7)** (también en `pyproject`).
  - Bug corregido: Enter elegía nada en las listas del menú →
    `ui/widgets.ListaOpciones` (emite en Return/Enter, no sólo `itemActivated`).
  - Elegir un ejemplo salta directo a "Proceso y resultado" (`sesion.origen`);
    "Atrás" desde ahí vuelve al menú.
  - Entrada de términos: campo estrecho y centrado (no de lado a lado).
  - **ADR-0001** (`docs/ADR-0001-entrada-numerica.md`): `formato.normalizar_entrada`
    ajusta lo tecleado a una fracción tidy (den ≤ 64) o a 4 decimales; el mismo
    tope rige qué se muestra como fracción. `6.3333`, `19/3` ⇒ `19/3`; `6.33` ⇒ `6.33`.
- [ ] Abrir PR y mergear a `main` (pendiente de confirmación del usuario).

## Notes

- Issues: #15 (LaTeX renderizado + declutter), #16 (verificación sustituyendo
  valores), #17 (fracciones), #18 (migración a Textual TUI — solo issue/investigación,
  no se implementa en esta rama).
- Rama: `fix/latex-renderizado-fracciones-verificacion`.
- Restricción vigente: `gauss.py` sin librerías externas ni stdlib. El helper de
  fracciones vive en `formato.py` (capa de presentación) y también evita `import`
  para mantener el espíritu del ejercicio.
- El algoritmo sigue trabajando en `float`; las fracciones son solo presentación.

## History

### Solución Vectorial, Rango, Nulidad, LaTeX y Formas Escalonadas (semana2/tarea1)

Implementa análisis avanzado de sistemas lineales en `gauss.py` sin librerías externas:
- `rango_matriz()` calcula el rango de una matriz
- `verificar_rango_nulidad()` verifica Rango(A) + Nulidad(A) = n
- `es_forma_escalonada()` y `es_forma_escalonada_reducida()` detectan REF/RREF
- `clasificar_forma_escalonada()` clasifica la forma escalonada
- `solucion_general_vectorial()` expresa soluciones como x = xp + t1*v1 + ... + tk*vk
- `generar_latex_solucion()` genera código LaTeX copiable

Integración en `main.py`: muestra rango, nulidad, forma escalonada y solución vectorial.
Interfaz PyQt6 en `gui.py`: panel de análisis avanzado con QTextEdit para LaTeX y botón "Copiar LaTeX".
Tests exhaustivos: 18 nuevos tests en `test_gauss.py` (todos pasan).
Mergeado a `main` (rama `feature/solucion-vectorial-rango-latex-formas` eliminada).

### Verificación Explícita de la Solución (semana2/tarea1)

Agrega `verificar_solucion()` y `evaluar_solucion_parametrica()` a `gauss.py` (sin
librerías) para sustituir la solución hallada en el sistema original `[A | b]` y
comprobar la igualdad, tal como exige el enunciado de la Tarea 1. `main.py` ahora
muestra esta comprobación ecuación por ecuación tras imprimir la solución, tanto para
sistemas determinados (solución única) como indeterminados (con un valor concreto de
ejemplo para los parámetros libres). No aplica al caso inconsistente. Tests agregados en
`test_gauss.py`. Cierra el issue acr301/alg-lineal-I#3. Mergeado a `main` (rama
`feature/verificacion-explicita-solucion` eliminada).

### Eliminación Gaussiana Interactiva (semana2/tarea1)

Programa interactivo en Python (`semana2/tarea1/`) que resuelve sistemas Ax=b mediante
eliminación de Gauss con pivoteo parcial (reducción a forma escalonada), implementado sin
numpy ni ninguna función de álgebra lineal ya dada en Python (solo listas, bucles y
aritmética básica). Muestra cada paso de la reducción, clasifica el sistema (compatible
determinado / indeterminado con solución paramétrica / incompatible), e incluye tests
(`test_gauss.py`) para la lógica pura. Mergeado a `main` (rama
`feature/eliminacion-gaussiana-interactiva` eliminada). Pendiente: interfaz gráfica con
PyQt (fuera de alcance de este feature).
