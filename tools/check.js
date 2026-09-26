/**
 * Responsive + accessibility smoke test for the ZEYA static site.
 *
 *   node tools/check.js
 *
 * For every page at every target width it reports horizontal overflow, the
 * elements causing it, missing alt text, heading-order jumps, small tap
 * targets and any images that failed to load.
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
const PAGES = ["index", "about", "products", "process", "contact", "faq", "curtains", "blinds", "motorized", "residential-commercial", "review", "product-sheer-curtains", "product-smart-window-automation"];
const WIDTHS = [1440, 1200, 1024, 768, 480, 390];
const PORT = 9334;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map(); this.sessionId = null;
    ws.addEventListener("message", (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
      }
    });
  }
  send(method, params = {}, useSession = true) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (useSession && this.sessionId) payload.sessionId = this.sessionId;
    this.ws.send(JSON.stringify(payload));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
}

const AUDIT = `(function () {
  var doc = document;
  var vw = document.documentElement.clientWidth;
  var out = { overflow: Math.round(document.documentElement.scrollWidth - vw), wide: [],
              noAlt: [], badImages: [], headings: [], smallTargets: [], notes: [] };

  Array.prototype.forEach.call(doc.querySelectorAll('body *'), function (el) {
    var r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.right > vw + 1.5 || r.left < -1.5) {
      var cs = getComputedStyle(el);
      if (cs.position === 'fixed' || cs.visibility === 'hidden') return;
      out.wide.push((el.tagName + '.' + (el.className.baseVal || el.className || '')).slice(0, 70)
        + ' [' + Math.round(r.left) + '→' + Math.round(r.right) + ']');
    }
  });
  out.wide = out.wide.slice(0, 6);

  Array.prototype.forEach.call(doc.images, function (im) {
    if (!im.hasAttribute('alt')) out.noAlt.push(im.getAttribute('src'));
    if (im.complete && im.naturalWidth === 0) out.badImages.push(im.getAttribute('src'));
  });

  var last = 0;
  Array.prototype.forEach.call(doc.querySelectorAll('main h1, main h2, main h3, main h4'), function (h) {
    var lvl = Number(h.tagName[1]);
    if (last && lvl > last + 1) out.headings.push(h.tagName + ' after H' + last + ': ' + h.textContent.trim().slice(0, 30));
    last = lvl;
  });

  Array.prototype.forEach.call(doc.querySelectorAll('a[href], button'), function (el) {
    var r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.height < 30 && el.closest('.zeya-nav, .zeya-footer, .zeya-crumbs') === null) {
      out.smallTargets.push(el.textContent.trim().slice(0, 26) + ' (' + Math.round(r.height) + 'px)');
    }
  });
  out.smallTargets = out.smallTargets.slice(0, 5);

  if (doc.querySelectorAll('h1').length !== 1) out.notes.push('h1 count = ' + doc.querySelectorAll('h1').length);
  if (!doc.querySelector('meta[name="description"]')) out.notes.push('no meta description');

  return JSON.stringify(out);
}())`;

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "zeya-chk-"));
  const chrome = spawn(CHROME, [
    "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
    "--hide-scrollbars", "--disable-gpu", "--no-first-run", "--allow-file-access-from-files",
    "about:blank",
  ], { stdio: "ignore" });

  let version = null;
  for (let i = 0; i < 60 && !version; i++) {
    try { version = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); }
    catch (_) { await sleep(250); }
  }

  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  const cdp = new CDP(ws);
  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" }, false);
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true }, false);
  cdp.sessionId = sessionId;
  await cdp.send("Page.enable");

  let problems = 0;

  for (const width of WIDTHS) {
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width, height: width < 820 ? 844 : 900, deviceScaleFactor: 1,
      mobile: width < 820, screenWidth: width, screenHeight: width < 820 ? 844 : 900,
    });
    console.log(`\n=== ${width}px ===`);

    for (const page of PAGES) {
      await cdp.send("Page.navigate", {
        url: "file:///" + path.join(SITE, page + ".html").replace(/\\/g, "/"),
      });
      await sleep(1400);
      const { result } = await cdp.send("Runtime.evaluate", { expression: AUDIT, returnByValue: true });
      const r = JSON.parse(result.value);

      const bits = [];
      if (r.overflow > 1) bits.push(`OVERFLOW +${r.overflow}px → ${r.wide.join(" | ")}`);
      if (r.noAlt.length) bits.push(`NO ALT: ${r.noAlt.join(", ")}`);
      if (r.badImages.length) bits.push(`BROKEN IMG: ${r.badImages.join(", ")}`);
      if (r.headings.length) bits.push(`HEADINGS: ${r.headings.join("; ")}`);
      if (r.smallTargets.length) bits.push(`SMALL TAP: ${r.smallTargets.join(", ")}`);
      if (r.notes.length) bits.push(r.notes.join("; "));

      if (bits.length) { problems += bits.length; console.log(`  ✗ ${page}\n      ${bits.join("\n      ")}`); }
      else { console.log(`  ✓ ${page}`); }
    }
  }

  console.log(problems ? `\n${problems} issue(s) found.` : "\nAll checks passed.");
  ws.close(); chrome.kill(); process.exit(problems ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
