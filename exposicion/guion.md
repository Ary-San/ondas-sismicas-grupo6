# Guion de exposición — Grupo 6: Ondas sísmicas superficiales

Basado en `maqueta/maqueta_etapaBC.pdf`. El enunciado no fija la duración: el **núcleo dura ~5 min** y hay
**extensiones** para llegar a ~10 min. Las acotaciones entre [corchetes] indican qué señalar en el póster.
Si exponen varios, el reparto natural es una persona por columna (Columna 1 / Columna 2 / Columna 3 + cierre).

---

## Núcleo (~5 min)

### 0. Gancho y pregunta — 30 s · [cabecera]
> Cuando un sismo llega a Lima, el temblor que más se siente cerca de la superficie suele ser una onda
> superficial: la onda de Rayleigh. Nuestra pregunta es: **¿cómo revela la dispersión de las ondas de Rayleigh
> la estructura mecánica del subsuelo?** Vamos a derivar la ecuación que la gobierna, simular dos suelos y
> mostrar qué profundidad "ve" cada frecuencia.

### 1. Qué es una onda de Rayleigh — 60 s · [Columna 1, Fig. 1]
> P y S viajan por el interior: P comprime en la dirección de avance, S cizalla de forma perpendicular
> [señalar (a) y (b)]. Rayleigh viaja por la superficie libre y combina las dos. [señalar (c)] Esta figura no es
> un dibujo: la calculamos con nuestras ecuaciones (4) y (5). Cada partícula describe una **elipse vertical**.
> En la superficie gira en sentido **retrógrado**, contrario al avance. A 0,17 longitudes de onda de
> profundidad el movimiento horizontal se anula y el giro se invierte. La amplitud decae en
> aproximadamente una longitud de onda: por eso es superficial.

### 2. De dónde sale c_R — 60 s · [Columna 1, ecs. 1–8]
> Partimos de la ecuación de Navier (1) y escribimos el desplazamiento con dos potenciales: φ cambia el volumen
> (P) y ψ solo cizalla (SV). Así aparecen v_p y v_s (2). En la superficie el aire no ejerce tracción: σ_xz y
> σ_zz deben anularse. Eso da un sistema homogéneo para las amplitudes A y B (7). Solo hay solución no nula
> si **det M = 0**, y esa es la **ecuación secular** (8). Para nuestro semiespacio la raíz es
> c_R = 0,9325 v_s = 606,1 m/s.
> **¿Por qué c_R < v_s < v_p?** Si la onda fuera más rápida que S, la parte de corte radiaría energía hacia
> abajo y dejaría de ser superficial. Sin material encima, la superficie "cede", y por eso c_R queda ~7 % por
> debajo de v_s. Como (8) no contiene la frecuencia, **en un medio homogéneo no hay dispersión**.

### 3. Dos suelos, dos curvas — 75 s · [Columna 2, Figs. 2–4]
> Ahora agregamos una capa blanda sobre el semiespacio [Fig. 2]. Modelo A: 10 m con v_s = 200 m/s.
> Modelo B: 20 m con v_s = 300 m/s. Ojo: su V_s30 es casi igual (371 y 366 m/s) y la norma E.030 los
> clasifica igual (S2), pero sus curvas son muy distintas. Un solo número oculta la estratificación.
> [Fig. 3] Calculamos las curvas con disba, que usa el método de Dunkin. A baja frecuencia c_R tiende a
> 606 m/s, la velocidad de Rayleigh del semiespacio. A alta frecuencia tiende a la de la capa: 189,5 o
> 279,8 m/s. La velocidad de grupo cae por debajo de la de fase y tiene un mínimo, la **fase de Airy**.
> [Fig. 4] Si cambiamos un parámetro a la vez: duplicar h **divide por 2** la frecuencia de transición, porque
> c_R depende solo de f·h. Subir v_s eleva la asíntota de alta frecuencia.

### 4. Qué profundidad ve cada frecuencia — 45 s · [Columna 3, Fig. 5]
> Esta es la respuesta a nuestra pregunta. Calculamos cuánto cambia c_R si cambiamos v_s a cada profundidad.
> A 10 Hz, el **98 %** de la sensibilidad está en los primeros 10 m. A 3 Hz, solo el **10 %**: esa frecuencia
> "mira" mucho más hondo. No hay una regla fija frecuencia → profundidad: depende de la longitud de onda,
> del perfil y del modo.

