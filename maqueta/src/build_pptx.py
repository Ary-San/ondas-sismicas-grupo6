"""Construye un .pptx A0 horizontal (editable en Canva) a partir de canva/layout.json."""
import json
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
L = json.loads((HERE / "canva" / "layout.json").read_text())
E = lambda pt: Emu(int(round(pt * 12700)))

prs = Presentation()
prs.slide_width, prs.slide_height = E(L["page"]["w"]), E(L["page"]["h"])
slide = prs.slides.add_slide(prs.slide_layouts[6])  # en blanco


def rect(x, y, w, h, fill=None, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    s.shadow.inherit = False
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = RGBColor(*fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = RGBColor(*line["c"]); s.line.width = Pt(line["w"])
    else:
        s.line.fill.background()
    return s


# 1) formas
for sh in L["shapes"]:
    if sh["fill"] or sh["border"]:
        rect(sh["x"], sh["y"], sh["w"], sh["h"], sh["fill"], sh["border"])
    if sh.get("left"):
        rect(sh["x"], sh["y"], sh["left"]["w"], sh["h"], sh["left"]["c"])
    if sh.get("top") and sh["top"]["c"]:
        rect(sh["x"], sh["y"], sh["w"], max(sh["top"]["w"], 1), sh["top"]["c"])

# 2) imágenes (ecuaciones, figuras, logo, QR)
for im in L["images"]:
    pic = slide.shapes.add_picture(im["file"], E(im["x"]), E(im["y"]), E(im["w"]), E(im["h"]))
    pic.name = ("Ecuación " if im["kind"] == "ecuacion" else "Imagen ") + im["id"]

# 3) textos editables
ALIGN = {"center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT, "end": PP_ALIGN.RIGHT}
for t in L["texts"]:
    pd = t["pad"]
    x, y = t["x"] + pd["l"], t["y"] + pd["t"]
    w, h = t["w"] - pd["l"] - pd["r"], t["h"] - pd["t"] - pd["b"]
    single = t["lh"] > 1.6 * t["size"]  # barras de título: una línea centrada en vertical
    extra = 0.04 * w + 4               # margen para diferencias de métrica entre navegador y Canva
    tb = slide.shapes.add_textbox(E(x), E(y), E(w + extra), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE if single else MSO_ANCHOR.TOP
    para = tf.paragraphs[0]

    def setup(p):
        p.alignment = ALIGN.get(t["align"], PP_ALIGN.LEFT)
        p.line_spacing = Pt(1.2 * t["size"] if single else t["lh"])
        p.space_before = p.space_after = Pt(0)

    setup(para)
    for r in t["runs"]:
        if r["t"] == "\n":
            para = tf.add_paragraph(); setup(para); continue
        run = para.add_run()
        run.text = r["t"]
        f = run.font
        f.name = t["font"]
        f.size = Pt(t["size"] if r["va"] else r["s"])
        f.bold, f.italic = r["b"], r["i"]
        if r["c"]:
            f.color.rgb = RGBColor(*r["c"])
        if r["va"]:
            run._r.get_or_add_rPr().set("baseline", "-25000" if r["va"] == "sub" else "30000")

out = HERE / "poster_grupo6_canva.pptx"
prs.save(out)
print("guardado", out, f"({out.stat().st_size / 1e6:.1f} MB)")
