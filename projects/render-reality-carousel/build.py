"""Render vs reality carousel: viral render-vs-reality fails, then Bugatti Residences by Binghatti (render vs today),
then The Arts District by Binghatti. Own editorial design: cream paper, black type, orange tape labels.

Photos: viral comparison images (src/fish, library, triangle, pyramid) sent by Omar; Bugatti Residences render and
street photo sent by Omar; Arts District renders from the Binghatti files.
Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')
NAME = 'Omar Akthar'
PHONE = '+971 56 837 6676'
TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''

WA = '<svg class="wa" viewBox="0 0 24 24"><path fill="#25D366" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/><path fill="#fff" d="M16.5 14.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def foot(dark=False):
    return (f'<div class="foot{" dk" if dark else ""}"><img src="img/avatar.png" alt=""><div><div class="fn"><b>{NAME}</b>{TICK}<strong>(Dubai Property Consultant)</strong></div>'
            f'<div class="fp">{WA}{PHONE}</div></div></div>')


def tape(t, cls=''):
    return f'<div class="tape {cls}">{t}</div>'


def frame(img, label, cls='', pos='center', lab_cls=''):
    return f'<div class="fr {cls}" style="background-image:url(\'img/{img}\');background-position:{pos}">{tape(label, lab_cls)}</div>'


def s1():
    return f"""
<section class="slide">
  <div class="mast"><span>Issue 01</span><span>Dubai off-plan</span></div>
  <h1 class="h1">Renders<br><em>can lie.</em></h1>
  {frame('fish_r.jpg', 'The render', 'f1')}
  {frame('fish_b.jpg', 'What got built', 'f2', 'center', 'bad')}
  <div class="swipe">More proof &rarr;</div>
</section>"""


def s2():
    pair = lambda r, b: f'<div class="pair">{frame(r, "Render", "p")}{frame(b, "Reality", "p", "center", "bad")}</div>'
    return f"""
<section class="slide">
  <div class="mast"><span>Exhibit A, B, C</span><span>Viral render-vs-reality posts</span></div>
  <h2 class="h2">It happens <em>more than<br>you think.</em></h2>
  <div class="pairs">{pair('lib_r.jpg', 'lib_b.jpg')}{pair('tri_r.jpg', 'tri_b.jpg')}{pair('pyr_r.jpg', 'pyr_b.jpg')}</div>
  <div class="moral">In off-plan, you're not buying the render.<br><b>You're buying the developer.</b></div>
</section>"""


def s3():
    return f"""
<section class="slide">
  <div class="mast"><span>Exhibit D</span><span>Business Bay, Dubai</span></div>
  <h2 class="h2">Then Binghatti<br><em>showed this.</em></h2>
  <div class="s3row">
    {frame('bug_render.jpg', 'The render', 'f3')}
    <div class="s3txt">
      <div class="kn">Bugatti Residences</div>
      <p>A tower that flows like water, with a pool in the sky.</p>
      <p class="doubt">&ldquo;That can never be built.&rdquo;</p>
      <p class="small">What a lot of people said when it launched.</p>
    </div>
  </div>
  {foot()}
</section>"""


def s4():
    return f"""
<section class="slide s4">
  <div class="s4photo" style="background-image:url('img/bug_street.jpg')"></div>
  <div class="s4band">
    <div class="mast lt"><span>Exhibit D, today</span><span>Under construction, Nov 2026</span></div>
    <h2 class="h2 lt">Today, it's rising<br><em>exactly like the render.</em></h2>
  </div>
  <div class="inset">{frame('bug_render.jpg', 'Render', 'fi')}</div>
  {tape('Reality', 'real big')}
  {foot(True)}
</section>"""


def s5():
    return f"""
<section class="slide">
  <div class="mast"><span>Next from Binghatti</span><span>Dubai Silicon Oasis &amp; Academic City</span></div>
  <h2 class="h2">Now they're<br><em>doing it again.</em></h2>
  <div class="grid5">
    {frame('plaza-000.jpg', 'The Arts District', 'g1')}
    {frame('violin.jpg', 'Render', 'g2', '45% 40%')}
    {frame('kids.jpg', 'Render', 'g3', 'center 55%')}
  </div>
  <p class="cap">Same developer. Same ambition. A whole <b>district built around art</b>, with sculptures, a plaza and resort-style amenities.</p>
  {foot()}
