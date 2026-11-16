# Auditoría matemática, física y numérica — Póster Grupo 6

**Objeto auditado:** `maqueta/maqueta_etapaBC.pdf` (ecs. 1–10, Figs. 1–6, textos y conclusiones). Las
observaciones marcadas **[orig.]** también se aplican al póster original `poster_A0.pdf`.
**Evidencia reproducible (esta carpeta):**
- `simbolico.py`: sympy, 23 comprobaciones de las ecs. 1–9.
- `solver_mp.py`: solver propio de capa sobre semiespacio. Usa una matriz global 6×6 real y mpmath con 40 dígitos. No usa disba.
- `numerico.py`, `extra.py`, `inv_check.py`: comparan contra disba y contra las cifras del póster. Resultados en `numerico.json`.

## 1. Diagnóstico general
- **Derivaciones (1)–(9):** todas son exactas. Las rederivé de forma simbólica desde la ley de Hooke y la ecuación de Navier, sin partir de las fórmulas del póster.
- **Valores de c<sub>R</sub>:** el solver independiente los reproduce con diferencias ≤ 0,0003 m/s en 24 casos (4 modelos × 6 frecuencias).
- **Errores encontrados:** ninguno crítico ni alto.
  - **Medios (5):** frecuencia de la fase de Airy mal redondeada [orig.], atribución invertida del error de v<sub>g</sub> [orig.], curvas de v<sub>g</sub> con el sesgo de disba, definición incompleta del "% de sensibilidad" y relación A–B omitida en (4)–(5).
  - **Bajos (5):** argumento de unicidad incompleto, "0,93 v<sub>s</sub>" presentado como general, convención de ejes no declarada, notación de (A, B) y resolución de la inversión.

**Dictamen: VALIDADO CON OBSERVACIONES. Nota: 87/100.**

## 2. Inventario examinado
| Ítem | Ubicación | Verificación |
|---|---|---|
| (1) Navier | Col. 1 | Simbólica: residuo 0 en x y en z |
| (2) ondas desacopladas, v<sub>p</sub>, v<sub>s</sub> | Col. 1 | ∇·u = ∇²φ; ∇×∇×(ψŷ) = −∇²ψ ŷ, porque ∂<sub>y</sub> = 0 |
| (3) φ, ψ, q², s² | Col. 1 | Ambas ecuaciones de onda se cumplen exactamente |
| (4)–(5) u<sub>x</sub>, u<sub>z</sub> | Col. 1 | Exactas con B = −2ikqA/(k²+s²) |
| z<sub>rev</sub> = ln[(k²+s²)/2qs]/(q−s) | Mockup A | u<sub>x</sub>(z<sub>rev</sub>) = 10⁻¹⁶ (numérico) |
| (6) σ<sub>zz</sub>, σ<sub>xz</sub> | Col. 1 | Iguales a Hooke: σ<sub>ij</sub> = λδ<sub>ij</sub>∇·u + 2με<sub>ij</sub> |
| (7) matriz M | Col. 1 | Las 4 entradas coinciden |
| det M; (8) | Col. 1 | det M = 4k²qs − (k²+s²)²; (8) = −det M/k⁴ |
| Raíz ξ, 606,1 m/s | Col. 1–2 | ξ = 0,932526; c<sub>R</sub> = 606,1418 m/s |
| (9) v<sub>g</sub> | Col. 3 | Exacta |
| (10) χ | Col. 3 | Adimensional y bien definida |
| Fig. 1: H/V, 0,17 Λ, sentido de giro | Col. 1 | 0,639; 0,173 Λ; retrógrado arriba (comprobado con aserción) |
| Fig. 2: Vs30 | Col. 2 | 371,43 y 365,63 m/s |
| Fig. 3: asíntotas, Airy | Col. 2 | Asíntotas ✓; Airy ✗ (E1) |
| Fig. 4: f·h | Col. 2 | c(f; 20 m) = c(2f; 10 m) exactamente |
| Fig. 5: fracciones | Col. 3 | 9,7 / 79,6 / 97,9 / 100 % ✓; definición incompleta (E4) |
| Fig. 6: χ, rangos | Col. 3 | χ idéntico con el solver independiente |

