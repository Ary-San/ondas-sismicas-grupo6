"""Fase I–V: verificación simbólica independiente (sympy) de las ecs. (1)–(8) del póster."""
import sympy as sp

x, z, t = sp.symbols("x z t", real=True)
k, w, lam, mu, rho = sp.symbols("k omega lambda mu rho", positive=True)
q, s = sp.symbols("q s", positive=True)
A, B = sp.symbols("A B")
vp2 = (lam + 2 * mu) / rho
vs2 = mu / rho
E = sp.exp(sp.I * (k * x - w * t))
phi = A * sp.exp(-q * z) * E
psi = B * sp.exp(-s * z) * E
qsub = {q: sp.sqrt(k**2 - w**2 / vp2), s: sp.sqrt(k**2 - w**2 / vs2)}

ok = lambda e: sp.simplify(e) == 0
res = {}

# --- desplazamiento: u = grad(phi) + curl(psi*yhat), coordenadas (x, y, z) dextrógiras, nada depende de y
ux = sp.diff(phi, x) - sp.diff(psi, z)          # (curl psi y)_x = -d psi/dz
uz = sp.diff(phi, z) + sp.diff(psi, x)          # (curl psi y)_z = +d psi/dx
res["curl(psi y) = (-psi_z, 0, psi_x)"] = True  # por definición de rotacional, ver comentario

# --- (2)-(3): cada potencial cumple su ecuación de onda con q^2, s^2 del póster
res["(3) phi cumple onda P"] = ok((sp.diff(phi, t, 2) - vp2 * (sp.diff(phi, x, 2) + sp.diff(phi, z, 2))).subs(qsub))
res["(3) psi cumple onda S"] = ok((sp.diff(psi, t, 2) - vs2 * (sp.diff(psi, x, 2) + sp.diff(psi, z, 2))).subs(qsub))

# --- (1) Navier con u en 2D (x,z): rho u_tt = (lam+2mu) grad(div u) - mu curl curl u
divu = sp.diff(ux, x) + sp.diff(uz, z)
res["div u = lap phi"] = ok(divu - (sp.diff(phi, x, 2) + sp.diff(phi, z, 2)))
curl_y = sp.diff(ux, z) - sp.diff(uz, x)        # única componente no nula (y)
cc_x = -sp.diff(curl_y, z)                      # curl(curl u) para campo (0, Cy, 0): (-dCy/dz, 0, dCy/dx)
cc_z = sp.diff(curl_y, x)
nav_x = rho * sp.diff(ux, t, 2) - (lam + 2 * mu) * sp.diff(divu, x) + mu * cc_x
nav_z = rho * sp.diff(uz, t, 2) - (lam + 2 * mu) * sp.diff(divu, z) + mu * cc_z
res["(1) Navier se cumple (x)"] = ok(nav_x.subs(qsub))
res["(1) Navier se cumple (z)"] = ok(nav_z.subs(qsub))

# --- (6) esfuerzos desde la ley de Hooke sigma_ij = lam delta_ij div u + 2 mu eps_ij
eps_zz = sp.diff(uz, z)
eps_xz = sp.Rational(1, 2) * (sp.diff(ux, z) + sp.diff(uz, x))
szz = lam * divu + 2 * mu * eps_zz
sxz = 2 * mu * eps_xz
lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, z, 2)
szz_poster = lam * lap(phi) + 2 * mu * (sp.diff(phi, z, 2) + sp.diff(psi, x, z))
sxz_poster = mu * (2 * sp.diff(phi, x, z) + sp.diff(psi, x, 2) - sp.diff(psi, z, 2))
res["(6) sigma_zz del póster = Hooke"] = ok(szz - szz_poster)
res["(6) sigma_xz del póster = Hooke"] = ok(sxz - sxz_poster)

# --- (7) matriz: coeficientes de A y B en z=0 (dividiendo por mu*E)
row1 = sp.expand(sp.simplify((szz.subs(z, 0) / (mu * E))).subs(qsub))
row2 = sp.expand(sp.simplify((sxz.subs(z, 0) / (mu * E))))
M = sp.Matrix([[row1.coeff(A), row1.coeff(B)], [row2.coeff(A), row2.coeff(B)]])
M_poster = sp.Matrix([[k**2 + s**2, -2 * sp.I * k * s], [-2 * sp.I * k * q, -(k**2 + s**2)]])
res["(7) fila 1 (sigma_zz) = póster"] = ok(sp.simplify(M[0, 0] - M_poster[0, 0].subs(qsub))) and ok(M[0, 1] - M_poster[0, 1])
res["(7) fila 2 (sigma_xz) = póster"] = ok(M[1, 0] - M_poster[1, 0]) and ok(M[1, 1] - M_poster[1, 1])
res["identidad lam(q^2-k^2)+2mu q^2 = mu(k^2+s^2)"] = ok((lam * (q**2 - k**2) + 2 * mu * q**2 - mu * (k**2 + s**2)).subs(qsub))
det = sp.expand(M_poster.det())
res["det M = 4k^2qs - (k^2+s^2)^2"] = ok(det - (4 * k**2 * q * s - (k**2 + s**2) ** 2))

