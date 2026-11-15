"""
Curvas de dispersión de Rayleigh (cR(f), vg(f)) para los Modelos A y B del póster,
mas las pruebas de sensibilidad aisladas (solo h, solo vS) desde el Modelo A.

Usa disba (metodo de Dunkin) para resolver la ecuacion secular del modo fundamental.
Unidades de entrada en el poster: m, m/s, kg/m^3. disba espera km, km/s, g/cm^3.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from disba import PhaseDispersion, GroupDispersion

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
F_MIN, F_MAX, N_FREQ = 1.0, 60.0, 200


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
    """cR(f) y vg(f) del modo fundamental de Rayleigh, en f = 1..60 Hz."""
    freq = np.linspace(F_MIN, F_MAX, N_FREQ)
    period = np.sort(1.0 / freq)  # disba exige el eje de periodos ascendente

    pd = PhaseDispersion(thickness, vp, vs, rho)
    gd = GroupDispersion(thickness, vp, vs, rho)

    cp = pd(period, mode=0, wave="rayleigh")
    cg = gd(period, mode=0, wave="rayleigh")

    # disba puede devolver menos periodos que los pedidos si el modo
    # no se resuelve en todo el rango; se reconstruye f a partir de cp.period
    f_phase = 1.0 / cp.period
    f_group = 1.0 / cg.period
    return f_phase, cp.velocity * 1000.0, f_group, cg.velocity * 1000.0  # m/s


def slugify(name):
    for ch in " :=/":
        name = name.replace(ch, "_")
    return name


def save_csv(name, f_phase, cR, f_group, vg):
    path = OUT_DIR / f"{slugify(name)}.csv"
    n = max(len(f_phase), len(f_group))
    with open(path, "w") as fh:
        fh.write("f_Hz_fase,cR_mps,f_Hz_grupo,vg_mps\n")
        for i in range(n):
            row = [
                f"{f_phase[i]:.4f}" if i < len(f_phase) else "",
                f"{cR[i]:.4f}" if i < len(cR) else "",
                f"{f_group[i]:.4f}" if i < len(f_group) else "",
                f"{vg[i]:.4f}" if i < len(vg) else "",
            ]
            fh.write(",".join(row) + "\n")
    return path


def plot_models(results, title, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    for name, (f_phase, cR, f_group, vg) in results.items():
        ax1.plot(f_phase, cR, label=name)
        ax2.plot(f_group, vg, label=name)
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
        f_phase, cR, f_group, vg = dispersion_curves(thickness, vp, vs, rho)
        results[name] = (f_phase, cR, f_group, vg)
        save_csv(name, f_phase, cR, f_group, vg)
        print(f"{name}: cR {cR.min():.1f}-{cR.max():.1f} m/s, vg {vg.min():.1f}-{vg.max():.1f} m/s")

    comparacion = {k: results[k] for k in ("Modelo A", "Modelo B")}
    plot_models(comparacion, "Modelo A vs Modelo B", "modelos_A_vs_B.png")

    sensibilidad_h = {k: results[k] for k in ("Modelo A", "Sensibilidad: solo h=20m")}
    plot_models(sensibilidad_h, "Sensibilidad aislada: solo h (10m -> 20m)", "sensibilidad_h.png")

    sensibilidad_vs = {k: results[k] for k in ("Modelo A", "Sensibilidad: solo vS=300m/s")}
    plot_models(sensibilidad_vs, "Sensibilidad aislada: solo vS (200 -> 300 m/s)", "sensibilidad_vs.png")

    print(f"\nCSV y figuras guardados en {OUT_DIR}")


if __name__ == "__main__":
    main()