## 3. Auditoría dimensional
| Variable | Significado | Unidad SI | Verificación |
|---|---|---|---|
| λ, μ | Parámetros de Lamé | Pa = kg m⁻¹ s⁻² | ✓ |
| ρ | Densidad | kg m⁻³ (la tabla usa kg/m³; disba, g/cm³ ÷ 1000) | ✓ |
| v<sub>p</sub>, v<sub>s</sub>, c<sub>R</sub>, v<sub>g</sub> | Velocidades | m s⁻¹ | √(Pa / kg m⁻³) = m/s ✓ |
| ω; f | Frecuencia angular; frecuencia | rad s⁻¹; Hz | ✓ |
| k, q, s | Números de onda | m⁻¹ | Los argumentos qz, sz y kx − ωt son adimensionales ✓ |
| φ, ψ (A, B) | Potenciales | m² | u = ∇φ → m ✓ |
| u<sub>x</sub>, u<sub>z</sub> | Desplazamientos | m | ✓ |
| σ | Esfuerzo | Pa | λ∇²φ: Pa·m²/m² ✓ |
| Filas de M | — | m⁻² (tras dividir por μE) | Homogéneas ✓ |
| ξ, β, χ, H/V | — | Adimensionales | ✓ |
| Λ | Longitud de onda (no es la λ de Lamé) | m | Λ = c<sub>R</sub>/f ✓ |
| V<sub>s30</sub> | Velocidad promedio | m s⁻¹ | 30 / Σ(h/v): m / (m/(m/s)) ✓ |

Todas las ecuaciones son dimensionalmente homogéneas.

**Notación (E8):** el póster BC no declara explícitamente que el medio ocupa z ≥ 0, que z apunta hacia el interior y que (x, y, z) es un sistema dextrógiro. Las dos cosas fijan el signo de ∇×(ψŷ) y el decaimiento de e^(−qz). El original sí dice "z ≥ 0".

## 4. Velocidades P y S
- **Fórmulas:** v<sub>p</sub> = √((λ+2μ)/ρ) y v<sub>s</sub> = √(μ/ρ) son correctas. El póster no da λ ni μ numéricos; las velocidades son datos de entrada, así que no hay sustituciones que verificar.
- **Relación P/S:** v<sub>p</sub>²/v<sub>s</sub>² = 2 + λ/μ.
- **Estabilidad:** exige μ > 0 y K = λ + 2μ/3 > 0, de donde v<sub>p</sub>/v<sub>s</sub> > √(4/3) = 1,1547. El póster dice "> 1,15" ✓.
- **Modelos:** v<sub>p</sub>/v<sub>s</sub> vale 3 (capa A), 2 (capa B) y 2 (semiespacio), todos admisibles.
- **Coeficiente de Poisson:**
  - Para v<sub>p</sub>/v<sub>s</sub> = 3: ν = 7/16 = 0,4375.
  - Para v<sub>p</sub>/v<sub>s</sub> = 2: ν = 1/3.
  - El póster dice "ν 0,44 → 0,33" ✓.

## 5. Potenciales y desplazamientos
- **Rotacional:** ∇×(ψŷ) = (−∂<sub>z</sub>ψ, 0, ∂<sub>x</sub>ψ). Por tanto u<sub>x</sub> = ∂<sub>x</sub>φ − ∂<sub>z</sub>ψ y u<sub>z</sub> = ∂<sub>z</sub>φ + ∂<sub>x</sub>ψ ✓.
- **Componentes con potenciales:**
  - u<sub>x</sub> = (ikAe^(−qz) + sBe^(−sz))E
  - u<sub>z</sub> = (−qAe^(−qz) + ikBe^(−sz))E
