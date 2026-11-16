"""Figura 1 de la maqueta: (a) P, (b) S, (c) Rayleigh calculada (semiespacio vP/vS = 2)."""
import sys
import numpy as np

NAVY, TEAL, GREY, LIGHT, SEC = "#102A43", "#006C78", "#8A9BA8", "#E6F0F2", "#40596D"
FONT = "font-family:'Source Sans 3',sans-serif"
SUB = 'baseline-shift="sub" font-size="72%"'


def secular(xi, beta):
    return (2 - xi**2) ** 2 - 4 * np.sqrt(1 - xi**2) * np.sqrt(1 - beta * xi**2)


def xi_root(beta):
    a, b = 0.5, 0.999999
    for _ in range(200):
        m = 0.5 * (a + b)
        if np.sign(secular(m, beta)) == np.sign(secular(a, beta)):
            a = m
        else:
            b = m
    return 0.5 * (a + b)


beta = 1 / 2.0**2
xi = xi_root(beta)
k = 2 * np.pi  # Lambda = 1
q = k * np.sqrt(1 - beta * xi**2)
s = k * np.sqrt(1 - xi**2)
c_x = 2 * q * s / (k**2 + s**2)
c_z = 2 * k**2 / (k**2 + s**2)


def U(z):  # u_x = i * U(z) * A * E   (ec. 4)
    return k * (np.exp(-q * z) - c_x * np.exp(-s * z))


def W(z):  # u_z = W(z) * A * E        (ec. 5)
    return -q * (np.exp(-q * z) - c_z * np.exp(-s * z))


z_rev = np.log((k**2 + s**2) / (2 * q * s)) / (q - s)
W0 = W(0.0)
print(f"xi={xi:.4f} H/V={U(0)/W0:.3f} z_rev={z_rev:.3f} Lambda", file=sys.stderr)


def disp(x, z):
    """Desplazamiento real en t=0 y dirección de la velocidad; u = Re[(iU, W) e^{i(kx-wt)}], z hacia abajo."""
    e = np.exp(1j * k * x)
    return ((1j * U(z) * e).real, (W(z) * e).real, (U(z) * e).real, (-1j * W(z) * e).real)


# Comprobación: en la cresta de la órbita superficial la partícula va hacia -x (retrógrado); a 0,4 Λ, hacia +x.
xs = np.linspace(0, 1, 2001)
for zz_, sign in ((0.0, -1), (0.4, 1)):
    ux, uz, vx, vz = disp(xs, zz_)
    assert np.sign(vx[np.argmin(uz)]) == sign, "sentido de giro inesperado"

o = []
import os
FS = float(os.environ.get("FS", "1"))
def t(x, y, s_, size=19, fill=SEC, anchor="start", weight=400, style=""):
    size = size * FS
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {style}>{s_}</text>')
def arrow(x1, y1, x2, y2, both=False, w=2.2, col=NAVY):
    ms = ' marker-start="url(#ah)"' if both else ""
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{ms} marker-end="url(#ah)"/>')

W_, H_ = 630, 440
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}pt" height="{H_}pt" viewBox="0 0 {W_} {H_}" style="{FONT}">')
o.append(f"""<defs>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{NAVY}"/></marker>
<marker id="aht" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.4" markerHeight="4.4" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>
</defs>""")

# ---------- (a) P   (b) S ----------
t(0, 20, "(a) Onda P", 20, NAVY, weight=700)
t(325, 20, "(b) Onda S", 20, NAVY, weight=700)
yP = 52
for row in (-10, 0, 10):
    for x0 in np.arange(6, 296, 8.5):
        x = x0 + 5.5 * np.sin(2 * np.pi * x0 / 120)
        o.append(f'<circle cx="{x:.1f}" cy="{yP + row:.1f}" r="2.4" fill="{TEAL}"/>')
for x0 in np.arange(331, 621, 8.5):
    o.append(f'<circle cx="{x0:.1f}" cy="{yP + 16 * np.sin(2 * np.pi * (x0 - 331) / 120):.1f}" r="2.4" fill="{TEAL}"/>')
arrow(20, yP + 30, 64, yP + 30, both=True)
t(72, yP + 36, "longitudinal: ∥ al avance", 17)
arrow(330, yP - 16, 330, yP + 16, both=True)
t(345, yP + 36, "transversal: ⊥ al avance", 17)
for x2 in (300, 625):
    arrow(x2 - 52, 14, x2, 14)
    t(x2 - 58, 20, "avance", 17, anchor="end")

