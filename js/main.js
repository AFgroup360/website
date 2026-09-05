/* AmeriFinancial site behaviour. No dependencies. */
(function () {
  'use strict';

  /* TODO Farid. Set this to a form service endpoint before going live.
     Formspree looks like https://formspree.io/f/xxxxxxxx and Web3Forms like
     https://api.web3forms.com/submit (with an access_key field added to the
     form). Until it is set, the form explains where to send the message. */
  var CONTACT_ENDPOINT = '';

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
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });

    var mq = window.matchMedia('(min-width: 901px)');
    var onChange = function (e) { if (e.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  function initCurrent() {
    function leaf(url) {
      var last = url.split('#')[0].split('?')[0].split('/').pop().replace(/\.html$/, '');
      return last === '' ? 'index' : last;
    }
    var here = leaf(window.location.pathname);
    // Articles sit under Our Thinking.
    if (here.indexOf('thinking-') === 0) here = 'our-thinking';
    document.querySelectorAll('.nav__link').forEach(function (link) {
      if (leaf(link.getAttribute('href') || '') === here) link.setAttribute('aria-current', 'page');
    });
  }

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

      if (!CONTACT_ENDPOINT) {
        show('err', 'The form is not connected yet. Please email hello@ameri-group.ca or call +1 (416) 879-0969.');
        return;
      }

      var payload = Object.fromEntries(new FormData(form).entries());
      if (submit) { submit.disabled = true; submit.textContent = 'Sending'; }

      fetch(CONTACT_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (res) {
          if (!res.ok) throw new Error('Request failed');
          form.reset();
          show('ok', 'Thank you. Farid will follow up shortly. If it is urgent, call +1 (416) 879-0969.');
        })
        .catch(function () {
          show('err', 'Something went wrong sending your message. Please email hello@ameri-group.ca or call +1 (416) 879-0969.');
        })
        .then(function () {
          if (submit) { submit.disabled = false; submit.textContent = submitLabel; }
        });
    });
  }

  function init() {
    initNav();
    initCurrent();
    initContactForm();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
