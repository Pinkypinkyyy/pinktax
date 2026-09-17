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
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.16 });
      document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
    } else {
      document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
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
          }
        }
      } catch (err) {}
    });
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

  var form = document.getElementById("enquiryForm");
  var ok = document.getElementById("enquiryOk");
  if (form) {
    var params = new URLSearchParams(window.location.search);
    if (params.get("sent") === "1" && ok) {
      form.hidden = true;
      ok.hidden = false;
      var pick0 = document.getElementById("pick-time");
      if (pick0) {
        pick0.classList.add("is-next");
        pick0.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector("[name=_gotcha]").value) return;
      var btn = form.querySelector("button[type=submit]");
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
      fetch("https://formsubmit.co/ajax/admin@pinktax.com.au", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error("send-failed");
          return res.json();
        })
        .then(function () {
          form.hidden = true;
          if (ok) ok.hidden = false;
          var pick = document.getElementById("pick-time");
          if (pick) {
            pick.classList.add("is-next");
            pick.scrollIntoView({ behavior: "smooth", block: "start" });
          }
          try {
            if (typeof gtag === "function") gtag("event", "generate_lead", { method: "enquiry-form" });
          } catch (err) {}
        })
        .catch(function () {
          var body =
            "Name: " + (data.name || "") +
            "\nVenue: " + (data.venue || "") +
            "\nEmail: " + (data.email || "") +
            "\nMobile: " + (data.mobile || "") +
            "\nRevenue: " + (data.revenue || "") +
            "\nStaff: " + (data.staff || "") +
            "\nHurting: " + (data.hurt || "") +
            "\nCurrent position: " + (data.position || "") +
            "\n12-month vision: " + (data.vision || "");
          window.location.href =
            "mailto:admin@pinktax.com.au?subject=" +
            encodeURIComponent("Pink Accounting hospitality intake") +
            "&body=" +
            encodeURIComponent(body);
        })
        .finally(function () {
          if (btn) {
            btn.disabled = false;
            btn.textContent = "Send this";
          }
        });
    });
  }
})();
