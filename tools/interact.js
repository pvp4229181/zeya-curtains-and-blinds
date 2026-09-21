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
  check("burger is exposed", await cdp.eval(
    `getComputedStyle(document.querySelector('[data-zeya-burger]')).display`), "block");

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
  check("transparent at top", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), false);
  await cdp.eval(`window.scrollTo(0, 900)`);
  await sleep(700);
  check("solid after scrolling", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('is-scrolled')`), true);

  await go("about", 1440);
  check("inner page starts solid", await cdp.eval(
    `document.querySelector('[data-zeya-header]').classList.contains('zeya-header--solid')`), true);
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

  // ----------------------------------------------------- reduced motion ----
  console.log("\nReduced motion");
  await cdp.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: "reduce" }],
  });
  await go("index", 1440);
  check("reveals are visible immediately", await cdp.eval(
    `Array.from(document.querySelectorAll('.zeya-reveal')).every(function (el) {
       return getComputedStyle(el).opacity === '1';
     })`), true);
  check("hero zoom disabled", await cdp.eval(
    `getComputedStyle(document.querySelector('.zeya-hero__media img')).animationName`), "none");

  console.log(failures ? `\n${failures} check(s) failed.` : "\nAll interaction checks passed.");
  ws.close(); chrome.kill(); process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
