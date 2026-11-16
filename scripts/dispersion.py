"""
Curvas de dispersión de Rayleigh (cR(f), vg(f)) para los Modelos A y B del póster,
mas las pruebas de sensibilidad aisladas (solo h, solo vS) desde el Modelo A.

Usa disba (metodo de Dunkin) para resolver la ecuacion secular del modo fundamental.
Unidades de entrada en el poster: m, m/s, kg/m^3. disba espera km, km/s, g/cm^3.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from disba import PhaseDispersion

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
F_MIN, F_MAX, DF = 1.0, 60.0, 0.05


def build_layer_model(h_m, vp_mps, vs_mps, rho_kgm3, vp_half, vs_half, rho_half):
    """Capa sobre semiespacio, en unidades disba (km, km/s, g/cm3)."""
    thickness = np.array([h_m / 1000.0, 0.0])
    vp = np.array([vp_mps, vp_half]) / 1000.0
    vs = np.array([vs_mps, vs_half]) / 1000.0
    rho = np.array([rho_kgm3, rho_half]) / 1000.0
    return thickness, vp, vs, rho


# Semiespacio comun a todos los modelos del poster
HALF_SPACE = dict(vp_half=1300.0, vs_half=650.0, rho_half=2100.0)

MODELS = {
    "Modelo A": build_layer_model(h_m=10.0, vp_mps=600.0, vs_mps=200.0, rho_kgm3=1800.0, **HALF_SPACE),
    "Modelo B": build_layer_model(h_m=20.0, vp_mps=600.0, vs_mps=300.0, rho_kgm3=1800.0, **HALF_SPACE),
    "Sensibilidad: solo h=20m": build_layer_model(h_m=20.0, vp_mps=600.0, vs_mps=200.0, rho_kgm3=1800.0, **HALF_SPACE),
    "Sensibilidad: solo vS=300m/s": build_layer_model(h_m=10.0, vp_mps=600.0, vs_mps=300.0, rho_kgm3=1800.0, **HALF_SPACE),
}


def dispersion_curves(thickness, vp, vs, rho):
    """cR(f) y vg(f) del modo fundamental de Rayleigh, en f = 1..60 Hz (m/s).

    vg se obtiene con la ec. (9) del póster, vg = cR / [1 - (f/cR) dcR/df], por diferencias
    centrales con paso DF. No se usa GroupDispersion de disba: frente a una referencia de alta
    precisión se desvía hasta 1,1 m/s en el mínimo de vg (ver auditoria/auditoria_matematica.md).
    """
    freq = np.arange(F_MIN - DF, F_MAX + 1.5 * DF, DF)  # un punto extra a cada lado para la derivada
    period = np.sort(1.0 / freq)  # disba exige el eje de periodos ascendente
    cp = PhaseDispersion(thickness, vp, vs, rho)(period, mode=0, wave="rayleigh")

    # disba puede devolver menos periodos si el modo no se resuelve en todo el rango
    f = 1.0 / cp.period[::-1]
    c = cp.velocity[::-1] * 1000.0
    vg = c / (1.0 - (f / c) * np.gradient(c, f))
    keep = (f >= F_MIN - 1e-9) & (f <= F_MAX + 1e-9)
    return f[keep], c[keep], vg[keep]


def airy_minimum(f, vg):
    """Mínimo de vg refinado con el vértice de la parábola por los 3 puntos más bajos."""
    i = int(np.argmin(vg))
    if i == 0 or i == len(vg) - 1:
        return float(f[i]), float(vg[i])
    a2, a1, a0 = np.polyfit(f[i - 1:i + 2] - f[i], vg[i - 1:i + 2], 2)
    x = -a1 / (2 * a2)
    return float(f[i] + x), float(np.polyval([a2, a1, a0], x))


def slugify(name):
    for ch in " :=/":
        name = name.replace(ch, "_")
    return name


def save_csv(name, f, cR, vg):
    path = OUT_DIR / f"{slugify(name)}.csv"
    np.savetxt(path, np.column_stack([f, cR, vg]), delimiter=",", fmt="%.4f",
               header="f_Hz,cR_mps,vg_mps", comments="")
    return path


def plot_models(results, title, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    for name, (f, cR, vg) in results.items():
        ax1.plot(f, cR, label=name)
        ax2.plot(f, vg, label=name)
    ax1.set_xlabel("f (Hz)"); ax1.set_ylabel("c_R (m/s)"); ax1.set_title("Velocidad de fase")
    ax2.set_xlabel("f (Hz)"); ax2.set_ylabel("v_g (m/s)"); ax2.set_title("Velocidad de grupo")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(OUT_DIR / filename)
    plt.close(fig)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    results = {}
    for name, (thickness, vp, vs, rho) in MODELS.items():
        f, cR, vg = dispersion_curves(thickness, vp, vs, rho)
        results[name] = (f, cR, vg)
        save_csv(name, f, cR, vg)
        fa, va = airy_minimum(f, vg)
        print(f"{name}: cR {cR.min():.1f}-{cR.max():.1f} m/s; mínimo de vg (Airy) {va:.2f} m/s a {fa:.3f} Hz")

    comparacion = {k: results[k] for k in ("Modelo A", "Modelo B")}
    plot_models(comparacion, "Modelo A vs Modelo B", "modelos_A_vs_B.png")

    sensibilidad_h = {k: results[k] for k in ("Modelo A", "Sensibilidad: solo h=20m")}
    plot_models(sensibilidad_h, "Sensibilidad aislada: solo h (10m -> 20m)", "sensibilidad_h.png")

    sensibilidad_vs = {k: results[k] for k in ("Modelo A", "Sensibilidad: solo vS=300m/s")}
    plot_models(sensibilidad_vs, "Sensibilidad aislada: solo vS (200 -> 300 m/s)", "sensibilidad_vs.png")

    print(f"\nCSV y figuras guardados en {OUT_DIR}")


if __name__ == "__main__":
    main()