# --- (8) adimensionalización: xi = c/vs, beta=(vs/vp)^2 ; q/k = sqrt(1-beta xi^2), s/k = sqrt(1-xi^2)
xi, beta = sp.symbols("xi beta", positive=True)
lhs = ((k**2 + s**2) ** 2 - 4 * k**2 * q * s) / k**4
lhs8 = lhs.subs({s: k * sp.sqrt(1 - xi**2), q: k * sp.sqrt(1 - beta * xi**2)})
res["(8) = det/k^4 (signo global)"] = ok(lhs8 - ((2 - xi**2) ** 2 - 4 * sp.sqrt(1 - xi**2) * sp.sqrt(1 - beta * xi**2)))

# --- (4)-(5): B de la fila 2 y forma cerrada
Bsol = sp.solve(sp.Eq(M_poster[1, 0] * A + M_poster[1, 1] * B, 0), B)[0]
res["B = -2ikqA/(k^2+s^2) (fila 2)"] = ok(Bsol + 2 * sp.I * k * q * A / (k**2 + s**2))
ux4 = sp.I * k * A * (sp.exp(-q * z) - 2 * q * s / (k**2 + s**2) * sp.exp(-s * z)) * E
uz5 = -q * A * (sp.exp(-q * z) - 2 * k**2 / (k**2 + s**2) * sp.exp(-s * z)) * E
res["(4) u_x del póster"] = ok(ux.subs(B, Bsol) - ux4)
res["(5) u_z del póster"] = ok(uz.subs(B, Bsol) - uz5)
# Con B de la fila 1 coincide solo si det M = 0:
Bsol1 = sp.solve(sp.Eq(M_poster[0, 0] * A + M_poster[0, 1] * B, 0), B)[0]
res["B fila1 - B fila2 ∝ det M"] = ok(sp.simplify((Bsol1 - Bsol) * (-2 * sp.I * k * s) * (k**2 + s**2) / A + det))

# --- profundidad donde u_x = 0
zr = sp.log((k**2 + s**2) / (2 * q * s)) / (q - s)
res["u_x(z_rev) = 0"] = ok(sp.simplify((ux4 / (sp.I * k * A * E)).subs(z, zr)))

# --- secular racionalizada y desarrollo en xi pequeño
X = sp.symbols("X", positive=True)  # X = xi^2
rat = sp.expand((2 - X) ** 4 - 16 * (1 - X) * (1 - beta * X))
res["racionalizada = X(X^3-8X^2+(24-16b)X-16(1-b))"] = ok(rat - X * (X**3 - 8 * X**2 + (24 - 16 * beta) * X - 16 * (1 - beta)))
ser = sp.series((2 - xi**2) ** 2 - 4 * sp.sqrt(1 - xi**2) * sp.sqrt(1 - beta * xi**2), xi, 0, 4).removeO()
res["R(xi) ≈ -2(1-beta) xi^2"] = ok(ser + 2 * (1 - beta) * xi**2)
res["R(1) = 1"] = ok(((2 - xi**2) ** 2 - 4 * sp.sqrt(1 - xi**2) * sp.sqrt(1 - beta * xi**2)).subs(xi, 1) - 1)

# --- (9) velocidad de grupo desde c(f)
f = sp.symbols("f", positive=True)
c = sp.Function("c")(f)
vg = sp.diff(2 * sp.pi * f, f) / sp.diff(2 * sp.pi * f / c, f)
res["(9) v_g = c/(1-(f/c)c')"] = ok(vg - c / (1 - f / c * sp.diff(c, f)))

# --- vp/vs mínimo por estabilidad
res["vp^2/vs^2 = 2 + lam/mu"] = ok(vp2 / vs2 - (2 + lam / mu))
for kk_, v in res.items():
    print(("OK  " if v else "FALLA ") + kk_)

print("\n--- revisión numérica de las 3 comprobaciones fallidas ---")
import random
for trial in range(3):
    vals = {k: random.uniform(0.5, 3), lam: random.uniform(1, 5), mu: random.uniform(0.5, 2), rho: random.uniform(1, 3)}
    vals[w] = random.uniform(0.1, 0.9) * vals[k] * sp.sqrt(vals[mu] / vals[rho])   # c < vs
    qn, sn = [sp.N(e.subs(vals)) for e in (qsub[q], qsub[s])]
    full = {**vals, q: qn, s: sn}
    d00 = sp.N(M[0, 0].subs(vals)) - sp.N(M_poster[0, 0].subs(full))
    d01 = sp.N(M[0, 1].subs(vals)) - sp.N(M_poster[0, 1].subs(full))
    lhsB = sp.N(((Bsol1 - Bsol) * (-2 * sp.I * k * s) * (k**2 + s**2) / A).subs(full))
    rhsB = sp.N((-det).subs(full))
    zrn = sp.N(zr.subs(full))
    uxz = sp.N((ux4 / (sp.I * k * A * E)).subs(full).subs(z, zrn))
    print(f"fila1: dif M00={float(abs(d00)):.2e} dif M01={float(abs(d01)):.2e} | (B1-B2)·(-2iks)(k²+s²)/A = {complex(lhsB):.4g} vs -det = {complex(rhsB):.4g} | u_x(z_rev)={float(abs(complex(uxz))):.1e}")
