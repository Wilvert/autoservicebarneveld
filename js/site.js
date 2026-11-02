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

  // Vervangend vervoer: bij "Ja" de keuze tonen en verplicht maken
  var vervoerKeuze = venster.querySelector('.vervoer-keuze');
  var radios = vervoerKeuze.querySelectorAll('input[type="radio"]');
  function zetVervoer() {
    var aan = veld('vervoer').checked;
    vervoerKeuze.hidden = !aan;
    radios[0].required = aan;
    if (!aan) Array.prototype.forEach.call(radios, function (r) { r.checked = false; });
  }
  function keuzeVervoer() {
    var gekozen = vervoerKeuze.querySelector('input:checked');
    return gekozen ? gekozen.value : 'Ja';
  }
  veld('vervoer').addEventListener('change', zetVervoer);

  /* Voorkeursdatum: eigen kalender. Geblokkeerde dagen zijn niet te kiezen:
     - eerder dan twee weken vanaf vandaag
     - zaterdag en zondag
     - de weekdagen in GEBLOKKEERD (per maand, 'jjjj-mm'; 1 = ma, 2 = di, 3 = wo ...)
     - losse data in GEBLOKKEERDE_DATA ('jjjj-mm-dd') */
  var GEBLOKKEERD = {
    '2026-11': [2, 3],   // november: dinsdag en woensdag
    '2026-12': [2]       // december: dinsdag
  };
  var GEBLOKKEERDE_DATA = [];
  var MAANDEN_VOORUIT = 4;

  var datumKnop = venster.querySelector('.datum-knop');
  var datumKeuze = venster.querySelector('.datum-keuze');
  var kalMaand = venster.querySelector('.kal-maand');
  var kalRaster = venster.querySelector('.kal-raster');
  var kalVorige = venster.querySelector('.kal-vorige');
  var kalVolgende = venster.querySelector('.kal-volgende');
  var gekozenTekst = venster.querySelector('.datum-gekozen');
  var gekozen = [];
  var toonMaand;

  function twee(n) { return ('0' + n).slice(-2); }
  function iso(d) { return d.getFullYear() + '-' + twee(d.getMonth() + 1) + '-' + twee(d.getDate()); }
  function vandaag() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function eersteDag() { var d = vandaag(); d.setDate(d.getDate() + 14); return d; }
  function laatsteDag() { var d = vandaag(); d.setMonth(d.getMonth() + MAANDEN_VOORUIT); return d; }
  function lees(v) { var p = v.split('-'); return new Date(+p[0], p[1] - 1, +p[2]); }
  function mooiDatum(v) {
    return lees(v).toLocaleDateString('nl-NL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
  function kort(v) {
    return lees(v).toLocaleDateString('nl-NL', { weekday: 'short', day: 'numeric', month: 'short' });
  }
  function beschikbaar(d) {
    var dag = d.getDay();
    if (dag === 0 || dag === 6) return false;
    if (d < eersteDag() || d > laatsteDag()) return false;
    var maand = GEBLOKKEERD[d.getFullYear() + '-' + twee(d.getMonth() + 1)];
    if (maand && maand.indexOf(dag) !== -1) return false;
    return GEBLOKKEERDE_DATA.indexOf(iso(d)) === -1;
  }

  function teken() {
    var j = toonMaand.getFullYear(), m = toonMaand.getMonth();
    kalMaand.textContent = toonMaand.toLocaleDateString('nl-NL', { month: 'long', year: 'numeric' });
    var eerste = eersteDag(), laatste = laatsteDag();
    kalVorige.disabled = j * 12 + m <= eerste.getFullYear() * 12 + eerste.getMonth();
    kalVolgende.disabled = j * 12 + m >= laatste.getFullYear() * 12 + laatste.getMonth();
    kalRaster.innerHTML = '';
    var leeg = (new Date(j, m, 1).getDay() + 6) % 7;
    for (var i = 0; i < leeg; i++) kalRaster.appendChild(document.createElement('span'));
    var aantal = new Date(j, m + 1, 0).getDate();
    for (var dag = 1; dag <= aantal; dag++) {
      var d = new Date(j, m, dag), waarde = iso(d), knop = document.createElement('button');
      var nr = gekozen.indexOf(waarde);
      knop.type = 'button';
      knop.textContent = dag;
      knop.dataset.datum = waarde;
      knop.disabled = !beschikbaar(d);
      knop.setAttribute('aria-label', mooiDatum(waarde) + (knop.disabled ? ', niet beschikbaar' : nr !== -1 ? ', ' + (nr + 1) + 'e voorkeur' : ''));
      if (nr !== -1) { knop.className = 'gekozen'; knop.setAttribute('data-nr', nr + 1); knop.setAttribute('aria-pressed', 'true'); }
      kalRaster.appendChild(knop);
    }
    venster.querySelector('[name="datum1"]').value = gekozen[0] || '';
    venster.querySelector('[name="datum2"]').value = gekozen[1] || '';
    gekozenTekst.classList.remove('fout');
    gekozenTekst.innerHTML = gekozen.length
      ? '<span>1e voorkeur: <strong>' + kort(gekozen[0]) + '</strong></span><span>2e voorkeur: <strong>' + (gekozen[1] ? kort(gekozen[1]) : 'kies nog een dag') + '</strong></span>'
      : 'Klik op twee dagen die u schikken.';
  }
  kalRaster.addEventListener('click', function (e) {
    var waarde = e.target.dataset && e.target.dataset.datum;
    if (!waarde || e.target.disabled) return;
    var nr = gekozen.indexOf(waarde);
    if (nr !== -1) gekozen.splice(nr, 1);
    else if (gekozen.length < 2) gekozen.push(waarde);
    else gekozen[1] = waarde;
    teken();
    var zelfde = kalRaster.querySelector('[data-datum="' + waarde + '"]');
    if (zelfde) zelfde.focus();
  });
  kalVorige.addEventListener('click', function () { toonMaand.setMonth(toonMaand.getMonth() - 1); teken(); });
  kalVolgende.addEventListener('click', function () { toonMaand.setMonth(toonMaand.getMonth() + 1); teken(); });

  function zetDatum(aan) {
    datumKeuze.hidden = !aan;
    datumKnop.hidden = aan;
    datumKnop.setAttribute('aria-expanded', aan);
    gekozen = [];
    var e = eersteDag();
    toonMaand = new Date(e.getFullYear(), e.getMonth(), 1);
    teken();
  }
  function datumsOk() {
    if (datumKeuze.hidden || gekozen.length === 2) return true;
    gekozenTekst.textContent = 'Kies twee voorkeursdata, of klik op "Geen voorkeursdatum".';
    gekozenTekst.classList.add('fout');
    datumKeuze.scrollIntoView({ block: 'nearest' });
    return false;
  }
  datumKnop.addEventListener('click', function () {
    zetDatum(true);
    var eerste = kalRaster.querySelector('button:not(:disabled)');
    if (eerste) eerste.focus();
  });
  venster.querySelector('.datum-weg').addEventListener('click', function () {
    zetDatum(false);
    datumKnop.focus();
  });

  formulier.addEventListener('submit', function (e) {
    e.preventDefault();
    controleerKenteken(veld('kenteken'));
    if (!formulier.reportValidity() || !datumsOk()) return;

    // WhatsApp-bericht: kopjes met *vet* (WhatsApp-opmaak) en een emoji per blok
    var bericht = [
      'Hallo Autoservice Barneveld,',
      '',
      'Graag maak ik een afspraak. Hieronder mijn gegevens.',
      '',
      '🔧 *Werkzaamheden*',
      veld('dienst').value,
      '',
      '🚗 *Voertuig*',
      'Kenteken: ' + veld('kenteken').value.trim().toUpperCase(),
      'Kilometerstand: ' + veld('kilometerstand').value + ' km',
      '',
      '🔑 *Vervangend vervoer*',
      veld('vervoer').checked ? keuzeVervoer() : 'Niet nodig'
    ];
    if (!datumKeuze.hidden) {
      bericht.push('',
        '📅 *Voorkeursdata*',
        '1e keuze: ' + mooiDatum(gekozen[0]),
        '2e keuze: ' + mooiDatum(gekozen[1]),
        '_Ik hoor graag welke datum u kunt bevestigen._');
    }
    bericht.push('',
      '✉️ *Contact*',
      'E-mail: ' + veld('email').value.trim(),
      '',
      'Met vriendelijke groet');
    bericht = bericht.join('\n');
    var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(bericht);

    linkOpnieuw.href = url;
    stapInvullen.hidden = true;
    stapKlaar.hidden = false;

    var tab = window.open(url, '_blank');
    if (tab) { tab.opener = null; } else { window.location.href = url; }
  });
}());

