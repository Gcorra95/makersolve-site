/* ============================================================
   MakerSolve — comportamenti condivisi
   nav sticky · reveal on scroll · contatori · step attivi
   ============================================================ */
(function(){
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav che si solidifica allo scroll */
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function(){ nav.classList.toggle('stuck', window.scrollY > 20); };
    onScroll();
    addEventListener('scroll', onScroll, {passive:true});
  }

  /* anno corrente in footer */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* fallback: niente animazioni */
  if (rm || !('IntersectionObserver' in window)) {
    document.querySelectorAll('.rv').forEach(function(el){ el.classList.add('in'); });
    document.querySelectorAll('[data-count]').forEach(function(el){ el.textContent = el.dataset.count; });
    return;
  }

  /* reveal progressivo */
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, {threshold:.14, rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });

  /* contatori numerici */
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (!e.isIntersecting) return;
      var el = e.target, target = parseInt(el.dataset.count, 10), t0 = null;
      (function step(ts){
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / 1100, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
      cio.unobserve(el);
    });
  }, {threshold:.6});
  document.querySelectorAll('[data-count]').forEach(function(el){ cio.observe(el); });

  /* --------------------------------------------------------------
     Rete di sicurezza sul form.
     Finche' la access_key di Web3Forms non e' stata inserita, l'invio
     fallirebbe in silenzio e il contatto andrebbe perso. In quel caso
     intercettiamo il submit e apriamo una mail precompilata.
     Quando la chiave e' valida questo blocco non fa nulla.
     -------------------------------------------------------------- */
  document.querySelectorAll('form[action*="web3forms"]').forEach(function(f){
    var key = f.querySelector('[name="access_key"]');
    if (!key || key.value.indexOf('INSERISCI') === -1) return;

    var banner = document.createElement('p');
    banner.style.cssText = 'margin:0 0 18px;padding:12px 14px;border-radius:10px;'
      + 'background:rgba(255,176,32,.10);border:1px solid rgba(255,176,32,.35);'
      + 'color:#ffce7a;font-size:.82rem;line-height:1.5';
    banner.textContent = 'Invio diretto non ancora attivo: premendo il pulsante si apre '
      + 'il tuo programma di posta con la richiesta già compilata.';
    f.insertBefore(banner, f.firstChild);

    f.addEventListener('submit', function(ev){
      ev.preventDefault();
      var righe = [];
      f.querySelectorAll('input, select, textarea').forEach(function(el){
        if (!el.name || el.type === 'hidden' || el.type === 'checkbox' || el.type === 'file') return;
        if (!el.value) return;
        var lab = f.querySelector('label[for="' + el.id + '"]');
        righe.push((lab ? lab.textContent.replace(' *','').trim() : el.name) + ': ' + el.value);
      });
      var cfg = window.MAKERSOLVE_CONFIG || {};
      var dest = cfg.email || 'giulio.corazzari@gmail.com';
      window.location.href = 'mailto:' + dest
        + '?subject=' + encodeURIComponent('Richiesta di fattibilità — makersolve.com')
        + '&body=' + encodeURIComponent(righe.join('\n')
            + '\n\n(Allega qui foto, schizzi o file 3D prima di inviare.)');
    });
  });

  /* evidenzia lo step del metodo in vista */
  var steps = document.querySelectorAll('.step');
  if (steps.length) {
    var sio = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ e.target.classList.toggle('on', e.isIntersecting); });
    }, {threshold:.55});
    steps.forEach(function(el){ sio.observe(el); });
  }
})();
