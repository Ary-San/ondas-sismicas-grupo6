"""Figuras para la versión en plantilla UTEC (A0 horizontal). Mismos cálculos que figuras.py (v_g por ec. 9)."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, NullFormatter
from disba import PhaseDispersion, PhaseSensitivity

HERE = Path(__file__).resolve().parent
for f in (HERE / "ttf").glob("OpenSans-*.ttf"):
    font_manager.fontManager.addfont(str(f))
NAVY, TEAL, ORANGE, GREY, SEC, LIGHT, PALE, INK = "#102A43", "#006C78", "#AD481F", "#8A9BA8", "#3D4F5C", "#E6F0F2", "#BCDBE1", "#231F20"
plt.rcParams.update({
    "font.family": "Open Sans", "font.size": 22, "svg.fonttype": "path",
    "mathtext.fontset": "custom", "mathtext.rm": "Open Sans", "mathtext.it": "Open Sans:italic", "mathtext.bf": "Open Sans:bold",
    "axes.edgecolor": SEC, "axes.labelcolor": INK, "xtick.color": SEC, "ytick.color": SEC, "axes.linewidth": 1.2,
    "xtick.labelsize": 21, "ytick.labelsize": 21, "axes.labelsize": 22, "legend.fontsize": 20, "legend.frameon": False,
    "axes.spines.top": False, "axes.spines.right": False, "grid.color": "#DDE3E7", "grid.linewidth": 1.0,
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
})
IN = lambda pt: pt / 72
NUM = {}


def model(h, vs1, vp1=600.0, rho1=1800.0):
    return (np.array([h, 0]) / 1000, np.array([vp1, 1300]) / 1000, np.array([vs1, 650]) / 1000, np.array([rho1, 2100]) / 1000)


def phase(m, f):
    T = np.sort(1 / np.asarray(f, float))
    cp = PhaseDispersion(*m)(T, 0, "rayleigh")
    return 1 / cp.period[::-1], cp.velocity[::-1] * 1000


def curves(m):
    ff = np.arange(0.95, 60.0501, 0.05)
    fp, c = phase(m, ff)
    vg = c / (1 - (fp / c) * np.gradient(c, fp))      # ec. (9)
    keep = (fp >= 1) & (fp <= 60)
    return fp[keep], c[keep], vg[keep]


def logx(ax):
    ax.set_xscale("log"); ax.set_xlim(1, 60)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50]))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticklabels(["1", "2", "5", "10", "20", "50"])


def save(fig, name):
    fig.savefig(HERE / name, transparent=True); plt.close(fig)


M = {"A": model(10, 200), "B": model(20, 300), "h20": model(20, 200), "vs300": model(10, 300)}
C = {k: curves(m) for k, m in M.items()}
ASYM = {"capa A": 189.5, "capa B": 279.8, "semiesp.": 606.1}

# ---- Modelos A y B (500 x 330) ----
fig = plt.figure(figsize=(IN(500), IN(330)))
ax = fig.add_axes([0.13, 0.17, 0.85, 0.72])
ax.set_xlim(0, 100); ax.set_ylim(35, 0); ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
ax.set_yticks([0, 10, 20, 30]); ax.set_ylabel("z (m)")
for x0, (name, h, vs, col) in zip((2, 52), (("Modelo A", 10, 200, TEAL), ("Modelo B", 20, 300, ORANGE))):
    ax.add_patch(plt.Rectangle((x0, 0), 15, h, fc=LIGHT, ec=col, lw=2.4))
    ax.add_patch(plt.Rectangle((x0, h), 15, 35 - h, fc=PALE, ec=SEC, lw=1.2))
    ax.text(x0 + 7.5, h / 2, f"{h} m", ha="center", va="center", fontsize=18, color=INK, weight="bold")
    ax.text(x0 + 17, h / 2, f"$v_s$ {vs}\n$v_p$ 600\nρ 1800", va="center", fontsize=17, color=col, weight="semibold", linespacing=1.05)
    ax.text(x0 + 17, h + (35 - h) / 2, "$v_s$ 650\n$v_p$ 1300\nρ 2100", va="center", fontsize=17, color=SEC, linespacing=1.05)
    ax.text(x0, -1.5, name, fontsize=21, color=col, weight="bold", va="bottom")
    v = 30 / (h / vs + (30 - h) / 650)
    ax.text(x0, 37.3, f"$V_{{s30}}$ = {v:.0f} m/s (S2)", fontsize=18, color=INK, va="top", weight="semibold")
save(fig, "u_suelos.svg")

# ---- Dispersión: c_R y v_g lado a lado (1020 x 360) ----
fig, axs = plt.subplots(1, 2, figsize=(IN(1020), IN(370)), sharey=True, gridspec_kw={"wspace": 0.30})
fig.subplots_adjust(left=0.075, right=0.865, top=0.86, bottom=0.18)
airy = {}
for ax, idx, ttl in ((axs[0], 1, "Velocidad de fase $c_R$ (m/s)"), (axs[1], 2, "Velocidad de grupo $v_g$ (m/s)")):
    for k, col, ls, lab in (("A", TEAL, "-", "Modelo A"), ("B", ORANGE, "--", "Modelo B")):
        ax.plot(C[k][0], C[k][idx], color=col, ls=ls, lw=3, label=lab)
    for v in ASYM.values():
        ax.axhline(v, color=GREY, ls=":", lw=1.6)
    ax.set_ylim(50, 660); ax.set_yticks([100, 200, 300, 400, 500, 600]); ax.grid(True)
    ax.set_title(ttl, loc="left", fontsize=22, color=INK, weight="bold", pad=8)
    logx(ax); ax.set_xlabel("f (Hz, escala log)")
for lab, v in ASYM.items():
    axs[1].text(66, v + (16 if lab == "capa B" else -16 if lab == "capa A" else 0), f"{v:.1f} {lab}".replace(".", ",", 1), fontsize=15, color=SEC, va="center")
for k, col in (("A", TEAL), ("B", ORANGE)):
    f_, g = C[k][0], C[k][2]
    i = int(np.argmin(g))
    a2, a1, a0 = np.polyfit(f_[i - 1:i + 2] - f_[i], g[i - 1:i + 2], 2)
    fm = f_[i] - a1 / (2 * a2); gm = float(np.polyval([a2, a1, a0], fm - f_[i]))
    airy[k] = (round(float(fm), 3), round(gm, 2))
    axs[1].plot(fm, gm, "o", ms=11, mfc="white", mec=col, mew=3)
axs[1].annotate("fase de Airy", xy=airy["A"], xytext=(18, 75), fontsize=19, color=INK, arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
axs[0].legend(loc="lower left")
NUM["airy"] = airy
save(fig, "u_dispersion.svg")

# ---- Cambios aislados (500 x 330) ----
fig, ax = plt.subplots(figsize=(IN(500), IN(330)))
fig.subplots_adjust(left=0.17, right=0.97, top=0.95, bottom=0.24)
ax.plot(C["A"][0], C["A"][1], color=TEAL, lw=3, label="A")
ax.plot(C["h20"][0], C["h20"][1], color=INK, lw=2.6, ls="--", label="solo h = 20 m")
ax.plot(C["vs300"][0], C["vs300"][1], color=INK, lw=2.6, ls=":", label="solo $v_s$ = 300")
ax.set_ylim(150, 640); ax.set_yticks([200, 300, 400, 500, 600]); ax.grid(True); logx(ax)
ax.set_xlabel("f (Hz, escala log)"); ax.set_ylabel("$c_R$ (m/s)")
ax.annotate("", xy=(4.85, 400), xytext=(9.65, 400), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
ax.text(6.8, 410, "f ÷ 2", fontsize=19, color=INK, ha="center", va="bottom", weight="bold")
ax.legend(loc="upper right", fontsize=17)
save(fig, "u_aislados.svg")

# ---- Kernels en 4 paneles (1020 x 340) ----
dz = 1.0; nz = 160
zc = (np.arange(nz) + 0.5) * dz
th = np.full(nz + 1, dz); th[-1] = 0
inl = np.r_[zc < 10, False]
ps = PhaseSensitivity(th / 1000, np.where(inl, 600, 1300.0) / 1000, np.where(inl, 200, 650.0) / 1000, np.where(inl, 1800, 2100.0) / 1000)
fig, axs = plt.subplots(1, 4, figsize=(IN(1020), IN(340)), sharey=True, gridspec_kw={"wspace": 0.12})
fig.subplots_adjust(left=0.07, right=0.995, top=0.86, bottom=0.22)
kern = {}
for ax, (fq, col) in zip(axs, ((3, "#7FBFC8"), (6, "#3C9DA8"), (10, TEAL), (20, NAVY))):
    kk = ps(1 / fq, 0, "rayleigh", "velocity_s").kernel
    frac = float(kk[:-1][zc < 10].sum() / kk.sum())
    lam = float(np.interp(fq, C["A"][0], C["A"][1])) / fq
    dn = (kk[:-1] / dz) / (kk[:-1] / dz).max()
    kern[fq] = {"lambda_m": round(lam, 1), "frac_capa": round(frac, 3)}
    ax.axhspan(0, 10, color=LIGHT, zorder=0); ax.axhline(10, color=GREY, ls="--", lw=1.4)
    ax.fill_betweenx(zc, 0, dn, color=col, alpha=0.30, lw=0); ax.plot(dn, zc, color=col, lw=2.6)
    ax.set_ylim(60, 0); ax.set_xlim(0, 1.05); ax.set_xticks([0, 1])
    ax.set_title(f"{fq} Hz · Λ = {lam:.0f} m", loc="left", fontsize=19, color=INK, weight="bold", pad=6)
    ax.text(0.97, 0.58, f"{frac * 100:.0f} %", transform=ax.transAxes, ha="right", fontsize=40, color=col, weight="bold")
    ax.text(0.97, 0.49, "en la capa", transform=ax.transAxes, ha="right", fontsize=16, color=SEC)
    ax.set_xlabel("∂$c_R$/∂$v_s$ (norm.)", fontsize=17)
axs[0].set_ylabel("z (m)")
NUM["kernels"] = kern
save(fig, "u_kernels.svg")

# ---- Inversión (500 x 330) ----
rng = np.random.default_rng(0)
fo = np.geomspace(3, 40, 25)
_, cobs = phase(M["A"], fo)
sig = 0.02 * cobs
cn = cobs + rng.normal(0, sig)
hs = np.arange(4, 40.01, 0.5); v1s = np.arange(150, 250.01, 2.0); hi = fo >= 15
chi_a = np.full((len(v1s), len(hs)), np.nan); chi_h = np.full_like(chi_a, np.nan)
for i, v in enumerate(v1s):
    for j, h in enumerate(hs):
        try:
            _, cc = phase(model(h, v), fo)
        except Exception:
            continue
        if len(cc) != len(fo):
            continue
        r = (cc - cn) / sig
        chi_a[i, j] = np.sqrt(np.mean(r**2)); chi_h[i, j] = np.sqrt(np.mean(r[hi] ** 2))
HH, VV = np.meshgrid(hs, v1s)
fig, ax = plt.subplots(figsize=(IN(500), IN(330)))
fig.subplots_adjust(left=0.19, right=0.97, top=0.95, bottom=0.24)
ax.contourf(HH, VV, np.nan_to_num(chi_h, nan=99), levels=[0, 1.5], colors=[PALE])
ax.contour(HH, VV, np.nan_to_num(chi_h, nan=99), levels=[1.5], colors=[INK], linewidths=2, linestyles="--")
ax.contourf(HH, VV, np.nan_to_num(chi_a, nan=99), levels=[0, 1.5], colors=[TEAL])
ax.plot(10, 200, marker="*", ms=19, color="white", mec=INK, mew=1.6)
ax.set_xlim(4, 40); ax.set_ylim(186, 214); ax.grid(True)
ax.set_xlabel("h de la capa (m)"); ax.set_ylabel("$v_s$ de la capa (m/s)")
ax.text(14, 210.3, "solo f ≥ 15 Hz", fontsize=18, color=INK)
ax.text(14, 188.3, "3–40 Hz", fontsize=18, color=TEAL, weight="bold")
ax.annotate("", xy=(10.4, 197), xytext=(13.6, 189.6), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
okA, okH = chi_a <= 1.5, chi_h <= 1.5
NUM["inversion"] = {"full_h": [float(HH[okA].min()), float(HH[okA].max())], "full_vs": [float(VV[okA].min()), float(VV[okA].max())],
                    "hi_h": [float(HH[okH].min()), float(HH[okH].max())]}
save(fig, "u_inversion.svg")
print(json.dumps(NUM, ensure_ascii=False))
