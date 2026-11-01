/* Autoservice Barneveld: menu en afspraakvenster.
   Het venster verstuurt niets zelf: het opent WhatsApp met een ingevuld bericht,
   dat de bezoeker daar zelf verstuurt. Zonder JavaScript gaan de knoppen naar
   de contactpagina. */
(function () {
  'use strict';

  var WHATSAPP = '31342234003';

  /* ---------- Menu op mobiel ---------- */
  var menuKnop = document.querySelector('.menu-knop');
  var menu = document.getElementById('menu');
  if (menuKnop && menu) {
    menuKnop.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      menuKnop.setAttribute('aria-expanded', open);
      menuKnop.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('open');
        menuKnop.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Kenteken: hoofdletters en controle ---------- */
  function kentekenOk(waarde) {
    var kaal = waarde.replace(/[\s-]/g, '');
    return /^[A-Z0-9]{6}$/i.test(kaal) && /[A-Z]/i.test(kaal) && /[0-9]/.test(kaal);
  }
  function controleerKenteken(invoer) {
    var positie = invoer.selectionStart;
    invoer.value = invoer.value.toUpperCase();
    if (positie !== null) invoer.setSelectionRange(positie, positie);
    invoer.setCustomValidity(invoer.value && !kentekenOk(invoer.value)
      ? 'Vul een Nederlands kenteken in, bijvoorbeeld AB-123-C.' : '');
  }
  Array.prototype.forEach.call(document.querySelectorAll('input[name="kenteken"]'), function (invoer) {
    invoer.addEventListener('input', function () { controleerKenteken(invoer); });
  });

  /* ---------- Afspraakvenster ---------- */
  var venster = document.getElementById('afspraak-venster');
  if (!venster || typeof venster.showModal !== 'function') return;

  var formulier = venster.querySelector('form');
  var stapInvullen = venster.querySelector('.venster-invullen');
  var stapKlaar = venster.querySelector('.venster-klaar');
  var linkOpnieuw = venster.querySelector('.wa-opnieuw');
  var velden = ['kenteken', 'dienst', 'kilometerstand', 'email'];
  function veld(naam) { return formulier.elements[naam]; }

  function open(waarden) {
    stapInvullen.hidden = false;
    stapKlaar.hidden = true;
    Object.keys(waarden).forEach(function (naam) {
      if (waarden[naam]) veld(naam).value = waarden[naam];
    });
    controleerKenteken(veld('kenteken'));
    venster.showModal();
    var leeg = velden.map(veld).filter(function (v) { return !v.value; })[0];
    (leeg || veld('kenteken')).focus();
  }

  // Stap 1 op de homepage: kenteken + dienst, daarna het venster
  var snel = document.getElementById('afspraak-snel');
  if (snel) {
    snel.addEventListener('submit', function (e) {
      e.preventDefault();
      open({ kenteken: snel.elements.kenteken.value, dienst: snel.elements.dienst.value });
    });
  }

  // Alle "Plan afspraak"-knoppen
  Array.prototype.forEach.call(document.querySelectorAll('[data-afspraak]'), function (knop) {
    knop.addEventListener('click', function (e) {
      e.preventDefault();
      open({ dienst: knop.getAttribute('data-dienst') || '' });
    });
  });

  venster.querySelector('.sluit').addEventListener('click', function () { venster.close(); });
  venster.addEventListener('click', function (e) { if (e.target === venster) venster.close(); });

  // Kilometerstand: alleen cijfers, met punten voor de leesbaarheid
  veld('kilometerstand').addEventListener('input', function () {
    var cijfers = this.value.replace(/\D/g, '').slice(0, 7);
    this.value = cijfers ? Number(cijfers).toLocaleString('nl-NL') : '';
  });

  formulier.addEventListener('submit', function (e) {
    e.preventDefault();
    controleerKenteken(veld('kenteken'));
    if (!formulier.reportValidity()) return;

    var bericht = [
      'Hallo Autoservice Barneveld,',
      '',
      'Ik wil graag een afspraak maken.',
      '',
      'Dienst: ' + veld('dienst').value,
      'Kenteken: ' + veld('kenteken').value.trim(),
      'Kilometerstand: ' + veld('kilometerstand').value + ' km',
      'Leenauto nodig: ' + (veld('leenauto').checked ? 'Ja' : 'Nee'),
      'E-mail: ' + veld('email').value.trim()
    ].join('\n');
    var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(bericht);

    linkOpnieuw.href = url;
    stapInvullen.hidden = true;
    stapKlaar.hidden = false;

    var tab = window.open(url, '_blank');
    if (tab) { tab.opener = null; } else { window.location.href = url; }
  });
}());

/* ---------- Reviewcarrousel ---------- */
(function () {
  'use strict';
  var kaart = document.querySelector('.review-kaart');
  if (!kaart) return;
  var dias = kaart.querySelectorAll('.review-dia');
  var bediening = kaart.querySelector('.review-bediening');
  if (dias.length < 2 || !bediening) return;

  var teller = kaart.querySelector('.review-teller');
  var pauzeKnop = kaart.querySelector('.review-pauze');
  var INTERVAL = 8000;
  var huidig = 0, timer = null;
  var gepauzeerd = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var erboven = false;

  bediening.hidden = false;

  function toon(n) {
    dias[huidig].classList.remove('actief');
    dias[huidig].setAttribute('aria-hidden', 'true');
    huidig = (n + dias.length) % dias.length;
    dias[huidig].classList.add('actief');
    dias[huidig].removeAttribute('aria-hidden');
    teller.textContent = (huidig + 1) + ' / ' + dias.length;
  }
  function start() {
    stop();
    if (!gepauzeerd && !erboven) timer = setInterval(function () { toon(huidig + 1); }, INTERVAL);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function zetPauze(aan) {
    gepauzeerd = aan;
    pauzeKnop.classList.toggle('gepauzeerd', aan);
    pauzeKnop.setAttribute('aria-label', aan ? 'Afspelen' : 'Pauzeren');
    start();
  }

  kaart.querySelector('.review-vorige').addEventListener('click', function () { toon(huidig - 1); start(); });
  kaart.querySelector('.review-volgende').addEventListener('click', function () { toon(huidig + 1); start(); });
  pauzeKnop.addEventListener('click', function () { zetPauze(!gepauzeerd); });

  // Stilhouden zolang de muis erop staat of de focus erin zit
  kaart.addEventListener('mouseenter', function () { erboven = true; stop(); });
  kaart.addEventListener('mouseleave', function () { erboven = false; start(); });
  kaart.addEventListener('focusin', function () { erboven = true; stop(); });
  kaart.addEventListener('focusout', function (e) { if (!kaart.contains(e.relatedTarget)) { erboven = false; start(); } });
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });

  zetPauze(gepauzeerd);
}());