- **Relación A–B:** al sustituir B = −2ikqA/(k²+s²) (fila 2 de (7)) se obtienen exactamente (4) y (5).
  - Con la fila 1 se obtiene otro B. La diferencia entre ambos es proporcional a det M, así que coinciden solo sobre la raíz secular (comprobado).
  - **(E5):** el póster BC no dice qué relación usa. Hay que escribirla.
- **Decaimiento:**
  - q² = k² − ω²/v<sub>p</sub>² y s² = k² − ω²/v<sub>s</sub>² satisfacen las ecuaciones de onda.
  - Hay decaimiento si q y s son reales positivos, es decir, c < v<sub>s</sub> < v<sub>p</sub>, con la rama positiva de la raíz.
  - No hay crecimiento exponencial no físico.

## 6. Elasticidad y esfuerzos
- **Deformaciones:** ε<sub>zz</sub> = ∂<sub>z</sub>u<sub>z</sub> y ε<sub>xz</sub> = ½(∂<sub>z</sub>u<sub>x</sub> + ∂<sub>x</sub>u<sub>z</sub>).
- **σ<sub>zz</sub>:** λ∇·u + 2μ∂<sub>z</sub>u<sub>z</sub> = λ∇²φ + 2μ(∂<sub>z</sub>²φ + ∂<sub>x</sub>∂<sub>z</sub>ψ) ✓.
- **σ<sub>xz</sub>:** μ(2∂<sub>x</sub>∂<sub>z</sub>φ + ∂<sub>x</sub>²ψ − ∂<sub>z</sub>²ψ) ✓.
- Las dos coinciden simbólicamente con la ley de Hooke.

## 7. Condiciones de frontera y matriz M
Evaluando en z = 0 y dividiendo por μE:
- **Fila 1, coeficiente de A:** [λ(q²−k²) + 2μq²]/μ = k² + s². La identidad se verificó simbólicamente: con λ = ρv<sub>p</sub>² − 2μ se obtiene −ρω² + 2μk² = μ(2k² − ω²/v<sub>s</sub>²).
- **Fila 1, coeficiente de B:** 2(ik)(−s) = −2iks ✓.
- **Fila 2:** 2(ik)(−q) = −2ikq y (−k²) − s² = −(k²+s²) ✓.
- **Determinante:** det M = −(k²+s²)² − (−2iks)(−2ikq) = 4k²qs − (k²+s²)² ✓.
- **Notación (E9):** "A, B ≠ 0" debe escribirse "(A, B) ≠ (0, 0)". Sobre la raíz ambas son no nulas de todos modos, porque B ∝ A.

## 8. Ecuación secular
- **Adimensionalización:** s/k = √(1−ξ²) y q/k = √(1−βξ²). Con eso, det M/k⁴ = 0 equivale exactamente a (8) ✓.
- **Forma racionalizada** (X = ξ²): X·[X³ − 8X² + (24−16β)X − 16(1−β)] = 0.
  - Para β = 1/4: X = 0,8696 → ξ = 0,93253. Las otras dos raíces son complejas, 3,565 ± 1,043i.
  - Para β = 1/9: ξ = 0,94731.
- **Raíces físicas:**
  - Semiespacio: c<sub>R</sub> = 606,142 m/s.
  - Capa A: 189,462 m/s.
  - Capa B: 279,758 m/s.
  - Todas cumplen c<sub>R</sub> < v<sub>s</sub> < v<sub>p</sub>.
- **Existencia de la raíz:** R(ξ) ≈ −2(1−β)ξ² para ξ → 0 (desarrollo comprobado) y R(1) = 1.
- **Unicidad (E6):** el teorema del valor intermedio solo prueba que existe una raíz, no que sea única. La unicidad es cierta: la comprobé numéricamente para 300 valores de β en (0, 3/4) y siempre hay exactamente una raíz en (0, 1). Hay que corregir la frase o citar la prueba.
- **Generalidad (E7):** "c<sub>R</sub> ≈ 0,93 v<sub>s</sub>" vale para v<sub>p</sub>/v<sub>s</sub> = 2. Para la capa A es 0,947, y en general varía entre ~0,87 y 0,96 según ν.

