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


def tomb(x, rot, line1, line2, fs=72):
    return f'''<div class="tomb" style="left:{x}px;transform:rotate({rot}deg)"><div class="rip">RIP</div>
      <div class="t1" style="font-size:{fs}px">{line1}</div><div class="t2">{line2}</div></div>'''


def slide1():
    tombs = tomb(28, -4, '1%', 'payment plans') + tomb(370, 1.5, 'AED 800K', 'for a studio', 58) + tomb(712, 4, '20%', 'down payment')
    return f'''
<section class="slide s1">
  <div class="moon"></div>
  <div class="glow"></div>
  {tombs}
  <div class="ground"></div>
  <div class="card">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <p class="lead">Because now you get these from <b>Binghatti</b>:</p>
    <div class="prices"><div><span>Studio</span><b>AED 499K</b></div><div><span>1 bed</span><b>AED 799K</b></div><div><span>2 bed</span><b>AED 1.2M</b></div></div>
    <p class="body">The developer that has collaborated with <b>Bugatti</b> and <b>Mercedes-Benz</b>.</p>
    <div class="deal"><b>10%</b> down payment <span>+</span> <b>AED 2,500</b> a month</div>
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
.s1 .glow {{ position: absolute; left: 50%; top: 380px; width: 1200px; height: 700px; transform: translate(-50%,-50%); background: radial-gradient(closest-side, rgba(200,215,255,0.28), transparent); }}
.moon {{ position: absolute; right: 70px; top: 34px; width: 90px; height: 90px; border-radius: 50%; background: #F3EBD3; box-shadow: 0 0 60px rgba(243,235,211,0.5); }}
.tomb {{ position: absolute; top: 110px; width: 340px; height: 660px; border-radius: 170px 170px 12px 12px; background: linear-gradient(180deg, #E4E8EF, #A9B1BF);
  box-shadow: inset 0 -20px 40px rgba(0,0,0,0.25), 0 20px 40px rgba(0,0,0,0.5); text-align: center; padding-top: 110px; color: #1F2430; }}
.rip {{ font-weight: 800; font-size: 96px; letter-spacing: 0.12em; color: #2A303C; }}
.t1 {{ margin-top: 54px; font-weight: 800; font-size: 72px; line-height: 1.05; white-space: nowrap; color: #10131A; text-decoration: line-through; text-decoration-color: #E0182D; text-decoration-thickness: 9px; }}
.t2 {{ margin-top: 14px; font-weight: 700; font-size: 36px; color: #1F2430; }}
.ground {{ position: absolute; left: 0; right: 0; top: 720px; height: 140px; background: linear-gradient(180deg, #1B2A1E, #07090F); border-radius: 50% 50% 0 0 / 30px 30px 0 0; }}
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
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html')
