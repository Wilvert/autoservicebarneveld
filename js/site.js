/* Autoservice Barneveld: menu en afspraakvenster.
   Het venster verstuurt niets zelf: het opent WhatsApp met een ingevuld bericht,
   dat de bezoeker daar zelf verstuurt. Zonder JavaScript gaan de knoppen naar
   de contactpagina. */
(function () {
  'use strict';

  var WHATSAPP = '31342234003';
  var MAIL = 'contact@autoservicebarneveld.nl';

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
  Array.prototype.forEach.call(document.querySelectorAll('input[name="kenteken"]:not([data-geen-rdw])'), function (invoer) {
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

  /* ---------- APK-check: openbare RDW-gegevens bij een kenteken ---------- */
  (function () {
    var form = document.getElementById('apk-check');
    if (!form || !window.fetch) return;
    var invoer = form.elements.kenteken;
    var melding = form.querySelector('.apk-check-melding');
    var uitslag = document.getElementById('apk-uitslag');
    var status = uitslag.querySelector('.apk-status');
    var agendaKnop = uitslag.querySelector('.apk-agenda');
    var RDW = 'https://opendata.rdw.nl/resource/';
    var KLEUREN = { ZWART: '#1f2125', WIT: '#f3f4f5', GRIJS: '#8b9097', BLAUW: '#2b5ca8', ROOD: '#c3282e', GROEN: '#2f7d4f',
      GEEL: '#f0c12c', ORANJE: '#e4782c', BRUIN: '#6d4b30', BEIGE: '#d9c8a4', CREME: '#efe6cf', PAARS: '#6b3e90', ROSE: '#e8a4b7' };
    var huidig = null;

    function dag(d) { var x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
    function lang(d) { return d.toLocaleDateString('nl-NL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); }
    function kort(d) { return d.toLocaleDateString('nl-NL', { day: 'numeric', month: 'long', year: 'numeric' }); }
    function rdwDatum(v) { return v ? new Date(+v.slice(0, 4), +v.slice(4, 6) - 1, +v.slice(6, 8)) : null; }
    // Twee maanden eerder, op dezelfde dag (of de laatste dag van die maand)
    function tweeMaandenEerder(d) {
      var x = new Date(d.getFullYear(), d.getMonth() - 2, 1);
      var laatste = new Date(x.getFullYear(), x.getMonth() + 1, 0).getDate();
      x.setDate(Math.min(d.getDate(), laatste));
      return x;
    }
    function duur(dagen) {
      if (dagen === 1) return '1 dag';
      if (dagen < 62) return dagen + ' dagen';
      var m = Math.floor(dagen / 30.44);
      return 'ruim ' + (m >= 24 ? Math.floor(m / 12) + ' jaar' : m + ' maanden');
    }
    function getal(n) { return Number(n).toLocaleString('nl-NL'); }
    function tekst(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

    function plaatje(kleur, bestel) {
      var vul = KLEUREN[(kleur || '').toUpperCase()] || '#9aa3ad';
      var rand = vul === '#f3f4f5' || vul === '#efe6cf' ? '#9aa3ad' : 'rgba(0,0,0,.25)';
      var lijf = bestel
        ? 'M14 74V40q0-8 8-10l40-6h96q10 0 16 7l26 24 20 4q10 2 10 12v3z'
        : 'M16 74V60q2-8 12-10l42-5 26-19q5-4 12-4h52q10 0 17 6l23 18 24 5q10 2 10 12v11z';
      var ramen = bestel
        ? '<path d="M150 31h20q5 0 9 4l20 18h-49z" fill="#cfe2f2" stroke="' + rand + '"/>'
        : '<path d="M104 31h30v19H80z" fill="#cfe2f2" stroke="' + rand + '"/><path d="M140 31h22q6 0 10 4l16 15h-48z" fill="#cfe2f2" stroke="' + rand + '"/>';
      function wiel(x) { return '<circle cx="' + x + '" cy="76" r="17" fill="#26282c"/><circle cx="' + x + '" cy="76" r="7" fill="#c7cbd1"/>'; }
      return '<svg viewBox="0 0 256 100" role="img" aria-label="Illustratie van de auto">' +
        '<ellipse cx="128" cy="93" rx="112" ry="5" fill="rgba(0,0,0,.12)"/>' +
        '<path d="' + lijf + '" fill="' + vul + '" stroke="' + rand + '" stroke-width="1.5"/>' + ramen +
        wiel(bestel ? 62 : 64) + wiel(bestel ? 196 : 194) + '</svg>';
    }

    function toonStatus(apk, kenteken) {
      var vandaag = dag(new Date());
      status.className = 'apk-status';
      var label = uitslag.querySelector('.apk-status-label');
      var kop = uitslag.querySelector('.apk-status-kop');
      var uitleg = uitslag.querySelector('.apk-status-uitleg');
      huidig = null;
      agendaKnop.hidden = true;
      if (!apk) {
        status.classList.add('onbekend');
        label.textContent = 'Geen APK-datum';
        kop.textContent = 'De RDW heeft geen APK-vervaldatum voor dit voertuig.';
        uitleg.textContent = 'Mogelijk is het voertuig niet APK-plichtig. Twijfelt u? Bel of app ons gerust.';
        return;
      }
      var dagen = Math.round((apk - vandaag) / 864e5);
      var vanaf = tweeMaandenEerder(apk);
      if (dagen < 0) {
        status.classList.add('verlopen');
        label.textContent = 'APK verlopen';
        kop.textContent = 'Uw APK is verlopen op ' + kort(apk) + '.';
        uitleg.textContent = 'Met een verlopen APK mag u niet de weg op. Plan zo snel mogelijk uw keuring, of bel ons voor een snelle afspraak.';
      } else if (vandaag >= vanaf) {
        status.classList.add('nu');
        label.textContent = 'U kunt nu keuren';
        kop.textContent = 'Uw APK verloopt over ' + duur(dagen) + ', op ' + lang(apk) + '.';
        uitleg.textContent = 'U kunt nu al keuren met behoud van uw vervaldatum: de nieuwe datum wordt gerekend vanaf ' + kort(apk) + '.';
      } else {
        status.classList.add('geldig');
        label.textContent = 'APK geldig';
        kop.textContent = 'Uw APK is nog ' + duur(dagen) + ' geldig, tot ' + lang(apk) + '.';
        uitleg.textContent = 'Vanaf ' + lang(vanaf) + ' kunt u keuren met behoud van uw vervaldatum.';
        huidig = { vanaf: vanaf, apk: apk, kenteken: kenteken };
        agendaKnop.hidden = false;
      }
    }

    function toonAuto(a, brandstof) {
      var merk = netjes(a.merk || ''), type = netjes(a.handelsbenaming || '');
      var naam = type.toLowerCase().indexOf(merk.toLowerCase()) === 0 ? type : (merk + ' ' + type).trim();
      uitslag.querySelector('.apk-naam').textContent = naam;
      var kleur = (a.eerste_kleur || '').toLowerCase();
      var bestel = /bedrijfsauto/i.test(a.voertuigsoort || '');
      uitslag.querySelector('.apk-svg').innerHTML = plaatje(a.eerste_kleur, bestel);
      uitslag.querySelector('.apk-plaatje figcaption').textContent =
        'Illustratie' + (kleur && kleur !== 'n.v.t.' && kleur !== 'diversen' ? ' in de kleur van uw auto (' + kleur + ')' : '');
      var eerste = rdwDatum(a.datum_eerste_toelating), nl = rdwDatum(a.datum_eerste_tenaamstelling_in_nederland);
      var rijen = [];
      function rij(k, v) { if (v) rijen.push('<dt>' + k + '</dt><dd>' + v + '</dd>'); }
      rij('Kenteken', tekst(kentekenNetjes(a.kenteken)));
      rij('Soort', tekst([a.voertuigsoort, a.inrichting && a.inrichting !== 'Niet geregistreerd' ? a.inrichting : ''].filter(Boolean).join(', ')));
      rij('Kleur', tekst(kleur && kleur !== 'n.v.t.' ? kleur.charAt(0).toUpperCase() + kleur.slice(1) : ''));
      rij('Brandstof', tekst(brandstof.soort.charAt(0) + brandstof.soort.slice(1).toLowerCase()));
      rij('Vermogen', brandstof.kw ? getal(Math.round(brandstof.kw)) + ' kW (' + getal(Math.round(brandstof.kw * 1.36)) + ' pk)' : '');
      rij('Eerste toelating', eerste ? kort(eerste) : '');
      if (eerste && nl && Math.abs(nl - eerste) > 864e5 * 30) rij('In Nederland sinds', kort(nl) + ' (import)');
      rij('Cilinderinhoud', +a.cilinderinhoud ? getal(a.cilinderinhoud) + ' cc' : '');
      rij('Zitplaatsen', tekst(a.aantal_zitplaatsen || ''));
      rij('Gewicht rijklaar', +a.massa_rijklaar ? getal(a.massa_rijklaar) + ' kg' : '');
      rij('Trekgewicht', +a.maximum_trekken_massa_geremd ? getal(a.maximum_trekken_massa_geremd) + ' kg geremd' +
        (+a.maximum_massa_trekken_ongeremd ? ', ' + getal(a.maximum_massa_trekken_ongeremd) + ' kg ongeremd' : '') : '');
      rij('Energielabel', tekst(a.zuinigheidsclassificatie || ''));
      rij('Tellerstand', tekst(a.tellerstandoordeel || ''));
      rij('Verzekerd (WAM)', tekst(a.wam_verzekerd || ''));
      if (a.openstaande_terugroepactie_indicator === 'Ja') {
        rij('Terugroepactie', '<span class="apk-let-op">Ja, er staat een terugroepactie open.</span> Neem contact op met de dealer of vraag het ons.');
      } else rij('Terugroepactie', a.openstaande_terugroepactie_indicator === 'Nee' ? 'Geen openstaande' : '');
      uitslag.querySelector('.apk-gegevens dl').innerHTML = rijen.join('');
    }

    function check(waarde, schuif) {
      melding.hidden = true;
      if (!kentekenOk(waarde)) {
        melding.textContent = 'Vul een Nederlands kenteken in, bijvoorbeeld AB-123-C.';
        melding.hidden = false; uitslag.hidden = true; invoer.focus(); return;
      }
      var kaal = waarde.replace(/[\s-]/g, '').toUpperCase();
      var knop = form.querySelector('button[type="submit"]');
      knop.disabled = true;
      Promise.all([
        fetch(RDW + 'm9d7-ebf2.json?kenteken=' + kaal).then(function (r) { return r.json(); }),
        fetch(RDW + '8ys7-d773.json?kenteken=' + kaal).then(function (r) { return r.json(); }).catch(function () { return []; })
      ]).then(function (res) {
        var a = res[0] && res[0][0];
        if (!a) {
          melding.textContent = 'Dit kenteken vinden we niet bij de RDW. Controleer of het goed is ingevuld.';
          melding.hidden = false; uitslag.hidden = true; return;
        }
        var soorten = [], kw = 0;
        (res[1] || []).forEach(function (b) {
          if (b.brandstof_omschrijving && soorten.indexOf(b.brandstof_omschrijving) === -1) soorten.push(b.brandstof_omschrijving);
          if (!kw && +b.nettomaximumvermogen) kw = +b.nettomaximumvermogen;
        });
        toonStatus(rdwDatum(a.vervaldatum_apk), kentekenNetjes(kaal));
        toonAuto(a, { soort: soorten.join(' en '), kw: kw });
        uitslag.hidden = false;
        try { history.replaceState(null, '', '?kenteken=' + kaal); } catch (e) { /* niets */ }
        if (schuif) uitslag.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }).catch(function () {
        melding.textContent = 'De gegevens van de RDW zijn nu niet bereikbaar. Probeer het later nog eens of bel ons.';
        melding.hidden = false;
      }).then(function () { knop.disabled = false; });
    }

    invoer.addEventListener('input', function () { controleerKenteken(invoer); melding.hidden = true; });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      invoer.value = kentekenNetjes(invoer.value);
      check(invoer.value, true);
    });

    // Herinnering: agenda-afspraak (.ics) op de dag dat keuren met behoud van datum kan
    agendaKnop.addEventListener('click', function () {
      if (!huidig) return;
      function ics(d) { return d.getFullYear() + ('0' + (d.getMonth() + 1)).slice(-2) + ('0' + d.getDate()).slice(-2); }
      var eind = new Date(huidig.vanaf); eind.setDate(eind.getDate() + 1);
      var regels = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Autoservice Barneveld//APK-check//NL', 'BEGIN:VEVENT',
        'UID:apk-' + huidig.kenteken + '-' + ics(huidig.vanaf) + '@autoservicebarneveld.nl',
        'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z',
        'DTSTART;VALUE=DATE:' + ics(huidig.vanaf), 'DTEND;VALUE=DATE:' + ics(eind),
        'SUMMARY:APK ' + huidig.kenteken + ' plannen',
        'DESCRIPTION:Vanaf vandaag kunt u keuren met behoud van uw vervaldatum (' + kort(huidig.apk) + '). Plan uw APK via www.autoservicebarneveld.nl of bel 0342-234003.'.replace(/([,;])/g, '\\$1'),
        'END:VEVENT', 'END:VCALENDAR'];
      var url = URL.createObjectURL(new Blob([regels.join('\r\n')], { type: 'text/calendar' }));
      var link = document.createElement('a');
      link.href = url; link.download = 'APK-' + huidig.kenteken + '.ics';
      document.body.appendChild(link); link.click(); link.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });

    var gevraagd = new URLSearchParams(location.search).get('kenteken');
    if (gevraagd) { invoer.value = kentekenNetjes(gevraagd); check(invoer.value, false); }
  })();

  /* ---------- Afspraakvenster ---------- */
  var venster = document.getElementById('afspraak-venster');
  if (!venster || typeof venster.showModal !== 'function') return;

  var formulier = venster.querySelector('form');
  var stapInvullen = venster.querySelector('.venster-invullen');
  var stapKlaar = venster.querySelector('.venster-klaar:not(.venster-klaar-mail)');
  var stapKlaarMail = venster.querySelector('.venster-klaar-mail');
  var mailMelding = venster.querySelector('.mail-melding');
  var linkOpnieuw = venster.querySelector('.wa-opnieuw');
  var velden = ['kenteken', 'kilometerstand', 'email', 'postcode', 'huisnummer'];
  function veld(naam) { return formulier.elements[naam]; }

  function open(waarden) {
    stapInvullen.hidden = false;
    stapKlaar.hidden = true;
    stapKlaarMail.hidden = true;
    mailMelding.hidden = true;
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

  // Link met #plan-afspraak (bijv. vanuit Google) opent meteen de planner
  if (location.hash === '#plan-afspraak') {
    window.addEventListener('load', function () { open({}); });
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
      var van = knop.getAttribute('data-kenteken-van');
      var bron = van && document.querySelector(van);
      open({ dienst: knop.getAttribute('data-dienst') || '', kenteken: bron && kentekenOk(bron.value) ? kentekenNetjes(bron.value) : '' });
    });
  });

  venster.querySelector('.sluit').addEventListener('click', function () { venster.close(); });
  venster.addEventListener('click', function (e) { if (e.target === venster) venster.close(); });

  // Kilometerstand: alleen cijfers, met punten voor de leesbaarheid
  veld('kilometerstand').addEventListener('input', function () {
    var cijfers = this.value.replace(/\D/g, '').slice(0, 7);
    this.value = cijfers ? Number(cijfers).toLocaleString('nl-NL') : '';
  });

  // Overleggrens: alleen cijfers
  veld('overleggrens').addEventListener('input', function () {
    var cijfers = this.value.replace(/\D/g, '').slice(0, 5);
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
     - losse data in GEBLOKKEERDE_DATA ('jjjj-mm-dd')
     - officiële feestdagen (elk jaar automatisch, zie feestdagen()) */
  var GEBLOKKEERD = {
    '2026-11': [2, 3],   // november: dinsdag en woensdag
    '2026-12': [2]       // december: dinsdag
  };
  var GEBLOKKEERDE_DATA = [
    // Kerstvakantie: dicht van 25 december 2026 t/m 3 januari 2027
    '2026-12-28', '2026-12-29', '2026-12-30', '2026-12-31'
  ];
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
  // Officiële vrije dagen in Nederland, per jaar berekend.
  // Bevrijdingsdag alleen in lustrumjaren (2030, 2035 ...); Goede Vrijdag niet.
  var feestCache = {};
  function feestdagen(j) {
    if (feestCache[j]) return feestCache[j];
    // Paasdatum (Meeus/Jones/Butcher)
    var a = j % 19, b = Math.floor(j / 100), c = j % 100, d = Math.floor(b / 4), e = b % 4,
        f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
        i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7,
        m = Math.floor((a + 11 * h + 22 * l) / 451), mnd = Math.floor((h + l - 7 * m + 114) / 31),
        dg = ((h + l - 7 * m + 114) % 31) + 1;
    function naPasen(n) { return iso(new Date(j, mnd - 1, dg + n)); }
    var koning = new Date(j, 3, 27);
    if (koning.getDay() === 0) koning = new Date(j, 3, 26);
    var lijst = [
      j + '-01-01',      // Nieuwjaarsdag
      naPasen(1),        // Tweede paasdag
      iso(koning),       // Koningsdag
      naPasen(39),       // Hemelvaartsdag
      naPasen(50),       // Tweede pinksterdag
      j + '-12-25',      // Eerste kerstdag
      j + '-12-26'       // Tweede kerstdag
    ];
    if (j % 5 === 0) lijst.push(j + '-05-05'); // Bevrijdingsdag (lustrumjaar)
    return (feestCache[j] = lijst);
  }

  function beschikbaar(d) {
    var dag = d.getDay();
    if (dag === 0 || dag === 6) return false;
    if (d < eersteDag() || d > laatsteDag()) return false;
    var maand = GEBLOKKEERD[d.getFullYear() + '-' + twee(d.getMonth() + 1)];
    if (maand && maand.indexOf(dag) !== -1) return false;
    if (feestdagen(d.getFullYear()).indexOf(iso(d)) !== -1) return false;
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

  // Diensten: meerdere aanvinken. Het opmerkingenveld staat er altijd (optioneel);
  // bij Reparatie of Overig wordt het een verplichte korte omschrijving.
  var dienstVinkjes = formulier.querySelectorAll('input[name="diensten"]');
  var omschrijving = venster.querySelector('.omschrijving');
  var omschrijvingLabel = omschrijving.querySelector('.omschrijving-label');
  var omschrijvingOptioneel = omschrijving.querySelector('.label-optioneel');
  function gekozenDiensten() {
    return Array.prototype.filter.call(dienstVinkjes, function (v) { return v.checked; })
      .map(function (v) { return v.value; });
  }
  function controleerDiensten() {
    dienstVinkjes[0].setCustomValidity(gekozenDiensten().length ? '' : 'Kies minimaal één optie.');
  }
  function omschrijvingNodig() {
    var g = gekozenDiensten();
    return g.indexOf('Reparatie') !== -1 || g.indexOf('Overig') !== -1;
  }
  function zetOmschrijving() {
    var nodig = omschrijvingNodig();
    omschrijvingLabel.textContent = nodig ? 'Korte omschrijving' : 'Opmerking';
    omschrijvingOptioneel.textContent = nodig ? 'wat is er aan de hand?' : 'optioneel';
    veld('omschrijving').placeholder = nodig
      ? 'Bijv. piepende remmen, een lampje op het dashboard of een vreemd geluid'
      : 'Bijv. wanneer u de auto kunt brengen of iets wat we moeten weten';
    veld('omschrijving').required = nodig;
    controleerDiensten();
  }
  Array.prototype.forEach.call(dienstVinkjes, function (v) {
    v.addEventListener('change', function () {
      zetOmschrijving();
      if ((v.value === 'Reparatie' || v.value === 'Overig') && v.checked) veld('omschrijving').focus();
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

  // Welke knop is gebruikt: WhatsApp (standaard) of e-mail
  var kanaal = 'whatsapp';
  Array.prototype.forEach.call(formulier.querySelectorAll('[data-kanaal]'), function (knop) {
    knop.addEventListener('click', function () { kanaal = knop.getAttribute('data-kanaal'); });
  });

  // De aanvraag als blokken met kopjes; daaruit maken we het WhatsApp-bericht of de e-mail
  function aanvraag() {
    var werk = gekozenDiensten();
    if (veld('omschrijving').value.trim()) {
      werk.push((omschrijvingNodig() ? 'Omschrijving: ' : 'Opmerking: ') + veld('omschrijving').value.trim().replace(/\s+/g, ' '));
    }
    if (veld('overleggrens').value) {
      werk.push('Eerst overleggen als het meer kost dan: € ' + veld('overleggrens').value);
    }
    var voertuig = kentekenBlok.hidden
      ? ['Kenteken: onbekend', 'Merk en model: ' + veld('merk').value.trim() + ' ' + veld('model').value.trim()]
      : ['Kenteken: ' + kentekenNetjes(veld('kenteken').value)];
    var rdw = !kentekenBlok.hidden && veld('kenteken').rdw;
    if (rdw) {
      voertuig.push('Auto: ' + rdw.auto);
      if (rdw.apk) voertuig.push('APK geldig tot: ' + rdw.apk);
    }
    voertuig.push('Kilometerstand: ' + (veld('kilometerstand').value ? 'ca. ' + veld('kilometerstand').value + ' km' : 'weet ik niet'));
    var blokken = [
      { kop: 'Werkzaamheden', regels: werk },
      { kop: 'Voertuig', regels: voertuig },
      { kop: 'Vervangend vervoer', regels: [veld('vervoer').checked ? keuzeVervoer() : 'Niet nodig'] }
    ];
    if (!datumKeuze.hidden) {
      blokken.push({ kop: 'Voorkeursdata', regels: ['1e keuze: ' + mooiDatum(gekozen[0]), '2e keuze: ' + mooiDatum(gekozen[1])],
        noot: 'Ik hoor graag welke datum u kunt bevestigen.' });
    }
    blokken.push({ kop: 'Contact', regels: [
      'Adres: ' + (adres || (postcodeNet(veld('postcode').value).replace(/^(\d{4})/, '$1 ') + ', huisnummer ' + veld('huisnummer').value.trim())),
      'E-mail: ' + veld('email').value.trim()
    ] });
    return blokken;
  }

  // WhatsApp-bericht: kopjes met ▸ en *vet*, regels met •.
  // Geen emoji: de doorstuurpagina van WhatsApp maakt die kapot (�).
  function whatsappTekst(blokken) {
    var r = ['Hallo Autoservice Barneveld,', '', 'Graag maak ik een afspraak. Hieronder mijn gegevens.'];
    blokken.forEach(function (b) {
      r.push('', '▸ *' + b.kop + '*');
      b.regels.forEach(function (t) { r.push('• ' + t); });
      if (b.noot) r.push('_' + b.noot + '_');
    });
    r.push('', 'Met vriendelijke groet');
    return r.join('\n');
  }

  function verstuurPerMail(blokken) {
    var knop = formulier.querySelector('[data-kanaal="mail"]');
    var data = {
      _subject: 'Afspraakaanvraag via de website' +
        (kentekenBlok.hidden ? '' : ' - ' + kentekenNetjes(veld('kenteken').value)),
      _template: 'table',
      _captcha: 'false',
      email: veld('email').value.trim()
    };
    blokken.forEach(function (b) { data[b.kop] = b.regels.join(' | ') + (b.noot ? ' (' + b.noot + ')' : ''); });
    knop.disabled = true;
    var label = knop.querySelector('span');
    label.textContent = 'Bezig met versturen…';
    mailMelding.hidden = true;
    fetch('https://formsubmit.co/ajax/' + MAIL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (antwoord) {
      if (String(antwoord.success) !== 'true') throw new Error(antwoord.message);
      stapInvullen.hidden = true;
      stapKlaarMail.hidden = false;
    }).catch(function () {
      mailMelding.innerHTML = 'Versturen per e-mail is niet gelukt. Probeer WhatsApp of bel <a href="tel:+31342234003">0342-234003</a>.';
      mailMelding.hidden = false;
    }).then(function () {
      knop.disabled = false;
      label.textContent = 'Verstuur per e-mail';
    });
  }

  formulier.addEventListener('submit', function (e) {
    e.preventDefault();
    var gekozenKanaal = (e.submitter && e.submitter.getAttribute('data-kanaal')) || kanaal;
    kanaal = 'whatsapp';
    if (!kentekenBlok.hidden) controleerKenteken(veld('kenteken'));
    controleerDiensten();
    controleerPostcode();
    if (!formulier.reportValidity() || !datumsOk()) return;

    var blokken = aanvraag();
    if (gekozenKanaal === 'mail') { verstuurPerMail(blokken); return; }

    var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(whatsappTekst(blokken));
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
      melding.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = {};
      new FormData(form).forEach(function (waarde, naam) { data[naam] = waarde; });
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