## 9. Dispersión
- **Conversiones:** ω = 2πf, k = 2πf/c<sub>R</sub> = 2π/Λ ✓.
- **Medio homogéneo:** (8) no contiene ω, así que c<sub>R</sub> no depende de la frecuencia. El solver con capa igual al semiespacio da 606,1418 m/s a cualquier f ✓.
- **c<sub>R</sub>(f) frente al solver independiente:** diferencias máximas de 0,0003 m/s (A 0,0002; B 0,0001; h20 0,0003; vs300 0,0003).
- **Tolerancia interna de disba:** cambiar `dc` de 0,005 a 0,0005 km/s altera c<sub>R</sub> en 0,0003 m/s.
- **Asíntotas:** c<sub>R</sub>(1 Hz) = 596,74 → 606,14 y c<sub>R</sub>(60 Hz) = 189,462, que es la velocidad de Rayleigh de la capa A ✓.
- **Escala f·h:** con las velocidades y densidades fijas, la relación de dispersión depende solo de kh y c, así que c = F(f·h).
  - Comprobado numéricamente: c(3 Hz; 20 m) = c(6 Hz; 10 m) = 520,8987 m/s.
  - También c(10 Hz; 20 m) = c(20 Hz; 10 m) = 191,6528 m/s.
  - La flecha "f ÷ 2" de la Fig. 4 es exacta.
- **Monotonía:** el solver independiente muestra que c<sub>R</sub> decrece de forma monótona hasta 60 Hz. Los aparentes dc/df ≥ 0 que aparecen con disba (≤ 1,5·10⁻⁴ m/s, por encima de 23 Hz) son cuantización numérica. "v<sub>g</sub> < c<sub>R</sub>" es correcto.

## 10. Velocidad de grupo
- **Fórmula (9):** derivada de k = 2πf/c, da dk/df = (2π/c)(1 − fc′/c). Es exacta.
- **Referencia de alta precisión:** diferencia central con paso de 10⁻⁴ Hz sobre el solver mpmath.

| Punto | Referencia | disba GroupDispersion | (9) con Δf = 0,05 Hz |
|---|---|---|---|
| A, 9,66 Hz | 76,506 | 77,618 (**+1,11**) | 76,530 (+0,02) |
| A, 10 Hz | 81,968 | 82,172 (+0,20) | 81,944 (−0,02) |
| A, 6 Hz | 383,439 | 383,190 (−0,25) | 383,443 |
| B, 6 Hz | 198,213 | 198,559 (+0,35) | 198,306 (+0,09) |

- **Mínimos verdaderos:**
  - A: v<sub>g,mín</sub> = 76,49 m/s a **9,646 Hz** (disba da 77,62 m/s a 9,664 Hz).
  - B: v<sub>g,mín</sub> = 163,29 m/s a **6,636 Hz** (disba da 163,78 m/s a 6,646 Hz).
- **(E1) [orig.]:** "9,7 Hz (A), 6,7 Hz (B)" y "9,7 → 4,8 Hz" deben decir **9,6 Hz, 6,6 Hz y 9,6 → 4,8 Hz**. Por la escala f·h, el valor exacto para 20 m es 9,646/2 = 4,823 Hz, así que "4,8" es correcto.
- **(E2) [orig.]:** "(9) difiere del solver ≤ 1,0 m/s" atribuye el error al revés. El que se desvía hasta 1,1 m/s (1,5 %) es el v<sub>g</sub> interno de disba, que usa diferencias finitas. La fórmula (9) queda dentro de 0,1 m/s de la referencia en los puntos probados.
- **(E3):** las curvas de v<sub>g</sub> de la Fig. 3 usan GroupDispersion. El sesgo no se ve a esa escala, pero es incoherente con E2.
- **"82,0 m/s" a 10 Hz [orig.]:** la referencia da 81,97, así que es correcto.

