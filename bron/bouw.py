"""Bouwt alle pagina's van autoservicebarneveld.nl.

Gebruik (vanuit de map van de repo):  python bron/bouw.py

Kop, voet, afspraakvenster en bedrijfsgegevens staan hier op één plek.
Bedrijfsgegevens voor Google (schema.org) staan in bron/bedrijf.json.
Alleen de Python-standaardbibliotheek is nodig.
"""
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def versie(pad):
    """Korte hash van een bestand, achter de link gezet (?v=...) zodat browsers
    na een wijziging meteen de nieuwe versie laden in plaats van een oude kopie."""
    return hashlib.sha1((ROOT / pad).read_bytes()).hexdigest()[:8]
SITE = "https://www.autoservicebarneveld.nl"
DATUM = __import__("datetime").date.today().isoformat()  # lastmod in de sitemap = bouwdatum

TEL = "0342-234003"
REVIEW_LINK = "https://g.page/r/CVfGuGQnGn8fEBM/review"  # Google: schrijf een review
TEL_LINK = "tel:+31342234003"
WA_LINK = "https://wa.me/31342234003"
MAIL = "contact@autoservicebarneveld.nl"
ADRES = "Verlengde Parallelweg 4-10"
POSTCODE_PLAATS = "3771 LP Barneveld"
KVK = "61874744"
BTW = "NL005077005B42"
TIJDEN_KORT = "Ma–vr 08:00–17:00 · za op afspraak"
PROFIELEN = [
    ("Google", "https://share.google/3KAll3CN6YYB3Vqca"),
    ("Facebook", "https://www.facebook.com/p/Autoservice-Barneveld-61586756678035/"),
    ("Instagram", "https://www.instagram.com/autoservicebarneveld/"),
    ("LinkedIn", "https://nl.linkedin.com/company/autoservice-barneveld"),
]

CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
       "frame-src https://www.openstreetmap.org; connect-src 'self' https://formsubmit.co https://api.pdok.nl https://opendata.rdw.nl https://api.open-meteo.com; form-action 'self' mailto: https://formsubmit.co; "
       "base-uri 'self'; object-src 'none'")

# ------------------------------------------------------------------ iconen
I_TEL = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
I_MAIL = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg>'
I_PIN = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/></svg>'
I_WA = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
I_KLOK = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></g></svg>'
I_PIJL = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.6"/></svg>'
I_BLIKSEM = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>'
I_VINK = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M5 12.5 10 17l9-10"/></svg>'
I_NL = '<svg viewBox="0 0 24 20"><g fill="#f6c500"><circle cx="19.00" cy="10.00" r="1.2"/><circle cx="18.06" cy="13.50" r="1.2"/><circle cx="15.50" cy="16.06" r="1.2"/><circle cx="12.00" cy="17.00" r="1.2"/><circle cx="8.50" cy="16.06" r="1.2"/><circle cx="5.94" cy="13.50" r="1.2"/><circle cx="5.00" cy="10.00" r="1.2"/><circle cx="5.94" cy="6.50" r="1.2"/><circle cx="8.50" cy="3.94" r="1.2"/><circle cx="12.00" cy="3.00" r="1.2"/><circle cx="15.50" cy="3.94" r="1.2"/><circle cx="18.06" cy="6.50" r="1.2"/></g></svg>'
I_STER = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 2 3 6.6 7 .7-5.3 4.8 1.6 7L12 17.5 5.7 21l1.6-7L2 9.3l7-.7z"/></svg>'

# ------------------------------------------------------------------ diensten
# slug, naam, title (max 60), description, kopregel, foto, alt, korte tekst (homepage), knoptekst
DIENSTEN = [
    ("onderhoud-reparatie", "Onderhoud & reparatie",
     "Onderhoud en reparatie Barneveld | Autoservice Barneveld",
     "Kleine of grote beurt en reparaties voor alle merken in Barneveld. U bepaalt wanneer we overleggen en krijgt updates via WhatsApp. Bel 0342-234003.",
     "Onderhoud en reparatie in Barneveld", "dienst-onderhoud", "Monteur aan het werk bij een wiel",
     "Grote of kleine onderhoudsbeurt, of het vervangen van een lampje: wij zorgen dat uw auto veilig, betrouwbaar en in topconditie blijft.",
     "Plan onderhoud"),
    ("apk-keuring", "APK-keuring",
     "APK-keuring Barneveld, alle merken | Autoservice Barneveld",
     "RDW-erkende APK-keuring in Barneveld voor alle merken, ook elektrische auto's. Plan uw afspraak eenvoudig via WhatsApp.",
     "APK-keuring in Barneveld", "dienst-apk", "Auto op de brug tijdens een APK-keuring",
     "De verplichte keuring voor verkeersveiligheid en milieu, zorgvuldig uitgevoerd voor alle merken.",
     "Plan APK"),
    ("diagnose", "Diagnose",
     "Auto uitlezen en diagnose Barneveld | Autoservice Barneveld",
     "Brandt er een storingslampje? Wij lezen uw auto uit met moderne diagnoseapparatuur en verhelpen de storing. Alle merken, in Barneveld.",
     "Diagnose en storingen verhelpen", "dienst-diagnose", "Uitleesapparatuur bij een auto",
     "Met moderne (uitlees)apparatuur sporen wij storingen en elektronische problemen snel op en verhelpen ze.",
     "Plan diagnose"),
    ("bandenservice", "Bandenservice & uitlijnen",
     "Banden en uitlijnen Barneveld | Autoservice Barneveld",
     "Montage, balanceren, seizoenswissel en uitlijnen in Barneveld. Zomer-, winter- en all-seasonbanden voor alle merken, ook elektrische auto's.",
     "Bandenservice en uitlijnen in Barneveld", "dienst-banden", "Band op de bandenmontagemachine",
     "Montage, balanceren, (seizoens)wissel en uitlijnen. Snel en vakkundig, voor alle merken, ook elektrische auto's.",
     "Plan banden"),
    ("airco-service", "Aircoservice",
     "Aircoservice auto in Barneveld | Autoservice Barneveld",
     "Auto-airco vullen, controleren, lekdetectie en reparatie voor alle merken in Barneveld. Koel in de zomer, heldere ruiten in de winter.",
     "Aircoservice voor uw auto", "dienst-airco", "Aircoservice onder de motorkap",
     "Vullen, controleren, lekdetectie en reparaties. Koel in de zomer en helder zicht in de winter.",
     "Plan airco"),
    ("elektrische-auto", "Elektrische auto",
     "Onderhoud elektrische auto Barneveld | Autoservice Barneveld",
     "Ook een elektrische auto heeft onderhoud nodig. Banden, remmen, ophanging, airco en APK voor alle merken. Autoservice Barneveld.",
     "Onderhoud van uw elektrische auto", "dienst-onderhoud", "Monteur werkt aan de wielophanging van een auto",
     "Het reguliere onderhoud, banden, airco en APK van elektrische auto's van alle merken.",
     "Plan onderhoud"),
]
# Keuzes in de planner (meerdere mogelijk). Reparatie en Overig vragen om een korte omschrijving.
DIENST_OPTIES = ["Onderhoudsbeurt", "APK", "Diagnose", "Aircoservice", "Bandenservice", "Uitlijnen", "Reparatie", "Overig"]
# Welke plannerkeuze vooraf aangevinkt wordt vanaf een dienstpagina
DIENST_NAAR_KEUZE = {"Onderhoud & reparatie": "Onderhoudsbeurt", "APK-keuring": "APK", "Diagnose": "Diagnose",
                     "Bandenservice & uitlijnen": "Bandenservice", "Aircoservice": "Aircoservice",
                     "Elektrische auto": "Onderhoudsbeurt"}

TEKST = {
"apk-keuring": """
<p>De APK (Algemene Periodieke Keuring) is verplicht en controleert of uw auto veilig en milieuvriendelijk genoeg is voor de weg. Autoservice Barneveld is door de RDW erkend en keurt auto's van alle merken, ook elektrische auto's. We voeren de keuring zorgvuldig uit, zodat u veilig en volgens de wettelijke eisen de weg op gaat.</p>

<p class="apk-tip"><a href="{r}apk-check/"><strong>Gratis APK-check</strong><span>Zie met uw kenteken tot wanneer uw APK geldig is en vanaf wanneer u kunt keuren.</span></a></p>

<h2>Wanneer moet uw auto voor de APK?</h2>
<p>De vervaldatum van uw APK ziet u direct met onze <a href="{r}apk-check/">APK-check</a>. U kunt de keuring tot twee maanden vóór die datum laten doen zonder dat u er tijd mee verliest: de nieuwe vervaldatum wordt dan gerekend vanaf de oude.</p>

<h2>APK en onderhoud in één afspraak</h2>
<p>Veel klanten combineren de APK met een kleine of grote <a href="{r}onderhoud-reparatie/">onderhoudsbeurt</a>. Dat scheelt een extra ritje naar de garage. Komt er tijdens de keuring iets naar boven dat vervangen moet worden? Valt dat boven het bedrag dat u bij uw afspraak heeft opgegeven, dan overleggen we eerst met u, eventueel met een foto of filmpje via WhatsApp.</p>

<h2>Mobiel blijven</h2>
<p>Moet uw auto wat langer blijven? U kunt gebruikmaken van ons <a href="{r}vervangend-vervoer/">vervangend vervoer</a>, zoals een elektrische leenauto of een leenfiets. Het station ligt op vijf minuten lopen.</p>
""",
"onderhoud-reparatie": """
<p>Wij onderhouden en repareren auto's van alle merken en modellen. Of het nu gaat om een kleine of grote onderhoudsbeurt, nieuwe remmen of het vervangen van een lampje: wij zorgen dat uw auto veilig, betrouwbaar en in topconditie blijft.</p>

<h2>Kleine en grote beurt</h2>
<p>Regelmatig onderhoud voorkomt dure reparaties later. Bij een beurt controleren en vervangen we wat volgens het onderhoudsschema van uw auto nodig is, zoals olie, filters en vloeistoffen, en kijken we naar remmen, banden, verlichting en ophanging.</p>

<h2>Reparaties</h2>
<p>Van remmen en ophanging tot uitlaat en elektronische storingen: onze werkplaats is uitgerust met moderne apparatuur, zodat we zowel regulier onderhoud als complexere reparaties kunnen uitvoeren. Heeft uw auto een storing? Lees meer over onze <a href="{r}diagnose/">diagnose</a>.</p>

<h2>Geen verrassingen achteraf</h2>
<p>U geeft zelf aan tot welk bedrag we mogen doorwerken. Wordt het duurder, dan overleggen we eerst met u. Ontdekken we tijdens het werk iets onverwachts, dan houden we u direct op de hoogte via WhatsApp, met foto's, korte filmpjes of een duidelijke toelichting. Zo weet u altijd wie er aan uw auto werkt en wat er gaat gebeuren.</p>

<h2>Combineer met uw APK</h2>
<p>Is uw <a href="{r}apk-keuring/">APK</a> bijna verlopen? Plan die dan tegelijk met uw onderhoudsbeurt in.</p>
""",
"diagnose": """
<p>Brandt er een storingslampje op uw dashboard, of doet uw auto vreemd? Moderne auto's zitten vol elektronica, en dan is goed uitlezen het halve werk. Wij beschikken over moderne (uitlees)apparatuur om storingen en elektronische problemen aan uw auto snel te vinden en te verhelpen.</p>

<h2>Hoe werkt het?</h2>
<p>We sluiten de diagnoseapparatuur aan op uw auto en lezen de opgeslagen foutcodes uit. Een foutcode alleen zegt niet alles, dus daarna zoeken we de oorzaak gericht op. U hoort van ons wat er aan de hand is en wat het herstel kost, voordat we iets vervangen.</p>

<h2>Welke storingen?</h2>
<p>Bijvoorbeeld een brandend motorlampje, ABS- of airbaglampje, problemen met starten of laden, sensoren die het niet meer doen of storingen in de elektronica. Dat geldt voor alle merken, ook voor <a href="{r}elektrische-auto/">elektrische auto's</a>.</p>

<h2>Snel weer op weg</h2>
<p>Is de storing gevonden, dan kunnen we de <a href="{r}onderhoud-reparatie/">reparatie</a> meestal direct inplannen. U blijft mobiel met ons <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p>
""",
"bandenservice": """
<p>Goede banden zijn belangrijk voor uw veiligheid, uw remweg en uw verbruik. Wij verzorgen montage, balanceren, de seizoenswissel en het uitlijnen van uw wielen. We werken snel en vakkundig, zodat uw auto altijd de juiste grip houdt.</p>

<h2>Zomer- en winterbanden wisselen</h2>
<p>Rijdt u in de winter op winterbanden, dan wisselen we ze in het najaar en voorjaar voor u om. We controleren daarbij meteen het profiel, de bandenspanning en eventuele schade.</p>

<h2>Nieuwe banden</h2>
<p>Toe aan nieuwe banden? Wij leveren en monteren banden voor alle merken, ook voor elektrische auto's. Die zijn zwaarder en hebben meer koppel, en vragen daarom vaak om banden die daarvoor geschikt zijn. We adviseren u graag over de juiste keuze.</p>

<h2>Balanceren</h2>
<p>Trilt uw stuur bij een bepaalde snelheid? Dan zijn uw wielen mogelijk uit balans. Met balanceren rijdt uw auto weer rustig en slijten uw banden gelijkmatiger.</p>

<h2>Uitlijnen</h2>
<p>Trekt uw auto naar links of rechts, staat uw stuur scheef terwijl u rechtdoor rijdt, of slijten uw banden aan de binnen- of buitenkant? Dan staan uw wielen waarschijnlijk niet meer goed. Bij het uitlijnen meten we de stand van uw wielen nauwkeurig op en stellen we die af volgens de voorschriften van de fabrikant.</p>
<p>Laat uw auto in elk geval nakijken na een flinke klap tegen een stoeprand of door een diepe kuil, en na vervanging van onderdelen van de wielophanging of besturing. Goed uitgelijnde wielen zorgen voor een auto die recht en stabiel rijdt, banden die langer meegaan en een lager verbruik.</p>
""",
"airco-service": """
<p>Voor een goed werkende airco bent u bij ons aan het juiste adres. Wij controleren en vullen aircosystemen van alle merken, sporen lekkages op en voeren reparaties uit. Zo blijft uw auto koel in de zomer en blijven uw ruiten helder in de winter.</p>

<h2>Waarom aircoservice?</h2>
<p>Een airco verliest ieder jaar een beetje koudemiddel. Koelt uw airco minder goed, ruikt het muf of beslaan uw ruiten snel? Dan is het tijd voor een controle. Een goed werkende airco droogt de lucht, waardoor uw ruiten in de winter sneller ontwasemen.</p>

<h2>Wat we doen</h2>
<p>We controleren het systeem, vullen het koudemiddel bij en sporen eventuele lekkages op. Is er een onderdeel defect, dan hoort u van ons wat er nodig is. Valt de reparatie boven het bedrag dat u heeft opgegeven, dan overleggen we eerst.</p>

<h2>Combineer met onderhoud</h2>
<p>Een aircoservice laat zich goed combineren met een <a href="{r}onderhoud-reparatie/">onderhoudsbeurt</a> of uw <a href="{r}apk-keuring/">APK</a>.</p>
""",
"elektrische-auto": """
<p>Een elektrische auto heeft geen olie te verversen, maar onderhoud is nog steeds nodig. Bij Autoservice Barneveld kunt u terecht voor het reguliere onderhoud van elektrische auto's van alle merken. U hoeft daarvoor niet naar de dealer.</p>

<h2>Wat onderhouden we aan een elektrische auto?</h2>
<p>Elektrische auto's zijn zwaarder dan auto's met een brandstofmotor. Daardoor vragen vooral <a href="{r}bandenservice/">banden</a>, wielophanging en draagarmen extra aandacht. Daarnaast controleren we remmen en remvloeistof, verlichting, ruitenwissers, het interieurfilter, de <a href="{r}airco-service/">airco</a> en de 12-voltaccu.</p>

<h2>Ervaring van een klant</h2>
<blockquote>"Autoservice Barneveld heeft onlangs de draagarmen van mijn Tesla vervangen. Tijdens de werkzaamheden hield Matthijs me goed op de hoogte. Het vervangend vervoer was perfect geregeld. Top service!"</blockquote>

<h2>APK en diagnose</h2>
<p>Ook een elektrische auto is APK-plichtig. Wij keuren alle merken, zie <a href="{r}apk-keuring/">APK-keuring</a>. Brandt er een storingslampje? Onze <a href="{r}diagnose/">diagnoseapparatuur</a> is ook geschikt voor elektrische auto's.</p>

<h2>Zelf ook elektrisch onderweg</h2>
<p>Terwijl uw auto bij ons staat, kunt u rijden in onze elektrische Renault 5. Lees meer over ons <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p>
""",
}


def e(t):
    return html.escape(t, quote=True)


def srcset(r, naam, sizes):
    """srcset + sizes voor een foto in img/, met de kleinere varianten (naam-480.webp enz.) die bestaan."""
    from PIL import Image
    breedte = Image.open(ROOT / "img" / f"{naam}.webp").size[0]
    delen = [f"{r}img/{naam}-{b}.webp {b}w" for b in (480, 960, 1440) if (ROOT / "img" / f"{naam}-{b}.webp").exists()]
    delen.append(f"{r}img/{naam}.webp {breedte}w")
    return f'srcset="{", ".join(delen)}" sizes="{sizes}"'


# ------------------------------------------------------------------ vaste blokken
def schema_tag():
    data = json.loads((ROOT / "bron" / "bedrijf.json").read_text(encoding="utf-8"))
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>")


def head(r, pad, title, desc, noindex=False, og="deelafbeelding.jpg"):
    regels = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        '<meta name="theme-color" content="#0a467f">',
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(desc)}">',
    ]
    if noindex:
        regels.append('<meta name="robots" content="noindex">')
    else:
        url = SITE + "/" + pad
        regels += [
            f'<link rel="canonical" href="{url}">',
            '<meta property="og:type" content="website">',
            '<meta property="og:locale" content="nl_NL">',
            '<meta property="og:site_name" content="Autoservice Barneveld">',
            f'<meta property="og:title" content="{e(title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:image" content="{SITE}/img/{og}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta name="twitter:card" content="summary_large_image">',
            schema_tag(),
        ]
    regels += [
        f'<link rel="icon" href="{r}img/favicon-32.png" sizes="32x32">',
        f'<link rel="apple-touch-icon" href="{r}img/apple-touch-icon.png">',
        f'<link rel="preload" href="{r}fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="preload" href="{r}fonts/bebas-neue.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="stylesheet" href="{r}css/style.css?v={versie('css/style.css')}">',
        f'<script src="{r}js/site.js?v={versie('js/site.js')}" defer></script>',
    ]
    return "\n".join(regels)


