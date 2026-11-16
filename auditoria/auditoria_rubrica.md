# Auditoría del póster según la rúbrica oficial (TD2 · Óptica y Ondas · 2026-1)

**Objeto auditado:** `maqueta/maqueta_utec.pdf`, el póster en la plantilla oficial con el contenido B+C corregido.
**Documentos normativos:**
- `Rúbrica - TD2.pdf`: criterios y descripción de cada nivel.
- `TD2_Teo11_Proyectos&Grupos.pdf`, Grupo 6: el "contenido mínimo declarado", es decir, las actividades 1–6 y el entregable.

**Evidencia previa:** `auditoria/auditoria_matematica.md`. Allí se verificaron todas las ecuaciones y cifras de forma simbólica y con un solver independiente.

> Las calificaciones de los criterios 2 y 5 dependen de la exposición oral. Aquí solo se evalúa lo que el
> póster demuestra y cuánto prepara a los expositores.

---

## Resumen de puntajes

| Criterio | Máx. | Estado actual | Nivel | Con el plan de §7 |
|---|---:|---:|---|---:|
| 1. Póster con contenido mínimo | 8 | **6,0** | Logrado | 8,0 |
| 2. Habilidades expositivas | 2 | no calificable | — | depende de la exposición |
| 3. Conceptos y definiciones | 3 | **2,5** | Logrado | 3,0 |
| 4. Modelado, ecuaciones y supuestos | 3 | **2,5** | Logrado | 3,0 |
| 5. Profundidad y preguntas | 4 | **3,0** (lo que muestra el póster) | Logrado | 4,0 (si las respuestas orales acompañan) |
| **Total del póster (sin criterio 2)** | **18** | **14,0** | | **18,0** |

**Errores matemáticos:** ninguno. La auditoría matemática dictaminó "validado con observaciones" y esas observaciones ya están corregidas en esta versión.

**Lo que falta para Destacado son omisiones de contenido y de presentación:**
1. No se explica qué información aporta cada velocidad, cuando la actividad 5 lo pide.
2. No hay analogías, que el descriptor Destacado del criterio 3 exige.
3. Faltan supuestos explícitos: isotropía, linealidad y condiciones en la interfaz.
4. No se proponen extensiones.
5. Hay detalles de rotulado, legibilidad y créditos: nombres pendientes, unidades en la Fig. 2, letras pequeñas en la Fig. 1 y crédito de las figuras.

---

## 1. Criterio 1 · Presentación del póster con el contenido mínimo (8 pts)

**Descriptor Destacado:** "Cumple y supera el contenido mínimo declarado: estructura clara; figuras/tablas legibles y con unidades; ecuaciones bien formateadas; coherencia visual y jerarquía tipográfica; créditos y fuentes completas; evita texto excesivo."

### A. Contenido mínimo (enunciado del Grupo 6)
| Actividad | Evidencia en el póster | Estado |
|---|---|---|
| 1. P, S y Rayleigh, con esquema de propagación horizontal y decaimiento | Introducción y Fig. 1 (a, b, c), con las órbitas calculadas y el perfil de amplitud | ✅ |
| 2. Cómo aparecen v_p y v_s desde los potenciales; por qué Rayleigh combina componentes longitudinal y transversal | Metodología, ecs. (1)–(5) y frase sobre el factor i | ✅ |
| 3. Frontera libre → ecuación secular para c_R = ω/k | Ecs. (6)–(8) | ✅ |
| 4. Por qué c_R < v_s < v_p; cómo cambia c_R(f) con h y con v_s | "¿Por qué c_R < v_s < v_p?" y Fig. 4 | ✅ |
| 5. Calcular v_g, compararla con c_R y **explicar qué información aporta cada una** | Ec. (9), "v_g < c_R" y fase de Airy. **No dice qué información aporta cada velocidad.** El texto "fase / envolvente que transporta la energía" de versiones anteriores se perdió al pasar a la plantilla | ⚠️ parcial |
| 6. Simulación con c_R(f) y v_g(f) variando h y v_s, e interpretación de la sensibilidad con la profundidad | Figs. 3, 4 y 5 | ✅ |
| Entregable: dos modelos estratificados y una aplicación | Fig. 2, MASW, V_s30 y E.030 | ✅ |

