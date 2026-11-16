// Extrae del póster renderizado: formas, imágenes (capturas en alta resolución) y textos con formato por tramo.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const dir = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(dir, 'canva');
fs.mkdirSync(path.join(out, 'img'), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 4494, height: 3178 }, deviceScaleFactor: 2.5 });
await page.goto('file://' + path.join(dir, 'maqueta_canva.html'));
await page.evaluate(() => document.fonts.ready);

const data = await page.evaluate(() => {
  const PT = 72 / 96;
  const box = r => ({ x: r.left * PT, y: r.top * PT, w: r.width * PT, h: r.height * PT });
  const rgb = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(Number); if (v.length === 4 && v[3] === 0) return null; return v.slice(0, 3); };

  // 1) Formas: fondos y bordes
  const shapes = [];
  const shapeSel = ['#logo', '#cyanband', '#blackband', '.box', '.box > .hd', '.ana', '.flow span.c', '.lim'];
  document.querySelectorAll(shapeSel.join(',')).forEach(el => {
    const cs = getComputedStyle(el);
    shapes.push({
      ...box(el.getBoundingClientRect()),
      fill: rgb(cs.backgroundColor),
      border: parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none' && el.matches('.box,.flow span.c') ? { w: parseFloat(cs.borderTopWidth) * PT, c: rgb(cs.borderTopColor) } : null,
      left: parseFloat(cs.borderLeftWidth) > 2 && el.matches('.ana') ? { w: parseFloat(cs.borderLeftWidth) * PT, c: rgb(cs.borderLeftColor) } : null,
      top: el.matches('.lim') ? { w: parseFloat(cs.borderTopWidth) * PT, c: rgb(cs.borderTopColor) } : null,
    });
  });

  // 2) Imágenes: ecuaciones de bloque, figuras (img y svg en línea), logo y QR
  const images = [];
  let n = 0;
  document.querySelectorAll('.katex-display, img, svg.fig').forEach(el => {
    const id = 'im' + (n++);
    el.setAttribute('data-cid', id);
    const src = el.tagName === 'IMG' ? el.getAttribute('src') : null;
    images.push({ id, ...box(el.getBoundingClientRect()), src, kind: el.classList.contains('katex-display') ? 'ecuacion' : 'figura' });
  });

  // 3) Textos con tramos (negrita, cursiva, sub/superíndice, color)
  const texts = [];
  const sel = '#title,#subtitle,#names,#doc,#affil,.hd,h3,p,li,.lead,.find .n,.flow span.c,.flow span.a,.lim,.qr';
  const all = [...document.querySelectorAll(sel)];
  const chosen = all.filter(el => !all.some(o => o !== el && o.contains(el)));
  for (const el of chosen) {
    const cs = getComputedStyle(el);
    const runs = [];
    const walk = (node) => {
      if (node.nodeType === 3) {
        const t = node.textContent.replace(/\s+/g, ' ');
        if (!t) return;
        const p = node.parentElement, pcs = getComputedStyle(p);
        let va = null;
        for (let a = p; a && a !== el.parentElement; a = a.parentElement) { if (a.tagName === 'SUB') { va = 'sub'; break; } if (a.tagName === 'SUP') { va = 'sup'; break; } }
        runs.push({ t, b: parseInt(pcs.fontWeight) >= 600, i: pcs.fontStyle === 'italic', c: rgb(pcs.color), s: parseFloat(pcs.fontSize) * PT, va });
        return;
      }
      if (node.nodeType !== 1) return;
      if (node.tagName === 'IMG' || node.tagName === 'svg' || node.classList?.contains('katex')) return;
      if (node.tagName === 'BR') { runs.push({ t: '\n' }); return; }
      node.childNodes.forEach(walk);
    };
    el.childNodes.forEach(walk);
    if (el.matches('li') && el.closest('ul.tight')) runs.unshift({ t: '▸ ', b: false, i: false, c: [0, 128, 173], s: parseFloat(cs.fontSize) * PT, va: null });
    // texto sin espacios al inicio y al final
    while (runs.length && runs[0].t !== '\n' && !runs[0].t.trim()) runs.shift();
    if (runs.length && runs[0].t) runs[0].t = runs[0].t.replace(/^\s+/, '');
    if (runs.length && runs[runs.length - 1].t) runs[runs.length - 1].t = runs[runs.length - 1].t.replace(/\s+$/, '');
    if (!runs.some(r => r.t && r.t.trim())) continue;
    // área ocupada por el texto (sin la imagen, en el caso del QR)
    let r = el.getBoundingClientRect();
    if (el.matches('.qr')) { const im = el.querySelector('img').getBoundingClientRect(); r = { left: r.left, top: im.bottom, width: r.width, height: r.bottom - im.bottom }; }
    const fam = cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
    const pad = { l: parseFloat(cs.paddingLeft) * PT, r: parseFloat(cs.paddingRight) * PT, t: parseFloat(cs.paddingTop) * PT, b: parseFloat(cs.paddingBottom) * PT };
    texts.push({ ...box(r), pad, font: fam, size: parseFloat(cs.fontSize) * PT, lh: parseFloat(cs.lineHeight) * PT, align: cs.textAlign, runs,
                 frags: el.getClientRects().length });
  }
  return { page: { w: document.body.getBoundingClientRect().width * PT, h: document.body.getBoundingClientRect().height * PT }, shapes, images, texts };
});

// capturas de ecuaciones y figuras
for (const im of data.images) {
  if (im.src && /\.(png)$/.test(im.src)) { im.file = path.join(dir, im.src); continue; }
  const f = path.join(out, 'img', im.id + '.png');
  await page.locator(`[data-cid="${im.id}"]`).screenshot({ path: f, omitBackground: im.kind === 'figura' });
  im.file = f;
}
fs.writeFileSync(path.join(out, 'layout.json'), JSON.stringify(data, null, 1));
console.log(`formas ${data.shapes.length}, imágenes ${data.images.length}, textos ${data.texts.length}, textos partidos en columnas: ${data.texts.filter(t => t.frags > 1 && !t.runs.some(r => r.t === '\n')).length}`);
await browser.close();