# ---------- (c) Rayleigh ----------
cy = 130
t(0, cy, f"(c) Rayleigh · semiespacio, v<tspan {SUB}>p</tspan>/v<tspan {SUB}>s</tspan> = 2", 20, NAVY, weight=700)
X0, L = 150, 330.0          # 1 Λ = 330 unidades, igual en x y en z
Z0 = cy + 62
ZMAX = 0.58
amp = 18.0 / W0
t(X0 - 8, cy + 30, "Superficie libre z = 0", 17, anchor="start")
arrow(X0 + L - 110, cy + 24, X0 + L, cy + 24)
t(X0 + L - 116, cy + 30, "+x", 17, anchor="end")
o.append(f'<rect x="{X0 - 8}" y="{Z0}" width="{L + 16}" height="{ZMAX * L + 10}" fill="{LIGHT}"/>')
xx = np.linspace(-0.02, 1.02, 300)
ux, uz, _, _ = disp(xx, 0.0)
o.append('<polyline points="' + " ".join(f"{X0 + L * x + amp * a:.1f},{Z0 + amp * b:.1f}" for x, a, b in zip(xx, ux, uz))
         + f'" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="5 4"/>')
yr = Z0 + L * z_rev
o.append(f'<line x1="{X0 - 8}" y1="{yr:.1f}" x2="{X0 + L + 8}" y2="{yr:.1f}" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="7 5"/>')
th = np.linspace(0, 2 * np.pi, 100)
rows = (0.0, 0.12, 0.30, 0.50)
for zr in rows:
    for xc in (0.125, 0.375, 0.625, 0.875):
        cx, cz = X0 + L * xc, Z0 + L * zr
        a_, b_ = amp * abs(U(zr)), amp * abs(W(zr))
        o.append('<polygon points="' + " ".join(f"{cx + a_ * np.cos(v):.1f},{cz + b_ * np.sin(v):.1f}" for v in th)
                 + f'" fill="none" stroke="{TEAL}" stroke-width="1.8"/>')
        ux, uz, vx, vz = disp(xc, zr)
        px, pz, nv = cx + amp * ux, cz + amp * uz, np.hypot(vx, vz)
        o.append(f'<circle cx="{px:.1f}" cy="{pz:.1f}" r="3.4" fill="{NAVY}"/>')
        o.append(f'<line x1="{px:.1f}" y1="{pz:.1f}" x2="{px + 13 * vx / nv:.1f}" y2="{pz + 13 * vz / nv:.1f}" stroke="{TEAL}" stroke-width="2.2" marker-end="url(#aht)"/>')
    lab = "z = 0" if zr == 0 else f"z = {zr:.2f} Λ".replace(".", ",")
    t(X0 - 16, Z0 + L * zr + 2, lab, 17, NAVY, anchor="end", weight=600)
    t(X0 - 16, Z0 + L * zr + 21, "retrógrado" if zr < z_rev else "prógrado", 16, TEAL, anchor="end", style='font-style="italic"')
t(X0 + L + 12, yr + 6, f'u<tspan {SUB}>x</tspan> = 0', 16, NAVY, weight=700)

# perfil de amplitudes (ecs. 4–5), normalizado por u_z(0)
PX0, PW = X0 + L + 62, 630 - (X0 + L + 62) - 4
zz = np.linspace(0, ZMAX, 300)
def px_(v):
    return PX0 + PW * (v + 0.3) / 1.35
o.append(f'<line x1="{px_(0):.1f}" y1="{Z0}" x2="{px_(0):.1f}" y2="{Z0 + L * ZMAX:.1f}" stroke="{GREY}" stroke-width="1.2"/>')
o.append('<polyline points="' + " ".join(f"{px_(W(z) / W0):.1f},{Z0 + L * z:.1f}" for z in zz) + f'" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')
o.append('<polyline points="' + " ".join(f"{px_(U(z) / W0):.1f},{Z0 + L * z:.1f}" for z in zz) + f'" fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-dasharray="6 4"/>')
o.append(f'<line x1="{px_(-0.3):.1f}" y1="{yr:.1f}" x2="{PX0 + PW:.1f}" y2="{yr:.1f}" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="7 5"/>')
for v in (0, 1):
    t(px_(v), Z0 - 8, str(v), 15, anchor="middle")
yb = Z0 + L * ZMAX + 34
o.append(f'<line x1="{PX0 - 50}" y1="{yb - 6}" x2="{PX0 - 26}" y2="{yb - 6}" stroke="{TEAL}" stroke-width="2.6"/>')
t(PX0 - 21, yb, f'u<tspan {SUB}>z</tspan>', 16, TEAL, weight=700)
o.append(f'<line x1="{PX0 + 22}" y1="{yb - 6}" x2="{PX0 + 46}" y2="{yb - 6}" stroke="{NAVY}" stroke-width="2.2" stroke-dasharray="6 4"/>')
t(PX0 + 51, yb, f'u<tspan {SUB}>x</tspan>', 16, NAVY, weight=700)
t(X0 + L / 2, yb, "1 Λ (a escala); órbitas ampliadas", 15, anchor="middle")
o.append("</svg>")
print("\n".join(o))