### B. Estructura
Sigue la plantilla oficial: Introducción → Metodología → Resultados → Conclusiones → Referencias.

La pregunta central y el objetivo están en Introducción, y las conclusiones responden la pregunta con tres cifras. La secuencia es lógica.

**Observación:** la inversión de prueba (Fig. 6) está en Conclusiones y no en Resultados. Se justifica como evidencia de la conclusión 3, pero un evaluador estricto podría verlo como un resultado mal ubicado. No es un error.

### C. Figuras
- **Unidades:** las Figs. 3, 4, 5 y 6 tienen ejes rotulados, unidades y leyenda ✅.
- **Fig. 2:** los valores de v_s y v_p (200, 600, 650…) **no indican m/s**. El pie solo menciona "ρ en kg/m³". Es una imprecisión de rotulado.
- **Fig. 1, legibilidad:** los rótulos tienen entre **10,6 y 19,6 pt** (medido en el PDF). Por ejemplo, "1 Λ (a escala); órbitas ampliadas" y las etiquetas z = 0,12 Λ. En un A0 son difíciles de leer a más de 1 m.
- **Explicación en el texto:** todas las figuras se citan ✅.
- **Créditos:** las figuras son propias, pero el póster **no lo dice**. Conviene indicar "Figuras: elaboración propia (Python, disba)".

### D. Ecuaciones
Las 10 ecuaciones están numeradas con tipografía matemática y fueron verificadas ✅.

**Variables sin definir con palabras:** k (número de onda horizontal), ω (frecuencia angular) y la relación ω = 2πf. Λ solo aparece en la Fig. 1 y en los kernels.

### E. Coherencia visual y tipografía
- **Jerarquía:** título 116 pt, encabezados de caja 50 pt, subtítulos 29–32 pt y cuerpo 25–29 pt. Es clara ✅.
- **Densidad:** la Metodología, a dos subcolumnas de 25 pt con 10 ecuaciones, es densa. Hay riesgo de que se lea como "texto excesivo", aunque todo es contenido exigido.

### F. Redacción y fuentes
- **Redacción:** académica y sin errores ortográficos detectados ✅.
- **Referencias:** las 8 están completas y verificadas ✅.
- **Créditos:** los integrantes figuran como **"[APELLIDOS Y NOMBRES DE LOS INTEGRANTES]"**. Sin los nombres, "créditos completos" no se cumple.

**Puntaje: 6,0 (Logrado).** El contenido mínimo está casi completo; la falta más importante es la explicación de la actividad 5. Hay imprecisiones de rotulado (unidades en la Fig. 2), de legibilidad (Fig. 1) y de créditos (nombres y autoría de las figuras).

**Riesgo:** si se entrega sin nombres y sin la actividad 5 completa, puede bajar a "En proceso (2,0)", cuyo descriptor es "falta parte del contenido mínimo".

---

## 2. Criterio 2 · Habilidades expositivas (2 pts): preparación

No se puede calificar sin ver la exposición. Lo que el póster aporta para que salga bien:

**A favor:**
- Secuencia narrable de izquierda a derecha: pregunta → teoría → simulación → respuesta.
- Ecuaciones numeradas, que permiten señalarlas mientras se habla.
- Cifras memorables: 98 %, f·h y h ≈ 10 m.
- Ya existe un guion (`exposicion/guion.md`) con un núcleo de 5 minutos y extensiones.

**En contra:**
- La Metodología es densa y tienta a leerla; el descriptor En proceso menciona "lectura excesiva".
- El guion se escribió para la maqueta vertical: hay que actualizar las indicaciones de dónde señalar.

**Recomendaciones:**
1. **Reparto:** una persona por caja (Introducción · Metodología · Resultados · Conclusiones), para evitar "participación desigual".
2. **Ecuaciones:** no leerlas. Contar la cadena: "Navier → dos potenciales → frontera libre → determinante → ecuación secular" y señalar solo (8).
3. **Ensayo:** cronometrado a 5 minutos; extender solo si sobra tiempo.
4. **Cifras clave:** cada expositor memoriza dos.
5. **Respuestas:** practicar el banco de preguntas de §6 con respuestas de 20–30 segundos.

---

## 3. Criterio 3 · Conceptos fundamentales y definiciones (3 pts)

