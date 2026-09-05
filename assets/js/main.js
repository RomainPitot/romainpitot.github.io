// Pitot Engine portfolio — shared behaviour
(function () {
  "use strict";

  /* Hero: mouse-reactive glow + subtle parallax ---------------------------- */
  var heroSection = document.querySelector(".hero");
  var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (heroSection && !prefersReducedMotion) {
    var heroBg = heroSection.querySelector(".hero-bg");
    var pendingX = 0.5, pendingY = 0.35, rafScheduled = false;

    function renderPointer() {
      rafScheduled = false;
      heroSection.style.setProperty("--mx", (pendingX * 100) + "%");
      heroSection.style.setProperty("--my", (pendingY * 100) + "%");
      if (heroBg) {
        var dx = (pendingX - 0.5) * 20;
        var dy = (pendingY - 0.5) * 20;
        heroBg.style.transform = "translate(" + (-dx) + "px, " + (-dy) + "px)";
      }
    }

    heroSection.addEventListener("mousemove", function (e) {
      var rect = heroSection.getBoundingClientRect();
      pendingX = (e.clientX - rect.left) / rect.width;
      pendingY = (e.clientY - rect.top) / rect.height;
      heroSection.classList.add("mouse-active");
      if (!rafScheduled) {
        rafScheduled = true;
        requestAnimationFrame(renderPointer);
      }
    });

    heroSection.addEventListener("mouseleave", function () {
      heroSection.classList.remove("mouse-active");
      if (heroBg) heroBg.style.transform = "";
    });
  }

  /* Scroll progress bar ---------------------------------------------------- */
  var progressBar = document.querySelector(".scroll-progress");
  if (progressBar) {
    var updateProgress = function () {
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - doc.clientHeight;
      var pct = scrollable > 0 ? (doc.scrollTop / scrollable) * 100 : 0;
      progressBar.style.width = pct + "%";
    };
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
    updateProgress();
  }

  /* Nav hover indicator: sliding pill follows the hovered link ------------- */
  var navIndicator = document.querySelector(".nav-indicator");
  var navList = document.querySelector(".main-nav");
  if (navIndicator && navList) {
    var navLinks = Array.prototype.slice.call(navList.querySelectorAll("a"));
    var moveIndicatorTo = function (link) {
      navIndicator.style.left = link.offsetLeft + "px";
      navIndicator.style.width = link.offsetWidth + "px";
      navIndicator.style.opacity = "1";
    };
    navLinks.forEach(function (link) {
      link.addEventListener("mouseenter", function () { moveIndicatorTo(link); });
    });
    navList.addEventListener("mouseleave", function () {
      navIndicator.style.opacity = "0";
    });
  }

  /* Magnetic buttons -------------------------------------------------------- */
  if (!prefersReducedMotion) {
    document.querySelectorAll(".btn").forEach(function (btn) {
      btn.addEventListener("mousemove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = (e.clientX - r.left - r.width / 2) * 0.25;
        var dy = (e.clientY - r.top - r.height / 2) * 0.25;
        btn.style.transform = "translate(" + dx + "px, " + dy + "px)";
      });
      btn.addEventListener("mouseleave", function () {
        btn.style.transform = "";
      });
    });
  }

  /* Card tilt on hover ------------------------------------------------------ */
  document.querySelectorAll(".project-card, .system-card").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      // Spotlight follows the cursor even when motion is reduced (no movement, just light)
      card.style.setProperty("--sx", (e.clientX - r.left) + "px");
      card.style.setProperty("--sy", (e.clientY - r.top) + "px");
      if (prefersReducedMotion) return;
      var px = (e.clientX - r.left) / r.width - 0.5;
      var py = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform = "perspective(600px) scale(1.015) rotateX(" + (-py * 6) + "deg) rotateY(" + (px * 6) + "deg)";
    });
    card.addEventListener("mouseleave", function () {
      card.style.transform = "";
    });
  });

  /* Word-by-word scroll reveal ---------------------------------------------- */
  document.querySelectorAll(".reveal-words").forEach(function (el) {
    if (el.dataset.split === "done") return;
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    words.forEach(function (w, i) {
      var span = document.createElement("span");
      span.className = "word";
      span.textContent = w;
      span.style.transitionDelay = Math.min(i * 28, 700) + "ms";
      el.appendChild(span);
      if (i < words.length - 1) el.appendChild(document.createTextNode(" "));
    });
    el.dataset.split = "done";
  });

  /* Mobile nav toggle -------------------------------------------------- */
  var navToggle = document.querySelector(".nav-toggle");
  var mainNav = document.querySelector(".main-nav");
  if (navToggle && mainNav) {
    var iconMenu = navToggle.querySelector(".icon-menu");
    var iconClose = navToggle.querySelector(".icon-close");
    function setNavOpen(open) {
      mainNav.classList.toggle("mobile-open", open);
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (iconMenu) iconMenu.hidden = open;
      if (iconClose) iconClose.hidden = !open;
    }
    navToggle.addEventListener("click", function () {
      setNavOpen(!mainNav.classList.contains("mobile-open"));
    });
    mainNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setNavOpen(false); });
    });
  }

  /* Reveal-on-scroll ----------------------------------------------------- */
  var revealEls = document.querySelectorAll(".reveal, .reveal-words");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* Stat counters: count up when scrolled into view ------------------------ */
  var countEls = document.querySelectorAll("[data-count-to]");
  if (countEls.length) {
    var animateCount = function (el) {
      var target = parseFloat(el.getAttribute("data-count-to"));
      if (prefersReducedMotion || isNaN(target)) {
        el.textContent = target;
        return;
      }
      var steps = 22;
      var stepMs = 1100 / steps;
      var step = 0;
      var timer = setInterval(function () {
        step++;
        var p = Math.min(step / steps, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased);
        if (p >= 1) clearInterval(timer);
      }, stepMs);
    };
    if ("IntersectionObserver" in window) {
      var countIo = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              animateCount(entry.target);
              countIo.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.6 }
      );
      countEls.forEach(function (el) { countIo.observe(el); });
    } else {
      countEls.forEach(animateCount);
    }
  }

  /* Click-spark: tiny particle burst on button clicks ----------------------- */
  if (!prefersReducedMotion) {
    document.querySelectorAll(".btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        var count = 6;
        for (var i = 0; i < count; i++) {
          var angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.4;
          var distance = 22 + Math.random() * 18;
          var spark = document.createElement("span");
          spark.className = "click-spark";
          spark.style.left = e.clientX + "px";
          spark.style.top = e.clientY + "px";
          spark.style.setProperty("--dx", Math.cos(angle) * distance + "px");
          spark.style.setProperty("--dy", Math.sin(angle) * distance + "px");
          document.body.appendChild(spark);
          (function (node) {
            setTimeout(function () { node.remove(); }, 600);
          })(spark);
        }
      });
    });
  }

  /* Decrypt-text: hero name scrambles into place on load -------------------- */
  var decryptSegs = document.querySelectorAll("[data-decrypt] .decrypt-seg");
  if (decryptSegs.length && !prefersReducedMotion) {
    var SCRAMBLE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01#$%";
    decryptSegs.forEach(function (seg) {
      var original = seg.textContent;
      var len = original.length;
      var revealed = 0;
      var frame = 0;
      var timer = setInterval(function () {
        frame++;
        if (frame % 2 === 0 && revealed < len) revealed++;
        var out = "";
        for (var i = 0; i < len; i++) {
          if (original[i] === " ") { out += " "; continue; }
          out += i < revealed ? original[i] : SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
        }
        seg.textContent = out;
        if (revealed >= len) {
          seg.textContent = original;
          clearInterval(timer);
        }
      }, 40);
    });
  }

  /* i18n ------------------------------------------------------------------ */
  var LANG_KEY = "pitot-lang";
  function getLang() {
    try { return localStorage.getItem(LANG_KEY) || "en"; } catch (e) { return "en"; }
  }
  function setLang(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  }
  function applyLang(lang) {
    if (!window.PITOT_I18N) return;
    var dict = window.PITOT_I18N[lang] || window.PITOT_I18N.en;
    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var value = key.split(".").reduce(function (acc, k) { return acc && acc[k]; }, dict);
      if (typeof value === "string") el.textContent = value;
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-placeholder");
      var value = key.split(".").reduce(function (acc, k) { return acc && acc[k]; }, dict);
      if (typeof value === "string") el.setAttribute("placeholder", value);
    });
    var toggle = document.querySelector(".lang-toggle");
    if (toggle) toggle.textContent = lang === "en" ? "FR" : "EN";
  }
  var langToggle = document.querySelector(".lang-toggle");
  var currentLang = getLang();
  applyLang(currentLang);
  if (langToggle) {
    langToggle.addEventListener("click", function () {
      currentLang = currentLang === "en" ? "fr" : "en";
      setLang(currentLang);
      applyLang(currentLang);
    });
  }

  /* Projects filter / sort (projects listing page) ------------------------ */
  var filterBar = document.querySelector("[data-filter-bar]");
  if (filterBar) {
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-project-card]"));
    var filterBtns = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
    var sortBtns = Array.prototype.slice.call(document.querySelectorAll("[data-sort]"));
    var activeFilter = "All";
    var activeSort = "latest";

    function render() {
      var visible = cards.filter(function (card) {
        if (activeFilter === "All") return true;
        return (card.getAttribute("data-tags") || "").split("|").indexOf(activeFilter) !== -1;
      });
      visible.sort(function (a, b) {
        if (activeSort === "alpha") {
          return a.getAttribute("data-title").localeCompare(b.getAttribute("data-title"));
        }
        return Number(b.getAttribute("data-year")) - Number(a.getAttribute("data-year"));
      });
      var grid = document.querySelector("[data-project-grid]");
      cards.forEach(function (c) { c.style.display = "none"; });
      visible.forEach(function (c) {
        c.style.display = "";
        grid.appendChild(c);
      });
    }

    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activeFilter = btn.getAttribute("data-filter");
        filterBtns.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        render();
      });
    });
    sortBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activeSort = btn.getAttribute("data-sort");
        sortBtns.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        render();
      });
    });
    render();
  }

  /* Contact form -> Formspree (AJAX, stays on page) ------------------------ */
  var contactForm = document.querySelector("[data-contact-form]");
  if (contactForm) {
    var statusEl = contactForm.querySelector("[data-form-status]");
    var submitBtn = contactForm.querySelector("button[type=submit]");

    function t(key) {
      var dict = (window.PITOT_I18N && window.PITOT_I18N[currentLang]) || {};
      return key.split(".").reduce(function (acc, k) { return acc && acc[k]; }, dict) || key;
    }
    function showStatus(text, isError) {
      if (!statusEl) return;
      statusEl.textContent = text;
      statusEl.hidden = false;
      statusEl.style.color = isError ? "hsl(0 84% 65%)" : "hsl(var(--green))";
    }

    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (submitBtn) submitBtn.disabled = true;
      showStatus(t("contact.sending"), false);

      var subjectField = contactForm.querySelector("[name=subject]");
      var nameField = contactForm.querySelector("[name=name]");
      var hiddenSubject = contactForm.querySelector("[name=_subject]");
      if (hiddenSubject) {
        var userSubject = subjectField && subjectField.value.trim();
        var senderName = nameField && nameField.value.trim();
        hiddenSubject.value = userSubject
          ? "Portfolio contact: " + userSubject
          : "New message from " + (senderName || "your portfolio") + " (romainpitot.github.io)";
      }

      fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { Accept: "application/json" },
      })
        .then(function (response) {
          if (response.ok) {
            showStatus(t("contact.sent"), false);
            contactForm.reset();
          } else {
            showStatus(t("contact.error"), true);
          }
        })
        .catch(function () {
          showStatus(t("contact.error"), true);
        })
        .finally(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }
})();
