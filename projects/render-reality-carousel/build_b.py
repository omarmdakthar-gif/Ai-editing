"""Render vs reality carousel, version B: native Instagram look (full-bleed photos, story-style text highlights).
Same content as build.py (version A). Writes slides_b.html; render_b.js screenshots into out_b/.
"""
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')
NAME = 'Omar Akthar'
PHONE = '+971 56 837 6676'
TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''

WA = '<svg class="wa" viewBox="0 0 24 24"><path fill="#25D366" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/><path fill="#fff" d="M16.5 14.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def foot():
    return (f'<div class="foot"><img src="img/avatar.png" alt=""><div><div class="fn"><b>{NAME}</b>{TICK}<span>(Dubai Property Consultant)</span></div>'
            f'<div class="fp">{WA}{PHONE}</div></div></div>')


def story(lines, cls='', style=''):
    """Instagram-story style text: each line gets its own white highlight box."""
    return f'<div class="story {cls}" style="{style}">' + ''.join(f'<div><span>{l}</span></div>' for l in lines) + '</div>'


def lab(t, dark=False):
    return f'<div class="lab{" dk" if dark else ""}">{t}</div>'


def half(img, label, top, h, dark=False, pos='center'):
    return f'<div class="half" style="top:{top}px;height:{h}px;background-image:url(\'img/{img}\');background-position:{pos}">{lab(label, dark)}</div>'


def b1():
    return f"""
<section class="slide">
  {half('fish_r.jpg', 'Render', 0, 675)}
  {half('fish_b.jpg', 'Reality', 675, 675, True)}
  {story(['Render vs reality 👀'], 'mid big')}
  <div class="swp">swipe &rarr;</div>
</section>"""


def b2():
    cell = lambda img, l, d, x, y: f'<div class="cell" style="left:{x}px;top:{y}px;background-image:url(\'img/{img}\')">{lab(l, d)}</div>'
    cells = ''.join([cell('lib_r.jpg', 'Render', False, 0, 0), cell('lib_b.jpg', 'Reality', True, 540, 0),
                     cell('tri_r.jpg', 'Render', False, 0, 450), cell('tri_b.jpg', 'Reality', True, 540, 450),
                     cell('pyr_r.jpg', 'Render', False, 0, 900), cell('pyr_b.jpg', 'Reality', True, 540, 900)])
    return f"""
<section class="slide">
  {cells}
  {story(['It happens more', 'than you think.'], 'mid')}
</section>"""


def b3():
    return f"""
<section class="slide">
  <div class="blurbg" style="background-image:url('img/bug_render.jpg')"></div>
  <div class="hero" style="background-image:url('img/bug_render.jpg')">{lab('Render')}</div>
  {story(['Then Binghatti announced', 'Bugatti Residences 🤯'], 'top')}
  {story(['People said it could', 'never be built.'], 'low', 'top:1010px')}
  {foot()}
</section>"""


def b4():
    return f"""
<section class="slide">
  <div class="full" style="background-image:url('img/bug_street.jpg');background-position:center 40%"></div>
  <div class="mini" style="background-image:url('img/bug_render.jpg')">{lab('Render')}</div>
  {story(['Today 👇', "It's rising exactly", 'like the render.'], 'top')}
  {lab('Reality · Nov 2026', True).replace('class="lab dk"', 'class="lab dk big"')}
  {foot()}
</section>"""


def b5():
    return f"""
<section class="slide">
  <div class="blurbg" style="background-image:url('img/plaza-000.jpg')"></div>
  <div class="wide" style="background-image:url('img/plaza-000.jpg')"></div>
  <div class="wide2" style="background-image:url('img/kids.jpg')"></div>
  {story(['Now the same developer', 'is doing it again.'], 'top')}
  {story(['The Arts District', 'by Binghatti'], 'low inv', 'top:960px')}
  {foot()}
</section>"""


def b6():
    return f"""
<section class="slide">
  <div class="full" style="background-image:url('img/violin.jpg');background-position:center 40%"></div>
  <div class="dim dark"></div>
  {story(['The numbers 👇'], 'top')}
  <div class="list">
    <div><span>Studio from</span><b>AED 499K</b></div>
    <div><span>1 bed from</span><b>AED 799K</b></div>
    <div><span>2 bed from</span><b>AED 1.2M</b></div>
    <div class="hl"><span>Payment</span><b>20% &amp; AED 2,500/month</b></div>
    <div class="hl"><span>EOI this weekend</span><b>extra 7% off</b></div>
  </div>
  <p class="fine">Prices shown are after the 7% EOI discount</p>
  {foot()}
</section>"""


