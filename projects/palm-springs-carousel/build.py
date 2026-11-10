"""Palm Springs carousel: 9 tweet-card slides (1080x1350) for Instagram.

Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
Every price and date comes from Nakheel's launch brochure (src/prices.jpg, src/payment.jpg).
Text markup: **bold**, __underline__, *italic*.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')

NAME = 'Sanjay Ram'          # confirm with the user
HANDLE = '@sanjayram.dxb'    # confirm with the user
PHONE = '+971 56 837 6676'
RENDERS = "Renders: Nakheel, artist's impressions"
BROCHURE = "Prices and payment plan: Nakheel launch brochure"


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t


SLIDES = [
    {'img': 'aerial_sunset', 'size': 50, 'swipe': True, 'note': RENDERS,
     'paras': ["Nakheel's new villas next to **Palm Jebel Ali** start at __AED 3.8M__.",
               "And you only need *10%* to lock one in.",
               "Here's what to know **before the best units go.**"]},
    {'img': 'aerial_entrance', 'size': 46, 'note': RENDERS,
     'paras': ["**Palm Springs** is Nakheel's new townhouse and villa community in Jebel Ali.",
               "It sits right beside __Palm Jebel Ali__, with access from Sheikh Zayed Road."]},
    {'img': 'villa_front', 'size': 40, 'note': BROCHURE,
     'paras': ["**Starting prices** (AED)"],
     'table': [('3-bed townhouse · G+1', '3.8M'), ('4-bed townhouse · G+1', '4.6M'), ('4-bed townhouse · G+2', '5.2M'),
               ('4-bed villa · G+2', '7.0M'), ('5-bed villa · G+2', '8.9M')]},
    {'img': 'living_pool', 'size': 44, 'note': BROCHURE,
     'paras': ["**60%** during construction. **40%** on handover in __October 2030__."],
     'table': [('On booking', '10%'), ('6 instalments · Apr 2027 to May 2029', '50%'), ('On handover · Oct 2030', '40%')]},
    {'img': 'villas_dusk', 'size': 46, 'note': BROCHURE + " · DLD fee is Dubai's standard 4%",
     'paras': ["On the AED 3.8M townhouse:", "**AED 380,000** on booking, plus the 4% DLD fee.",
               "Then *nothing* until __April 2027__."]},
    {'img': 'aerial_night', 'size': 44, 'note': RENDERS,
     'paras': ["**Why this location?**",
               "Next to Palm Jebel Ali, close to __Jebel Ali Free Zone__, Jebel Ali Port and Al Maktoum Airport.",
               "This is *Dubai's next growth corridor.*"]},
    {'img': 'lagoon_fountain', 'size': 46, 'note': RENDERS,
     'paras': ["Lagoons, parks and landscaped walking trails.", "A **resort-style community** built for *families*."]},
    {'img': 'villas_lagoon', 'size': 42, 'note': RENDERS,
     'paras': ["**Best for:**"],
     'bullets': ["Families upgrading to a villa", "Buyers who want Palm Jebel Ali next door, without island prices",
                 "Investors happy to hold until 2030"]},
    {'img': 'pool_club', 'size': 46, 'note': RENDERS,
     'paras': ["Want the floor plans and the full price list?",
               f"Comment **PALM SPRINGS** or WhatsApp me on __{PHONE}__.", "I'll send you everything."]},
]
PLAN = [(10, 'Booking'), (10, 'Apr 27'), (10, 'Sep 27'), (10, 'Feb 28'), (10, 'Jul 28'), (5, 'Dec 28'), (5, 'May 29'), (40, 'Oct 30')]


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('table'):
        rows = ''.join(f'<div class="row"><span>{html.escape(a)}</span><b>{b}</b></div>' for a, b in s['table'])
        body += f'<div class="table">{rows}</div>'
    if s.get('bullets'):
        body += '<ul>' + ''.join(f'<li>{md(b)}</li>' for b in s['bullets']) + '</ul>'
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
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}</div><div class="handle">{HANDLE}</div></div></div>
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
.name {{ font-weight: 700; font-size: 44px; letter-spacing: -0.01em; }}
.handle {{ font-weight: 400; font-size: 32px; color: #5B6470; margin-top: 2px; }}
.body {{ font-size: var(--fs); line-height: 1.24; font-weight: 400; }}
.body p {{ text-wrap: pretty; }}
.body p + p {{ margin-top: 0.55em; }}
.body b {{ font-weight: 700; }}
.body u {{ text-decoration-thickness: 2px; text-underline-offset: 6px; }}
.table {{ margin-top: 22px; display: grid; gap: 14px; }}
.row {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1.5px solid #E6E8EC; padding-bottom: 12px; font-size: 36px; }}
.row b {{ font-size: 44px; font-variant-numeric: tabular-nums; }}
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