**Descriptor Destacado:** "Define con precisión el fenómeno estudiado; establece variables, unidades y condiciones; **reconoce analogías y límites del régimen aplicable**."

| Aspecto | Evidencia | Estado |
|---|---|---|
| Definición del fenómeno | Rayleigh superficial, P + SV, elipses y decaimiento en ~1 Λ | ✅ |
| Variables | λ, μ, ρ, v_p, v_s, q, s, ξ y β definidas; **k y ω no se nombran** | ⚠️ |
| Unidades | Presentes en figuras y resultados; ausentes en las variables de la Metodología y en la Fig. 2 | ⚠️ |
| Condiciones | z ≥ 0, superficie libre y decaimiento ✅; **isotropía, linealidad y deformación plana no se dicen** | ⚠️ |
| Conceptos que se confunden | Fase frente a grupo: bien distinguidas en la fórmula, pero sin explicar la información que aporta cada una | ⚠️ |
| Analogías | **Ninguna** | ❌ |
| Límites del régimen | Asíntotas de baja y alta frecuencia, limitaciones del modelo y banda de 1–60 Hz | ✅ |

No hay definiciones incorrectas ni generalizaciones inválidas; la frase "0,87–0,96 v_s según ν" ya se corrigió en la auditoría.

**Puntaje: 2,5 (Logrado):** define correctamente, con omisiones menores. **Para llegar a 3,0** hay que agregar una analogía. La más natural para un curso de Óptica y Ondas:
- **Onda evanescente:** con q y s reales, los potenciales son campos evanescentes, igual que la onda evanescente en la reflexión total interna; en ambos casos la velocidad de fase horizontal es menor que la del medio.
- **Guía de onda:** la capa actúa como una guía, igual que una guía óptica de lámina, donde el modo depende de la relación espesor/longitud de onda; de ahí sale la dispersión.

---

## 4. Criterio 4 · Modelado, ecuaciones y supuestos (3 pts)

**Descriptor Destacado:** "Presenta las ecuaciones relevantes con derivaciones resumidas y supuestos explícitos; discute validez y límites; aplica correctamente notación y unidades."

- **A. Ecuaciones:** pertinentes, correctas y dimensionalmente consistentes; coinciden con los resultados (disba frente a solver independiente, ≤ 0,0003 m/s) ✅.
- **B. Derivaciones:** cadena completa (1)→(8) sin saltos; la relación A–B está explícita ✅.
- **C. Supuestos:**
  - Explícitos: medio en z ≥ 0, superficie libre, decaimiento, modo fundamental y limitaciones (1D, sin atenuación, datos sintéticos, v_p y ρ fijos) ✅.
  - **Faltan:**
    - Elasticidad **lineal** e **isótropa**: está implícita en λ y μ, pero no se dice.
    - Dependencia armónica y deformación plana (∂_y = 0).
    - **Condiciones en la interfaz** del modelo de capas: continuidad del desplazamiento y de la tracción, contacto soldado. Estaban en el póster original y en la versión B+C, pero se perdieron al pasar a la plantilla.
- **D. Aplicación física:** cada ecuación lleva interpretación (factor i → elipse; sin ω → sin dispersión; (9) → v_g < c_R) ✅. Validez discutida con asíntotas y limitaciones ✅.

**Puntaje: 2,5 (Logrado):** "la mayoría de supuestos". **Para llegar a 3,0** basta con una línea de supuestos (ver §7).

---

## 5. Criterio 5 · Profundidad en el tema y resolución de preguntas (4 pts)

**Descriptor Destacado:** "Integra el modelo con experimentos, aplicaciones; analiza casos límite y fuentes de error; propone extensiones o comparaciones."

| Aspecto | Evidencia | Estado |
|---|---|---|
| Modelo ↔ simulación | Ecuación secular frente a disba (606,1 m/s); validación de v_g | ✅ |
| Interpretación | Asíntotas, escala f·h, kernels y Vs30 que oculta la estratificación | ✅ |
| Casos límite | f → 0 (semiespacio), f → ∞ (capa) y medio homogéneo | ✅ |
| Órdenes de magnitud | Λ de 192 m a 10 m, Vs30 y fracciones de sensibilidad | ✅ |
| Fuentes de error | Ruido del 2 % y resolución de la rejilla; error numérico de v_g mencionado | ⚠️ falta agruparlas como "fuentes de error" |
| Aplicaciones | MASW, V_s30, E.030 y microzonificación | ✅ |
| Comparaciones | A frente a B; cambios aislados | ✅ |
| **Extensiones** | No se proponen (modos superiores, Love, atenuación, datos reales) | ❌ |
| Experimentos | Solo datos sintéticos, declarado como limitación | — no hay datos de campo |

