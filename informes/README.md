# Informes de las entregas (Programa N)

Cada "Programa N" del Proyecto Integrador lleva un informe en PDF además del
código. Aquí vive **solo la plantilla reutilizable**; los informes concretos
(con nombres legales y capturas) y los PDF compilados **no se versionan**.

## Qué se versiona y qué no

| | |
|---|---|
| ✅ `plantilla/informe.tex` | Portada + estructura + secciones. Reutilizable entre entregas. |
| ✅ `plantilla/datos.example.tex` | Guía de con qué rellenar `datos.tex`. |
| ✅ este `README.md` | |
| 🚫 `datos.tex` | Nombres legales, grupo, docente, fecha — **local**, en `.gitignore`. |
| 🚫 `Informe_Programa_*/` | Carpeta de trabajo de cada entrega (copia de `plantilla/` + `datos.tex` + `img/`). |
| 🚫 `*.pdf`, `img/*` | El entregable compilado y sus capturas / el logo. |

## Preparar una entrega

```bash
cd informes
cp -r plantilla Informe_Programa_N_Grupo_7
cd Informe_Programa_N_Grupo_7

cp datos.example.tex datos.tex        # y editar: título, integrantes (nombres LEGALES), fecha
cp /ruta/al/uam-logo.png img/uam-logo.png

# adaptar la sección "Explicación del algoritmo" y los 3 casos en informe.tex
# poner las capturas:  img/caso1-unica.png  img/caso2-libres.png  img/caso3-inconsistente.png

pdflatex informe.tex && pdflatex informe.tex   # dos veces, por el índice
mv informe.pdf "Informe_Programa N_Grupo 7.pdf"
```

Si falta `datos.tex` la plantilla compila igual, con placeholders `[...]`.
Si falta una captura, deja un recuadro **[PENDIENTE]** en su sitio.

## Capturas

Se generan de la GUI **real** (backend nativo de macOS, tema y render de la app),
de forma reproducible. Con el paquete instalado (`uv sync --extra qt`), desde la
raíz del repo:

```bash
uv run python informes/plantilla/generar-capturas.py \
    informes/Informe_Programa_N_Grupo_7/img
```

Por cada caso del menú (única / infinitas / inconsistente) deja dos PNG:

| archivo | pantalla |
|---|---|
| `casoN-proceso.png` | "3 · Proceso y resultado" en el último paso (RREF / forma escalonada final) |
| `casoN-vectorial.png` | "4 · Solución en notación vectorial" |

El script usa `QWidget.grab()` (los mismos píxeles que pinta la app, sin la barra
de título del sistema): es determinista y no necesita permiso de *Grabación de
pantalla*. Para tomarlas a mano en su lugar: `uv run aqua-gauss` → menú →
"Ejemplo rápido" → el caso → `→` hasta el último paso, luego `Enter`.