</section>"""


def s6():
    row = lambda k, v, e: f'<div class="pr"><span>{k}</span><em>{e}</em><b>{v}</b></div>'
    return f"""
<section class="slide">
  <div class="mast"><span>The details</span><span>The Arts District by Binghatti</span></div>
  <h2 class="h2">Get in <em>before<br>it rises.</em></h2>
  <div class="ptab">
    {row('Studio', 'AED 499K', 'from')}
    {row('1 bedroom', 'AED 799K', 'from')}
    {row('2 bedroom', 'AED 1.2M', 'from')}
  </div>
  <div class="chips">
    <div class="ch blk"><b>20%</b><span>down payment</span></div>
    <div class="ch blk"><b>AED 2,500</b><span>a month</span></div>
  </div>
  <div class="eoi"><b>EOI opens this weekend</b> &middot; book at EOI and get an <b>extra 7% off</b></div>
  <p class="fine">Prices shown are after the 7% EOI discount. Next to Dubai Silicon Oasis &amp; Academic City.</p>
  {foot()}
</section>"""


def s7():
    return f"""
<section class="slide s7">
  <div class="s7img" style="background-image:url('img/aerial.jpg')"></div>
  <div class="s7card">
    <div class="mast"><span>Your move</span><span>The Arts District by Binghatti</span></div>
    <h2 class="h2">Trust the<br><em>track record.</em></h2>
    <div class="cta">Comment <b>ARTS DISTRICT</b></div>
    <p class="ctad">or DM me for the price list, floor plans and payment plan.</p>
  </div>
  {foot()}
