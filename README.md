# Autoservice Barneveld

Statische website van [autoservicebarneveld.nl](https://autoservicebarneveld.nl).
Overgenomen van de oude IONOS/Strato-site (november 2026): dezelfde teksten,
opmaak, kleuren en foto's, maar als gewone HTML en één CSS-bestand.

## Opbouw

```
index.html                 Home
over-ons/index.html        Over Ons
vervangend-vervoer/        Vervangend Vervoer
contact/index.html         Contact
css/style.css              Alle opmaak (kleuren staan bovenaan in :root)
img/                       Foto's, logo, favicon
fonts/                     Nunito, Nunito Sans, Merriweather (zelf gehost)
```

Geen JavaScript, geen cookies, geen externe lettertypes. De kop en voet
staan in elke pagina; pas ze bij een wijziging in alle vier aan.

## Bekijken

Lokaal: `python3 -m http.server` in deze map en open http://localhost:8000.

## Open punten

- Het contactformulier opent nu het mailprogramma van de bezoeker
  (`mailto:`). Vervangen door een formulierdienst als dat gewenst is.
- De kaart op de contactpagina komt van OpenStreetMap (geen cookies).
