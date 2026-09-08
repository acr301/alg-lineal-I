# Informe — Programa 2 (Grupo 7)

Plantilla LaTeX del informe documental de la **Tarea 2** (Reducción a RREF por
Gauss-Jordan e identificación de columnas pivote). La portada y la estructura se
replicaron del `Informe_Programa_1_Grupo_7.pdf` (hecho en Word) para que las
entregas siguientes reutilicen la misma base.

## Compilar

```bash
cd informes/Informe_Programa_2_Grupo_7
pdflatex informe.tex && pdflatex informe.tex   # dos veces por el índice
# o:  latexmk -pdf informe.tex
```

Genera `informe.pdf`. Renombrar la copia final a **`Informe_Programa 2_Grupo 7.pdf`**
para la entrega en Moodle.

## Pendiente antes de entregar

1. **Capturas de pantalla** (`img/`): ejecutar `uv run aqua-gauss` y capturar la
   pantalla "Proceso y resultado" para cada caso. Guardar como:
   - `img/caso1-unica.png` — sistema con solución única
   - `img/caso2-libres.png` — sistema con variables libres / infinitas soluciones
   - `img/caso3-inconsistente.png` — sistema inconsistente

   Sistemas sugeridos (ya descritos en el `.tex`, coinciden con los ejemplos del menú):
   | Caso | Matriz `[A | b]` |
   |------|------------------|
   | única | `[[1,1,1,6],[0,2,5,-4],[2,5,-1,27]]` |
   | libres | `[[1,1,1,6],[2,2,2,12],[1,-1,0,0]]` |
   | inconsistente | `[[1,1,2],[1,1,5]]` |

   Mientras falten, el `.tex` compila igual y deja un recuadro **[PENDIENTE]** en su lugar.
2. **Logo UAM**: `img/uam-logo.png` (mismo escudo del informe 1). Sin él, la
   portada muestra un recuadro con el nombre del archivo.
3. **Integrantes**: editar `\integrantes` en el preámbulo del `.tex`. Hoy están
   Andrés Castillo y Fátima Zogaib; confirmar si el Grupo 7 suma a Roberto Macías
   y Reynaldo Molina (ya añadidos como colaboradores del repo).
4. **Fecha**: `\ciudadFecha` usa `\today`; fijarla a la fecha de entrega si hace falta.

## Editar entre entregas

Todo lo variable está en el preámbulo (`\programaTitulo`, `\grupoNum`, `\docente`,
`\integrantes`, `\ciudadFecha`). Para el Programa 3 se copia esta carpeta, se
cambia ese bloque, la sección "Explicación del algoritmo" y las 3 capturas.
