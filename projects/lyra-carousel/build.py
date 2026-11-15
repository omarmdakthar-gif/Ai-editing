"""Lyra at Ghaf Woods carousel: 6 tweet-card slides (1080x1350) for Instagram, same card design as the other carousels.

Every price, size and payment date comes from Majid Al Futtaim's Lyra factsheet (src/factsheet.pdf).
Renders come from the Lyra digital brochure (artist's impressions). Developer facts: brochure page 36.
Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
Text markup: **bold**, __underline__, *italic*, ==highlight==.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')

NAME = 'Omar Akthar'
HANDLE = '@omarakthar.in'
PHONE = '+971 56 837 6676'
INK = '#D6E6FF'  # only used by leftover blueprint CSS
RENDERS = "Renders: Majid Al Futtaim, artist's impressions"
FACTS = "Prices and payment plan: Majid Al Futtaim Lyra factsheet · Excludes 4% DLD fee"


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)
    return t.replace('\n', '<br>')




def grid_html(g):
    rows = ''.join(f'<div class="gr{" hi" if k in g["hi"] else ""}"><span>{md(a)}</span><em>{b}</em><b>{c}</b></div>'
                   for k, (a, b, c) in enumerate(g['rows']))
    h = g['head']
    return f'<div class="grid{" compact" if g.get("compact") else ""}"><div class="gr h"><span>{h[0]}</span><em>{h[1]}</em><b>{h[2]}</b></div>{rows}</div>'


SLIDES = [
    {'img': 'forest_skyline', 'pos': '30% center', 'size': 46, 'swipe': True, 'note': RENDERS,
     'paras': ["It's been a long time since I found a project around **AED 1 million** that's actually worth it.",
               "==**This is the one.**=="],
     'alert': "**Busy? Save or share this now** so you can come back to it later."},
    {'img': 'aerial_day', 'size': 42, 'note': RENDERS,
     'paras': ["**Lyra at Ghaf Woods**",
               "A new tower of __348 homes__ by Majid Al Futtaim, inside *Dubai's first forest-living community* in Dubailand.",
               "Pool lounge, sky garden, sky lounge, gym, sports court and a podcast studio. **20 mins** to DXB and Mall of the Emirates."]},
    {'img': 'living', 'size': 42, 'note': FACTS,
     'paras': ["**Prices start at __AED 1.19M__.**"],
     'grid': {'head': ('Unit', 'Size', 'From'), 'hi': [0],
              'rows': [('1 bed', '638 sq ft', 'AED 1.19M'), ('1 bed + garden', '859 sq ft', 'AED 1.47M'),
                       ('2 bed', '967 sq ft', 'AED 1.94M'), ('2 bed + garden', '1,325 sq ft', 'AED 2.38M')]}},
    {'img': 'pool', 'size': 34, 'note': FACTS,
     'paras': ["**50/50 payment plan** · 1 bed from AED 1.19M"],
     'grid': {'head': ('Instalment', '%', '1 bed'), 'hi': [0, 8], 'compact': True,
              'rows': [('On booking · Nov 2026', '10%', 'AED 119K'), ('March 2027', '5%', 'AED 59.5K'), ('July 2027', '5%', 'AED 59.5K'),
                       ('December 2027', '5%', 'AED 59.5K'), ('May 2028', '10%', 'AED 119K'), ('October 2028', '5%', 'AED 59.5K'),
                       ('March 2029', '5%', 'AED 59.5K'), ('July 2029', '5%', 'AED 59.5K'), ('On completion', '50%', 'AED 595K')]}},
    {'img': 'aerial_night', 'size': 42, 'note': "Developer facts: Majid Al Futtaim · " + RENDERS.split(': ')[1],
     'paras': ["**Who's behind it?**",
               "**Majid Al Futtaim**, the group behind **Mall of the Emirates**, the **City Centre** malls, **Ski Dubai** and **VOX Cinemas**.",
               "Since __1992__. Their communities are already home to **2,500+ families** across the UAE, Oman and Lebanon."]},
    {'img': 'terrace', 'size': 44, 'note': RENDERS,
     'paras': ["Want the floor plans, the full price list and the payment plan?", "Comment **LYRA**, or WhatsApp me:"],
     'cta': PHONE},
]

WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('alert'):
        icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M6 2h12a1 1 0 0 1 1 1v19l-7-4.5L5 22V3a1 1 0 0 1 1-1z"/></svg>'
        body += f'<div class="alert">{icon}<p>{md(s["alert"])}</p></div>'
    if s.get('grid'):
        body += grid_html(s['grid'])
    if s.get('ol'):
        body += '<ol>' + ''.join(f'<li><span class="n">{k + 1}</span><span>{md(b)}</span></li>' for k, b in enumerate(s['ol'])) + '</ol>'
    if s.get('cta'):
        body += f'<div class="wa">{WA}<b>{html.escape(s["cta"])}</b></div>'
    if s.get('paras2'):
        body += ''.join(f'<p class="gap">{md(p)}</p>' for p in s['paras2'])
    swipe = '<div class="swipe">Swipe &rarr;</div>' if s.get('swipe') else ''
    if s.get('art'):
        visual = f'<div class="photo">{s["art"]}</div>'
    else:
        visual = f'<div class="photo" style="background-image:url(\'img/{s["img"]}.jpg\');background-position:{s.get("pos", "center")}"></div>'
    return f'''
<section class="slide" id="s{i + 1}">
  {visual}
  <div class="fade"></div>
  {swipe}
  <div class="card" style="--fs:{s['size']}px">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.210-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.790 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.990 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg></div><div class="handle">{HANDLE}</div></div></div>
    <div class="body">{body}</div>
  </div>
  <div class="note">{html.escape(s['note'])}</div>
  <div class="count">{i + 1}/{len(SLIDES)}</div>
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
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
.handle {{ font-weight: 400; font-size: 32px; color: #5B6470; margin-top: 2px; }}
.body {{ font-size: var(--fs); line-height: 1.26; font-weight: 400; }}
.body p {{ text-wrap: pretty; }}
.body p + p {{ margin-top: 0.55em; }}
.body p.gap {{ margin-top: 0.7em; }}
.body b {{ font-weight: 700; }}
.body u {{ text-decoration-thickness: 2px; text-underline-offset: 6px; }}
.body mark {{ background: #FFD43B; color: #111; font-weight: 600; padding: 0 8px; border-radius: 8px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }}
.alert {{ margin-top: 30px; display: flex; align-items: center; gap: 22px; padding: 24px 30px; border-radius: 26px;
  background: linear-gradient(135deg, #FF3B3B, #E0115F); color: #fff; box-shadow: 0 14px 34px rgba(224, 17, 95, 0.38); }}
.alert svg {{ width: 50px; height: 50px; flex: none; }}
.alert p {{ font-size: 0.9em; line-height: 1.22; }}
ol {{ list-style: none; margin-top: 22px; display: grid; gap: 20px; }}
ol li {{ display: flex; gap: 20px; align-items: flex-start; }}
ol .n {{ flex: none; width: 54px; height: 54px; border-radius: 50%; background: #111; color: #fff; font-weight: 700; font-size: 28px;
  display: grid; place-items: center; margin-top: -4px; }}
.wa {{ margin-top: 22px; display: flex; align-items: center; gap: 20px; padding: 22px 30px; border-radius: 24px; background: #25D366; color: #fff;
  box-shadow: 0 14px 34px rgba(37, 211, 102, 0.35); }}
.wa svg {{ width: 58px; height: 58px; flex: none; }}
.wa b {{ font-size: 50px; letter-spacing: 0.01em; font-variant-numeric: tabular-nums; }}
.grid {{ margin-top: 20px; display: grid; }}
.gr {{ display: grid; grid-template-columns: 1fr 200px 240px; gap: 16px; align-items: baseline; padding: 14px 0; border-bottom: 1.5px solid #E6E8EC; font-size: 34px; }}
.gr em {{ font-style: normal; color: #4A5260; font-variant-numeric: tabular-nums; }}
.gr b {{ white-space: nowrap; text-align: right; font-size: 38px; font-variant-numeric: tabular-nums; }}
.gr.h {{ font-size: 18px; letter-spacing: 0.14em; text-transform: uppercase; color: #8A9099; padding: 0 0 8px; }} .gr.h b {{ font-size: 18px; font-weight: 600; }} .gr.h em {{ color: #8A9099; }}
.gr.hi {{ background: #FFF6D6; margin: 4px -14px; padding: 14px; border-radius: 12px; border-bottom: none; }}
.grid.compact .gr {{ grid-template-columns: 1fr 80px 220px; font-size: 25px; padding: 7px 0; color: #3A414C; }}
.grid.compact .gr b {{ font-size: 27px; }}
.grid.compact .gr.hi {{ font-size: 32px; color: #111; padding: 12px 14px; margin: 6px -14px; }} .grid.compact .gr.hi b {{ font-size: 38px; }} .grid.compact .gr.hi em {{ color: #111; font-weight: 600; }}
.grid.compact .gr.h {{ font-size: 17px; padding: 0 0 6px; }} .grid.compact .gr.h b {{ font-size: 17px; }}
/* blueprint art */
.bp {{ position: absolute; inset: 0; background-color: #0B2F6B;
  background-image: linear-gradient(rgba(214,230,255,0.10) 2px, transparent 2px), linear-gradient(90deg, rgba(214,230,255,0.10) 2px, transparent 2px),
    linear-gradient(rgba(214,230,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(214,230,255,0.05) 1px, transparent 1px);
  background-size: 120px 120px, 120px 120px, 24px 24px, 24px 24px; }}
.bp-svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.rl {{ fill: {INK}; font: 600 19px Outfit, sans-serif; letter-spacing: 0.16em; text-anchor: middle; opacity: 0.85; }}
.dim {{ fill: {INK}; font: 600 22px Outfit, sans-serif; letter-spacing: 0.22em; text-anchor: middle; }}
.dim.red {{ fill: #FF6B78; }}
.arr {{ stroke: #FF4D5E; stroke-width: 6; fill: none; }}
.pills {{ position: absolute; left: 0; right: 0; top: 528px; display: flex; justify-content: center; gap: 16px; }}
.pill {{ display: flex; align-items: center; gap: 10px; padding: 10px 24px 10px 12px; border-radius: 40px; font-weight: 600; font-size: 28px;
  background: rgba(255,255,255,0.12); color: #fff; border: 2px solid rgba(214,230,255,0.35); }}
.pill b {{ width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; font-size: 24px; }}
.pill.ok b {{ background: #2ECC71; }} .pill.q b {{ background: #FFC940; color: #111; }} .pill.bad {{ border-color: #FF4D5E; background: rgba(255,77,94,0.18); }}
.pill.bad b {{ background: #FF4D5E; }}
.tags {{ display: flex; justify-content: center; align-items: flex-start; gap: 34px; padding-top: 60px; }}
.tag {{ width: 330px; background: #fff; border-radius: 26px; padding: 26px 30px 28px; color: #111; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.35); }}
.tag::before {{ content: ''; position: absolute; top: 18px; right: 22px; width: 22px; height: 22px; border-radius: 50%; border: 4px solid #C9D2E0; }}
.tn {{ font-size: 22px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #5B6470; }}
.tp {{ font-size: 54px; font-weight: 800; margin-top: 6px; letter-spacing: -0.01em; }}
.ts {{ font-size: 28px; color: #4A5260; }}
.tline {{ height: 2px; background: #E6E8EC; margin: 16px 0 12px; }}
.tq {{ font-size: 36px; font-weight: 700; }} .tq span {{ font-size: 22px; font-weight: 500; color: #5B6470; margin-left: 6px; }}
.tv {{ display: inline-block; margin-top: 12px; padding: 6px 16px; border-radius: 30px; font-size: 22px; font-weight: 700; }}
.tag.bad .tv {{ background: #FFE3E6; color: #C8102E; }} .tag.good .tv {{ background: #DDF7E7; color: #128A43; }}
.tag.good {{ outline: 5px solid #2ECC71; }}
.vs {{ align-self: center; margin-top: -40px; color: #fff; font-size: 34px; font-weight: 700; opacity: 0.8; }}
.note {{ position: absolute; left: 84px; right: 84px; bottom: 62px; color: #8A9099; font-size: 20px; text-align: center; }}
.count {{ position: absolute; right: 44px; bottom: 60px; color: #5B6470; font-size: 20px; font-weight: 600; }}
</style></head><body>
{''.join(slide_html(i, s) for i, s in enumerate(SLIDES))}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html', len(SLIDES), 'slides')