def b7():
    return f"""
<section class="slide">
  <div class="full" style="background-image:url('img/aerial.jpg')"></div>
  <div class="dim"></div>
  {story(['Want the price list', '& floor plans?'], 'top')}
  {story(['Comment ARTS DISTRICT'], 'mid2 inv big')}
  {story(['or DM me'], 'low', 'top:820px')}
  {foot()}
</section>"""


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; background: #000; }}
.half, .cell, .full, .hero, .mini, .wide, .wide2 {{ position: absolute; background-size: cover; background-position: center; }}
.wide {{ left: 40px; right: 40px; top: 260px; height: 390px; border-radius: 22px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
.wide2 {{ position: absolute; left: 40px; right: 40px; top: 670px; height: 270px; border-radius: 22px; background-size: cover; background-position: center 62%; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
.mini {{ position: absolute; background-size: cover; background-position: center; }}
.half {{ left: 0; right: 0; }}
.cell {{ width: 540px; height: 450px; outline: 2px solid #000; }}
.full {{ inset: 0; }}
.dim {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.35), rgba(0,0,0,0.05) 40%, rgba(0,0,0,0.55) 100%); }}
.dim.dark {{ background: linear-gradient(180deg, rgba(0,0,0,0.55), rgba(0,0,0,0.35) 50%, rgba(0,0,0,0.6)); }}
.lab {{ position: absolute; left: 24px; top: 24px; background: rgba(255,255,255,0.92); color: #000; font-weight: 700; font-size: 28px; padding: 6px 16px; border-radius: 10px; }}
.lab.dk {{ background: rgba(0,0,0,0.75); color: #fff; }}
.lab.big {{ left: 40px; top: auto; bottom: 170px; font-size: 32px; padding: 10px 20px; }}
.story {{ position: absolute; left: 0; right: 0; text-align: center; font-weight: 700; font-size: 58px; line-height: 1; }}
.story div {{ margin: 0 0 -2px; }}
.story span {{ display: inline-block; background: #fff; color: #000; padding: 12px 22px 14px; border-radius: 14px; }}
.story.inv span {{ background: #000; color: #fff; }}
.story.big {{ font-size: 72px; }}
.story.mid {{ top: 50%; transform: translateY(-50%); }}
.story.mid2 {{ top: 640px; }}
.story.top {{ top: 70px; }}
.swp {{ position: absolute; right: 34px; bottom: 34px; color: #fff; font-weight: 600; font-size: 30px; text-shadow: 0 2px 10px rgba(0,0,0,0.6); }}
.blurbg {{ position: absolute; inset: -40px; background-size: cover; background-position: center; filter: blur(30px) brightness(0.55); }}
.hero {{ left: 140px; right: 140px; top: 250px; height: 740px; border-radius: 24px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); }}
.mini {{ right: 40px; top: 400px; width: 260px; height: 326px; border-radius: 18px; border: 5px solid #fff; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
.mini .lab {{ font-size: 22px; left: 12px; top: 12px; }}
.list {{ position: absolute; left: 60px; right: 60px; top: 230px; display: grid; gap: 18px; }}
.list div {{ display: flex; justify-content: space-between; align-items: baseline; background: #fff; color: #000; border-radius: 16px; padding: 22px 28px; }}
.list span {{ font-size: 32px; font-weight: 500; }} .list b {{ font-size: 50px; font-weight: 800; }}
.list .hl {{ background: #FFD43B; }} .list .hl b {{ font-size: 40px; }}
.fine {{ position: absolute; left: 60px; right: 60px; top: 1060px; color: #ddd; font-size: 24px; text-align: center; }}
.foot {{ position: absolute; left: 0; right: 0; bottom: 0; display: flex; align-items: center; gap: 16px; padding: 22px 40px 26px; background: rgba(0,0,0,0.78); color: #fff; }}
.foot img {{ width: 68px; height: 68px; border-radius: 50%; }}
.fn {{ display: flex; align-items: center; gap: 8px; font-size: 28px; }} .fn .tick {{ width: 26px; height: 26px; }} .fn span {{ font-weight: 700; color: #FFD43B; }}
.fp {{ display: flex; align-items: center; gap: 8px; margin-top: 4px; font-size: 26px; font-weight: 600; }}
.wa {{ width: 28px; height: 28px; }}
</style></head><body>
{b1()}{b2()}{b3()}{b4()}{b5()}{b6()}{b7()}
</body></html>"""
(HERE / 'slides_b.html').write_text(page)
print('slides_b.html')
