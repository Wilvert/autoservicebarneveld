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
DATUM = "2026-11-01"

TEL = "0342-234003"
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
       "frame-src https://www.openstreetmap.org; connect-src 'self' https://formsubmit.co https://api.pdok.nl https://opendata.rdw.nl; form-action 'self' mailto: https://formsubmit.co; "
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
     "Onderhoud en reparatie | Autoservice Barneveld",
     "Kleine of grote beurt en reparaties voor alle merken in Barneveld. Kosten vooraf duidelijk en updates via WhatsApp. Bel 0342-234003.",
     "Onderhoud en reparatie in Barneveld", "dienst-onderhoud", "Monteur aan het werk bij een wiel",
     "Grote of kleine onderhoudsbeurt, of het vervangen van een lampje: wij zorgen dat uw auto veilig, betrouwbaar en in topconditie blijft.",
     "Plan onderhoud"),
    ("apk-keuring", "APK-keuring",
     "APK-keuring Barneveld, alle merken | Autoservice Barneveld",
     "RDW-erkende APK-keuring in Barneveld voor alle merken, ook elektrische auto's. Kosten vooraf duidelijk. Plan uw afspraak via WhatsApp.",
     "APK-keuring in Barneveld", "dienst-apk", "Auto op de brug tijdens een APK-keuring",
     "De verplichte keuring voor verkeersveiligheid en milieu, zorgvuldig uitgevoerd voor alle merken.",
     "Plan APK"),
    ("diagnose", "Diagnose",
     "Auto uitlezen en diagnose | Autoservice Barneveld",
     "Brandt er een storingslampje? Wij lezen uw auto uit met moderne diagnoseapparatuur en verhelpen de storing. Alle merken, in Barneveld.",
     "Diagnose en storingen verhelpen", "dienst-diagnose", "Uitleesapparatuur bij een auto",
     "Met moderne (uitlees)apparatuur sporen wij storingen en elektronische problemen snel op en verhelpen ze.",
     "Plan diagnose"),
    ("bandenservice", "Bandenservice",
     "Banden en winterbanden wisselen | Autoservice Barneveld",
     "Montage, balanceren en seizoenswissel van zomer- en winterbanden in Barneveld. Banden voor alle merken, ook elektrische auto's.",
     "Bandenservice in Barneveld", "dienst-banden", "Band op de bandenmontagemachine",
     "Montage, balanceren en (seizoens)wissel. Snel en vakkundig, voor alle merken, ook elektrische auto's.",
     "Plan banden"),
    ("airco-service", "Aircoservice",
     "Airco-service auto in Barneveld | Autoservice Barneveld",
     "Auto-airco vullen, controleren, lekdetectie en reparatie voor alle merken in Barneveld. Koel in de zomer, heldere ruiten in de winter.",
     "Aircoservice voor uw auto", "dienst-airco", "Aircoservice onder de motorkap",
     "Vullen, controleren, lekdetectie en reparaties. Koel in de zomer en helder zicht in de winter.",
     "Plan airco"),
    ("elektrische-auto", "Elektrische auto",
     "Onderhoud elektrische auto | Autoservice Barneveld",
     "Ook een elektrische auto heeft onderhoud nodig. Banden, remmen, ophanging, airco en APK voor alle merken. Autoservice Barneveld.",
     "Onderhoud van uw elektrische auto", "dienst-onderhoud", "Monteur werkt aan de wielophanging van een auto",
     "Het reguliere onderhoud, banden, airco en APK van elektrische auto's van alle merken.",
     "Plan onderhoud"),
]
DIENST_OPTIES = [d[1] for d in DIENSTEN if d[0] != "elektrische-auto"] + ["Overig"]

