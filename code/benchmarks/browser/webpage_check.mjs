// Drives the real web page in headless Edge/Chrome (DevTools protocol): fills the example patient,
// encrypts in the browser, sends it, decrypts the answer. Needs the FHE service and the gateway running.
//   node benchmarks/browser/webpage_check.mjs http://127.0.0.1:3000 <api-token>
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const [url = 'http://127.0.0.1:3000', token = 'dev-client'] = process.argv.slice(2);
const exe = ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe'].find((p) => fs.existsSync(p));
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'webcheck-'));
const port = 9333;
const browser = spawn(exe, ['--headless=new', '--disable-gpu', '--no-first-run', `--user-data-dir=${profile}`,
  `--remote-debugging-port=${port}`, url], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let failed = 0;
try {
  let target;
  for (let i = 0; i < 60 && !target; i++) {
    await sleep(500);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page' && t.url.startsWith(url)); } catch { /* not ready */ }
  }
  if (!target) throw new Error('browser page not found');
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok, no) => { ws.onopen = ok; ws.onerror = no; });
  let id = 0;
  const pending = new Map();
  ws.onmessage = (m) => { const d = JSON.parse(m.data); pending.get(d.id)?.(d); };
  const run = (expression) => new Promise((resolve) => {
    id += 1; pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method: 'Runtime.evaluate', params: { expression, awaitPromise: true, returnByValue: true } }));
  }).then((d) => d.result.result.value);
  await sleep(1500);
  for (const dataset of ['cleveland', 'edinburgh']) {
    for (const output of ['logit', 'probability_poly']) {
      const r = await run(`(async () => {
        const $ = (i) => document.getElementById(i);
        $('dataset').value = '${dataset}'; $('dataset').dispatchEvent(new Event('change'));
        $('token').value = '${token}'; $('output').value = '${output}';
        $('fill-example').click(); $('result').hidden = true; $('form-error').hidden = true;
        const t0 = performance.now(); $('patient-form').requestSubmit();
        for (let i = 0; i < 600; i++) {
          await new Promise((ok) => setTimeout(ok, 200));
          if (!$('result').hidden) return { ok: true, ms: Math.round(performance.now() - t0), verdict: $('verdict').textContent, prob: $('prob').textContent, sent: $('wire-summary').textContent };
          if (!$('form-error').hidden) return { ok: false, error: $('form-error').textContent };
        }
        return { ok: false, error: 'timed out' };
      })()`);
      if (!r?.ok) failed += 1;
      console.log(dataset, output, JSON.stringify(r));
    }
  }
  ws.close();
} finally {
  browser.kill();
  await sleep(800);
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch { /* still locked */ }
}
console.log(failed ? `${failed} web page check(s) FAILED` : 'ALL WEB PAGE CHECKS PASSED');
process.exit(failed ? 1 : 0);