## 11. Modelos estratificados
- **Estructura:** cada modelo es una capa sobre un semiespacio, con espesores y densidades positivos y v<sub>p</sub>/v<sub>s</sub> admisibles. La tabla y la Fig. 2 son coherentes.
- **Método:** Dunkin, implementado en disba y equivalente a Thomson–Haskell pero estable a alta frecuencia. Mi solver impone por separado la superficie libre, la continuidad de (u<sub>x</sub>, u<sub>z</sub>, σ<sub>zz</sub>, σ<sub>xz</sub>) en z = h y el decaimiento en el semiespacio, y reproduce disba.
- **Modo:** se toma la primera raíz en c > 0,8·min(v<sub>s</sub>), que es el modo fundamental.
- **V<sub>s30</sub>:** 30 / (10/200 + 20/650) = 371,43 m/s y 30 / (20/300 + 10/650) = 365,63 m/s. Ambos en el rango S2 de la E.030 (180–500 m/s).
- **Sensibilidad (E4):** las fracciones en la capa coinciden por tres vías: el kernel de disba, diferencias finitas con disba y diferencias finitas con mi solver (9,7 %, 79,6 %, 97,9 % y 100 %). Pero son fracciones de ∂c<sub>R</sub>/∂v<sub>s</sub> con v<sub>p</sub> y ρ fijos. Si se usa sensibilidad relativa (v<sub>s</sub>·∂c/∂v<sub>s</sub>), dan **3 %, 55 % y 93 %**. La cifra depende de la definición, y el póster debe declararla.
- **Relación frecuencia–profundidad:** la conclusión se apoya en los kernels y no en una regla fija ✓.

## 12. Gráficas y resultados
- **Figs. 1, 2, 4 y 6:** variables, unidades y valores verificados ✓.
- **Fig. 3:** fase ✓; grupo con sesgo de hasta 1,1 m/s (E3) y Airy mal redondeado (E1).
- **Fig. 5:** valores ✓, definición incompleta (E4).
- **Fig. 6 (inversión):** χ recalculado con el solver independiente da el mismo valor con 3 decimales en 5 modelos. Por ejemplo, χ(10 m; 200 m/s) = 0,858 y χ<sub>f≥15</sub>(40 m; 200 m/s) = 0,926.
- **E10:** los rangos de la inversión están limitados por la rejilla (Δh = 0,5 m, Δv<sub>s</sub> = 2 m/s) y salen de una sola realización de ruido (semilla 0). "40 m" es el borde de la rejilla, no una cota. Además, χ ≤ 1,5 es un criterio elegido y hay que declararlo.

## 13. Código
- **`scripts/dispersion.py`:**
  - Usa una malla lineal de 200 puntos (Δf ≈ 0,30 Hz) y el v<sub>g</sub> interno de disba, así que hereda E1–E3.
  - No implementa (9) ni pruebas de regresión.
  - Las unidades de disba (km, km/s, g/cm³) se convierten bien ✓.
- **`maqueta/src/figuras.py`:** mismo v<sub>g</sub> (E3). Las fracciones de sensibilidad incluyen el semiespacio en el denominador ✓. Los modelos que no convergen (excepción de disba) se excluyen sin avisarlo.
- **`fig1.py`:** incluye una aserción que comprueba el sentido de giro físico ✓.
- **Código del póster original:** no disponible. Por eso "Al refinar de 0,10 a 0,05 Hz, v<sub>g</sub> cambió hasta 0,7 m/s" y "las cuatro ramas se mantuvieron continuas" son **NO VERIFICABLES**.

