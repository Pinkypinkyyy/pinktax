(function () {
  var GA = "G-8T6SXPNSCW";
  var GT = "GT-WVXQ29L2";
  // Google Ads conversion ID. Empty until the Ads account supplies it — the
  // tag is skipped rather than half-configured and silently wrong.
  var AW = "";
  // Meta dataset 'Pink Document Capture' in Events Manager. Confirm this is
  // the dataset you want before it carries real spend; the name suggests it
  // was created for something else.
  var META = "26989404134047568";

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

  // One place to fire a Meta event. Everything that counts as a lead on
  // Google calls this too, so a lead cannot count on one platform and go
  // missing on the other.
  // ponytail: browser pixel only. The Conversions API needs a server and
  // this is static hosting — see the review note before relying on it.
  window.pinkMeta = function (ev, params) {
    try {
      if (typeof fbq === "function") fbq("track", ev, params || {});
    } catch (err) {}
  };
})();
