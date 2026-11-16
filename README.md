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
- Reforzar la justificación de `cR < vS < vP` (actividad 4).

### Maqueta con las correcciones de la Etapa A

`maqueta/maqueta_etapaA.pdf` (A0) aplica las correcciones obligatorias de la auditoría:
Navier → vp, vs; componentes ux, uz y la elipse; σ en función de los potenciales y la matriz M;
justificación de cR < vs < vp; Fig. 1 nueva calculada con las ecs. (4)–(5) (`maqueta/fig1_rayleigh.svg`).
`maqueta_etapaA_anotada.pdf` marca cada cambio. Pendiente: nombres de integrantes y confirmar "TEMA 37"
(no figura en el enunciado).

Regenerar: `cd maqueta/src && npm install && cp ../../assets/qr_repo.png . && python3 fig1.py > fig1.svg && node build.mjs`

### QR del póster

`assets/qr_repo.png` apunta a este repositorio (`https://github.com/Ary-San/ondas-sismicas-grupo6`),
donde está el script de simulación (`scripts/dispersion.py`) que generó las curvas de dispersión
del póster. Insertarlo en una esquina del póster (p. ej. junto a las referencias).

## Script de simulación

`scripts/dispersion.py` usa `disba` (método de Dunkin) para generar las curvas de dispersión
del modo fundamental de Rayleigh, `cR(f)` y `vg(f)` (1–60 Hz), para:

- **Modelo A**: capa de 10 m, vp=600, vs=200, ρ=1800 sobre semiespacio vp=1300, vs=650, ρ=2100.
- **Modelo B**: capa de 20 m, vp=600, vs=300, ρ=1800 (mismo semiespacio).
- **Sensibilidad aislada (solo h)**: Modelo A con h=20 m (vS sin cambiar).
- **Sensibilidad aislada (solo vS)**: Modelo A con vS=300 m/s (h sin cambiar).

Uso:

```bash
pip install -r requirements.txt
python3 scripts/dispersion.py
```

Genera en `outputs/`: un CSV por modelo (`f_Hz_fase,cR_mps,f_Hz_grupo,vg_mps`) y tres figuras
PNG (Modelo A vs B, sensibilidad a `h`, sensibilidad a `vS`) listas para comparar con los
paneles del póster o reemplazarlos si hace falta.

## Requisitos del curso

Ver el documento original `TD2_Teo11_Proyectos&Grupos.pdf` (Grupo 6, página 6) para el enunciado completo.
