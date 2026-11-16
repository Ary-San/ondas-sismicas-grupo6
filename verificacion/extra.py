import numpy as np, mpmath as mp
from numerico import dis, MOD, HALF
from solver_mp import c_fund
# (a) dónde dc/df >= 0 en disba y magnitud
for m in ("A", "B", "h20"):
    f_, c_ = dis(MOD[m], np.geomspace(1, 60, 2000))
    d = np.diff(c_); bad = np.where(d >= 0)[0]
    print(m, "n_pos", len(bad), "f rango", (round(f_[bad].min(),2), round(f_[bad].max(),2)) if len(bad) else None, "max dc>0 (m/s)", float(d[bad].max()) if len(bad) else 0)
# (b) monotonía con el solver mp en la zona señalada
for m, fs in (("A", [40, 45, 50, 55, 60]), ("B", [25, 35, 45, 60]), ("h20", [20, 30, 45, 60])):
    print(m, [round(float(c_fund(f, MOD[m], HALF)), 6) for f in fs])
# (c) mínimo verdadero de v_g (referencia mp) para A y B
def vg_ref(m, f, d=mp.mpf("1e-4")):
    cp, cm = c_fund(f + d, MOD[m], HALF), c_fund(f - d, MOD[m], HALF)
    return float(2 * mp.pi * 2 * d / (2 * mp.pi * (f + d) / cp - 2 * mp.pi * (f - d) / cm))
for m, (a, b) in (("A", (9.4, 9.9)), ("B", (6.4, 6.9))):
    fs = np.linspace(a, b, 26); v = [vg_ref(m, f) for f in fs]; i = int(np.argmin(v))
    fs2 = np.linspace(fs[max(i-1,0)], fs[min(i+1,25)], 21); v2 = [vg_ref(m, f) for f in fs2]; j = int(np.argmin(v2))
    print(m, "Airy ref: f =", round(float(fs2[j]), 3), "vg_min =", round(v2[j], 3))
