"""Maakt downloads/checklist-tweedehands-auto.pdf uit dezelfde tekst als de webpagina.

Gebruik:  python3 bron/maak_pdf.py   (na bron/bouw.py; vraagt Playwright met Chromium)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bouw  # noqa: E402

ROOT = bouw.ROOT
fonts = (ROOT / "fonts").as_uri()

def blok(k, items):
    return f'<section><h2>{bouw.e(k)}</h2><ul class="checklijst">' + "".join(f"<li>{bouw.e(i)}</li>" for i in items) + "</ul></section>"


C = bouw.CHECKLIST + [("Neem mee naar de aankoopkeuring", bouw.MEENEMEN)]
links, rechts = [C[0], C[1], C[4]], [C[2], C[3], C[5]]
kolommen = "<div>" + "".join(blok(*b) for b in links) + "</div><div>" + "".join(blok(*b) for b in rechts) + "</div>"

html = f"""<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><title>Checklist tweedehands auto kopen</title>
<style>
@font-face {{ font-family: "Montserrat"; src: url("{fonts}/montserrat.woff2") format("woff2"); font-weight: 300 900; }}
@font-face {{ font-family: "Bebas Neue"; src: url("{fonts}/bebas-neue.woff2") format("woff2"); }}
@page {{ size: A4; margin: 14mm 15mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Montserrat, Arial, sans-serif; font-size: 9pt; line-height: 1.38; color: #404042; }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #e7814d; padding-bottom: 8px; margin-bottom: 10px; }}
header img {{ width: 120px; }}
header p {{ margin: 0; text-align: right; font-size: 8.5pt; color: #666668; }}
h1 {{ font-family: "Bebas Neue", sans-serif; font-weight: 400; font-size: 30pt; line-height: 1; color: #0a467f; margin: 6px 0 2px; }}
.intro {{ margin: 0 0 6px; }}
h2 {{ font-family: "Bebas Neue", sans-serif; font-weight: 400; font-size: 17pt; color: #0a467f; margin: 12px 0 3px; break-after: avoid; }}
h3 {{ margin: 0 0 3px; font-size: 10.5pt; color: #0a467f; }}
p {{ margin: 0 0 6px; }}
ul {{ list-style: none; margin: 0; padding: 0; }}
.checklijst li {{ position: relative; padding: 2.5px 0 2.5px 20px; break-inside: avoid; }}
.checklijst li::before {{ content: ""; position: absolute; left: 0; top: 4px; width: 11px; height: 11px; border: 1.5px solid #6c90b2; border-radius: 2px; }}
.kolommen {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 9mm; }}
.rechten {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.rechten > div {{ border: 1px solid #d9d9d9; border-radius: 6px; padding: 8px 10px; }}
.misverstanden {{ margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 10px; }}
.misverstanden > div {{ border-left: 3px solid #9db5cc; background: #f4f6f9; padding: 6px 9px; break-inside: avoid; }}
.misverstanden dt {{ font-weight: 700; }}
.misverstanden dd {{ margin: 1px 0 0; font-size: 9pt; }}
.te-mooi {{ margin-top: 12px; padding: 10px 14px; border-left: 4px solid #e7814d; background: #fff3e3; border-radius: 0 6px 6px 0; break-inside: avoid; }}
.te-mooi h2 {{ margin-top: 0; }}
.lijst-let-op {{ columns: 2; column-gap: 8mm; }}
.lijst-let-op li {{ position: relative; padding: 2px 0 2px 16px; }}
.lijst-let-op li::before {{ content: "!"; position: absolute; left: 0; top: 3px; width: 11px; height: 11px; border-radius: 50%; background: #e7814d; color: #fff; font-size: 7pt; font-weight: 800; text-align: center; line-height: 11px; }}
.klein-noot {{ font-size: 8pt; color: #666668; margin-top: 8px; }}
.pagina2 {{ break-before: page; }}
footer {{ margin-top: 12px; padding-top: 8px; border-top: 1px solid #d9d9d9; font-size: 8.5pt; color: #666668; display: flex; justify-content: space-between; }}
footer strong {{ color: #0a467f; }}
</style></head><body>
<header><img src="{(ROOT / 'img' / 'logo.svg').as_uri()}" alt="Autoservice Barneveld">
<p>{bouw.ADRES}, {bouw.POSTCODE_PLAATS}<br>{bouw.TEL} · {bouw.MAIL}<br>www.autoservicebarneveld.nl</p></header>
<h1>Checklist tweedehands auto kopen</h1>
<p class="intro">Vink af wat u heeft gecontroleerd. Doe vooraf de gratis kentekencheck op www.autoservicebarneveld.nl/kentekencheck en neem deze lijst mee naar de bezichtiging.</p>
<div class="kolommen">{kolommen}</div>
<div class="pagina2">
<h2>Waar heeft u recht op?</h2>
<div class="rechten">{"".join(f"<div><h3>{bouw.e(k)}</h3><p>{bouw.e(t)}</p></div>" for k, t in bouw.RECHTEN)}</div>
<h2>Veelvoorkomende misverstanden</h2>
<dl class="misverstanden">{"".join(f"<div><dt>{bouw.e(k)}</dt><dd>{bouw.e(t)}</dd></div>" for k, t in bouw.MISVERSTANDEN)}</dl>
<div class="te-mooi"><h2>Te mooi om waar te zijn?</h2>
<p><strong>Als iets te mooi lijkt om waar te zijn, is dat vaak ook zo.</strong> Wees extra voorzichtig als:</p>
<ul class="lijst-let-op">{"".join(f"<li>{bouw.e(i)}</li>" for i in bouw.TE_MOOI)}</ul></div>
<h2>Twijfelt u? Laat de auto even nakijken</h2>
<p>Autoservice Barneveld is een onafhankelijke garage: we verkopen zelf geen auto's en vertellen u eerlijk wat we zien. Bij een aankoopkeuring bekijken we de auto op de brug, lezen we de elektronica uit en maken we een proefrit. Bel of app {bouw.TEL} of plan uw afspraak via de website.</p>
<p class="klein-noot">Deze checklist is algemene informatie en geen juridisch advies. Twijfelt u over uw rechten? Kijk op ConsuWijzer of vraag het Juridisch Loket. Een aankoopkeuring is een momentopname en geen garantie.</p>
<footer><span><strong>Autoservice Barneveld</strong> · zelfstandige garage voor alle merken</span><span>{bouw.TEL} · www.autoservicebarneveld.nl</span></footer>
</div>
</body></html>"""

tmp = ROOT / "bron" / "_checklist.html"
tmp.write_text(html, encoding="utf-8")
from playwright.sync_api import sync_playwright  # noqa: E402
doel = ROOT / "downloads" / "checklist-tweedehands-auto.pdf"
doel.parent.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(300)
    pg.pdf(path=str(doel), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
tmp.unlink()
print("geschreven", doel.relative_to(ROOT))