### 5. Invertir y aplicar — 45 s · [Columna 3, Fig. 6 y MASW]
> En campo se hace al revés: se mide la curva y se busca el suelo que la explica. Lo probamos: tomamos la
> curva de A, le añadimos 2 % de ruido y buscamos h y v_s. Con 3–40 Hz recuperamos **h ≈ 10 m**. Con solo
> f ≥ 15 Hz, h queda indeterminado entre 8,5 y 40 m. **La banda medida decide qué se puede invertir.**
> Así funciona MASW: geófonos, curva de dispersión, inversión, perfil V_s(z) y V_s30 para la norma
> sísmica. Por ejemplo, para microzonificación en Lima.

### 6. Cierre — 15 s · [banda de conclusiones]
> En resumen: **cada frecuencia ve una profundidad distinta**. Por eso la curva de dispersión funciona como una
> tomografía del subsuelo. El código está en el QR. Gracias.

---

## Extensiones (para llegar a ~10 min)

| Dónde insertarla | Contenido | Tiempo |
|---|---|---|
| Tras el bloque 1 | Por qué la elipse: en (4) aparece el factor *i*, así que u_x va 90° desfasado de u_z. H/V = 0,64 en superficie. | +40 s |
| Tras el bloque 2 | Derivar la matriz (7) en la pizarra: sustituir (3) en (6) en z = 0. | +60 s |
| Tras el bloque 3 | Fase frente a grupo: c_R sigue un punto de fase y v_g la envolvente. La ec. (9) coincide con el solver ≤ 1,0 m/s. | +45 s |
| Tras el bloque 3 | Escala f·h: la única longitud del problema es h, así que c_R depende de h/Λ. | +30 s |
| Tras el bloque 5 | Limitaciones: medio 1D elástico sin atenuación, solo modo fundamental, datos sintéticos, v_p y ρ fijos. | +30 s |

---

## Preguntas probables del jurado

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué c_R < v_s? | Si c > v_s, s sería imaginaria y la parte SV radiaría energía hacia el interior: la onda no quedaría confinada. La ec. (8) tiene una raíz en 0 < ξ < 1 porque su lado izquierdo pasa de negativo a +1. |
| ¿Y por qué v_s < v_p? | v_p²/v_s² = 2 + λ/μ. La estabilidad del material (μ > 0 y módulo volumétrico K = λ + 2μ/3 > 0) exige v_p/v_s > √(4/3) ≈ 1,15. |
| ¿Por qué el giro es retrógrado? | Sale de (4)–(5): en la cresta de la órbita superficial la partícula se mueve hacia −x. u_x cambia de signo a 0,17 Λ, y debajo el giro es prógrado. |
| ¿Por qué no hay dispersión en el semiespacio? | No hay ninguna longitud característica: la ec. (8) no depende de ω, así que c_R es constante y v_g = c_R. |
| ¿Qué es la fase de Airy? | El mínimo de v_g. Muchas frecuencias viajan con casi la misma velocidad de grupo y llegan juntas, lo que produce una llegada tardía de gran amplitud. |
| ¿Qué significa el 98 %? | Es la fracción de ∂c_R/∂v_s(z) acumulada dentro de la capa de 10 m: cuánto de la sensibilidad de c_R viene de esos 10 m. |
| ¿Por qué la inversión no es única? | Con solo f ≥ 15 Hz casi toda la sensibilidad está en la capa: se fija v_s, pero no se "ve" dónde termina la capa. |
| ¿Por qué χ ≤ 1,5? | Es el criterio de ajuste aceptable que elegimos: error medio ≤ 1,5 σ, con σ = 2 % de c_R. Con χ ≤ 1 la región es más chica, pero la conclusión no cambia. |
| ¿Usaron datos reales? | No: los modelos y la inversión son sintéticos. Con datos de campo habría ruido, modos superiores y heterogeneidad lateral. |
| ¿Por qué fijar v_p y ρ? | c_R de Rayleigh es mucho más sensible a v_s que a v_p y ρ (Xia et al., 1999). |
| ¿Qué hace disba / Dunkin? | Resuelve la ecuación secular de un medio estratificado con una formulación matricial estable a alta frecuencia (Dunkin, 1965). |
| ¿Qué es Vs30 y para qué sirve? | Es el promedio de v_s en los primeros 30 m: V_s30 = 30 / Σ(hᵢ/v_si). La E.030 lo usa para clasificar el suelo (S2: 180–500 m/s). |
| ¿Y los modos superiores? | Solo usamos el modo 0. Con contrastes fuertes los modos superiores pueden dominar a alta frecuencia, y es una limitación declarada. |

## Consejos
- Señalen el póster en cada frase: la figura es la evidencia; el texto, el apoyo.
- Las tres cifras que hay que decir sí o sí: **98 %**, **f ÷ 2** y **h ≈ 10 m**.
- Si preguntan algo fuera del póster, respondan con lo que muestran las figuras y, si no lo saben, díganlo.