</section>"""


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; background: #F3EFE6; color: #111; padding: 50px 56px 0; }}
.slide::before {{ content: ''; position: absolute; inset: 0; background-image: radial-gradient(rgba(0,0,0,0.035) 1px, transparent 1.2px); background-size: 6px 6px; pointer-events: none; }}
.mast {{ position: relative; display: flex; justify-content: space-between; font-size: 22px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase;
  border-top: 4px solid #111; border-bottom: 1.5px solid #111; padding: 12px 0; }}
.mast.lt {{ color: #fff; border-color: #fff; }}
.h1 {{ position: relative; margin-top: 26px; font-size: 128px; font-weight: 800; line-height: 0.92; letter-spacing: -0.03em; }}
.h2 {{ position: relative; margin-top: 26px; font-size: 84px; font-weight: 800; line-height: 0.98; letter-spacing: -0.02em; }}
.h1 em, .h2 em {{ font-style: normal; color: #FF5A1F; }}
.h2.lt {{ color: #fff; }}
.fr {{ position: relative; background-size: cover; border: 6px solid #fff; box-shadow: 0 14px 30px rgba(0,0,0,0.18); }}
.tape {{ position: absolute; left: -10px; top: 18px; background: #FF5A1F; color: #fff; font-weight: 800; font-size: 26px; letter-spacing: 0.12em; text-transform: uppercase;
  padding: 8px 18px; transform: rotate(-3deg); box-shadow: 0 4px 10px rgba(0,0,0,0.25); white-space: nowrap; }}
.tape.bad {{ background: #111; }}
.f1 {{ position: absolute; left: 56px; right: 56px; top: 420px; height: 420px; transform: rotate(-1.2deg); }}
.f2 {{ position: absolute; left: 56px; right: 56px; top: 870px; height: 420px; transform: rotate(1deg); }}
.swipe {{ position: absolute; right: 56px; top: 300px; background: #111; color: #fff; font-weight: 700; font-size: 28px; padding: 14px 26px; border-radius: 40px; }}
.pairs {{ position: relative; margin-top: 30px; display: grid; gap: 20px; }}
.pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.fr.p {{ height: 262px; border-width: 5px; }} .fr.p .tape {{ font-size: 20px; padding: 6px 12px; top: 12px; }}
.moral {{ position: relative; margin-top: 30px; font-size: 40px; line-height: 1.25; border-left: 10px solid #FF5A1F; padding-left: 24px; }} .moral b {{ font-weight: 800; }}
.s3row {{ position: relative; margin-top: 40px; display: grid; grid-template-columns: 540px 1fr; gap: 44px; align-items: center; }}
.f3 {{ height: 800px; transform: rotate(-1.5deg); background-position: center; }}
.kn {{ font-size: 54px; font-weight: 800; line-height: 1.05; }}
.s3txt p {{ margin-top: 20px; font-size: 36px; line-height: 1.3; color: #333; }}
.s3txt .doubt {{ margin-top: 44px; font-size: 62px; font-weight: 800; line-height: 1.1; color: #111; font-style: italic; }}
.s3txt .small {{ font-size: 27px; color: #6B6B6B; }}
.s4 {{ padding: 0; }}
.s4photo {{ position: absolute; inset: 0; background-size: cover; background-position: center 40%; }}
.s4band {{ position: absolute; left: 0; right: 0; top: 0; padding: 50px 56px 120px; background: linear-gradient(180deg, rgba(10,10,12,0.85) 0%, rgba(10,10,12,0.6) 60%, rgba(10,10,12,0) 100%); }}
.inset {{ position: absolute; right: 56px; top: 560px; transform: rotate(3deg); }}
.fi {{ width: 260px; height: 330px; border-width: 6px; }} .fi .tape {{ font-size: 20px; padding: 6px 12px; }}
.tape.real.big {{ left: 56px; top: auto; bottom: 200px; font-size: 40px; padding: 10px 26px; background: #111; border: 3px solid #fff; }}
.grid5 {{ position: relative; margin-top: 34px; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 440px 270px; gap: 18px; }}
.g1 {{ grid-column: 1 / 3; }}
.cap {{ position: relative; margin-top: 22px; font-size: 30px; line-height: 1.3; color: #333; }} .cap b {{ color: #111; }}
.ptab {{ position: relative; margin-top: 40px; border-top: 3px solid #111; }}
.pr {{ display: grid; grid-template-columns: 1fr auto 330px; gap: 20px; align-items: baseline; padding: 32px 0; border-bottom: 1.5px solid #111; }}
.pr span {{ font-size: 44px; font-weight: 500; }} .pr em {{ font-style: normal; font-size: 26px; color: #6B6B6B; }} .pr b {{ text-align: right; font-size: 58px; font-weight: 800; }}
.chips {{ position: relative; margin-top: 40px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
.ch {{ background: #111; color: #fff; padding: 22px 26px; }} .ch b {{ display: block; font-size: 60px; font-weight: 800; color: #FF8A5B; line-height: 1; }} .ch span {{ display: block; margin-top: 8px; font-size: 28px; font-weight: 600; }}
.eoi {{ position: relative; margin-top: 22px; background: #FF5A1F; color: #fff; padding: 20px 26px; font-size: 32px; line-height: 1.25; }} .eoi b {{ font-weight: 800; }}
.fine {{ position: relative; margin-top: 14px; font-size: 22px; color: #6B6B6B; }}
.s7 {{ padding: 0; }}
.s7img {{ position: absolute; left: 0; right: 0; top: 0; height: 700px; background-size: cover; background-position: center; }}
.s7card {{ position: absolute; left: 0; right: 0; top: 640px; bottom: 0; background: #F3EFE6; padding: 40px 56px 0; }}
.cta {{ margin-top: 40px; display: inline-block; background: #111; color: #fff; font-size: 62px; font-weight: 700; padding: 18px 34px; }} .cta b {{ color: #FF8A5B; font-weight: 800; }}
.ctad {{ margin-top: 22px; font-size: 34px; color: #333; }}
.foot {{ position: absolute; left: 56px; right: 56px; bottom: 40px; display: flex; align-items: center; gap: 16px; border-top: 2px solid #111; padding-top: 18px; }}
.foot img {{ width: 72px; height: 72px; border-radius: 50%; border: 3px solid #FF5A1F; }}
.fn {{ display: flex; align-items: center; gap: 8px; font-size: 28px; }} .fn .tick {{ width: 26px; height: 26px; }} .fn strong {{ font-weight: 800; color: #FF5A1F; margin-left: 4px; }}
.fp {{ display: flex; align-items: center; gap: 8px; margin-top: 4px; font-size: 26px; font-weight: 700; }}
.wa {{ width: 28px; height: 28px; }}
.foot.dk {{ color: #fff; border-color: rgba(255,255,255,0.6); }} .foot.dk .fn strong {{ color: #FFB08A; }}
.foot.dk::before {{ content: ''; position: absolute; left: -56px; right: -56px; top: -30px; bottom: -40px; background: linear-gradient(rgba(10,10,12,0), rgba(10,10,12,0.85) 40%); z-index: -1; }}
</style></head><body>
{s1()}{s2()}{s3()}{s4()}{s5()}{s6()}{s7()}
</body></html>"""
(HERE / 'slides.html').write_text(page)
print('slides.html')
