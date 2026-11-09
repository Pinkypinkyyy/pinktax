// Carries campaign parameters from the landing URL onto /book/ and the
// booking widget. With none of these present, hrefs are left untouched.
(function () {
  var KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"];
  var STORE = "pinkBookUtm";

  function pick(search) {
    var incoming = new URLSearchParams(search || "");
    var found = {};
    var any = false;
    KEYS.forEach(function (key) {
      var value = incoming.get(key);
      if (value) {
        found[key] = value;
        any = true;
      }
    });
    return any ? found : null;
  }

  function read() {
    try {
      var parsed = JSON.parse(sessionStorage.getItem(STORE) || "null");
      var found = {};
      var any = false;
      KEYS.forEach(function (key) {
        if (parsed && typeof parsed[key] === "string" && parsed[key]) {
          found[key] = parsed[key];
          any = true;
        }
      });
      return any ? found : null;
    } catch (err) {
      return null;
    }
  }

  function write(found) {
    try {
      sessionStorage.setItem(STORE, JSON.stringify(found));
    } catch (err) {}
  }

  var fromUrl = pick(window.location.search);
  if (fromUrl) write(fromUrl);
  var params = fromUrl || read();
  if (!params) return;

  function kindOf(url) {
    if (url.origin === window.location.origin && url.pathname.replace(/\/+$/, "") === "/book") return "book";
    if (url.hostname === "api.leadconnectorhq.com" && url.pathname.indexOf("/widget/bookings/") !== -1) return "widget";
    return "";
  }

  document.querySelectorAll("a[href]").forEach(function (anchor) {
    var href = anchor.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (err) {
      return;
    }
    var kind = kindOf(url);
    if (!kind) return;
    var changed = false;
    KEYS.forEach(function (key) {
      if (params[key] && !url.searchParams.has(key)) {
        url.searchParams.append(key, params[key]);
        changed = true;
      }
    });
    if (!changed) return;
    anchor.setAttribute("href", (kind === "book" ? "" : url.origin) + url.pathname + url.search + url.hash);
  });
})();
