# Ondas Sísmicas Superficiales: Modos de Rayleigh, Dispersión e Inversión del Subsuelo

**Universidad de Ingeniería y Tecnología (UTEC)**  
**Curso:** Óptica y Ondas (2026-1) — Trabajo Dirigido 2 (TD2)  
**Grupo 6:**  
- Danna Gala  
- Ary Sanchez  
- Eduardo Guevara  
- Mendoza Gracia  

**Docentes:** Marco Cuyubamba y Eduardo Castillo  

---

## 1. Descripción del Proyecto

Este proyecto estudia la propagación, dispersión y sensibilidad de las **ondas sísmicas superficiales de Rayleigh** en medios elásticos estratificados, y su aplicación en la caracterización geotécnica mediante el método de Análisis Multicanal de Ondas Superficiales (**MASW**) y la estimación de $V_{s30}$ conforme a la **Norma Técnica E.030 (Diseño Sismorresistente)** de Perú.

### Objetivos y Actividades Cubiertas:
1. **Ondas P, S y Rayleigh:** Análisis de ondas de cuerpo longitudinales (P) y transversales (S) frente a las ondas superficiales de Rayleigh, modelando sus órbitas elípticas retrógradas superficiales y prógradas en profundidad, y su decaimiento exponencial ($\sim 1\Lambda$).
2. **Ecuación de Navier y Potenciales de Helmholtz:** Desacoplamiento de la ecuación de movimiento en potenciales escalar $\phi$ y vectorial $\psi$, deduciendo las velocidades $v_P = \sqrt{(\lambda+2\mu)/\rho}$ y $v_S = \sqrt{\mu/\rho}$.
3. **Condición de Frontera Libre y Ecuación Secular:** Imposición de tracción nula en la superficie libre ($\sigma_{zz} = \sigma_{xz} = 0$), obteniendo la ecuación secular para la velocidad de fase $c_R = \omega/k$.
4. **Relación $c_R < v_S < v_P$ y Dispersión:** Demostración analítica de la existencia y unicidad de la velocidad de Rayleigh, y análisis del efecto del espesor de capa $h$ y su velocidad transversal $v_S$.
5. **Velocidad de Fase ($c_R$) vs. Velocidad de Grupo ($v_g$):** Cálculo analítico de $v_g = d\omega/dk = c_R / [1 - (f/c_R) dc_R/df]$ y localización precisa de la **fase de Airy** (mínimo de velocidad de grupo).
6. **Simulación Numérica y Sensibilidad en Profundidad:** Implementación en Python para generar curvas $c_R(f)$ y $v_g(f)$ de los modelos base y de dos variaciones aisladas de $h$ y $v_S$. El repositorio conserva además resultados de sensibilidad en profundidad y su interpretación física.

---

## 2. Estructura del Repositorio

```text
.
├── README.md                      # Documentación general del proyecto
├── requirements.txt               # Dependencias del proyecto (disba, numpy, matplotlib, etc.)
├── scripts/
│   └── dispersion.py              # Script principal: curvas cR, vg y sensibilidades aisladas
├── outputs/                       # Resultados versionados y resultados generados
│   ├── 1_modelos_A_vs_B.png       # Figura versionada del contraste entre los modelos A y B
│   ├── 2_variacion_espesor_h.png  # Figura versionada de variación del espesor
│   ├── 3_variacion_velocidad_vs.png # Figura versionada de variación de vS
│   ├── 4_sensibilidad_profundidad.png # Figura versionada de sensibilidad en profundidad
│   ├── interpretacion_sensibilidad.md # Interpretación física versionada
│   └── *.csv                      # Tablas versionadas de dispersión (f, cR, vg)
├── maqueta/
│   ├── maqueta_utec.pdf           # Póster oficial en plantilla horizontal A0 de UTEC
│   ├── maqueta_utec.png           # Vista previa en alta resolución del póster
│   ├── maqueta_utec_ecuaciones.pdf# Variante del póster con subcolumnas de ecuaciones
│   ├── derivacion_completa.md     # Derivación matemática formal paso a paso
│   └── figuras_utec/              # Figuras vectoriales (SVG) incorporadas en el póster
├── exposicion/
│   └── guion.md                   # Guion estructurado para la presentación oral del equipo
└── verificacion/                  # Suite de validación matemática y física independiente
    ├── solver_mp.py               # Solver de alta precisión (matriz 6x6 en mpmath, sin disba)
    ├── simbolico.py               # Comprobación analítica con SymPy de las ecs. (1)–(8)
    ├── numerico.py                # Contraste cuantitativo entre métodos
    └── inv_check.py               # Verificación de unicidad e inversión
```

---

## 3. Instalación y Ejecución

### Requisitos Previos:
- Python 3.10 o superior.
- Las versiones concretas de las dependencias están indicadas en `requirements.txt`.

### Configuración del Entorno:

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la Simulación:

```bash
python scripts/dispersion.py
```

