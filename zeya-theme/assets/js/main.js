/* ==========================================================================
   ZEYA CURTAINS & BLINDS — main behaviour
   Vanilla JS, no dependencies. Loaded with `defer`.

   Contents
     0. Contact configuration  ← the only block you normally need to edit
     1. Helpers
     2. Header scroll state
     3. Mobile navigation
     4. Active page indicator
     5. Contact detail hydration
     6. Hero slide indicators
     7. Contact form
     8. Footer year
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
    whatsapp: "",       // digits only, e.g. "971500000000"
    whatsappLabel: "",  // e.g. "+971 50 000 0000"
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
        if (first) { first.focus(); }
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
     4. Active page indicator
     Driven by `data-zeya-page` on <body> so it also works once WordPress is
     generating the menu.
  --------------------------------------------------------------------- */
  (function activeLink() {
    var page = doc.body.getAttribute("data-zeya-page");
    if (!page) { return; }

    $$("[data-zeya-nav-item]").forEach(function (link) {
      var match = link.getAttribute("data-zeya-nav-item") === (['curtains', 'blinds', 'motorized'].indexOf(page) !== -1 || page.indexOf('product-') === 0 ? 'products' : page);
      link.classList.toggle("is-active", match);
      if (match) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }());

  /* ---------------------------------------------------------------------
     5. Contact detail hydration
     Placeholders stay as plain, unlinked labels until a real value exists.
  --------------------------------------------------------------------- */
  (function contactDetails() {
    var builders = {
      address: function (value) { return CONTACT.addressUrl || ""; },
      whatsapp: function (value) { return "https://wa.me/" + digits(value).replace(/^\+/, ""); },
      phone: function (value) { return "tel:" + digits(value); },
      email: function (value) { return "mailto:" + value; }
    };

    var displays = {
      // The address label already reads "Dubai, UAE", so the secondary line
      // stays empty until a fuller address is configured.
      address: function () { return CONTACT.addressLine || ""; },
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
     6. Hero slide indicators
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
     7. Contact form
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
     8. Footer year
  --------------------------------------------------------------------- */
  $$("[data-zeya-year]").forEach(function (node) {
    node.textContent = String(new Date().getFullYear());
  });
}());

// Carry the selected product into the enquiry without overwriting user input.
document.addEventListener('DOMContentLoaded', function () {
  var product = new URLSearchParams(window.location.search).get('product');
  var field = document.querySelector('[name="your-message"]');
  if (product && /^[a-z0-9-]{1,100}$/.test(product) && field && !field.value) {
    field.value = 'I would like to enquire about ' + product.replace(/-/g, ' ') + '.';
  }
});