**Puntaje del póster: 3,0 (Logrado).** Para el 4,0 hace falta proponer extensiones en una línea y que las respuestas orales sean rigurosas (§6).

---

## 6. Banco de preguntas con respuestas modelo

### Conceptuales
1. **¿Qué diferencia una onda de Rayleigh de una onda S?**
   - *Respuesta:* la S es una onda de cuerpo transversal que viaja a v_s. La Rayleigh es una onda superficial: combina componentes P y SV evanescentes que, juntas, anulan la tracción en la superficie. Viaja a c_R < v_s, las partículas describen elipses retrógradas en la superficie y su amplitud decae en ~1 Λ.
   - *Extra:* se atenúa geométricamente como 1/√r, frente a 1/r de las ondas de cuerpo; por eso domina lejos de la fuente.
   - *En el póster:* Introducción, Fig. 1 y ecs. (3)–(5).
2. **¿Por qué el movimiento es elíptico y no circular?**
   - *Respuesta:* u_x lleva un factor i respecto de u_z, así que están desfasadas 90°. Además sus amplitudes son distintas: H/V = 0,64 para v_p/v_s = 2.
   - *En el póster:* ecs. (4)–(5) y Fig. 1.
3. **¿Qué es la dispersión y por qué no ocurre en un semiespacio homogéneo?**
   - *Respuesta:* es la dependencia de la velocidad de fase con la frecuencia. Un medio homogéneo no tiene ninguna longitud característica: la ec. (8) no contiene ω, así que c_R es constante. El espesor h de la capa introduce esa escala.
   - *En el póster:* texto bajo (8) y Fig. 3.
4. **¿Qué diferencia hay entre velocidad de fase y velocidad de grupo, y qué información aporta cada una?**
   - *Respuesta:* c = ω/k es la velocidad de un punto de fase constante; es lo que mide MASW y lo que se invierte. v_g = dω/dk es la velocidad de la envolvente de un paquete de banda estrecha y la del transporte de energía; fija los tiempos de llegada. Con dispersión normal (dc/df < 0), v_g < c.
   - *En el póster:* ec. (9) y Fig. 3. **Falta en el póster la frase sobre la información que aporta cada una.**
5. **¿Qué significa "superficie libre" y por qué implica σ_xz = σ_zz = 0?**
   - *Respuesta:* el aire no transmite tracción apreciable, así que el vector de tracción t = σ·ẑ debe anularse en z = 0. En el problema P-SV en 2D, σ_yz = 0 se cumple de forma automática.
   - *En el póster:* Metodología, "Frontera libre".

### Ecuaciones y modelado
6. **¿De dónde salen v_p y v_s?**
   - *Respuesta:* se sustituye u = ∇φ + ∇×(ψŷ) en la ecuación de Navier (1). La divergencia solo afecta a φ y da una ecuación de onda con velocidad √((λ+2μ)/ρ). El rotacional solo afecta a ψ y da otra con velocidad √(μ/ρ).
   - *En el póster:* ecs. (1)–(2).
7. **¿Por qué tiene que anularse el determinante?**
   - *Respuesta:* M·(A, B) = 0 es un sistema homogéneo. Tiene solución no trivial solo si det M = 0, y esa condición liga ω con k: es la relación de dispersión.
   - *En el póster:* ec. (7).
8. **¿Cómo se pasa de det M = 0 a la ec. (8)?**
   - *Respuesta:* det M = 4k²qs − (k² + s²)² = 0. Se divide por k⁴ y se usa s/k = √(1 − ξ²) y q/k = √(1 − βξ²). La raíz es ξ = 0,9325 para β = 1/4.
   - *En el póster:* ecs. (7)–(8).
