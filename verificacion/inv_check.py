import numpy as np
from disba import PhaseDispersion
from solver_mp import c_fund
HALF = (1300, 650, 2100)
def dis(h, v, f):
    T = np.sort(1 / f)
    C = PhaseDispersion(np.array([h, 0]) / 1000, np.array([.6, 1.3]), np.array([v, 650]) / 1000, np.array([1.8, 2.1]))(T, 0, "rayleigh")
    return C.velocity[::-1] * 1000
rng = np.random.default_rng(0)
fo = np.geomspace(3, 40, 25)
cobs = dis(10, 200, fo); sig = 0.02 * cobs; cn = cobs + rng.normal(0, sig)
hi = fo >= 15
for (h, v, band) in ((10, 200, "all"), (9.5, 200, "all"), (11, 200, "all"), (40, 200, "hi"), (25, 202, "hi")):
    cm = np.array([float(c_fund(f, (h, 600, v, 1800), HALF)) for f in fo])
    r = (cm - cn) / sig
    sel = hi if band == "hi" else slice(None)
    print(f"h={h} vs={v} banda={band}: chi(mp)={np.sqrt(np.mean(r[sel]**2)):.3f}  chi(disba)={np.sqrt(np.mean(((dis(h, v, fo) - cn) / sig)[sel]**2)):.3f}")
