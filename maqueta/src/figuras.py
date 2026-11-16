"""Figuras de la maqueta B+C (SVG a tamaño real, 1 pt = 1 pt). Imprime las cifras usadas en el texto."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, NullFormatter
from disba import PhaseDispersion, GroupDispersion, PhaseSensitivity

HERE = Path(__file__).resolve().parent
for f in (HERE / "ttf").glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))
NAVY, TEAL, ORANGE, GREY, SEC, LIGHT, PALE = "#102A43", "#006C78", "#AD481F", "#8A9BA8", "#40596D", "#E6F0F2", "#BCDBE1"
plt.rcParams.update({
    "font.family": "Source Sans 3", "font.size": 24, "svg.fonttype": "path",
    "mathtext.fontset": "custom", "mathtext.rm": "Source Sans 3", "mathtext.it": "Source Sans 3:italic",
    "mathtext.bf": "Source Sans 3:bold",
    "axes.edgecolor": SEC, "axes.labelcolor": NAVY, "xtick.color": SEC, "ytick.color": SEC,
    "axes.linewidth": 1.2, "xtick.labelsize": 23, "ytick.labelsize": 23, "axes.labelsize": 25,
    "legend.fontsize": 22, "legend.frameon": False, "axes.spines.top": False, "axes.spines.right": False,
    "grid.color": "#D5DEE3", "grid.linewidth": 1.0, "figure.facecolor": "none", "axes.facecolor": "none",
    "savefig.facecolor": "none",
})
W = 717 / 72  # ancho de columna en pulgadas
NUM = {}


def model(h, vs1, vp1=600.0, rho1=1800.0):
    return (np.array([h, 0]) / 1000, np.array([vp1, 1300]) / 1000,
            np.array([vs1, 650]) / 1000, np.array([rho1, 2100]) / 1000)


def phase(m, f):
    T = np.sort(1 / np.asarray(f, float))
    cp = PhaseDispersion(*m)(T, 0, "rayleigh")
    return 1 / cp.period[::-1], cp.velocity[::-1] * 1000


def curves(m, f=None):
    """c_R(f) de disba y v_g por la ec. (9) con diferencias centrales, Δf = 0,05 Hz (auditoría E2/E3:
    el v_g interno de disba se desvía hasta 1,1 m/s en el mínimo)."""
    ff = np.arange(0.95, 60.0501, 0.05)
    fp, c = phase(m, ff)
    vg = c / (1 - (fp / c) * np.gradient(c, fp))
    keep = (fp >= 1) & (fp <= 60)
    return fp[keep], c[keep], fp[keep], vg[keep]


def logx(ax, lo=1, hi=60):
    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50]))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50"])


def save(fig, name):
    fig.savefig(HERE / name, transparent=True)
    plt.close(fig)


f = np.geomspace(1, 60, 400)
M = {"A": model(10, 200), "B": model(20, 300), "h20": model(20, 200), "vs300": model(10, 300)}
C = {k: curves(m, f) for k, m in M.items()}
ASYM = {"capa A": 189.5, "capa B": 279.8, "semiespacio": 606.1}

# ---------- 1. Suelos A y B (tabla + perfil + Vs30) ----------
fig = plt.figure(figsize=(W, 380 / 72))
ax = fig.add_axes([0.11, 0.16, 0.87, 0.72])
ax.set_xlim(0, 100)
ax.set_ylim(35, 0)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_yticks([0, 10, 20, 30])
ax.set_ylabel("z (m)", labelpad=6)
vs30 = {}
for x0, (name, h, vs, col) in zip((2, 52), (("Modelo A", 10, 200, TEAL), ("Modelo B", 20, 300, ORANGE))):
    ax.add_patch(plt.Rectangle((x0, 0), 14, h, fc=LIGHT, ec=col, lw=2.4))
    ax.add_patch(plt.Rectangle((x0, h), 14, 35 - h, fc=PALE, ec=SEC, lw=1.2))
    ax.text(x0 + 7, h / 2, f"{h} m", ha="center", va="center", fontsize=22, color=NAVY, weight="bold")
    ax.text(x0 + 16, h / 2, f"$v_s$ {vs} · $v_p$ 600\nρ 1800", va="center", fontsize=21, color=NAVY, linespacing=1.15)
    ax.text(x0 + 16, h + (35 - h) / 2, "$v_s$ 650 · $v_p$ 1300\nρ 2100  (semiespacio)", va="center", fontsize=21, color=SEC, linespacing=1.15)
    ax.text(x0, -1.6, name, fontsize=25, color=col, weight="bold", va="bottom")
    v = 30 / (h / vs + (30 - h) / 650)
    vs30[name] = v
    ax.text(x0, 37.2, f"$V_{{s30}}$ = {v:.0f} m/s  →  E.030: S2", fontsize=22, color=NAVY, va="top", weight="semibold")
NUM["vs30"] = {k: round(v, 1) for k, v in vs30.items()}
save(fig, "fig_suelos.svg")

# ---------- 2. Dispersión A vs B (log f, asíntotas, Airy) ----------
fig, axs = plt.subplots(2, 1, figsize=(W, 740 / 72), sharex=True, gridspec_kw={"hspace": 0.14})
fig.subplots_adjust(left=0.13, right=0.83, top=0.93, bottom=0.10)
for ax, idx, ttl in ((axs[0], 1, "Velocidad de fase $c_R$ (m/s)"), (axs[1], 3, "Velocidad de grupo $v_g$ (m/s)")):
    for k, col, ls, lab in (("A", TEAL, "-", "Modelo A"), ("B", ORANGE, "--", "Modelo B")):
        ax.plot(C[k][idx - 1], C[k][idx], color=col, ls=ls, lw=3.2, label=lab)
    for lab, v in ASYM.items():
        ax.axhline(v, color=GREY, ls=":", lw=1.8)
    ax.set_ylim(50, 660)
    ax.set_yticks([100, 200, 300, 400, 500, 600])
    ax.grid(True, which="major", axis="both")
    ax.set_title(ttl, loc="left", fontsize=25, color=NAVY, weight="bold", pad=8)
    logx(ax)
for lab, v in ASYM.items():
    axs[0].text(64, v + (14 if lab == "capa B" else -14 if lab == "capa A" else 0), f"{v:.1f} {lab}".replace(".", ",").replace("semiespacio", "semiesp."), fontsize=18, color=SEC, va="center")
airy = {}
for k, col in (("A", TEAL), ("B", ORANGE)):
    fg, g = C[k][2], C[k][3]
    i = np.argmin(g)
    a2, a1, _ = np.polyfit(fg[i - 1:i + 2] - fg[i], g[i - 1:i + 2], 2)   # vértice de la parábola por 3 puntos
    fmin = fg[i] - a1 / (2 * a2)
    gmin = float(np.polyval([a2, a1, _], fmin - fg[i]))
    airy[k] = (round(float(fmin), 3), round(gmin, 2))
    axs[1].plot(fmin, gmin, "o", ms=12, mfc="white", mec=col, mew=3)
axs[1].annotate("fase de Airy\n(mínimo de $v_g$)", xy=(airy["A"][0], airy["A"][1]), xytext=(17, 70), fontsize=21, color=NAVY,
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.6), va="bottom")
NUM["airy"] = airy
axs[1].set_xlabel("Frecuencia f (Hz, escala log)")
axs[0].legend(loc="lower left", ncol=1, handlelength=2.2)
save(fig, "fig_dispersion.svg")

# ---------- 3. Cambios aislados ----------
fig, ax = plt.subplots(figsize=(W, 380 / 72))
fig.subplots_adjust(left=0.13, right=0.97, top=0.95, bottom=0.21)
ax.plot(C["A"][0], C["A"][1], color=TEAL, lw=3.2, label="A (h 10 m, $v_s$ 200)")
ax.plot(C["h20"][0], C["h20"][1], color=NAVY, lw=2.8, ls="--", label="solo h → 20 m")
ax.plot(C["vs300"][0], C["vs300"][1], color=NAVY, lw=2.8, ls=":", label="solo $v_s$ → 300")
ax.set_ylim(150, 640)
ax.set_yticks([200, 300, 400, 500, 600])
ax.grid(True)
logx(ax)
ax.set_xlabel("Frecuencia f (Hz, escala log)")
ax.set_ylabel("$c_R$ (m/s)")
ax.annotate("", xy=(4.85, 400), xytext=(9.7, 400), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
ax.text(6.9, 412, "f ÷ 2", fontsize=22, color=NAVY, ha="center", va="bottom", weight="bold")
ax.annotate("", xy=(40, 279.8), xytext=(40, 192), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
ax.text(37, 252, "la asíntota sube con $v_s$", fontsize=20, color=NAVY, ha="right", va="center")
ax.legend(loc="upper right", fontsize=20)
# verificación del escalamiento f·h
fa, ca = C["A"][0], C["A"][1]
fh, ch = C["h20"][0], C["h20"][1]
NUM["fh_scaling_max_diff"] = round(float(np.max(np.abs(np.interp(2 * fh[fh <= 30], fa, ca) - ch[fh <= 30]))), 3)
save(fig, "fig_aislados.svg")

# ---------- 4. Kernels de sensibilidad (Modelo A) ----------
dz, zmax = 1.0, 160.0
nz = int(zmax / dz)
zc = (np.arange(nz) + 0.5) * dz
th = np.full(nz + 1, dz)
th[-1] = 0
inlay = np.r_[zc < 10, False]
vs = np.where(inlay, 200, 650.0)
vp = np.where(inlay, 600, 1300.0)
rho = np.where(inlay, 1800, 2100.0)
ps = PhaseSensitivity(th / 1000, vp / 1000, vs / 1000, rho / 1000)
fig, ax = plt.subplots(figsize=(W, 400 / 72))
fig.subplots_adjust(left=0.13, right=0.97, top=0.80, bottom=0.18)
kern = {}
for fq, col in ((3, "#8CC9D1"), (6, "#3C9DA8"), (10, TEAL), (20, NAVY)):
    kk = ps(1 / fq, 0, "rayleigh", "velocity_s").kernel
    frac = float(kk[:-1][zc < 10].sum() / kk.sum())
    lam = float(np.interp(fq, C["A"][0], C["A"][1])) / fq
    dens = kk[:-1] / dz
    kern[fq] = {"lambda_m": round(lam, 1), "frac_capa": round(frac, 3), "z_pico": float(zc[np.argmax(dens)])}
    ax.stairs(dens / dens.max(), np.r_[zc - dz / 2, zc[-1] + dz / 2], orientation="horizontal", color=col, lw=3, baseline=None,
              label=f"{fq} Hz · Λ {lam:.0f} m · {frac * 100:.0f} %")
ax.axhline(10, color=GREY, ls="--", lw=1.8)
ax.text(1.0, 11.0, "interfaz (10 m)", fontsize=20, color=SEC, ha="right", va="top")
ax.set_ylim(60, 0)
ax.set_xlim(0, 1.05)
ax.set_xlabel("∂$c_R$/∂$v_s$(z), normalizado")
ax.set_ylabel("z (m)")
ax.legend(loc="lower left", bbox_to_anchor=(-0.02, 1.01), ncol=2, fontsize=20, handlelength=1.4, columnspacing=1.2)
NUM["kernels"] = kern
save(fig, "fig_kernels.svg")

# ---------- 5. Inversión de prueba ----------
rng = np.random.default_rng(0)
fo = np.geomspace(3, 40, 25)
_, cobs = phase(M["A"], fo)
sig = 0.02 * cobs
cobs_n = cobs + rng.normal(0, sig)
hs = np.arange(4, 40.01, 0.5)
v1s = np.arange(150, 250.01, 2.0)
hi = fo >= 15
chi_all = np.full((len(v1s), len(hs)), np.nan)
chi_hi = np.full_like(chi_all, np.nan)
for i, v in enumerate(v1s):
    for j, h in enumerate(hs):
        T = np.sort(1 / fo)
        try:
            cp = PhaseDispersion(*model(h, v))(T, 0, "rayleigh")
        except Exception:
            continue
        if len(cp.velocity) != len(fo):
            continue
        cc = cp.velocity[::-1] * 1000
        r = (cc - cobs_n) / sig
        chi_all[i, j] = np.sqrt(np.mean(r**2))
        chi_hi[i, j] = np.sqrt(np.mean(r[hi] ** 2))
fig, ax = plt.subplots(figsize=(W, 390 / 72))
fig.subplots_adjust(left=0.13, right=0.97, top=0.95, bottom=0.2)
HH, VV = np.meshgrid(hs, v1s)
ax.contourf(HH, VV, np.nan_to_num(chi_hi, nan=99), levels=[0, 1.5], colors=[PALE])
ax.contour(HH, VV, np.nan_to_num(chi_hi, nan=99), levels=[1.5], colors=[NAVY], linewidths=2.2, linestyles="--")
ax.contourf(HH, VV, np.nan_to_num(chi_all, nan=99), levels=[0, 1.5], colors=[TEAL])
ax.plot(10, 200, marker="*", ms=22, color="white", mec=NAVY, mew=1.8)
ax.set_xlabel("Espesor de la capa h (m)")
ax.set_ylabel("$v_s$ de la capa (m/s)")
ax.set_xlim(4, 40)
ax.set_ylim(150, 250)
ax.grid(True)
ax.text(11.5, 236, "solo f ≥ 15 Hz: χ ≤ 1,5", fontsize=21, color=NAVY)
ax.text(12.0, 168, "3–40 Hz: χ ≤ 1,5", fontsize=21, color=TEAL, weight="bold")
ax.annotate("", xy=(10.6, 198), xytext=(12.5, 175), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
okA = chi_all <= 1.5
okH = chi_hi <= 1.5
NUM["inversion"] = {
    "chi_min": round(float(np.nanmin(chi_all)), 2),
    "full_h": [float(HH[okA].min()), float(HH[okA].max())], "full_vs": [float(VV[okA].min()), float(VV[okA].max())],
    "hi_h": [float(HH[okH].min()), float(HH[okH].max())], "hi_vs": [float(VV[okH].min()), float(VV[okH].max())],
}
save(fig, "fig_inversion.svg")
print(json.dumps(NUM, indent=1, ensure_ascii=False))
