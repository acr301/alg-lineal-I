# ADR-0001 · Normalización de la entrada numérica del usuario

**Estado:** aceptada · **Fecha:** 2026-09-01 · **Ámbito:** GUI (`ui/screen_input.py`) y presentación (`formato.py`)

## Contexto

La calculadora acepta que el usuario teclee cada término de la matriz aumentada.
La *misma* cantidad se puede escribir de muchas formas:

```
19/3      6.3333      6.333333333      633/100      63333/10000      6.33
```

Sin una política clara:

- unas entradas se guardan como fracción "bonita" (`19/3`) y otras como fracción
  fea (`63333/10000`), que además aparecería en cada paso de la eliminación;
- el usuario no sabe cuántos decimales "cuentan";
- dos personas que teclean lo mismo obtienen pantallas distintas.

## Decisión

### 1. Al confirmar un término (`formato.normalizar_entrada`)

1. Se interpreta el texto: enteros, decimales con `.` o `,`, y también `p/q`.
2. Si el valor está **a menos de `1e-4`** de una fracción cuyo **denominador
   reducido es ≤ `MAX_DEN_DISPLAY` (= 64)**, se ajusta a esa fracción exacta.
   → `6.3333`, `6.333333333`, `19/3` ⇒ **19/3**;  `0.3333` ⇒ **1/3**.
   (Un `0.333` con sólo 3 cifras queda a más de `1e-4` de `1/3`, así que **no**
   se ajusta: se toma como `0.333`.)
3. Si no, se **redondea a `DECIMALES_ENTRADA` (= 4)** decimales.
   → `6.33` ⇒ `6.33`;  `√2` ⇒ `1.4142`.

### 2. Al mostrar cualquier número (`formato.formatear_valor`, modo fracción)

Se muestra como fracción **solo si el denominador reducido es ≤ 64**; en otro
caso, decimal con 4 cifras. Así la entrada y la salida son coherentes: lo que se
teclea como "≈ 19/3" se ve siempre `19/3`, y lo que no encaja en una fracción de
denominador chico se ve siempre con 4 decimales.

### 3. El cálculo no cambia

`gauss.py` sigue operando en `float`. Las fracciones son una *representación* del
`float` almacenado, no un tipo numérico nuevo (se respeta la restricción de no
usar `fractions`).

## Consecuencias

- **+** Entrada consistente e idempotente: re-teclear el valor mostrado no lo altera.
- **+** Los pasos de la eliminación no se llenan de fracciones de 5 cifras.
- **+** Cubre los recíprocos "de a mano" (`/2 /3 /4 … /64`).
- **−** Un valor legítimo con denominador > 64 (p. ej. `7/128`) se ve como decimal.
- **−** El umbral `1e-4` puede "enganchar" `6.3333` a `19/3` aunque el usuario
  quisiera exactamente `6.3333`; se consideró aceptable porque a esa distancia casi
  siempre se está aproximando la fracción.

## Parámetros

En `formato.py`: `MAX_DEN_DISPLAY = 64`, `DECIMALES_ENTRADA = 4`. Cambiarlos ajusta
a la vez la normalización de entrada y el criterio de mostrar fracción.
