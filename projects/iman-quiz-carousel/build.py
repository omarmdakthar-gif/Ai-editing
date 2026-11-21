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
               "Their newest one is in **Dubai Science Park**:"],
     'times': [('15', 'Palm Jumeirah'), ('20', 'Downtown Dubai'), ('15', 'Mall of the Emirates')]},
    {'kind': 'why',
     'title': "Why ==**Dubai Science Park?**==",
     'lead': "It already hosts major companies like **Pfizer**.",
     'stats': [('90+', 'Labs'), ('500+', 'Companies'), ('6,500+', 'Professionals')],
     'statnote': "in pharma, life sciences and energy",
     'rows': [('hosp', "**American Hospital** opened here in 2026 with 100 beds, and __2 more hospitals__ are on the way."),
              ('school', "Top schools: **Repton, Brighton College, GEMS World Academy, Dubai Schools** and **Safa Community School**."),
              ('park', "A green escape park with a **1 km jogging track**."),
              ('road', "Easy access to **Umm Suqeim Road, Al Khail Road** and **Mohammed Bin Zayed Road**.")],
     'close': "For the **high-earning medical professionals** working here, it's the perfect community to live in."},
    {'kind': 'price',
     'title': "Prices start at ==**AED 684K.**==",
     'rows': [('Studio', 'AED 684K'), ('1 bed', 'AED 1.06M'), ('2 bed', 'AED 1.59M'), ('3 bed with pool', 'AED 2.65M')],
     'cta': "Interested? Comment **INFO**\nand I'll send you the details."},
]

TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''


def photo(img, num, cls, stamp_html):
    return f'''<div class="ph {cls}" style="background-image:url('img/{img}.jpg')"><div class="num">{num}</div>{stamp_html}</div>'''


def stamp(is_render):
    return '<div class="stamp render">RENDER</div>' if is_render else '<div class="stamp real">REAL ✓</div>'


ICONS = {
    'hosp': '<svg viewBox="0 0 24 24"><path fill="#111" d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/></svg>',
    'school': '<svg viewBox="0 0 24 24"><path fill="#111" d="M12 3 1 9l11 6 9-4.9V17h2V9zM5 13.2v3.6C5 18.6 8.1 20 12 20s7-1.4 7-3.2v-3.6l-7 3.8z"/></svg>',
    'road': '<svg viewBox="0 0 24 24"><path fill="#111" d="M9 2h2l-1 20H6zM13 2h2l3 20h-4zM11.2 4h1.6v3h-1.6zm0 5h1.6v3h-1.6zm0 5h1.6v3h-1.6z"/></svg>',
    'park': '<svg viewBox="0 0 24 24"><path fill="#111" d="M12 2 5 12h4l-4 6h6v4h2v-4h6l-4-6h4z"/></svg>',
}


def why_slide(s):
    stats = ''.join(f'<div class="st"><b>{n}</b><span>{l}</span></div>' for n, l in s['stats'])
    rows = ''.join(f'<div class="wr"><i>{ICONS[k]}</i><p>{md(t)}</p></div>' for k, t in s['rows'])
    return f'''
<section class="slide why">
  <header class="whyh">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE} · Spot the render</div></div><div class="pill">The location</div></div>
    <h1>{md(s['title'])}</h1>
    <p class="lead">{md(s['lead'])}</p>
  </header>
  <div class="stats">{stats}</div>
  <p class="statnote">{md(s['statnote'])}</p>
  <div class="rows">{rows}</div>
  <div class="close">{md(s['close'])}</div>
</section>'''


def price_slide(s):
    rows = ''.join(f'<div class="pr{" hi" if k == 0 else ""}"><span>{html.escape(a)}</span><em>from</em><b>{b}</b></div>' for k, (a, b) in enumerate(s['rows']))
    return f'''
<section class="slide why">
  <header class="whyh">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE} · Spot the render</div></div><div class="pill">The price</div></div>
    <h1>{md(s['title'])}</h1>
  </header>
  <div class="ptable">{rows}</div>
  <div class="plan">
    <div class="ptitle"><b>50/50</b> payment plan</div>
    <div class="steps">{''.join(f'<div class="sp {c}"><b>{pc}</b><span>{l}</span></div>' for pc, l, c in [('20%', 'On booking', 'y'), ('10%', 'In 90 days', ''), ('10%', 'At 40% construction', ''), ('10%', 'At 60% construction', ''), ('50%', 'On completion', 'k')])}</div>
  </div>
  <div class="close cta">{md(s['cta'])}</div>
</section>'''


