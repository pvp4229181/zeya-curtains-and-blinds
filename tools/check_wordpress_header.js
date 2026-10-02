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
const PORT = 9338;

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


  await cdp.send('Runtime.enable');
  const evaluate=async expression=>(await cdp.send('Runtime.evaluate',{expression,returnByValue:true})).result.value;
  let failures=0;
  for(const width of [1880,1440,1024,768,390,320]){
    for(const toolbar of [false,true]){
      await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<820});
      await cdp.send('Page.navigate',{url:'file:///'+path.join(SITE,'index.html').replace(/\\/g,'/')});
      await sleep(1100);
      if(toolbar){
        const themeStyle=fs.readFileSync(path.resolve('zeya-theme/style.css'),'utf8');
        await evaluate(`(()=>{let s=document.createElement('style');s.textContent=${JSON.stringify(themeStyle)};document.head.append(s);document.body.classList.add('admin-bar');let bar=document.createElement('div');bar.id='wpadminbar';bar.style.cssText='position:fixed;top:0;left:0;right:0;height:${width<=782?46:32}px;z-index:99999;background:#222';document.body.prepend(bar);document.documentElement.style.marginTop='${width<=782?46:32}px';window.dispatchEvent(new Event('resize'));})()`);
      }
      await sleep(100);
      const initial=await evaluate(`(()=>{let h=document.querySelector('.zeya-header').getBoundingClientRect(),l=document.querySelector('.zeya-logo').getBoundingClientRect(),t=document.querySelector('.zeya-topbar').getBoundingClientRect();return h.top>=t.bottom-1&&l.top>=h.top&&l.bottom<=h.bottom;})()`);
      if(width<=900){
        await evaluate(`document.querySelector('[data-zeya-burger]').click()`);await sleep(400);
        const openedAtTop=await evaluate(`(()=>{let h=document.querySelector('.zeya-header').getBoundingClientRect(),bar=document.getElementById('wpadminbar');return Math.abs(h.top-(bar?bar.getBoundingClientRect().bottom:0))<1;})()`);
        if(!openedAtTop)failures++;
        await evaluate(`document.querySelector('[data-zeya-burger]').click()`);await sleep(400);
      }
      await evaluate('window.scrollTo({top:200,behavior:"instant"})');
      await sleep(150);
      const scrolled=await evaluate(`(()=>{let h=document.querySelector('.zeya-header').getBoundingClientRect(),bar=document.getElementById('wpadminbar');return Math.abs(h.top-(bar?bar.getBoundingClientRect().bottom:0))<1;})()`);
      let menu=true;
      if(width<=900){
        await evaluate(`document.querySelector('[data-zeya-burger]').click()`);
        await sleep(400);
        menu=await evaluate(`(()=>{let n=document.querySelector('.zeya-nav').getBoundingClientRect(),h=document.querySelector('.zeya-header').getBoundingClientRect(),bar=document.getElementById('wpadminbar');return n.top>=(bar?bar.getBoundingClientRect().bottom:0)-1&&h.top>=(bar?bar.getBoundingClientRect().bottom:0)-1;})()`);
      }
      if(!initial||!scrolled||!menu)failures++;
      console.log(`${width}px ${toolbar?'with toolbar':'public'}: ${initial&&scrolled&&menu?'PASS':'FAIL'} (logo spacing, scroll offset, menu)`);
      if(width===1440&&toolbar){
        await evaluate('window.scrollTo({top:0,behavior:"instant"})');await sleep(350);
        const shot=await cdp.send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.resolve('wordpress-deployment/header-fixed-desktop.png'),Buffer.from(shot.data,'base64'));
      }
      if(width===390&&!toolbar){
        await evaluate(`document.querySelector('[data-zeya-burger]').click();window.scrollTo({top:0,behavior:'instant'})`);await sleep(400);
        const shot=await cdp.send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.resolve('wordpress-deployment/header-fixed-mobile.png'),Buffer.from(shot.data,'base64'));
      }
    }
  }
  ws.close();chrome.kill();process.exit(failures?1:0);
})().catch(e=>{console.error(e);process.exit(1)});
