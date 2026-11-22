// Hero swarm: a small canvas port of the SwarmSim from Global Invasion.
//
// Same ideas as the game, at web scale:
//  - plain typed arrays, no per-roach objects (hundreds must stay cheap);
//  - the initial population comes from a seeded generator, so the layout is the
//    same on every visit ("N roaches appear here", seeded);
//  - they flee the cursor, a few bold ones come looking for it, and they crowd
//    the name without ever covering it;
//  - a click is a broom hit: roaches in the circle die, and new ones enter from
//    the edges a moment later.
// Reduced motion: one settled frame, no loop, no pointer handling.
(function () {
  "use strict";

  var hero = document.querySelector("[data-swarm-hero]");
  if (!hero) return;
  var canvas = hero.querySelector(".swarm-canvas");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var nameEl = hero.querySelector("[data-swarm-name]");
  var countEl = hero.querySelector("[data-squash-count]");
  var root = document.documentElement;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = window.matchMedia("(max-width: 700px)").matches || window.matchMedia("(pointer: coarse)").matches;

  var CAPACITY = small ? 100 : 210;       // game: 400
  var FEAR_RADIUS = small ? 90 : 130;
  var BROOM_RADIUS = small ? 56 : 46;
  var BOLD_FRACTION = 0.12;               // game: 0.3
  var BASE_SPEED = 26;                    // px/s
  var FLEE_SPEED = 240;

  function mulberry32(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var rand = mulberry32(20261122);

  var x = new Float32Array(CAPACITY), y = new Float32Array(CAPACITY);
  var heading = new Float32Array(CAPACITY), speed = new Float32Array(CAPACITY);
  var size = new Float32Array(CAPACITY), gait = new Float32Array(CAPACITY);
  var bold = new Uint8Array(CAPACITY), alive = new Uint8Array(CAPACITY);
  var respawnAt = new Float32Array(CAPACITY);

  var W = 0, H = 0, dpr = 1;
  var nameRects = [];
  var ptr = { x: 0, y: 0, on: false };
  var splats = [];
  var squashed = 0;
  var clock = 0;
  var ink = "hsl(25 20% 12% / 0.9)";
  var stain = "hsl(16 85% 38% / 0.5)";
  var inkAt = -1;

  function spawnAt(i, px, py) {
    x[i] = px; y[i] = py;
    heading[i] = rand() * Math.PI * 2;
    speed[i] = BASE_SPEED * (0.6 + rand() * 0.9);
    size[i] = 0.75 + rand() * 0.55;
    gait[i] = rand() * 6.28;
    bold[i] = rand() < BOLD_FRACTION ? 1 : 0;
    alive[i] = 1;
  }

  function spawnOnEdge(i) {
    var side = Math.floor(rand() * 4), p = rand();
    if (side === 0) spawnAt(i, p * W, -8);
    else if (side === 1) spawnAt(i, W + 8, p * H);
    else if (side === 2) spawnAt(i, p * W, H + 8);
    else spawnAt(i, -8, p * H);
    heading[i] = Math.atan2(H / 2 - y[i], W / 2 - x[i]) + (rand() - 0.5);
  }

  function measure() {
    var r = hero.getBoundingClientRect();
    W = Math.max(1, Math.round(r.width));
    H = Math.max(1, Math.round(r.height));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // No-go rectangles: every line of the name (tight, the heading itself is
    // wider) and each text block. Only the name is crowded around.
    nameRects = [];
    var els = hero.querySelectorAll(".h1-line, [data-swarm-avoid]");
    for (var li = 0; li < els.length; li++) {
      var n = els[li].getBoundingClientRect();
      var isName = els[li].classList.contains("h1-line");
      nameRects.push({
        l: n.left - r.left - 8, r: n.right - r.left + 8,
        t: n.top - r.top + (isName ? 4 : -4), b: n.bottom - r.top + (isName ? -2 : 4),
        crowd: isName
      });
    }
  }

  function insideAny(px, py) {
    for (var q = 0; q < nameRects.length; q++) {
      var nr = nameRects[q];
      if (px > nr.l && px < nr.r && py > nr.t && py < nr.b) return true;
    }
    return false;
  }

  function populate() {
    for (var i = 0; i < CAPACITY; i++) {
      var px, py, tries = 0;
      do { px = rand() * W; py = rand() * H; tries++; } while (insideAny(px, py) && tries < 30);
      spawnAt(i, px, py);
      respawnAt[i] = 0;
    }
  }

  function readInk() {
    var cs = getComputedStyle(root);
    var fg = cs.getPropertyValue("--foreground").trim();
    var pr = cs.getPropertyValue("--primary").trim();
    if (fg) ink = "hsl(" + fg + " / 0.9)";
    if (pr) stain = "hsl(" + pr + " / 0.5)";
  }

  function step(dt) {
    clock += dt;
    var R2 = FEAR_RADIUS * FEAR_RADIUS;
    for (var i = 0; i < CAPACITY; i++) {
      if (!alive[i]) {
        if (respawnAt[i] > 0 && clock >= respawnAt[i]) { respawnAt[i] = 0; spawnOnEdge(i); }
        continue;
      }
      var px = x[i], py = y[i], h = heading[i], s = speed[i];

      // Wander: slow drift in heading.
      h += (rand() - 0.5) * 3.2 * dt;

      // Cursor: flee, except the bold ones that approach until they get close.
      if (ptr.on) {
        var dx = px - ptr.x, dy = py - ptr.y, d2 = dx * dx + dy * dy;
        if (bold[i] && d2 > 60 * 60 && d2 < 260 * 260) {
          h = turnToward(h, Math.atan2(-dy, -dx), 2.2 * dt);
        } else if (d2 < R2) {
          var d = Math.sqrt(d2) || 1;
          h = turnToward(h, Math.atan2(dy, dx), 9 * dt);
          s = BASE_SPEED + FLEE_SPEED * (1 - d / FEAR_RADIUS);
        }
      }

      // The name: never inside it, a little crowd around it.
      for (var q = 0; q < nameRects.length; q++) {
        var nr = nameRects[q];
        if (px > nr.l && px < nr.r && py > nr.t && py < nr.b) {
          var toL = px - nr.l, toR = nr.r - px, toT = py - nr.t, toB = nr.b - py;
          var m = Math.min(toL, toR, toT, toB);
          var tx = px, ty = py;
          if (m === toL) tx = nr.l - 4; else if (m === toR) tx = nr.r + 4;
          else if (m === toT) ty = nr.t - 4; else ty = nr.b + 4;
          h = turnToward(h, Math.atan2(ty - py, tx - px), 12 * dt);
          s = Math.max(s, 90);
        } else {
          var cx = Math.max(nr.l, Math.min(px, nr.r));
          var cy = Math.max(nr.t, Math.min(py, nr.b));
          var ex = cx - px, ey = cy - py, ed2 = ex * ex + ey * ey;
          if (nr.crowd && ed2 < 120 * 120 && ed2 > 16 * 16) h = turnToward(h, Math.atan2(ey, ex), 0.7 * dt);
        }
      }

      // Edges: turn back in.
      if (px < 6) h = turnToward(h, 0, 6 * dt); else if (px > W - 6) h = turnToward(h, Math.PI, 6 * dt);
      if (py < 6) h = turnToward(h, Math.PI / 2, 6 * dt); else if (py > H - 6) h = turnToward(h, -Math.PI / 2, 6 * dt);

      // Ease the speed back to a stroll.
      var target = bold[i] ? BASE_SPEED * 1.4 : speed[i];
      s += (target - s) * Math.min(1, 3 * dt);
      if (s < BASE_SPEED * 0.4) s = BASE_SPEED * 0.4;

      x[i] = px + Math.cos(h) * s * dt;
      y[i] = py + Math.sin(h) * s * dt;
      heading[i] = h;
      gait[i] += s * dt * 0.55;
    }
    for (var k = splats.length - 1; k >= 0; k--) {
      splats[k].age += dt;
      if (splats[k].age > 7) splats.splice(k, 1);
    }
  }

  function turnToward(h, target, amount) {
    var diff = target - h;
    while (diff > Math.PI) diff -= Math.PI * 2;
    while (diff < -Math.PI) diff += Math.PI * 2;
    if (Math.abs(diff) <= amount) return target;
    return h + (diff > 0 ? amount : -amount);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    for (var k = 0; k < splats.length; k++) {
      var sp = splats[k], a = Math.max(0, 1 - sp.age / 7) * 0.8;
      ctx.fillStyle = stain.replace(/\/ [0-9.]+\)/, "/ " + a.toFixed(2) + ")");
      for (var j = 0; j < 5; j++) {
        var ang = j * 1.256 + sp.seed, r = 3 + (j % 2) * 3;
        ctx.beginPath();
        ctx.arc(sp.x + Math.cos(ang) * r, sp.y + Math.sin(ang) * r, 1.6 + (j % 3) * 0.5, 0, 6.283);
        ctx.fill();
      }
    }

    ctx.fillStyle = ink;
    ctx.strokeStyle = ink;
    ctx.lineWidth = 1;
    for (var i = 0; i < CAPACITY; i++) {
      if (!alive[i]) continue;
      var px = x[i], py = y[i];
      if (px < -12 || px > W + 12 || py < -12 || py > H + 12) continue;
      var sc = size[i], c = Math.cos(heading[i]), sn = Math.sin(heading[i]);
      // Body axis along the heading.
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate(heading[i]);
      ctx.scale(sc, sc);
      ctx.beginPath();
      ctx.ellipse(0, 0, 5.4, 3.1, 0, 0, 6.283);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(5.8, 0, 1.9, 0, 6.283);
      ctx.fill();
      // Legs: three pairs, alternating.
      var g = Math.sin(gait[i]) * 1.6;
      ctx.beginPath();
      for (var l = -1; l <= 1; l++) {
        var lx = l * 2.6, sw = (l % 2 === 0 ? g : -g);
        ctx.moveTo(lx, 2.4); ctx.lineTo(lx + sw, 6.6);
        ctx.moveTo(lx, -2.4); ctx.lineTo(lx - sw, -6.6);
      }
      // Antennae.
      ctx.moveTo(7, 0.8); ctx.lineTo(10.5, 3.4);
      ctx.moveTo(7, -0.8); ctx.lineTo(10.5, -3.4);
      ctx.stroke();
      ctx.restore();
    }
  }

  // --- loop -----------------------------------------------------------------
  var running = false, visible = true, last = 0;
  function frame(now) {
    if (!running) return;
    var dt = Math.min(0.05, (now - last) / 1000 || 0.016);
    last = now;
    if (now - inkAt > 300) { readInk(); inkAt = now; }
    step(dt);
    draw();
    requestAnimationFrame(frame);
  }
  function start() {
    if (running || reduced || !visible || document.hidden) return;
    running = true; last = performance.now();
    requestAnimationFrame(frame);
  }
  function stop() { running = false; }

  // --- input ----------------------------------------------------------------
  function local(e) {
    var r = hero.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top, inside: e.clientY >= r.top && e.clientY <= r.bottom };
  }
  if (!reduced) {
    window.addEventListener("pointermove", function (e) {
      var p = local(e);
      ptr.x = p.x; ptr.y = p.y; ptr.on = p.inside;
    }, { passive: true });
    hero.addEventListener("pointerleave", function () { ptr.on = false; });
    window.addEventListener("pointerup", function (e) { if (e.pointerType === "touch") ptr.on = false; });
    hero.addEventListener("pointerdown", function (e) {
      if (e.target.closest("a, button")) return;
      var p = local(e), r2 = BROOM_RADIUS * BROOM_RADIUS, hits = 0;
      for (var i = 0; i < CAPACITY; i++) {
        if (!alive[i]) continue;
        var dx = x[i] - p.x, dy = y[i] - p.y;
        if (dx * dx + dy * dy < r2) {
          alive[i] = 0;
          respawnAt[i] = clock + 1.5 + rand() * 2.5;
          splats.push({ x: x[i], y: y[i], age: 0, seed: rand() * 6 });
          hits++;
        }
      }
      if (hits && countEl) { squashed += hits; countEl.textContent = squashed; }
    });
  }

  // --- setup ----------------------------------------------------------------
  function init() {
    measure();
    populate();
    readInk();
    if (reduced) {
      for (var n = 0; n < 150; n++) step(1 / 30);
      draw();
    } else {
      start();
    }
  }

  var resizeTimer = 0;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var oldW = W, oldH = H;
      measure();
      for (var i = 0; i < CAPACITY; i++) { x[i] = x[i] * W / (oldW || W); y[i] = y[i] * H / (oldH || H); }
      if (reduced) draw();
    }, 120);
  });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) start(); else stop();
    }).observe(hero);
  }
  document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else start(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

  init();
})();
