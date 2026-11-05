# Autoservice Barneveld

Statische website van [autoservicebarneveld.nl](https://www.autoservicebarneveld.nl),
gehost op GitHub Pages. Ontwerp: mock-up 06 "Afspraak eerst" (november 2026),
kleuren en lettertypes uit het merkboek.

## Pagina's aanpassen

De HTML wordt gemaakt door een klein bouwscript. **Pas de teksten aan in
`bron/bouw.py`, niet in de HTML-bestanden**, en bouw daarna opnieuw:

```
python bron/bouw.py
```

Nodig: Python 3 met Pillow (`pip install pillow`), voor de fotoformaten. Kop, voet, afspraakvenster,
openingstijden, telefoon, KvK en btw staan bovenin `bron/bouw.py`. De
bedrijfsgegevens voor Google (schema.org JSON-LD) staan in `bron/bedrijf.json`.

## Opbouw

```
index.html                 Home (afspraakblok, diensten, waarom, over ons, vervoer, zelf checken, reviews, contact)
merken/, werkgebied/, veelgestelde-vragen/   Vindbaarheid: merken, plaatsen, FAQ (met FAQ-schema)
apk-keuring/ ...           Zes dienstpagina's (met eigen vragen + Service/FAQ-schema)
aankoopkeuring/            Dienst aankoopkeuring (met voorbehoud in kleine letters)
kentekencheck/             Eén kentekencheck op de open data van de RDW: APK, overzicht, gegevens, APK-historie
apk-check/, occasion-check/, terugroepactie-check/, trekgewicht-check/
                           Oude adressen; sturen door naar kentekencheck/ (doorsturen() in bouw.py)
checklist-tweedehands-auto/  Checklist occasion kopen; tekst in CHECKLIST e.a. in bouw.py
downloads/checklist-tweedehands-auto.pdf
                           Dezelfde checklist als PDF (stijl briefpapier): na bouw.py draaien `python3 bron/maak_pdf.py`
downloads/voorbereiding-aankoopkeuring.pdf
                           Korte lijst voor wie een aankoopkeuring plant (VOORBEREIDING in bouw.py; planner)
winterbanden/, bandencheck/, onderhoudswijzer/, dashboardlampjes/
                           Overige checks en uitleg (weer via Open-Meteo; bandencheck = uitleg met illustraties)
hulp/                      "Wat is er met mijn auto?" + acht klachtpagina's (KLACHTEN in bouw.py)
handig/                    Overzicht van alle checks (HANDIG in bouw.py; vult ook het menu "Zelf checken")
over-ons/, vervangend-vervoer/, contact/, privacy/
404.html                   Foutpagina (absolute paden, noindex)
css/style.css              Alle opmaak (kleuren bovenin :root)
js/site.js                 Mobiel menu en het afspraakvenster
fonts/                     Montserrat en Bebas Neue (zelf gehost)
img/                       Foto's (WebP, met -480/-960/-1440 varianten voor srcset), logo's (SVG),
                           deelafbeelding.jpg en og-*.jpg (deelafbeelding per pagina)
robots.txt, sitemap.xml, llms.txt, .well-known/security.txt
<sleutel>.txt              IndexNow-sleutel; .github/workflows/indexnow.yml meldt na elke push alle pagina's aan
mockups/                   De tien ontwerpvoorstellen (noindex)
```

## Afspraak plannen

"Plan afspraak" opent een venster met kenteken (of merk en model), een of meer
diensten, kilometerstand, adres (postcode + huisnummer; straat en plaats via
PDOK),
e-mailadres en eventueel vervangend vervoer (Renault 5, VW Caddy of leenfiets).
Optioneel kiest de bezoeker twee voorkeursdata in een kalender (minimaal twee
weken vooruit, geen weekend). Dagen blokkeren doe je bovenin het
voorkeursdatum-blok in `js/site.js`: `GEBLOKKEERD` (weekdagen per maand) en
`GEBLOKKEERDE_DATA` (losse data). Officiële feestdagen gaan automatisch dicht
(`feestdagen()`).
Bij versturen opent WhatsApp (`wa.me/31342234003`) met een
ingevuld bericht dat de bezoeker zelf verstuurt; de site slaat niets op.
Zonder JavaScript gaan de knoppen naar de contactpagina.

## Beveiliging

Geen cookies, geen trackers, geen externe scripts of lettertypes. Een
Content-Security-Policy staat als meta-tag in elke pagina (GitHub Pages laat
geen eigen headers toe). Het contactformulier verstuurt via FormSubmit
(formsubmit.co) een e-mail naar contact@autoservicebarneveld.nl.

CSS en JS worden gelinkt met `?v=<hash>`, zodat bezoekers na een wijziging
meteen de nieuwe versie krijgen. Daarom altijd opnieuw bouwen na het aanpassen
van `css/style.css` of `js/site.js`.

## Nieuwe foto toevoegen

Zet de foto als WebP in `img/` en maak de kleinere varianten en de
deelafbeelding, bijvoorbeeld met Pillow: `naam-480.webp`, `naam-960.webp`,
`naam-1440.webp` (alleen kleiner dan het origineel) en `og-naam.jpg`
(1200 x 630). Het bouwscript gebruikt ze automatisch als ze bestaan.
