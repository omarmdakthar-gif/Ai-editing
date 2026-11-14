"""Architect carousel: 6 tweet-card slides (1080x1350) for Instagram, same card design as the Nakheel carousel.

Story: an architect who designs for Dubai's big developers says one quality-focused developer is shrinking
apartment sizes (not quality) to keep prices affordable. The developer is deliberately NOT named: hearsay only.

Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
Visuals: skyline photo (Unsplash licence), Dubai South map (OpenStreetMap, rendered with the Remotion kit, map1.json),
and blueprint floor plans / price tags drawn here in SVG.
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


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)
    return t.replace('\n', '<br>')


# ---------- blueprint art (viewBox 1080 x 800; the card covers roughly y > 520) ----------
INK = '#D6E6FF'


def rooms(stroke=INK, width=7, label=True):
    """A simple 2-bed apartment, outline x 300..780, y 110..430, plus a balcony."""
    w = f'stroke="{stroke}" stroke-width="{width}" fill="none" stroke-linecap="square"'
    t = lambda x, y, s: f'<text x="{x}" y="{y}" class="rl">{s}</text>' if label else ''
    return f'''
    <rect x="300" y="110" width="480" height="320" {w}/>
    <path d="M520 110 V200 M520 250 V430 M520 270 H600 M650 270 H780 M300 215 H360 M410 215 H520 M420 110 V215" {w}/>
    <rect x="300" y="430" width="220" height="56" stroke="{stroke}" stroke-width="4" stroke-dasharray="12 10" fill="none"/>
    <path d="M360 215 A50 50 0 0 0 410 215" stroke="{stroke}" stroke-width="3" fill="none" opacity="0.7"/>
    {t(360, 170, 'KITCHEN')}{t(470, 170, 'BATH')}{t(410, 340, 'LIVING')}{t(650, 195, 'BED 1')}{t(650, 360, 'BED 2')}{t(410, 466, 'BALCONY')}'''


def pills(items):
    return '<div class="pills">' + ''.join(
        f'<span class="pill {c}"><b>{sym}</b>{lab}</span>' for lab, sym, c in items) + '</div>'


def art_known():
    svg = f'<svg viewBox="0 0 1080 800" class="bp-svg">{rooms()}' \
          f'<path d="M300 80 H780" stroke="{INK}" stroke-width="2"/><path d="M300 70 V90 M780 70 V90" stroke="{INK}" stroke-width="2"/>' \
          f'<text x="540" y="64" class="dim">GENEROUS LAYOUT</text></svg>'
    return '<div class="bp">' + svg + pills([('Quality', '✓', 'ok'), ('Comfort', '✓', 'ok'), ('Size', '?', 'q')]) + '</div>'


def art_shrink():
    k, cx, cy = 0.78, 540, 298
    arrows = ''.join(f'<path d="M{x1} {y1} L{x2} {y2}" class="arr" marker-end="url(#h)"/>' for x1, y1, x2, y2 in
                     [(292, 102, 345, 142), (788, 102, 735, 142), (292, 438, 345, 398), (788, 438, 735, 398)])
    svg = f'''<svg viewBox="0 0 1080 800" class="bp-svg">
      <defs><marker id="h" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
        <path d="M0 0 L10 5 L0 10 z" fill="#FF4D5E"/></marker></defs>
      <rect x="300" y="110" width="480" height="320" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12" fill="none" opacity="0.45"/>
      <g transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">{rooms()}</g>
      {arrows}
      <text x="540" y="78" class="dim red">SAME STANDARD · FEWER SQ FT</text></svg>'''
    return '<div class="bp">' + svg + pills([('Quality', '✓', 'ok'), ('Comfort', '✓', 'ok'), ('Size', '↓', 'bad')]) + '</div>'


def tag(name, price, sqft, ppsf, good):
    c = 'good' if good else 'bad'
    verdict = 'Better value' if good else 'Cheaper tag'
    return f'''<div class="tag {c}"><div class="tn">{name}</div><div class="tp">{price}</div><div class="ts">{sqft}</div>
      <div class="tline"></div><div class="tq">{ppsf}<span>/ sq ft</span></div><div class="tv">{verdict}</div></div>'''


def art_tags():
    return '<div class="bp tags">' + tag('Launch A', 'AED 1.2M', '600 sq ft', 'AED 2,000', False) + \
        '<div class="vs">vs</div>' + tag('Launch B', 'AED 1.4M', '850 sq ft', 'AED 1,647', True) + '</div>'


SLIDES = [
    {'img': 'skyline', 'size': 46, 'swipe': True, 'note': 'Photo: Unsplash',
     'paras': ["Yesterday I bought a car from an **architect in Dubai**.",
               "What he told me about Dubai apartments changed how I look at floor plans, **and showed me a massive opportunity.**"],
     'alert': "**Busy? Save this for later.**"},
    {'img': 'map_south', 'pos': 'center top', 'size': 46, 'note': 'Map: OpenStreetMap contributors · Dubai South area approximate',
     'paras': ["His firm designs for Dubai's biggest developers: **Emaar, Ellington, Sobha and Meraki.**",
               "Right now, he's working on a project in __Dubai South__."]},
    {'art': art_known(), 'size': 46, 'note': 'Illustration, not an actual floor plan',
     'paras': ["The project is from a developer **well known for quality, comfort and generous sizes.**",
               "But on this one, they're letting go of something, ==*and that's where the opportunity lies.*=="]},
    {'art': art_shrink(), 'size': 42, 'note': 'Illustration, not an actual floor plan',
     'paras': ["Construction costs keep rising.",
               "To protect their margins and keep prices affordable, the developer is **making each apartment smaller**, while keeping the same quality and comfort."]},
    {'art': art_tags(), 'size': 36, 'note': 'Illustrative numbers, not real listings',
     'paras': ["**What this means for you**"],
     'ol': ["Units with bigger sizes and layouts will become **scarce, and face more demand.**",
            "When comparing new launches, **check the price per sq ft**, not just the price tag.",
            "A lower price tag can hide a **smaller home.**"]},
    {'img': 'skyline', 'pos': '85% center', 'size': 44, 'note': 'Photo: Unsplash',
     'paras': ["For a transparent, **free consultation** on Dubai real estate, contact me:"],
     'cta': PHONE,
     'paras2': ["**Follow me** for more insights like this."]},
]

WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('alert'):
        icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M6 2h12a1 1 0 0 1 1 1v19l-7-4.5L5 22V3a1 1 0 0 1 1-1z"/></svg>'
        body += f'<div class="alert">{icon}<p>{md(s["alert"])}</p></div>'
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
