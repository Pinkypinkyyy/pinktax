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
