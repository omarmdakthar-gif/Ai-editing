"""IMAN quiz carousel, slides 1-6: "Spot the render" in 3 rounds (question + answer per round).

Photos: IMAN Developers' own render / real-life marketing images, cropped from screenshots (src/) so that
no third-party labels remain (img/r*a_top.png, img/r*a_bot.png). Our own design: two tilted polaroids,
round pill, stamps on the answer slides, and the usual white tweet card.
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


# Each round: photo 1 and photo 2, and which number is the render.
ROUNDS = [
    {'p1': 'r1a_bot', 'p2': 'r1a_top', 'render': 2},
    {'p1': 'r2a_bot', 'p2': 'r2a_top', 'render': 1},
    {'p1': 'r3a_top', 'p2': 'r3a_bot', 'render': 2},
]

SLIDES = [
    {'round': 0, 'answer': False, 'swipe': True,
     'paras': ["**Spot the render.**",
               "One of these is a 3D render. The other is the finished building.",
               "Which one is the render: ==**1 or 2?**== Swipe to find out."]},
    {'round': 0, 'answer': True,
     'paras': ["**Photo 2 was the render.**",
               "The giveaway: the real lobby has a luggage trolley by the door. Renders never bother with those.",
               "Got it right? Keep score: __1 of 3__."]},
    {'round': 1, 'answer': False, 'swipe': True,
     'paras': ["**Round 2. A little harder.**",
               "Same game: one render, one real photo of the same lobby.",
               "Make your guess: ==**1 or 2?**=="]},
    {'round': 1, 'answer': True,
     'paras': ["**Photo 1 was the render.**",
               "Tricky one. The render's lighting is just a touch too perfect, with every vein of marble glowing evenly.",
               "Keep score: __2 of 3__."]},
    {'round': 2, 'answer': False, 'swipe': True,
     'paras': ["**Final round.**",
               "Got the first two? This one decides it.",
               "Which is the render: ==**1 or 2?**=="]},
    {'round': 2, 'answer': True,
     'paras': ["**Photo 2 was the render.**",
               "Real marble reflects the room around it. The render's floor is spotless.",
               "How many did you get? Now see who built all three."]},
]


def polaroid(img, num, cls, stamp=''):
    return f'''<figure class="pol {cls}"><div class="ph" style="background-image:url('img/{img}.png')"></div>
      <figcaption>{num}</figcaption>{stamp}</figure>'''


def stamp(is_render):
    return '<div class="stamp render">RENDER</div>' if is_render else '<div class="stamp real">REAL ✓</div>'


def slide_html(i, s):
    r = ROUNDS[s['round']]
    st1 = stamp(r['render'] == 1) if s['answer'] else ''
    st2 = stamp(r['render'] == 2) if s['answer'] else ''
    pill = f'<div class="pill">{"Answer · " if s["answer"] else ""}Round {s["round"] + 1} of 3</div>'
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    swipe = ''
    dim1 = ' dim' if s['answer'] and r['render'] != 1 else ''
    dim2 = ' dim' if s['answer'] and r['render'] != 2 else ''
    return f'''
<section class="slide">
  <div class="title">SPOT THE <span>RENDER</span></div>
  {pill}
  {polaroid(r['p1'], 1, 'left' + dim1, st1)}
  {polaroid(r['p2'], 2, 'right' + dim2, st2)}
  {swipe}
  <div class="card">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg></div><div class="handle">{HANDLE}</div></div></div>
    <div class="body">{body}</div>
  </div>
  <div class="count">{i + 1}/8</div>
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden;
  background: radial-gradient(80% 60% at 50% 28%, #2A2420 0%, #14110F 55%, #0A0908 100%); }}
.slide::before {{ content: ''; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,0.05) 1.5px, transparent 1.5px); background-size: 30px 30px; }}
.title {{ position: absolute; left: 0; right: 0; top: 46px; text-align: center; color: #fff; font-weight: 800; font-size: 54px; letter-spacing: 0.08em; }}
.title span {{ color: #FFC940; }}
.pill {{ position: absolute; left: 50%; top: 122px; transform: translateX(-50%); padding: 8px 22px; border-radius: 30px; border: 2px solid rgba(255,201,64,0.6);
  color: #FFE7A6; font-weight: 600; font-size: 24px; letter-spacing: 0.06em; white-space: nowrap; }}
.pol {{ position: absolute; top: 196px; width: 468px; background: #FBFAF7; padding: 18px 18px 0; border-radius: 6px;
  box-shadow: 0 24px 50px rgba(0,0,0,0.55); }}
.pol.left {{ left: 52px; transform: rotate(-4deg); }}
.pol.right {{ right: 52px; transform: rotate(3.5deg); top: 214px; }}
.ph {{ width: 432px; height: 418px; background-size: cover; background-position: center; border-radius: 2px; }}
.pol figcaption {{ height: 74px; display: grid; place-items: center; font-weight: 800; font-size: 46px; color: #1B1B1B; }}
.pol.dim .ph {{ filter: saturate(0.85) brightness(0.92); }}
.stamp {{ position: absolute; left: 50%; top: 74%; transform: translate(-50%, -50%) rotate(-10deg); padding: 10px 26px; border: 7px solid; border-radius: 14px;
  font-weight: 800; font-size: 58px; letter-spacing: 0.06em; background: rgba(255,255,255,0.86); white-space: nowrap; }}
.stamp.render {{ color: #D7263D; border-color: #D7263D; }}
.stamp.real {{ color: #138A4B; border-color: #138A4B; transform: translate(-50%, -50%) rotate(8deg); }}
.swipe {{ position: absolute; right: 44px; top: 54px; background: rgba(255,255,255,0.12); color: #fff; font-weight: 600; font-size: 24px; padding: 8px 18px; border-radius: 30px; }}
.card {{ position: absolute; left: 84px; right: 84px; bottom: 96px; background: #fff; border-radius: 34px; padding: 40px 52px 44px; color: #111; }}
.who {{ display: flex; align-items: center; gap: 24px; margin-bottom: 24px; }}
.who img {{ width: 112px; height: 112px; border-radius: 50%; }}
.name {{ font-weight: 700; font-size: 40px; letter-spacing: -0.01em; display: flex; align-items: center; gap: 10px; }}
.tick {{ width: 36px; height: 36px; flex: none; }}
.handle {{ font-weight: 400; font-size: 29px; color: #5B6470; margin-top: 2px; }}
.body {{ font-size: 38px; line-height: 1.26; }}
.body p {{ text-wrap: pretty; }}
.body p + p {{ margin-top: 0.5em; }}
.body b {{ font-weight: 700; }}
.body u {{ text-decoration-thickness: 2px; text-underline-offset: 6px; }}
.body mark {{ background: #FFD43B; color: #111; padding: 0 8px; border-radius: 8px; }}
.count {{ position: absolute; right: 44px; bottom: 44px; color: #6B6560; font-size: 20px; font-weight: 600; }}
</style></head><body>
{''.join(slide_html(i, s) for i, s in enumerate(SLIDES))}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html', len(SLIDES), 'slides')
