/* ==========================================================================
   ZEYA CURTAINS & BLINDS — main behaviour
   Vanilla JS, no dependencies. Loaded with `defer`.

   Contents
     0. Contact configuration  ← the only block you normally need to edit
     1. Helpers
     2. Header scroll state
     3. Mobile navigation
     4. Product dropdown
     5. Active page indicator
     6. Contact detail hydration
     7. Hero slide indicators
     8. Contact form
     9. Footer year
   ========================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------------
     0. CONTACT CONFIGURATION
     ---------------------------------------------------------------------
     Fill these in once the real ZEYA details are available. Anything left
     empty renders as a plain label with no link, exactly as in the design,
     so nothing on the page ever points at an invented number or address.

     In WordPress these same values come from functions.php (they are printed
     as `window.ZEYA_CONTACT` by wp_localize_script), so this object is only
     the static-site fallback.
  --------------------------------------------------------------------- */
  var CONTACT = window.ZEYA_CONTACT || {
    address: "Dubai, UAE",
    addressLine: "",    // optional second line, e.g. a street address
    addressUrl: "",     // e.g. a Google Maps link
    // Every WhatsApp link on the site reads from here: the floating button,
    // the product CTAs and the footer row all stay hidden until it is set.
    // Until then the floating "Book a consultation" pill holds that corner.
    // TEST NUMBER: replace both values with ZEYA's real WhatsApp number before launch.
    whatsapp: "971500000000",       // digits only, country code first
    whatsappLabel: "+971 50 000 0000",  // display form
    phone: "",          // e.g. "+971 4 000 0000"
    email: "",          // e.g. "hello@example.com"
    instagram: "",      // full profile URL
    facebook: "",       // full profile URL
    formEndpoint: ""    // POST target; leave empty until a handler is connected
  };

  /* ---------------------------------------------------------------------
     1. Helpers
  --------------------------------------------------------------------- */
  var doc = document;
  var root = doc.documentElement;

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }

  function digits(value) {
    return String(value || "").replace(/[^\d+]/g, "");
  }

  root.classList.add("zeya-js");

  /* ---------------------------------------------------------------------
     2. Header scroll state
     A zero-height sentinel at the top of the document is observed instead of
     listening to every scroll event.
  --------------------------------------------------------------------- */
  (function header() {
    var el = $("[data-zeya-header]");
    if (!el) { return; }

    // Inner pages render the solid bar from the start; only the transparent
    // variant needs the scroll transition.
    if (el.classList.contains("zeya-header--solid")) { return; }

    // A sentinel as tall as the trigger distance sits at the very top of the
    // document. While any part of it is still on screen the bar stays
    // transparent; once it has scrolled away the solid bar takes over.
    var sentinel = doc.createElement("div");
    sentinel.setAttribute("aria-hidden", "true");
    sentinel.style.cssText =
      "position:absolute;top:0;left:0;width:1px;height:80px;pointer-events:none;visibility:hidden;";
    doc.body.insertBefore(sentinel, doc.body.firstChild);

    if (!("IntersectionObserver" in window)) {
      el.classList.add("is-scrolled");
      return;
    }

    new IntersectionObserver(function (entries) {
      el.classList.toggle("is-scrolled", !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(sentinel);
  }());

  /* ---------------------------------------------------------------------
     3. Mobile navigation
  --------------------------------------------------------------------- */
  (function mobileNav() {
    var header = $("[data-zeya-header]");
    var burger = $("[data-zeya-burger]");
    var nav = $("[data-zeya-nav]");
    if (!burger || !nav || !header) { return; }

    var FOCUSABLE = 'a[href], button:not([disabled]), input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';
    var isOpen = false;

    function setOpen(open) {
      isOpen = open;
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
      header.classList.toggle("is-open", open);
      doc.body.classList.toggle("zeya-no-scroll", open);

      if (open) {
        var first = nav.querySelector(FOCUSABLE);
        if (first) { requestAnimationFrame(function () { if (isOpen) { first.focus(); } }); }
      }
    }

    burger.addEventListener("click", function () {
      setOpen(!isOpen);
    });

    // Close on navigation, Escape, or when the layout leaves the mobile range.
    nav.addEventListener("click", function (event) {
      if (isOpen && event.target.closest("a")) { setOpen(false); }
    });

    doc.addEventListener("keydown", function (event) {
      if (!isOpen) { return; }

      if (event.key === "Escape") {
        setOpen(false);
        burger.focus();
        return;
      }

      if (event.key !== "Tab") { return; }

      // Keep focus inside the open panel (the toggle stays part of the loop).
      var items = [burger].concat($$(FOCUSABLE, nav)).filter(function (node) {
        return node.offsetParent !== null || node === burger;
      });
      if (!items.length) { return; }

      var firstItem = items[0];
      var lastItem = items[items.length - 1];

      if (event.shiftKey && doc.activeElement === firstItem) {
        event.preventDefault();
        lastItem.focus();
      } else if (!event.shiftKey && doc.activeElement === lastItem) {
        event.preventDefault();
        firstItem.focus();
      }
    });

    var mq = window.matchMedia("(min-width: 961px)");
    var onChange = function (event) {
      if (event.matches && isOpen) { setOpen(false); }
    };
    if (mq.addEventListener) {
      mq.addEventListener("change", onChange);
    } else if (mq.addListener) {
      mq.addListener(onChange);
    }
  }());

  /* ---------------------------------------------------------------------
     4. Product dropdown
     On pointer devices the category panel opens on hover; the <details>
     element keeps working as a click/keyboard toggle everywhere else, so
     touch and no-JS visitors lose nothing.
  --------------------------------------------------------------------- */
  (function productMenu() {
    var wrap = $(".zeya-nav-products");
    var menu = wrap && $(".zeya-product-menu", wrap);
    if (!menu) { return; }

    var mq = window.matchMedia("(min-width: 901px) and (hover: hover)");
    var closeTimer = null;

    function hoverable() {
      return mq.matches;
    }

    function open(state) {
      window.clearTimeout(closeTimer);
      menu.open = state;
    }

    wrap.addEventListener("mouseenter", function () {
      if (hoverable()) { open(true); }
    });

    // A short grace period keeps the menu up while the pointer crosses the
    // gap between the link and the panel.
    wrap.addEventListener("mouseleave", function () {
      if (!hoverable()) { return; }
      window.clearTimeout(closeTimer);
      closeTimer = window.setTimeout(function () { menu.open = false; }, 120);
    });

    wrap.addEventListener("focusin", function () {
      if (hoverable()) { open(true); }
    });

    wrap.addEventListener("focusout", function (event) {
      if (hoverable() && !wrap.contains(event.relatedTarget)) { open(false); }
    });

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && menu.open) {
        open(false);
        // The summary is hidden on desktop, so hand focus back to whichever
        // of the two toggles is actually on screen.
        var toggle = $(".zeya-nav__link", wrap) || $("summary", menu);
        if (toggle && wrap.contains(doc.activeElement)) { toggle.focus(); }
      }
    });

    doc.addEventListener("click", function (event) {
      if (menu.open && !wrap.contains(event.target)) { open(false); }
    });

    // Leaving the hover range (or the mobile panel closing) must not strand
    // the menu open.
    var onChange = function () { open(false); };
    if (mq.addEventListener) {
      mq.addEventListener("change", onChange);
    } else if (mq.addListener) {
      mq.addListener(onChange);
    }
  }());

  /* ---------------------------------------------------------------------
     4b. Hero video
     The markup ships only a poster frame; the file itself is chosen here, so
     a visitor who asked for reduced motion never downloads it and a phone
     gets the light encode instead of the desktop one. Autoplay can still be
     refused by the browser — the poster simply stays, which is a valid hero.
  --------------------------------------------------------------------- */
  (function heroVideo() {
    var video = $("[data-zeya-hero-video]");
    if (!video) { return; }

    var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
    if (calm && calm.matches) {
      video.removeAttribute("autoplay");
      return;
    }

    var small = window.matchMedia && window.matchMedia("(max-width: 700px)").matches;
    var src = (small && video.getAttribute("data-src-sm")) || video.getAttribute("data-src");
    if (!src) { return; }

    video.src = src;
    var started = video.play();
    if (started && started.catch) { started.catch(function () { /* poster stays */ }); }
  }());

  /* ---------------------------------------------------------------------
     5. Active page indicator
     Driven by `data-zeya-page` on <body> so it also works once WordPress is
     generating the menu.
  --------------------------------------------------------------------- */
  (function activeLink() {
    var page = doc.body.getAttribute("data-zeya-page");
    if (!page) { return; }

    $$("[data-zeya-nav-item]").forEach(function (link) {
      var match = link.getAttribute("data-zeya-nav-item") === (['curtains', 'blinds', 'motorized', 'curtain-accessories'].indexOf(page) !== -1 || page.indexOf('product-') === 0 ? 'products' : page);
      link.classList.toggle("is-active", match);
      if (match) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }());

  /* ---------------------------------------------------------------------
     5b. WhatsApp enquiry links
     One number (CONTACT.whatsapp) feeds the floating button, the product
     CTAs and the footer/contact rows. Each link carries a prefilled message
     so the enquiry arrives with context instead of an empty chat. Anything
     marked [data-zeya-wa] stays hidden while no number is configured.
  --------------------------------------------------------------------- */
  function waNumber() {
    return digits(CONTACT.whatsapp).replace(/^\+/, "");
  }

  function waLink(product) {
    var number = waNumber();
    if (!number) { return ""; }
    var message = product
      ? "Hello ZEYA, I would like to enquire about " + product + "."
      : "Hello ZEYA, I would like to enquire about your curtains and blinds.";
    return "https://wa.me/" + number + "?text=" + encodeURIComponent(message);
  }

  (function whatsappEnquiry() {
    var nodes = $$("[data-zeya-wa]");
    if (!nodes.length || !waNumber()) { return; }

    // On the enquiry page the ?product= parameter is the visitor's context,
    // so the general button inherits it rather than asking twice.
    var selected = new URLSearchParams(window.location.search).get("product");
    var fromQuery = selected && /^[a-z0-9-]{1,100}$/.test(selected)
      ? selected.replace(/-/g, " ")
      : "";

    nodes.forEach(function (node) {
      var product = node.getAttribute("data-zeya-wa-product") || fromQuery;
      node.setAttribute("href", waLink(product));
      node.setAttribute("target", "_blank");
      node.setAttribute("rel", "noopener");
      node.removeAttribute("hidden");
    });

    // The floating consultation link stands in for the WhatsApp bubble
    // until a number exists; once it does, only one float is shown.
    $$("[data-zeya-consult-float]").forEach(function (node) {
      node.setAttribute("hidden", "");
    });
  }());

  /* ---------------------------------------------------------------------
     6. Contact detail hydration
     Placeholders stay as plain, unlinked labels until a real value exists.
  --------------------------------------------------------------------- */
  (function contactDetails() {
    var builders = {
      address: function (value) { return CONTACT.addressUrl || ""; },
      whatsapp: function (value) { return waLink(); },
      phone: function (value) { return "tel:" + digits(value); },
      email: function (value) { return "mailto:" + value; }
    };

    var displays = {
      // The address label already reads "Dubai, UAE", so the secondary line
      // stays empty until a fuller address is configured.
      address: function () { return CONTACT.addressLine || CONTACT.address || ""; },
      whatsapp: function () { return CONTACT.whatsappLabel || CONTACT.whatsapp; },
      phone: function () { return CONTACT.phone; },
      email: function () { return CONTACT.email; }
    };

    $$("[data-zeya-contact]").forEach(function (node) {
      var key = node.getAttribute("data-zeya-contact");
      var value = CONTACT[key === "address" ? "address" : key];
      var valueNode = node.querySelector("[data-zeya-contact-value]");
      var text = displays[key] ? displays[key]() : value;

      if (valueNode) {
        valueNode.textContent = text || "";
      }

      // Nothing configured means nothing to show: the row leaves the layout
      // rather than standing there as an empty label.
      if (text) {
        node.removeAttribute("hidden");
      } else {
        node.setAttribute("hidden", "");
      }

      var href = value && builders[key] ? builders[key](value) : "";

      if (node.tagName === "A") {
        if (href) {
          node.setAttribute("href", href);
          node.removeAttribute("aria-disabled");
          node.removeAttribute("tabindex");
          if (key === "whatsapp" || key === "address") {
            node.setAttribute("target", "_blank");
            node.setAttribute("rel", "noopener");
          }
        } else {
          node.removeAttribute("href");
          node.setAttribute("aria-disabled", "true");
        }
      }
    });

    $$(".zeya-methods").forEach(function (block) {
      var shown = $$(".zeya-method", block).some(function (row) {
        return !row.hasAttribute("hidden");
      });
      block.hidden = !shown;
    });

    // Social icons: only linked once a real profile URL is supplied.
    $$("[data-zeya-social]").forEach(function (node) {
      var url = CONTACT[node.getAttribute("data-zeya-social")];
      if (url) {
        node.setAttribute("href", url);
        node.setAttribute("target", "_blank");
        node.setAttribute("rel", "noopener");
        node.removeAttribute("aria-disabled");
      } else {
        node.removeAttribute("href");
        node.setAttribute("aria-disabled", "true");
      }
    });
  }());

  /* ---------------------------------------------------------------------
     7. Hero slide indicators
     The indicators only become interactive when more than one slide exists,
     so a single-image hero shows them as the quiet decorative marks in the
     design rather than pretending to be a carousel.
  --------------------------------------------------------------------- */
  (function heroSlides() {
    var region = $("[data-zeya-hero]");
    if (!region) { return; }

    var slides = $$("[data-zeya-hero-slide]", region);
    var marks = $$("[data-zeya-hero-mark]", region);
    if (slides.length < 2 || !marks.length) { return; }

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var index = 0;
    var timer = null;

    function show(next) {
      index = (next + slides.length) % slides.length;
      slides.forEach(function (slide, i) { slide.classList.toggle("is-active", i === index); });
      marks.forEach(function (mark, i) {
        mark.classList.toggle("is-active", i === index);
        mark.setAttribute("aria-selected", String(i === index));
      });
    }

    function start() {
      if (reduced) { return; }
      stop();
      timer = window.setInterval(function () { show(index + 1); }, 6500);
    }

    function stop() {
      if (timer) { window.clearInterval(timer); timer = null; }
    }

    marks.forEach(function (mark, i) {
      mark.addEventListener("click", function () { show(i); start(); });
    });

    region.addEventListener("mouseenter", stop);
    region.addEventListener("mouseleave", start);
    doc.addEventListener("visibilitychange", function () {
      if (doc.hidden) { stop(); } else { start(); }
    });

    show(0);
    start();
  }());

  /* ---------------------------------------------------------------------
     8. Contact form
     Client-side validation only. The markup mirrors Contact Form 7 / WPForms
     field naming so it can be swapped for a plugin-rendered form, and it will
     not claim to have sent anything unless a real endpoint is configured.
  --------------------------------------------------------------------- */
  (function contactForm() {
    var form = $("[data-zeya-form]");
    if (!form) { return; }

    var status = $("[data-zeya-form-status]", form);
    var submit = form.querySelector('[type="submit"]');
    var EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

    var rules = {
      "zeya-name": function (v) {
        if (!v.trim()) { return "Please enter your name."; }
        if (v.trim().length < 2) { return "Please enter your full name."; }
        return "";
      },
      "zeya-email": function (v) {
        if (!v.trim()) { return "Please enter your email address."; }
        if (!EMAIL.test(v.trim())) { return "Please enter a valid email address."; }
        return "";
      },
      "zeya-phone": function (v) {
        if (!v.trim()) { return "Please enter a phone number we can reach you on."; }
        if (digits(v).replace(/\D/g, "").length < 7) { return "Please enter a valid phone number."; }
        return "";
      },
      "zeya-message": function (v) {
        if (!v.trim()) { return "Please tell us a little about your space."; }
        if (v.trim().length < 10) { return "Please add a few more details."; }
        return "";
      }
    };

    function errorNode(field) {
      return doc.getElementById(field.id + "-error");
    }

    function setError(field, message) {
      var node = errorNode(field);
      field.setAttribute("aria-invalid", message ? "true" : "false");
      if (node) {
        node.textContent = message;
        node.classList.toggle("is-visible", Boolean(message));
      }
      return !message;
    }

    function validate(field) {
      var rule = rules[field.id];
      return rule ? setError(field, rule(field.value)) : true;
    }

    function setStatus(message, state) {
      if (!status) { return; }
      status.textContent = message;
      status.setAttribute("data-state", state);
      status.classList.toggle("is-visible", Boolean(message));
    }

    Object.keys(rules).forEach(function (id) {
      var field = doc.getElementById(id);
      if (!field) { return; }
      field.addEventListener("blur", function () { validate(field); });
      field.addEventListener("input", function () {
        if (field.getAttribute("aria-invalid") === "true") { validate(field); }
      });
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      // Honeypot: silently ignore anything that fills the hidden field.
      var trap = form.querySelector("[data-zeya-hp]");
      if (trap && trap.value) { return; }

      var firstInvalid = null;
      Object.keys(rules).forEach(function (id) {
        var field = doc.getElementById(id);
        if (field && !validate(field) && !firstInvalid) { firstInvalid = field; }
      });

      if (firstInvalid) {
        setStatus("Please check the highlighted fields and try again.", "error");
        firstInvalid.focus();
        return;
      }

      var endpoint = form.getAttribute("action") || CONTACT.formEndpoint;

      if (!endpoint) {
        // No handler wired up yet — say so plainly rather than faking a send.
        setStatus(
          "Your details are valid, but this form is not connected to a mail handler yet. " +
          "Connect Contact Form 7, WPForms or your own endpoint to start receiving enquiries — " +
          "in the meantime please reach us using the contact details on this page.",
          "info"
        );
        return;
      }

      setStatus("Sending your message…", "info");
      if (submit) { submit.disabled = true; }

      window.fetch(endpoint, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      }).then(function (response) {
        if (!response.ok) { throw new Error("Request failed"); }
        form.reset();
        setStatus("Thank you — your message has been sent. Our team will be in touch shortly.", "success");
      }).catch(function () {
        setStatus("Sorry, your message could not be sent. Please try again or contact us directly.", "error");
      }).then(function () {
        if (submit) { submit.disabled = false; }
      });
    });
  }());

  /* ---------------------------------------------------------------------
     9. Footer year
  --------------------------------------------------------------------- */
  $$("[data-zeya-year]").forEach(function (node) {
    node.textContent = String(new Date().getFullYear());
  });
}());

