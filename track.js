(function () {
  var GA = "G-8T6SXPNSCW";
  var GT = "GT-WVXQ29L2";
  // Google Ads conversion ID. Empty until the Ads account supplies the AW-
  // number. The Google tag GT-WVXQ29L2 still loads, so conversion linker
  // and GA4 import keep working. Do not invent an AW- id.
  var AW = "";
  // "Pink Accounting's Pixel", the only dataset in business 317537009282419
  // and the one attached to ad account 543906261707152, so it is the one Meta
  // can actually build audiences and optimise from.
  //
  // This was 26989404134047568 until 18 Sep 2026. That id is not a dataset in
  // this business at all: Events Manager routes it as an app and returns
  // "content isn't available", so every Meta event the site fired went
  // nowhere. Verified live before changing. Do not restore it.
  var META = "1237708438188688";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA);
  gtag("config", GT);
  if (AW) gtag("config", AW, { allow_enhanced_conversions: true });

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA;
  document.head.appendChild(s);

  if (META) {
    !function (f, b, e, v, n, t, s2) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = "2.0";
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s2 = b.getElementsByTagName(e)[0];
      s2.parentNode.insertBefore(t, s2);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    fbq("init", META);
    fbq("track", "PageView");
  }

  // SHA-256 hex for Meta advanced matching. Never pass a raw email or
  // phone to fbq. This site is static GitHub Pages, so there is no
  // Conversions API server; hashed browser matching is the closest we
  // can do without standing up a backend.
  function sha256hex(str) {
    if (!str || !window.crypto || !window.crypto.subtle) {
      return Promise.resolve("");
    }
    return window.crypto.subtle
      .digest("SHA-256", new TextEncoder().encode(str))
      .then(function (buf) {
        return Array.from(new Uint8Array(buf))
          .map(function (b) { return b.toString(16).padStart(2, "0"); })
          .join("");
      })
      .catch(function () { return ""; });
  }

  window.pinkHash = function (email, phone) {
    var em = String(email || "").trim().toLowerCase();
    var digits = String(phone || "").replace(/\D/g, "");
    if (digits.indexOf("0") === 0) digits = "61" + digits.slice(1);
    return Promise.all([sha256hex(em), sha256hex(digits)]).then(function (pair) {
      var out = {};
      if (pair[0]) out.em = pair[0];
      if (pair[1]) out.ph = pair[1];
      return out;
    });
  };

  // One place to fire a Meta event. Everything that counts as a lead on
  // Google calls this too, so a lead cannot count on one platform and go
  // missing on the other. Optional third argument is {em, ph} already hashed.
  window.pinkMeta = function (ev, params, hashed) {
    try {
      if (typeof fbq !== "function") return;
      if (hashed && (hashed.em || hashed.ph)) {
        fbq("init", META, hashed);
      }
      fbq("track", ev, params || {});
    } catch (err) {}
  };
})();
