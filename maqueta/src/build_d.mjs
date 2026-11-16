import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const katex = require('katex');
const { chromium } = require('playwright');

const dir = path.dirname(new URL(import.meta.url).pathname);
let tpl = fs.readFileSync(path.join(dir, 'template_d.html'), 'utf8');
tpl = tpl.replace('{{FIG1}}', fs.readFileSync(path.join(dir, 'fig1_d.svg'), 'utf8').replace('<svg ', '<svg class="fig" '));
const render = (tex, display) => katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: false });
tpl = tpl.replace(/<M>([\s\S]*?)<\/M>/g, (_, t) => render(t.trim(), true));
tpl = tpl.replace(/<m>([\s\S]*?)<\/m>/g, (_, t) => render(t.trim(), false));
const file = path.join(dir, 'maqueta_estetica.html');
fs.writeFileSync(file, tpl.replace('{{MODE}}', ''));

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 3179, height: 4494 }, deviceScaleFactor: 0.6 });
await page.goto('file://' + file);
await page.evaluate(() => document.fonts.ready);
// medir con las columnas compactadas (sin repartir el espacio sobrante)
await page.evaluate(() => document.body.classList.add('measure'));
const rep = await page.evaluate(() => {
  const pt = 96 / 72, o = {};
  for (const id of ['c1', 'c2', 'c3', 'hero']) {
    const el = document.getElementById(id), r = el.getBoundingClientRect();
    const bottom = Math.max(...[...el.children].map(k => k.getBoundingClientRect().bottom));
    o[id] = { used: Math.round((bottom - r.top) / pt), limit: Math.round(r.height / pt) };
  }
  o.wideEq = [...document.querySelectorAll('.katex-display')].filter(e => e.scrollWidth > e.clientWidth + 1).length;
  return o;
});
console.log(JSON.stringify(rep));
await page.evaluate(() => document.body.classList.remove('measure'));
await page.screenshot({ path: path.join(dir, 'maqueta_estetica.png') });
await page.pdf({ path: path.join(dir, 'maqueta_estetica.pdf'), width: '841mm', height: '1189mm', printBackground: true, pageRanges: '1' });
await browser.close();