9. **¿Por qué q y s tienen que ser reales y positivos?**
   - *Respuesta:* para que e^(−qz) y e^(−sz) decaigan con la profundidad (z ≥ 0 hacia abajo). Eso exige c < v_s < v_p. Si c > v_s, s es imaginaria y la parte SV radia energía hacia el interior: el modo deja de estar confinado ("leaky").
   - *En el póster:* "¿Por qué c_R < v_s < v_p?".
10. **¿Cómo calcularon las curvas del medio estratificado?**
    - *Respuesta:* con disba, que usa el método de Dunkin, una variante estable del método de matrices de Thomson–Haskell. Impone superficie libre, continuidad del desplazamiento y de la tracción en la interfaz, y decaimiento en el semiespacio; luego busca la raíz del modo fundamental para cada período. v_g se calcula con (9) por diferencias centrales con Δf = 0,05 Hz.
    - *Validación:* un solver independiente reproduce c_R con diferencias ≤ 0,0003 m/s.
    - *En el póster:* "Simulación". **Falta mencionar la condición en la interfaz.**

### Interpretación física
11. **¿Por qué c_R tiende a 606 m/s a baja frecuencia y a 189,5 m/s a alta?**
    - *Respuesta:* cuando Λ ≫ h, la onda "ve" sobre todo el semiespacio: 0,9325 × 650 = 606,1 m/s. Cuando Λ ≪ h, queda confinada en la capa: 0,947 × 200 = 189,5 m/s.
    - *En el póster:* Fig. 3 y su pie.
12. **¿Qué es la fase de Airy?**
    - *Respuesta:* es el mínimo de v_g, donde dv_g/df = 0. Muchas frecuencias viajan casi a la misma velocidad de grupo y llegan juntas, lo que produce una llegada tardía de gran amplitud. En A ocurre a 9,6 Hz con 76,5 m/s.
    - *En el póster:* Fig. 3.
13. **¿Por qué duplicar h divide por 2 la frecuencia?**
    - *Respuesta:* con las velocidades y densidades fijas, la única longitud del problema es h. Entonces c_R depende solo de kh, es decir, de f·h. Se verificó numéricamente: la diferencia es menor que 0,1 m/s.
    - *En el póster:* Fig. 4.
14. **¿Qué significa "98 % a 10 Hz"?**
    - *Respuesta:* es la fracción de ∫∂c_R/∂v_s dz que cae dentro de la capa de 10 m, con v_p y ρ fijos. A 10 Hz (Λ = 27 m), c_R depende casi solo de la v_s de la capa. Con la sensibilidad relativa (v_s·∂c/∂v_s), la fracción es 93 %.
    - *En el póster:* Fig. 5.
15. **¿Por qué A y B tienen casi el mismo V_s30 pero curvas tan distintas?**
    - *Respuesta:* V_s30 es un promedio armónico (un tiempo de viaje vertical) sobre 30 m. Distintas combinaciones de h y v_s dan el mismo tiempo. La curva de dispersión, en cambio, distingue cómo se reparte v_s en profundidad.
    - *En el póster:* Fig. 2 y Resultados.

### Aplicaciones y limitaciones
16. **¿Cómo funciona MASW?**
    - *Respuesta:*
      1. Una fuente activa y una línea de geófonos registran el paso de la onda.
      2. Una transformada frecuencia–velocidad produce la imagen de dispersión.
      3. Se identifica la curva del modo fundamental.
      4. Se invierte un modelo de capas minimizando (10).
      5. Se obtiene V_s(z) y de ahí V_s30.
    - *En el póster:* Conclusiones, flujo MASW.
17. **¿Por qué importa V_s en ingeniería sísmica?**
    - *Respuesta:* el módulo de corte es G = ρv_s², y v_s controla la amplificación del sitio. La Norma E.030 clasifica los suelos por V_s (S2: 180–500 m/s), y esa clase fija el factor de suelo y los períodos de diseño.
    - *En el póster:* Fig. 2 y Conclusiones.
18. **¿Qué limita la inversión?**
    - *Respuesta:*
      - No unicidad, más fuerte cuando la banda es limitada (Fig. 6).
      - Compensación entre h y v_s.
      - Ruido en la curva medida.
      - Confusión con modos superiores.
      - Heterogeneidad lateral.
      - v_p y ρ supuestos.
    - *En el póster:* Fig. 6 y Limitaciones.