def map_slide(s):
    body = ''.join(f'<p>{md(p)}</p>' for p in s['paras'])
    return f'''
<section class="slide">
  <header class="tall">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE} · Spot the render</div></div><div class="pill">The reveal</div></div>
    <h1>{md(s['title'])}</h1>
    <div class="paras">{body}</div>
    <div class="times">{''.join(f'<div class="tm"><b>{m}<small> min</small></b><span>{html.escape(l)}</span></div>' for m, l in s.get('times', []))}</div>
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
    if s.get('kind') == 'why':
        return why_slide(s)
    if s.get('kind') == 'price':
        return price_slide(s)
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
header.tall {{ height: 552px; }} header.tall h1 {{ font-size: 52px; margin-top: 22px; }}
.paras {{ margin-top: 16px; font-size: 34px; line-height: 1.3; color: #2A2F38; }}
.paras p + p {{ margin-top: 0.5em; }} .paras b {{ font-weight: 700; color: #111; }} .paras u {{ text-decoration-thickness: 2px; text-underline-offset: 5px; }}
.times {{ display: flex; gap: 14px; margin-top: 18px; }}
.tm {{ flex: 1; background: #FFD43B; color: #111; border-radius: 16px; padding: 12px 18px 14px; }}
.tm b {{ display: block; font-size: 40px; font-weight: 800; color: #111; line-height: 1; }} .tm b small {{ font-size: 24px; font-weight: 700; }}
.tm span {{ display: block; margin-top: 6px; font-size: 22px; font-weight: 600; color: #111; white-space: nowrap; }}
.whyh {{ height: auto; padding-bottom: 0; }} .whyh h1 {{ font-size: 60px; margin-top: 26px; }}
.lead {{ margin-top: 18px; font-size: 40px; color: #2A2F38; }} .lead b {{ color: #111; }}
.stats {{ display: flex; gap: 16px; padding: 40px 44px 0; }}
.st {{ flex: 1; background: #111; border-radius: 22px; padding: 28px 24px 24px; }}
.st b {{ display: block; font-size: 74px; font-weight: 800; color: #FFC940; line-height: 1; }}
.st span {{ display: block; margin-top: 10px; font-size: 30px; font-weight: 600; color: #fff; }}
.statnote {{ padding: 14px 44px 0; font-size: 29px; color: #5B6470; }}
.rows {{ padding: 44px 44px 0; display: grid; gap: 30px; }}
.wr {{ display: flex; gap: 22px; align-items: flex-start; }}
.wr i {{ flex: none; width: 76px; height: 76px; border-radius: 50%; background: #FFD43B; display: grid; place-items: center; }}
.wr i svg {{ width: 40px; height: 40px; }}
.wr p {{ font-size: 36px; line-height: 1.3; color: #2A2F38; padding-top: 6px; }} .wr b {{ color: #111; font-weight: 700; }}
.wr u {{ text-decoration-thickness: 2px; text-underline-offset: 5px; }}
.close {{ position: absolute; left: 44px; right: 44px; bottom: 52px; background: #FFD43B; border-radius: 22px; padding: 28px 34px; font-size: 38px; line-height: 1.28; color: #111; }}
.close b {{ font-weight: 800; }}
.ptable {{ padding: 34px 44px 0; }}
.pr {{ display: grid; grid-template-columns: 1fr auto 280px; gap: 18px; align-items: baseline; padding: 30px 0; border-bottom: 2px solid #E6E8EC; font-size: 42px; }}
.pr em {{ font-style: normal; font-size: 26px; color: #8A9099; }}
.pr b {{ text-align: right; font-size: 48px; font-weight: 800; white-space: nowrap; }}
.pr.hi {{ background: #FFF6D6; margin: 0 -18px; padding: 30px 18px; border-radius: 16px; border-bottom: none; }}
.plan {{ margin: 56px 44px 0; }}
.ptitle {{ font-size: 40px; margin-bottom: 18px; }} .ptitle b {{ font-weight: 800; }}
.pbar {{ display: flex; gap: 10px; }}
.pbar div {{ flex: 1; background: #FFD43B; border-radius: 18px; padding: 24px 26px; }}
.pbar div.dark {{ background: #111; color: #fff; }}
.pbar b {{ display: block; font-size: 52px; font-weight: 800; line-height: 1; }} .pbar div.dark b {{ color: #FFC940; }}
.pbar span {{ display: block; margin-top: 6px; font-size: 26px; font-weight: 600; }}
.down {{ margin-top: 34px; font-size: 62px; font-weight: 600; text-align: center; }}
.down mark {{ background: #FFD43B; color: #111; padding: 0 18px; border-radius: 14px; }} .down b {{ font-weight: 800; }}
.steps {{ display: flex; gap: 10px; }}
.sp {{ flex: 1; background: #EEF0F3; border-radius: 20px; padding: 40px 12px 36px; text-align: center; }}
.sp b {{ display: block; font-size: 60px; font-weight: 800; line-height: 1; }}
.sp span {{ display: block; margin-top: 14px; font-size: 25px; font-weight: 600; line-height: 1.2; color: #3A414C; }}
.sp.y {{ background: #FFD43B; }} .sp.y span {{ color: #111; }}
.sp.k {{ background: #111; }} .sp.k b {{ color: #FFC940; }} .sp.k span {{ color: #fff; }}
.close.cta {{ background: #111; color: #fff; font-size: 40px; text-align: center; }} .close.cta b {{ color: #111; background: #FFD43B; padding: 0 12px; border-radius: 10px; }}
.map {{ position: relative; width: 1080px; height: 790px; background-size: cover; background-position: center top; }}
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
