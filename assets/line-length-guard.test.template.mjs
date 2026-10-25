// Line-length guard (delivery-harness template). Copy into the project's test
// directory, set ROOTS / MAX, run with `node --test`. No dependencies.
// It measures CODE only: strings, template literals (including ${...}), regex
// literals and comments are removed first, so long text never trips it while a
// 3000-character line of real code always does. Contract: references/formatting.md.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const ROOTS = (process.env.GUARD_ROOTS || 'src').split(',');
const MAX = Number(process.env.GUARD_MAX || 100); // keep equal to Prettier printWidth
const EXT = new Set(['.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx']);
const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'coverage']);

const REGEX_PREFIX = /(?:^|[(,=:[!&|?{};+\-*%<>~^]|\b(?:return|typeof|case|do|else|in|of|new|delete|void|throw|yield|await))\s*$/;

function skipString(src, pos, quote) {
  let j = pos + 1;
  while (j < src.length && src[j] !== quote && src[j] !== '\n') j += src[j] === '\\' ? 2 : 1;
  return j + 1;
}

function skipTemplate(src, pos) {
  // index after the closing backtick; nested ${ ... } (with strings/templates) is skipped too
  let j = pos + 1;
  while (j < src.length) {
    if (src[j] === '\\') j += 2;
    else if (src[j] === '`') return j + 1;
    else if (src[j] === '$' && src[j + 1] === '{') {
      let depth = 1;
      j += 2;
      while (j < src.length && depth > 0) {
        const c = src[j];
        if (c === '"' || c === "'") j = skipString(src, j, c);
        else if (c === '`') j = skipTemplate(src, j);
        else { depth += c === '{' ? 1 : c === '}' ? -1 : 0; j++; }
      }
    } else j++;
  }
  return j;
}

export function stripCode(src) {
  const keepNewlines = (text) => text.replace(/[^\n]/g, '');
  let out = '';
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    const next = src[i + 1];
    if (c === '/' && next === '/') {
      while (i < src.length && src[i] !== '\n') i++;
    } else if (c === '/' && next === '*') {
      const end = src.indexOf('*/', i + 2);
      const stop = end < 0 ? src.length : end + 2;
      out += keepNewlines(src.slice(i, stop));
      i = stop;
    } else if (c === '"' || c === "'") {
      out += c + c;
      i = skipString(src, i, c);
    } else if (c === '`') {
      const stop = skipTemplate(src, i);
      out += '``' + keepNewlines(src.slice(i, stop));
      i = stop;
    } else if (c === '/' && REGEX_PREFIX.test(out.slice(-40))) {
      let j = i + 1;
      let inClass = false;
      while (j < src.length && src[j] !== '\n') {
        if (src[j] === '\\') { j += 2; continue; }
        if (src[j] === '[') inClass = true;
        else if (src[j] === ']') inClass = false;
        else if (src[j] === '/' && !inClass) break;
        j++;
      }
      j++;
      while (/[a-z]/.test(src[j] || '')) j++;
      out += '//';
      i = j;
    } else {
      out += c;
      i++;
    }
  }
  return out;
}

export function longLines(src, max = MAX) {
  return stripCode(src)
    .split('\n')
    .map((line, index) => ({ line: index + 1, length: line.trimEnd().length }))
    .filter((item) => item.length > max);
}

function* files(dir) {
  let entries = [];
  try { entries = readdirSync(dir); } catch { return; }
  for (const name of entries) {
    if (SKIP_DIRS.has(name)) continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) yield* files(path);
    else if (EXT.has(extname(name))) yield path;
  }
}

test('guard self-test: text is ignored, code is measured', () => {
  const pad = 'x'.repeat(200);
  assert.deepEqual(longLines(`const a = '${pad}';`, 40), []);
  assert.deepEqual(longLines('const b = `' + pad + '${ fn(`' + pad + '`) }' + pad + '`;', 40), []);
  assert.deepEqual(longLines(`const r = /${pad}/g.test(s);`, 40), []);
  assert.deepEqual(longLines(`call(); // ${pad}`, 40), []);
  assert.deepEqual(longLines(`/* ${pad} */ go();`, 40), []);
  assert.equal(longLines(`const c = ${'a + '.repeat(30)}1;`, 40).length, 1);
  assert.equal(longLines(`const d = total / count / ${'n + '.repeat(20)}1;`, 40).length, 1);
  assert.deepEqual(longLines('line1();\n`a\nb`;\nline4();', 40), []);
});

test(`code lines stay within ${MAX} characters`, () => {
  const offenders = [];
  for (const root of ROOTS) {
    for (const path of files(root)) {
      for (const item of longLines(readFileSync(path, 'utf8'))) offenders.push(`${path}:${item.line} (${item.length})`);
    }
  }
  assert.deepEqual(offenders, [], `lines over ${MAX} code characters:\n${offenders.join('\n')}`);
});