def kop(r, actief):
    home = r or "./"
    items = [(f"{home}#diensten" if r else "#diensten", "Diensten", "diensten"),
             (f"{r}over-ons/", "Over ons", "over-ons"),
             (f"{r}vervangend-vervoer/", "Vervangend vervoer", "vervangend-vervoer"),
             (f"{r}contact/", "Contact", "contact")]
    huidig = ' aria-current="page"'
    menu = "\n".join(
        f'      <a href="{h}"{huidig if k == actief else ""}>{n}</a>'
        for h, n, k in items) + f'\n      <a class="alleen-mobiel" href="{r}handig/">Zelf checken</a>'
    checks = "\n".join(f'          <li><a href="{r}{slug}/">{e(n)}</a></li>'
                        for _kop, _sub, lijst in HANDIG for slug, n, _u in lijst)
    return f"""<a class="naar-inhoud" href="#inhoud">Direct naar de inhoud</a>

<div class="topbalk">
  <div class="wrap">
    <span class="links">{TIJDEN_KORT} · zo gesloten</span>
    <span class="rechts"><a href="{TEL_LINK}">{TEL}</a><a href="{WA_LINK}">WhatsApp</a><a class="mail" href="mailto:{MAIL}">{MAIL}</a></span>
  </div>
</div>

<header class="kop">
  <div class="wrap">
    <a class="kop-logo" href="{home}"><img src="{r}img/logo.svg" alt="Autoservice Barneveld" width="136" height="56"></a>
    <nav class="menu" id="menu" aria-label="Hoofdmenu">
{menu}
    </nav>
    <details class="checks-menu">
      <summary>Zelf checken <svg width="12" height="12" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></summary>
      <ul>
{checks}
          <li class="alles"><a href="{r}handig/">Alles bij elkaar</a></li>
      </ul>
    </details>
    <a class="apk-knop" href="{r}apk-check/"{' aria-current="page"' if actief == "apk-check" else ""}><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M8.5 14l2.5 2.5 4.5-5"/></g></svg>APK-check</a>
    <a class="knop blauw" href="{r}contact/" data-afspraak>Plan afspraak</a>
    <button class="menu-knop" type="button" aria-expanded="false" aria-controls="menu" aria-label="Menu openen">
      <svg width="22" height="16" viewBox="0 0 22 16" aria-hidden="true"><path d="M0 1h22M0 8h22M0 15h22" stroke="currentColor" stroke-width="2.2"/></svg>
    </button>
  </div>
</header>"""


def dienst_select(id_, verplicht=True, leeg="Kies een dienst"):
    opties = "\n".join(f"            <option>{e(o)}</option>" for o in DIENST_OPTIES)
    return (f'<select id="{id_}" name="dienst"{" required" if verplicht else ""}>\n'
            f'            <option value="">{leeg}</option>\n{opties}\n          </select>')


def diensten_vinkjes():
    return "\n".join(
        f'            <label><input type="checkbox" name="diensten" value="{e(o)}"><span>{e(o)}</span></label>'
        for o in DIENST_OPTIES)


def kenteken_veld(id_, verplicht=True):
    return f"""<div class="kenteken">
            <span class="nl" aria-hidden="true">
              {I_NL}
              NL
            </span>
            <input id="{id_}" name="kenteken" placeholder="AB-123-C" maxlength="8" autocomplete="off" spellcheck="false" autocapitalize="characters"{" required" if verplicht else ""}>
          </div>
          <p class="rdw-info" aria-live="polite" hidden></p>"""


def venster(r):
    return f"""<dialog class="venster" id="afspraak-venster" aria-labelledby="venster-titel">
  <button class="sluit" type="button" aria-label="Sluiten"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2l12 12M14 2 2 14" stroke="currentColor" stroke-width="2.4"/></svg></button>
  <div class="venster-binnen">
    <div class="venster-invullen">
      <h2 id="venster-titel">Plan uw afspraak</h2>
      <p class="uitleg">Vul uw gegevens in. Daarna opent WhatsApp met uw aanvraag al klaar; u verstuurt hem zelf. Geen WhatsApp? Versturen per e-mail kan ook.</p>
      <form method="dialog" novalidate data-verplicht>
        <div class="veld kenteken-blok">
          <label for="v-kenteken">Kenteken</label>
          {kenteken_veld("v-kenteken")}
          <button type="button" class="link-klein kenteken-onbekend">Ik weet mijn kenteken niet</button>
        </div>
        <div class="merk-model" hidden>
          <div class="rij">
            <div class="veld"><label for="v-merk">Merk</label><input class="invoer" id="v-merk" name="merk" autocomplete="off" placeholder="bijv. Volkswagen"></div>
            <div class="veld"><label for="v-model">Model</label><input class="invoer" id="v-model" name="model" autocomplete="off" placeholder="bijv. Golf"></div>
          </div>
          <button type="button" class="link-klein kenteken-bekend">Toch kenteken invullen</button>
        </div>
        <fieldset class="veld diensten-keuze">
          <legend>Wat mogen we voor u doen? <small>Meerdere mogelijk</small></legend>
          <div class="diensten-raster">
{diensten_vinkjes()}
          </div>
        </fieldset>
        <div class="veld omschrijving">
          <label for="v-omschrijving"><span class="omschrijving-label">Opmerking</span> <small class="label-optioneel">optioneel</small></label>
          <textarea class="invoer" id="v-omschrijving" name="omschrijving" rows="2" maxlength="300" placeholder="Bijv. wanneer u de auto kunt brengen of iets wat we moeten weten"></textarea>
        </div>
        <div class="veld overleg">
          <label for="v-grens">Eerst overleggen boven <small class="label-optioneel">optioneel</small></label>
          <div class="overleg-rij">
            <span class="euro-veld"><span aria-hidden="true">€</span><input class="invoer" id="v-grens" name="overleggrens" inputmode="numeric" autocomplete="off" placeholder="bijv. 250" maxlength="6"></span>
            <small class="overleg-uitleg">Kost het werk meer, dan nemen we eerst contact met u op. Leeg laten? Dan overleggen we bij alles wat extra is.</small>
          </div>
        </div>
        <div class="rij">
          <div class="veld">
            <label for="v-km">Kilometerstand</label>
            <input class="invoer" id="v-km" name="kilometerstand" inputmode="numeric" autocomplete="off" placeholder="bijv. 85.000" required>
            <button type="button" class="link-klein km-onbekend" aria-pressed="false">Ik weet de km-stand niet</button>
          </div>
          <div class="veld">
            <label for="v-mail">E-mailadres</label>
            <input class="invoer" id="v-mail" name="email" type="email" autocomplete="email" placeholder="naam@voorbeeld.nl" required>
          </div>
        </div>
        <div class="rij adres">
          <div class="veld">
            <label for="v-postcode">Postcode</label>
            <input class="invoer" id="v-postcode" name="postcode" autocomplete="postal-code" placeholder="1234 AB" maxlength="7" required>
          </div>
          <div class="veld">
            <label for="v-huisnummer">Huisnummer</label>
            <input class="invoer" id="v-huisnummer" name="huisnummer" autocomplete="off" placeholder="bijv. 12A" maxlength="10" required>
          </div>
        </div>
        <p class="adres-gevonden" aria-live="polite" hidden></p>
        <label class="schakel" for="v-vervoer">
          <span class="schakel-tekst"><strong>Vervangend vervoer nodig?</strong><span>Terwijl uw auto bij ons staat.</span></span>
          <input type="checkbox" id="v-vervoer" name="vervoer" role="switch" aria-controls="v-vervoer-keuze">
          <span class="schakel-baan" aria-hidden="true"><span class="ja">Ja</span><span class="nee">Nee</span></span>
        </label>
        <fieldset class="vervoer-keuze" id="v-vervoer-keuze" hidden>
          <legend class="sr-only">Kies uw vervangend vervoer</legend>
          <label><input type="radio" name="vervoermiddel" value="Renault 5 (elektrisch)"><span><strong>Renault 5 <svg class="blad" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 3C10 3 4 8 4 15c0 1.6.4 3 1 4.2C7 14 11 10.5 16 8.5c-4 2.6-7.4 6.4-9.3 11.3 1.3.8 2.8 1.2 4.3 1.2C18 21 21 13 20 3z"/></svg><span class="sr-only"> (milieuvriendelijk)</span></strong><small>€ 34,70 p/d</small></span></label>
          <label><input type="radio" name="vervoermiddel" value="Volkswagen Caddy"><span><strong>Volkswagen Caddy</strong><small>€ 23,60 p/d</small></span></label>
          <label><input type="radio" name="vervoermiddel" value="Leenfiets"><span><strong>Leenfiets <svg class="blad" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 3C10 3 4 8 4 15c0 1.6.4 3 1 4.2C7 14 11 10.5 16 8.5c-4 2.6-7.4 6.4-9.3 11.3 1.3.8 2.8 1.2 4.3 1.2C18 21 21 13 20 3z"/></svg><span class="sr-only"> (milieuvriendelijk)</span></strong><small>Gratis</small></span></label>
          <p class="vervoer-btw">Prijzen incl. btw.</p>
        </fieldset>
        <button type="button" class="datum-knop" aria-expanded="false" aria-controls="v-datum-keuze"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></g></svg><span><strong>Voorkeursdatum opgeven</strong><small>Optioneel, kies twee dagen in de kalender</small></span></button>
        <fieldset class="datum-keuze" id="v-datum-keuze" hidden>
          <legend>Kies twee voorkeursdata</legend>
          <div class="kalender">
            <div class="kal-kop">
              <button type="button" class="kal-vorige" aria-label="Vorige maand">‹</button>
              <strong class="kal-maand" aria-live="polite"></strong>
              <button type="button" class="kal-volgende" aria-label="Volgende maand">›</button>
            </div>
            <div class="kal-dagen" aria-hidden="true"><span>ma</span><span>di</span><span>wo</span><span>do</span><span>vr</span><span>za</span><span>zo</span></div>
            <div class="kal-raster"></div>
          </div>
          <p class="datum-gekozen" aria-live="polite"></p>
          <input type="hidden" name="datum1"><input type="hidden" name="datum2">
          <p class="datum-let-op"><strong>Let op: dit is nog geen afspraak.</strong> Wij bekijken uw voorkeur en bevestigen de afspraak daarna.</p>
          <p class="datum-haast">{I_TEL.format(s=18)}<span><strong>Haast, of wilt u eerder geholpen worden?</strong> Bel even <a href="{TEL_LINK}">{TEL}</a>. U heeft dan direct contact met ons en we helpen u meteen verder.</span></p>
          <button type="button" class="datum-weg">Geen voorkeursdatum</button>
        </fieldset>
        <button class="knop wa" type="submit" data-kanaal="whatsapp">{I_WA} Verstuur via WhatsApp</button>
        <p class="kanaal-uitleg">De snelste manier om uw afspraak te regelen.</p>
        <div class="mail-optie">
          <span>Geen WhatsApp?</span>
          <button type="submit" class="knop-mail" data-kanaal="mail"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 5h18v14H3zM3 6l9 7 9-7"/></svg><span>Verstuur per e-mail</span></button>
        </div>
        <p class="mail-melding" role="status" hidden></p>
        <p class="klein">Uw gegevens gaan alleen naar ons. Zie de <a href="{r}privacy/">privacyverklaring</a>. Liever bellen? <a href="{TEL_LINK}">{TEL}</a></p>
      </form>
    </div>
    <div class="venster-klaar" hidden>
      <svg width="56" height="56" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.2 3L17 9"/></g></svg>
      <h2>Bijna klaar</h2>
      <p class="uitleg">WhatsApp is geopend met uw aanvraag. Druk daar op <strong>verzenden</strong>, dan nemen wij zo snel mogelijk contact op om de afspraak vast te leggen.</p>
      <p class="klein">Opent WhatsApp niet? <a class="wa-opnieuw" href="{WA_LINK}">Probeer het opnieuw</a> of bel <a href="{TEL_LINK}">{TEL}</a>.</p>
    </div>
    <div class="venster-klaar venster-klaar-mail" hidden>
      <svg width="56" height="56" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.2 3L17 9"/></g></svg>
      <h2>Aanvraag verstuurd</h2>
      <p class="uitleg">Uw aanvraag is per e-mail bij ons binnengekomen. Wij nemen zo snel mogelijk contact op om de afspraak vast te leggen.</p>
      <p class="klein">Haast? Bel <a href="{TEL_LINK}">{TEL}</a>.</p>
    </div>
  </div>
</dialog>"""


def voet(r):
    home = r or "./"
    diensten = "".join(f'<li><a href="{r}{d[0]}/">{e(d[1])}</a></li>' for d in DIENSTEN)
    profielen = " · ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in PROFIELEN)
    return f"""<footer class="voet">
  <div class="wrap">
    <div>
      <a href="{home}"><img class="logo" src="{r}img/logo-wit.svg" alt="Autoservice Barneveld" width="160" height="66"></a>
      <p>Universele garage in Barneveld voor onderhoud, reparatie, APK, diagnose, banden, uitlijnen en airco. Alle merken, ook elektrisch.</p>
      <img class="rdw" src="{r}img/rdw-erkend.webp" alt="RDW erkend" width="132" height="77" loading="lazy">
    </div>
    <div>
      <h2>Adres en tijden</h2>
      <ul><li>{ADRES}</li><li>{POSTCODE_PLAATS}</li><li>Ma–vr 08:00–17:00</li><li>Za op afspraak · zo gesloten</li><li><a href="{r}contact/">Route plannen</a></li></ul>
    </div>
    <div>
      <h2>Contact</h2>
      <ul><li><a href="{TEL_LINK}">{TEL}</a></li><li><a href="{WA_LINK}">WhatsApp</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="{r}contact/" data-afspraak>Plan afspraak</a></li></ul>
      <h2 class="voet-sub">Handig</h2>
      <ul><li><a href="{r}apk-check/">APK-check</a></li><li><a href="{r}occasion-check/">Occasion-check</a></li><li><a href="{r}dashboardlampjes/">Dashboardlampjes</a></li><li><a href="{r}hulp/">Hulp bij klachten</a></li><li><a href="{r}handig/">Alle checks en uitleg</a></li></ul>
    </div>
    <div>
      <h2>Diensten</h2>
      <ul>{diensten}<li><a href="{r}aankoopkeuring/">Aankoopkeuring</a></li><li><a href="{r}vervangend-vervoer/">Vervangend vervoer</a></li></ul>
      <h2 class="voet-sub">Meer</h2>
      <ul><li><a href="{r}merken/">Alle merken</a></li><li><a href="{r}werkgebied/">Werkgebied</a></li><li><a href="{r}veelgestelde-vragen/">Veelgestelde vragen</a></li></ul>
    </div>
    <p class="onder">© 2026 Autoservice Barneveld · KvK {KVK} · btw {BTW} · <a href="{r}privacy/">Privacyverklaring</a> · Volg ons: {profielen}</p>
  </div>
</footer>"""


def pagina(r, pad, title, desc, actief, main, noindex=False):
    foto, OG_FOTO[0] = OG_FOTO[0], None
    og = f"og-{foto}.jpg" if foto and (ROOT / "img" / f"og-{foto}.jpg").exists() else "deelafbeelding.jpg"
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
{head(r, pad, title, desc, noindex, og)}
</head>
<body>
{kop(r, actief)}

<main id="inhoud">
{main}
</main>

{voet(r)}