19. **¿Qué cambiaría si se incluyera atenuación?**
    - *Respuesta:* el medio sería viscoelástico, con módulos complejos. La amplitud decaería a lo largo de x y aparecería una dispersión adicional débil (por causalidad), incluso en un medio homogéneo. El póster no la incluye y lo declara.
    - *En el póster:* Limitaciones.
20. **¿Cuándo es válido el modelo 1D?**
    - *Respuesta:* cuando el subsuelo es lateralmente homogéneo a lo largo del arreglo de geófonos, en una escala mayor que la Λ máxima usada. Con contrastes laterales (rellenos, quebradas) aparecen efectos 2D y 3D.
    - *En el póster:* Limitaciones.

### Casos nuevos
21. **¿Y si la capa fuera más rápida que el semiespacio?**
    - *Respuesta:* sería una inversión de velocidad. La curva ya no decrece de forma monótona, y donde c supera a la v_s del semiespacio el modo deja de estar confinado ("leaky"). La inversión con solo el modo fundamental se vuelve ambigua [7]. Habría que calcularlo; el modelo actual no cubre este caso.
22. **Con un equipo que solo mide de 1 a 5 Hz, ¿qué se resolvería en el Modelo A?**
    - *Respuesta:* Λ = c_R/f va de ~600 m a ~110 m. Según la Fig. 5, a 3 Hz solo el 10 % de la sensibilidad está en la capa. Se resolvería la v_s del semiespacio, pero no la capa de 10 m: para eso hace falta f ≳ 8–10 Hz (Λ ≲ 30 m).
23. **Si la capa estuviera saturada (v_p ≈ 1500 m/s, v_s = 200 m/s), ¿cambiaría mucho c_R?**
    - *Respuesta:* poco. ν pasaría de 0,44 a 0,49, y ξ de 0,947 a ~0,953 (aproximación de Viktorov), es decir, < 1 %. c_R depende sobre todo de v_s, y por eso la inversión estima V_s y no V_p.

---

## 7. Plan para llegar a Destacado (cambios concretos sobre `maqueta_utec.pdf`)

| # | Criterio | Cambio | Dónde |
|---|---|---|---|
| 1 | C1 | Completar los nombres de los integrantes | Franja negra |
| 2 | C1, C3 | Actividad 5: "c_R es la velocidad de las crestas: lo que mide MASW y se invierte. v_g es la de la envolvente y la energía: fija los tiempos de llegada; en la fase de Airy se acumula energía." | Junto a la ec. (9) en Resultados |
| 3 | C1 | Unidades en la Fig. 2: "v_s, v_p en m/s" | Pie o rótulos de la Fig. 2 |
| 4 | C1 | Agrandar los rótulos de la Fig. 1 a ≥ 18 pt (dar más ancho a la figura o acortar el texto de la izquierda) | Introducción |
| 5 | C1 | Crédito: "Figuras: elaboración propia (Python + disba 0.7.0)" | Referencias |
| 6 | C3 | Definir k (número de onda horizontal, m⁻¹), ω = 2πf (rad/s), Λ = 2π/k = c_R/f (m) | Inicio de Metodología |
| 7 | C3 | Analogía: "q, s > 0 → campos evanescentes, como en la reflexión total interna; la capa actúa como guía de onda y su modo depende de h/Λ, igual que en una guía óptica" | Metodología o Conclusiones |
| 8 | C4 | Supuestos: medio elástico lineal, isótropo y homogéneo por capas; onda plana armónica; deformación plana (∂_y = 0); en la interfaz, continuidad de u y de la tracción | Metodología, "Simulación" |
| 9 | C5 | Fuentes de error agrupadas: numéricas (c_R ≤ 0,0003 m/s; v_g ≤ 0,1 m/s), ruido del 2 % y resolución de la rejilla en la inversión, supuestos del modelo | Conclusiones |
| 10 | C5 | Extensiones: modos superiores, ondas Love, atenuación (Q), inversión de un registro MASW real | Conclusiones, junto a Limitaciones |
| 11 | C2 | Actualizar el guion con las ubicaciones del formato horizontal y repartir una caja por expositor | `exposicion/guion.md` |

Los cambios 2, 6, 7, 8, 9 y 10 suman unas 6–8 líneas. Para que entren sin perder legibilidad: llevar el cambio 8 a la línea de "Simulación" que ya existe, y los cambios 9 y 10 al recuadro de Limitaciones.

