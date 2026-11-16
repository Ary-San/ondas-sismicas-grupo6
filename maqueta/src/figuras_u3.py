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
save(fig, "u_suelos3.svg")

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
axs[1].annotate("fase de Airy\n9,6 Hz (A)", xy=airy["A"], xytext=(16, 54), fontsize=17, color=INK, va="bottom", linespacing=0.95,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
axs[1].annotate("6,6 Hz (B)", xy=airy["B"], xytext=(2.0, 95), fontsize=18, color=ORANGE, weight="semibold",
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.5))
axs[0].legend(loc="lower left")
NUM["airy"] = airy
save(fig, "u_dispersion3.svg")

print(json.dumps(NUM, ensure_ascii=False))
