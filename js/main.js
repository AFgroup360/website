/* AmeriFinancial — site behaviour. No dependencies. */
(function () {
  'use strict';

  /* --- Endpoint the contact form posts to. -------------------------------
     Currently matches the previous site. If the site is served from static
     hosting with no backend, swap this for a form service endpoint
     (Formspree, Web3Forms) — nothing else needs to change.            */
  var CONTACT_ENDPOINT = '/api/contact';

  /* --- Mobile navigation -------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('primary-nav');
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });

    // Reset when the layout returns to desktop.
    var mq = window.matchMedia('(min-width: 901px)');
    var onChange = function (e) { if (e.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* --- Header shadow on scroll -------------------------------------------- */
  function initHeader() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var ticking = false;

    function update() {
      header.classList.toggle('is-stuck', window.scrollY > 8);
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });

    update();
  }

  /* --- FAQ accordion ------------------------------------------------------ */
  function initFaq() {
    document.querySelectorAll('.faq__q').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.faq__item');
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        item.classList.toggle('is-open', !open);
      });
    });
  }

  /* --- Scroll reveal ------------------------------------------------------- */
  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
      io.observe(el);
    });
  }

  /* --- Contact form -------------------------------------------------------- */
  function initContactForm() {
    var form = document.getElementById('contact-form');
    if (!form) return;

    var status = form.querySelector('.form-status');
    var submit = form.querySelector('[type="submit"]');
    var submitLabel = submit ? submit.textContent : '';

    function show(kind, message) {
      if (!status) return;
      status.textContent = message;
      status.className = 'form-status is-visible form-status--' + kind;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      if (!form.reportValidity()) return;

      var payload = Object.fromEntries(new FormData(form).entries());

      if (submit) { submit.disabled = true; submit.textContent = 'Sending…'; }

      fetch(CONTACT_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (res) {
          if (!res.ok) throw new Error('Request failed');
          form.reset();
          show('ok', 'Thank you — Farid will follow up shortly. If urgent, call +1 (416) 879-0969.');
        })
        .catch(function () {
          show('err', 'Something went wrong sending your message. Please email hello@ameri-group.ca or call +1 (416) 879-0969.');
        })
        .then(function () {
          if (submit) { submit.disabled = false; submit.textContent = submitLabel; }
        });
    });
  }

  /* --- Mark the current page in the nav ------------------------------------ */
  function initCurrent() {
    var path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    if (path.length > 1) path = path.replace(/\/$/, '');

    document.querySelectorAll('.nav__link').forEach(function (link) {
      var href = link.getAttribute('href') || '';
      var target = href.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
      if (target.length > 1) target = target.replace(/\/$/, '');
      if (target === path) link.setAttribute('aria-current', 'page');
    });
  }

  function init() {
    initNav();
    initHeader();
    initFaq();
    initReveal();
    initContactForm();
    initCurrent();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
