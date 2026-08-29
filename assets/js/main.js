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
  var revealEls = document.querySelectorAll(".reveal");
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