TEKST = {
"apk-keuring": """
<p>De APK (Algemene Periodieke Keuring) is verplicht en controleert of uw auto veilig en milieuvriendelijk genoeg is voor de weg. Autoservice Barneveld is door de RDW erkend en keurt auto's van alle merken, ook elektrische auto's. We voeren de keuring zorgvuldig uit, zodat u veilig en volgens de wettelijke eisen de weg op gaat.</p>

<h2>Wanneer moet uw auto APK?</h2>
<p>De vervaldatum van uw APK ziet u bij de <a href="https://ovi.rdw.nl/">kentekencheck van de RDW</a>. U kunt de keuring tot twee maanden vóór die datum laten doen zonder dat u er tijd mee verliest: de nieuwe vervaldatum wordt dan gerekend vanaf de oude.</p>

<h2>APK en onderhoud in één afspraak</h2>
<p>Veel klanten combineren de APK met een kleine of grote <a href="{r}onderhoud-reparatie/">onderhoudsbeurt</a>. Dat scheelt een extra ritje naar de garage. Komt er tijdens de keuring iets naar boven dat vervangen moet worden? Dan bespreken we eerst de kosten met u, eventueel met een foto of filmpje via WhatsApp. Pas na uw akkoord gaan we aan de slag.</p>

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
<p>Alle kosten worden vooraf besproken. Ontdekken we tijdens het werk iets onverwachts, dan houden we u direct op de hoogte via WhatsApp, met foto's, korte filmpjes of een duidelijke toelichting. U weet dus altijd wie er aan uw auto werkt en wat er gaat gebeuren.</p>

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
<p>Goede banden zijn belangrijk voor uw veiligheid, uw remweg en uw verbruik. Wij verzorgen montage, balanceren en de seizoenswissel van uw banden. We werken snel en vakkundig, zodat uw auto altijd de juiste grip houdt.</p>

<h2>Zomer- en winterbanden wisselen</h2>
<p>Rijdt u in de winter op winterbanden, dan wisselen we ze in het najaar en voorjaar voor u om. We controleren daarbij meteen het profiel, de bandenspanning en eventuele schade.</p>

<h2>Nieuwe banden</h2>
<p>Toe aan nieuwe banden? Wij leveren en monteren banden voor alle merken, ook voor elektrische auto's. Die zijn zwaarder en hebben meer koppel, en vragen daarom vaak om banden die daarvoor geschikt zijn. We adviseren u graag over de juiste keuze.</p>

<h2>Balanceren</h2>
<p>Trilt uw stuur bij een bepaalde snelheid? Dan zijn uw wielen mogelijk uit balans. Met balanceren rijdt uw auto weer rustig en slijten uw banden gelijkmatiger.</p>
""",
"airco-service": """
<p>Voor een goed werkende airco bent u bij ons aan het juiste adres. Wij verzorgen het vullen, controleren, lekdetectie en reparaties van aircosystemen van alle merken. Zo blijft uw auto koel in de zomer en blijven uw ruiten helder in de winter.</p>

<h2>Waarom aircoservice?</h2>
<p>Een airco verliest ieder jaar een beetje koudemiddel. Koelt uw airco minder goed, ruikt het muf of beslaan uw ruiten snel? Dan is het tijd voor een controle. Een goed werkende airco droogt de lucht, waardoor uw ruiten in de winter sneller ontwasemen.</p>

<h2>Wat we doen</h2>
<p>We controleren het systeem, vullen het koudemiddel bij en sporen eventuele lekkages op. Is er een onderdeel defect, dan bespreken we de reparatie en de kosten eerst met u.</p>

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
<p>Ook een elektrische auto moet APK. Wij keuren alle merken, zie <a href="{r}apk-keuring/">APK-keuring</a>. Brandt er een storingslampje? Onze <a href="{r}diagnose/">diagnoseapparatuur</a> is ook geschikt voor elektrische auto's.</p>

<h2>Zelf ook elektrisch onderweg</h2>
<p>Terwijl uw auto bij ons staat, kunt u rijden in onze elektrische Renault 5. Lees meer over ons <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p>
""",
}


def e(t):
    return html.escape(t, quote=True)


# ------------------------------------------------------------------ vaste blokken
def schema_tag():
    data = json.loads((ROOT / "bron" / "bedrijf.json").read_text(encoding="utf-8"))
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>")


