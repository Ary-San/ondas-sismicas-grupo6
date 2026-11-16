# Interpretación Física: Dispersión y Sensibilidad en Profundidad de Ondas de Rayleigh
**Grupo 6 · Óptica y Ondas (UTEC)**

---

## 1. Relación entre Frecuencia, Longitud de Onda y Profundidad de Muestreo

Las ondas de Rayleigh son ondas superficiales elásticas acopladas (P-SV) cuya amplitud decae exponencialmente con la profundidad $z$. La penetración vertical depende intrínsecamente de su longitud de onda horizontal:
$$\Lambda(f) = \frac{c_R(f)}{f}$$

A partir de la formulación variacional de Rayleigh y el principio de Rayleigh-Ritz, la sensibilidad de la velocidad de fase $c_R$ respecto a la velocidad de onda transversal $v_S$ a profundidad $z$ viene dada por el kernel de sensibilidad:
$$K_{v_S}(z, f) = \frac{\partial c_R}{\partial v_S}(z, f)$$

### Resultados Cuantitativos del Modelo A ($h = 10$ m, $v_{S1} = 200$ m/s, $v_{S2} = 650$ m/s):

| Frecuencia $f$ | Longitud de Onda $\Lambda$ | Fracción en Capa ($z \le 10$ m) | Fracción en Semiespacio ($z > 10$ m) | Régimen Físico |
|:---:|:---:|:---:|:---:|:---|
| **3 Hz** | ~192 m | **25.5 %** | **74.5 %** | Muestreo profundo: onda sensible casi enteramente al basamento. |
| **6 Hz** | ~87 m | **81.8 %** | **18.2 %** | Muestreo de transición e interfaz capa-sustrato. |
| **10 Hz** | ~27 m | **97.8 %** | **2.2 %** | Confinamiento casi total en la capa superficial. |
| **20 Hz** | ~10 m | **99.9 %** | **0.1 %** | Onda superficial pura: ciega a lo que exista bajo $10$ m. |

---

## 2. Interpretación de la Variación de Parámetros de la Capa

### A. Variación del Espesor $h$ (Escalamiento $f \cdot h$)
- En un medio estratificado de una capa sobre semiespacio, la única dimensión de longitud estructural es el espesor $h$.
- En consecuencia, la ecuación de dispersión adimensional depende exclusivamente del producto adyacente **$f \cdot h$** (o $h / \Lambda$).
- **Efecto observado**: Duplicar el espesor de la capa ($h: 10\text{ m} \to 20\text{ m}$) desplaza la curva de dispersión exactamente a la mitad de frecuencia ($f \to f/2$).
- La frecuencia del mínimo de velocidad de grupo (fase de Airy) se reduce a la mitad:
  - Para $h = 10$ m: $f_{\mathrm{Airy}} \approx 9.6$ Hz ($v_g = 76.5$ m/s).
  - Para $h = 20$ m: $f_{\mathrm{Airy}} \approx 4.8$ Hz ($v_g = 76.6$ m/s).

### B. Variación de la Velocidad de Corte $v_{S1}$
- $v_{S1}$ controla directamente la rigidez a corte de la capa superior.
- **Asíntota de alta frecuencia ($f \to \infty$)**: $\Lambda \ll h$, por lo que la onda queda totalmente atrapada en el estrato superior y se propaga como una onda de Rayleigh sobre un semiespacio homogéneo con las propiedades de la capa:
  $$c_R(f \to \infty) = \xi_1 \, v_{S1} \approx 0.947 \, v_{S1}$$
- Al aumentar $v_{S1}$ de $200$ m/s a $300$ m/s, la asíntota de alta frecuencia asciende directamente de $189.5$ m/s a $279.8$ m/s.
- **Asíntota de baja frecuencia ($f \to 0$)**: $\Lambda \gg h$, por lo que la capa es transparente para la onda y $c_R$ tiende a la velocidad de Rayleigh del semiespacio inferior ($606.1$ m/s).

---

## 3. Velocidad de Fase ($c_R$) vs. Velocidad de Grupo ($v_g$) y Fase de Airy

1. **Velocidad de fase $c_R = \omega / k$**:
   - Es la velocidad a la que se propagan los frentes de onda (crestas y valles individuales).
   - Es el parámetro que se mide experimentalmente en el procesado espectral de ondas superficiales (MASW / SASW).
2. **Velocidad de grupo $v_g = d\omega / dk$**:
   - Es la velocidad de propagación de la envolvente del paquete de ondas y representa el transporte de energía física.
   - En un medio normalmente dispersivo donde $dc_R / df < 0$, se cumple rigurosamente que **$v_g < c_R$**.
3. **Fase de Airy**:
   - Se produce en el mínimo local de la velocidad de grupo ($dv_g / df = 0$).
   - Al coincidir la velocidad de grupo para un rango de frecuencias adyacentes, estas componentes llegan simultáneamente a la estación receptora, interfiriendo constructivamente y generando un tren de ondas de gran amplitud y duración en el sismograma.
   - Para el Modelo A ocurre a **9.65 Hz** con $v_g = 76.52$ m/s.
   - Para el Modelo B ocurre a **6.64 Hz** con $v_g = 163.31$ m/s.

---

## 4. Aplicación Geotécnica: Inversión Sísmica y $V_{s30}$

- Debido a que cada frecuencia muestrea una profundidad diferente, la curva de dispersión experimental $c_R(f)$ constituye una tomografía implícita del subsuelo.
- El problema inverso consiste en ajustar los parámetros elásticos ($h_i, v_{Si}$) minimizando la discrepancia $\chi^2$ entre las velocidades calculadas y las observadas en terreno.
- Si solo se registran frecuencias altas ($f \ge 15$ Hz), el espesor $h$ del estrato queda matemáticamente indeterminado (no-unicidad del problema inverso), puesto que la onda no penetra lo suficiente para detectar la interfaz basal.
- Esta metodología permite obtener el perfil $V_S(z)$ para determinar la velocidad promedio en los primeros 30 metros ($V_{s30}$), requerida por la **Norma Técnica E.030 de Diseño Sismorresistente** para clasificar el tipo de suelo (S1, S2, S3 o S4) en estudios de microzonificación urbana.