/* ---------- Reviewband: pauzeknop ---------- */
(function () {
  'use strict';
  var sectie = document.querySelector('.review');
  var knop = sectie && sectie.querySelector('.review-pauze');
  if (!knop) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  knop.hidden = false;
  knop.addEventListener('click', function () {
    var gepauzeerd = sectie.classList.toggle('gepauzeerd');
    knop.classList.toggle('gepauzeerd', gepauzeerd);
    knop.setAttribute('aria-label', gepauzeerd ? 'Reviews laten bewegen' : 'Reviews stilzetten');
    knop.setAttribute('aria-pressed', gepauzeerd);
  });
}());

/* ---------- Contactformulier: versturen via FormSubmit ---------- */
(function () {
  'use strict';
  Array.prototype.forEach.call(document.querySelectorAll('form.formulier'), function (form) {
    if (!window.fetch || !window.FormData) return; // zonder fetch: gewoon posten
    var knop = form.querySelector('button[type="submit"]');
    var melding = form.querySelector('.formulier-melding');
    var knopTekst = knop.textContent;

    function toon(tekst, fout) {
      melding.innerHTML = tekst;
      melding.classList.toggle('fout', !!fout);
      melding.hidden = false;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = {};
      new FormData(form).forEach(function (waarde, naam) { data[naam] = waarde; });
      if (data._honey) return; // spam
      knop.disabled = true;
      knop.textContent = 'Bezig met versturen…';
      melding.hidden = true;

      fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) { return r.json(); }).then(function (antwoord) {
        if (String(antwoord.success) !== 'true') throw new Error(antwoord.message);
        form.reset();
        toon('Bedankt voor uw bericht! We nemen zo snel mogelijk contact met u op.');
      }).catch(function () {
        toon('Versturen is niet gelukt. Mail ons op <a href="mailto:contact@autoservicebarneveld.nl">contact@autoservicebarneveld.nl</a> of bel <a href="tel:+31342234003">0342-234003</a>.', true);
      }).then(function () {
        knop.disabled = false;
        knop.textContent = knopTekst;
      });
    });
  });
}());