{venster(r)}
</body>
</html>
"""


def zijkaart(r, dienst=""):
    dienst = DIENST_NAAR_KEUZE.get(dienst, dienst if dienst in DIENST_OPTIES else "")
    data = f' data-dienst="{e(dienst)}"' if dienst else ""
    return f"""<aside class="zijkaart" aria-labelledby="zijkaart-titel">
        <h2 id="zijkaart-titel">Plan uw afspraak</h2>
        <p>Vul uw kenteken en gegevens in, dan staat uw aanvraag klaar in WhatsApp. Per e-mail kan ook.</p>
        <a class="knop oranje" href="{r}contact/" data-afspraak{data}>Plan afspraak {I_PIJL}</a>
        <ul>
          <li>Bel <a href="{TEL_LINK}">{TEL}</a></li>
          <li>App via <a href="{WA_LINK}">WhatsApp</a></li>
          <li>{TIJDEN_KORT}</li>
          <li>{ADRES}, {POSTCODE_PLAATS}</li>
        </ul>
      </aside>"""


OG_FOTO = [None]  # foto van de laatst opgebouwde paginakop, voor de deelafbeelding


def pagina_kop(r, h1, foto, kicker="", inleiding=""):
    OG_FOTO[0] = foto
    k = f'<span class="kicker"><i aria-hidden="true"></i>{kicker}</span>\n      ' if kicker else ""
    i = f'\n      <p class="inleiding">{inleiding}</p>' if inleiding else ""
    return f"""  <section class="pagina-kop">
    <div class="hero-foto"><img src="{r}img/{foto}.webp" {srcset(r, foto, "100vw")} alt="" width="1848" height="1232" fetchpriority="high"></div>
    <div class="wrap">
      {k}<h1>{h1}</h1>{i}
    </div>
  </section>"""


def schrijf(pad, inhoud):
    doel = ROOT / pad
    doel.parent.mkdir(parents=True, exist_ok=True)
    doel.write_text(inhoud, encoding="utf-8", newline="\n")
    print("geschreven", pad)


# ------------------------------------------------------------------ reviews
# Overgenomen van het Google Bedrijfsprofiel (november 2026). Namen ingekort
# tot voornaam en voorletter. Reviews zonder tekst staan er niet in.
REVIEWS = [
    ("Jan W.", "Autoservice Barneveld heeft onlangs de draagarmen van mijn Tesla vervangen. Tijdens de werkzaamheden hield Matthijs me goed op de hoogte. Het vervangend vervoer was perfect geregeld. Top service!"),
    ("Griselda M.", "Wat een topservice van Matthijs! Helemaal blij ermee, ik reed weer weg in een nieuwe auto! Tot de volgende keer. 😊"),
    ("Erik", "Kon snel terecht en communicatie verliep soepel. Netjes vooraf verteld wat het ging kosten. Leenauto ook erg handig!"),
    ("John V.", "Top service, kon snel terecht en mijn auto was ook snel weer klaar. Vriendelijk geholpen door Matthijs!"),
    ("Jens G.", "Auto bij Matthijs gebracht voor een servicebeurt. Goede communicatie, snelle service en ook nog eens de auto gewassen!"),
    ("D. B.", "Super service! Zeker aan te raden"),
    ("Mario", "Matthijs is heel vriendelijk en neemt de tijd voor je om alles uit te leggen. Denkt met je mee en is helder in wat je kunt verwachten. Tot de volgende keer!"),
    ("Diederick B.", "Kwam voor wat onderhoud maar door proactief even een check te doen ontdekte Matthijs meer problemen die eerst werden gedeeld voordat er werd gerepareerd. …"),
    ("Jaap V.", "Transparant, goede service en prima communicatie. Zeer tevreden met deze autogarage"),
    ("Marjolyntje K.", "Matthijs, wat een vakman! Ik ben heel blij met jou. Dat je zo snel en vakkundig mijn slepende problemen direct hebt gevonden en opgelost. Ik heb iedere keer weer een grote grijns op mijn gezicht zodra ik weer in mijn auto rond zoef en vlotjes kan inhalen :-)"),
    ("Martijn C.", "Goede service, een betrouwbare knul."),
    ("André W.", "Fijne garage dat goed meedenkt!"),
    ("Herwin H.", "Top service en lekker snel!"),
]


def review_sectie():
    google = dict(PROFIELEN)["Google"]

    def kaartjes(kopie):
        uit = []
        for naam, tekst in REVIEWS:
            verborgen = ' aria-hidden="true"' if kopie else ""
            uit.append(f"""          <figure class="review-kaartje"{verborgen}>
            <div class="sterren" role="img" aria-label="Vijf sterren">{I_STER * 5}</div>
            <blockquote><p>{e(tekst)}</p></blockquote>
            <figcaption>{e(naam)} · Google-review</figcaption>
          </figure>""")
        return "\n".join(uit)

    return f"""  <section class="review" aria-labelledby="review-titel">
    <div class="wrap">
      <div class="kopje">
        <div>
          <span class="label">Reviews</span>
          <h2 class="groot" id="review-titel">Wat klanten zeggen</h2>
        </div>
        <div class="review-acties">
          <a class="review-schrijf" href="{REVIEW_LINK}" rel="noopener">{I_STER}<span>Schrijf een review</span></a>
          <a class="review-alle" href="{google}" rel="noopener">Alle reviews op Google</a>
          <button type="button" class="review-pauze" aria-label="Reviews stilzetten" aria-pressed="false" hidden><svg class="ico-pauze" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg><svg class="ico-speel" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 4l13 8-13 8z"/></svg></button>
        </div>
      </div>
    </div>
    <div class="review-band">
      <div class="review-spoor">
{kaartjes(False)}
{kaartjes(True)}
      </div>
    </div>
  </section>"""


# ------------------------------------------------------------------ homepage
WAAROM = [
    ("Korte lijnen",
     "Wie u aan de telefoon of op WhatsApp spreekt, sleutelt ook aan uw auto. Uw vraag komt dus nooit via via bij de monteur terecht.",
     '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>'),
    ("Geen wachttijden",
     "Geen keuzemenu, geen receptie en geen rij aan de balie. U belt of appt en krijgt direct antwoord van de vakman zelf.",
     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    ("Dealermogelijkheden",
     "Ik heb toegang tot alle dealersoftware en de mogelijkheid om originele onderdelen te bestellen.",
     '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    ("Uw fabrieksgarantie blijft geldig",
     'Onderhoud volgens de voorschriften van de fabrikant houdt uw garantie intact. Daarvoor hoeft u niet naar de dealer. <a href="merken/">Lees meer</a>',
     '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    ("Bijgeschoold en gecertificeerd",
     "Auto's veranderen snel. Daarom volg ik regelmatig bijscholing en heb ik diverse aanvullende certificaten behaald.",
     '<circle cx="12" cy="9" r="5"/><path d="M9 13.5 8 21l4-2 4 2-1-7.5"/>'),
    ("Een eerlijk tarief",
     "Geen personeel, geen receptie en geen showroom. Die lagere kosten ziet u terug in een scherp en eerlijk tarief.",
     '<path d="M17 6.5A6.5 6.5 0 1 0 17 17.5M4 10h9M4 14h9"/>'),
]


def waarom_sectie():
    items = "\n".join(f"""        <li>
          <span class="ico" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ico}</g></svg></span>
          <h3>{e(kop)}</h3>
          <p>{tekst}</p>
        </li>""" for kop, tekst, ico in WAAROM)
    return f"""  <section class="sectie waarom" id="waarom" aria-labelledby="waarom-titel">
    <div class="wrap">
      <div class="kopje">
        <span class="label">Waarom Autoservice Barneveld</span>
        <h2 class="groot" id="waarom-titel">Dealerkwaliteit, zonder de omweg</h2>
        <p>Bij een dealer of grote garage spreekt u vaak eerst een receptie of serviceadviseur, en de monteur ziet u zelden. Bij ons regelt u alles rechtstreeks met de monteur die ook aan uw auto werkt.</p>
      </div>
      <ul class="waarom-raster">
{items}
      </ul>
      <p class="waarom-kortom"><strong>Kortom:</strong> u bespaart tijd, gedoe en geld, zonder in te leveren op kwaliteit.</p>
    </div>
  </section>"""


def homepage():
    r = ""
    lijst = []
    for slug, naam, _t, _d, _h, foto, alt, kort, knop in DIENSTEN:
        if slug == "elektrische-auto":
            continue
        lijst.append(f"""        <li class="dienst">
          <img src="img/{foto}.webp" {srcset("", foto, "(max-width: 600px) 100vw, 220px")} alt="{e(alt)}" width="960" height="639" loading="lazy">
          <div><h3><a href="{slug}/">{e(naam)}</a></h3><p>{kort}</p><a class="meer" href="{slug}/">Meer over {e(naam.lower() if slug != 'apk-keuring' else 'de APK')}</a></div>
          <a class="plan" href="contact/" data-afspraak data-dienst="{e(DIENST_NAAR_KEUZE.get(naam, "Onderhoudsbeurt"))}">{knop} <span aria-hidden="true">→</span></a>
        </li>""")
    lijst.append(f"""        <li class="dienst">
          <img src="img/hero-home.webp" {srcset("", "hero-home", "(max-width: 600px) 100vw, 220px")} alt="Auto op de brug voor een aankoopkeuring" width="960" height="639" loading="lazy">
          <div><h3><a href="aankoopkeuring/">Aankoopkeuring</a></h3><p>Een tweedehands auto vóór de koop onafhankelijk laten nakijken, met een eerlijk advies van de monteur.</p><a class="meer" href="aankoopkeuring/">Meer over de aankoopkeuring</a></div>
          <a class="plan" href="contact/" data-afspraak data-dienst="Overig" data-omschrijving="Aankoopkeuring">Plan aankoopkeuring <span aria-hidden="true">→</span></a>
        </li>""")
    diensten = "\n".join(lijst)
    main = f"""  <section class="hero" id="afspraak" aria-labelledby="hero-titel">
    <div class="hero-foto"><img src="img/hero-home.webp" {srcset("", "hero-home", "100vw")} alt="" width="1848" height="1232" fetchpriority="high"></div>
    <div class="wrap">
      <div class="hero-tekst">
        <h1 id="hero-titel">Vakkundig onderhoud voor uw auto in Barneveld</h1>
        <p>Onderhoud, reparatie, APK, diagnose, banden, uitlijnen en airco. Vul uw kenteken in, kies een dienst en verstuur uw aanvraag via WhatsApp.</p>
        <a class="hero-bel" href="{TEL_LINK}"><span aria-hidden="true">{I_TEL.format(s=20)}</span>Liever bellen? {TEL}</a>
        <p class="hero-bel-noot">Geen keuzemenu, geen wachtmuziek en geen receptie: u heeft meteen de monteur zelf aan de lijn.</p>
      </div>

      <form class="afspraak" id="afspraak-snel" action="contact/" method="get" aria-labelledby="afspraak-titel">
        <h2 id="afspraak-titel">Plan uw afspraak</h2>
        <p>In twee stappen geregeld via WhatsApp.</p>
        <div class="veld kenteken-blok">
          <label for="kenteken">Kenteken</label>
          {kenteken_veld("kenteken", verplicht=False)}
          <button type="button" class="link-klein kenteken-onbekend">Ik weet mijn kenteken niet</button>
        </div>
        <div class="merk-model" hidden>
          <div class="rij">
            <div class="veld"><label for="merk">Merk</label><input class="invoer" id="merk" name="merk" autocomplete="off" placeholder="bijv. Volkswagen"></div>
            <div class="veld"><label for="model">Model</label><input class="invoer" id="model" name="model" autocomplete="off" placeholder="bijv. Golf"></div>
          </div>
          <button type="button" class="link-klein kenteken-bekend">Toch kenteken invullen</button>
        </div>
        <fieldset class="veld diensten-keuze">
          <legend>Wat mogen we voor u doen? <small>Meerdere mogelijk</small></legend>
          <div class="diensten-raster">
{diensten_vinkjes()}
          </div>
        </fieldset>
        <button class="knop oranje" type="submit">Plan afspraak
          {I_PIJL}
        </button>
        <div class="afspraak-voet"><span>{TIJDEN_KORT}</span><a href="vervangend-vervoer/">Vervangend vervoer nodig?</a></div>
      </form>
    </div>
  </section>

  <section class="vertrouwen" aria-label="Waarom Autoservice Barneveld">
    <ul>
      <li><img class="rdw-mini" src="img/rdw-erkend.webp" alt="" width="62" height="36"><span><strong>APK</strong>RDW erkend · <a href="apk-check/">check uw APK-datum</a></span></li>
      <li><span class="ico" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 16V11l2-5h14l2 5v5M3 16h18M3 16v2h3v-2m12 0v2h3v-2M5 11h14"/></svg></span><span><strong><a href="merken/">Alle merken <span class="geen-breuk">(ook EV's)</span></a></strong>Onderhoud en reparatie</span></li>
      <li><span class="ico" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></span><span><strong>Alles onder één dak</strong>Alle zorg voor uw auto</span></li>
      <li><span class="ico" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/></g></svg></span><span><strong>Vervangend vervoer</strong>Leenauto of leenfiets</span></li>
    </ul>
  </section>

  <section class="sectie" id="diensten" aria-labelledby="diensten-titel">
    <div class="wrap">
      <div class="kopje">
        <span class="label">Diensten</span>
        <h2 class="groot" id="diensten-titel">Professioneel onderhoud en reparaties</h2>
        <p>Autoservice Barneveld is een moderne, universele garage met professionele apparatuur, duidelijke communicatie en heldere tarieven.</p>
      </div>
      <ul class="diensten">
{diensten}
      </ul>
      <p class="ev">{I_BLIKSEM.format(s=24)}<span>Ook een elektrische auto heeft onderhoud nodig. Wij verzorgen het reguliere onderhoud, banden, airco en APK van elektrische auto's van alle merken. <a href="elektrische-auto/">Meer over elektrische auto's</a></span></p>
    </div>
  </section>

{waarom_sectie()}

  <section class="sectie over" id="over-ons" aria-labelledby="over-titel">
    <div class="wrap">
      <div class="over-foto"><img src="img/hero-over-ons.webp" {srcset("", "hero-over-ons", "(max-width: 900px) 100vw, 560px")} alt="De monteur van Autoservice Barneveld in de werkplaats" width="1232" height="1848" loading="lazy"></div>
      <div>
        <span class="label">Over ons</span>
        <h2 class="groot" id="over-titel">Kwaliteit en service staan voorop</h2>
        <p>Bij Autoservice Barneveld draait alles om vakmanschap, transparantie en persoonlijk contact. Als zelfstandige monteur werk ik rechtstreeks met mijn klanten samen, zonder tussenpersonen. Zo weet u altijd precies wie er aan uw auto werkt. De werkplaats is uitgerust met de nieuwste apparatuur, voor regulier onderhoud én complexe diagnoses.</p>
        <ol class="stappen" aria-label="Zo werkt het">
          <li><strong>U plant een afspraak</strong><p>Online met uw kenteken via WhatsApp, of telefonisch.</p></li>
          <li><strong>U bepaalt wanneer we overleggen</strong><p>Geef bij uw afspraak aan tot welk bedrag we mogen doorwerken. Wordt het duurder, dan nemen we eerst contact met u op.</p></li>
          <li><strong>Op de hoogte via WhatsApp</strong><p>Iets onverwachts? Dan hoort u het direct, met foto's, korte filmpjes of een duidelijke toelichting.</p></li>
          <li><strong>U blijft mobiel</strong><p>Met een leenauto of leenfiets.</p></li>
        </ol>
        <a class="verder" href="over-ons/">Meer over ons <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>

{vervoer_sectie("")}

{handig_sectie()}

{review_sectie()}

{contact_sectie("", kaart=False)}
  <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "Autoservice Barneveld", "url": SITE + "/", "inLanguage": "nl-NL", "publisher": {"@id": SITE + "/#bedrijf"}}, ensure_ascii=False, indent=1)}
  </script>"""
    schrijf("index.html", pagina(
        "", "", "Garage Barneveld: APK & onderhoud | Autoservice Barneveld",
        "Universele garage in Barneveld voor APK, onderhoud, reparatie, diagnose, banden, uitlijnen en airco. Alle merken, ook elektrisch. Bel 0342-234003.",
        "home", main))


def vervoer_sectie(r, titel_h="h2", link=True):
    verder = (f'\n      <p><a class="verder" href="{r}vervangend-vervoer/">Alles over vervangend vervoer <span aria-hidden="true">→</span></a></p>'
              if link else "")
    kopje = "" if titel_h != "h2" else f"""      <div class="kopje">
        <span class="label">Vervangend vervoer</span>
        <h2 class="groot" id="vervoer-titel">Altijd mobiel</h2>
        <p>Terwijl uw auto bij ons in onderhoud of reparatie is, bieden wij verschillende mogelijkheden om uw dag zorgeloos voort te zetten.</p>
      </div>
