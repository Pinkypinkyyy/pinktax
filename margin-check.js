(function () {
  var form = document.getElementById("pmc-calc");
  if (!form) return;
  var BENCH = {
    wage: { t: 30, w: 35, l: "Wage cost" },
    cogs: { t: 36, w: 40, l: "Food & beverage cost" },
    prime: { t: 62, w: 68, l: "Prime cost (wages + stock)" },
    rent: { t: 10, w: 15, l: "Rent" },
    margin: { good: 15, thin: 5, l: "Operating margin" }
  };
  function $(id) { return document.getElementById(id); }
  function fmt(n) { return Math.round(n).toLocaleString("en-AU"); }
  function band(p, b) { return p <= b.t ? "good" : p <= b.w ? "watch" : "leak"; }
  function word(s) { return s === "good" ? "On track" : s === "watch" ? "Watch" : "Leak"; }
  function card(label, pct, bench, state) {
    return '<article class="card"><h3>' + label + '</h3><p><strong>' + pct.toFixed(1) + '%</strong> · ' + word(state) + '</p><p>' + bench + "</p></article>";
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var sales = parseFloat($("pmc-sales").value) || 0;
    var err = $("pmc-err");
    if (sales <= 0) {
      err.hidden = false;
      return;
    }
    err.hidden = true;
    var wages = parseFloat($("pmc-wages").value) || 0;
    var cogs = parseFloat($("pmc-cogs").value) || 0;
    var rentM = parseFloat($("pmc-rent").value) || 0;
    var other = parseFloat($("pmc-other").value) || 0;
    var rentW = (rentM * 12) / 52;
    var wageP = (wages / sales) * 100;
    var cogsP = (cogs / sales) * 100;
    var primeP = ((wages + cogs) / sales) * 100;
    var rentP = (rentW / sales) * 100;
    var marginP = ((sales - wages - cogs - rentW - other) / sales) * 100;
    var annual = sales * 52;
    var cards = [];
    cards.push(card(BENCH.wage.l, wageP, "Aim ≤" + BENCH.wage.t + "%", band(wageP, BENCH.wage)));
    cards.push(card(BENCH.cogs.l, cogsP, "Aim ≤" + BENCH.cogs.t + "%", band(cogsP, BENCH.cogs)));
    cards.push(card(BENCH.prime.l, primeP, "Aim ≤" + BENCH.prime.t + "%", band(primeP, BENCH.prime)));
    cards.push(card(BENCH.rent.l, rentP, "Aim ≤" + BENCH.rent.t + "%", band(rentP, BENCH.rent)));
    $("pmc-metrics").innerHTML = cards.join("");
    var leaks = [
      { d: ((wageP - BENCH.wage.t) / 100) * annual, msg: "Wages are running hot" },
      { d: ((cogsP - BENCH.cogs.t) / 100) * annual, msg: "Food and beverage cost is high" },
      { d: ((rentP - BENCH.rent.t) / 100) * annual, msg: "Rent is eating more than it should" }
    ].sort(function (a, b) { return b.d - a.d; });
    var top = leaks[0];
    if (top.d > 0 && marginP < BENCH.margin.good) {
      $("pmc-hl-label").textContent = "Your most likely leak";
      $("pmc-hl-text").textContent = top.msg + " — about $" + fmt(top.d) + "/yr above benchmark";
    } else if (marginP >= BENCH.margin.good && top.d <= 0) {
      $("pmc-hl-label").textContent = "Nice work";
      $("pmc-hl-text").textContent = "Your headline ratios are in range";
    } else {
      $("pmc-hl-label").textContent = "Worth a closer look";
      $("pmc-hl-text").textContent = "Your operating margin is " + marginP.toFixed(1) + "%";
    }
    $("pmc-hl-note").textContent = "Sketch from the numbers you typed. Not your file. Not a promise.";
    var out = $("pmc-results");
    out.hidden = false;
    out.scrollIntoView({ behavior: "smooth", block: "start" });
    try {
      if (typeof gtag === "function") gtag("event", "pink_margin_check_complete", { method: "calculator" });
    } catch (err2) {}
  });
})();
