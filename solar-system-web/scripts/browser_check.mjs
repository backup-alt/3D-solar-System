// Local desktop/mobile visual QA using the bundled Playwright runtime.
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/Sherwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const project = path.resolve(import.meta.dirname, '..');
const output = path.join(project, 'scripts', 'browser-qa');
const siteUrl = process.env.SOLAR_QA_URL || 'http://127.0.0.1:5174/';
fs.mkdirSync(output, { recursive: true });
const browser = await chromium.launch({
  executablePath: 'C:/Users/Sherwin/.cache/puppeteer/chrome/win64-149.0.7827.22/chrome-win64/chrome.exe',
  headless: true,
  args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--use-angle=swiftshader'],
});
const problems = [];
async function check(name, viewport, chapters) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1, reducedMotion: 'no-preference' });
  const page = await context.newPage();
  page.on('pageerror', error => problems.push(`${name} JS: ${error.message}`));
  page.on('console', message => { if (message.type() === 'error') problems.push(`${name} console: ${message.text()}`); });
  page.on('requestfailed', request => {
    if (request.url().includes('/models/')) problems.push(`${name} model request: ${request.url()} ${request.failure()?.errorText}`);
  });
  await page.goto(new URL('?debug=true', siteUrl).href, { waitUntil: 'domcontentloaded' });
  await page.locator('#loader').waitFor({ state: 'detached', timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.addStyleTag({ content: '.debug-panel{display:none!important}' });
  await page.screenshot({ path: path.join(output, `${name}-hero.png`) });
  const results = { viewport, hero: await page.evaluate(() => ({chapters:document.querySelectorAll('.chapter').length,models:document.querySelector('.debug-panel')?.textContent?.match(/LOADED ([^\n]+)/)?.[1] || '',scrollWidth:document.documentElement.scrollWidth,innerWidth})) };
  for (const chapter of chapters) {
    await page.locator(`#${chapter}`).scrollIntoViewIfNeeded();
    await page.waitForTimeout(1900);
    await page.screenshot({ path: path.join(output, `${name}-${chapter}.png`) });
    results[chapter] = await page.evaluate(id => ({ active:document.getElementById(id)?.classList.contains('is-active'), debug:document.querySelector('.debug-panel')?.textContent?.split('\n').slice(0,3).join(' | ') }), chapter);
  }
  await context.close();
  return results;
}
try {
  const desktop = await check('desktop', {width:1440,height:900}, ['mercury','venus','earth','mars','jupiter','saturn','uranus','neptune']);
  const mobile = await check('mobile', {width:393,height:852}, ['mercury','neptune']);
  const report = { desktop, mobile, problems };
  fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
} finally {
  await browser.close();
}
