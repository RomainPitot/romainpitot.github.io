// Home page only: the palette follows the scroll like the mission clock in
// Global Invasion: Day (hero) -> Night (the work) -> Dawn (the call to action).
//
// The day palette is the CSS default for html[data-page="home"], so there is no
// flash and no dependency on this script. The script only blends towards the
// night and dawn palettes. Colours are blended in RGB, not HSL: hues 40 and 228
// would otherwise pass through green and magenta on the way.
(function () {
  "use strict";

  var root = document.documentElement;
  if (root.getAttribute("data-page") !== "home") return;
  var hero = document.querySelector("[data-swarm-hero]");
  var dawnEl = document.querySelector("[data-phase-dawn]");
  var hud = document.querySelector(".phase-hud");
  if (!hero || !dawnEl) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Palettes as [h, s%, l%]. Day = default CSS, kept here to blend from.
  var DAY = {
    "--background": [40, 30, 92], "--background-deep": [38, 26, 86], "--foreground": [25, 24, 11],
    "--card": [40, 36, 96], "--card-foreground": [25, 24, 11], "--primary": [16, 85, 38],
    "--primary-foreground": [40, 45, 97], "--secondary": [38, 24, 85], "--secondary-foreground": [25, 14, 30],
    "--muted": [38, 24, 86], "--muted-foreground": [25, 12, 33], "--accent": [201, 85, 27],
    "--accent-foreground": [40, 45, 97], "--border": [35, 20, 76], "--indigo": [234, 60, 42],
    "--teal": [174, 80, 24], "--violet": [280, 55, 38], "--green": [142, 70, 24]
  };
  var NIGHT = {
    "--background": [228, 25, 10], "--background-deep": [228, 33, 5], "--foreground": [210, 40, 98],
    "--card": [228, 22, 14], "--card-foreground": [210, 40, 96], "--primary": [38, 92, 60],
    "--primary-foreground": [20, 14, 8], "--secondary": [228, 20, 18], "--secondary-foreground": [215, 25, 72],
    "--muted": [228, 20, 17], "--muted-foreground": [215, 20, 62], "--accent": [196, 80, 54],
    "--accent-foreground": [228, 25, 10], "--border": [228, 20, 20], "--indigo": [234, 89, 74],
    "--teal": [174, 72, 56], "--violet": [280, 68, 72], "--green": [142, 71, 55]
  };
  // Dawn: the day palette, warmer and a little pinker.
  var DAWN = {};
  Object.keys(DAY).forEach(function (k) {
    var v = DAY[k].slice();
    if (k === "--background") v = [24, 62, 90];
    if (k === "--background-deep") v = [22, 52, 84];
    if (k === "--card") v = [26, 66, 95];
    if (k === "--border") v = [22, 38, 74];
    DAWN[k] = v;
  });
  var KEYS = Object.keys(DAY);

  function hslToRgb(h, s, l) {
    h = ((h % 360) + 360) % 360 / 360; s /= 100; l /= 100;
    var q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    function f(t) {
      if (t < 0) t += 1; if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }
    return [f(h + 1 / 3), f(h), f(h - 1 / 3)];
  }
  function rgbToHsl(r, g, b) {
    var max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2, h = 0, s = 0, d = max - min;
    if (d) {
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      if (max === r) h = (g - b) / d + (g < b ? 6 : 0);
      else if (max === g) h = (b - r) / d + 2;
      else h = (r - g) / d + 4;
      h *= 60;
    }
    return [h, s * 100, l * 100];
  }
  function mix(a, b, t) {
    if (t <= 0) return a;
    if (t >= 1) return b;
    var ra = hslToRgb(a[0], a[1], a[2]), rb = hslToRgb(b[0], b[1], b[2]);
    return rgbToHsl(ra[0] + (rb[0] - ra[0]) * t, ra[1] + (rb[1] - ra[1]) * t, ra[2] + (rb[2] - ra[2]) * t);
  }
  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function smooth(t) { return t * t * (3 - 2 * t); }
  function css(c) { return Math.round(c[0]) + " " + Math.round(c[1]) + "% " + Math.round(c[2]) + "%"; }

  var queued = false, lastKey = "";

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  function update() {
    queued = false;
    var y = window.pageYOffset, vh = window.innerHeight;
    var heroH = hero.offsetHeight;
    var tNight = smooth(clamp01((y - heroH * 0.5) / (heroH * 0.22)));
    var dTop = dawnEl.getBoundingClientRect().top;
    var tDawn = smooth(clamp01((vh * 0.85 - dTop) / (vh * 0.3)));
    if (reduced) { tNight = tNight > 0.5 ? 1 : 0; tDawn = tDawn > 0.5 ? 1 : 0; }

    var key = tNight.toFixed(3) + "|" + tDawn.toFixed(3);
    if (key === lastKey) return;
    lastKey = key;

    if (tNight === 0 && tDawn === 0) {
      KEYS.forEach(function (k) { root.style.removeProperty(k); });
    } else {
      KEYS.forEach(function (k) {
        var base = mix(DAY[k], NIGHT[k], tNight);
        root.style.setProperty(k, css(mix(base, DAWN[k], tDawn)));
      });
    }

    var phase = tDawn > 0.5 ? "dawn" : tNight > 0.5 ? "night" : "day";
    root.setAttribute("data-phase", phase);
    if (hud) {
      // 07:00 -> 23:00 across the day-to-night blend, then 23:00 -> 05:30.
      var hours = 7 + tNight * 16;
      if (tDawn > 0) hours = 23 + tDawn * 6.5;
      var hh = Math.floor(hours) % 24, mm = Math.floor((hours % 1) * 60);
      hud.querySelector(".phase-name").textContent = phase.toUpperCase();
      hud.querySelector(".phase-time").textContent = pad(hh) + ":" + pad(mm);
    }
  }

  function queue() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(update);
  }
  // Keep the chip off the footer text.
  var footer = document.querySelector(".site-footer");
  if (hud && footer && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      hud.classList.toggle("is-hidden", entries[0].isIntersecting);
    }, { threshold: 0.15 }).observe(footer);
  }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue);
  update();
})();
