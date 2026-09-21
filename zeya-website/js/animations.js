/* ==========================================================================
   ZEYA CURTAINS & BLINDS — scroll motion
   IntersectionObserver reveals + a single rAF-driven parallax loop that only
   runs while a parallax layer is actually on screen.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel));
  }

  /* ---------------------------------------------------------------------
     Stagger indices
     Children of `.zeya-stagger` get an index that CSS turns into a delay.
  --------------------------------------------------------------------- */
  $$(".zeya-stagger").forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty("--zeya-index", String(i));
    });
  });

  /* ---------------------------------------------------------------------
     Line-by-line text reveal
     Authors write `data-zeya-lines` on a heading and separate the lines with
     <br>; each resulting line is wrapped so it can slide up from a mask.
  --------------------------------------------------------------------- */
  $$("[data-zeya-lines]").forEach(function (el) {
    if (el.querySelector(".zeya-line")) { return; }

    var parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map(function (part, i) {
      return '<span class="zeya-line" style="--zeya-index:' + i + '">' +
             '<span class="zeya-line__inner">' + part + "</span></span>";
    }).join("");
    el.classList.add("zeya-lines");
  });

  /* ---------------------------------------------------------------------
     Reveal on enter
  --------------------------------------------------------------------- */
  var revealSelector = ".zeya-reveal, .zeya-reveal-mask, .zeya-lines, .zeya-timeline";
  var targets = $$(revealSelector);

  function revealAll() {
    targets.forEach(function (el) { el.classList.add("is-in"); });
  }

  if (!("IntersectionObserver" in window) || reduced.matches) {
    revealAll();
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        entry.target.classList.add("is-in");
        observer.unobserve(entry.target);
      });
    }, {
      // Fire a little before the element reaches the fold, and treat anything
      // taller than the viewport as visible once its top edge is in view.
      rootMargin: "0px 0px -12% 0px",
      threshold: 0.08
    });

    targets.forEach(function (el) {
      // Anything already above the fold on load is shown immediately, so the
      // first screen never animates in after the user can see it.
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.88) {
        // Two frames so the hidden state paints first — otherwise the class
        // lands in the same frame and the transition is skipped entirely.
        window.requestAnimationFrame(function () {
          window.requestAnimationFrame(function () { el.classList.add("is-in"); });
        });
      } else {
        observer.observe(el);
      }
    });
  }

  /* ---------------------------------------------------------------------
     Parallax
     One rAF loop, started only while at least one layer intersects.
  --------------------------------------------------------------------- */
  (function parallax() {
    var layers = $$("[data-zeya-parallax]");
    if (!layers.length || reduced.matches || !("IntersectionObserver" in window)) { return; }

    var visible = [];
    var frame = null;

    function update() {
      frame = null;
      var vh = window.innerHeight;

      visible.forEach(function (layer) {
        var rect = layer.getBoundingClientRect();
        var speed = parseFloat(layer.getAttribute("data-zeya-parallax")) || 0.12;
        // -1 when the element sits below the fold, +1 when it has passed above.
        var progress = (rect.top + rect.height / 2 - vh / 2) / (vh / 2 + rect.height / 2);
        var shift = Math.max(-1, Math.min(1, progress)) * speed * rect.height * -1;
        layer.style.setProperty("--zeya-shift", shift.toFixed(2) + "px");
      });
    }

    function request() {
      if (frame === null && visible.length) {
        frame = window.requestAnimationFrame(update);
      }
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var i = visible.indexOf(entry.target);
        if (entry.isIntersecting && i === -1) {
          visible.push(entry.target);
        } else if (!entry.isIntersecting && i > -1) {
          visible.splice(i, 1);
          entry.target.style.setProperty("--zeya-shift", "0px");
        }
      });
      request();
    }, { rootMargin: "20% 0px" });

    layers.forEach(function (layer) {
      layer.classList.add("zeya-parallax");
      io.observe(layer);
    });

    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request, { passive: true });
    update();
  }());

  /* ---------------------------------------------------------------------
     Motion preference can change mid-session.
  --------------------------------------------------------------------- */
  var onPrefChange = function (event) {
    if (event.matches) { revealAll(); }
  };
  if (reduced.addEventListener) {
    reduced.addEventListener("change", onPrefChange);
  } else if (reduced.addListener) {
    reduced.addListener(onPrefChange);
  }
}());