/* -----------------------------------------------------------------------
   Motion
   Three systems share one rAF loop and one reduced-motion check:

     reveals()   3D entrance, driven by IntersectionObserver
     tilt()      pointer-driven rotation on cards
     scroll()    hero parallax, editorial image drift, header progress

   The elements that animate are tagged from here rather than in the markup,
   so the generators stay free of presentation classes and the WordPress
   theme picks all of this up without a template change.

   Everything bails out under prefers-reduced-motion, and the scroll loop
   only does work on frames where the page has actually moved.
----------------------------------------------------------------------- */
(function motion() {
  var doc = document;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  function each(sel, fn, ctx) {
    Array.prototype.forEach.call((ctx || doc).querySelectorAll(sel), fn);
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  /* --------------------------------------------------------- reveals --- */
  (function reveals() {
    var SINGLE = [
      ".zeya-section-heading", ".zeya-split__copy", ".zeya-process__step",
      ".zeya-catalog-toolbar", ".zeya-detail-copy", ".zeya-formcard",
      ".zeya-footer-cta__inner", ".zeya-signature-heading", ".zeya-art__copy",
      ".zeya-services__intro"
    ];
    // Media settles in from further back than text does.
    var DEPTH = [".zeya-split__media", ".zeya-product-detail__media",
                 ".zeya-contact__aside", ".zeya-art__media",
                 ".zeya-service-band__image"];
    var GROUP = [".zeya-collections", ".zeya-steps", ".zeya-catalog-grid",
                 ".zeya-collection-nav", ".zeya-solution-grid", ".zeya-mini-grid",
                 ".zeya-quality-grid", ".zeya-service-band__features",
                 ".zeya-services__list"];

    var nodes = [];
    function tag(list, classes) {
      list.forEach(function (sel) {
        each(sel, function (node) {
          classes.forEach(function (c) { node.classList.add(c); });
          nodes.push(node);
        });
      });
    }
    tag(SINGLE, ["zeya-reveal"]);
    tag(DEPTH, ["zeya-reveal", "zeya-reveal--depth"]);
    tag(GROUP, ["zeya-stagger"]);
    if (!nodes.length) { return; }

    if (reduced.matches || !("IntersectionObserver" in window)) {
      nodes.forEach(function (n) { n.classList.add("is-revealed"); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        entry.target.classList.add("is-revealed");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });

    nodes.forEach(function (n) { observer.observe(n); });
  }());

  /* ------------------------------------------------------------ tilt --- */
  /* Only for devices that actually have a pointer to follow: a finger has no
     hover state, and tilting under a fingertip just hides the card. */
  (function tilt() {
    var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
    if (!fine.matches || reduced.matches) { return; }

    var MAX = 5.5; // degrees of rotation at the card's edge

    each(".zeya-product, .zeya-collection, .zeya-solution", function (card) {
      card.classList.add("zeya-tilt");

      var frame = null;
      var box = null;
      var point = { x: 0.5, y: 0.5 };

      function paint() {
        frame = null;
        card.style.setProperty("--zeya-ry", ((point.x - 0.5) * 2 * MAX).toFixed(2) + "deg");
        card.style.setProperty("--zeya-rx", ((0.5 - point.y) * 2 * MAX).toFixed(2) + "deg");
        card.style.setProperty("--zeya-mx", (point.x * 100).toFixed(1) + "%");
        card.style.setProperty("--zeya-my", (point.y * 100).toFixed(1) + "%");
      }

      card.addEventListener("pointerenter", function () {
        box = card.getBoundingClientRect();
        card.classList.add("is-tilting");
      });

      card.addEventListener("pointermove", function (event) {
        if (!box) { box = card.getBoundingClientRect(); }
        point.x = clamp((event.clientX - box.left) / box.width, 0, 1);
        point.y = clamp((event.clientY - box.top) / box.height, 0, 1);
        if (frame) { return; } // at most one write per frame
        frame = window.requestAnimationFrame(paint);
      });

      function reset() {
        if (frame) { window.cancelAnimationFrame(frame); frame = null; }
        box = null;
        card.classList.remove("is-tilting");
        card.style.removeProperty("--zeya-rx");
        card.style.removeProperty("--zeya-ry");
      }
      card.addEventListener("pointerleave", reset);
      card.addEventListener("pointercancel", reset);
    });
  }());

  /* ---------------------------------------------------------- scroll --- */
  (function scrollMotion() {
    if (reduced.matches) { return; }

    var hero = doc.querySelector(".zeya-hero");
    var heroMedia = hero && hero.querySelector(".zeya-hero__media");

    var drifters = [];
    each(".zeya-split__media, .zeya-product-detail__media, .zeya-contact__aside," +
         " .zeya-footer-cta__media, .zeya-art__media, .zeya-service-band__image",
         function (n) { drifters.push(n); });

    // The progress rule is injected rather than authored into the markup, so
    // the WordPress header gets it without a template change.
    var header = doc.querySelector("[data-zeya-header]");
    var progress = null;
    if (header) {
      progress = doc.createElement("span");
      progress.className = "zeya-header__progress";
      progress.setAttribute("aria-hidden", "true");
      header.appendChild(progress);
    }

    if (!hero && !drifters.length && !progress) { return; }

    // Only the frames currently on screen get written to each tick.
    var visible = drifters.slice();
    if ("IntersectionObserver" in window && drifters.length) {
      visible = [];
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          var at = visible.indexOf(entry.target);
          if (entry.isIntersecting && at === -1) {
            visible.push(entry.target);
            entry.target.classList.add("is-parallaxing");
          } else if (!entry.isIntersecting && at !== -1) {
            visible.splice(at, 1);
            entry.target.classList.remove("is-parallaxing");
            entry.target.style.removeProperty("--zeya-shift");
          }
        });
      }, { rootMargin: "20% 0px 20% 0px" });
      drifters.forEach(function (n) { io.observe(n); });
    }

    var ticking = false;
    var last = -1;

    function paint() {
      ticking = false;
      var y = window.pageYOffset || doc.documentElement.scrollTop;
      var vh = window.innerHeight || doc.documentElement.clientHeight;

      if (hero) {
        var h = hero.offsetHeight || 1;
        hero.style.setProperty("--zeya-p", clamp(y / h, 0, 1).toFixed(4));
        if (heroMedia) { heroMedia.style.willChange = y < h ? "transform" : "auto"; }
      }

      visible.forEach(function (node) {
        var rect = node.getBoundingClientRect();
        // -1 while the frame is entering from below, +1 on its way out.
        var centre = (rect.top + rect.height / 2) / vh;
        node.style.setProperty("--zeya-shift", clamp((centre - 0.5) * 2, -1, 1).toFixed(4));
      });

      if (progress) {
        var max = doc.documentElement.scrollHeight - vh;
        progress.style.setProperty("--zeya-progress",
          max > 0 ? clamp(y / max, 0, 1).toFixed(4) : "0");
      }
    }

    function onScroll() {
      var y = window.pageYOffset || doc.documentElement.scrollTop;
      if (y === last) { return; } // nothing moved, so nothing to repaint
      last = y;
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(paint);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { last = -1; onScroll(); },
                            { passive: true });
    paint();
  }());
}());

// Carry the selected product into the enquiry without overwriting user input.
document.addEventListener('DOMContentLoaded', function () {
  var product = new URLSearchParams(window.location.search).get('product');
  var field = document.querySelector('[name="your-message"]');
  if (product && /^[a-z0-9-]{1,100}$/.test(product) && field && !field.value) {
    field.value = 'I would like to enquire about ' + product.replace(/-/g, ' ') + '.';
  }
});