El script ejecutará automáticamente:
1. El cálculo de $c_R(f)$ y $v_g(f)$ (1 a 60 Hz) para el **Modelo A** ($h=10$ m, $v_{S1}=200$ m/s) y **Modelo B** ($h=20$ m, $v_{S1}=300$ m/s) sobre un semiespacio rocoso ($v_{S2}=650$ m/s, $v_{P2}=1300$ m/s).
2. El cálculo de dos sensibilidades aisladas desde el Modelo A: cambiar $h$ de 10 m a 20 m y cambiar $v_{S1}$ de 200 m/s a 300 m/s.
3. La exportación de cuatro archivos CSV y tres figuras en `outputs/`. Los nombres de las figuras generadas por este script son `modelos_A_vs_B.png`, `sensibilidad_h.png` y `sensibilidad_vs.png`.

El script no realiza un barrido de varios valores de $h$ o $v_{S1}$, no calcula kernels de sensibilidad en profundidad y no genera `interpretacion_sensibilidad.md`; esos archivos son resultados versionados de análisis previos.

### Ejecutar la Validación Matemática Independiente:

```bash
python verificacion/simbolico.py
python verificacion/numerico.py
python verificacion/inv_check.py
```

`simbolico.py`, `numerico.py` e `inv_check.py` imprimen sus comprobaciones en la terminal. `numerico.py` importa el solver independiente de alta precisión definido en `solver_mp.py`; ejecutar `solver_mp.py` directamente no ejecuta una comprobación.

---

## 4. Síntesis de Resultados y Física de la Onda

### A. Escalamiento por Espesor de Capa ($f \cdot h$)
En un suelo constituido por una capa sobre un semiespacio, la única dimensión longitudinal intrínseca es el espesor $h$. Como consecuencia directa, la dispersión está gobernada por el producto adimensional $f \cdot h$:
- Duplicar el espesor de la capa ($10\text{ m} \to 20\text{ m}$) divide a la mitad la frecuencia de transición.
- La **fase de Airy** (mínimo de velocidad de grupo) ocurre a **9.65 Hz** para $h=10$ m, y se desplaza a **4.83 Hz** para $h=20$ m.

### B. Control Asintótico por la Velocidad $v_S$
- **Alta frecuencia ($f \to \infty$, $\Lambda \ll h$):** La longitud de onda es pequeña en comparación con el espesor de la capa; la onda queda confinada en ella y su velocidad tiende a la velocidad de Rayleigh de la capa:
  $$c_R \to \xi_1 v_{S1} \approx 0.947 \, v_{S1}$$
- **Baja frecuencia ($f \to 0$, $\Lambda \gg h$):** La onda penetra profundamente en el semiespacio, haciéndose insensible a la capa superficial; la velocidad tiende a la del sustrato rocoso:
  $$c_R \to \xi_2 v_{S2} \approx 0.933 \, v_{S2} = 606.1\text{ m/s}$$

### C. Sensibilidad con la Profundidad
La profundidad efectiva de muestreo de la onda de Rayleigh escala directamente con su longitud de onda $\Lambda(f) = c_R(f) / f$:
- **A 20 Hz ($\Lambda \approx 9.6$ m):** El **99.9 %** de la sensibilidad se ubica en los primeros 10 metros. La onda no detecta el semiespacio.
- **A 10 Hz ($\Lambda \approx 27.0$ m):** El **97.8 %** de la sensibilidad permanece en la capa.
- **A 6 Hz ($\Lambda \approx 86.8$ m):** Zona de transición; el **81.8 %** de la sensibilidad está en la capa y el **18.2 %** en el sustrato.
- **A 3 Hz ($\Lambda \approx 191.8$ m):** La onda penetra profundamente; solo el **25.5 %** de la sensibilidad proviene de la capa, muestreando mayoritariamente el lecho rocoso profundo.

Esta dependencia espectral de la profundidad de muestreo es el fundamento que permite realizar la **inversión sísmica (tomografía del subsuelo)** a partir de mediciones no invasivas en superficie (MASW).

---

## 5. Referencias Bibliográficas

1. **Rayleigh, L. (1885).** On waves propagated along the plane surface of an elastic solid. *Proc. London Math. Soc.*, s1-17(1), 4–11.
2. **Aki, K. & Richards, P. G. (2002).** *Quantitative Seismology* (2.ª ed.). University Science Books.
3. **Ministerio de Vivienda, Construcción y Saneamiento (2018).** *Norma Técnica E.030 Diseño Sismorresistente*. Reglamento Nacional de Edificaciones, Perú.
4. **Dunkin, J. W. (1965).** Computation of modal solutions in layered, elastic media at high frequencies. *BSSA*, 55(2), 335–358.
5. **Luu, K.** *disba: Numba-accelerated computation of surface wave dispersion* (v0.7.0). Zenodo.
6. **Xia, J., Miller, R. D. & Park, C. B. (1999).** Estimation of near-surface shear-wave velocity by inversion of Rayleigh waves. *Geophysics*, 64(3), 691–700.
7. **Park, C. B., Miller, R. D. & Xia, J. (1999).** Multichannel analysis of surface waves. *Geophysics*, 64(3), 800–808.