"""
    if not kopje:
        kopje = '      <h2 class="sr-only">Onze mogelijkheden</h2>\n'
    return f"""  <section class="sectie" id="vervangend-vervoer" aria-labelledby="vervoer-titel">
    <div class="wrap">
{kopje.replace('class="sr-only"', 'class="sr-only" id="vervoer-titel"')}      <div class="vervoer-raster">
        <article class="optie">
          <span class="ico" aria-hidden="true">{I_BLIKSEM.format(s=26)}</span>
          <small>Voor particulieren</small>
          <h3>Elektrische Renault <span class="geen-breuk">5 <svg class="blad" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 3C10 3 4 8 4 15c0 1.6.4 3 1 4.2C7 14 11 10.5 16 8.5c-4 2.6-7.4 6.4-9.3 11.3 1.3.8 2.8 1.2 4.3 1.2C18 21 21 13 20 3z"/></svg><span class="sr-only"> (milieuvriendelijk)</span></span></h3>
          <p>Een moderne, duurzame en comfortabele leenauto waarmee u direct verder kunt rijden.</p>
        </article>
        <article class="optie">
          <span class="ico" aria-hidden="true"><svg width="26" height="26" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M8 7V5h8v2"/></g></svg></span>
          <small>Voor zakelijke klanten</small>
          <h3>Volkswagen Caddy</h3>
          <p>Praktisch en ruim, ideaal voor ondernemers die hun werk niet kunnen onderbreken.</p>
        </article>
        <div class="optie foto"><img src="{r}img/hero-vervangend-vervoer.webp" {srcset(r, "hero-vervangend-vervoer", "(max-width: 1060px) 100vw, 400px")} alt="Leenauto van Autoservice Barneveld in de werkplaats" width="1848" height="1232" loading="lazy"></div>
      </div>
      <ul class="extra">
        <li>{I_VINK}<span><strong>Leenfiets <svg class="blad" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20 3C10 3 4 8 4 15c0 1.6.4 3 1 4.2C7 14 11 10.5 16 8.5c-4 2.6-7.4 6.4-9.3 11.3 1.3.8 2.8 1.2 4.3 1.2C18 21 21 13 20 3z"/></svg><span class="sr-only"> (milieuvriendelijk)</span></strong>Voor korte ritten.</span></li>
        <li>{I_VINK}<span><strong>Station op 5 minuten</strong>Lopen vanaf de garage.</span></li>
        <li>{I_VINK}<span><strong>Wachtruimte</strong>Met koffie en wifi, als u even wacht.</span></li>
      </ul>{verder}
    </div>
  </section>"""


def contact_sectie(r, kaart=True, titel="Neem vandaag nog contact op", h="h2"):
    osm = ("""
        <iframe class="kaart-osm" title="Kaart: Verlengde Parallelweg 4-10, Barneveld" loading="lazy"
          src="https://www.openstreetmap.org/export/embed.html?bbox=5.5951%2C52.1606%2C5.6071%2C52.1656&amp;layer=mapnik&amp;marker=52.16313%2C5.60113"></iframe>
        <p><a class="knop blauw" href="https://www.google.com/maps/dir/?api=1&amp;destination=Verlengde+Parallelweg+4-10%2C+3771LP+Barneveld">Route plannen</a></p>"""
           if kaart else "")
    kop_html = (f'<h1 class="groot" id="contact-titel">{titel}</h1>' if h == "h1"
                else f'<h2 class="groot" id="contact-titel">{titel}</h2>')
    return f"""  <section class="sectie contact" id="contact" aria-labelledby="contact-titel">
    <div class="wrap">
      <div>
        <span class="label">Contact</span>
        {kop_html}
        <p>Heeft u vragen over onze diensten of wilt u een afspraak maken? Neem dan direct contact met ons op voor betrouwbare en professionele service.</p>
        <ul class="contact-lijst">
          <li>{I_TEL.format(s=22)}<span><span class="sr-only">Telefoon: </span><a href="{TEL_LINK}">{TEL}</a></span></li>
          <li>{I_WA}<span><span class="sr-only">WhatsApp: </span><a href="{WA_LINK}">WhatsApp {TEL}</a></span></li>
          <li>{I_MAIL}<span><span class="sr-only">E-mail: </span><a href="mailto:{MAIL}">{MAIL}</a></span></li>
          <li>{I_PIN}<span>{ADRES}<br>{POSTCODE_PLAATS}</span></li>
        </ul>
        <div class="tijden-bord">{I_KLOK}<span>Maandag t/m vrijdag 08:00–17:00<br>Zaterdag op afspraak<br>Zondag gesloten</span></div>{osm}
      </div>
      <form class="formulier" action="https://formsubmit.co/{MAIL}" method="post" aria-label="Contactformulier">
        <input type="hidden" name="_subject" value="Nieuw bericht via de website">
        <input type="hidden" name="_template" value="table">
        <div class="rij">
          <div class="veld"><label for="naam">Naam *</label><input class="invoer" id="naam" name="Naam" autocomplete="name" required></div>
          <div class="veld"><label for="tel">Telefoonnummer</label><input class="invoer" id="tel" name="Telefoonnummer" type="tel" autocomplete="tel"></div>
        </div>
        <div class="veld"><label for="mail">E-mail *</label><input class="invoer" id="mail" name="email" type="email" autocomplete="email" required></div>
        <div class="veld"><label for="bericht">Bericht *</label><textarea id="bericht" name="Bericht" required></textarea></div>
        <label class="akkoord"><input type="checkbox" required> Ik ga ermee akkoord dat deze gegevens worden opgeslagen en verwerkt met het doel contact op te nemen. Ik kan mijn toestemming op elk moment intrekken. *</label>
        <button class="knop blauw" type="submit">Versturen</button>
        <p class="formulier-melding" role="status" hidden></p>
      </form>
    </div>
  </section>"""


# ------------------------------------------------------------------ subpagina's
def tip(slug, kop, tekst):
    return f'<p class="apk-tip"><a href="{{r}}{slug}/"><strong>{kop}</strong><span>{tekst}</span></a></p>\n\n'


TIPS = {
    "onderhoud-reparatie": tip("onderhoudswijzer", "Kleine of grote beurt?", "Zie met onze onderhoudswijzer wanneer uw volgende beurt komt."),
    "diagnose": tip("dashboardlampjes", "Welk lampje brandt er?", "Zie per lampje wat het betekent en of u nog kunt doorrijden."),
    "bandenservice": tip("winterbanden", "Al tijd voor winterbanden?", "Onze bandenmeter kijkt naar de temperatuur in Barneveld voor de komende dagen."),
    "airco-service": tip("hulp/airco-koelt-niet", "Airco koelt niet of ruikt muf?", "Lees de meest voorkomende oorzaken."),
    "elektrische-auto": tip("hulp/auto-start-niet", "Elektrische auto gaat niet aan?", "Vaak is de kleine 12V-accu leeg. Lees wat u kunt doen."),
}


DIENST_VRAGEN = {
    "apk-keuring": [
        ("Hoe lang van tevoren kan ik mijn auto laten keuren?",
         "Tot twee maanden vóór de vervaldatum, zonder dat u er tijd mee verliest: de nieuwe datum wordt gerekend vanaf de oude. Uw datum ziet u met de <a href=\"{r}apk-check/\">APK-check</a>."),
        ("Wat gebeurt er als mijn auto wordt afgekeurd?",
         "Dan hoort u van ons welke punten hersteld moeten worden. Valt het herstel binnen het bedrag dat u bij uw afspraak heeft opgegeven, dan gaan we door; anders overleggen we eerst met u."),
        ("Moet een elektrische auto ook APK?",
         "Ja. Ook elektrische auto's zijn APK-plichtig, en wij keuren ze net zo goed als auto's op benzine of diesel."),
    ],
    "onderhoud-reparatie": [
        ("Wat is het verschil tussen een kleine en een grote beurt?",
         "Bij een kleine beurt verversen we olie en oliefilter en controleren we de belangrijkste onderdelen. Bij een grote beurt vervangen we ook filters zoals het lucht- en interieurfilter. Met de <a href=\"{r}onderhoudswijzer/\">onderhoudswijzer</a> ziet u wanneer uw volgende beurt komt."),
        ("Blijft mijn fabrieksgarantie geldig?",
         "Ja. Wordt het onderhoud volgens de voorschriften van de fabrikant uitgevoerd, dan blijft uw garantie gewoon geldig. U hoeft daarvoor niet naar de dealer."),
        ("Hoor ik het als er tijdens het werk iets extra's nodig is?",
         "Ja. Valt het boven het bedrag dat u heeft opgegeven, dan overleggen we eerst met u, meestal via WhatsApp met een foto of korte toelichting."),
    ],
    "diagnose": [
        ("Er brandt een oranje motorlampje. Wat nu?",
         "Brandt het continu, laat de auto dan binnenkort uitlezen. Knippert het, rijd dan rustig en laat hem direct nakijken. Meer lampjes vindt u bij <a href=\"{r}dashboardlampjes/\">dashboardlampjes</a>."),
        ("Kunnen jullie ook elektrische auto's uitlezen?",
         "Ja. Onze diagnoseapparatuur is geschikt voor alle merken, ook voor elektrische en hybride auto's."),
    ],
    "bandenservice": [
        ("Wanneer moet ik winterbanden laten monteren?",
         "Als de temperatuur structureel onder de 7 °C zakt. Onze <a href=\"{r}winterbanden/\">winterbandenmeter</a> kijkt naar de verwachting voor Barneveld."),
        ("Hoeveel profiel moet er minimaal op mijn banden?",
         "Wettelijk 1,6 mm. Wij adviseren minimaal 3 mm voor zomerbanden en 4 mm voor winter- en all-season banden. Zie ook de <a href=\"{r}bandencheck/\">bandencheck</a>."),
        ("Wanneer moet mijn auto worden uitgelijnd?",
         "Als de auto naar één kant trekt, het stuur scheef staat of de banden ongelijk slijten, en na een flinke klap tegen een stoeprand."),
    ],
    "airco-service": [
        ("Hoe vaak moet de airco worden gecontroleerd?",
         "Als vuistregel eens per twee jaar, en eerder als hij minder goed koelt, muf ruikt of als uw ruiten snel beslaan."),
        ("Waarom ruikt mijn airco muf?",
         "Meestal door bacteriën en schimmel in het systeem of een vervuild interieurfilter. Reinigen en het filter vervangen helpt. Lees meer bij <a href=\"{r}hulp/airco-koelt-niet/\">airco koelt niet of ruikt muf</a>."),
    ],
    "elektrische-auto": [
        ("Hoe vaak heeft een elektrische auto onderhoud nodig?",
         "Als vuistregel eens per jaar een controlebeurt, met aandacht voor remmen, banden, ophanging, remvloeistof, airco en de 12V-accu."),
        ("Moet ik voor onderhoud naar de dealer om mijn garantie te houden?",
         "Nee. Wordt het onderhoud volgens de voorschriften van de fabrikant uitgevoerd, dan blijft uw garantie geldig."),
    ],
}


def dienstpagina(d):
    slug, naam, title, desc, h1, foto, _alt, kort, _knop = d
    r = "../"
    andere = "\n".join(f'          <li><a href="{r}{s}/">{e(n)}</a></li>'
                       for s, n, *_ in DIENSTEN if s != slug) + f'\n          <li><a href="{r}aankoopkeuring/">Aankoopkeuring</a></li>'
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": naam, "serviceType": naam, "description": desc, "url": f"{SITE}/{slug}/",
         "areaServed": "Barneveld en omgeving",
         "provider": {"@type": "AutoRepair", "name": "Autoservice Barneveld", "url": SITE, "telephone": TEL}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": naam, "item": f"{SITE}/{slug}/"}]}]}
    if slug in DIENST_VRAGEN:
        import re as _re
        schema["@graph"].append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": _re.sub(r"<[^>]+>", "", a)}}
            for v, a in DIENST_VRAGEN[slug]]})
    main = f"""{pagina_kop(r, h1, foto, "Dienst · alle merken", kort)}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
{TIPS.get(slug, "").format(r=r)}{TEKST[slug].strip().format(r=r)}

