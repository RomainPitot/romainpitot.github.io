// Background: a field of short strokes that follows a slow noise flow and reacts
// to the pointer (they swirl around it, stretch and light up) and to clicks (a
// ripple). Nothing here is tied to a project: it is just the site's surface.
(function () {
  "use strict";
  var canvas = document.querySelector(".bg-field");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W = 0, H = 0, cols = 0, rows = 0, GAP = 30;
  var mx = -9999, my = -9999, tx = -9999, ty = -9999, active = 0;
  var ripples = [];
  var running = true, raf = 0;
  var base = [128, 128, 128], hot = [255, 180, 60];

  function readColors() {
    var s = getComputedStyle(document.documentElement);
    function triplet(name) {
      var m = /([\d.]+)\s+([\d.]+)%\s+([\d.]+)%/.exec(s.getPropertyValue(name));
      if (!m) return null;
      var h = +m[1] / 360, sa = +m[2] / 100, l = +m[3] / 100;
      var q = l < 0.5 ? l * (1 + sa) : l + sa - l * sa, p = 2 * l - q;
      function f(t) { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < 0.5 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; }
      return [Math.round(f(h + 1 / 3) * 255), Math.round(f(h) * 255), Math.round(f(h - 1 / 3) * 255)];
    }
    base = triplet("--muted-foreground") || base;
    hot = triplet("--primary") || hot;
  }

  // Cheap smooth noise: sum of a few sines, good enough for a slow flow.
  function flow(x, y, t) {
    return Math.sin(x * 0.0031 + t * 0.21) * 1.6 + Math.sin(y * 0.0043 - t * 0.17) * 1.4 +
      Math.sin((x + y) * 0.0021 + t * 0.11) * 1.2;
  }

  function resize() {
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    GAP = W < 700 ? 34 : 30;
    cols = Math.ceil(W / GAP) + 1; rows = Math.ceil(H / GAP) + 1;
  }

  function draw(now) {
    var t = now / 1000;
    mx += (tx - mx) * 0.18; my += (ty - my) * 0.18;
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = "round";
    var R = 190, R2 = R * R;
    for (var i = ripples.length - 1; i >= 0; i--) {
      ripples[i].r += 9; ripples[i].a -= 0.014;
      if (ripples[i].a <= 0) ripples.splice(i, 1);
    }
    for (var gy = 0; gy < rows; gy++) {
      for (var gx = 0; gx < cols; gx++) {
        var x = gx * GAP + (gy % 2 ? GAP / 2 : 0), y = gy * GAP;
        var ang = flow(x, y, t), len = 6, heat = 0;
        var dx = x - mx, dy = y - my, d2 = dx * dx + dy * dy;
        if (d2 < R2) {
          var k = 1 - Math.sqrt(d2) / R; k = k * k * (3 - 2 * k) * active;
          // swirl: blend the flow angle toward the tangent around the pointer
          var tang = Math.atan2(dy, dx) + Math.PI / 2;
          var da = Math.atan2(Math.sin(tang - ang), Math.cos(tang - ang));
          ang += da * k; len += 14 * k; heat = k;
        }
        for (var r = 0; r < ripples.length; r++) {
          var rp = ripples[r], dd = Math.sqrt((x - rp.x) * (x - rp.x) + (y - rp.y) * (y - rp.y)) - rp.r;
          if (dd > -40 && dd < 40) {
            var w = (1 - Math.abs(dd) / 40) * rp.a;
            ang += Math.atan2(y - rp.y, x - rp.x) * 0 + w * 1.5; len += 12 * w; heat = Math.max(heat, w);
          }
        }
        var cx = Math.cos(ang) * len / 2, cy = Math.sin(ang) * len / 2;
        var a = 0.22 + heat * 0.75;
        var c = heat > 0.02 ? hot : base;
        ctx.strokeStyle = "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a.toFixed(3) + ")";
        ctx.lineWidth = 1.4 + heat * 1.4;
        ctx.beginPath(); ctx.moveTo(x - cx, y - cy); ctx.lineTo(x + cx, y + cy); ctx.stroke();
      }
    }
    active += ((tx > -9000 ? 1 : 0) - active) * 0.08;
  }

  function loop(now) {
    if (!running) return;
    draw(now);
    raf = requestAnimationFrame(loop);
  }

  window.addEventListener("pointermove", function (e) { tx = e.clientX; ty = e.clientY; if (mx < -9000) { mx = tx; my = ty; } }, { passive: true });
  window.addEventListener("pointerleave", function () { tx = -9999; ty = -9999; });
  window.addEventListener("pointerdown", function (e) {
    if (e.target.closest && e.target.closest("a, button, input, textarea, select, label")) return;
    ripples.push({ x: e.clientX, y: e.clientY, r: 0, a: 1 });
  }, { passive: true });
  window.addEventListener("resize", function () { resize(); if (reduced) draw(0); });
  document.addEventListener("visibilitychange", function () {
    running = !document.hidden && !reduced;
    if (running) raf = requestAnimationFrame(loop);
  });

  readColors();
  resize();
  if (reduced) { draw(0); } else { raf = requestAnimationFrame(loop); }
})();
