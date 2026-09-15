/* Lint rules for the page's JavaScript.
 *
 *     npm run lint
 *
 * The point is bugs, not style. `node --check` only answers "does this parse", which
 * means a typo'd variable name or a duplicated object key sails straight through it and
 * onto the live site, where it shows up as one silently wrong number or a dead button.
 *
 * Style rules are deliberately off. This file is 4,600 lines written in a dense house
 * style; a linter that argues about spacing would be turned off within a day and then
 * the useful half goes with it.
 */
const browser = {
  window: 'readonly', document: 'readonly', navigator: 'readonly', location: 'readonly',
  history: 'readonly', localStorage: 'readonly', sessionStorage: 'readonly',
  console: 'readonly', setTimeout: 'readonly', clearTimeout: 'readonly',
  setInterval: 'readonly', clearInterval: 'readonly', requestAnimationFrame: 'readonly',
  cancelAnimationFrame: 'readonly', addEventListener: 'readonly',
  removeEventListener: 'readonly', matchMedia: 'readonly', getComputedStyle: 'readonly',
  innerWidth: 'readonly', innerHeight: 'readonly', scrollY: 'readonly', scrollX: 'readonly',
  scrollTo: 'readonly', scrollBy: 'readonly', devicePixelRatio: 'readonly',
  Image: 'readonly', Blob: 'readonly', URL: 'readonly', FileReader: 'readonly',
  CustomEvent: 'readonly', Event: 'readonly', KeyboardEvent: 'readonly',
  MutationObserver: 'readonly', IntersectionObserver: 'readonly', ResizeObserver: 'readonly',
  performance: 'readonly', fetch: 'readonly', CSS: 'readonly', DOMParser: 'readonly',
  HTMLElement: 'readonly', HTMLCanvasElement: 'readonly', SVGElement: 'readonly',
  getSelection: 'readonly', alert: 'readonly', screen: 'readonly', crypto: 'readonly',
  structuredClone: 'readonly', queueMicrotask: 'readonly', AbortController: 'readonly',
  File: 'readonly', FileList: 'readonly', URLSearchParams: 'readonly',
  ClipboardItem: 'readonly', ResizeObserverEntry: 'readonly', Node: 'readonly',
};

module.exports = [
  {
    files: ['page/site.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: {
        ...browser,
        /* Defined by the other inline <script> blocks on the page, not by this file.
           They are real and they are global on purpose -- the page has no module system.
           Anything NOT listed here that no-undef flags is a genuine typo. */
        DATA: 'readonly',
      },
    },
    linterOptions: { reportUnusedDisableDirectives: true },
    rules: {
      /* every one of these is a real bug, not a preference */
      'no-undef': 'error',
      'no-dupe-keys': 'error',
      'no-dupe-args': 'error',
      'no-dupe-else-if': 'error',
      'no-duplicate-case': 'error',
      'no-unreachable': 'error',
      'no-const-assign': 'error',
      'no-func-assign': 'error',
      'no-class-assign': 'error',
      'no-self-assign': 'error',
      'no-self-compare': 'error',
      'no-cond-assign': 'error',
      'no-compare-neg-zero': 'error',
      'use-isnan': 'error',
      'valid-typeof': 'error',
      'no-sparse-arrays': 'error',
      'no-obj-calls': 'error',
      'no-unsafe-negation': 'error',
      'no-unsafe-finally': 'error',
      'no-unused-labels': 'error',
      'no-constant-condition': ['error', { checkLoops: true }],
      'no-empty-pattern': 'error',
      'no-invalid-regexp': 'error',
      'no-irregular-whitespace': 'error',
      'no-misleading-character-class': 'error',
      'no-prototype-builtins': 'off',
      'getter-return': 'error',
      'no-setter-return': 'error',
      'no-async-promise-executor': 'error',
      'require-atomic-updates': 'error',
      /* a variable assigned and never read is usually a half-finished edit */
      /* catch(e){} with e unused is the house idiom for best-effort work -- storage
         that may be blocked, a chart that may not be on the page yet. 29 warnings
         about it would drown the ones that mean something. */
      'no-unused-vars': ['warn', { args: 'none', caughtErrors: 'none', varsIgnorePattern: '^_' }],
    },
  },
  {
    files: ['page/sw.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',
      globals: {
        self: 'readonly', caches: 'readonly', fetch: 'readonly', Response: 'readonly',
        Request: 'readonly', URL: 'readonly', location: 'readonly',
        setTimeout: 'readonly', Promise: 'readonly', console: 'readonly',
      },
    },
    rules: { 'no-undef': 'error', 'no-unreachable': 'error', 'use-isnan': 'error' },
  },
];
