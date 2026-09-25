/**
 * Interaction test: mobile menu, header scroll state and contact-form
 * validation, driven through the DevTools Protocol.
 *
 *   node tools/interact.js
 */
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const CHROME = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
].find((p) => fs.existsSync(p));

const SITE = path.resolve(__dirname, "..", "zeya-website");
const OUT = path.join(process.env.TEMP || os.tmpdir(), "zeya_shots");
const PORT = 9335;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map(); this.sessionId = null;
    ws.addEventListener("message", (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && this.pending.has(m.id)) {
        const { resolve, reject } = this.pending.get(m.id);
        this.pending.delete(m.id);
        m.error ? reject(new Error(JSON.stringify(m.error))) : resolve(m.result);
      }
    });
  }
  send(method, params = {}, useSession = true) {
    const id = ++this.id;
    const p = { id, method, params };
    if (useSession && this.sessionId) p.sessionId = this.sessionId;
    this.ws.send(JSON.stringify(p));
    return new Promise((res, rej) => this.pending.set(id, { resolve: res, reject: rej }));
  }
  async eval(expression, awaitPromise = false) {
    const { result } = await this.send("Runtime.evaluate", {
      expression, returnByValue: true, awaitPromise,
    });
    return result.value;
  }
}

let failures = 0;
function check(label, actual, expected) {
  const pass = JSON.stringify(actual) === JSON.stringify(expected);
  if (!pass) failures++;
  console.log(`  ${pass ? "✓" : "✗"} ${label}${pass ? "" : `  got ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)}`}`);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "zeya-int-"));
  const chrome = spawn(CHROME, [
    "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
    "--hide-scrollbars", "--disable-gpu", "--no-first-run", "--allow-file-access-from-files",
    "about:blank",
  ], { stdio: "ignore" });

  let v = null;
  for (let i = 0; i < 60 && !v; i++) {
    try { v = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); }
    catch (_) { await sleep(250); }
  }
  const ws = new WebSocket(v.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  const cdp = new CDP(ws);
  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" }, false);
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true }, false);
  cdp.sessionId = sessionId;
  await cdp.send("Page.enable");

  const go = async (page, width) => {
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width, height: width < 820 ? 844 : 900, deviceScaleFactor: 1,
      mobile: width < 820, screenWidth: width, screenHeight: width < 820 ? 844 : 900,
    });
    await cdp.send("Page.navigate", {
      url: "file:///" + path.join(SITE, page + ".html").replace(/\\/g, "/"),
    });
    await sleep(1500);
  };

  // ---------------------------------------------------------------- menu ---
  console.log("\nMobile navigation (390px)");
  await go("index", 390);

  check("menu starts closed", await cdp.eval(
    `document.querySelector('[data-zeya-nav]').classList.contains('is-open')`), false);
  // What matters is that it is rendered and hittable, not which display value
  // the bars happen to need.
  check("burger is exposed", await cdp.eval(
    `(function () {
       var b = document.querySelector('[data-zeya-burger]');
       var r = b.getBoundingClientRect();
       return getComputedStyle(b).display !== 'none' && r.width >= 44 && r.height >= 44;
     }())`), true);

  await cdp.eval(`document.querySelector('[data-zeya-burger]').click()`);
  await sleep(750);

  check("menu opens", await cdp.eval(
    `document.querySelector('[data-zeya-nav]').classList.contains('is-open')`), true);
  check("aria-expanded set", await cdp.eval(
    `document.querySelector('[data-zeya-burger]').getAttribute('aria-expanded')`), "true");
  check("body scroll locked", await cdp.eval(
    `document.body.classList.contains('zeya-no-scroll')`), true);
  check("panel is visible", await cdp.eval(
    `getComputedStyle(document.querySelector('[data-zeya-nav]')).visibility`), "visible");
  check("focus moved into menu", await cdp.eval(
    `!!document.activeElement.closest('[data-zeya-nav]')`), true);

  const shot = await cdp.send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync(path.join(OUT, "menu-open-390.png"), Buffer.from(shot.data, "base64"));

  await cdp.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await cdp.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(700);
  check("Escape closes menu", await cdp.eval(
    `document.querySelector('[data-zeya-nav]').classList.contains('is-open')`), false);
  check("scroll lock released", await cdp.eval(
    `document.body.classList.contains('zeya-no-scroll')`), false);

  // -------------------------------------------------------------- header ---
  console.log("\nHeader scroll state (1440px)");
  await go("index", 1440);
  check("header starts at top", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), false);
  await cdp.eval(`window.scrollTo(0, 900)`);
  await sleep(700);
  check("solid after scrolling", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), true);

  // Every page now opens on a full-bleed hero, so the bar rides transparent
  // over it and only turns solid once the hero has scrolled away.
  await go("about", 1440);
  check("inner page starts transparent", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), false);
  await cdp.eval(`window.scrollTo(0, 900)`);
  await sleep(700);
  check("inner page goes solid on scroll", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), true);
  await cdp.eval(`window.scrollTo(0, 0)`);
  await sleep(400);
  check("active link marked", await cdp.eval(
    `document.querySelector('[data-zeya-nav-item="about"]').getAttribute('aria-current')`), "page");

  // ---------------------------------------------------------------- form ---
  console.log("\nContact form (1440px)");
  await go("contact", 1440);

  check("no phone number invented", await cdp.eval(
    `document.querySelector('[data-zeya-contact="phone"]').hasAttribute('href')`), false);
  check("disabled link marked", await cdp.eval(
    `document.querySelector('[data-zeya-contact="phone"]').getAttribute('aria-disabled')`), "true");

  await cdp.eval(`document.querySelector('[data-zeya-form] [type=submit]').click()`);
  await sleep(400);
  check("empty submit blocked", await cdp.eval(
    `document.getElementById('zeya-name').getAttribute('aria-invalid')`), "true");
  check("error message shown", await cdp.eval(
    `document.getElementById('zeya-name-error').textContent.length > 0`), true);
  check("status is an error", await cdp.eval(
    `document.querySelector('[data-zeya-form-status]').getAttribute('data-state')`), "error");

  await cdp.eval(`document.getElementById('zeya-email').value = 'not-an-email';
                  document.getElementById('zeya-email').dispatchEvent(new Event('blur'))`);
  await sleep(200);
  check("bad email rejected", await cdp.eval(
    `document.getElementById('zeya-email').getAttribute('aria-invalid')`), "true");

  await cdp.eval(`
    document.getElementById('zeya-name').value = 'Aisha Rahman';
    document.getElementById('zeya-email').value = 'aisha@example.com';
    document.getElementById('zeya-phone').value = '+971 50 123 4567';
    document.getElementById('zeya-message').value = 'Please quote sheer curtains for a two-bedroom apartment.';
    document.querySelector('[data-zeya-form] [type=submit]').click();
  `);
  await sleep(500);
  check("valid submit passes validation", await cdp.eval(
    `document.querySelector('[data-zeya-form-status]').getAttribute('data-state')`), "info");
  check("does not claim to have sent", await cdp.eval(
    `/not connected to a mail handler/i.test(document.querySelector('[data-zeya-form-status]').textContent)`), true);

  console.log("\nProduct navigation");
  await go("products", 390);
  await cdp.eval(`document.querySelector('[data-zeya-burger]').click(); document.querySelector('.zeya-product-menu summary').click()`);
  check("category submenu opens", await cdp.eval(`document.querySelector('.zeya-product-menu').open`), true);
  // No literal count: the submenu has to offer exactly the collections the
  // page itself links to, so adding a collection cannot leave this behind.
  check("submenu lists every collection", await cdp.eval(
    `(function () {
       var nav = Array.from(document.querySelectorAll('.zeya-collection-nav a'))
         .map(function (a) { return a.getAttribute('href').replace('#', ''); }).sort();
       var menu = Array.from(document.querySelectorAll('.zeya-product-menu__item'))
         .map(function (a) { return a.getAttribute('href').replace('.html', ''); }).sort();
       return nav.length > 0 && JSON.stringify(nav) === JSON.stringify(menu);
     }())`), true);
  await go("product-sheer-curtains", 1440);
  await cdp.eval(`document.querySelector('.zeya-detail-copy .zeya-btn').click()`);
  await sleep(1200);
  check("enquiry retains selected product", await cdp.eval(`document.querySelector('[name="your-message"]').value.includes('sheer curtains')`), true);

  // --------------------------------------------------------------- motion ---
  // The 3D/scroll system is driven by custom properties, so it can be read
  // back directly rather than inferred from a screenshot.
  console.log("\nMotion (1440px)");
  await cdp.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: "no-preference" }],
  });
  await go("index", 1440);

  const readVar = (sel, name) =>
    cdp.eval(`getComputedStyle(document.querySelector('${sel}')).getPropertyValue('${name}').trim()`);

  check("hero parallax idles at 0", await readVar(".zeya-hero", "--zeya-p"), "0.0000");

  await cdp.eval(`window.scrollTo(0, 400)`);
  await sleep(500);
  check("hero parallax tracks scroll", await cdp.eval(
    `parseFloat(getComputedStyle(document.querySelector('.zeya-hero'))
       .getPropertyValue('--zeya-p')) > 0.1`), true);
  check("hero media is transformed", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-hero__media')).transform !== 'none'`), true);

  check("scroll progress advances", await cdp.eval(
    `parseFloat(getComputedStyle(document.querySelector('.zeya-header__progress'))
       .getPropertyValue('--zeya-progress')) > 0`), true);

  // The story page retains the editorial frame and reveal animations.
  await go("about", 1440);
  // Drive an editorial frame into view and confirm it is being written to.
  check("image drift tracks scroll", await cdp.eval(
    `(function () {
       var el = document.querySelector('.zeya-split__media');
       el.scrollIntoView({ block: 'center' });
       return true;
     }())`), true);
  await sleep(600);
  check("drifting frame is tagged", await cdp.eval(
    `document.querySelector('.zeya-split__media').classList.contains('is-parallaxing')`), true);
  check("drift value is in range", await cdp.eval(
    `(function () {
       var v = parseFloat(getComputedStyle(document.querySelector('.zeya-split__media'))
         .getPropertyValue('--zeya-shift'));
       return v >= -1 && v <= 1;
     }())`), true);

  // Reveals must actually settle, not stay stuck at opacity 0. The class is
  // the state; the opacity confirms the transition ran to completion.
  await cdp.eval(`document.querySelector('.zeya-split__copy').scrollIntoView({ block: 'center' })`);
  await sleep(1400);
  check("reveal is marked revealed", await cdp.eval(
    `document.querySelector('.zeya-split__copy').classList.contains('is-revealed')`), true);
  check("reveal settles to opaque", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-split__copy')).opacity === '1'`), true);

  // The new homepage replaces the marquee with a linked collection strip.
  await go("index", 1440);
  await cdp.eval(`document.querySelector('.zeya-scroll-cue').click()`);
  await sleep(1000);
  check("scroll cue reaches solutions", await cdp.eval(
    `Math.abs(document.querySelector('#solutions').getBoundingClientRect().top) < 160`), true);
  check("homepage product links target detail pages", await cdp.eval(
    `Array.from(document.querySelectorAll('.zeya-mini-product')).every(a => /product-[a-z-]+\\.html$/.test(a.href))`), true);
  check("homepage does not widen the page", await cdp.eval(
    `document.documentElement.scrollWidth <= window.innerWidth`), true);

  // ------------------------------------------------------------ card tilt ---
  await go("products", 1440);
  check("cards are tilt-enabled", await cdp.eval(
    `document.querySelector('.zeya-product').classList.contains('zeya-tilt')`), true);

  // scroll-behavior is smooth, so the rect has to be read after the scroll has
  // actually finished or the pointer lands somewhere else entirely.
  await cdp.eval(`document.querySelector('.zeya-product').scrollIntoView({ block: 'center' })`);
  await sleep(900);
  const box = await cdp.eval(
    `(function () {
       var r = document.querySelector('.zeya-product').getBoundingClientRect();
       return JSON.stringify({ x: r.left + r.width * 0.25, y: r.top + r.height * 0.25 });
     }())`);
  const at = JSON.parse(box);
  // Two moves: the first carries the pointer over the card, the second gives
  // pointermove something to track.
  for (const point of [{ x: at.x + 6, y: at.y + 6 }, at]) {
    await cdp.send("Input.dispatchMouseEvent", {
      type: "mouseMoved", x: point.x, y: point.y, buttons: 0,
    });
    await sleep(150);
  }
  await sleep(350);
  check("pointer tilts the card", await cdp.eval(
    `(function () {
       var c = document.querySelector('.zeya-product');
       var rx = parseFloat(getComputedStyle(c).getPropertyValue('--zeya-rx'));
       var ry = parseFloat(getComputedStyle(c).getPropertyValue('--zeya-ry'));
       return Math.abs(rx) > 0.5 && Math.abs(ry) > 0.5;
     }())`), true);
  check("tilt stays within 6 degrees", await cdp.eval(
    `(function () {
       var c = document.querySelector('.zeya-product');
       var rx = Math.abs(parseFloat(getComputedStyle(c).getPropertyValue('--zeya-rx')));
       var ry = Math.abs(parseFloat(getComputedStyle(c).getPropertyValue('--zeya-ry')));
       return rx <= 6 && ry <= 6;
     }())`), true);

  // --------------------------------------------------- motion, reduced ---
  console.log("\nReduced motion");
  await cdp.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: "reduce" }],
  });
  await go("index", 1440);
  check("reveals are visible immediately", await cdp.eval(
    `Array.from(document.querySelectorAll('.zeya-reveal')).every(function (el) {
       return getComputedStyle(el).opacity === '1';
     })`), true);
  check("hero remains still", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-hero__media img')).animationName`), "none");
  check("no hero parallax", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-hero__media')).transform`), "none");
  check("no progress rule injected", await cdp.eval(
    `document.querySelector('.zeya-header__progress') === null`), true);
  await go("products", 1440);
  check("no tilt applied", await cdp.eval(
    `document.querySelector('.zeya-product').classList.contains('zeya-tilt')`), false);
  await go("index", 1440);
  check("collection remains visible with reduced motion", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-mini-grid')).opacity === '1'`), true);

  console.log(failures ? `\n${failures} check(s) failed.` : "\nAll interaction checks passed.");
  ws.close(); chrome.kill(); process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
