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
    {'img': 'map_coast', 'size': 46, 'swipe': True, 'note': MAPS,
     'paras': ["**Who is Nakheel?**",
               "The government-owned developer that *built new land* off Dubai's coast.",
               "Since __2003__, it has shaped Dubai's skyline and shoreline. Today it is part of **Dubai Holding**."]},
    {'img': 'map_communities', 'size': 40, 'note': MAPS,
     'paras': ["**What they've built**"],
     'bullets': ["**Palm Jumeirah**, The World Islands, Dubai Islands", "Jumeirah Islands, Jumeirah Park, Jumeirah Village",
                 "Ibn Battuta Mall, Dragon Mart",
                 "Now building: **Palm Jebel Ali**, Palm Springs, Como Residences and much more"]},
    {'img': 'map_landbank', 'size': 50,
     'note': "Highlighted: Dubai Holding Real Estate communities · Map: OpenStreetMap contributors",
     'paras': ["**Who's behind them?**",
               "Owned by the Government of Dubai through **Dubai Holding**, the Ruler's investment group."]},
    {'img': 'aerial_sunset', 'size': 44, 'note': RENDERS,
     'paras': ["**Now: Palm Springs.**",
               "Nakheel's new townhouse and villa community in Jebel Ali, right beside __Palm Jebel Ali__.",
               "3 and 4-bed townhouses, 4 and 5-bed villas, on an easy **60/40** payment plan."]},
    {'img': 'villas_dusk', 'size': 36,
     'note': "Palm Springs: brochure price ÷ published floor-plan size (2,326 sq ft) · Others: 2026 market data and recent releases",
     'paras': ["**Price per sq ft** (AED)"],
     'table': [('Emirates Hills', '~3,500'), ('Palm Jebel Ali', '~2,650'), ('The Springs', '~2,300'), ('Dubai villa average', '2,241'),
               ('Damac Islands', '~1,850'), ('**Palm Springs 3-bed townhouse**', '~1,634')],
     'paras2': ["Beside Palm Jebel Ali, for *less per sq ft than The Springs.*"]},
    {'img': 'pool_club', 'size': 50, 'note': RENDERS,
     'paras': ["Want the Palm Springs price list, floor plans and EOI details?", "Comment **PALM SPRINGS**."]},
]
PLAN = [(10, 'Booking'), (10, 'Apr 27'), (10, 'Sep 27'), (10, 'Feb 28'), (10, 'Jul 28'), (5, 'Dec 28'), (5, 'May 29'), (40, 'Oct 30')]


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('table'):
        rows = ''.join(f'<div class="row{" hi" if a.startswith("**") else ""}"><span>{md(a)}</span><b>{b}</b></div>' for a, b in s['table'])
        body += f'<div class="table">{rows}</div>'
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