## 8. Estado: cambios aplicados a `maqueta/maqueta_utec.pdf`
| # | Estado | Dónde quedó |
|---|---|---|
| 1 | ✅ | Franja negra: Danna Gala · Ary Sanchez · Eduardo Salvador · Mendoza Gracia |
| 2 | ✅ | Junto a la ec. (9): qué informa c_R y qué informa v_g |
| 3 | ✅ | Pie de la Fig. 2: "v_s, v_p en m/s" |
| 4 | ✅ | Fig. 1 con rótulos principales ≥ 18 pt; solo los subíndices quedan por debajo |
| 5 | ✅ | Bajo el QR: "Figuras: elaboración propia (Python, disba)" |
| 6 | ✅ | Línea "Supuestos" de Metodología: k, ω = 2πf y Λ = c_R/f con unidades |
| 7 | ✅ | Recuadro "Analogía óptica" en Conclusiones |
| 8 | ✅ | Supuestos (lineal, isótropo, por capas, onda plana armónica, ∂_y = 0, z ≥ 0) e interfaz soldada en "Simulación" |
| 9 | ✅ | "Fuentes de error" en Conclusiones |
| 10 | ✅ | "Extensiones" en Conclusiones |
| 11 | ✅ | `exposicion/guion.md`: ubicaciones del formato horizontal, un expositor por caja, analogía y frase de fase frente a grupo |

**Ajustes de tamaño para que todo entre:**
- Metodología pasó a 24 pt.
- La Fig. 6 quedó en 400 pt de ancho.
- Las fuentes de error, las limitaciones y las extensiones están en 20 pt.

---

## 9. Reauditoría de la versión final (`maqueta/maqueta_utec.pdf`)

**Verificación en el PDF.** Se extrajo el texto del PDF y se comprobó que los 11 cambios de §7 están presentes. También se confirmó que la fase de Airy figura como "9,6 Hz" en todas partes y que no queda ningún "9,7".

**Tamaños medidos:**
- Cuerpo: 23–29 pt.
- Textos secundarios (referencias, fuentes de error): 20 pt.
- Rótulos de figuras: ≥ 18 pt; solo los subíndices son más chicos.

**Volumen:** ~6 600 caracteres de texto visible.

| Criterio | Antes | Ahora | Evidencia | Qué falta |
|---|---:|---:|---|---|
| 1. Contenido mínimo (8) | 6,0 | **6,0 estricto → 8,0 con 2 retoques** | Actividades 1–6 y entregable completos; unidades; Fig. 1 legible; crédito de las figuras; nombres | (a) Referencias acortadas al pasar a la plantilla: [3] dice solo "MVCS" y [5] no tiene el título completo de disba. (b) El formato de los nombres no es uniforme: tres van nombre-apellido y "Mendoza Gracia" parece apellido-nombre. Son las "1–2 imprecisiones menores" del descriptor Logrado. |
| 2. Exposición (2) | — | — | Guion por caja, con 4 expositores y núcleo de 5 min | Depende de la exposición |
| 3. Conceptos (3) | 2,5 | **3,0** | Variables con unidades (k, ω, Λ, λ, μ, ρ); condiciones (lineal, isótropo, z ≥ 0, ∂_y = 0); analogía óptica (onda evanescente y guía de onda); límites del régimen (asíntotas y limitaciones) | — |
| 4. Modelado (3) | 2,5 | **3,0** | Ecuaciones (1)–(10) con derivación resumida; supuestos explícitos con interfaz soldada; validez y limitaciones; notación verificada | — |
| 5. Profundidad (4) | 3,0 | **4,0 (el póster lo permite)** | Casos límite, órdenes de magnitud, fuentes de error, aplicación (MASW, E.030), comparaciones (A/B y cambios aislados) y extensiones | La nota final depende de las respuestas orales (§6) |
| **Total del póster (sin criterio 2)** | **14,0** | **16,0 estricto · 18,0 con los 2 retoques** | | |

**Riesgo no medible:** la Metodología, a 24 pt con 10 ecuaciones, es densa. Un evaluador podría verla como "texto excesivo". Está mitigado, porque todo es contenido que exige el enunciado y la exposición no debe leerla.
