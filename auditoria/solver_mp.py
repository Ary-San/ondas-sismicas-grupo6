"""Solver independiente (no usa disba): capa sobre semiespacio, matriz global 6x6 real, mpmath 40 dígitos.

Capa (0<z<h): phi = a1*cosh(qz) + a2*sinh(qz)/q ; psi = i*(b1*cosh(sz) + b2*sinh(sz)/s)
Semiespacio (z>h): phi = C*exp(-q2(z-h)) ; psi = i*D*exp(-s2(z-h))
Con psi = i*Psi, las magnitudes ux/i, uz, szz, sxz/i son reales (q^2, s^2 pueden ser de cualquier signo).
"""
import mpmath as mp

mp.mp.dps = 40


def ch(q2, z):   # cosh(qz) como función entera de q^2
    return mp.cosh(mp.sqrt(q2) * z) if q2 >= 0 else mp.cos(mp.sqrt(-q2) * z)


def sh_q(q2, z):  # sinh(qz)/q
    if q2 > 0:
        r = mp.sqrt(q2); return mp.sinh(r * z) / r
    if q2 < 0:
        r = mp.sqrt(-q2); return mp.sin(r * z) / r
    return mp.mpf(z)


def q_sh(q2, z):  # q*sinh(qz) = d/dz cosh(qz)
    if q2 > 0:
        r = mp.sqrt(q2); return r * mp.sinh(r * z)
    if q2 < 0:
        r = mp.sqrt(-q2); return -r * mp.sin(r * z)
    return mp.mpf(0)


def fields(F, dF, d2F, G, dG, d2G, k, q2, s2, lam, mu):
    """Para phi_r = F(z), Psi = G(z) (psi = i*Psi): devuelve (ux/i, uz, szz, sxz/i) por unidad de amplitud.
    ux = ik phi - dz psi = i(k F - dG) ; uz = dF + ik(iG) = dF - k G
    szz = lam(q2 - k^2)F + 2mu(d2F - k dG) ; sxz = mu(2ik dF - (k^2+s2) iG) = i mu(2k dF - (k^2+s2)G)"""
    return [k * F - dG, dF - k * G, lam * (q2 - k**2) * F + 2 * mu * (d2F - k * dG), mu * (2 * k * dF - (k**2 + s2) * G)]


def det(c, f, layer, half):
    h, vp1, vs1, r1 = layer
    vp2, vs2, r2 = half
    w = 2 * mp.pi * f
    k = w / c
    mu1, lam1 = r1 * vs1**2, r1 * vp1**2 - 2 * r1 * vs1**2
    mu2, lam2 = r2 * vs2**2, r2 * vp2**2 - 2 * r2 * vs2**2
    q1, s1 = k**2 - (w / vp1) ** 2, k**2 - (w / vs1) ** 2
    q2_, s2_ = k**2 - (w / vp2) ** 2, k**2 - (w / vs2) ** 2
    Q, S = mp.sqrt(q2_), mp.sqrt(s2_)

    def layer_cols(z):
        cols = []
        # a1: F=cosh(qz)
        cols.append(fields(ch(q1, z), q_sh(q1, z), q1 * ch(q1, z), 0, 0, 0, k, q1, s1, lam1, mu1))
        # a2: F=sinh(qz)/q
        cols.append(fields(sh_q(q1, z), ch(q1, z), q_sh(q1, z), 0, 0, 0, k, q1, s1, lam1, mu1))
        # b1: G=cosh(sz)
        cols.append(fields(0, 0, 0, ch(s1, z), q_sh(s1, z), s1 * ch(s1, z), k, q1, s1, lam1, mu1))
        # b2: G=sinh(sz)/s
        cols.append(fields(0, 0, 0, sh_q(s1, z), ch(s1, z), q_sh(s1, z), k, q1, s1, lam1, mu1))
        return cols

    top, bot = layer_cols(mp.mpf(0)), layer_cols(h)
    hc = [fields(1, -Q, Q**2, 0, 0, 0, k, q2_, s2_, lam2, mu2), fields(0, 0, 0, 1, -S, S**2, k, q2_, s2_, lam2, mu2)]
    Mx = mp.matrix(6, 6)
    for j in range(4):
        Mx[0, j], Mx[1, j] = top[j][2], top[j][3]          # superficie libre: szz, sxz
        for i in range(4):
            Mx[2 + i, j] = bot[j][i]                        # continuidad en z = h
    for j in range(2):
        for i in range(4):
            Mx[2 + i, 4 + j] = -hc[j][i]
    return mp.det(Mx)


def c_fund(f, layer, half, cmin=None, n=400):
    """Primera raíz (modo fundamental) en (cmin, vs_semiespacio)."""
    vs_lo = min(layer[2], half[1])
    a = mp.mpf(cmin if cmin is not None else 0.80 * vs_lo)
    b = half[1] * (1 - mp.mpf("1e-12"))
    grid = [a + (b - a) * i / n for i in range(n + 1)]
    prev = det(grid[0], f, layer, half)
    for c0, c1 in zip(grid[:-1], grid[1:]):
        cur = det(c1, f, layer, half)
        if mp.sign(cur) != mp.sign(prev):
            lo, hi, slo = c0, c1, mp.sign(prev)
            for _ in range(120):
                mid = (lo + hi) / 2
                if mp.sign(det(mid, f, layer, half)) == slo:
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev = cur
    return None


def homog_root(vp, vs):
    beta = (mp.mpf(vs) / vp) ** 2
    R = lambda x: (2 - x**2) ** 2 - 4 * mp.sqrt(1 - x**2) * mp.sqrt(1 - beta * x**2)
    return mp.findroot(R, (mp.mpf("0.5"), mp.mpf("0.999999")), solver="anderson") * vs
