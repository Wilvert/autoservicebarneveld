"""Maakt de PDF's in downloads/ in de stijl van het briefpapier:
logo linksboven, veel wit, blauwe voetband met de bedrijfsgegevens.

  downloads/checklist-tweedehands-auto.pdf   uitgebreide checklist (zelfde tekst als de webpagina)
  downloads/voorbereiding-aankoopkeuring.pdf korte lijst voor wie een aankoopkeuring plant

Gebruik:  python3 bron/maak_pdf.py   (na bron/bouw.py; vraagt Playwright met Chromium)
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
import bouw  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = bouw.ROOT
e = bouw.e
FONT = base64.b64encode((ROOT / "fonts" / "montserrat.woff2").read_bytes()).decode()
FONT_KOP = base64.b64encode((ROOT / "fonts" / "bebas-neue.woff2").read_bytes()).decode()
LOGO = base64.b64encode((ROOT / "img" / "logo.svg").read_bytes()).decode()
BLAUW, GRIJS, ORANJE = "#0a467f", "#404042", "#e7814d"
FONTS = (f'@font-face {{ font-family: "Montserrat"; src: url(data:font/woff2;base64,{FONT}) format("woff2"); font-weight: 300 900; }}'
         f'@font-face {{ font-family: "Bebas Neue"; src: url(data:font/woff2;base64,{FONT_KOP}) format("woff2"); }}')

# Voetband zoals op het briefpapier (zonder IBAN: op een lijst over betalen zou dat verwarren)
VOET = f"""<style>{FONTS}
* {{ margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.band {{ width: 100%; height: 30mm; background: {BLAUW}; color: #fff; font-family: Montserrat, Arial, sans-serif;
         font-size: 10.5pt; line-height: 1.7; display: flex; align-items: center; padding: 0 15mm; box-sizing: border-box; gap: 12mm; }}
.band div {{ flex: 1; }} .band div:last-child {{ flex: .8; }} b {{ font-weight: 700; }} .k {{ display: inline-block; width: 19mm; font-weight: 700; }}
.nr {{ position: absolute; right: 15mm; bottom: 33mm; font-size: 7.5pt; color: #8c8c8e; font-family: Montserrat, Arial, sans-serif; }}
</style>
<div class="band">
  <div><b>Autoservice Barneveld</b><br>{bouw.ADRES}<br>{bouw.POSTCODE_PLAATS}</div>
  <div>{bouw.TEL}<br>{bouw.MAIL}<br>www.autoservicebarneveld.nl</div>
  <div><span class="k">KvK</span>{bouw.KVK}<br><span class="k">BTW-nr</span>{bouw.BTW}</div>
</div>"""

STIJL = f"""{FONTS}
@page {{ size: A4; margin: 14mm 15mm 36mm; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font-family: Montserrat, Arial, sans-serif; font-size: 9.2pt; line-height: 1.42; color: {GRIJS}; }}
.logo {{ width: 52mm; display: block; margin: 0 0 9mm; }}
h1 {{ font-family: "Bebas Neue", sans-serif; font-weight: 400; font-size: 28pt; line-height: 1; color: {BLAUW}; margin: 0 0 3mm; }}
.intro {{ margin: 0 0 4mm; max-width: 150mm; }}
h2 {{ font-family: "Bebas Neue", sans-serif; font-weight: 400; font-size: 15.5pt; color: {BLAUW}; margin: 5mm 0 1.5mm; break-after: avoid; }}
h3 {{ margin: 0 0 1mm; font-size: 9.8pt; color: {BLAUW}; }}
p {{ margin: 0 0 2mm; }}
ul {{ list-style: none; margin: 0; padding: 0; }}
.vak li {{ position: relative; padding: 1.1mm 0 1.1mm 6.5mm; break-inside: avoid; }}
.vak li::before {{ content: ""; position: absolute; left: 0; top: 1.9mm; width: 3.4mm; height: 3.4mm; border: 1.3px solid {BLAUW}; border-radius: .8mm; }}
.kolommen {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 10mm; }}
.kolommen section {{ break-inside: avoid; }}
.blok {{ border: 1px solid #d9d9d9; border-radius: 2mm; padding: 3mm 4mm; break-inside: avoid; }}
.blok h2 {{ margin-top: 0; }}
.rechten {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }}
.misverstanden {{ margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 2mm 3mm; }}
.misverstanden > div {{ border-left: 1mm solid #9db5cc; background: #f4f6f9; padding: 2mm 3mm; break-inside: avoid; }}
.misverstanden dt {{ font-weight: 700; }}
.misverstanden dd {{ margin: .5mm 0 0; font-size: 8.4pt; line-height: 1.35; }}
.te-mooi {{ margin-top: 4mm; padding: 3.5mm 5mm; border-left: 1.3mm solid {ORANJE}; background: #fff3e3; break-inside: avoid; }}
.te-mooi h2 {{ margin-top: 0; }}
.lijst-let-op {{ columns: 2; column-gap: 8mm; }}
.lijst-let-op li {{ position: relative; padding: .7mm 0 .7mm 5.5mm; }}
.lijst-let-op li::before {{ content: "!"; position: absolute; left: 0; top: 1.2mm; width: 3.5mm; height: 3.5mm; border-radius: 50%; background: {ORANJE}; color: #fff; font-size: 6.5pt; font-weight: 800; text-align: center; line-height: 3.5mm; }}
.noot {{ font-size: 7.8pt; color: #666668; margin-top: 4mm; }}
.nieuwe-pagina {{ break-before: page; }}
.groet {{ margin-top: 5mm; }}
.groet strong {{ display: block; color: {BLAUW}; }}
.ruim .vak li {{ padding: 1.3mm 0 1.3mm 7mm; font-size: 10pt; }}
.ruim .vak li::before {{ top: 2.1mm; width: 3.8mm; height: 3.8mm; }}
.ruim h2 {{ font-size: 18pt; margin-top: 5mm; }}
.ruim .intro {{ font-size: 10pt; }}
.kader {{ margin-top: 5mm; padding: 4mm 5mm; background: #f4f6f9; border-left: 1.3mm solid {BLAUW}; font-size: 9.6pt; }}
"""


def lijst(items, klasse="vak"):
    return f'<ul class="{klasse}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def blok(kop, items):
    return f"<section><h2>{e(kop)}</h2>{lijst(items)}</section>"


def pagina(titel, body):
    return f"""<!DOCTYPE html><html lang="nl"><head><meta charset="utf-8"><title>{e(titel)}</title><style>{STIJL}</style></head>
<body><img class="logo" src="data:image/svg+xml;base64,{LOGO}" alt="Autoservice Barneveld">{body}</body></html>"""


def checklist():
    C = dict(bouw.CHECKLIST)
    links = ["Vóór de bezichtiging", "Buitenkant en banden"]
    rechts = ["Motorruimte en interieur", "Proefrit, minstens 20 minuten"]
    body = f"""<h1>Checklist tweedehands auto kopen</h1>
<p class="intro">Vink af wat u heeft gecontroleerd. Doe vooraf de gratis kentekencheck op www.autoservicebarneveld.nl/kentekencheck en neem deze lijst mee naar de bezichtiging.</p>
<div class="kolommen"><div>{"".join(blok(k, C[k]) for k in links)}</div><div>{"".join(blok(k, C[k]) for k in rechts)}</div></div>
<div class="nieuwe-pagina kolommen">
<div>{blok("Papieren en overschrijven", C["Papieren en overschrijven"])}<div class="blok" style="margin-top:5mm">{blok("Neem mee naar de aankoopkeuring", bouw.MEENEMEN)}</div></div>
<div><div class="blok" style="margin-top:5mm">{blok("Betalen via de bank", C["Betalen via de bank"])}</div></div>
</div>
<h2>Waar heeft u recht op?</h2>
<div class="rechten">{"".join(f'<div class="blok"><h3>{e(k)}</h3><p>{e(t)}</p></div>' for k, t in bouw.RECHTEN)}</div>
<h2>Veelvoorkomende misverstanden</h2>
<dl class="misverstanden">{"".join(f"<div><dt>{e(k)}</dt><dd>{e(t)}</dd></div>" for k, t in bouw.MISVERSTANDEN)}</dl>
<div class="te-mooi"><h2>Te mooi om waar te zijn?</h2>
<p><strong>Als iets te mooi lijkt om waar te zijn, is dat vaak ook zo.</strong> Wees extra voorzichtig als:</p>{lijst(bouw.TE_MOOI, "lijst-let-op")}</div>
<div class="kader"><strong>Twijfelt u? Laat de auto even nakijken.</strong> Autoservice Barneveld is onafhankelijk: we verkopen zelf geen auto's en vertellen u eerlijk wat we zien. Op de brug, uitlezen en een proefrit. Bel of app {bouw.TEL}.</div>
<p class="noot">Algemene informatie, geen juridisch advies. Twijfelt u over uw rechten? Kijk op ConsuWijzer of vraag het Juridisch Loket.</p>"""
    return pagina("Checklist tweedehands auto kopen", body)


def voorbereiding():
    (k1, vooraf), (k2, mee) = bouw.VOORBEREIDING
    body = f"""<div class="ruim">
<h1>Voorbereiding op uw aankoopkeuring</h1>
<p class="intro">Fijn dat u de auto door ons laat nakijken. Het technische deel doen wij: op de brug, uitlezen en een proefrit. Met deze lijst regelt u vooraf de rest, zodat u na de keuring meteen een besluit kunt nemen.</p>
<h2>{e(k1)}</h2>{lijst(vooraf)}
<h2>{e(k2)}</h2>
<p>Hoe meer we weten, hoe beter ons advies. Neem alles mee wat er is:</p>{lijst(mee)}
<div class="kader"><strong>Uitgebreidere checklist nodig?</strong> Op www.autoservicebarneveld.nl/checklist-tweedehands-auto vindt u ook waar u bij de bezichtiging op let, hoe u veilig betaalt en waar u recht op heeft.</div>
<p class="groet">Tot ziens in de werkplaats,<strong>Matthijs de Wilde</strong>Autoservice Barneveld</p>
</div>"""
    return pagina("Voorbereiding op uw aankoopkeuring", body)


def maak(html, naam, pg):
    tmp = ROOT / "bron" / "_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(300)
    doel = ROOT / "downloads" / naam
    doel.parent.mkdir(exist_ok=True)
    pg.pdf(path=str(doel), format="A4", print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template="<span></span>", footer_template=VOET)
    tmp.unlink()
    print("geschreven", doel.relative_to(ROOT))


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    maak(checklist(), "checklist-tweedehands-auto.pdf", pg)
    maak(voorbereiding(), "voorbereiding-aankoopkeuring.pdf", pg)
    b.close()
