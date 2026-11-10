"""Who is Nakheel carousel: 6 tweet-card slides (1080x1350) for Instagram, same design as the Palm Springs carousel.

Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
Every price and date comes from Nakheel's launch brochure (src/prices.jpg, src/payment.jpg).
Text markup: **bold**, __underline__, *italic*.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')

NAME = 'Omar Akthar'
HANDLE = '@omarakthar.in'
PHONE = '+971 56 837 6676'
RENDERS = "Renders: Nakheel, artist's impressions"
BROCHURE = "Prices and payment plan: Nakheel launch brochure"


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t


MAPS = "Map: OpenStreetMap contributors"
SOURCES = "Nakheel facts: public company records and press coverage"
SLIDES = [
    {'img': 'aerial_sunset', 'size': 48, 'swipe': True, 'note': RENDERS,
     'paras': ["**One of Dubai's hottest launches right now.**",
               "A government-backed developer. Villas next to __Palm Jebel Ali__. And a price per sq ft *most people won't believe.*"],
     'alert': "**Busy? Save or share this now** so you can come back to it later."},
    {'img': 'map_coast', 'size': 46, 'note': MAPS,
     'paras': ["**Who is Nakheel?**",
               "The government-owned developer that *built new land* off Dubai's coast.",
               "Since __2003__, it has shaped Dubai's skyline and shoreline. Today it is part of **Dubai Holding**."]},
    {'img': 'map_landbank', 'size': 46,
     'note': "Highlighted: Dubai Holding Real Estate communities · Map: OpenStreetMap contributors",
     'paras': ["**Who's behind them?**",
               "Owned by the Government of Dubai through **Dubai Holding**, the Ruler's investment group.",
               "Their land bank includes *entire islands* and a total of __752 million sq ft__ across Dubai."]},
    {'img': 'map_communities', 'size': 40, 'note': MAPS,
     'paras': ["**What they've built**"],
     'bullets': ["**Palm Jumeirah**, The World Islands, Dubai Islands", "Jumeirah Islands, Jumeirah Park, Jumeirah Village",
                 "Ibn Battuta Mall, Dragon Mart",
                 "Now building: **Palm Jebel Ali**, Palm Springs, Como Residences and much more"]},
    {'img': 'map_location', 'size': 42, 'note': MAPS,
     'paras': ["**Now: Palm Springs.**",
               "Nakheel's new townhouse and villa community in Jebel Ali, right beside __Palm Jebel Ali__.",
               "In Dubai's growth corridor, next to **Al Maktoum Airport** and Jebel Ali Port."]},
    {'img': 'villas_dusk', 'size': 36,
     'note': "Palm Springs: brochure price ÷ published floor-plan size (2,326 sq ft) · Others: 2026 market data and recent releases",
     'paras': ["**Price per sq ft** (AED)"],
     'table': [('Emirates Hills', '~3,500'), ('Palm Jebel Ali', '~2,650'), ('The Springs', '~2,300'), ('Dubai villa average', '2,241'),
               ('Damac Islands', '~1,850'), ('**Palm Springs 3-bed townhouse**', '~1,634')],
     'paras2': ["Beside Palm Jebel Ali, for *less per sq ft than The Springs.*"]},
    {'img': 'living_pool', 'size': 34,
     'note': "1 AED = ₹25.57 (10 Nov 2026) · Rupee amounts move with the exchange rate · Excludes 4% DLD fee",
     'paras': ["**3-bed townhouse: AED 3.8M** (≈ ₹9.72 Cr)"],
     'rows3': [('On booking · **10%**', '380K', '₹97.2 L'), ('April 2027 · **10%**', '380K', '₹97.2 L'), ('September 2027 · **10%**', '380K', '₹97.2 L'), ('February 2028 · **10%**', '380K', '₹97.2 L'), ('July 2028 · **10%**', '380K', '₹97.2 L'), ('December 2028 · **5%**', '190K', '₹48.6 L'), ('May 2029 · **5%**', '190K', '₹48.6 L'), ('On handover · **40%**', '1.52M', '₹3.89 Cr')]},
    {'img': 'pool_club', 'size': 50, 'note': RENDERS,
     'paras': ["Want the Palm Springs price list, floor plans and EOI details?", "Comment **PALM SPRINGS**."]},
]
PLAN = [(10, 'Booking'), (10, 'Apr 27'), (10, 'Sep 27'), (10, 'Feb 28'), (10, 'Jul 28'), (5, 'Dec 28'), (5, 'May 29'), (40, 'Oct 30')]


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('alert'):
        icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M6 2h12a1 1 0 0 1 1 1v19l-7-4.5L5 22V3a1 1 0 0 1 1-1z"/></svg>'
        body += f'<div class="alert">{icon}<p>{md(s["alert"])}</p></div>'
    if s.get('table'):
        rows = ''.join(f'<div class="row{" hi" if a.startswith("**") else ""}"><span>{md(a)}</span><b>{b}</b></div>' for a, b in s['table'])
        body += f'<div class="table">{rows}</div>'
    if s.get('rows3'):
        r3 = ''.join(f'<div class="r3{" hi" if a.startswith(("On booking", "On handover")) else ""}"><span>{md(a)}</span><b>{b}</b><em>{c}</em></div>' for a, b, c in s['rows3'])
        body += f'<div class="t3"><div class="r3 h"><span>Instalment</span><b>AED</b><em>INR</em></div>{r3}</div>'
    if s.get('bullets'):
        body += '<ul>' + ''.join(f'<li>{md(b)}</li>' for b in s['bullets']) + '</ul>'
    if s.get('paras2'):
        body += ''.join(f'<p class="gap">{md(p)}</p>' for p in s['paras2'])
    if s.get('bullets2'):
        body += '<ul>' + ''.join(f'<li>{md(b)}</li>' for b in s['bullets2']) + '</ul>'
    if s.get('plan'):
        segs = ''.join(f'<div class="seg{" big" if p == 40 else ""}" style="flex:{p}"><b>{p}%</b><span>{l}</span></div>' for p, l in PLAN)
        body += f'<div class="plan">{segs}</div>'
    swipe = '<div class="swipe">Swipe &rarr;</div>' if s.get('swipe') else ''
    return f'''
<section class="slide" id="s{i + 1}">
  <div class="photo" style="background-image:url('img/{s['img']}.jpg')"></div>
  <div class="fade"></div>
  {swipe}
  <div class="card" style="--fs:{s['size']}px">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg></div><div class="handle">{HANDLE}</div></div></div>
    <div class="body">{body}</div>
  </div>
  <div class="note">{html.escape(s['note'])}</div>
  <div class="count">{i + 1}/{len(SLIDES)}</div>
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; background: #000; }}
.photo {{ position: absolute; left: 0; right: 0; top: 0; height: 800px; background-size: cover; background-position: center; }}
.fade {{ position: absolute; left: 0; right: 0; top: 480px; height: 340px; background: linear-gradient(rgba(0,0,0,0), #000); }}
.swipe {{ position: absolute; right: 44px; top: 40px; background: rgba(0,0,0,0.45); color: #fff; font-weight: 600; font-size: 26px;
  padding: 10px 22px; border-radius: 40px; letter-spacing: 0.02em; }}
.card {{ position: absolute; left: 84px; right: 84px; bottom: 120px; background: #fff; border-radius: 34px; padding: 46px 52px 50px; color: #111; }}
.who {{ display: flex; align-items: center; gap: 26px; margin-bottom: 30px; }}
.who img {{ width: 128px; height: 128px; border-radius: 50%; }}
.name {{ font-weight: 700; font-size: 44px; letter-spacing: -0.01em; display: flex; align-items: center; gap: 10px; }}
.tick {{ width: 40px; height: 40px; flex: none; }}
.alert {{ margin-top: 30px; display: flex; align-items: center; gap: 22px; padding: 24px 30px; border-radius: 26px;
  background: linear-gradient(135deg, #FF3B3B, #E0115F); color: #fff; box-shadow: 0 14px 34px rgba(224, 17, 95, 0.38); }}
.alert svg {{ width: 50px; height: 50px; flex: none; }}
.alert p {{ font-size: 0.9em; line-height: 1.22; }}
.alert b {{ font-weight: 700; }}
.body p.gap {{ margin-top: 0.8em; }}
.handle {{ font-weight: 400; font-size: 32px; color: #5B6470; margin-top: 2px; }}
.body {{ font-size: var(--fs); line-height: 1.24; font-weight: 400; }}
.body p {{ text-wrap: pretty; }}
.body p + p {{ margin-top: 0.55em; }}
.body b {{ font-weight: 700; }}
.body u {{ text-decoration-thickness: 2px; text-underline-offset: 6px; }}
.table {{ margin-top: 22px; display: grid; gap: 14px; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1.5px solid #E6E8EC; padding-bottom: 12px; font-size: 36px; }}
.row b {{ font-size: 44px; font-variant-numeric: tabular-nums; }}
.t3 {{ margin-top: 16px; display: grid; gap: 0; }}
.r3 {{ display: grid; grid-template-columns: 1fr auto 150px; gap: 18px; align-items: baseline; padding: 9px 0; border-bottom: 1.5px solid #E6E8EC; font-size: 29px; }}
.r3 b {{ font-size: 32px; font-variant-numeric: tabular-nums; text-align: right; }}
.r3 em {{ font-style: normal; color: #4A5260; font-variant-numeric: tabular-nums; text-align: right; }}
.r3:not(.h):not(.hi) {{ font-size: 25px; padding: 7px 0; color: #3A414C; }}
.r3:not(.h):not(.hi) b {{ font-size: 27px; }}
.r3.hi {{ font-size: 34px; background: #FFF6D6; margin: 6px -14px; padding: 12px 14px; border-radius: 12px; border-bottom: none; }}
.r3.hi b {{ font-size: 40px; }} .r3.hi em {{ color: #111; font-weight: 600; }}
.r3.h {{ font-size: 18px; letter-spacing: 0.14em; text-transform: uppercase; color: #8A9099; padding-top: 0; }}
.r3.h b {{ font-size: 18px; }} .r3.h em {{ color: #8A9099; }}
.row.hi {{ background: #FFF6D6; margin: 0 -14px; padding: 8px 14px 12px; border-radius: 10px; border-bottom: none; }}
ul {{ margin-top: 18px; padding-left: 1.1em; display: grid; gap: 14px; }}
li::marker {{ color: #111; }}
.plan {{ display: flex; gap: 6px; margin-top: 30px; height: 110px; }}
.seg {{ background: #EEF0F3; border-radius: 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; min-width: 0; }}
.seg b {{ font-size: 24px; }} .seg span {{ font-size: 15px; color: #5B6470; margin-top: 4px; white-space: nowrap; }}
.seg.big {{ background: #111; color: #fff; }} .seg.big span {{ color: #C9CDD3; }}
.note {{ position: absolute; left: 84px; right: 84px; bottom: 62px; color: #8A9099; font-size: 20px; text-align: center; }}
.count {{ position: absolute; right: 44px; bottom: 60px; color: #5B6470; font-size: 20px; font-weight: 600; }}
</style></head><body>
{''.join(slide_html(i, s) for i, s in enumerate(SLIDES))}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html', len(SLIDES), 'slides')