def head(r, pad, title, desc, noindex=False):
    regels = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
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
            f'<meta property="og:image" content="{SITE}/img/deelafbeelding.jpg">',
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
        for h, n, k in items)
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
      <p class="uitleg">Vul uw gegevens in. Daarna opent WhatsApp met uw aanvraag al klaar; u verstuurt hem zelf.</p>
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
        <div class="veld omschrijving" hidden>
          <label for="v-omschrijving">Korte omschrijving</label>
          <textarea class="invoer" id="v-omschrijving" name="omschrijving" rows="3" maxlength="300" placeholder="Bijv. piepende remmen of een lampje op het dashboard"></textarea>
        </div>
        <div class="rij">
          <div class="veld">
            <label for="v-km">Kilometerstand <small class="label-hint">ongeveer is prima</small></label>
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
          <p class="datum-haast">{I_TEL.format(s=18)}<span><strong>Haast of eerder geholpen worden?</strong> Bel even <a href="{TEL_LINK}">{TEL}</a>. U heeft dan direct contact met ons en we helpen u meteen verder.</span></p>
          <button type="button" class="datum-weg">Geen voorkeursdatum</button>
        </fieldset>
        <button class="knop wa" type="submit">{I_WA} Verstuur via WhatsApp</button>
        <p class="klein">Uw gegevens gaan alleen naar ons via WhatsApp. Zie de <a href="{r}privacy/">privacyverklaring</a>. Liever bellen? <a href="{TEL_LINK}">{TEL}</a></p>
      </form>
    </div>
    <div class="venster-klaar" hidden>
      <svg width="56" height="56" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.2 3L17 9"/></g></svg>
      <h2>Bijna klaar</h2>
      <p class="uitleg">WhatsApp is geopend met uw aanvraag. Druk daar op <strong>verzenden</strong>, dan nemen wij zo snel mogelijk contact op om de afspraak vast te leggen.</p>
      <p class="klein">Opent WhatsApp niet? <a class="wa-opnieuw" href="{WA_LINK}">Probeer het opnieuw</a> of bel <a href="{TEL_LINK}">{TEL}</a>.</p>
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
      <p>Universele garage in Barneveld voor onderhoud, reparatie, APK, diagnose, banden en airco. Alle merken, ook elektrisch.</p>
      <img class="rdw" src="{r}img/rdw-erkend.webp" alt="RDW erkend" width="132" height="77" loading="lazy">
    </div>
    <div>
      <h3>Adres en tijden</h3>
      <ul><li>{ADRES}</li><li>{POSTCODE_PLAATS}</li><li>Ma–vr 08:00–17:00</li><li>Za op afspraak · zo gesloten</li><li><a href="{r}contact/">Route plannen</a></li></ul>
    </div>
    <div>
      <h3>Contact</h3>
      <ul><li><a href="{TEL_LINK}">{TEL}</a></li><li><a href="{WA_LINK}">WhatsApp</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="{r}contact/" data-afspraak>Plan afspraak</a></li></ul>
    </div>
    <div>
      <h3>Diensten</h3>
      <ul>{diensten}<li><a href="{r}vervangend-vervoer/">Vervangend vervoer</a></li></ul>
    </div>
    <p class="onder">© 2026 Autoservice Barneveld · KvK {KVK} · btw {BTW} · <a href="{r}privacy/">Privacyverklaring</a> · Volg ons: {profielen}</p>
  </div>
