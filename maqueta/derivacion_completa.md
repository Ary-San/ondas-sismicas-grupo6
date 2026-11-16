# Desarrollo completo: de Navier a la ecuación secular de Rayleigh

Complemento del póster (`maqueta/maqueta_estetica.pdf`): aquí están todos los pasos que el póster resume en
cuatro. La verificación simbólica independiente está en `auditoria/simbolico.py`.

**Convención.** El medio ocupa z ≥ 0, con z hacia el interior y (x, y, z) dextrógiro. La onda avanza en +x
y nada depende de y.

## 1. Navier y separación en P y S
Para un medio homogéneo e isótropo:

ρ ∂²u/∂t² = (λ + 2μ) ∇(∇·u) − μ ∇×∇×u

Con u = ∇φ + ∇×(ψ ŷ):
- ∇·u = ∇²φ, porque ∇·(∇×·) = 0. Solo φ cambia el volumen: es la onda **P**.
- ∇×u = −∇²ψ ŷ, porque ∂_y = 0. Solo ψ cizalla el medio: es la onda **SV**.

Basta con que cada potencial cumpla su propia ecuación de onda:

∂²φ/∂t² = v_p² ∇²φ, ∂²ψ/∂t² = v_s² ∇²ψ, con v_p = √((λ+2μ)/ρ), v_s = √(μ/ρ)

Como v_p²/v_s² = 2 + λ/μ y la estabilidad exige μ > 0 y K = λ + 2μ/3 > 0, resulta v_p/v_s > √(4/3) ≈ 1,15.

## 2. Potenciales que decaen
φ = A e^(−qz) E, ψ = B e^(−sz) E, con E = e^(i(kx−ωt))

q² = k² − ω²/v_p², s² = k² − ω²/v_s²

Hay decaimiento con la profundidad (q, s reales y positivos) solo si c = ω/k < v_s < v_p.

## 3. Desplazamientos
u_x = ∂_xφ − ∂_zψ = (ikA e^(−qz) + sB e^(−sz)) E

u_z = ∂_zφ + ∂_xψ = (−qA e^(−qz) + ikB e^(−sz)) E

## 4. Esfuerzos (ley de Hooke σ_ij = λ δ_ij ∇·u + 2μ ε_ij)
σ_zz = λ∇²φ + 2μ(∂_z²φ + ∂_x∂_zψ)

σ_xz = μ(2∂_x∂_zφ + ∂_x²ψ − ∂_z²ψ)

## 5. Superficie libre → sistema homogéneo
Se impone σ_zz = σ_xz = 0 en z = 0 y se divide por μE. Se usa la identidad
λ(q² − k²) + 2μq² = μ(k² + s²):

| | A | B |
|---|---|---|
| σ_zz = 0 | k² + s² | −2iks |
| σ_xz = 0 | −2ikq | −(k² + s²) |

Hay solución (A, B) ≠ (0, 0) si y solo si det M = 4k²qs − (k² + s²)² = 0.

## 6. Ecuación secular
Se divide por k⁴, con ξ = c_R/v_s y β = (v_s/v_p)²:

(2 − ξ²)² − 4√(1 − ξ²)√(1 − βξ²) = 0

- **Existencia de la raíz:** el lado izquierdo vale ≈ −2(1−β)ξ² para ξ pequeño y +1 en ξ = 1, así que hay una raíz en (0, 1).
- **Unicidad:** la ecuación racionalizada en X = ξ² es X³ − 8X² + (24 − 16β)X − 16(1 − β) = 0. Tiene una única raíz admisible si 0 < β < 3/4 (verificado numéricamente).
- **Valores:**
  - Semiespacio (v_p/v_s = 2): ξ = 0,9325, c_R = 606,1 m/s.
  - Capa A (v_p/v_s = 3): ξ = 0,9473, c_R = 189,5 m/s.
- **Sin dispersión:** la ecuación no contiene ω, así que en el medio homogéneo c_R no depende de la frecuencia y v_g = c_R.

## 7. Componentes sobre la raíz y la elipse
De la segunda fila de M, B = −2ikqA/(k² + s²). Entonces:

u_x = ikA [e^(−qz) − (2qs/(k²+s²)) e^(−sz)] E

u_z = −qA [e^(−qz) − (2k²/(k²+s²)) e^(−sz)] E

- **Forma de la órbita:** el factor i desfasa u_x 90° respecto de u_z, así que cada partícula describe una elipse. Para v_p/v_s = 2, la relación de amplitudes en la superficie es H/V = 0,64.
- **Inversión del giro:** u_x = 0 en z = ln[(k²+s²)/(2qs)]/(q − s) = 0,173 Λ. Por encima el giro es retrógrado y por debajo prógrado.

## 8. Velocidad de grupo a partir de c_R(f)
Con k = 2πf/c_R, la velocidad de grupo es:

v_g = dω/dk = c_R / [1 − (f/c_R) dc_R/df]

En el póster se calcula con diferencias centrales y paso de 0,05 Hz. Coincide en ≤ 0,1 m/s con una referencia
de alta precisión (`auditoria/solver_mp.py`).
