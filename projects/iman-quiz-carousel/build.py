"""IMAN quiz carousel, slides 1-6: "Spot the render" in 3 rounds (question + answer per round).

Photos: IMAN Developers' own render / real-life marketing images, cropped from screenshots (src/) so that
no third-party labels remain (img/r*a_top.png, img/r*a_bot.png). Our own design: white header with the profile row,
question and round pill, two full-width photos with gold number badges, stamps on the answer slides.
Slides 7-8 (reveal + project) are added once Omar sends the content.
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


def md(text):
    t = html.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'==(.+?)==', r'<mark>\1</mark>', t)
    return t.replace('\n', '<br>')


# Each round: photo 1 and photo 2 (full-width halves of IMAN's comparison images), and which one is the render.
ROUNDS = [
    {'p1': 'f1_bot', 'p2': 'f1_top', 'render': 2},
    {'p1': 'f2_bot', 'p2': 'f2_top', 'render': 1},
    {'p1': 'f3_top', 'p2': 'f3_bot', 'render': 2},
]

SLIDES = [
    {'round': 0, 'answer': False, 'title': "Which one is the **render**? ==**1 or 2**==",
     'sub': "One is a 3D render. The other is the finished lobby. Guess, then swipe."},
    {'round': 0, 'answer': True, 'title': "**Photo 2 was the render.**",
     'sub': "The giveaway: the real lobby has a luggage trolley by the door. Keep score: 1 of 3."},
    {'round': 1, 'answer': False, 'title': "Round 2. Harder. ==**1 or 2?**==",
     'sub': "Same game: one render, one real photo of the same lobby."},
    {'round': 1, 'answer': True, 'title': "**Photo 1 was the render.**",
     'sub': "Tricky one. The render's lighting is just a touch too perfect. Keep score: 2 of 3."},
    {'round': 2, 'answer': False, 'title': "Final round. ==**1 or 2?**==",
     'sub': "Got the first two right? This one decides it."},
    {'round': 2, 'answer': True, 'title': "**Photo 2 was the render.**",
     'sub': "Real marble reflects the room around it. How many did you get? Now see who built all three."},
    {'kind': 'map', 'title': "All 3 are by the same\n==**boutique developer.**==",
     'paras': ["They've handed over __multiple projects on or before the promised\u00a0date__.",
               "Their newest one is in **Dubai Science Park**."]},
]

TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''


def photo(img, num, cls, stamp_html):
    return f'''<div class="ph {cls}" style="background-image:url('img/{img}.jpg')"><div class="num">{num}</div>{stamp_html}</div>'''


def stamp(is_render):
    return '<div class="stamp render">RENDER</div>' if is_render else '<div class="stamp real">REAL ✓</div>'


def map_slide(s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    return f'''
<section class="slide">
  <header class="tall">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE} · Spot the render</div></div><div class="pill">The reveal</div></div>
    <h1>{md(s['title'])}</h1>
    <div class="paras">{body}</div>
  </header>
  <div class="bar"></div>
  <div class="map" style="background-image:url('img/map_dsp.jpg')">
    <div class="ml" style="left:470px;top:44px">Palm Jumeirah</div>
    <div class="rl szr" style="left:300px;top:220px;transform:translate(-50%,-50%) rotate(-2deg)">Sheikh Zayed Road</div>
    <div class="ml" style="right:540px;top:288px">Mall of the Emirates</div>
    <div class="rl" style="left:648px;top:318px;transform:translate(-50%,-50%) rotate(81deg)">Umm Suqeim Rd</div>
    <div class="rl" style="left:790px;top:346px;transform:translate(-50%,-50%) rotate(-27deg)">Al Khail Road</div>
    <div class="ml" style="left:668px;top:432px">Dubai Hills Mall</div>
    <div class="ml" style="left:236px;top:430px">JVC</div>
    <div class="rl" style="left:690px;top:760px">Mohammed Bin Zayed Rd</div>
    <div class="dsp" style="left:624px;top:530px"><b>Dubai Science Park</b><span>Their newest project</span></div>
  </div>
</section>'''


def slide_html(i, s):
    if s.get('kind') == 'map':
        return map_slide(s)
    r = ROUNDS[s['round']]
    st1 = stamp(r['render'] == 1) if s['answer'] else ''
    st2 = stamp(r['render'] == 2) if s['answer'] else ''
    pill = f'<div class="pill">{"Answer · " if s["answer"] else ""}Round {s["round"] + 1}/3</div>'
    return f'''
<section class="slide">
  <header>
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE} · Spot the render</div></div>{pill}</div>
    <h1>{md(s['title'])}</h1>
    <p class="sub">{md(s['sub'])}</p>
  </header>
  {photo(r['p1'], 1, 'p1', st1)}
  <div class="bar"></div>
  {photo(r['p2'], 2, 'p2', st2)}
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; background: #fff; }}
header {{ height: 268px; padding: 26px 44px 0; color: #111; }}
.who {{ display: flex; align-items: center; gap: 18px; }}
.who img {{ width: 74px; height: 74px; border-radius: 50%; }}
.name {{ font-weight: 700; font-size: 32px; display: flex; align-items: center; gap: 8px; }}
.tick {{ width: 30px; height: 30px; }}
.handle {{ font-size: 23px; color: #5B6470; }}
.pill {{ margin-left: auto; padding: 8px 20px; border-radius: 30px; background: #111; color: #FFC940; font-weight: 700; font-size: 23px; letter-spacing: 0.04em; white-space: nowrap; }}
h1 {{ margin-top: 20px; font-size: 50px; font-weight: 600; line-height: 1.12; letter-spacing: -0.01em; }}
h1 b {{ font-weight: 800; }}
h1 mark {{ background: #FFD43B; color: #111; padding: 0 10px; border-radius: 10px; }}
.sub {{ margin-top: 10px; font-size: 27px; line-height: 1.3; color: #4A5260; }}
.ph {{ position: relative; width: 1080px; height: 537px; background-size: cover; background-position: center; }}
.bar {{ height: 8px; background: #FFC940; }}
header.tall {{ height: 525px; }} header.tall h1 {{ font-size: 58px; margin-top: 34px; }}
.paras {{ margin-top: 26px; font-size: 40px; line-height: 1.3; color: #2A2F38; }}
.paras p + p {{ margin-top: 0.5em; }} .paras b {{ font-weight: 700; color: #111; }} .paras u {{ text-decoration-thickness: 2px; text-underline-offset: 5px; }}
.map {{ position: relative; width: 1080px; height: 817px; background-size: cover; background-position: center top; }}
.ml {{ position: absolute; padding: 7px 16px; border-radius: 10px; background: rgba(10,16,32,0.85); border: 1.5px solid rgba(120,200,230,0.6); color: #fff;
  font-weight: 600; font-size: 24px; letter-spacing: 0.02em; white-space: nowrap; }}
.rl {{ position: absolute; color: #C9D6F2; font-weight: 600; font-size: 21px; letter-spacing: 0.14em; text-transform: uppercase; white-space: nowrap;
  text-shadow: 0 0 6px #0A1020, 0 0 12px #0A1020; }}
.rl.szr {{ color: #FFC58A; }}
.gold {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.gold path {{ fill: none; stroke: #FFD43B; stroke-width: 7; stroke-dasharray: 22 12; stroke-linecap: round; filter: drop-shadow(0 0 6px rgba(255,212,59,0.7)); }}
.legend {{ position: absolute; display: flex; align-items: center; gap: 14px; padding: 9px 18px; border-radius: 12px; background: rgba(10,16,32,0.88);
  border: 1.5px solid rgba(255,212,59,0.6); color: #FFE7A6; font-weight: 700; font-size: 22px; letter-spacing: 0.04em; white-space: nowrap; }}
.legend i {{ width: 54px; height: 0; border-top: 6px dashed #FFD43B; }}
.gl {{ position: absolute; padding: 5px 14px; border-radius: 8px; background: #FFD43B; color: #111; font-weight: 700; font-size: 20px; letter-spacing: 0.06em;
  text-transform: uppercase; white-space: nowrap; }}
.dsp {{ position: absolute; display: flex; flex-direction: column; align-items: flex-start; gap: 6px; }}
.dsp b {{ padding: 8px 18px; border-radius: 12px; background: #FFC940; color: #111; font-weight: 800; font-size: 28px; white-space: nowrap; box-shadow: 0 8px 24px rgba(0,0,0,0.45); }}
.dsp span {{ padding: 4px 14px; border-radius: 8px; background: rgba(10,16,32,0.85); color: #FFE7A6; font-weight: 600; font-size: 21px; border: 1.5px solid rgba(255,201,64,0.6); }}
.num {{ position: absolute; left: 28px; top: 24px; width: 88px; height: 88px; border-radius: 50%; background: #FFC940; color: #111; font-weight: 800; font-size: 52px;
  display: grid; place-items: center; box-shadow: 0 8px 22px rgba(0,0,0,0.35); }}
.stamp {{ position: absolute; right: 54px; bottom: 50px; transform: rotate(-8deg); padding: 10px 28px; border: 7px solid; border-radius: 16px;
  font-weight: 800; font-size: 64px; letter-spacing: 0.06em; background: rgba(255,255,255,0.9); white-space: nowrap; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
.stamp.render {{ color: #D7263D; border-color: #D7263D; }}
.stamp.real {{ color: #138A4B; border-color: #138A4B; transform: rotate(6deg); }}
</style></head><body>
{''.join(slide_html(i, s) for i, s in enumerate(SLIDES))}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html', len(SLIDES), 'slides')
