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

Se generan desde la GUI real. De forma reproducible (con el paquete instalado,
`uv sync --extra qt`), desde la raíz del repo:

```bash
uv run python informes/plantilla/generar-capturas.py \
    informes/Informe_Programa_N_Grupo_7/img
```

Renderiza la pantalla "Proceso y resultado" para los tres casos del menú
(única / infinitas / inconsistente), saltando al último paso (forma escalonada
final / RREF), y guarda `caso1-unica.png`, `caso2-libres.png`,
`caso3-inconsistente.png`.

Para tomarlas a mano: `uv run aqua-gauss` → menú → "Ejemplo rápido" → el caso →
recorrer los pasos con `→`.
