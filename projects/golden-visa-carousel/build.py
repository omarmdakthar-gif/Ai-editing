"""UAE Golden Visa carousel: 8 tweet-card slides (1080x1350) for Instagram, same card design as the other carousels.

Slides 1-6 keep the country secret ("this country"), so their visuals are neutral gold-on-navy icons drawn here in SVG.
Slide 7 reveals the UAE Golden Visa over the Dubai skyline (Unsplash photo).
Facts: UAE Ministry of Foreign Affairs consular services for Golden Visa holders (Oct 2025); see post.md for sources.
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
INK = '#D6E6FF'
GOLD = '#FFC940'
MOFA = 'Source: UAE Ministry of Foreign Affairs, consular services for Golden Visa holders'


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)
    return t.replace('\n', '<br>')


# ---------- gold icon art (viewBox 1080 x 800; the card covers roughly y > 520) ----------
G = f'stroke="{GOLD}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"'
G2 = f'stroke="{GOLD}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"'


def scene(svg, chip=''):
    c = f'<div class="chip">{chip}</div>' if chip else ''
    return f'<div class="gv"><svg viewBox="0 0 1080 800" class="gv-svg">{svg}</svg>{c}</div>'


def passport(x, y, s=1.0, rot=0):
    return f"""<g transform="translate({x} {y}) rotate({rot}) scale({s})">
      <rect x="-120" y="-165" width="240" height="330" rx="22" fill="#0E1E3F" {G}/>
      <circle cx="0" cy="-20" r="62" {G2}/><ellipse cx="0" cy="-20" rx="26" ry="62" {G2}/>
      <path d="M-62 -20 H62 M-55 -50 H55 M-55 10 H55" {G2}/>
      <rect x="-60" y="78" width="120" height="16" rx="8" fill="{GOLD}" opacity="0.8"/>
      <rect x="-40" y="108" width="80" height="10" rx="5" fill="{GOLD}" opacity="0.45"/></g>"""


def art_cover():
    return scene(passport(430, 300, 1.05, -8) +
                 f'<circle cx="680" cy="250" r="105" fill="{GOLD}"/><text x="680" y="292" class="q">?</text>')


def art_evac():
    return scene(f"""<circle cx="540" cy="300" r="190" {G2} opacity="0.9"/>
      <ellipse cx="540" cy="300" rx="80" ry="190" {G2} opacity="0.6"/><ellipse cx="540" cy="300" rx="150" ry="190" {G2} opacity="0.35"/>
      <path d="M350 300 H730 M380 200 H700 M380 400 H700" {G2} opacity="0.5"/>
      <path d="M300 420 Q540 40 800 300" stroke="{GOLD}" stroke-width="6" fill="none" stroke-dasharray="4 18" stroke-linecap="round"/>
      <circle cx="300" cy="420" r="16" fill="{GOLD}"/>
      <g transform="translate(800 300) rotate(60)"><path d="M0 -46 L10 -12 L46 6 L46 16 L10 8 L8 34 L20 44 L20 52 L0 46 L-20 52 L-20 44 L-8 34 L-10 8 L-46 16 L-46 6 L-10 -12 Z" fill="{GOLD}"/></g>""",
                 'Included in emergency evacuation plans')


def art_passport30():
    return scene(passport(420, 300, 1.0, -6) + f"""
      <circle cx="680" cy="300" r="130" fill="#0E1E3F" {G}/>
      <path d="M680 300 V215 M680 300 L740 335" {G}/><rect x="660" y="148" width="40" height="22" rx="6" fill="{GOLD}"/>
      <text x="680" y="400" class="mins">30 MIN</text>""", 'Free return document')


def art_hotline():
    return scene(f"""
      <rect x="440" y="90" width="200" height="380" rx="36" fill="#0E1E3F" {G}/>
      <rect x="510" y="112" width="60" height="10" rx="5" fill="{GOLD}" opacity="0.7"/>
      <text x="540" y="300" class="big">24/7</text>
      <path d="M690 210 q30 70 0 140 M730 180 q50 100 0 200 M390 210 q-30 70 0 140 M350 180 q-50 100 0 200" {G2} opacity="0.8"/>""",
                 'Direct line to the Foreign Ministry')


def art_ten():
    return scene(f"""
      <rect x="380" y="110" width="320" height="320" rx="30" fill="#0E1E3F" {G}/>
      <path d="M380 190 H700" {G}/><path d="M460 80 V140 M620 80 V140" {G}/>
      <text x="540" y="360" class="ten">10</text><text x="540" y="410" class="yrs">YEARS</text>""",
                 'No employer · No sponsor · No job needed')


def person(x, y, s):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-70" r="34" fill="{GOLD}"/><path d="M-55 40 Q-55 -25 0 -25 Q55 -25 55 40 Z" fill="{GOLD}"/></g>'


def art_family():
    return scene(f"""
      <path d="M540 70 L780 150 V290 C780 410 680 470 540 500 C400 470 300 410 300 290 V150 Z" fill="rgba(255,201,64,0.08)" {G}/>
      {person(455, 330, 1.0)}{person(625, 330, 1.0)}{person(540, 390, 0.62)}""", 'You, your spouse and your children')


SLIDES = [
    {'art': art_cover(), 'size': 48, 'swipe': True, 'note': ' ',
     'paras': ["**India doesn't allow dual citizenship.**", "So smart Indians are doing ==**this**== instead."],
     'alert': "**Save this,** you'll need it later."},
    {'art': art_evac(), 'size': 44, 'note': MOFA,
     'paras': ["**Stuck in another country during a war, disaster or crisis?**",
               "This country includes you in its __emergency evacuation plans__, through its embassies around the world.",
               "*Even though you're not their citizen.*"]},
    {'art': art_passport30(), 'size': 44, 'note': MOFA,
     'paras': ["**Lost your passport abroad? Damaged it?**",
               "This country issues you a **free return document** in just __30 minutes__, so you can fly back home to that country."]},
    {'art': art_hotline(), 'size': 44, 'note': MOFA,
     'paras': ["**A 24/7 government hotline, just for you.**",
               "Wherever you are in the world, one call gets you direct help from the country's __Ministry of Foreign Affairs__."]},
    {'art': art_ten(), 'size': 40, 'note': ' ',
     'paras': ["It's valid for **10 years**, and renewable as long as you meet the requirements.",
               "**No employer. No sponsor. No job needed.**",
               "And unlike normal visas, it __doesn't get cancelled__ if you stay outside the country for more than 6 months."]},
    {'art': art_family(), 'size': 44, 'note': MOFA,
     'paras': ["It lets you **sponsor your spouse and children** too.",
               "And this protection abroad covers your __registered family members__ as well."]},
    {'img': 'skyline', 'size': 38, 'note': '1 AED = ₹25.70 (16 Nov 2026) · Subject to DLD valuation and GDRFA approval',
     'paras': ["This is the ==**UAE Golden Visa.**==",
               "One way to get it: own property worth **AED 2M** (≈ ₹5.14 Cr) in Dubai."],
     'checks': ["You're eligible the moment you **complete the down payment** on an off-plan property",
                "**Mortgaged** property works",
                "**Multiple properties** can be combined"]},
    {'img': 'skyline', 'pos': '85% center', 'size': 44, 'note': ' ',
     'paras': ["Want a **free consultation** on Dubai real estate and how to get a Golden Visa?",
               "Comment ==**GOLDEN VISA**== and I'll send it to your DMs."]},
]

WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def slide_html(i, s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    if s.get('alert'):
        icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M6 2h12a1 1 0 0 1 1 1v19l-7-4.5L5 22V3a1 1 0 0 1 1-1z"/></svg>'
        body += f'<div class="alert">{icon}<p>{md(s["alert"])}</p></div>'
    if s.get('checks'):
        body += '<ul class="checks">' + ''.join(f'<li><span class="ck">✓</span><span>{md(c)}</span></li>' for c in s['checks']) + '</ul>'
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
.gv {{ position: absolute; inset: 0; background: radial-gradient(90% 75% at 50% 30%, #1A2F5E 0%, #0A1430 60%, #050A1A 100%); }}
.gv::before {{ content: ''; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,201,64,0.16) 1.5px, transparent 1.5px); background-size: 34px 34px; opacity: 0.6; }}
.gv-svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.q {{ fill: #0A1430; font: 800 130px Outfit, sans-serif; text-anchor: middle; }}
.mins {{ fill: {GOLD}; font: 800 44px Outfit, sans-serif; text-anchor: middle; letter-spacing: 0.04em; }}
.big {{ fill: {GOLD}; font: 800 84px Outfit, sans-serif; text-anchor: middle; }}
.ten {{ fill: {GOLD}; font: 800 150px Outfit, sans-serif; text-anchor: middle; }}
.yrs {{ fill: {GOLD}; font: 700 34px Outfit, sans-serif; text-anchor: middle; letter-spacing: 0.3em; }}
.chip {{ position: absolute; left: 50%; top: 506px; transform: translateX(-50%); white-space: nowrap; padding: 12px 28px; border-radius: 40px;
  background: rgba(255,201,64,0.14); border: 2px solid rgba(255,201,64,0.55); color: #FFE7A6; font-weight: 600; font-size: 28px; }}
.checks {{ list-style: none; margin-top: 20px; display: grid; gap: 14px; }}
.checks li {{ display: flex; gap: 18px; align-items: flex-start; }}
.checks .ck {{ flex: none; width: 46px; height: 46px; border-radius: 50%; background: #2ECC71; color: #fff; font-weight: 800; font-size: 26px; display: grid; place-items: center; margin-top: -2px; }}
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