{vragen_blok([(v, a.replace("{r}", r)) for v, a in DIENST_VRAGEN.get(slug, [])]) if slug in DIENST_VRAGEN else ""}

        <ul class="andere-diensten" aria-label="Andere diensten">
{andere}
        </ul>
      </div>
      {zijkaart(r, naam)}
    </div>
  </section>
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
  </script>"""
    schrijf(f"{slug}/index.html", pagina(r, f"{slug}/", title, desc, None, main))


def over_ons():
    r = "../"
    main = f"""{pagina_kop(r, "Meer over Autoservice Barneveld", "hero-over-ons", "Over ons", "Een zelfstandige, universele garage met een moderne werkplaats in Barneveld.")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
        <h2>Kwaliteit en service staan voorop</h2>
        <p>Bij Autoservice Barneveld draait alles om vakmanschap, transparantie en persoonlijk contact. Als zelfstandige monteur werk ik rechtstreeks met mijn klanten samen, zonder tussenpersonen of ingewikkelde processen. Zo weet u altijd precies wie er aan uw auto werkt en wat er gaat gebeuren.</p>

        <h2>Moderne werkplaats, alle merken</h2>
        <p>Mijn werkplaats is uitgerust met de nieuwste apparatuur en geschikt voor zowel regulier onderhoud als complexe diagnoses. Ik verzorg onderhoud en reparaties aan alle merken en modellen, inclusief het reguliere onderhoud van <a href="{r}elektrische-auto/">elektrische auto's</a>.</p>

        <h2>Heldere communicatie</h2>
        <p>Transparantie staat centraal in mijn werkwijze. U geeft zelf aan tot welk bedrag ik mag doorwerken; wordt het duurder, dan overleg ik eerst met u. Kom ik tijdens het werk iets onverwachts tegen? Dan houd ik u direct op de hoogte via WhatsApp, met foto's, korte filmpjes of een duidelijke toelichting.</p>

        <h2>Waarom klanten kiezen voor Autoservice Barneveld</h2>
        <p>Klanten waarderen vooral de combinatie van deskundigheid, duidelijke communicatie en een nuchtere aanpak. Waar u bij een dealer of grote garage eerst langs een receptie of serviceadviseur gaat, spreekt u bij ons direct de monteur die ook aan uw auto werkt. Dat scheelt misverstanden en wachttijd.</p>
        <p>Tegelijk biedt een zelfstandige garage dezelfde mogelijkheden als een dealer. Ik heb toegang tot alle dealersoftware en de mogelijkheid om originele onderdelen te bestellen. Daarnaast houd ik mijn kennis bij met regelmatige bijscholing en aanvullende certificaten. Omdat ik geen personeel, receptie of showroom heb, zijn de kosten lager, en dat ziet u terug in een eerlijk tarief. Kortom: u bespaart tijd, gedoe en geld.</p>

        <ol class="stappen" aria-label="Zo werkt het">
          <li><strong>U plant een afspraak</strong><p>Online met uw kenteken via WhatsApp, of telefonisch.</p></li>
          <li><strong>U bepaalt wanneer we overleggen</strong><p>Geef bij uw afspraak aan tot welk bedrag we mogen doorwerken. Wordt het duurder, dan nemen we eerst contact met u op.</p></li>
          <li><strong>Op de hoogte via WhatsApp</strong><p>Iets onverwachts? Dan hoort u het direct.</p></li>
          <li><strong>U blijft mobiel</strong><p>Met een leenauto of leenfiets, zie <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p></li>
        </ol>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("over-ons/index.html", pagina(
        r, "over-ons/", "Over ons | Autoservice Barneveld",
        "Autoservice Barneveld: zelfstandige monteur met moderne werkplaats. Vakmanschap, korte lijnen en updates via WhatsApp.",
        "over-ons", main))


def vervangend_vervoer():
    r = "../"
    main = f"""{pagina_kop(r, "Altijd mobiel met ons vervangend vervoer", "hero-vervangend-vervoer", "Vervangend vervoer", "Bij Autoservice Barneveld zorgen we ervoor dat u nooit stil hoeft te staan. Terwijl uw auto bij ons in onderhoud of reparatie is, bieden wij verschillende mogelijkheden om uw dag zorgeloos voort te zetten.")}

{vervoer_sectie(r, titel_h="geen", link=False)}

  <section class="sectie zonder-boven">
    <div class="wrap artikel">
      <div class="tekst">
        <h2>Voor particulieren en zakelijke klanten</h2>
        <p>Particulieren rijden in onze elektrische Renault 5. Zakelijke klanten kunnen de Volkswagen Caddy gebruiken, zodat het werk gewoon door kan gaan.</p>
        <p>Of u nu particulier bent of zakelijke klant, wij zorgen dat u mobiel blijft. Geef bij het plannen van uw afspraak aan welke optie u wilt gebruiken.</p>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("vervangend-vervoer/index.html", pagina(
        r, "vervangend-vervoer/", "Vervangend vervoer en leenauto Barneveld | Autoservice Barneveld",
        "Leenauto (elektrische Renault 5 of VW Caddy) of leenfiets terwijl uw auto bij ons in Barneveld staat.",
        "vervangend-vervoer", main))


def contact():
    r = "../"
    main = contact_sectie(r, kaart=True, titel="Contact en route", h="h1")
    schrijf("contact/index.html", pagina(
        r, "contact/", "Contact en route Barneveld | Autoservice Barneveld",
        "Maak een afspraak bij Autoservice Barneveld: Verlengde Parallelweg 4-10, 3771 LP Barneveld. Bel of app 0342-234003 of mail contact@autoservicebarneveld.nl.",
        "contact", main))


def privacy():
    r = "../"
    main = f"""{pagina_kop(r, "Privacyverklaring", "hero-contact")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
        <p>Autoservice Barneveld, {ADRES}, {POSTCODE_PLAATS} (KvK {KVK}), gaat zorgvuldig om met uw persoonsgegevens. In deze verklaring leest u welke gegevens we gebruiken en waarom.</p>

        <h2>Welke gegevens en waarvoor</h2>
        <p>Neemt u contact met ons op via telefoon, e-mail, WhatsApp of het contactformulier, dan gebruiken we uw naam, contactgegevens en bericht om uw vraag te beantwoorden en een afspraak te maken. Laat u werk aan uw auto uitvoeren, dan gebruiken we ook uw kenteken, kilometerstand en voertuiggegevens om de opdracht uit te voeren en te factureren.</p>
        <p>Berichten via het contactformulier worden als e-mail aan ons doorgestuurd door FormSubmit (formsubmit.co). Die dienst verwerkt daarvoor de gegevens die u invult en technische gegevens zoals uw IP-adres.</p>
        <p>Bij een APK-keuring zijn we wettelijk verplicht de uitslag aan de RDW door te geven. Facturen bewaren we zolang de fiscale bewaarplicht dat vereist.</p>

        <h2>Afspraak plannen via WhatsApp</h2>
        <p>Het afspraakformulier op deze website slaat niets op. Het zet uw kenteken (of merk en model), de gekozen werkzaamheden, eventueel uw overleggrens, kilometerstand, adres, e-mailadres en eventuele voorkeursdata in een WhatsApp-bericht, dat u daarna zelf verstuurt. Voor dat bericht gelden ook de voorwaarden van WhatsApp (Meta). Kiest u voor versturen per e-mail, dan gaan dezelfde gegevens via FormSubmit (formsubmit.co) als e-mail naar ons. Om uw straat en woonplaats bij uw postcode en huisnummer te vinden, vraagt het formulier die op bij de Basisregistratie Adressen via PDOK (Kadaster). Bij een ingevuld kenteken haalt het formulier het merk, model en de APK-vervaldatum op uit de openbare gegevens van de RDW. Bij beide wordt niets opgeslagen.</p>
        <p>De kenteken-checks op deze website (zoals de <a href="{r}apk-check/">APK-check</a> en de <a href="{r}occasion-check/">occasion-check</a>) werken op dezelfde manier: uw browser vraagt de openbare voertuiggegevens rechtstreeks op bij de RDW. Wij zien en bewaren het kenteken niet. De <a href="{r}winterbanden/">winterbandenmeter</a> haalt de weersverwachting voor Barneveld op bij Open-Meteo. Daarbij gaan alleen technische gegevens mee, zoals uw IP-adres, die nodig zijn om de verwachting te leveren.</p>

        <h2>Deze website</h2>
        <p>Deze website gebruikt geen cookies, geen analyse- of advertentiediensten en laadt geen externe lettertypes. De website wordt gehost via GitHub Pages; GitHub kan daarbij technische gegevens zoals uw IP-adres verwerken om de site te leveren en te beveiligen. De kaart op de contactpagina wordt geladen van OpenStreetMap.</p>

        <h2>Delen met anderen</h2>
        <p>We verkopen uw gegevens niet en delen ze alleen als dat nodig is voor de uitvoering van de opdracht of wettelijk verplicht is.</p>

        <h2>Uw rechten</h2>
        <p>U kunt uw gegevens inzien, laten aanpassen of laten verwijderen, voor zover we ze niet wettelijk moeten bewaren. Stuur daarvoor een e-mail naar <a href="mailto:{MAIL}">{MAIL}</a>. Bent u het niet eens met hoe we met uw gegevens omgaan, dan kunt u een klacht indienen bij de <a href="https://autoriteitpersoonsgegevens.nl/">Autoriteit Persoonsgegevens</a>.</p>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("privacy/index.html", pagina(
        r, "privacy/", "Privacyverklaring | Autoservice Barneveld",
        "Hoe Autoservice Barneveld omgaat met uw persoonsgegevens.", None, main))


def niet_gevonden():
    r = "/"
    lijst = "\n".join(f'          <li><a href="/{s}/">{e(n)}</a></li>' for s, n, *_ in DIENSTEN)
    main = f"""{pagina_kop(r, "Pagina niet gevonden", "hero-home")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
        <p>Deze pagina bestaat niet (meer). Ga naar de <a href="/">homepage</a> of kies een van onze diensten:</p>
        <ul class="andere-diensten">
{lijst}
        </ul>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("404.html", pagina(r, "404.html", "Pagina niet gevonden | Autoservice Barneveld",
                               "Deze pagina bestaat niet.", None, main, noindex=True))


# ------------------------------------------------------------------ merken, werkgebied, vragen
MERKEN = ["Volkswagen", "Toyota", "Kia", "Peugeot", "Renault", "Opel", "Ford", "Škoda",
          "Hyundai", "Volvo", "Audi", "BMW", "Mercedes-Benz", "Citroën", "Seat", "Nissan",
          "Mazda", "Suzuki", "Fiat", "Dacia", "Tesla", "MG", "BYD", "Polestar"]

PLAATSEN = [
    ("Barneveld", "Onze werkplaats staat aan de Verlengde Parallelweg. Brengt u uw auto, dan loopt u in vijf minuten naar het station."),
    ("Voorthuizen", "Vanuit Voorthuizen bent u zo bij ons. Moet uw auto langer blijven, dan rijdt u verder in een leenauto of op een leenfiets."),
    ("Kootwijkerbroek", "Voor onderhoud, APK of banden hoeft u vanuit Kootwijkerbroek niet ver te rijden."),
    ("Terschuur en Zwartebroek", "Ook vanuit Terschuur en Zwartebroek komen klanten bij ons voor onderhoud, reparatie en APK."),
    ("Garderen en Stroe", "Woont u in Garderen of Stroe? Plan uw afspraak online en gebruik ons vervangend vervoer als dat handig is."),
    ("De Glind en Lunteren", "Ook voor klanten uit De Glind en Lunteren verzorgen we onderhoud, diagnose, banden en aircoservice."),
]

VRAGEN = [
    ("Hoe maak ik een afspraak?",
     "Via de knop Plan afspraak op deze website. U vult uw kenteken (of merk en model), de werkzaamheden en uw gegevens in en verstuurt de aanvraag via WhatsApp of per e-mail. Bellen kan ook: {tel}."),
    ("Is een aanvraag via de website meteen een afspraak?",
     "Nee. U geeft uw voorkeur door en wij nemen contact op om de afspraak te bevestigen. Heeft u haast, bel dan {tel}."),
    ("Wat is het verschil met een dealer?",
     "U spreekt direct de monteur die aan uw auto werkt, zonder receptie of tussenpersoon. We hebben toegang tot alle dealersoftware en de mogelijkheid om originele onderdelen te bestellen. Omdat er geen personeel of showroom is, zijn de kosten lager. Uw fabrieksgarantie blijft gewoon geldig."),
    ("Onderhouden jullie alle merken?",
     "Ja. Wij zijn een universele, zelfstandige garage en werken aan alle merken en modellen, ook aan elektrische en hybride auto's. Zie ook <a href=\"{r}merken/\">alle merken</a>."),
    ("Blijft mijn fabrieksgarantie geldig als ik bij jullie onderhoud laat doen?",
     "Ja, zolang het onderhoud volgens de voorschriften van de fabrikant wordt uitgevoerd met geschikte onderdelen. Dat is in de Europese regels vastgelegd. Wij werken volgens het onderhoudsschema van uw auto."),
    ("Doen jullie ook elektrische auto's?",
     "Ja. Ook een elektrische auto heeft onderhoud nodig: banden, remmen, ophanging, airco en APK. Lees meer over <a href=\"{r}elektrische-auto/\">onderhoud van elektrische auto's</a>."),
    ("Wanneer verloopt mijn APK?",
     "Dat ziet u direct met onze gratis <a href=\"{r}apk-check/\">APK-check</a>: vul uw kenteken in en u ziet de vervaldatum uit de gegevens van de RDW. U kunt de keuring tot twee maanden vóór die datum laten doen zonder dat u er tijd mee verliest."),
    ("Er brandt een lampje op mijn dashboard. Kan ik doorrijden?",
     "Dat hangt af van de kleur. Bij rood is direct actie nodig, bij oranje laat u de auto binnenkort nakijken. Per lampje leest u het in onze uitleg over <a href=\"{r}dashboardlampjes/\">dashboardlampjes</a>. Twijfelt u, bel ons dan even: {tel}."),
    ("Doen jullie ook aankoopkeuringen?",
     "Ja. Wij kijken een tweedehands auto vóór de koop onafhankelijk na en vertellen u eerlijk wat we zien. Lees meer over de <a href=\"{r}aankoopkeuring/\">aankoopkeuring</a>, of check eerst zelf de APK-historie met de <a href=\"{r}occasion-check/\">occasion-check</a>."),
    ("Hoe weet ik wat het gaat kosten?",
     "U geeft bij het plannen van uw afspraak aan tot welk bedrag we mogen doorwerken. Wordt het duurder, of komen we iets onverwachts tegen, dan overleggen we eerst met u, meestal via WhatsApp met een foto of korte toelichting."),
    ("Kan ik wachten terwijl mijn auto wordt gemaakt?",
     "Ja, voor kortere klussen kunt u wachten in onze wachtruimte met koffie en wifi."),
    ("Wat als mijn auto langer moet blijven?",
     "Dan kunt u gebruikmaken van een elektrische Renault 5, een Volkswagen Caddy of een leenfiets. U kiest dit bij het plannen van uw afspraak. Zie <a href=\"{r}vervangend-vervoer/\">vervangend vervoer</a>."),
    ("Wat zijn jullie openingstijden?",
     "Maandag tot en met vrijdag van 08:00 tot 17:00. Zaterdag op afspraak, zondag gesloten."),
    ("Waar zitten jullie?",
     "Aan de {adres}, {postcode}. Het station ligt op vijf minuten lopen. Zie <a href=\"{r}contact/\">contact en route</a>."),
]


def merken():
    r = "../"
    lijst = "\n".join(f"          <li>{e(m)}</li>" for m in MERKEN)
    main = f"""{pagina_kop(r, "Onderhoud en APK voor alle automerken", "hero-home", "Alle merken", "Of u nu in een Volkswagen, Toyota, Kia of Tesla rijdt: bij Autoservice Barneveld bent u voor onderhoud, reparatie en APK aan het juiste adres.")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
        <h2>Universele garage in Barneveld</h2>
        <p>Als zelfstandige, universele garage werken we aan alle merken en modellen: benzine, diesel, hybride en volledig elektrisch. Met moderne diagnoseapparatuur lezen we ook nieuwere auto's goed uit, en we werken volgens het onderhoudsschema van de fabrikant.</p>

        <h2>Merken die we vaak onderhouden</h2>
        <ul class="merken-lijst" aria-label="Automerken">
{lijst}
        </ul>
        <p>Staat uw merk er niet bij? Dan helpen we u net zo goed. Neem gerust <a href="{r}contact/">contact</a> op.</p>

        <h2>Uw fabrieksgarantie blijft geldig</h2>
        <p>U hoeft niet naar de dealer om uw garantie te behouden. Wordt het onderhoud uitgevoerd volgens de voorschriften van de fabrikant, met geschikte onderdelen, dan blijft uw fabrieksgarantie gewoon geldig. Dat is in de Europese regels vastgelegd.</p>

        <h2>Wat we voor elk merk doen</h2>
        <p><a href="{r}onderhoud-reparatie/">Onderhoud en reparatie</a>, <a href="{r}apk-keuring/">APK-keuring</a>, <a href="{r}diagnose/">diagnose</a>, <a href="{r}bandenservice/">banden en uitlijnen</a>, <a href="{r}airco-service/">aircoservice</a> en het onderhoud van <a href="{r}elektrische-auto/">elektrische auto's</a>.</p>

        <p class="klein-noot">Autoservice Barneveld is een onafhankelijke garage en geen officiële dealer van de genoemde merken. Merknamen zijn eigendom van hun respectieve eigenaren.</p>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("merken/index.html", pagina(
        r, "merken/", "Onderhoud alle automerken Barneveld | Autoservice Barneveld",
        "Onderhoud, reparatie en APK voor alle merken in Barneveld: Volkswagen, Toyota, Kia, Peugeot, Renault, Tesla en meer. Fabrieksgarantie blijft geldig.",
        None, main))


def werkgebied():
    r = "../"
    blokken = "\n\n".join(f"        <h2>Garage voor {e(n)}</h2>\n        <p>{e(tk)}</p>" for n, tk in PLAATSEN)
    main = f"""{pagina_kop(r, "Garage voor Barneveld en omgeving", "hero-contact", "Werkgebied", "Vanuit onze werkplaats in Barneveld helpen we klanten uit de hele omgeving met onderhoud, APK, diagnose, banden, uitlijnen en airco.")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
{blokken}

        <h2>Altijd mobiel</h2>
        <p>Moet uw auto langer bij ons blijven? Dan rijdt u verder in een elektrische Renault 5 of een Volkswagen Caddy, of pakt u een leenfiets. Wachten kan ook, met koffie en wifi. Zie <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p>

        <h2>Even zelf checken</h2>
        <p>Met onze gratis <a href="{r}apk-check/">APK-check</a> ziet u direct tot wanneer uw APK geldig is. Meer checks en uitleg, zoals de <a href="{r}winterbanden/">winterbandenmeter</a> en de uitleg over <a href="{r}dashboardlampjes/">dashboardlampjes</a>, vindt u bij <a href="{r}handig/">handige checks</a>.</p>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("werkgebied/index.html", pagina(
        r, "werkgebied/", "Garage Barneveld, Voorthuizen en omgeving | Autoservice Barneveld",
        "Garage voor Barneveld, Voorthuizen, Kootwijkerbroek, Terschuur, Zwartebroek, Garderen, Stroe, De Glind en Lunteren. Onderhoud, APK en banden.",
        None, main))


def vragen():
    r = "../"
    def a(tekst):
        return tekst.format(r=r, tel=f'<a href="{TEL_LINK}">{TEL}</a>', adres=ADRES, postcode=POSTCODE_PLAATS)
    items = "\n".join(f"""        <details class="vraag">
          <summary>{e(v)}</summary>
          <p>{a(ant)}</p>
        </details>""" for v, ant in VRAGEN)
    import re as _re
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": v,
         "acceptedAnswer": {"@type": "Answer", "text": _re.sub(r"<[^>]+>", "", a(ant))}}
        for v, ant in VRAGEN]}
    main = f"""{pagina_kop(r, "Veelgestelde vragen", "hero-vervangend-vervoer", "Vragen", "Antwoorden op de vragen die we het vaakst krijgen. Staat uw vraag er niet bij? Bel of app ons gerust.")}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst vragen">
{items}
      </div>
      {zijkaart(r)}
    </div>
  </section>
  <script type="application/ld+json">
{json.dumps(faq, ensure_ascii=False, indent=1)}
  </script>"""
    schrijf("veelgestelde-vragen/index.html", pagina(
        r, "veelgestelde-vragen/", "Veelgestelde vragen | Autoservice Barneveld",
        "Antwoorden over afspraak maken, APK, fabrieksgarantie, elektrische auto's, vervangend vervoer en openingstijden bij Autoservice Barneveld.",
        None, main))


APK_VRAGEN = [
    ("Hoe lang van tevoren kan ik mijn auto APK laten keuren?",
     "U kunt uw auto tot twee maanden vóór de vervaldatum laten keuren. Uw nieuwe vervaldatum wordt dan gerekend vanaf de oude datum, zodat u geen dag verliest."),
    ("Wat gebeurt er als mijn APK verlopen is?",
     "Met een verlopen APK mag u niet de weg op. De RDW controleert dit automatisch en u kunt een boete krijgen. Plan daarom zo snel mogelijk een keuring."),
    ("Hoe vaak moet mijn auto APK?",
     "Een nieuwe auto op benzine of stroom gaat voor het eerst na vier jaar naar de APK, daarna na twee jaar en vanaf acht jaar oud elk jaar. Een auto op diesel of lpg gaat na drie jaar voor het eerst en daarna elk jaar. Voor oudere auto's en oldtimers gelden aparte regels; de APK-check toont altijd uw eigen vervaldatum."),
    ("Waar komen de gegevens vandaan?",
     "Uit de openbare voertuiggegevens van de RDW. Uw browser vraagt ze daar rechtstreeks op; wij zien en bewaren het kenteken niet."),
]


RDW_CTA = {
    "apk": ("Plan uw APK", "APK", ""),
    "occasion": ("Plan een aankoopkeuring", "Overig", "Aankoopkeuring"),
    "kenteken": ("Plan een afspraak", "", ""),
    "terugroep": ("Plan een afspraak", "", ""),
    "trekgewicht": ("Plan een afspraak", "", ""),
}


def rdw_tool(r, modus, knop):
    cta, dienst, oms = RDW_CTA[modus]
    agenda = ('\n                <button type="button" class="link-klein apk-agenda" hidden>Zet een herinnering in uw agenda</button>'
              if modus == "apk" else "")
    extra = '\n          <div class="apk-extra"></div>' if modus == "occasion" else ""
    return f"""        <form class="apk-check" data-modus="{modus}" action="./" method="get" novalidate>
          <label for="kt-{modus}">Uw kenteken</label>
          <div class="apk-check-rij">
            <div class="kenteken">
              <span class="nl" aria-hidden="true">
                {I_NL}
                NL
              </span>
              <input id="kt-{modus}" name="kenteken" data-geen-rdw placeholder="AB-123-C" maxlength="8" autocomplete="off" spellcheck="false" autocapitalize="characters" required>
            </div>
            <button class="knop oranje" type="submit">{knop} {I_PIJL}</button>
          </div>
          <p class="apk-check-melding" role="alert" hidden></p>
        </form>
        <div class="apk-uitslag" aria-live="polite" hidden>
          <div class="apk-status">
            <span class="apk-status-label"></span>
            <p class="apk-status-kop"></p>
            <div class="apk-status-uitleg"></div>
            <div class="apk-status-knoppen">
              <a class="knop blauw" href="{r}contact/" data-afspraak data-dienst="{dienst}" data-omschrijving="{oms}" data-kenteken-van="#kt-{modus}">{cta} {I_PIJL}</a>{agenda}
            </div>
          </div>{extra}
          <div class="apk-auto">
            <figure class="apk-plaatje">
              <div class="apk-svg"></div>
              <figcaption></figcaption>
            </figure>
            <div class="apk-gegevens">
              <p class="apk-naam"></p>
              <dl></dl>
            </div>
          </div>
          <p class="apk-bron">Bron: openbare voertuiggegevens van de RDW. Aan deze gegevens kunnen geen rechten worden ontleend.</p>
        </div>"""


def vragen_blok(vragen, kop="Veelgestelde vragen"):
    items = "\n".join(f"""          <details class="vraag">
            <summary>{e(v)}</summary>
            <p>{a}</p>
          </details>""" for v, a in vragen)
    return f"""        <h2>{kop}</h2>
        <div class="vragen">
{items}
        </div>"""


def tool_pagina(slug, title, desc, h1, foto, kicker, inleiding, inhoud, vragen=(), app=None, dienst="", actief=None, kruimel=None, naam=None):
    """Een pagina in de stijl van de dienstpagina's, met optioneel een tool (app) en vragen."""
    import re as _re
    r = "../" * (slug.count("/") + 1)
    graph = []
    if app:
        graph.append({"@type": "WebApplication", "name": app[0], "url": f"{SITE}/{slug}/",
                      "applicationCategory": "UtilitiesApplication", "operatingSystem": "Alle",
                      "description": app[1], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
                      "provider": {"@type": "AutoRepair", "name": "Autoservice Barneveld", "url": SITE}})
    if vragen:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": _re.sub(r"<[^>]+>", "", a)}}
            for v, a in vragen]})
    stappen = [("Home", SITE + "/")] + list(kruimel or []) + [(naam or app[0] if (naam or app) else h1, f"{SITE}/{slug}/")]
    graph.append({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": naam, "item": url} for n, (naam, url) in enumerate(stappen)]})
    schema = {"@context": "https://schema.org", "@graph": graph}
    main = f"""{pagina_kop(r, h1, foto, kicker, inleiding)}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
{inhoud.replace("{r}", r)}
{vragen_blok([(v, a.replace("{r}", r)) for v, a in vragen]) if vragen else ""}
      </div>
      {zijkaart(r, dienst)}
    </div>
  </section>
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
  </script>"""
    schrijf(f"{slug}/index.html", pagina(r, f"{slug}/", title, desc, actief, main))


def apk_check():
    r = "../"
    inhoud = rdw_tool(r, "apk", "Check APK") + """

        <h2>Keuren met behoud van uw APK-datum</h2>
        <p>U mag uw auto tot twee maanden vóór de vervaldatum laten keuren. De nieuwe vervaldatum wordt dan gerekend vanaf de oude, dus u verliest er geen dag mee. Verloopt uw APK bijvoorbeeld op 15 juni, dan kunt u vanaf 15 april keuren en blijft 15 juni de basis voor uw volgende APK.</p>

        <h2>APK laten doen in Barneveld</h2>
        <p>Autoservice Barneveld is door de RDW erkend en keurt auto's van alle merken, ook elektrische auto's. Combineer de keuring gerust met een <a href="{r}onderhoud-reparatie/">onderhoudsbeurt</a>, dan bent u in één keer klaar. Meer weten? Lees alles over onze <a href="{r}apk-keuring/">APK-keuring</a>.</p>""" + meer_checks("apk-check")
    tool_pagina("apk-check", "APK-check: wanneer verloopt mijn APK? | Autoservice Barneveld",
                "Gratis APK-check: zie met uw kenteken direct tot wanneer uw APK geldig is en vanaf wanneer u kunt keuren met behoud van uw datum. Plus de RDW-gegevens.",
                "APK-check: hoe lang is uw APK nog geldig?", "dienst-apk", "Gratis APK-check",
                "Vul uw kenteken in en zie direct tot wanneer uw APK geldig is, vanaf wanneer u kunt keuren zonder tijd te verliezen, en de openbare gegevens van uw auto.",
                inhoud, [(v, e(a)) for v, a in APK_VRAGEN],
                ("APK-check", "Zie met uw kenteken tot wanneer uw APK geldig is en vanaf wanneer u kunt keuren met behoud van de vervaldatum."),
                "APK", "apk-check")


OCCASION_VRAGEN = [
    ("Welke gegevens toont de occasion-check?",
     "De openbare gegevens van de RDW: APK-vervaldatum, gemelde gebreken en adviespunten bij eerdere APK-keuringen, het oordeel over de tellerstand, of de auto is geïmporteerd, openstaande terugroepacties en technische gegevens zoals brandstof, vermogen en gewicht."),
    ("Wat betekent het tellerstandoordeel?",
     "De RDW verzamelt kilometerstanden bij onder meer onderhoud en APK. Is de reeks logisch, dan staat er ‘Logisch’. Staat er ‘Onlogisch’ of ‘Geen oordeel’, vraag de verkoper dan om uitleg en om onderhoudsfacturen."),
    ("Zegt de check alles over de staat van de auto?",
     "Nee. Hij laat zien wat er officieel geregistreerd is. Roest, lekkages, slijtage en storingen ziet u alleen als iemand de auto echt bekijkt. Daarvoor is een <a href=\"{r}aankoopkeuring/\">aankoopkeuring</a> bedoeld."),
    ("Ziet de verkoper dat ik zijn kenteken check?",
     "Nee. De gegevens zijn openbaar en uw browser vraagt ze rechtstreeks op bij de RDW. Wij zien en bewaren het kenteken ook niet."),
]


def occasion_check():
    inhoud = rdw_tool("{r}", "occasion", "Check auto") + """

        <h2>Een tweedehands auto kopen?</h2>
        <p>Met deze check ziet u in een paar seconden wat er over de auto bekend is bij de RDW: tot wanneer de APK loopt, welke gebreken en adviespunten keurmeesters eerder hebben gemeld, of de tellerstand logisch is en of er een terugroepactie openstaat. Zo weet u vóór de bezichtiging al waar u op moet letten.</p>

        <h2>Waar let u verder op?</h2>
        <ul class="lijst-vink">
          <li>Vraag naar onderhoudsfacturen of het onderhoudsboekje.</li>
          <li>Maak een proefrit met een koude motor, ook over een stuk snelweg.</li>
          <li>Let op storingslampjes op het dashboard, zie onze uitleg over <a href="{r}dashboardlampjes/">dashboardlampjes</a>.</li>
          <li>Kijk onder de auto en in de motorruimte naar roest en lekkages.</li>
        </ul>

        <h2>Laat de auto even nakijken</h2>
        <p>Twijfelt u, of wilt u gewoon zeker zijn? Breng de auto vóór de koop even langs voor een <a href="{r}aankoopkeuring/">aankoopkeuring</a>. We bekijken hem op de brug, lezen de elektronica uit en vertellen u eerlijk wat we zien. Bij een importauto met een onduidelijke geschiedenis kan dat met een uitgebreid historierapport.</p>""" + meer_checks("occasion-check")
    tool_pagina("occasion-check", "Occasion-check: APK-historie en gebreken | Autoservice Barneveld",
                "Gratis occasion-check: zie bij een kenteken de APK-datum, eerder gemelde gebreken, tellerstand, import en terugroepacties. Handig vóór u een occasion koopt.",
                "Occasion-check: wat is er bekend over deze auto?", "dienst-diagnose", "Gratis occasion-check",
                "Een tweedehands auto op het oog? Vul het kenteken in en zie de APK-historie, gemelde gebreken, het tellerstandoordeel en meer.",
                inhoud, OCCASION_VRAGEN,
                ("Occasion-check", "Zie bij een kenteken de APK-datum, eerder gemelde gebreken, het tellerstandoordeel, import en terugroepacties."),
                "Overig")


AANKOOP_VRAGEN = [
    ("Moet de verkoper meewerken?",
     "Ja, de auto moet bij ons langs kunnen komen. Vraag de verkoper of u de auto even mag laten nakijken. Een eerlijke verkoper vindt dat meestal geen probleem; u kunt ook samen komen."),
    ("Wat kost een aankoopkeuring?",
     "Bel of app ons even, dan hoort u vooraf wat het kost."),
    ("Krijg ik garantie op de auto na een aankoopkeuring?",
     "Nee. Een aankoopkeuring is een momentopname en een advies op basis van wat we op dat moment kunnen zien en uitlezen. Het is geen garantie dat de auto vrij is van gebreken."),
]


def aankoopkeuring():
    inhoud = """        <p>Een tweedehands auto op het oog? Laat hem even door ons nakijken voordat u tekent. Een frisse blik van een monteur voorkomt dure verrassingen achteraf, en u staat sterker als u over de prijs praat.</p>

        <h2>Onafhankelijk</h2>
        <p>Autoservice Barneveld is een onafhankelijke garage. We verkopen zelf geen auto's en zijn niet verbonden aan een merk of verkoper. We hebben dus geen enkel belang bij de koop: u hoort gewoon wat we zien.</p>

        <h2>Wat we bekijken</h2>
        <ul class="lijst-vink">
          <li>Onderkant en carrosserie op de brug: roest, schade en lekkages</li>
          <li>Remmen, banden, ophanging en uitlaat</li>
          <li>Motor, koppeling of automaat, en vloeistoffen</li>
          <li>Uitlezen van de elektronica op opgeslagen storingen</li>
          <li>Verlichting, airco en de belangrijkste elektrische functies</li>
          <li>Een korte proefrit</li>
          <li>De openbare RDW-gegevens, zoals APK, tellerstand en terugroepacties</li>
        </ul>

        <h2>Twijfel over een importauto?</h2>
        <p>Komt de auto uit het buitenland en is de geschiedenis niet helemaal duidelijk? Dan vragen we bij de aankoopkeuring een uitgebreid historierapport aan van Carfax of carVertical. Daarin staan onder meer eerder geregistreerde kilometerstanden en gemelde schades, ook uit het buitenland.</p>

        <h2>Eerlijk advies</h2>
        <p>Na afloop hoort u van ons wat er goed is, wat binnenkort aandacht nodig heeft en wat dat ongeveer kost. Geen verkooppraatje, gewoon een eerlijk verhaal van de monteur zelf. Elektrisch of hybride? Ook dan kijken we graag met u mee.</p>

        <h2>Eerst zelf even checken</h2>
        <p>Met onze gratis <a href="{r}occasion-check/">occasion-check</a> ziet u vooraf al de APK-historie, gemelde gebreken en het tellerstandoordeel van de auto.</p>

        <p class="klein-noot">Een aankoopkeuring is een momentopname en een advies op basis van wat we op dat moment kunnen zien, uitlezen en tijdens de proefrit merken. Er kunnen geen rechten aan worden ontleend. Autoservice Barneveld is niet aansprakelijk voor gebreken die bij de keuring niet zichtbaar waren of later ontstaan of aan het licht komen. Een historierapport van Carfax of carVertical komt van een externe partij; voor de juistheid daarvan zijn wij niet verantwoordelijk.</p>"""
    tool_pagina("aankoopkeuring", "Aankoopkeuring tweedehands auto Barneveld | Autoservice Barneveld",
                "Laat uw tweedehands auto vóór de koop onafhankelijk nakijken in Barneveld: op de brug, uitlezen en een proefrit. Bij importauto's ook een historierapport.",
                "Aankoopkeuring: eerst laten nakijken, dan kopen", "dienst-onderhoud", "Dienst · alle merken",
                "Laat een tweedehands auto vóór de koop onafhankelijk nakijken. U hoort eerlijk wat er goed is en wat aandacht nodig heeft.",
                inhoud, AANKOOP_VRAGEN, None, "Overig", naam="Aankoopkeuring")


CHECKS = [("apk-check", "APK-check", "Tot wanneer is uw APK geldig?"),
          ("occasion-check", "Occasion-check", "APK-historie en gemelde gebreken"),
          ("kentekencheck", "Kentekencheck", "Alle gegevens van een auto"),
          ("terugroepactie-check", "Terugroepactie-check", "Staat er iets open voor uw auto?"),
          ("trekgewicht-check", "Trekgewicht-check", "Hoeveel mag uw auto trekken?")]


def meer_checks(huidig):
    items = "\n".join(f'          <li><a href="{{r}}{slug}/">{naam}</a><span>{uitleg}</span></li>'
                      for slug, naam, uitleg in CHECKS if slug != huidig)
    return f"""
        <h2>Meer gratis checks</h2>
        <ul class="check-links">
{items}
        </ul>"""


def kentekencheck():
    inhoud = rdw_tool("{r}", "kenteken", "Check kenteken") + """

        <h2>Wat ziet u bij de kentekencheck?</h2>
        <p>De openbare gegevens die de RDW over een auto bijhoudt: merk en model, kleur, brandstof, vermogen, bouwjaar, gewicht en trekgewicht, de APK-vervaldatum, het oordeel over de tellerstand, of de auto verzekerd is en of er een terugroepactie openstaat. Handig als u uw eigen auto wilt nakijken, of een auto die u wilt kopen.</p>
""" + meer_checks("kentekencheck")
    vragen = [
        ("Is de kentekencheck gratis?", "Ja. De gegevens zijn openbaar en de check kost niets. U hoeft niets in te vullen behalve het kenteken."),
        ("Kan ik zien wie de eigenaar is?", "Nee. De RDW deelt geen gegevens over de eigenaar of houder van een auto. Die zijn privé."),
        ("Waar komen de gegevens vandaan?", "Uit de openbare voertuiggegevens van de RDW. Uw browser vraagt ze daar rechtstreeks op; wij zien en bewaren het kenteken niet."),
    ]
    tool_pagina("kentekencheck", "Kentekencheck: gratis autogegevens | Autoservice Barneveld",
                "Gratis kentekencheck: zie direct merk, model, bouwjaar, brandstof, vermogen, gewicht, APK-datum en tellerstand van een auto, rechtstreeks van de RDW.",
                "Kentekencheck: alle gegevens van een auto", "dienst-diagnose", "Gratis kentekencheck",
                "Vul een kenteken in en zie direct de openbare gegevens van de auto, rechtstreeks van de RDW.",
                inhoud, vragen, ("Kentekencheck", "Zie bij een kenteken de openbare RDW-gegevens van een auto, zoals merk, model, bouwjaar, brandstof, APK-datum en tellerstandoordeel."))


def terugroepactie_check():
    inhoud = rdw_tool("{r}", "terugroep", "Check terugroepactie") + """

        <h2>Wat is een terugroepactie?</h2>
        <p>Ontdekt een fabrikant een fout aan een type auto, bijvoorbeeld aan de remmen, de airbags of de software, dan roept hij die auto's terug om de fout te verhelpen. Dat gebeurt meestal gratis, bij een merkdealer. De RDW houdt bij voor welke auto's nog een terugroepactie openstaat.</p>

        <h2>Wat moet u doen?</h2>
        <p>Meestal krijgt u als eigenaar een brief van de importeur met uitleg en een advies. Volg die op en maak een afspraak bij een dealer van uw merk. Heeft u geen brief gehad, of twijfelt u wat het betekent? Bel of app ons gerust, dan zoeken we het samen uit. Uw gewone onderhoud en APK kunt u gewoon bij ons blijven doen.</p>
""" + meer_checks("terugroepactie-check")
    vragen = [
        ("Kost een terugroepactie geld?", "Nee, een terugroepactie wordt in de regel kosteloos uitgevoerd door een dealer van het merk."),
        ("Ik heb de auto tweedehands gekocht. Geldt het dan ook?", "Ja. De terugroepactie hoort bij de auto, niet bij de eigenaar. Ook als u de auto later heeft gekocht, kunt u hem laten uitvoeren."),
        ("Waar komen de gegevens vandaan?", "Uit de openbare voertuiggegevens van de RDW. Uw browser vraagt ze daar rechtstreeks op; wij zien en bewaren het kenteken niet."),
    ]
    tool_pagina("terugroepactie-check", "Terugroepactie-check op kenteken | Autoservice Barneveld",
                "Gratis terugroepactie-check: zie met uw kenteken of er voor uw auto een terugroepactie openstaat, en wat u dan moet doen. Rechtstreeks uit de RDW-gegevens.",
                "Terugroepactie-check: staat er iets open voor uw auto?", "dienst-onderhoud", "Gratis terugroepactie-check",
                "Vul uw kenteken in en zie direct of er volgens de RDW een terugroepactie openstaat voor uw auto.",
                inhoud, vragen, ("Terugroepactie-check", "Zie met uw kenteken of er volgens de RDW een terugroepactie openstaat voor uw auto."))


def trekgewicht_check():
    inhoud = rdw_tool("{r}", "trekgewicht", "Check trekgewicht") + """

        <h2>Geremd en ongeremd</h2>
        <p>Een caravan of grotere aanhanger heeft meestal eigen remmen: dan geldt het geremde trekgewicht. Een lichte aanhanger zonder remmen mag niet zwaarder zijn dan het ongeremde trekgewicht. Het gaat steeds om het gewicht van de aanhanger zoals u hem trekt, dus inclusief lading.</p>

        <h2>Welk rijbewijs heeft u nodig?</h2>
        <p>Met rijbewijs B mag u een aanhanger trekken met een toegestane maximummassa tot 750 kg. Is de aanhanger zwaarder, dan mogen auto en aanhanger samen niet zwaarder zijn dan 3.500 kg (toegestane maximummassa). Is de combinatie zwaarder, dan heeft u code 96 op uw rijbewijs nodig (tot 4.250 kg) of rijbewijs BE. Kijk voor de precieze regels bij het CBR.</p>

        <h2>Op vakantie met de caravan?</h2>
        <p>Laat uw auto vóór vertrek even nakijken: banden, remmen, verlichting en vloeistoffen. Dan rijdt u met een gerust hart weg. <a href="{r}onderhoud-reparatie/">Meer over onderhoud</a>.</p>
""" + meer_checks("trekgewicht-check")
    vragen = [
        ("Waar staat het trekgewicht van mijn auto?", "Op het kentekenbewijs en in de gegevens van de RDW. Met deze check ziet u het direct bij uw kenteken."),
        ("Er staat geen trekgewicht bij mijn auto. Wat nu?", "Dan is er voor deze auto geen trekgewicht geregistreerd en mag u in principe geen aanhanger trekken. Twijfelt u? Vraag het ons gerust."),
        ("Waar komen de gegevens vandaan?", "Uit de openbare voertuiggegevens van de RDW. Uw browser vraagt ze daar rechtstreeks op; wij zien en bewaren het kenteken niet."),
    ]
    tool_pagina("trekgewicht-check", "Trekgewicht-check op kenteken | Autoservice Barneveld",
                "Gratis trekgewicht-check: zie met uw kenteken hoeveel uw auto geremd en ongeremd mag trekken, plus uitleg over caravan, aanhanger en rijbewijs.",
                "Trekgewicht-check: hoeveel mag uw auto trekken?", "dienst-banden", "Gratis trekgewicht-check",
                "Caravan of aanhanger? Vul uw kenteken in en zie direct het geremde en ongeremde trekgewicht van uw auto.",
                inhoud, vragen, ("Trekgewicht-check", "Zie met uw kenteken hoeveel uw auto geremd en ongeremd mag trekken."))


LAMPJES = [
    ("rood", "Rood: direct actie nodig", [
        ("Oliedruk", "Een oliekannetje met een druppel.",
         "De oliedruk is te laag. Zonder goede smering kan de motor binnen korte tijd ernstig beschadigd raken.",
         "Stop zodra het veilig kan en zet de motor uit. Controleer het oliepeil met de peilstok. Rijd niet verder, maar bel ons of de pechhulp."),
        ("Koelvloeistof / motortemperatuur", "Een thermometer in golven.",
         "De motor wordt te warm, vaak door te weinig koelvloeistof of een probleem met de koeling.",
         "Stop en laat de motor afkoelen. Open het koelvloeistofreservoir niet als de motor nog heet is. Rijd niet door met dit lampje."),
        ("Remsysteem", "Een uitroepteken in een cirkel, soms met het woord BRAKE.",
         "De handrem staat nog aan, of er is iets mis met de remmen, bijvoorbeeld te weinig remvloeistof.",
         "Controleer eerst de handrem. Gaat het lampje niet uit, rijd dan niet verder en laat de remmen nakijken."),
        ("Accu / laadstroom", "Een accu met een plus en een min.",
         "De accu wordt niet meer opgeladen, meestal door de dynamo of een defecte V-snaar. De auto rijdt op de accu tot die leeg is.",
         "Zet onnodige verbruikers uit (airco, verwarming, radio) en rijd rechtstreeks naar ons of naar een veilige plek. Bel ons gerust even."),
        ("Airbag", "Een zittend poppetje met een bal ervoor.",
         "Er is een storing in het airbagsysteem. Bij een aanrijding werken de airbags mogelijk niet.",
         "U kunt meestal doorrijden, maar laat het snel uitlezen. Dit gaat om uw veiligheid."),
    ]),
    ("oranje", "Oranje: binnenkort laten nakijken", [
        ("Motorstoring", "Een motorblokje, soms met het woord CHECK.",
         "De motorelektronica heeft een storing opgeslagen, bijvoorbeeld van een sensor, de ontsteking of de uitlaatgasreiniging.",
         "Brandt hij continu, laat de auto dan binnenkort uitlezen. Knippert hij, rijd dan rustig en laat hem direct nakijken: dat kan op een ernstigere storing wijzen."),
        ("ABS", "De letters ABS in een cirkel.",
         "Het antiblokkeersysteem werkt niet. Gewoon remmen werkt nog wel, maar bij hard remmen kunnen de wielen blokkeren.",
         "Rijd voorzichtig, houd meer afstand en laat het binnenkort nakijken."),
        ("Bandenspanning", "Een doorsnede van een band met een uitroepteken.",
         "De spanning van een of meer banden is te laag, of een sensor geeft een storing.",
         "Controleer en pomp de banden op tot de juiste spanning (zie de sticker in de deurstijl of het tankklepje). Gaat het lampje niet uit, laat het nakijken."),
        ("ESP / tractiecontrole", "Een autootje met slingerende strepen.",
         "Knippert hij kort tijdens het rijden, dan grijpt het systeem in omdat de auto dreigt te slippen. Dat is normaal. Blijft hij branden, dan is er een storing.",
         "Blijft het lampje branden, rijd dan voorzichtig en laat het uitlezen."),
        ("Voorgloeien (diesel)", "Een spiraaltje.",
         "Bij het starten van een diesel brandt hij even: dat is normaal. Knippert of brandt hij tijdens het rijden, dan is er een storing in de motorregeling.",
         "Laat de auto binnenkort uitlezen."),
        ("Roetfilter (diesel)", "Een rechthoek met puntjes erin.",
         "Het roetfilter raakt vol. Dat gebeurt vooral bij veel korte ritten.",
         "Een stuk doorrijden op de snelweg helpt vaak om het filter schoon te branden. Gaat het lampje niet uit, laat het dan nakijken."),
        ("AdBlue (diesel)", "Een vulopening met een druppel, soms met de tekst AdBlue.",
         "Het AdBlue-niveau is laag.",
         "Vul AdBlue bij. Raakt het helemaal op, dan kan de auto na het afzetten niet meer starten."),
        ("Stuurbekrachtiging", "Een stuurtje met een uitroepteken.",
         "Er is een storing in de stuurbekrachtiging. Sturen kan zwaarder gaan.",
         "Rijd voorzichtig en laat het snel nakijken. Is het lampje rood, rijd dan liever niet verder."),
        ("Onderhoud", "Een moersleuteltje, soms met het woord SERVICE.",
         "Volgens de auto is het tijd voor een onderhoudsbeurt.",
         "Plan een beurt in. Na het onderhoud zetten wij de melding weer terug."),
    ]),
    ("groen", "Groen of blauw: ter informatie", [
        ("Grootlicht", "Een blauwe koplamp met rechte strepen.",
         "Uw grootlicht staat aan.", "Zet het uit bij tegenliggers en voorliggers."),
        ("Mistlicht", "Een lamp met golvende streep: groen voor, oranje achter.",
         "Uw mistlampen staan aan.", "Mistachterlicht alleen bij zicht onder de 50 meter, anders verblindt u anderen."),
        ("Cruise control", "Een snelheidsmeter met een pijltje.",
         "De cruise control staat aan.", "Niets aan de hand."),
    ]),
]


def dashboardlampjes():
    blokken = []
    for kleur, kop, lijst in LAMPJES:
        items = "\n".join(f"""          <details class="lampje">
            <summary><span class="lampje-stip {kleur}" aria-hidden="true"></span>{e(naam)}<small>{e(teken)}</small></summary>
            <p><strong>Wat betekent het?</strong> {e(wat)}</p>
            <p><strong>Wat doet u?</strong> {e(doen)}</p>
          </details>""" for naam, teken, wat, doen in lijst)
        blokken.append(f"""        <h2>{kop}</h2>
        <div class="lampjes">
{items}
        </div>""")
    inhoud = """        <p>Een lampje op het dashboard zegt iets over de staat van uw auto. De kleur vertelt hoe dringend het is. Hieronder leest u per lampje wat het betekent en wat u het beste kunt doen. De symbolen verschillen soms per merk; kijk bij twijfel in het instructieboekje of bel ons even.</p>
        <ul class="lampjes-legenda">
          <li><span class="lampje-stip rood" aria-hidden="true"></span><strong>Rood</strong> direct actie nodig, vaak stoppen zodra het veilig kan</li>
          <li><span class="lampje-stip oranje" aria-hidden="true"></span><strong>Oranje</strong> binnenkort laten nakijken</li>
          <li><span class="lampje-stip groen" aria-hidden="true"></span><strong>Groen of blauw</strong> ter informatie</li>
        </ul>

""" + "\n\n".join(blokken) + """

        <h2>Lampje laten uitlezen</h2>
        <p>Brandt er een lampje en weet u niet precies wat er aan de hand is? Met onze <a href="{r}diagnose/">diagnoseapparatuur</a> lezen we de opgeslagen storing uit en zoeken we de oorzaak. Dat geldt voor alle merken, ook elektrische auto's.</p>"""
    vragen = [
        ("Mag ik doorrijden met een oranje lampje?", "Meestal wel, maar laat de auto binnenkort nakijken. Bij een rood lampje is direct actie nodig; vaak moet u dan stoppen zodra het veilig kan."),
        ("Het lampje is vanzelf weer uitgegaan. Moet ik iets doen?", "De storing staat vaak nog wel in het geheugen van de auto. Laat het bij de volgende gelegenheid even uitlezen, zeker als het vaker gebeurt."),
        ("Kan ik een storing zelf wissen?", "Wissen haalt alleen het lampje weg, niet de oorzaak. Komt het lampje terug, dan is er nog iets aan de hand."),
    ]
    tool_pagina("dashboardlampjes", "Dashboardlampje: wat betekent het? | Autoservice Barneveld",
                "Wat betekent het lampje op uw dashboard? Uitleg per kleur: motorstoring, oliedruk, accu, remmen, ABS, bandenspanning, roetfilter en wat u moet doen.",
                "Dashboardlampjes: wat betekent dit lampje?", "dienst-diagnose", "Uitleg",
                "Rood, oranje of groen: zo weet u wat een lampje betekent en of u nog kunt doorrijden.",
                inhoud, vragen, None, "Diagnose", naam="Dashboardlampjes")


def winterbanden():
    inhoud = """        <div class="weer-meter" id="weer-meter" aria-live="polite">
          <p class="weer-laden">De weersverwachting voor Barneveld wordt geladen…</p>
        </div>

        <h2>De 7-gradenregel</h2>
        <p>Winterbanden zijn gemaakt van een zachter rubber dat ook bij kou soepel blijft. Daardoor hebben ze onder de 7 °C meer grip dan zomerbanden, ook op een droge weg. Zakt de temperatuur in het najaar structureel onder de 7 graden, dan is het tijd om te wisselen. Stijgt hij in het voorjaar weer structureel boven de 7 graden, dan kunnen de zomerbanden er weer onder. De meter hierboven kijkt daarvoor naar de verwachting voor de komende dagen in Barneveld.</p>

        <h2>All-season banden</h2>
        <p>Liever niet twee keer per jaar wisselen? All-season banden zijn een goed alternatief voor de meeste rijders in Nederland. Kies dan banden met het bergsymbool met sneeuwvlok (3PMSF): die zijn ook in landen met een winterbandenplicht toegestaan.</p>

        <h2>Op wintersport?</h2>
        <p>In Nederland zijn winterbanden niet verplicht. In onder meer Duitsland en Oostenrijk wel, bij winterse omstandigheden. Kijk voor de regels van uw vakantieland bij de ANWB, en houd minimaal 4 mm profiel aan.</p>

        <h2>Banden laten wisselen</h2>
        <p>Wij wisselen uw banden snel en vakkundig en controleren meteen het profiel, de spanning en eventuele schade. <a href="{r}bandenservice/">Meer over onze bandenservice</a> of bekijk onze <a href="{r}bandencheck/">bandencheck</a>.</p>"""
    vragen = [
        ("Wanneer moet ik winterbanden onder mijn auto zetten?", "Als de temperatuur structureel onder de 7 °C zakt, meestal ergens tussen half oktober en eind november. In het voorjaar wisselt u terug als het structureel boven de 7 °C blijft."),
        ("Zijn winterbanden verplicht in Nederland?", "Nee. In Nederland niet, in onder meer Duitsland en Oostenrijk wel bij winterse omstandigheden."),
        ("Hoeveel profiel moeten winterbanden hebben?", "Wettelijk minimaal 1,6 mm, maar voor winterbanden adviseren we minimaal 4 mm. Daaronder nemen de grip op sneeuw en natte wegen sterk af."),
    ]
    tool_pagina("winterbanden", "Winterbanden: al tijd om te wisselen? | Autoservice Barneveld",
                "Is het tijd voor winterbanden? Bekijk de temperatuurverwachting voor Barneveld en de 7-gradenregel. Plus uitleg over all-season banden en wintersport.",
                "Winterbanden: is het al tijd om te wisselen?", "dienst-banden", "Bandenmeter",
                "Volgens de 7-gradenregel: onze meter kijkt naar de temperatuur in Barneveld voor de komende dagen.",
                inhoud, vragen, ("Winterbandenmeter", "Ziet aan de hand van de weersverwachting voor Barneveld of het tijd is voor winterbanden of zomerbanden."),
                "Bandenservice")


def bandencheck():
    inhoud = """        <form class="banden-tool" id="banden-maat" novalidate>
          <label for="bandmaat">Bandenmaat <small>zoals op de zijkant van uw band, bijv. 205/55 R16 91V</small></label>
          <div class="banden-rij">
            <input class="invoer" id="bandmaat" placeholder="205/55 R16 91V" autocomplete="off" spellcheck="false">
            <button class="knop blauw" type="submit">Bekijk uitleg</button>
          </div>
          <dl class="banden-uitleg" hidden></dl>
        </form>

        <form class="banden-tool" id="banden-dot" novalidate>
          <label for="dotcode">Hoe oud is uw band? <small>de 4 cijfers aan het eind van de DOT-code op de zijkant, bijv. 2321</small></label>
          <div class="banden-rij">
            <input class="invoer" id="dotcode" placeholder="2321" inputmode="numeric" maxlength="24" autocomplete="off">
            <button class="knop blauw" type="submit">Bereken</button>
          </div>
          <p class="banden-uitleg" hidden></p>
        </form>

        <h2>Profieldiepte</h2>
        <p>Wettelijk moet er minimaal 1,6 mm profiel op uw banden zitten. Voor een goede grip op natte wegen adviseren we 3 mm voor zomerbanden en 4 mm voor winter- en all-season banden. In de groeven van de band zitten kleine verhogingen, de slijtage-indicatoren: zit het profiel daarop gelijk, dan is de band op.</p>

        <h2>Bandenspanning</h2>
        <p>De juiste spanning vindt u op een sticker in de deurstijl, in het tankklepje of in het instructieboekje. Controleer hem eens per maand bij koude banden. Een te lage spanning kost brandstof, slijt de band sneller en verlengt de remweg.</p>

        <h2>Het bandenlabel</h2>
        <p>Op elke nieuwe band zit een Europees label. Daarop ziet u het rolgeluid (in decibel), de grip op een natte weg en de rolweerstand, van klasse A (best) tot E. Een betere rolweerstand scheelt brandstof of, bij een elektrische auto, actieradius.</p>

        <h2>Nieuwe banden nodig?</h2>
        <p>We adviseren u graag over de juiste band voor uw auto en rijstijl, ook voor elektrische auto's. <a href="{r}bandenservice/">Meer over onze bandenservice</a>. Twijfelt u over winterbanden? Kijk op onze <a href="{r}winterbanden/">winterbandenmeter</a>.</p>"""
    vragen = [
        ("Hoe lees ik de bandenmaat?", "Bij 205/55 R16 91V is 205 de breedte in millimeter, 55 de hoogte van de zijwand als percentage van de breedte, R staat voor radiaalband, 16 is de velgdiameter in inch, 91 de draagkracht (615 kg per band) en V de maximumsnelheid (240 km/u)."),
        ("Hoe oud mag een band zijn?", "Rubber veroudert, ook als u weinig rijdt. Let vanaf zes jaar extra op scheurtjes. Veel fabrikanten adviseren banden van tien jaar of ouder te vervangen, ook als er nog profiel op zit."),
        ("Wat is de minimale profieldiepte?", "Wettelijk 1,6 mm. Wij adviseren minimaal 3 mm voor zomerbanden en 4 mm voor winter- en all-season banden."),
    ]
    tool_pagina("bandencheck", "Bandencheck: maat, leeftijd en profiel | Autoservice Barneveld",
                "Wat betekent de bandenmaat op uw band, hoe oud is uw band (DOT-code) en hoeveel profiel moet erop? Gratis bandencheck met heldere uitleg.",
                "Bandencheck: maat, leeftijd en profiel", "dienst-banden", "Gratis bandencheck",
                "Vul de bandenmaat of DOT-code in en zie direct wat het betekent. Met uitleg over profiel, spanning en het bandenlabel.",
                inhoud, vragen, ("Bandencheck", "Legt de bandenmaat en DOT-code van een band uit, met leeftijd, draagvermogen en maximumsnelheid."),
                "Bandenservice")


def onderhoudswijzer():
    inhoud = """        <form class="banden-tool wijzer" id="wijzer" novalidate>
          <fieldset>
            <legend>Waar rijdt uw auto op?</legend>
            <div class="wijzer-keuzes">
              <label><input type="radio" name="aandrijving" value="brandstof" checked><span>Benzine of diesel</span></label>
              <label><input type="radio" name="aandrijving" value="hybride"><span>Hybride</span></label>
              <label><input type="radio" name="aandrijving" value="elektrisch"><span>Elektrisch</span></label>
            </div>
          </fieldset>
          <div class="wijzer-rij">
            <div>
              <label for="w-km">Kilometers per jaar</label>
              <select class="invoer" id="w-km">
                <option value="8000">Minder dan 10.000</option>
                <option value="15000" selected>10.000 tot 20.000</option>
                <option value="25000">20.000 tot 30.000</option>
                <option value="35000">Meer dan 30.000</option>
              </select>
            </div>
            <div>
              <label for="w-datum">Vorige beurt <small>maand en jaar</small></label>
              <input class="invoer" id="w-datum" type="month">
            </div>
          </div>
          <fieldset>
            <legend>Wat was de vorige beurt?</legend>
            <div class="wijzer-keuzes">
              <label><input type="radio" name="vorige" value="klein"><span>Kleine beurt</span></label>
              <label><input type="radio" name="vorige" value="groot"><span>Grote beurt</span></label>
              <label><input type="radio" name="vorige" value="" checked><span>Weet ik niet</span></label>
            </div>
          </fieldset>
          <button class="knop oranje" type="submit">Bekijk advies {I_PIJL}</button>
          <div class="apk-status wijzer-uitslag" aria-live="polite" hidden>
            <span class="apk-status-label"></span>
            <p class="apk-status-kop"></p>
            <div class="apk-status-uitleg"></div>
            <div class="apk-status-knoppen"><a class="knop blauw" href="{r}contact/" data-afspraak data-dienst="Onderhoudsbeurt">Plan uw beurt {I_PIJL}</a></div>
          </div>
        </form>
        <p class="apk-bron">Dit is een vuistregel. Het onderhoudsschema van uw auto (in het boekje of de app van het merk) is altijd leidend.</p>

        <h2>Kleine of grote beurt: wat is het verschil?</h2>
        <p>Bij een <strong>kleine beurt</strong> verversen we de motorolie en het oliefilter en controleren we de belangrijkste onderdelen: remmen, banden, verlichting, vloeistoffen, ophanging en uitlaat. Bij een <strong>grote beurt</strong> doen we dat ook, en vervangen we daarnaast filters zoals het luchtfilter, het interieurfilter en, afhankelijk van de auto, het brandstoffilter of de bougies. We kijken dan ook uitgebreider naar onder meer de aandrijfriemen en de remvloeistof.</p>

        <h2>Hoe vaak onderhoud?</h2>
        <p>Als vuistregel krijgt een auto op benzine of diesel elk jaar of elke 15.000 km een beurt, wat het eerst komt, afwisselend klein en groot. Rijdt u veel, dan komt u dus vaker. Een elektrische auto heeft geen olie en minder slijtende delen, maar remmen, banden, ophanging en remvloeistof vragen nog steeds aandacht; daarvoor is een jaarlijkse controlebeurt verstandig. Meer over <a href="{r}elektrische-auto/">onderhoud van elektrische auto's</a>.</p>

        <h2>Uw garantie blijft geldig</h2>
        <p>U hoeft voor onderhoud niet naar de dealer. Wordt het onderhoud volgens de voorschriften van de fabrikant uitgevoerd, dan blijft uw fabrieksgarantie geldig. <a href="{r}merken/">Lees meer</a>.</p>""".replace("{I_PIJL}", I_PIJL)
    vragen = [
        ("Wat is het verschil tussen een APK en een onderhoudsbeurt?", "De APK is een wettelijke keuring op veiligheid en milieu. Bij een onderhoudsbeurt houden we de auto in goede staat, zodat hij betrouwbaar blijft en slijtage op tijd wordt ontdekt. Ze laten zich goed combineren."),
        ("Er brandt een moersleuteltje op mijn dashboard. Wat betekent dat?", "Dat is de onderhoudsmelding: volgens de auto is het tijd voor een beurt. Na het onderhoud zetten wij de melding terug. Zie ook onze uitleg over <a href=\"{r}dashboardlampjes/\">dashboardlampjes</a>."),
        ("Wat als ik een beurt heb overgeslagen?", "Geen paniek. Plan gewoon een beurt in; wij kijken wat er nodig is om weer bij te zijn."),
    ]
    tool_pagina("onderhoudswijzer", "Kleine of grote beurt? Onderhoudswijzer | Autoservice Barneveld",
                "Wanneer is uw volgende onderhoudsbeurt, en wordt het een kleine of grote? Gratis onderhoudswijzer met uitleg over het verschil, ook voor elektrisch.",
                "Onderhoudswijzer: kleine of grote beurt?", "dienst-onderhoud", "Gratis onderhoudswijzer",
                "Vul in wanneer uw vorige beurt was en hoeveel u rijdt, en zie wanneer de volgende beurt komt.",
                inhoud, vragen, ("Onderhoudswijzer", "Geeft een vuistregel voor wanneer de volgende onderhoudsbeurt komt en of het een kleine of grote beurt is."),
                "Onderhoudsbeurt")


KLACHTEN = [
    ("remmen-piepen", "Remmen piepen of schuren", "Remmen piepen of schuren: oorzaken en wat te doen",
     "Piepen of schuren uw remmen? Lees de meest voorkomende oorzaken, of u nog kunt doorrijden en wanneer u de remmen moet laten nakijken.",
     "dienst-onderhoud", "Reparatie",
     "Piepende of schurende remmen zijn vervelend, en soms een teken dat er iets aan de hand is. Niet elk geluid is een probleem, maar remmen zijn te belangrijk om te laten zitten.",
     [("Roest na regen of stilstaan", "Een dun laagje roest op de remschijven geeft de eerste keren remmen een schurend of piepend geluid. Verdwijnt het na een paar keer remmen, dan is er niets aan de hand."),
      ("Versleten remblokken", "Veel remblokken hebben een slijtagestrip die gaat piepen als het blok bijna op is. Hoort u een metalen, schurend geluid, dan is het blok mogelijk al tot op het metaal versleten."),
      ("Vuil of een steentje", "Een steentje of vuil tussen blok en schijf geeft een continu krassend geluid, ook als u niet remt."),
      ("Ongelijke remschijven", "Trilt het stuur of het rempedaal bij het remmen, dan zijn de remschijven vaak ongelijk versleten.")],
     "Gaat het piepen na een paar keer remmen weg, dan kunt u gewoon doorrijden. Hoort u schuren, voelt het rempedaal anders of remt de auto minder goed? Laat het dan zo snel mogelijk nakijken.",
     "We controleren remblokken, remschijven, remklauwen en remvloeistof, en vertellen u eerlijk wat nodig is en wat nog even kan."),
    ("auto-trekt-scheef", "Auto trekt naar links of rechts", "Auto trekt naar links of rechts: oorzaken",
     "Trekt uw auto naar links of rechts, of staat het stuur scheef? Lees de oorzaken, zoals bandenspanning, uitlijning of de remmen, en wat u eraan kunt doen.",
     "dienst-banden", "Uitlijnen",
     "Trekt uw auto naar één kant terwijl u rechtdoor rijdt, of staat het stuur scheef? Een licht trekken naar rechts kan door de bolling van de weg komen. Is het duidelijk merkbaar, dan zit de oorzaak meestal in de banden, de uitlijning of de ophanging.",
     [("Bandenspanning", "Een zachte band links of rechts laat de auto trekken. Controleer eerst de spanning van alle banden."),
      ("Uitlijning", "Na een klap tegen een stoeprand of door een diepe kuil kan de wieluitlijning verlopen. De auto trekt dan, het stuur staat scheef en de banden slijten ongelijk."),
      ("Versleten ophanging", "Speling in draagarmen, rubbers of stuurkogels kan de auto laten trekken, vaak samen met een onrustig stuur."),
      ("Een vastzittende rem", "Trekt de auto vooral na het remmen naar één kant, of wordt één wiel warm? Dan kan een remklauw blijven hangen.")],
     "U kunt meestal voorzichtig doorrijden, maar laat het binnenkort nakijken. Trekt de auto sterk of wordt een wiel heet, rijd dan liever niet verder.",
     "We controleren banden, ophanging en remmen en meten de uitlijning nauwkeurig op. Lees meer over <a href=\"{r}bandenservice/\">uitlijnen</a>."),
    ("stuur-trilt", "Stuur trilt tijdens het rijden", "Stuur trilt tijdens het rijden: oorzaken",
     "Trilt uw stuur bij een bepaalde snelheid of tijdens het remmen? Lees de meest voorkomende oorzaken, van onbalans tot remschijven.",
     "dienst-banden", "Bandenservice",
     "Een trillend stuur is vervelend en vermoeiend. Het moment waarop het stuur trilt, zegt veel over de oorzaak.",
     [("Wielen uit balans", "Trilt het stuur vooral tussen ongeveer 80 en 120 km/u, dan zijn de wielen vaak uit balans. Balanceren lost dat meestal snel op."),
      ("Schade aan band of velg", "Een bult in de band of een kromme velg na een klap geeft trillingen bij elke snelheid."),
      ("Remschijven", "Trilt het alleen tijdens het remmen, dan zijn de remschijven waarschijnlijk ongelijk versleten."),
      ("Ophanging of aandrijving", "Speling in de ophanging of een versleten aandrijfas kan ook trillingen geven, vaak bij optrekken.")],
     "U kunt meestal doorrijden, maar laat het nakijken. Ziet u een bult in de band, rijd dan rustig en laat de band zo snel mogelijk vervangen.",
     "We controleren banden en velgen, balanceren de wielen en kijken naar remmen en ophanging. Lees meer over onze <a href=\"{r}bandenservice/\">bandenservice</a>."),
    ("auto-start-niet", "Auto start niet", "Auto start niet of accu leeg: oorzaken",
     "Start uw auto niet, of hoort u alleen een klik? Lees de meest voorkomende oorzaken, zoals een lege accu, en wat u zelf kunt doen. Ook voor elektrische auto's.",
     "dienst-diagnose", "Diagnose",
     "Draait de motor niet, hoort u alleen een klik of start de auto heel moeizaam? Meestal ligt het aan de accu, zeker in de winter.",
     [("Lege of oude accu", "Kou, veel korte ritten of een accu van vijf jaar of ouder: dan heeft de accu vaak niet genoeg kracht meer. De startmotor draait traag of u hoort alleen klikken."),
      ("Dynamo", "Laadt de dynamo de accu niet op, dan is de accu na een tijdje leeg. Vaak brandt dan eerst het accu-lampje tijdens het rijden."),
      ("Startmotor", "Is de accu goed maar gebeurt er niets of hoort u één klik, dan kan de startmotor defect zijn."),
      ("Sleutel of startonderbreker", "Een lege batterij in de sleutel of een storing in de startonderbreker kan het starten blokkeren."),
      ("Elektrische auto: de 12V-accu", "Ook een elektrische auto heeft een kleine 12V-accu. Is die leeg, dan gaat de auto niet aan, ook al is de grote accu vol.")],
     "Met startkabels of een startbooster komt u vaak weer op gang. Gaat het daarna opnieuw mis, laat de accu en de dynamo dan testen.",
     "We testen de accu en het laadsysteem, en lezen bij twijfel de auto uit. Lees meer over <a href=\"{r}diagnose/\">diagnose</a>."),
    ("airco-koelt-niet", "Airco koelt niet of ruikt muf", "Airco koelt niet of ruikt muf: oorzaken",
     "Koelt uw auto-airco niet meer goed, of ruikt het muf? Lees de oorzaken, zoals te weinig koudemiddel of een vervuild filter, en wat eraan te doen is.",
     "dienst-airco", "Aircoservice",
     "Een airco die niet meer koelt of een muffe lucht uit de roosters: het komt veel voor en is meestal goed op te lossen.",
     [("Te weinig koudemiddel", "Een airco verliest ieder jaar een beetje koudemiddel. Na een paar jaar koelt hij merkbaar minder. Gaat het snel, dan is er mogelijk een lek."),
      ("Compressor of ventilator", "Blijft de lucht warm, ook na bijvullen, dan kan de compressor, de koppeling ervan of de ventilator defect zijn."),
      ("Vervuild interieurfilter", "Een vol interieurfilter geeft minder luchtstroom en kan muf ruiken."),
      ("Bacteriën op de verdamper", "Een muffe of zure lucht komt vaak van bacteriën en schimmel in het aircosysteem. Reinigen helpt.")],
     "U kunt gewoon doorrijden. Gebruik de airco ook in de winter af en toe: dat houdt het systeem soepel en droogt de lucht, zodat uw ruiten minder beslaan.",
     "We controleren het systeem, vullen het koudemiddel bij, sporen lekkages op en reinigen of vervangen het filter. Lees meer over onze <a href=\"{r}airco-service/\">aircoservice</a>."),
    ("geluid-bij-drempels", "Geluid bij drempels of sturen", "Klunkend of krakend geluid bij drempels of sturen",
     "Hoort u een klunk bij drempels, of kraakt of tikt het bij het sturen? Lees welke onderdelen van de ophanging en besturing de oorzaak kunnen zijn.",
     "dienst-onderhoud", "Reparatie",
     "Een klunk bij een drempel, gekraak bij het sturen of getik in een bocht: geluiden uit de ophanging nemen meestal langzaam toe. Hoe eerder u het laat bekijken, hoe kleiner de reparatie vaak is.",
     [("Draagarmen en rubbers", "Versleten rubbers of kogels in de draagarmen geven een klunk bij drempels en een onrustig stuurgedrag. Bij zware auto's, zoals elektrische auto's, slijten ze sneller."),
      ("Stabilisatorstangen", "Een ratelend of klepperend geluid over oneffenheden komt vaak van de stabilisatorstangen."),
      ("Schokdempers en veren", "Een gebroken veer of versleten schokdemper geeft gebonk en een deinende auto."),
      ("Aandrijfas", "Een tikkend geluid bij vol insturen en optrekken, bijvoorbeeld op een parkeerplaats, wijst vaak op een versleten homokineet.")],
     "U kunt meestal doorrijden, maar wacht niet te lang: speling in de ophanging maakt de auto minder stabiel en laat de banden sneller slijten.",
     "We bekijken de ophanging op de brug en vertellen u wat er versleten is. Lees meer over <a href=\"{r}onderhoud-reparatie/\">onderhoud en reparatie</a>."),
    ("rook-uit-uitlaat", "Rook uit de uitlaat", "Rook uit de uitlaat: wat betekent de kleur?",
     "Witte, blauwe of zwarte rook uit de uitlaat? De kleur zegt veel over de oorzaak. Lees wat normaal is en wanneer u het moet laten nakijken.",
     "dienst-diagnose", "Diagnose",
     "Een beetje damp uit de uitlaat is normaal, zeker bij een koude motor. Blijft het roken, dan zegt de kleur veel over de oorzaak.",
     [("Witte damp bij een koude start", "Condens, vooral bij koud en vochtig weer. Verdwijnt het als de motor warm is, dan is er niets aan de hand."),
      ("Dikke witte rook die blijft", "Kan wijzen op koelvloeistof die in de motor komt, bijvoorbeeld door een defecte koppakking. Let op de temperatuurmeter en het koelvloeistofpeil."),
      ("Blauwe rook", "De motor verbrandt olie, bijvoorbeeld door versleten zuigerveren of klepsteeldichtingen, of een turboprobleem."),
      ("Zwarte rook", "Er wordt te veel brandstof verbrand. Bij een diesel kan het door een verstopt luchtfilter, de turbo of de verstuivers komen.")],
     "Witte damp bij een koude start is geen probleem. Blijft er rook komen, zeker blauw of dik wit, laat het dan snel nakijken. Loopt de temperatuur op, stop dan.",
     "We lezen de motor uit en zoeken gericht naar de oorzaak. Lees meer over <a href=\"{r}diagnose/\">diagnose</a>."),
    ("olie-lekt", "Vlek of lekkage onder de auto", "Vlek onder de auto: wat lekt er?",
     "Een vlek onder uw auto? De kleur verraadt meestal wat er lekt: motorolie, koelvloeistof, remvloeistof of gewoon condenswater van de airco.",
     "dienst-onderhoud", "Reparatie",
     "Een vlek onder de auto op de oprit? De kleur en de plek geven een goede aanwijzing.",
     [("Helder water", "Komt het van onder het dashboard, aan de voorkant, dan is het condenswater van de airco. Dat is normaal."),
      ("Bruin of zwart en vettig", "Motorolie. Controleer het oliepeil met de peilstok en laat het lek nakijken."),
      ("Groen, roze of blauw", "Koelvloeistof. Controleer het peil in het reservoir als de motor koud is. Een tekort kan de motor laten oververhitten."),
      ("Rood of roodbruin", "Vaak olie van de automatische versnellingsbak of de stuurbekrachtiging."),
      ("Helder tot geelachtig, bij een wiel", "Kan remvloeistof zijn. Rijd dan niet verder en laat het direct nakijken.")],
     "Condenswater is geen probleem. Bij olie of koelvloeistof kunt u meestal nog rustig naar de garage rijden als het peil goed is. Vermoedt u remvloeistof, of brandt er een rood lampje, rijd dan niet verder.",
     "We zoeken de lekkage op en vertellen u wat er nodig is. Zie ook onze uitleg over <a href=\"{r}dashboardlampjes/\">dashboardlampjes</a>."),
]


def klachtpagina(k):
    slug, naam, h1, desc, foto, dienst, intro, oorzaken, rijden, wij = k
    lijst = "\n".join(f"          <li><strong>{e(kop)}</strong> {e(tk)}</li>" for kop, tk in oorzaken)
    andere = "\n".join(f'          <li><a href="{{r}}hulp/{s2}/">{e(n2)}</a></li>' for s2, n2, *_ in KLACHTEN if s2 != slug)
    inhoud = f"""        <p>{e(intro)}</p>

        <h2>Wat kan het zijn?</h2>
        <ul class="oorzaken">
{lijst}
        </ul>

        <h2>Kunt u nog doorrijden?</h2>
        <p>{e(rijden)}</p>

        <h2>Wat doen wij?</h2>
        <p>{wij}</p>

        <h2>Andere klachten</h2>
        <ul class="hulp-links">
{andere}
        </ul>"""
    tool_pagina(f"hulp/{slug}", f"{naam}: oorzaken | Autoservice Barneveld", desc, h1, foto, "Hulp bij klachten", "Wat het kan zijn, of u nog kunt doorrijden en wanneer u het moet laten nakijken.",
                inhoud, (), None, dienst, kruimel=[("Wat is er met mijn auto?", f"{SITE}/hulp/")], naam=naam)


def hulp_overzicht():
    lijst = "\n".join(f'          <li><a href="{{r}}hulp/{slug}/">{e(naam)}</a><span>{e(intro.split(". ")[0].rstrip("."))}.</span></li>'
                      for slug, naam, _h, _d, _f, _di, intro, *_ in KLACHTEN)
    inhoud = f"""        <p>Merkt u iets geks aan uw auto? Hieronder vindt u de klachten die we het vaakst horen, met de meest voorkomende oorzaken en of u nog kunt doorrijden. Staat uw klacht er niet bij, of twijfelt u? Bel of app ons gerust.</p>

        <ul class="check-links hulp-overzicht">
{lijst}
        </ul>

        <h2>Brandt er een lampje?</h2>
        <p>Bekijk onze uitleg over <a href="{{r}}dashboardlampjes/">dashboardlampjes</a>: per lampje wat het betekent en wat u het beste kunt doen.</p>"""
    tool_pagina("hulp", "Wat is er met mijn auto? | Autoservice Barneveld",
                "Piepende remmen, een trillend stuur, rook uit de uitlaat of een auto die niet start? Uitleg over de meest voorkomende klachten en of u nog kunt doorrijden.",
                "Wat is er met mijn auto?", "dienst-diagnose", "Hulp bij klachten",
                "De meest voorkomende klachten op een rij: wat het kan zijn en of u nog kunt doorrijden.",
                inhoud, (), None, "Reparatie", naam="Wat is er met mijn auto?")


HANDIG = [
    ("Kenteken-checks", "", [
        ("apk-check", "APK-check", "Tot wanneer is uw APK geldig, en vanaf wanneer kunt u keuren?"),
        ("occasion-check", "Occasion-check", "APK-historie, gemelde gebreken en tellerstand van een tweedehands auto."),
        ("kentekencheck", "Kentekencheck", "Alle openbare gegevens van een auto op een rij."),
        ("terugroepactie-check", "Terugroepactie-check", "Staat er een terugroepactie open voor uw auto?"),
        ("trekgewicht-check", "Trekgewicht-check", "Hoeveel mag uw auto trekken met caravan of aanhanger?"),
    ]),
    ("Banden", "", [
        ("winterbanden", "Winterbandenmeter", "Is het al tijd voor winterbanden in Barneveld?"),
        ("bandencheck", "Bandencheck", "Bandenmaat, leeftijd en profiel uitgelegd."),
    ]),
    ("Onderhoud en storingen", "", [
        ("onderhoudswijzer", "Onderhoudswijzer", "Wanneer komt uw volgende beurt, klein of groot?"),
        ("dashboardlampjes", "Dashboardlampjes", "Wat betekent dit lampje, en kunt u nog doorrijden?"),
        ("hulp", "Wat is er met mijn auto?", "Piepende remmen, een trillend stuur, rook uit de uitlaat en meer."),
    ]),
]


def handig():
    blokken = []
    for kop, sub, items in HANDIG:
        lijst = "\n".join(f'          <li><a href="{{r}}{slug}/">{e(n)}</a><span>{e(u)}</span></li>' for slug, n, u in items)
        subp = f"\n        <p>{sub}</p>" if sub else ""
        blokken.append(f'        <h2>{kop}</h2>{subp}\n        <ul class="check-links">\n{lijst}\n        </ul>')
    inhoud = ("        <p>Even zelf iets nakijken? Hier vindt u al onze gratis checks en uitleg op één plek. "
              "Komt u er niet uit, of wilt u het zeker weten? Bel of app ons gerust.</p>\n\n" + "\n\n".join(blokken))
    tool_pagina("handig", "Handige checks en uitleg voor uw auto | Autoservice Barneveld",
                "Gratis APK-check, occasion-check, kentekencheck, winterbandenmeter, onderhoudswijzer en uitleg over dashboardlampjes en klachten. Van uw garage in Barneveld.",
                "Handige checks en uitleg", "dienst-diagnose", "Handig",
                "Gratis checks en heldere uitleg over uw auto, op één plek.",
                inhoud, (), None, "", naam="Handige checks en uitleg")


def handig_sectie():
    keuze = [("apk-check", "APK-check", "Hoe lang is uw APK nog geldig?"),
             ("occasion-check", "Occasion-check", "Wat is er bekend over een tweedehands auto?"),
             ("dashboardlampjes", "Dashboardlampjes", "Wat betekent dit lampje?"),
             ("winterbanden", "Winterbandenmeter", "Al tijd voor winterbanden?")]
    lijst = "\n".join(f'        <li><a href="{slug}/">{e(n)}</a><span>{e(u)}</span></li>' for slug, n, u in keuze)
    return f"""  <section class="sectie handig-sectie" aria-labelledby="handig-titel">
    <div class="wrap">
      <div class="kopje">
        <span class="label">Handig</span>
        <h2 class="groot" id="handig-titel">Even zelf checken</h2>
        <p>Gratis checks en heldere uitleg, voor als u even iets wilt nakijken.</p>
      </div>
      <ul class="check-links handig-raster">
{lijst}
      </ul>
      <p><a class="verder" href="handig/">Alle checks en uitleg <span aria-hidden="true">→</span></a></p>
    </div>
  </section>"""


def sitemap_en_llms():
    paden = ["", *[d[0] + "/" for d in DIENSTEN], "aankoopkeuring/", "apk-check/", "occasion-check/", "kentekencheck/", "terugroepactie-check/", "trekgewicht-check/",
             "winterbanden/", "bandencheck/", "onderhoudswijzer/", "dashboardlampjes/", "hulp/", *[f"hulp/{k[0]}/" for k in KLACHTEN],
             "handig/", "vervangend-vervoer/", "merken/", "werkgebied/", "veelgestelde-vragen/", "over-ons/", "contact/", "privacy/"]
    schrijf("sitemap.xml",
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{DATUM}</lastmod></url>\n" for p in paden)
            + "</urlset>\n")
    diensten = "\n".join(f"- [{n}]({SITE}/{s}/): {k}" for s, n, _t, _d, _h, _f, _a, k, _k in DIENSTEN)
    profielen = "\n".join(f"- [{n}]({u})" for n, u in PROFIELEN)
    schrijf("llms.txt", f"""# Autoservice Barneveld

> Zelfstandige, universele garage in Barneveld (Gelderland) voor APK, onderhoud, reparatie, diagnose, banden, uitlijnen en aircoservice. Alle merken, ook elektrische auto's. RDW-erkend. Afspraak maken kan via het formulier op de website (opent WhatsApp), telefonisch of per e-mail.

- Adres: {ADRES}, {POSTCODE_PLAATS}
- Telefoon en WhatsApp: {TEL}
- E-mail: {MAIL}
- Openingstijden: maandag t/m vrijdag 08:00–17:00, zaterdag op afspraak, zondag gesloten
- KvK: {KVK}
- Btw: {BTW}
- Werkgebied: Barneveld, Voorthuizen, Kootwijkerbroek, Terschuur, Zwartebroek, Garderen, Stroe, De Glind, Lunteren
- Uitlijnen: onderdeel van de bandenservice
- Vervangend vervoer: elektrische Renault 5 (particulier), VW Caddy (zakelijk), leenfiets; wachtruimte met koffie en wifi; station op vijf minuten lopen

## Diensten

{diensten}

## Meer

- [Aankoopkeuring]({SITE}/aankoopkeuring/): tweedehands auto vóór de koop onafhankelijk laten nakijken; bij importauto\'s met twijfel ook een historierapport van Carfax of carVertical.

## Gratis checks en uitleg

- [APK-check]({SITE}/apk-check/): vul een kenteken in en zie tot wanneer de APK geldig is, vanaf wanneer keuren met behoud van de vervaldatum kan, en de openbare RDW-gegevens van de auto.
- [Occasion-check]({SITE}/occasion-check/): APK-datum, gemelde gebreken en adviespunten bij eerdere APK-keuringen, tellerstandoordeel, import en terugroepacties per kenteken.
- [Kentekencheck]({SITE}/kentekencheck/): openbare RDW-gegevens van een auto.
- [Terugroepactie-check]({SITE}/terugroepactie-check/): staat er een terugroepactie open?
- [Trekgewicht-check]({SITE}/trekgewicht-check/): geremd en ongeremd trekgewicht, met uitleg over rijbewijs B, code 96 en BE.
- [Winterbandenmeter]({SITE}/winterbanden/): 7-gradenregel op basis van de weersverwachting voor Barneveld.
- [Bandencheck]({SITE}/bandencheck/): bandenmaat en DOT-code uitgelegd, profieldiepte en bandenlabel.
- [Onderhoudswijzer]({SITE}/onderhoudswijzer/): kleine of grote beurt, en wanneer.
- [Dashboardlampjes]({SITE}/dashboardlampjes/): betekenis van storingslampjes per kleur en wat te doen.
- [Wat is er met mijn auto?]({SITE}/hulp/): uitleg bij veelvoorkomende klachten.
- [Vervangend vervoer]({SITE}/vervangend-vervoer/)
- [Alle merken]({SITE}/merken/)
- [Werkgebied]({SITE}/werkgebied/)
- [Veelgestelde vragen]({SITE}/veelgestelde-vragen/)
- [Over ons]({SITE}/over-ons/)
- [Contact en route]({SITE}/contact/)
{profielen}
""")


if __name__ == "__main__":
    homepage()
    for d in DIENSTEN:
        dienstpagina(d)
    over_ons()
    vervangend_vervoer()
    merken()
    werkgebied()
    vragen()
    contact()
    privacy()
    niet_gevonden()
    apk_check()
    occasion_check()
    aankoopkeuring()
    kentekencheck()
    terugroepactie_check()
    trekgewicht_check()
    dashboardlampjes()
    winterbanden()
    bandencheck()
    onderhoudswijzer()
    hulp_overzicht()
    for k in KLACHTEN:
        klachtpagina(k)
    handig()
    sitemap_en_llms()
