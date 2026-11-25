"""Binghatti carousel. Slide 1: "RIP" hook with three tombstones, then the offer in the white tweet card.

Text from Omar. Writes slides.html; render.js screenshots each slide at 2x and the PNGs are downscaled to 1080x1350.
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


TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''


def tomb(x, rot, line1, line2, fs=84, cls=''):
    return f'''<div class="tomb" style="left:{x}px;transform:rotate({rot}deg)"><div class="rip">RIP</div>
      <div class="t1 {cls}" style="font-size:{fs}px">{line1}</div><div class="t2">{line2}</div></div>'''


def slide1():
    tombs = (tomb(28, -4, '1%', 'payment plans') + tomb(370, 1.5, 'AED 800K', 'for a studio', 66)
             + tomb(712, 4, '&ldquo;Dubai is<br>too<br>expensive&rdquo;', '', 54, 'quote'))
    return f'''
<section class="slide s1">
  <div class="moon"></div>
  <div class="glow"></div>
  {tombs}
  <div class="ground"></div>
  <div class="swipe">Swipe &rarr;</div>
</section>'''


def slide2():
    return f'''
<section class="slide s2">
  <div class="sun"></div>
  <div class="s2head">Because now,<br>from <span>Binghatti</span>&hellip;</div>
  <div class="card c2">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <div class="prices big">
      <div><span>Studio</span><em>from</em><b>AED 499K</b></div>
      <div><span>1 bed</span><em>from</em><b>AED 799K</b></div>
      <div><span>2 bed</span><em>from</em><b>AED 1.2M</b></div>
    </div>
    <div class="deal big"><div><b>10%</b><span>down payment</span></div><div class="plus">+</div><div><b>AED 2,500</b><span>a month</span></div></div>
    <p class="body big">From the developer that has collaborated with <b>Bugatti</b> and <b>Mercedes&#8209;Benz</b>.</p>
  </div>
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; }}
.s1 {{ background: radial-gradient(70% 45% at 75% 8%, #3A4766 0%, #151B2C 45%, #07090F 100%); }}
.s1::before {{ content: ''; position: absolute; inset: 0; background-image: radial-gradient(rgba(255,255,255,0.5) 1px, transparent 1.5px); background-size: 120px 90px; opacity: 0.25; }}
.s1 .glow {{ position: absolute; left: 50%; top: 600px; width: 1200px; height: 700px; transform: translate(-50%,-50%); background: radial-gradient(closest-side, rgba(200,215,255,0.28), transparent); }}
.moon {{ position: absolute; right: 110px; top: 70px; width: 120px; height: 120px; border-radius: 50%; background: #F3EBD3; box-shadow: 0 0 60px rgba(243,235,211,0.5); }}
.tomb {{ position: absolute; top: 210px; width: 340px; height: 920px; border-radius: 170px 170px 12px 12px; background: linear-gradient(180deg, #E4E8EF, #A9B1BF);
  box-shadow: inset 0 -20px 40px rgba(0,0,0,0.25), 0 20px 40px rgba(0,0,0,0.5); text-align: center; padding-top: 200px; color: #1F2430; }}
.rip {{ font-weight: 800; font-size: 112px; letter-spacing: 0.12em; color: #2A303C; }}
.t1 {{ margin-top: 70px; font-weight: 800; font-size: 72px; line-height: 1.12; white-space: nowrap; color: #10131A; text-decoration: line-through; text-decoration-color: #E0182D; text-decoration-thickness: 9px; }}
.t2 {{ margin-top: 18px; font-weight: 700; font-size: 42px; color: #1F2430; }}
.ground {{ position: absolute; left: 0; right: 0; top: 1080px; height: 280px; background: linear-gradient(180deg, #1B2A1E, #07090F); border-radius: 50% 50% 0 0 / 30px 30px 0 0; }}
.t1.quote {{ text-decoration: none; font-style: italic; color: #B3121F; }}
.swipe {{ position: absolute; left: 50%; bottom: 70px; transform: translateX(-50%); padding: 14px 34px; border-radius: 40px; background: #FFD43B; color: #111;
  font-weight: 800; font-size: 34px; letter-spacing: 0.04em; }}
.s2 {{ background: linear-gradient(180deg, #0B1530 0%, #3A2F5E 30%, #C2577A 55%, #F59E52 72%, #FFD27A 100%); }}
.sun {{ position: absolute; left: 50%; top: 420px; width: 520px; height: 520px; transform: translateX(-50%); border-radius: 50%;
  background: radial-gradient(circle, #FFF3C4 0%, #FFD27A 45%, rgba(255,210,122,0) 70%); }}
.s2head {{ position: absolute; left: 70px; right: 70px; top: 90px; color: #fff; font-weight: 800; font-size: 92px; line-height: 1.05; letter-spacing: -0.01em;
  text-shadow: 0 6px 30px rgba(0,0,0,0.35); }}
.s2head span {{ color: #FFD43B; }}
.c2 {{ padding: 36px 44px 42px; }}
.c2 .who img {{ width: 84px; height: 84px; }} .c2 .name {{ font-size: 34px; }} .c2 .handle {{ font-size: 25px; }}
.prices.big {{ flex-direction: column; gap: 0; margin-top: 8px; }}
.prices.big div {{ display: grid; grid-template-columns: 1fr auto 260px; align-items: baseline; gap: 14px; background: none; border-radius: 0; padding: 18px 0; border-bottom: 2px solid #E6E8EC; }}
.prices.big span {{ font-size: 40px; color: #111; font-weight: 500; }}
.prices.big em {{ font-style: normal; font-size: 24px; color: #8A9099; }}
.prices.big b {{ font-size: 50px; text-align: right; color: #111; }}
.deal.big {{ display: flex; align-items: center; gap: 14px; background: none; padding: 0; margin-top: 26px; }}
.deal.big > div {{ flex: 1; background: #FFD43B; border-radius: 20px; padding: 20px 22px; text-align: center; }}
.deal.big > div:last-child {{ background: #111; color: #fff; }} .deal.big > div:last-child b {{ color: #FFC940; }}
.deal.big b {{ display: block; font-size: 58px; font-weight: 800; line-height: 1; }}
.deal.big span {{ display: block; margin: 8px 0 0; font-size: 26px; font-weight: 600; color: inherit; }}
.deal.big .plus {{ flex: none; background: none; padding: 0; font-size: 50px; font-weight: 800; color: #111; }}
.body.big {{ margin-top: 24px; font-size: 32px; }}
.card {{ position: absolute; left: 70px; right: 70px; bottom: 50px; background: #fff; border-radius: 30px; padding: 28px 38px 32px; color: #111; }}
.who {{ display: flex; align-items: center; gap: 18px; margin-bottom: 14px; }}
.who img {{ width: 70px; height: 70px; border-radius: 50%; }}
.name {{ font-weight: 700; font-size: 30px; display: flex; align-items: center; gap: 10px; }}
.tick {{ width: 28px; height: 28px; flex: none; }}
.handle {{ font-size: 22px; color: #5B6470; }}
.lead {{ font-size: 30px; }} .lead b {{ font-weight: 800; }}
.prices {{ display: flex; gap: 10px; margin-top: 12px; }}
.prices div {{ flex: 1; background: #F1F2F5; border-radius: 14px; padding: 10px 16px; }}
.prices span {{ display: block; color: #5B6470; font-size: 20px; font-weight: 600; }}
.prices b {{ display: block; color: #111; font-size: 32px; font-weight: 800; margin-top: 2px; white-space: nowrap; }}
.body {{ margin-top: 12px; font-size: 26px; line-height: 1.3; color: #2A2F38; }} .body b {{ color: #111; font-weight: 700; }}
.deal {{ margin-top: 14px; background: #FFF1B8; border-radius: 14px; padding: 12px 18px; font-size: 28px; font-weight: 600; text-align: center; }}
.deal b {{ font-weight: 800; font-size: 32px; }} .deal span {{ margin: 0 8px; color: #5B4A00; }}
</style></head><body>
{slide1()}
{slide2()}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html')
