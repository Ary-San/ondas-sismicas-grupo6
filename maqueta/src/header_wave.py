"""Banda de cabecera: superficie deformada y órbitas de Rayleigh calculadas (semiespacio vp/vs = 2)."""
import numpy as np

beta = 0.25
xi = 0.932526
k = 2 * np.pi
q, s = k * np.sqrt(1 - beta * xi**2), k * np.sqrt(1 - xi**2)
cx, cz = 2 * q * s / (k**2 + s**2), 2 * k**2 / (k**2 + s**2)
U = lambda z: k * (np.exp(-q * z) - cx * np.exp(-s * z))
W = lambda z: -q * (np.exp(-q * z) - cz * np.exp(-s * z))

Wd, Hd, L, Z0 = 760, 240, 250.0, 70
amp = 26 / W(0)
PALE, LINE = "#BCDBE1", "#4A6A80"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}pt" height="{Hd}pt" viewBox="0 0 {Wd} {Hd}">',
     '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1D3B54" stop-opacity="0.9"/>'
     '<stop offset="1" stop-color="#102A43" stop-opacity="0"/></linearGradient>'
     '<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
     '<stop offset="0.18" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
     f'<mask id="m"><rect width="{Wd}" height="{Hd}" fill="url(#fade)"/></mask></defs>', '<g mask="url(#m)">']
xs = np.linspace(0, Wd / L, 600)
e = np.exp(1j * k * xs)
ux, uz = (1j * U(0) * e).real, (W(0) * e).real
surf = [(L * x + amp * a, Z0 + amp * b) for x, a, b in zip(xs, ux, uz)]
o.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in surf) + f' L{Wd},{Hd} L0,{Hd} Z" fill="url(#g)"/>')
o.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in surf) + f'" fill="none" stroke="{PALE}" stroke-width="2.4"/>')
th = np.linspace(0, 2 * np.pi, 80)
for zr, op in ((0.0, 0.85), (0.35, 0.4)):
    for xc in np.arange(0.25, Wd / L, 0.5):
        cxp, czp = L * xc, Z0 + L * zr * 0.75
        a_, b_ = amp * abs(U(zr)), amp * abs(W(zr))
        o.append('<polygon points="' + " ".join(f"{cxp + a_ * np.cos(t):.1f},{czp + b_ * np.sin(t):.1f}" for t in th)
                 + f'" fill="none" stroke="{PALE}" stroke-width="1.6" opacity="{op}"/>')
o.append("</g></svg>")
print("\n".join(o))
