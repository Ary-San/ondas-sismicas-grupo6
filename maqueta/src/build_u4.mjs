import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const katex = require('katex');
const { chromium } = require('playwright');

const dir = path.dirname(new URL(import.meta.url).pathname);
let tpl = fs.readFileSync(path.join(dir, 'template_u4.html'), 'utf8');
let fig1 = fs.readFileSync(path.join(dir, 'fig1_u3.svg'), 'utf8');
tpl = tpl.replace('{{FIG1}}', fig1);
const render = (tex, display) => katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: false });
tpl = tpl.replace(/<M>([\s\S]*?)<\/M>/g, (_, t) => render(t.trim(), true));
tpl = tpl.replace(/<m>([\s\S]*?)<\/m>/g, (_, t) => render(t.trim(), false));
const file = path.join(dir, 'maqueta_utec_revision_ecuaciones.html');
fs.writeFileSync(file, tpl);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 4494, height: 3178 }, deviceScaleFactor: 0.45 });
await page.goto('file://' + file);
await page.evaluate(() => document.fonts.ready);
const rep = await page.evaluate(() => {
  const pt = 96 / 72, o = {};
  for (const id of ['intro-in', 'result-in', 'concl-in', 'refs-in']) {
    const el = document.getElementById(id);
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const bottom = Math.max(...[...el.querySelectorAll(':scope > *')].map(k => k.getBoundingClientRect().bottom));
    o[id] = { exceso_pt: Math.round((bottom - (r.bottom - parseFloat(cs.paddingBottom))) / pt) };
  }
  // metodología a dos columnas: desborda si el contenido crea una 3.ª columna
  const c2 = document.querySelector('#metod-in .cols2');
  const kids = [...c2.children], cr = c2.getBoundingClientRect();
  o['metod-in'] = { exceso_horizontal_pt: Math.round((Math.max(...kids.map(k => k.getBoundingClientRect().right)) - cr.right) / pt) };
  o.wideEq = [...document.querySelectorAll('.katex-display')].filter(e => e.scrollWidth > e.clientWidth + 1).length;
  return o;
});
console.log(JSON.stringify(rep));
await page.screenshot({ path: path.join(dir, 'maqueta_utec_revision_ecuaciones.png') });
await page.pdf({ path: path.join(dir, 'maqueta_utec_revision_ecuaciones.pdf'), width: '1189mm', height: '841mm', printBackground: true, pageRanges: '1' });
await browser.close();
