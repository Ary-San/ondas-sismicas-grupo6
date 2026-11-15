# Ondas sísmicas superficiales — Grupo 6 (Óptica y Ondas, UTEC)

Proyecto: **Ondas sísmicas superficiales: modos de Rayleigh, dispersión e inversión del subsuelo**
Docentes: Marco Cuyubamba y Eduardo Castillo

## Póster

- Resultado actual (Canva): https://www.canva.com/design/DAHa8PVsbuA/o3pMXsLm-Zl38e6yMF44YA/edit
- PDF de referencia: `poster_A0.pdf` (841×1189 mm, fuente Source Sans 3 — ya verificado)

## Estado del póster (revisado)

Cobertura de las 6 actividades obligatorias del enunciado: completa, salvo un punto parcial.

| # | Actividad | Estado |
|---|---|---|
| 1 | P, S, Rayleigh + esquema | ✅ |
| 2 | Potenciales escalar/vectorial → vP, vS | ✅ |
| 3 | Condiciones de frontera → ecuación secular | ✅ |
| 4 | Por qué cR<vS<vP; variación con h y vS | ⚠️ se usa la desigualdad pero no se justifica por qué se cumple |
| 5 | vg vs vf | ✅ (con validación cuantitativa contra el solver `disba`) |
| 6 | Simulación cR(f), vg(f) variando h y vS | ✅ (Modelo A vs Modelo B) |

Pendientes señalados en conversación previa:
- Nombres de los integrantes (placeholder en el póster).
- QR: opcional, no exigido por el enunciado. Si se agrega, lo más útil es apuntar al repo de este código.
- Reforzar la justificación de `cR < vS < vP` (actividad 4).

## Script de simulación (pendiente de escribir)

El póster usa `disba` (método de Dunkin) para generar las curvas de dispersión de los
Modelos A y B (Fig. 2 y 3 del póster) y las pruebas de sensibilidad aisladas (variar solo
`h` o solo `vS` desde el Modelo A). Falta el script que:

1. Define los dos modelos estratificados (capa + semiespacio) usados en el póster:
   - Modelo A: capa de 10 m, vp=600, vs=200, ρ=1800 sobre semiespacio vp=1300, vs=650, ρ=2100.
   - Modelo B: capa de 20 m, vp=600, vs=300, ρ=1800 (mismo semiespacio).
2. Calcula `cR(f)` y `vg(f)` para el modo fundamental de Rayleigh (1–60 Hz) con `disba`.
3. Reproduce las pruebas de sensibilidad aisladas desde el Modelo A (solo cambiar `h` a 20 m,
   solo cambiar `vS` a 300 m/s) reportadas en el póster.
4. Exporta las curvas como SVG/PNG vectorial para reemplazar los paneles del póster si hace falta.

## Requisitos del curso

Ver el documento original `TD2_Teo11_Proyectos&Grupos.pdf` (Grupo 6, página 6) para el enunciado completo.
