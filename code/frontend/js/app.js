import { createSession } from './fhe.js';
import { FIELDS } from './fields.js';

const $ = (id) => document.getElementById(id);
const form = $('patient-form');
const sessions = new Map();   // dataset -> { meta, session }

function renderFields(dataset) {
  const box = $('fields');
  box.replaceChildren();
  for (const f of FIELDS[dataset]) {
    const row = document.createElement('div');
    row.className = 'row';
    const label = document.createElement('label');
    label.htmlFor = `f-${f.name}`;
    label.textContent = f.label;
    if (f.hint) { const h = document.createElement('span'); h.className = 'hint'; h.textContent = f.hint; label.append(h); }
    let input;
    if (f.type === 'select') {
      input = document.createElement('select');
      const blank = new Option('Choose…', '');
      input.append(blank, ...f.options.map(([v, t]) => new Option(t, String(v))));
    } else {
      input = document.createElement('input');
      Object.assign(input, { type: 'number', min: f.min, max: f.max, step: f.step, inputMode: 'decimal' });
    }
    input.id = `f-${f.name}`; input.name = f.name; input.required = true;
    row.append(label, input);
    box.append(row);
  }
}

function readValues(dataset) {
  const errors = [];
  const values = FIELDS[dataset].map((f) => {
    const el = $(`f-${f.name}`);
    const v = el.value === '' ? NaN : Number(el.value);
    const bad = !Number.isFinite(v) || (f.min !== undefined && (v < f.min || v > f.max));
    el.setAttribute('aria-invalid', String(bad));
    if (bad) errors.push(f.label);
    return v;
  });
  return { values, errors };
}

function step(name, state) {
  const li = document.querySelector(`[data-step="${name}"]`);
  if (li) li.className = state;
}

async function getSession(dataset) {
  if (!sessions.has(dataset)) {
    const r = await fetch(`/api/model/${dataset}`);
    const meta = await r.json();
    if (!r.ok) throw new Error(meta.error?.message ?? 'model not available');
    const names = FIELDS[dataset].map((f) => f.name).join(',');
    if (meta.feature_names.join(',') !== names) throw new Error('form fields do not match the model features');
    sessions.set(dataset, { meta, session: await createSession(meta.params, meta.scale_bits) });
  }
  return sessions.get(dataset);
}

async function onSubmit(ev) {
  ev.preventDefault();
  const dataset = $('dataset').value;
  const { values, errors } = readValues(dataset);
  $('form-error').hidden = errors.length === 0;
  if (errors.length) { $('form-error').textContent = `Please check: ${errors.join(', ')}`; return; }

  $('submit').disabled = true; $('result').hidden = true; $('wire').hidden = true;
  ['keys', 'encrypt', 'send', 'decrypt'].forEach((s) => step(s, ''));
  try {
    step('keys', 'active');
    const { meta, session } = await getSession(dataset);
    step('keys', 'done'); step('encrypt', 'active');
    const scaled = values.map((v, i) => (v - meta.scaler_mean[i]) / meta.scaler_scale[i]);
    const ciphertexts = session.encryptEach(scaled);
    let output = $('output').value;
    if (output === 'probability_poly' && !meta.supports_probability_poly) output = 'logit';
    const body = { dataset, parms: session.parmsB64(), ciphertexts, output,
      relin_keys: output === 'probability_poly' ? session.relinKeysB64() : null };
    step('encrypt', 'done'); step('send', 'active');
    const token = $('token').value.trim();
    const res = await fetch('/api/predict', { method: 'POST',
      headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify(body) });
    const j = await res.json();
    if (!res.ok) throw new Error(`${j.error?.code ?? res.status}: ${j.error?.message ?? 'request failed'}`);
    step('send', 'done'); step('decrypt', 'active');
    const v = session.decryptScalar(j.encrypted_result);
    const prob = j.output === 'logit' ? 1 / (1 + Math.exp(-v)) : Math.min(1, Math.max(0, v));
    step('decrypt', 'done');
    showResult(prob, j.threshold ?? meta.threshold, j.output, body);
  } catch (err) {
    $('form-error').hidden = false;
    $('form-error').textContent = err.message;
  } finally {
    $('submit').disabled = false;
  }
}

function showResult(prob, threshold, output, body) {
  const high = prob >= threshold;
  const verdict = $('verdict');
  verdict.textContent = high ? 'Higher risk' : 'Lower risk';
  verdict.className = `verdict ${high ? 'high' : 'low'}`;
  const pct = prob >= 0.995 ? 'over 99%' : prob <= 0.005 ? 'under 1%' : `${(prob * 100).toFixed(1)}%`;
  $('prob').textContent = `Estimated probability: ${pct} (decision threshold ${(threshold * 100).toFixed(0)}%)`;
  $('note').textContent = output === 'logit'
    ? 'The server returned an encrypted score; the sigmoid was applied here after decryption.'
    : 'The server applied a polynomial sigmoid to the encrypted score; this page only decrypted it.';
  $('result').hidden = false;
  const mb = (n) => (n / 1048576).toFixed(1);
  const ctBytes = body.ciphertexts.reduce((s, c) => s + c.length, 0);
  const keyText = body.relin_keys ? ` plus ${mb(body.relin_keys.length)} MB of relinearization keys (public, cannot decrypt)` : '';
  $('wire-summary').textContent = `${body.ciphertexts.length} ciphertexts (${mb(ctBytes)} MB of base64)${keyText}. No readable values and no secret key.`;
  $('wire-sample').textContent = `${body.ciphertexts[0].slice(0, 600)}…`;
  $('wire').hidden = false;
}

function fillExample() {
  for (const f of FIELDS[$('dataset').value]) $(`f-${f.name}`).value = String(f.example);
}

$('dataset').addEventListener('change', () => renderFields($('dataset').value));
$('fill-example').addEventListener('click', fillExample);
form.addEventListener('submit', onSubmit);
renderFields($('dataset').value);
