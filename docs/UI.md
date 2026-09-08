# UI.md — Diseño visual y notación de la interfaz

Recoge las decisiones de la pasada de UI (issues #24 y #25): diseño plano sin
degradados, un único color de acento con contraste AA y notación matemática con
subíndices Unicode consistente en consola y GUI.

## 1. Paleta (flat design)

Se eliminaron todos los `qlineargradient` de `ui/theme.py`. La paleta usa **un
acento** (`#1f4e79`, azul tinta) para acciones primarias, foco y selección;
neutros para el resto; y la jerarquía se marca por tamaño/peso, no por color.

| Rol | Token | Uso |
|-----|-------|-----|
| Acento | `#1f4e79` | botones primarios, `:focus`, ítem de lista seleccionado, hero, encabezados (`#h1`, `#prompt`), cabecera de tabla |
| Acento oscuro | `#173a5c` | `:pressed`, `:hover` de botones fantasma/ayuda, bordes del acento |
| Acento hover | `#2a69a4` | `QPushButton:hover` |
| Texto principal | `#153653` | cuerpo, celdas de matriz, corchetes, `mathrender.COLOR_TEXTO` |
| Texto atenuado | `#41738c` / `#4f6f82` | `#hint`, `#explain`, `#pie` |
| Superficie | `#ffffff` / `rgba(255,255,255,.9)` | tarjetas, inputs, tablas |
| Fondo de ventana | `#dff7ff` | ground de la app (sin cambios en este PR) |
| Estados | `#176b46` ok · `#805900` aviso · `#9f2520` error | siempre con texto descriptivo, sobre fondos desaturados |

### Contraste (WCAG 2.1 AA, texto normal ≥ 4.5:1)

Ratios medidos con la fórmula de luminancia relativa de la W3C:

| Combinación | Ratio |
|-------------|-------|
| Blanco sobre acento `#1f4e79` (botones) | **8.66:1** |
| Blanco sobre `:hover` `#2a69a4` | 5.75:1 |
| Blanco sobre `:pressed` `#173a5c` | 11.7:1 |
| `#153653` sobre fondo de ventana `#dff7ff` | 11.2:1 |
| Subtítulo `#dbe6f2` sobre hero `#1f4e79` | 6.85:1 |
| `#4f6f82` (`#explain` / `#pie`) sobre blanco | 5.4:1 |
| Error `#9f2520` sobre blanco | 7.6:1 |

`mathrender` y los corchetes de la matriz ya usan `#153653`, así que combinan con
la paleta sin cambios.

## 2. Notación con subíndices Unicode

`formato.py` centraliza la notación. `subindice()`, `var()` y `parametro()`
existen desde el PR #21; este PR añade `entrada_A()` / `entrada_b()` y aplica los
cinco helpers en **toda** la salida de texto plano (consola en `main.py`, y en la
GUI `ui/widgets.py`, `ui/state.py`, `ui/screen_process.py`). Donde se renderiza
LaTeX el subíndice ya salía bien y no se toca.

Todos los helpers indexan **desde 0**, igual que los bucles del código:

```python
def subindice(numero):        # 12 -> "₁₂";  "-3" -> "₋₃"
def var(indice, nombre="x"):  # var(0) -> "x₁";  var(2, "E") -> "E₃"
def parametro(indice):        # parametro(0) -> "t₁"
def entrada_A(fila, col):     # entrada_A(0, 0) -> "a₁₁"
def entrada_b(fila):          # entrada_b(0) -> "b₁"
```

Cobertura fijada por `test_formato.py::TestNotacionSubindices`,
`test_ui.py::TestNotacionSubindices` (etiquetas de celda y encabezados de
`MatrizGrid`) y `test_main.py` (solución y solución paramétrica en consola).