## 14. Matriz de errores
| ID | Ubicación | Original | Problema | Corrección | Gravedad |
|---|---|---|---|---|---|
| E1 | Fig. 3, col. 2, conclusión [orig.] | "Airy 9,7 Hz (A), 6,7 Hz (B)"; "9,7 → 4,8 Hz" | Se usó v<sub>g</sub> de disba (sesgado) y se redondeó | 9,6 Hz (A), 6,6 Hz (B); 9,6 → 4,8 Hz | MEDIO |
| E2 | Col. 3 [orig.] | "(9) difiere del solver ≤ 1,0 m/s" | Error atribuido al revés y no reproducible (0,94–1,28 m/s según la malla) | "(9) coincide con una referencia de alta precisión en ≤ 0,1 m/s; el v<sub>g</sub> de disba se desvía hasta 1,1 m/s en el mínimo" | MEDIO |
| E3 | Fig. 3, panel v<sub>g</sub> | GroupDispersion | Sesgo de hasta 1,1 m/s, incoherente con E2 | Graficar v<sub>g</sub> con (9) sobre c<sub>R</sub>(f) con Δf ≤ 0,05 Hz | MEDIO |
| E4 | Fig. 5, conclusión "98 % / 10 %" | "Sensibilidad de c<sub>R</sub> a v<sub>s</sub>(z)" | La cifra depende de la definición (relativa: 93 % / 3 %) | "Fracción de ∫∂c<sub>R</sub>/∂v<sub>s</sub> dz en la capa (v<sub>p</sub>, ρ fijos)" | MEDIO |
| E5 | Ecs. (4)–(5) | Sin relación A–B | No se pueden reproducir | "con B = −2ikqA/(k²+s²) (2.ª fila de (7))" | MEDIO |
| E6 | Col. 1 | "Raíz única… (va de < 0 a +1)" | El teorema del valor intermedio no prueba unicidad | "Existe raíz (TVI); es única para 0 < β < 3/4 (cúbica racionalizada; verificado)" | BAJO |
| E7 | Col. 1 | "c<sub>R</sub> ≈ 0,93 v<sub>s</sub>" | No es general | "0,87–0,96 v<sub>s</sub> según ν (0,9325 aquí)" | BAJO |
| E8 | Col. 1 | Sin convención de ejes | Ambigüedad de signos | "Medio en z ≥ 0, z hacia el interior, (x, y, z) dextrógiro" | BAJO |
| E9 | (7) | "A, B ≠ 0" | Notación | "(A, B) ≠ (0, 0)" | BAJO |
| E10 | Fig. 6 | Rangos sin precisión | Resolución de la rejilla y una sola semilla | Añadir "rejilla 0,5 m × 2 m/s; una realización; 40 m = borde" | BAJO |

## 15. Reconstrucción de los errores
**E1.**
- *Original:* "Fase de Airy: 9,7 Hz (A), 6,7 Hz (B)".
- *Primer paso incorrecto:* tomar el mínimo de GroupDispersion, que calcula v<sub>g</sub> por diferencias finitas con paso relativo 0,025, y redondearlo.
- *Procedimiento correcto:* v<sub>g</sub> = 2π·2δ/(k(f+δ) − k(f−δ)), con δ = 10⁻⁴ Hz y c<sub>R</sub> resuelto a 40 dígitos. Se refina el mínimo en dos pasadas.
- *Resultado:* A: 9,646 Hz y 76,49 m/s. B: 6,636 Hz y 163,29 m/s. Por la escala f·h, el modelo de 20 m tiene el mínimo en 4,823 Hz.
- *Comparación:* el error en frecuencia es de +0,018 Hz y en v<sub>g</sub> de +1,13 m/s (1,5 %). Basta para cambiar el redondeo.
- *Afecta a:* pie de la Fig. 3, texto de la Fig. 4 y banda de conclusiones de la maqueta BC; en el póster original, "Efectos de h y de vs".

**E2.**
- *Original:* "(9) difiere del solver ≤ 1,0 m/s".
- *Problema:* la referencia correcta no es el v<sub>g</sub> del solver, porque también es numérico.
- *Comparación con la referencia (tabla §10):* (9) queda dentro de 0,09 m/s; disba se desvía hasta 1,11 m/s.
- *Corrección:* cambiar la frase y, si se quiere conservar la validación, indicar la referencia usada.

**E3.** Recalcular la curva de v<sub>g</sub> con (9). El cambio visual es despreciable: 1,1 m/s sobre una escala de 600 m/s.