</footer>"""


def pagina(r, pad, title, desc, actief, main, noindex=False):
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
{head(r, pad, title, desc, noindex)}
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
    if dienst not in DIENST_OPTIES:
        dienst = "Onderhoud & reparatie" if dienst == "Elektrische auto" else ""
    data = f' data-dienst="{e(dienst)}"' if dienst else ""
    return f"""<aside class="zijkaart" aria-labelledby="zijkaart-titel">
        <h2 id="zijkaart-titel">Plan uw afspraak</h2>
        <p>Kenteken, kilometerstand en e-mail invullen, dan staat uw aanvraag klaar in WhatsApp.</p>
        <a class="knop oranje" href="{r}contact/" data-afspraak{data}>Plan afspraak {I_PIJL}</a>
        <ul>
          <li>Bel <a href="{TEL_LINK}">{TEL}</a></li>
          <li>App via <a href="{WA_LINK}">WhatsApp</a></li>
          <li>{TIJDEN_KORT}</li>
          <li>{ADRES}, {POSTCODE_PLAATS}</li>
        </ul>
      </aside>"""


def pagina_kop(r, h1, foto, kicker="", inleiding=""):
    k = f'<span class="kicker"><i aria-hidden="true"></i>{kicker}</span>\n      ' if kicker else ""
    i = f'\n      <p class="inleiding">{inleiding}</p>' if inleiding else ""
    return f"""  <section class="pagina-kop">
    <div class="hero-foto"><img src="{r}img/{foto}.webp" alt="" width="1848" height="1232" fetchpriority="high"></div>
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
def homepage():
    r = ""
    lijst = []
    for slug, naam, _t, _d, _h, foto, alt, kort, knop in DIENSTEN:
        if slug == "elektrische-auto":
            continue
        lijst.append(f"""        <li class="dienst">
          <img src="img/{foto}.webp" alt="{e(alt)}" width="960" height="639" loading="lazy">
          <div><h3><a href="{slug}/">{e(naam)}</a></h3><p>{kort}</p><a class="meer" href="{slug}/">Meer over {e(naam.lower() if slug != 'apk-keuring' else 'de APK')}</a></div>
          <a class="plan" href="contact/" data-afspraak data-dienst="{e(naam if naam in DIENST_OPTIES else "Onderhoud & reparatie")}">{knop} <span aria-hidden="true">→</span></a>
        </li>""")
    diensten = "\n".join(lijst)
    main = f"""  <section class="hero" id="afspraak" aria-labelledby="hero-titel">
    <div class="hero-foto"><img src="img/hero-home.webp" alt="" width="1848" height="1232" fetchpriority="high"></div>
    <div class="wrap">
      <div class="hero-tekst">
        <h1 id="hero-titel">Vakkundig onderhoud voor uw auto in Barneveld</h1>
        <p>Onderhoud, reparatie, APK, diagnose, banden en airco. Vul uw kenteken in, kies een dienst en verstuur uw aanvraag via WhatsApp.</p>
        <a class="hero-bel" href="{TEL_LINK}"><span aria-hidden="true">{I_TEL.format(s=20)}</span>Liever bellen? {TEL}</a>
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
      <li><img class="rdw-mini" src="img/rdw-erkend.webp" alt="" width="62" height="36"><span><strong>RDW erkend</strong>APK voor alle merken</span></li>
      <li><span class="ico" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 16V11l2-5h14l2 5v5M3 16h18M3 16v2h3v-2m12 0v2h3v-2M5 11h14"/></svg></span><span><strong>Alle merken</strong>Onderhoud en reparatie</span></li>
      <li><span class="ico" aria-hidden="true">{I_BLIKSEM.format(s=24)}</span><span><strong>Ook elektrisch</strong>Onderhoud van e-auto's</span></li>
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

  <section class="sectie over" id="over-ons" aria-labelledby="over-titel">
    <div class="wrap">
      <div class="over-foto"><img src="img/hero-over-ons.webp" alt="De monteur van Autoservice Barneveld in de werkplaats" width="1232" height="1848" loading="lazy"></div>
      <div>
        <span class="label">Over ons</span>
        <h2 class="groot" id="over-titel">Kwaliteit en service staan voorop</h2>
        <p>Bij Autoservice Barneveld draait alles om vakmanschap, transparantie en persoonlijk contact. Als zelfstandige monteur werk ik rechtstreeks met mijn klanten samen, zonder tussenpersonen. Zo weet u altijd precies wie er aan uw auto werkt. De werkplaats is uitgerust met de nieuwste apparatuur, voor regulier onderhoud én complexe diagnoses.</p>
        <ol class="stappen" aria-label="Zo werkt het">
          <li><strong>U plant een afspraak</strong><p>Online met uw kenteken via WhatsApp, of telefonisch.</p></li>
          <li><strong>Kosten vooraf besproken</strong><p>Zo komt u nooit voor verrassingen te staan.</p></li>
          <li><strong>Op de hoogte via WhatsApp</strong><p>Iets onverwachts? Dan hoort u het direct, met foto's, korte filmpjes of een duidelijke toelichting.</p></li>
          <li><strong>U blijft mobiel</strong><p>Met een leenauto of leenfiets.</p></li>
        </ol>
        <a class="verder" href="over-ons/">Meer over ons <span aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>

{vervoer_sectie("")}

{review_sectie()}

{contact_sectie("", kaart=False)}"""
    schrijf("index.html", pagina(
        "", "", "Garage Barneveld: APK & onderhoud | Autoservice Barneveld",
        "Universele garage in Barneveld voor APK, onderhoud, reparatie, diagnose, banden en airco. Alle merken, ook elektrisch. Bel 0342-234003.",
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
    return f"""  <section class="sectie" id="vervangend-vervoer"{' aria-labelledby="vervoer-titel"' if kopje else ' aria-label="Mogelijkheden"'}>
    <div class="wrap">
{kopje}      <div class="vervoer-raster">
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
        <div class="optie foto"><img src="{r}img/hero-vervangend-vervoer.webp" alt="Leenauto van Autoservice Barneveld in de werkplaats" width="1848" height="1232" loading="lazy"></div>
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
        <p>Heeft u vragen over onze diensten of wilt u een afspraak maken? Neem dan gelijk contact met ons op voor betrouwbare en professionele service.</p>
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
        <input type="text" name="_honey" class="honing" tabindex="-1" autocomplete="off" aria-hidden="true">
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
def dienstpagina(d):
    slug, naam, title, desc, h1, foto, _alt, kort, _knop = d
    r = "../"
    andere = "\n".join(f'          <li><a href="{r}{s}/">{e(n)}</a></li>'
                       for s, n, *_ in DIENSTEN if s != slug)
    main = f"""{pagina_kop(r, h1, foto, "Dienst · alle merken", kort)}

  <section class="sectie">
    <div class="wrap artikel">
      <div class="tekst">
{TEKST[slug].strip().format(r=r)}

        <ul class="andere-diensten" aria-label="Andere diensten">
{andere}
        </ul>
      </div>
      {zijkaart(r, naam)}
    </div>
  </section>"""
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
        <p>Onze werkplaats is uitgerust met de nieuwste apparatuur en geschikt voor zowel regulier onderhoud als complexe diagnoses. Ik verzorg onderhoud en reparaties aan alle merken en modellen, inclusief het reguliere onderhoud van <a href="{r}elektrische-auto/">elektrische auto's</a>.</p>

        <h2>Heldere communicatie</h2>
        <p>Transparantie staat centraal in mijn werkwijze. Alle kosten worden vooraf besproken, zodat u nooit voor verrassingen komt te staan. Ontdekken we tijdens het werk iets onverwachts? Dan houd ik u direct op de hoogte via WhatsApp, met foto's, korte filmpjes of een duidelijke toelichting.</p>

        <h2>Waarom klanten kiezen voor Autoservice Barneveld</h2>
        <p>Klanten waarderen vooral de combinatie van deskundigheid, duidelijke communicatie en een nuchtere aanpak. Zo weet u zeker dat uw auto in goede handen is.</p>

        <ol class="stappen" aria-label="Zo werkt het">
          <li><strong>U plant een afspraak</strong><p>Online met uw kenteken via WhatsApp, of telefonisch.</p></li>
          <li><strong>Kosten vooraf besproken</strong><p>Zo komt u nooit voor verrassingen te staan.</p></li>
          <li><strong>Op de hoogte via WhatsApp</strong><p>Iets onverwachts? Dan hoort u het direct.</p></li>
          <li><strong>U blijft mobiel</strong><p>Met een leenauto of leenfiets, zie <a href="{r}vervangend-vervoer/">vervangend vervoer</a>.</p></li>
        </ol>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("over-ons/index.html", pagina(
        r, "over-ons/", "Over ons | Autoservice Barneveld",
        "Autoservice Barneveld: zelfstandige monteur met moderne werkplaats. Vakmanschap, vooraf duidelijke kosten en updates via WhatsApp.",
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
        <p>Of u nu particulier of zakelijk klant bent, wij zorgen dat u mobiel blijft. Geef bij het plannen van uw afspraak aan welke optie u wilt gebruiken.</p>
      </div>
      {zijkaart(r)}
    </div>
  </section>"""
    schrijf("vervangend-vervoer/index.html", pagina(
        r, "vervangend-vervoer/", "Vervangend vervoer | Autoservice Barneveld",
        "Leenauto (elektrische Renault 5 of VW Caddy) of leenfiets terwijl uw auto bij ons in Barneveld staat.",
        "vervangend-vervoer", main))


def contact():
    r = "../"
    main = contact_sectie(r, kaart=True, titel="Contact en route", h="h1")
    schrijf("contact/index.html", pagina(
        r, "contact/", "Contact en route | Autoservice Barneveld",
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
        <p>Het afspraakformulier op deze website slaat niets op en verstuurt niets zelf. Het zet uw kenteken (of merk en model), de gekozen werkzaamheden, kilometerstand, adres, e-mailadres en eventuele voorkeursdata in een WhatsApp-bericht, dat u daarna zelf verstuurt. Voor dat bericht gelden ook de voorwaarden van WhatsApp (Meta). Om uw straat en woonplaats bij uw postcode en huisnummer te vinden, vraagt het formulier die op bij de Basisregistratie Adressen via PDOK (Kadaster). Bij een ingevuld kenteken haalt het formulier het merk, model en de APK-vervaldatum op uit de openbare gegevens van de RDW. Bij beide wordt niets opgeslagen.</p>

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


def sitemap_en_llms():
    paden = ["", *[d[0] + "/" for d in DIENSTEN], "vervangend-vervoer/", "over-ons/", "contact/", "privacy/"]
    schrijf("sitemap.xml",
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{DATUM}</lastmod></url>\n" for p in paden)
            + "</urlset>\n")
    diensten = "\n".join(f"- [{n}]({SITE}/{s}/): {k}" for s, n, _t, _d, _h, _f, _a, k, _k in DIENSTEN)
    profielen = "\n".join(f"- [{n}]({u})" for n, u in PROFIELEN)
    schrijf("llms.txt", f"""# Autoservice Barneveld

> Zelfstandige, universele garage in Barneveld (Gelderland) voor APK, onderhoud, reparatie, diagnose, banden en aircoservice. Alle merken, ook elektrische auto's. RDW-erkend. Afspraak maken kan via het formulier op de website (opent WhatsApp), telefonisch of per e-mail.

- Adres: {ADRES}, {POSTCODE_PLAATS}
- Telefoon en WhatsApp: {TEL}
- E-mail: {MAIL}
- Openingstijden: maandag t/m vrijdag 08:00–17:00, zaterdag op afspraak, zondag gesloten
- KvK: {KVK}
- Btw: {BTW}
- Werkgebied: Barneveld, Voorthuizen, Kootwijkerbroek, Terschuur, Zwartebroek, Garderen, Stroe, De Glind, Lunteren
- Vervangend vervoer: elektrische Renault 5 (particulier), VW Caddy (zakelijk), leenfiets; wachtruimte met koffie en wifi; station op vijf minuten lopen

## Diensten

{diensten}

## Meer

- [Vervangend vervoer]({SITE}/vervangend-vervoer/)
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
    contact()
    privacy()
    niet_gevonden()
    sitemap_en_llms()
