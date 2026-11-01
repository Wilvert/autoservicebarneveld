# Autoservice Barneveld

Statische website van [autoservicebarneveld.nl](https://autoservicebarneveld.nl).
Overgenomen van de oude IONOS/Strato-site (november 2026): dezelfde teksten,
opmaak, kleuren en foto's, maar als gewone HTML en één CSS-bestand.

## Opbouw

```
index.html                 Home
apk-keuring/               Dienstpagina's (elk een index.html)
onderhoud-reparatie/
diagnose/
bandenservice/
airco-service/
elektrische-auto/
over-ons/index.html        Over Ons
vervangend-vervoer/        Vervangend Vervoer
contact/index.html         Contact
privacy/index.html         Privacyverklaring
404.html                   Foutpagina (absolute paden, noindex)
robots.txt, sitemap.xml    Voor zoekmachines; nieuwe pagina's ook in sitemap.xml zetten
css/style.css              Alle opmaak (kleuren staan bovenaan in :root)
img/                       Foto's, logo, favicon
fonts/                     Nunito, Nunito Sans, Merriweather (zelf gehost)
```

Geen JavaScript, geen cookies, geen externe lettertypes. De kop en voet
staan in elke pagina; pas ze bij een wijziging in alle pagina's aan. Dat geldt
ook voor het JSON-LD-blok (`AutoRepair`) in de `<head>`: bedrijfsgegevens
zoals adres, telefoon en (later) openingstijden staan daar.

## Bekijken

Lokaal: `python3 -m http.server` in deze map en open http://localhost:8000.

## Open punten

- Het contactformulier opent nu het mailprogramma van de bezoeker
  (`mailto:`). Vervangen door een formulierdienst als dat gewenst is.
- De kaart op de contactpagina komt van OpenStreetMap (geen cookies).
- Openingstijden staan op de contactpagina, in de voet en in het JSON-LD-blok
  (`openingHoursSpecification`, alleen ma–vr; zaterdag is op afspraak).
- Foto's zijn WebP; `img/deelafbeelding.jpg` (1200x630) is de preview bij
  delen via WhatsApp/Facebook.
