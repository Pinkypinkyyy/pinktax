(function () {
  var nav = document.getElementById("pinkNav");
  var btn = document.getElementById("pinkBurger");

  function setMenu(open) {
    if (!nav || !btn) return;
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (nav && btn) {
    btn.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    document.addEventListener("click", function (e) {
      if (!nav.classList.contains("open")) return;
      if (nav.contains(e.target)) return;
      setMenu(false);
    });
  }

  /* Count-up on the proof bar. The correct values are already printed in the
     HTML, so this only animates them once when the band first scrolls into
     view. No JS, old browser or reduced motion: the numbers are simply there. */
  var ticks = document.querySelectorAll(".tick");
  if (
    ticks.length &&
    "IntersectionObserver" in window &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    var fmtTick = function (el, v) {
      var dp = parseInt(el.getAttribute("data-dp") || "0", 10);
      var s = v.toFixed(dp);
      if (el.getAttribute("data-sep") === "1") {
        var parts = s.split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        s = parts.join(".");
      }
      return (el.getAttribute("data-prefix") || "") + s;
    };
    var runTick = function (el) {
      var to = parseFloat(el.getAttribute("data-to"));
      if (!isFinite(to)) return;
      var dur = 1100;
      var t0 = null;
      var step = function (t) {
        if (t0 === null) t0 = t;
        var p = Math.min(1, (t - t0) / dur);
        el.textContent = fmtTick(el, to * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
        else el.textContent = fmtTick(el, to);
      };
      requestAnimationFrame(step);
    };
    var tickIO = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          tickIO.unobserve(e.target);
          runTick(e.target);
        });
      },
      { threshold: 0.4 }
    );
    ticks.forEach(function (el) {
      tickIO.observe(el);
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) {
    var nodes = document.querySelectorAll(".pcol, .feat, .tier, .stepc, .funnel .card, .meet");
    nodes.forEach(function (el) { el.classList.add("reveal"); });
    if ("IntersectionObserver" in window) {
      // Only now is it safe for CSS to hide anything.
      document.documentElement.classList.add("js-anim");
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.16 });
      document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
      // Failsafe. Whatever happens to the observer, nothing stays invisible.
      setTimeout(function () {
        document.querySelectorAll(".reveal:not(.is-in)").forEach(function (el) {
          el.classList.add("is-in");
        });
      }, 2500);
    }
  }

  var bar = document.getElementById("bookBar");
  if (bar) {
    window.addEventListener("scroll", function () {
      var y = window.scrollY || 0;
      var nearFoot = document.documentElement.scrollHeight - window.innerHeight - y < 280;
      bar.classList.toggle("show", y > 520 && !nearFoot && window.innerWidth > 940);
    }, { passive: true });
  }

  document.querySelectorAll("[data-event]").forEach(function (el) {
    el.addEventListener("click", function () {
      try {
        var row = {
          t: Date.now(),
          e: el.getAttribute("data-event"),
          href: el.getAttribute("href") || ""
        };
        var prev = JSON.parse(sessionStorage.getItem("spEvents") || "[]");
        prev.push(row);
        sessionStorage.setItem("spEvents", JSON.stringify(prev.slice(-50)));
        if (typeof gtag === "function") {
          gtag("event", "select_content", { content_id: row.e });
          // Intake moved wholly into Microsoft Bookings, which is another
          // origin we cannot observe. The click onto the calendar is the last
          // event we own, so it carries the Ads conversion.
          if (row.e === "book-calendar") {
            gtag("event", "generate_lead", { method: "booking-calendar" });
            if (typeof window.pinkMeta === "function") {
              window.pinkMeta("Lead", { content_name: "booking-calendar" });
            }
          }
        }
      } catch (err) {}
    });
  });

  // Every phone number on the site. A venue owner who rings instead of
  // booking is the same lead, and until now that click was invisible.
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href^="tel:"]') : null;
    if (!a) return;
    try {
      if (typeof gtag === "function") {
        gtag("event", "phone_click", { lead_source: "site_phone_link" });
      }
      if (typeof window.pinkMeta === "function") window.pinkMeta("Contact");
    } catch (err) {}
  });

  var hoursForm = document.getElementById("hoursCheck");
  var hoursOut = document.getElementById("hoursResult");
  var hoursLine = document.getElementById("hoursResultLine");
  if (hoursForm && hoursOut && hoursLine) {
    hoursForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var quoted = parseFloat(hoursForm.quoted.value);
      var tools = parseFloat(hoursForm.tools.value);
      var rate = parseFloat(hoursForm.rate.value);
      if (!(quoted > 0) || !(tools > 0) || !(rate > 0)) return;
      var extra = Math.max(0, Math.round((tools - quoted) * 10) / 10);
      var dollars = Math.round(extra * rate);
      if (extra <= 0) {
        hoursLine.textContent =
          "That job landed on quote. The leak is often the next job, or the bank. Book 15 minutes if the quotes and the tax still do not match.";
      } else {
        hoursLine.textContent =
          "That job ran " + extra + " hours over. At $" + rate +
          " an hour, about $" + dollars +
          " never made the next quote.";
      }
      hoursOut.hidden = false;
      hoursOut.scrollIntoView({ behavior: "smooth", block: "nearest" });
      try {
        if (typeof gtag === "function") gtag("event", "generate_lead", { method: "hours-check" });
      } catch (err) {}
    });
  }

  // Enquiry relays. Any form carrying data-relay posts to the firm mailbox
  // and counts as a lead, so the contact page and the margin check share one
  // tested path instead of two. The value of data-relay is the GA4 method.
  //
  // What a relay form may carry: a name, an email, a phone number, a venue
  // and a message. Nothing else. A venue's takings and wages never go through
  // a third-party relay — the margin check keeps those in the browser.
  document.querySelectorAll("form[data-relay]").forEach(function (form) {
    var ok = document.getElementById(form.getAttribute("data-ok") || "");
    var method = form.getAttribute("data-relay") || "enquiry-form";
    var subject = form.getAttribute("data-subject") || "Pink Accounting enquiry";

    function succeeded() {
      form.hidden = true;
      if (ok) ok.hidden = false;
      var pick = document.getElementById("pick-time");
      if (pick) {
        pick.classList.add("is-next");
        pick.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    if (ok && new URLSearchParams(window.location.search).get("sent") === "1") {
      succeeded();
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var trap = form.querySelector("[name=_gotcha]");
      if (trap && trap.value) return;
      var btn = form.querySelector("button[type=submit]");
      var label = btn ? btn.textContent : "";
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Sending…";
      }
      var data = {};
      new FormData(form).forEach(function (value, key) {
        data[key] = value;
      });
      data._template = "table";
      data._captcha = "false";
      data._subject = subject;
      fetch("https://formsubmit.co/ajax/admin@pinktax.com.au", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("send-failed");
          return res.json();
        })
        .then(function (json) {
          // The relay answers 200 with success:"false" when the endpoint is
          // not activated or the post is rejected. Reading only res.ok would
          // thank the visitor, hide the form and count a conversion for an
          // enquiry that was never delivered.
          if (!json || String(json.success) === "false") throw new Error("not-sent");
          succeeded();
          try {
            if (typeof gtag === "function") gtag("event", "generate_lead", { method: method });
            if (typeof window.pinkMeta === "function") {
              window.pinkMeta("Lead", { content_name: method });
            }
          } catch (err) {}
        })
        .catch(function () {
          // The relay is someone else's server. If it is down the enquiry
          // still has to reach us, so hand it to the visitor's mail client.
          var body = Object.keys(data)
            .filter(function (k) {
              return k.charAt(0) !== "_" && data[k];
            })
            .map(function (k) {
              return k.charAt(0).toUpperCase() + k.slice(1) + ": " + data[k];
            })
            .join("\n");
          window.location.href =
            "mailto:admin@pinktax.com.au?subject=" +
            encodeURIComponent(subject) +
            "&body=" +
            encodeURIComponent(body);
        })
        .finally(function () {
          if (btn) {
            btn.disabled = false;
            btn.textContent = label;
          }
        });
    });
  });
})();
