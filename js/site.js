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
  /* ---------- Kenteken: merk, model en APK-datum uit de open data van de RDW ---------- */
  function netjes(tekst) {
    return tekst.toLowerCase().split(' ').map(function (w) {
      return w.length <= 3 && /[a-z]/.test(w) ? w.toUpperCase()
        : w.replace(/(^|-)([a-z])/g, function (m, a, b) { return a + b.toUpperCase(); });
    }).join(' ');
  }
  // Kenteken in de gangbare notatie met streepjes (bijv. GSF11S -> GSF-11-S)
  function kentekenNetjes(waarde) {
    var kaal = waarde.replace(/[\s-]/g, '').toUpperCase();
    var delen = kaal.match(/[A-Z]+|[0-9]+/g) || [kaal];
    if (delen.length === 2) {
      var lang = delen[0].length === 4 ? 0 : 1;
      delen.splice(lang, 1, delen[lang].slice(0, 2), delen[lang].slice(2));
    }
    return delen.length === 3 ? delen.join('-') : kaal;
  }
  function datumNL(jjjjmmdd) {
    var d = new Date(+jjjjmmdd.slice(0, 4), +jjjjmmdd.slice(4, 6) - 1, +jjjjmmdd.slice(6, 8));
    return { datum: d, tekst: d.toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' }) };
  }
  function zoekRdw(invoer) {
    var info = invoer.closest('.veld').querySelector('.rdw-info');
    invoer.rdw = null;
    clearTimeout(invoer.rdwWacht);
    if (!info) return;
    if (!kentekenOk(invoer.value) || !window.fetch) { info.hidden = true; return; }
    var kaal = invoer.value.replace(/[\s-]/g, '').toUpperCase();
    invoer.rdwWacht = setTimeout(function () {
      fetch('https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken=' + kaal +
        '&$select=merk,handelsbenaming,vervaldatum_apk')
        .then(function (r) { return r.json(); })
        .then(function (rijen) {
          if (invoer.value.replace(/[\s-]/g, '').toUpperCase() !== kaal) return;
          var auto = rijen && rijen[0];
          info.hidden = false;
          info.className = 'rdw-info';
          if (!auto) { info.textContent = 'Dit kenteken vinden we niet bij de RDW. Klopt het?'; info.classList.add('let-op'); return; }
          var merk = netjes(auto.merk || ''), type = netjes(auto.handelsbenaming || '');
          var naam = type.toLowerCase().indexOf(merk.toLowerCase()) === 0 ? type : (merk + ' ' + type).trim();
          var apk = auto.vervaldatum_apk ? datumNL(auto.vervaldatum_apk) : null;
          invoer.rdw = { auto: naam, apk: apk ? apk.tekst : '' };
          var regel = '<strong>' + naam + '</strong>';
          if (!apk) {
            regel += '<span>Geen APK-datum bekend bij de RDW</span>';
          } else {
            var dagen = (apk.datum - new Date()) / 864e5;
            if (dagen < 0) { info.classList.add('verlopen'); regel += '<span>APK verlopen op ' + apk.tekst + '</span>'; }
            else if (dagen < 61) { info.classList.add('let-op'); regel += '<span>APK verloopt op ' + apk.tekst + ', plan uw keuring</span>'; }
            else regel += '<span>APK geldig tot ' + apk.tekst + '</span>';
          }
          info.innerHTML = regel;
        })
        .catch(function () { info.hidden = true; });
    }, 350);
  }
  Array.prototype.forEach.call(document.querySelectorAll('input[name="kenteken"]'), function (invoer) {
    invoer.addEventListener('input', function () { controleerKenteken(invoer); zoekRdw(invoer); });
  });

  /* ---------- Kenteken onbekend: merk en model invullen ---------- */
  function kentekenOnbekend(form, onbekend, focus) {
    var blok = form.querySelector('.kenteken-blok'), mm = form.querySelector('.merk-model');
    if (!blok || !mm) return;
    var kenteken = form.elements.kenteken, merk = form.elements.merk, model = form.elements.model;
    var verplicht = form.hasAttribute('data-verplicht');
    blok.hidden = onbekend;
    mm.hidden = !onbekend;
    kenteken.required = verplicht && !onbekend;
    merk.required = model.required = verplicht && onbekend;
    if (onbekend) { kenteken.value = ''; kenteken.setCustomValidity(''); zoekRdw(kenteken); if (focus) merk.focus(); }
    else { merk.value = ''; model.value = ''; if (focus) kenteken.focus(); }
  }
  Array.prototype.forEach.call(document.querySelectorAll('form'), function (form) {
    var aan = form.querySelector('.kenteken-onbekend'), uit = form.querySelector('.kenteken-bekend');
    if (aan) aan.addEventListener('click', function () { kentekenOnbekend(form, true, true); });
    if (uit) uit.addEventListener('click', function () { kentekenOnbekend(form, false, true); });
  });

  /* ---------- Afspraakvenster ---------- */
  var venster = document.getElementById('afspraak-venster');
  if (!venster || typeof venster.showModal !== 'function') return;

  var formulier = venster.querySelector('form');
  var stapInvullen = venster.querySelector('.venster-invullen');
  var stapKlaar = venster.querySelector('.venster-klaar');
  var linkOpnieuw = venster.querySelector('.wa-opnieuw');
  var velden = ['kenteken', 'kilometerstand', 'email', 'postcode', 'huisnummer'];
  function veld(naam) { return formulier.elements[naam]; }

  function open(waarden) {
    stapInvullen.hidden = false;
    stapKlaar.hidden = true;
    if (waarden.onbekend) {
      kentekenOnbekend(formulier, true, false);
      veld('merk').value = waarden.merk || '';
      veld('model').value = waarden.model || '';
    } else if (waarden.kenteken) {
      kentekenOnbekend(formulier, false, false);
      veld('kenteken').value = waarden.kenteken;
      zoekRdw(veld('kenteken'));
    }
    var diensten = waarden.diensten || (waarden.dienst ? [waarden.dienst] : []);
    if (diensten.length) {
      Array.prototype.forEach.call(dienstVinkjes, function (v) { v.checked = diensten.indexOf(v.value) !== -1; });
    }
    controleerKenteken(veld('kenteken'));
    zetOmschrijving();
    venster.showModal();
    var leeg = velden.map(veld).filter(function (v) { return !v.value && !v.disabled && !v.closest('[hidden]'); })[0];
    (leeg || veld('kenteken')).focus();
  }

  // Stap 1 op de homepage: kenteken + dienst, daarna het venster
  var snel = document.getElementById('afspraak-snel');
  if (snel) {
    snel.addEventListener('submit', function (e) {
      e.preventDefault();
      open({
        onbekend: !snel.querySelector('.merk-model').hidden,
        kenteken: snel.elements.kenteken.value,
        merk: snel.elements.merk.value.trim(),
        model: snel.elements.model.value.trim(),
        diensten: Array.prototype.filter.call(snel.querySelectorAll('input[name="diensten"]'),
          function (v) { return v.checked; }).map(function (v) { return v.value; })
      });
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

  // Diensten: meerdere aanvinken; bij "Overig" een vak voor een korte omschrijving
  var dienstVinkjes = formulier.querySelectorAll('input[name="diensten"]');
  var omschrijving = venster.querySelector('.omschrijving');
  function gekozenDiensten() {
    return Array.prototype.filter.call(dienstVinkjes, function (v) { return v.checked; })
      .map(function (v) { return v.value; });
  }
  function controleerDiensten() {
    dienstVinkjes[0].setCustomValidity(gekozenDiensten().length ? '' : 'Kies minimaal één onderdeel.');
  }
  function zetOmschrijving() {
    var overig = gekozenDiensten().indexOf('Overig') !== -1;
    omschrijving.hidden = !overig;
    veld('omschrijving').required = overig;
    controleerDiensten();
  }
  Array.prototype.forEach.call(dienstVinkjes, function (v) {
    v.addEventListener('change', function () {
      zetOmschrijving();
      if (v.value === 'Overig' && v.checked) veld('omschrijving').focus();
    });
  });

  // Kilometerstand onbekend: veld uit, niet verplicht
  var kmKnop = venster.querySelector('.km-onbekend');
  kmKnop.addEventListener('click', function () {
    var onbekend = kmKnop.getAttribute('aria-pressed') !== 'true';
    var km = veld('kilometerstand');
    kmKnop.setAttribute('aria-pressed', onbekend);
    kmKnop.textContent = onbekend ? 'Toch invullen' : 'Ik weet de km-stand niet';
    km.disabled = onbekend;
    km.required = !onbekend;
    km.value = '';
    km.placeholder = onbekend ? 'Onbekend' : 'bijv. 85.000';
    if (!onbekend) km.focus();
  });

  // Kenteken onbekend: zie kentekenOnbekend() bovenin
  var kentekenBlok = venster.querySelector('.kenteken-blok');

  // Adres: postcode + huisnummer; straat en plaats via PDOK (Basisregistratie Adressen)
  var adresGevonden = venster.querySelector('.adres-gevonden');
  var adres = null, adresVraag = 0;
  function postcodeNet(v) { return v.replace(/\s+/g, '').toUpperCase(); }
  function controleerPostcode() {
    var pc = postcodeNet(veld('postcode').value);
    veld('postcode').setCustomValidity(pc && !/^[1-9][0-9]{3}[A-Z]{2}$/.test(pc) ? 'Vul een geldige postcode in, bijvoorbeeld 3771 LP.' : '');
    return pc;
  }
  function zoekAdres() {
    adres = null;
    var pc = controleerPostcode();
    if (/^[1-9][0-9]{3}[A-Z]{2}$/.test(pc)) veld('postcode').value = pc.slice(0, 4) + ' ' + pc.slice(4);
    var nr = veld('huisnummer').value.trim();
    var cijfers = (nr.match(/^\d+/) || [])[0];
    if (!/^[1-9][0-9]{3}[A-Z]{2}$/.test(pc) || !cijfers || !window.fetch) { adresGevonden.hidden = true; return; }
    var vraag = ++adresVraag;
    fetch('https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?q=*&fq=type:adres&fq=postcode:' + pc +
      '&fq=huisnummer:' + cijfers + '&fl=straatnaam,woonplaatsnaam&rows=1')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (vraag !== adresVraag) return;
        var d = data.response && data.response.docs[0];
        adresGevonden.hidden = false;
        if (d) {
          adres = d.straatnaam + ' ' + nr + ', ' + pc.slice(0, 4) + ' ' + pc.slice(4) + ' ' + d.woonplaatsnaam;
          adresGevonden.className = 'adres-gevonden';
          adresGevonden.textContent = '✓ ' + adres;
        } else {
          adresGevonden.className = 'adres-gevonden fout';
          adresGevonden.textContent = 'Dit adres vinden we niet. Controleer uw postcode en huisnummer.';
        }
      })
      .catch(function () { if (vraag === adresVraag) adresGevonden.hidden = true; });
  }
  veld('postcode').addEventListener('change', zoekAdres);
  veld('huisnummer').addEventListener('change', zoekAdres);
  veld('postcode').addEventListener('input', function () { adresGevonden.hidden = true; adres = null; });
  veld('huisnummer').addEventListener('input', function () { adresGevonden.hidden = true; adres = null; });

  formulier.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!kentekenBlok.hidden) controleerKenteken(veld('kenteken'));
    controleerDiensten();
    controleerPostcode();
    if (!formulier.reportValidity() || !datumsOk()) return;

    // WhatsApp-bericht: kopjes met ▸ en *vet*, regels met •.
    // Geen emoji: de doorstuurpagina van WhatsApp maakt die kapot (�).
    function kop(t) { return '▸ *' + t + '*'; }
    function regel(t) { return '• ' + t; }
    var werk = gekozenDiensten().map(regel);
    if (!omschrijving.hidden && veld('omschrijving').value.trim()) {
      werk.push(regel('Omschrijving: ' + veld('omschrijving').value.trim().replace(/\s+/g, ' ')));
    }
    var bericht = [
      'Hallo Autoservice Barneveld,',
      '',
      'Graag maak ik een afspraak. Hieronder mijn gegevens.',
      '',
      kop('Werkzaamheden')
    ].concat(werk, [
      '',
      kop('Voertuig'),
      kentekenBlok.hidden
        ? regel('Kenteken: onbekend') + '\n' + regel('Merk en model: ' + veld('merk').value.trim() + ' ' + veld('model').value.trim())
        : [regel('Kenteken: ' + kentekenNetjes(veld('kenteken').value))].concat(
            veld('kenteken').rdw ? [regel('Auto: ' + veld('kenteken').rdw.auto)].concat(
              veld('kenteken').rdw.apk ? [regel('APK geldig tot: ' + veld('kenteken').rdw.apk)] : []) : []).join('\n'),
      regel('Kilometerstand: ' + (veld('kilometerstand').value ? 'ca. ' + veld('kilometerstand').value + ' km' : 'weet ik niet')),
      '',
      kop('Vervangend vervoer'),
      regel(veld('vervoer').checked ? keuzeVervoer() : 'Niet nodig')
    ]);
    if (!datumKeuze.hidden) {
      bericht.push('',
        kop('Voorkeursdata'),
        regel('1e keuze: ' + mooiDatum(gekozen[0])),
        regel('2e keuze: ' + mooiDatum(gekozen[1])),
        '_Ik hoor graag welke datum u kunt bevestigen._');
    }
    bericht.push('',
      kop('Contact'),
      regel('Adres: ' + (adres || (postcodeNet(veld('postcode').value).replace(/^(\d{4})/, '$1 ') + ', huisnummer ' + veld('huisnummer').value.trim()))),
      regel('E-mail: ' + veld('email').value.trim()),
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
