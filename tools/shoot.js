/**
 * Full-page screenshots of the ZEYA static site via the Chrome DevTools
 * Protocol. No npm dependencies — Node's built-in WebSocket drives Chrome.
 *
 *   node tools/shoot.js 1440 desktop index about products process contact
 *   node tools/shoot.js 390 mobile index
 *
 * The viewport stays at a real size (so `svh` units behave) while
 * `captureBeyondViewport` grabs the whole document. Scroll-reveal elements are
 * forced into their settled state first, since nothing scrolls in a capture.
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
const PORT = 9333;

const width = parseInt(process.argv[2] || "1440", 10);
const tag = process.argv[3] || "desktop";
const pages = process.argv.slice(4).length ? process.argv.slice(4) : ["index"];
const mobile = width <= 820;

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function getJSON(url) {
  const res = await fetch(url);
  return res.json();
}

class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.sessionId = null;
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

(async () => {
  if (!CHROME) throw new Error("No Chrome or Edge binary found.");
  fs.mkdirSync(OUT, { recursive: true });

  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "zeya-prof-"));
  const chrome = spawn(CHROME, [
    "--headless=new",
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${profile}`,
    "--hide-scrollbars",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--allow-file-access-from-files",
    "about:blank",
  ], { stdio: "ignore" });

  // Wait for the debugging endpoint to come up.
  let version = null;
  for (let i = 0; i < 60 && !version; i++) {
    try {
      version = await getJSON(`http://127.0.0.1:${PORT}/json/version`);
    } catch (_) {
      await sleep(250);
    }
  }
  if (!version) throw new Error("Chrome did not expose a debugging port.");

  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r, { once: true }));
  const cdp = new CDP(ws);

  const { targetId } = await cdp.send("Target.createTarget", { url: "about:blank" }, false);
  const { sessionId } = await cdp.send("Target.attachToTarget", { targetId, flatten: true }, false);
  cdp.sessionId = sessionId;

  await cdp.send("Page.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width,
    height: mobile ? 844 : 900,
    deviceScaleFactor: 1,
    mobile,
    screenWidth: width,
    screenHeight: mobile ? 844 : 900,
  });

  for (const page of pages) {
    const url = "file:///" + path.join(SITE, page + ".html").replace(/\\/g, "/");
    await cdp.send("Page.navigate", { url });
    await sleep(2200);

    // Settle every scroll-reveal, as nothing scrolls during a capture.
    await cdp.send("Runtime.evaluate", {
      expression: `
        document.querySelectorAll('.zeya-reveal,.zeya-reveal-mask,.zeya-lines,.zeya-timeline')
          .forEach(function (el) { el.classList.add('is-in'); });
        document.querySelectorAll('img[loading="lazy"]')
          .forEach(function (img) { img.loading = 'eager'; });
      `,
      awaitPromise: false,
    });

    // Walk the page once. `captureBeyondViewport` will happily emit an unpainted
    // tile for content that has never been on screen, so this forces raster.
    await cdp.send("Runtime.evaluate", {
      expression: `new Promise(function (done) {
        var y = 0;
        var step = window.innerHeight * 0.75;
        (function next() {
          window.scrollTo(0, y);
          y += step;
          if (y < document.body.scrollHeight + step) {
            setTimeout(next, 90);
          } else {
            window.scrollTo(0, 0);
            setTimeout(done, 350);
          }
        }());
      })`,
      awaitPromise: true,
    });
    await sleep(600);

    // Wait until every image has actually decoded, otherwise a slow one paints
    // as an empty placeholder box in the capture.
    for (let i = 0; i < 40; i++) {
      const { result } = await cdp.send("Runtime.evaluate", {
        expression: `Array.from(document.images).filter(function (im) {
          return !im.complete || im.naturalWidth === 0;
        }).length`,
        returnByValue: true,
      });
      if (result.value === 0) break;
      await sleep(250);
    }
    await sleep(600);

    if (process.env.ZEYA_DEBUG) {
      const dbg = await cdp.send("Runtime.evaluate", {
        expression: `JSON.stringify(Array.from(document.images).map(function (im) {
          var r = im.getBoundingClientRect();
          return { src: im.currentSrc.split('/').pop(), complete: im.complete,
                   nw: im.naturalWidth, w: Math.round(r.width), h: Math.round(r.height),
                   op: getComputedStyle(im).opacity, cp: getComputedStyle(im.parentElement).clipPath };
        }))`,
        returnByValue: true,
      });
      console.log(dbg.result.value);
    }

    const metrics = await cdp.send("Page.getLayoutMetrics");
    const size = metrics.cssContentSize || metrics.contentSize;

    const shot = await cdp.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: true,
      clip: { x: 0, y: 0, width: size.width, height: size.height, scale: 1 },
    });

    const file = path.join(OUT, `${page}-${tag}.png`);
    fs.writeFileSync(file, Buffer.from(shot.data, "base64"));
    console.log(`${file}  ${size.width}x${Math.round(size.height)}`);
  }

  ws.close();
  chrome.kill();
  process.exit(0);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