**E4.**
- *Definición actual:* fracción = Σ<sub>capa</sub>∂c/∂v<sub>s,i</sub> / Σ<sub>todo</sub>∂c/∂v<sub>s,i</sub>.
- *Valores con esa definición:* 10 Hz: 0,979; 3 Hz: 0,097.
- *Valores con sensibilidad relativa:* 10 Hz: 0,933; 3 Hz: 0,032.
- *Corrección:* el mensaje "a 10 Hz domina la capa; a 3 Hz, el semiespacio" se mantiene con ambas definiciones. Hay que declarar la definición usada.

**E5.** Añadir la relación B = −2ikqA/(k²+s²) junto a (4)–(5).

**E6–E10.** Correcciones de redacción, indicadas en la matriz.

## 16. Calificación (solo exactitud)
| Dimensión | Peso | Nota | Motivo |
|---|---:|---:|---|
| Consistencia dimensional y variables | 10 | 9 | Todo homogéneo; falta declarar la convención de ejes (E8) |
| Velocidades P y S | 10 | 10 | Correctas; cota de estabilidad exacta |
| Descomposición en potenciales | 15 | 13 | Exacta, pero falta la relación A–B (E5) |
| Elasticidad y condiciones de frontera | 15 | 14 | (6) y (7) exactas; notación (E9) |
| Ecuación secular | 20 | 18 | Exacta; unicidad mal argumentada (E6); 0,93 generalizado (E7) |
| Dispersión y velocidad de grupo | 10 | 7 | c<sub>R</sub> exacto; Airy (E1), validación (E2), curvas (E3) |
| Modelos y simulaciones | 15 | 13 | Reproducidos de forma independiente; definición de la fracción (E4) y rejilla (E10) |
| Precisión y reproducibilidad | 5 | 3 | Sin código del póster original; dos afirmaciones no verificables |
| **Total** | **100** | **87** | |

## 17. Correcciones obligatorias antes de entregar
1. Corregir E1: Airy en 9,6 Hz (A) y 6,6 Hz (B); "9,6 → 4,8 Hz". También en el póster original.
2. Corregir la frase de validación de v<sub>g</sub> (E2) y recalcular las curvas de v<sub>g</sub> con (9) (E3).
3. Definir el "%" de la Fig. 5 (E4).
4. Escribir la relación A–B junto a (4)–(5) (E5).
5. Si se mantiene el póster original: retirar o respaldar con código "0,7 m/s al refinar" y "cuatro ramas".

**Dictamen: VALIDADO CON OBSERVACIONES.**

**Evidencia que falta para una validación completa:**
- El código usado para el póster original, que permitiría verificar las cifras marcadas como NO VERIFICABLE.
- Datos de campo reales, si se quisiera validar la aplicación. Hoy todo es sintético y así se declara.

## 18. Estado: correcciones aplicadas a `maqueta/maqueta_etapaBC.pdf`
Las correcciones E1–E10 están aplicadas y marcadas en rojo en `maqueta_etapaBC_anotada.pdf`.

- **E1 y E3:** v<sub>g</sub> se calcula ahora con la ec. (9), con Δf = 0,05 Hz. El mínimo de Airy se refina con una parábola por tres puntos: A en 9,648 Hz y 76,52 m/s; B en 6,638 Hz y 163,31 m/s. La referencia de alta precisión da 9,646 Hz y 76,49 m/s (A) y 6,636 Hz y 163,29 m/s (B).
- **E2:** la frase de validación de v<sub>g</sub> está reescrita.
- **E4:** la Fig. 5 y la conclusión indican que la fracción se calcula sobre ∂c<sub>R</sub>/∂v<sub>s</sub>, con v<sub>p</sub> y ρ fijos.
- **E5–E10:** añadidos la relación A–B, la convención de ejes, la notación (A, B) ≠ (0, 0), la unicidad para 0 < β < 3/4, el rango 0,87–0,96 v<sub>s</sub> y la resolución de la inversión.

**Pendiente fuera de la maqueta:** `scripts/dispersion.py` sigue usando el v<sub>g</sub> interno de disba (ver §13). En el póster original de Canva hay que corregir "9,7 → 4,8 Hz" por "9,6 → 4,8 Hz".
