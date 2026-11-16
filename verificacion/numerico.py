"""Fases VI–XI: comparación solver independiente (mpmath) vs disba y vs cifras del póster."""
import json
import numpy as np
import mpmath as mp
from disba import PhaseDispersion, GroupDispersion, PhaseSensitivity
from solver_mp import c_fund, homog_root, det

HALF = (1300, 650, 2100)
MOD = {"A": (10, 600, 200, 1800), "B": (20, 600, 300, 1800), "h20": (20, 600, 200, 1800), "vs300": (10, 600, 300, 1800)}
out = {}


def dis(lay, f, group=False, dc=0.005):
    th = np.array([lay[0], 0]) / 1000
    vp, vs, rho = (np.array([lay[1], HALF[0]]) / 1000, np.array([lay[2], HALF[1]]) / 1000, np.array([lay[3], HALF[2]]) / 1000)
    T = np.sort(1 / np.atleast_1d(np.asarray(f, float)))
    C = (GroupDispersion if group else PhaseDispersion)(th, vp, vs, rho, dc=dc)(T, 0, "rayleigh")
    return 1 / C.period[::-1], C.velocity[::-1] * 1000


# 1) Raíces homogéneas
out["homog"] = {n: float(homog_root(vp, vs)) for n, (vp, vs) in {"semiesp": (1300, 650), "capaA": (600, 200), "capaB": (600, 300)}.items()}
# test: solver de capas con capa = semiespacio debe dar la raíz homogénea (control)
out["control_capa_igual_semiesp"] = float(c_fund(10, (10, 1300, 650, 2100), HALF, cmin=500))

# 2) c_R(f) en frecuencias del póster: solver independiente vs disba
F = [1, 3, 6, 10, 20, 60]
tab = {}
for m in ("A", "B", "h20", "vs300"):
    _, cd = dis(MOD[m], F)
    cm = [float(c_fund(f, MOD[m], HALF)) for f in F]
    tab[m] = {str(f): {"mp": round(a, 4), "disba": round(float(b), 4), "dif": round(float(b) - a, 4)} for f, a, b in zip(F, cm, cd)}
out["cR"] = tab

# 3) v_g de referencia (diferencia central fina sobre el solver mp, h=1e-4 Hz) vs disba y vs fórmula (9)
def vg_ref(m, f, d=mp.mpf("1e-4")):
    cp, cm_ = c_fund(f + d, MOD[m], HALF), c_fund(f - d, MOD[m], HALF)
    kp, km = 2 * mp.pi * (f + d) / cp, 2 * mp.pi * (f - d) / cm_
    return float(2 * mp.pi * 2 * d / (kp - km))
vg = {}
for m in ("A", "B"):
    for f in (3, 6, 9.66, 10, 20):
        ref = vg_ref(m, f)
        _, gd = dis(MOD[m], [f], group=True)
        # fórmula (9) con diferencias centrales sobre disba, paso 0,05 Hz (como el póster)
        fr = np.array([f - 0.05, f, f + 0.05])
        _, cc = dis(MOD[m], fr)
        dcdf = (cc[2] - cc[0]) / 0.1
        v9 = cc[1] / (1 - fr[1] / cc[1] * dcdf)
        vg[f"{m}@{f}"] = {"ref_mp": round(ref, 3), "disba_group": round(float(gd[0]), 3), "formula9_df0.05": round(float(v9), 3)}
out["vg"] = vg

# 4) Fase de Airy: mínimo de v_g refinado
airy = {}
for m in ("A", "B", "h20"):
    fg = np.arange(2, 20, 0.01)
    f_, g = dis(MOD[m], fg, group=True)
    i = np.argmin(g)
    fz = np.arange(f_[i] - 0.05, f_[i] + 0.05, 0.0005)
    f2, g2 = dis(MOD[m], fz, group=True)
    j = np.argmin(g2)
    airy[m] = {"f_min": round(float(f2[j]), 3), "vg_min": round(float(g2[j]), 2)}
out["airy"] = airy

# 5) Monotonía: dc/df < 0 en 1–60 Hz
mono = {}
for m in MOD:
    f_, c_ = dis(MOD[m], np.geomspace(1, 60, 2000))
    mono[m] = bool(np.all(np.diff(c_) < 0))
out["dcdf_negativa_1_60Hz"] = mono

# 6) Sensibilidad a la tolerancia interna de disba (dc)
_, c_def = dis(MOD["A"], F)
_, c_fine = dis(MOD["A"], F, dc=0.0005)
out["disba_dc_sens_max_dif_ms"] = float(np.max(np.abs(c_def - c_fine)))

# 7) Fracción de sensibilidad en la capa por diferencias finitas (independiente de PhaseSensitivity)
frac = {}
for f in (3, 6, 10, 20):
    d = 0.5  # m/s
    base = dis(MOD["A"], [f])[1][0]
    lay_p = (10, 600, 200 + d, 1800)
    c_lay = dis(lay_p, [f])[1][0]
    th = np.array([10, 0]) / 1000
    C = PhaseDispersion(th, np.array([.6, 1.3]), np.array([200 + d, 650 + d]) / 1000, np.array([1.8, 2.1]))(np.array([1 / f]), 0, "rayleigh")
    c_all = C.velocity[0] * 1000
    S_L, S_all = (c_lay - base) / d, (c_all - base) / d
    S_H = S_all - S_L
    frac[f] = {"frac_derivada": round(S_L / S_all, 3), "frac_logaritmica_vs_dc/dvs": round(200 * S_L / (200 * S_L + 650 * S_H), 3)}
out["fraccion_capa_FD"] = frac

# 8) Vs30
out["vs30"] = {"A": 30 / (10 / 200 + 20 / 650), "B": 30 / (20 / 300 + 10 / 650)}

# 9) Unicidad de la raíz secular en 0<xi<1 para todo beta admisible (0, 3/4)
cnt = []
for beta in np.linspace(0.001, 0.749, 300):
    xs = np.linspace(1e-4, 1 - 1e-9, 20001)
    R = (2 - xs**2) ** 2 - 4 * np.sqrt(1 - xs**2) * np.sqrt(1 - beta * xs**2)
    cnt.append(int(np.sum(np.sign(R[:-1]) != np.sign(R[1:]))))
out["raices_en_(0,1)_por_beta"] = sorted(set(cnt))
# raíces de la cúbica racionalizada para beta=0.25 (semiespacio) y espurias
for beta in (0.25, 1 / 9):
    r = np.roots([1, -8, 24 - 16 * beta, -16 * (1 - beta)])
    out[f"cubica_beta_{beta:.3f}"] = [str(np.round(x, 5)) for x in r]

print(json.dumps(out, indent=1, ensure_ascii=False))
