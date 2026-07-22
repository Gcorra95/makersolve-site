/* ============================================================
   MakerSolve — comportamenti e animazioni della landing
   nav sticky · reveal · titolo a righe · contatori ·
   parallasse · alone reattivo · progressione del metodo
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- anno in footer ---------------- */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---------------- nav che si solidifica ---------------- */
  var nav = document.getElementById('nav');
  function onNav() {
    if (!nav) return;
    var stuck = window.scrollY > 24;
    nav.classList.toggle('bg-ink/80', stuck);
    nav.classList.toggle('backdrop-blur-xl', stuck);
    nav.classList.toggle('border-white/10', stuck);
    nav.classList.toggle('border-transparent', !stuck);
  }
  onNav();
  addEventListener('scroll', onNav, { passive: true });

  /* ---------------- menu mobile ---------------- */
  var burger = document.getElementById('burger');
  var menu = document.getElementById('mobilemenu');
  if (burger && menu) {
    var open = false;
    function setMenu(v) {
      open = v;
      menu.style.maxHeight = v ? menu.scrollHeight + 'px' : '0px';
      burger.setAttribute('aria-expanded', v ? 'true' : 'false');
      burger.setAttribute('aria-label', v ? 'Chiudi il menu' : 'Apri il menu');
      var l = burger.querySelectorAll('.burger-l');
      l[0].style.transform = v ? 'translateY(5px) rotate(45deg)' : '';
      l[1].style.opacity   = v ? '0' : '1';
      l[2].style.transform = v ? 'translateY(-5px) rotate(-45deg)' : '';
    }
    burger.addEventListener('click', function () { setMenu(!open); });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    addEventListener('resize', function () { if (innerWidth >= 1024 && open) setMenu(false); });
  }

  /* ---------------- form Web3Forms senza redirect ---------------- */
  document.querySelectorAll('form[action="https://api.web3forms.com/submit"]').forEach(function (form) {
    var file = form.querySelector('input[type="file"]');
    var status = form.querySelector('[data-form-status]');
    var button = form.querySelector('button[type="submit"]');
    var originalLabel = button ? button.textContent : '';

    function showStatus(message, ok) {
      if (!status) return;
      status.textContent = message;
      status.classList.remove('hidden', 'is-ok', 'is-error');
      status.classList.add(ok ? 'is-ok' : 'is-error');
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (file && file.files[0] && file.files[0].size > 5 * 1024 * 1024) {
        showStatus('L’allegato supera 5 MB. Invialo direttamente a giulio.corazzari@gmail.com.', false);
        file.focus();
        return;
      }
      if (button) { button.disabled = true; button.textContent = 'Invio in corso…'; }
      if (status) status.classList.add('hidden');

      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (response) { return response.json().then(function (data) { return { ok: response.ok, data: data }; }); })
        .then(function (result) {
          if (!result.ok || result.data.success === false) throw new Error(result.data.message || 'Invio non riuscito');
          form.reset();
          showStatus('Richiesta inviata correttamente. Riceverai una risposta entro 24/48 ore.', true);
        })
        .catch(function () {
          showStatus('Invio non riuscito. Puoi scrivere direttamente a giulio.corazzari@gmail.com allegando i file alla mail.', false);
        })
        .finally(function () {
          if (button) { button.disabled = false; button.textContent = originalLabel; }
        });
    });
  });

  /* ---------------- fallback senza animazioni ---------------- */
  if (reduced || !('IntersectionObserver' in window)) {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
    document.querySelectorAll('.lines').forEach(function (el) { el.classList.add('in'); });
    document.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = el.dataset.count; });
    return;
  }

  /* ---------------- reveal progressivo ---------------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var d = parseInt(e.target.dataset.d || 0, 10);
      e.target.style.transitionDelay = (d * 90) + 'ms';
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });

  /* ---------------- titolo che sale riga per riga ---------------- */
  document.querySelectorAll('.lines').forEach(function (el) {
    el.querySelectorAll('span > i').forEach(function (line, i) {
      line.style.transitionDelay = (120 + i * 130) + 'ms';
    });
  });
  var lio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); lio.unobserve(e.target); }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.lines').forEach(function (el) { lio.observe(el); });

  /* ---------------- contatori numerici ---------------- */
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target,
          target = parseInt(el.dataset.count, 10),
          t0 = null;
      requestAnimationFrame(function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / 1200, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      });
      cio.unobserve(el);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------------- fasi del metodo + barra di avanzamento ---------------- */
  var steps = Array.prototype.slice.call(document.querySelectorAll('.step'));
  var bar = document.getElementById('methodbar');
  if (steps.length) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var on = e.isIntersecting;
        e.target.classList.toggle('border-copper/50', on);
        e.target.classList.toggle('bg-ink-700', on);
        var b = e.target.querySelector('.bar');
        if (b) b.style.transform = on ? 'scaleY(1)' : 'scaleY(0)';
      });
      if (bar) {
        var done = steps.filter(function (s) { return s.classList.contains('border-copper/50'); });
        var last = steps.reduce(function (acc, s, i) {
          return s.getBoundingClientRect().top < window.innerHeight * 0.6 ? i + 1 : acc;
        }, 0);
        bar.style.transform = 'scaleX(' + (last / steps.length) + ')';
      }
    }, { threshold: 0.55 });
    steps.forEach(function (el) { sio.observe(el); });
  }

  /* ---------------- parallasse ---------------- */
  var pxEls = Array.prototype.slice.call(document.querySelectorAll('.parallax'));
  var ticking = false;
  function parallax() {
    var vh = window.innerHeight;
    pxEls.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      // -1 (sopra) .. 1 (sotto) rispetto al centro della finestra
      var rel = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
      el.style.setProperty('--py', (rel * -42).toFixed(1) + 'px');
    });
    ticking = false;
  }
  function reqParallax() {
    if (!ticking) { ticking = true; requestAnimationFrame(parallax); }
  }
  if (pxEls.length) {
    parallax();
    addEventListener('scroll', reqParallax, { passive: true });
    addEventListener('resize', reqParallax);
  }

  /* ---------------- alone che segue il puntatore ---------------- */
  var halo = document.getElementById('halo');
  var hero = halo && halo.closest('header');
  if (halo && hero && matchMedia('(pointer:fine)').matches) {
    var hx = 44, hy = 38, tx = 44, ty = 38, raf = null;
    hero.addEventListener('mousemove', function (ev) {
      var r = hero.getBoundingClientRect();
      tx = ((ev.clientX - r.left) / r.width) * 100;
      ty = ((ev.clientY - r.top) / r.height) * 100;
      if (!raf) raf = requestAnimationFrame(follow);
    });
    hero.addEventListener('mouseleave', function () { tx = 44; ty = 38; if (!raf) raf = requestAnimationFrame(follow); });
    function follow() {
      hx += (tx - hx) * 0.06;
      hy += (ty - hy) * 0.06;
      halo.style.left = hx.toFixed(2) + '%';
      halo.style.top = hy.toFixed(2) + '%';
      if (Math.abs(tx - hx) > 0.1 || Math.abs(ty - hy) > 0.1) { raf = requestAnimationFrame(follow); }
      else { raf = null; }
    }
  }

  /* ---------------- indicatore di scroll che svanisce ---------------- */
  var dot = document.getElementById('scrolldot');
  if (dot) {
    var wrapDot = dot.parentElement.parentElement;
    addEventListener('scroll', function () {
      wrapDot.style.opacity = window.scrollY > 120 ? '0' : '1';
      wrapDot.style.transition = 'opacity .4s';
    }, { passive: true });
  }
})();
