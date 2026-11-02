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

Alleen de Python-standaardbibliotheek is nodig. Kop, voet, afspraakvenster,
openingstijden, telefoon, KvK en btw staan bovenin `bron/bouw.py`. De
bedrijfsgegevens voor Google (schema.org JSON-LD) staan in `bron/bedrijf.json`.

## Opbouw

```
index.html                 Home (afspraakblok, diensten, over ons, vervoer, contact)
apk-keuring/ ...           Zes dienstpagina's
over-ons/, vervangend-vervoer/, contact/, privacy/
404.html                   Foutpagina (absolute paden, noindex)
css/style.css              Alle opmaak (kleuren bovenin :root)
js/site.js                 Mobiel menu en het afspraakvenster
fonts/                     Montserrat en Bebas Neue (zelf gehost)
img/                       Foto's (WebP), logo's (SVG), deelafbeelding.jpg
robots.txt, sitemap.xml, llms.txt, .well-known/security.txt
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
`GEBLOKKEERDE_DATA` (losse data).
Bij versturen opent WhatsApp (`wa.me/31342234003`) met een
ingevuld bericht dat de bezoeker zelf verstuurt; de site slaat niets op.
Zonder JavaScript gaan de knoppen naar de contactpagina.

## Beveiliging

Geen cookies, geen trackers, geen externe scripts of lettertypes. Een
Content-Security-Policy staat als meta-tag in elke pagina (GitHub Pages laat
geen eigen headers toe). Het contactformulier verstuurt via FormSubmit
(formsubmit.co) een e-mail naar contact@autoservicebarneveld.nl.
