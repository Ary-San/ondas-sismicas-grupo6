import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const katex = require('katex');
const { chromium } = require('playwright');

const dir = path.dirname(new URL(import.meta.url).pathname);
let tpl = fs.readFileSync(path.join(dir, 'template.html'), 'utf8');
const fig1 = fs.readFileSync(path.join(dir, 'fig1.svg'), 'utf8');
tpl = tpl.replace('{{FIG1}}', fig1);
const render = (tex, display) => katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: false });
tpl = tpl.replace(/<M>([\s\S]*?)<\/M>/g, (_, t) => render(t.trim(), true));
tpl = tpl.replace(/<m>([\s\S]*?)<\/m>/g, (_, t) => render(t.trim(), false));

const browser = await chromium.launch();
for (const mode of ['clean', 'annot']) {
  const html = tpl.replace('{{MODE}}', mode);
  const file = path.join(dir, `maqueta_${mode}.html`);
  fs.writeFileSync(file, html);
  const page = await browser.newPage({ viewport: { width: 3179, height: 4494 }, deviceScaleFactor: mode === 'clean' ? 0.6 : 0.5 });
  await page.goto('file://' + file);
  await page.evaluate(() => document.fonts.ready);
  const report = await page.evaluate(() => {
    const pt = 96 / 72;
    const out = {};
    for (const id of ['c1', 'c2', 'c3']) {
      const col = document.getElementById(id);
      const r = col.getBoundingClientRect();
      const kids = [...col.children];
      const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
      out[id] = { used: +((bottom - r.top) / pt).toFixed(0), limit: +(r.height / pt).toFixed(0) };
    }
    const wide = [...document.querySelectorAll('.katex-display')].filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.textContent.slice(0, 40));
    return { cols: out, overflowingEquations: wide };
  });
  console.log(mode, JSON.stringify(report));
  await page.screenshot({ path: path.join(dir, `maqueta_${mode}.png`), fullPage: false });
  if (mode === 'clean') await page.pdf({ path: path.join(dir, 'maqueta_etapaA.pdf'), width: '841mm', height: '1189mm', printBackground: true, pageRanges: '1' });
  else await page.pdf({ path: path.join(dir, 'maqueta_etapaA_anotada.pdf'), width: '841mm', height: '1189mm', printBackground: true, pageRanges: '1' });
  await page.close();
}
await browser.close();
