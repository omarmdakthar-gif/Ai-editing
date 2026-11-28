"""'I wish...' carousel: everyone in Dubai wants the next thing up, and the whole world wants Dubai.
Own flat-vector cartoons drawn in SVG (no stock or AI images). Writes slides.html; render.js screenshots each slide.
"""
import math
import random
from pathlib import Path

HERE = Path(__file__).parent
FONTS = Path('/tmp/claude-0/-home-user-Ai-editing/8ddff90f-afa3-5ebe-a03c-5f12cab7e02e/scratchpad/fonts/node_modules/@fontsource/outfit/files')
NAME = 'Omar Akthar'
PHONE = '+971 56 837 6676'
TICK = '''<svg class="tick" viewBox="0 0 24 24" aria-label="Verified"><path fill="#1D9BF0" d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .494.083.964.237 1.4-1.272.65-2.147 2.018-2.147 3.6 0 1.495.782 2.798 1.942 3.486-.02.17-.032.34-.032.514 0 2.21 1.708 4 3.818 4 .47 0 .92-.086 1.335-.25.62 1.334 1.926 2.25 3.437 2.25 1.512 0 2.818-.916 3.437-2.25.415.163.865.248 1.336.248 2.11 0 3.818-1.79 3.818-4 0-.174-.012-.344-.033-.513 1.158-.687 1.943-1.99 1.943-3.484z"/><path fill="#fff" d="M10.54 16.2l-3.6-3.6 1.4-1.4 2.2 2.2 5.2-5.2 1.4 1.4z"/></svg>'''

WA = '<svg class="wa" viewBox="0 0 24 24"><path fill="#25D366" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/><path fill="#fff" d="M16.5 14.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
INK = '#1B1B2F'
O = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'


# ---------- drawing helpers (SVG, 1080 x 1350) ----------
def sky(c1, c2):
    return f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="1080" height="1350" fill="url(#sk)"/>'


def sun(x, y, r=70):
    return f'<circle cx="{x}" cy="{y}" r="{r + 30}" fill="#FFE9A8" opacity="0.5"/><circle cx="{x}" cy="{y}" r="{r}" fill="#FFD447" {O}/>'


def cloud(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 40 Q0 10 30 12 Q40 -14 75 -4 Q100 -24 125 2 Q160 0 160 40 Z" fill="#fff" {O}/></g>')


def sea(y, c='#3BB4E5'):
    waves = ''.join(f'<path d="M{x} {y + 40 + k * 60} q15 -10 30 0" stroke="#fff" stroke-width="4" fill="none" opacity="0.6" stroke-linecap="round"/>'
                    for k in range(6) for x in range(30 + (k % 2) * 60, 1080, 170))
    return f'<rect x="0" y="{y}" width="1080" height="{1350 - y}" fill="{c}"/>{waves}'


def palm_tree(x, y, s=1):
    fr = ''.join(f'<path d="M0 -150 q{dx * 0.5} {dy - 30} {dx} {dy}" stroke="#2E9E5B" stroke-width="18" fill="none" stroke-linecap="round"/>'
                 for dx, dy in [(-90, 20), (-70, -40), (0, -70), (70, -40), (90, 20), (-40, 40), (40, 40)])
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-8 0 Q-14 -80 0 -150 L10 -150 Q0 -80 8 0 Z" fill="#B07A45" {O}/>{fr}'
            f'<circle cx="0" cy="-150" r="10" fill="#7A4F2A"/></g>')


def villa(x, y, w, h, s=1, roof='#E07A4F', wall='#F6E7CF'):
    win = ''.join(f'<rect x="{x + 30 + i * (w - 60) / 3}" y="{y + 40}" width="{(w - 60) / 3 - 24}" height="{h * 0.3}" rx="6" fill="#7FD3F7" {O}/>' for i in range(3))
    win2 = ''.join(f'<rect x="{x + 30 + i * (w - 60) / 3}" y="{y + h * 0.55}" width="{(w - 60) / 3 - 24}" height="{h * 0.35}" rx="6" fill="#7FD3F7" {O}/>' for i in range(3))
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}" {O}/>'
            f'<path d="M{x - 30} {y} L{x + w / 2} {y - h * 0.35} L{x + w + 30} {y} Z" fill="{roof}" {O}/>{win}{win2}</g>')


def pool(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#5ED3F3" {O}/><path d="M{x + 30} {y + h / 2} q30 -12 60 0 t60 0 t60 0" stroke="#fff" stroke-width="5" fill="none" opacity="0.8"/>'


def tower(x, y, w, h, c='#C9D6E8', win='#8FC8EE', cols=4):
    h += 400
    rows = int((1750 - y) / 50)
    ws = ''.join(f'<rect x="{x + 14 + cx * (w - 28) / cols}" y="{y + 24 + r * 46}" width="{(w - 28) / cols - 12}" height="26" rx="4" fill="{win}"/>'
                 for r in range(rows) for cx in range(cols) if y + 24 + r * 46 < y + h - 30)
    return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}" {O}/>{ws}</g>'


def person(x, y, s=1, shirt='#FF6B6B', skin='#F2C9A0', look=1, extra=''):
    """Little cartoon resident, feet at (x, y). look = 1 faces right, -1 left."""
    e = 10 * look
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-20" y="-70" width="16" height="70" rx="8" fill="{INK}"/><rect x="4" y="-70" width="16" height="70" rx="8" fill="{INK}"/>'
            f'<rect x="-38" y="-170" width="76" height="110" rx="34" fill="{shirt}" {O}/>'
            f'<path d="M-36 -140 Q-62 -100 -50 -70" stroke="{shirt}" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<path d="M36 -140 Q62 -100 50 -70" stroke="{shirt}" stroke-width="20" fill="none" stroke-linecap="round"/>'
            f'<circle cx="0" cy="-222" r="56" fill="{skin}" {O}/>'
            f'<circle cx="{-16 + e}" cy="-228" r="7" fill="{INK}"/><circle cx="{16 + e}" cy="-228" r="7" fill="{INK}"/>'
            f'<path d="M{-14 + e} -202 Q{e} -194 {14 + e} -202" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="M{-30 + e} -246 q8 -6 16 0 M{14 + e} -246 q8 -6 16 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'{extra}</g>')


def bubble(text_lines, x, y, w, tail, fs=58):
    """Comic speech bubble centred at (x, y), tail pointing to tail=(tx, ty)."""
    h = 70 + fs * 1.15 * len(text_lines)
    tx, ty = tail
    lines = ''.join(f'<text x="{x}" y="{y - h / 2 + 52 + fs * 0.9 + i * fs * 1.15}" class="bt" font-size="{fs}">{t}</text>' for i, t in enumerate(text_lines))
    bx = max(x - w / 2 + 60, min(x + w / 2 - 60, tx))
    return (f'<path d="M{bx - 34} {y + h / 2 - 6} L{tx} {ty} L{bx + 34} {y + h / 2 - 6} Z" fill="#fff" {O}/>'
            f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#fff" {O}/>'
            f'<rect x="{bx - 30}" y="{y + h / 2 - 12}" width="60" height="10" fill="#fff"/>{lines}')


def palm_island(cx, cy, s=1, c='#F2D9A6'):
    """Top view of the Palm from the shore: trunk running away from the viewer, fronds fanning out, crescent at the far end."""
    fr = ''.join(f'<path d="M0 {-y} L{side * L} {-y - L * 0.35}" stroke="{c}" stroke-width="13" stroke-linecap="round"/>'
                 for y, L in [(40, 120), (75, 150), (110, 165), (145, 160), (180, 140), (212, 110)] for side in (-1, 1))
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M-250 -150 Q-250 -330 0 -340 Q250 -330 250 -150" stroke="{c}" stroke-width="18" fill="none" stroke-linecap="round"/>'
            f'<path d="M0 60 L0 -235" stroke="{c}" stroke-width="22" stroke-linecap="round"/>{fr}</g>')


# ---------- slides ----------
def idcard(lives, wants):
    return f'<div class="idc"><div><span>Lives in</span><b>{lives}</b></div><div class="arr">&rarr;</div><div class="w"><span>Wishes for</span><b>{wants}</b></div></div>'


def foot():
    return (f'<div class="foot"><img src="img/avatar.png" alt=""><div><div class="fn"><b>{NAME}</b>{TICK}<span>(Dubai Property Consultant)</span></div>'
            f'<div class="fp">{WA}{PHONE}</div></div></div>')


def slide(svg, extra_html='', shift=0):
    if shift:
        svg = svg.replace('1350', '1750')
    return f'<section class="slide"><svg class="scene" viewBox="0 {shift} 1080 1350">{svg}</svg>{extra_html}</section>'


def w1():
    svg = (sky('#7FD0F5', '#CDEFFF') + sun(900, 170) + cloud(80, 160, 1.2) + cloud(560, 250, 0.9)
           + sea(760, '#3BB4E5')
           + '<path d="M0 860 Q540 820 1080 860 L1080 1350 L0 1350 Z" fill="#F7E2B5" ' + O + '/>'
           + villa(60, 620, 420, 300) + villa(560, 420, 470, 500, roof='#D9643A')
           + pool(90, 1000, 360, 110) + palm_tree(520, 1010, 1.1) + palm_tree(1020, 960, 0.9)
           + person(380, 1180, 1.2, '#FF6B6B', look=1,
                    extra='<rect x="-30" y="-240" width="26" height="20" rx="8" fill="' + INK + '"/><rect x="10" y="-240" width="26" height="20" rx="8" fill="' + INK + '"/><path d="M-4 -232 L10 -232" stroke="' + INK + '" stroke-width="4"/>')
           + bubble(['I wish I had a', 'bigger villa'], 330, 400, 540, (380, 920)))
    return slide(svg, idcard('A Palm villa', 'A bigger villa') + '<div class="swp">swipe &rarr;</div>', 70)


def w2():
    bal = ''.join(f'<rect x="0" y="{y}" width="430" height="20" fill="#E8DCC8" {O}/><rect x="300" y="{y - 90}" width="130" height="90" fill="none" stroke="{INK}" stroke-width="4"/>' for y in (460, 680, 900, 1120))
    svg = (sky('#8AD6F7', '#D6F2FF') + sun(940, 150, 60) + cloud(560, 120, 1) + sea(700, '#3BB4E5')
           + '<path d="M540 860 Q800 820 1080 860 L1080 1750 L540 1750 Z" fill="#F7E2B5" ' + O + '/>'
           + villa(640, 760, 360, 230, 0.8) + pool(660, 1020, 300, 70) + palm_tree(1040, 1000, 0.8)
           + '<rect x="0" y="220" width="420" height="1530" fill="#F3EBDD" ' + O + '/>'
           + ''.join(f'<rect x="40" y="{y - 160}" width="230" height="130" rx="6" fill="#9FD7F2" {O}/>' for y in (460, 680, 900, 1120))
           + bal + person(370, 900, 1.05, '#4D96FF', look=1)
           + bubble(['I wish I had', 'a villa'], 690, 430, 480, (420, 620)))
    return slide(svg, idcard('A Palm apartment', 'A villa') + foot(), 120)


def w3():
    svg = (sky('#6FC6F2', '#C7ECFF') + cloud(60, 120, 1) + cloud(700, 90, 0.8)
           + sea(380, '#2FA8DD') + palm_island(560, 800, 1.05)
           + tower(40, 760, 170, 590, '#C2D3EA') + tower(230, 640, 150, 710, '#D6E2F2') + tower(400, 820, 140, 530, '#BCCDE6')
           + '<path d="M0 1180 Q300 1120 560 1200 L560 1350 L0 1350 Z" fill="#2FA8DD" ' + O + '/>'
           + '<rect x="600" y="980" width="480" height="40" fill="#E9E3D6" ' + O + '/>'
           + '<rect x="600" y="1020" width="480" height="730" fill="#DDE6F1" ' + O + '/>'
           + '<path d="M600 880 L1080 880" stroke="' + INK + '" stroke-width="5"/><path d="M600 880 L600 980 M760 880 L760 980 M920 880 L920 980" stroke="' + INK + '" stroke-width="4"/>'
           + person(820, 985, 1.15, '#FFB703', look=-1)
           + bubble(['I wish I lived', 'on the Palm'], 720, 300, 500, (790, 690)))
    return slide(svg, idcard('Dubai Marina', 'The Palm') + foot(), 120)


def w4():
    svg = (sky('#9ADCF8', '#E2F6FF') + sun(160, 170, 60) + cloud(700, 140, 1.1)
           + tower(560, 300, 150, 900, '#C2D3EA') + tower(720, 220, 170, 980, '#D3DFF0') + tower(900, 360, 150, 840, '#BCCDE6')
           + tower(420, 480, 120, 720, '#CFDBEE', cols=3)
           + '<rect x="0" y="1090" width="1080" height="660" fill="#E9D8B8" ' + O + '/>'
           + '<rect x="40" y="760" width="440" height="860" fill="#F6C89A" ' + O + '/>'
           + ''.join(f'<rect x="{70 + i * 140}" y="{800 + j * 140}" width="100" height="90" rx="6" fill="#9FD7F2" {O}/>' for i in range(3) for j in range(2))
           + palm_tree(530, 1150, 0.7)
           + person(260, 1150, 1.1, '#2EC4B6', look=1)
           + bubble(['I wish I lived', 'in Dubai Marina'], 470, 500, 580, (300, 880)))
    return slide(svg, idcard('A JVC studio', 'Dubai Marina') + foot(), 130)


def w5():
    rnd = random.Random(4)
    stars = ''.join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(0, 1350):.0f}" r="{rnd.choice([1.5, 2, 3])}" fill="#fff" opacity="{rnd.uniform(0.4, 1):.2f}"/>' for _ in range(120))
    land = ('<path d="M380 560 q60 -40 120 -10 q40 40 10 90 q-50 30 -40 90 q20 60 -30 90 q-60 10 -70 -60 q-30 -70 10 -120 z" fill="#5BBF6A" ' + O + '/>'
            '<path d="M560 520 q80 -30 150 10 q50 40 30 100 q-40 20 -90 0 q-60 -20 -90 -60 z" fill="#5BBF6A" ' + O + '/>'
            '<path d="M640 700 q60 -10 90 30 q10 60 -40 80 q-50 -10 -60 -60 z" fill="#5BBF6A" ' + O + '/>')
    people = (person(330, 470, 0.55, '#FF6B6B', look=-1) + person(540, 395, 0.55, '#4D96FF') + person(760, 470, 0.55, '#FFB703', look=1)
              + person(250, 820, 0.5, '#2EC4B6', look=-1) + person(840, 830, 0.5, '#C77DFF', look=1))
    svg = ('<rect width="1080" height="1350" fill="#0B1030"/>' + stars
           + '<circle cx="540" cy="700" r="330" fill="#2F8FE0" ' + O + '/>' + land
           + '<path d="M300 520 A330 330 0 0 1 780 520" stroke="#fff" stroke-width="6" fill="none" opacity="0.25"/>' + people
           + bubble(['I wish I lived', 'in Dubai'], 540, 190, 560, (540, 330)))
    return slide(svg, idcard('Everywhere else', 'Dubai') + foot())


def w6():
    return f"""
<section class="slide cta">
  <div class="ctabg"></div>
  <div class="ctab">
    <div class="ctk">Wherever you are on this list&hellip;</div>
    <h2>There's a <em>next step</em> for you in Dubai.</h2>
    <div class="steps">
      <span>Studio</span><i>&rarr;</i><span>Apartment</span><i>&rarr;</i><span>Marina</span><i>&rarr;</i><span>The Palm</span><i>&rarr;</i><span>Villa</span>
    </div>
    <div class="ctabtn">Looking for a property in Dubai?<br><b>Let's talk.</b></div>
  </div>
  <div class="foot big"><img src="img/avatar.png" alt=""><div><div class="fn"><b>{NAME}</b>{TICK}<span>(Dubai Property Consultant)</span></div><div class="fp">{WA}{PHONE}</div></div></div>
</section>"""


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; }}
.scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.bt {{ font-family: Outfit; font-weight: 800; fill: {INK}; text-anchor: middle; }}
.idc {{ position: absolute; left: 40px; right: 40px; bottom: 150px; display: flex; align-items: center; gap: 12px; background: #fff; border: 5px solid {INK}; border-radius: 22px;
  padding: 16px 22px; box-shadow: 8px 8px 0 {INK}; }}
.idc > div:not(.arr) {{ flex: 1; }}
.idc span {{ display: block; font-size: 22px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #6B6B7B; }}
.idc b {{ display: block; font-size: 38px; font-weight: 800; color: {INK}; margin-top: 2px; }}
.idc .w b {{ color: #E8505B; }}
.arr {{ font-size: 50px; font-weight: 800; color: {INK}; }}
.swp {{ position: absolute; right: 44px; bottom: 60px; background: {INK}; color: #fff; font-weight: 700; font-size: 30px; padding: 12px 26px; border-radius: 40px; }}
.slide:first-child .idc {{ bottom: 130px; }}
.foot {{ position: absolute; left: 40px; right: 40px; bottom: 30px; display: flex; align-items: center; gap: 14px; background: rgba(255,255,255,0.94); border: 4px solid {INK}; border-radius: 18px; padding: 10px 18px; }}
.foot img {{ width: 64px; height: 64px; border-radius: 50%; border: 3px solid {INK}; }}
.fn {{ display: flex; align-items: center; gap: 8px; font-size: 26px; color: {INK}; }} .fn .tick {{ width: 24px; height: 24px; }} .fn span {{ font-weight: 800; color: #E8505B; }}
.fp {{ display: flex; align-items: center; gap: 8px; margin-top: 2px; font-size: 24px; font-weight: 700; color: {INK}; }}
.wa {{ width: 26px; height: 26px; }}
.cta {{ background: #FFD447; }}
.ctabg {{ position: absolute; inset: 0; background-image: radial-gradient({INK} 2.2px, transparent 2.5px); background-size: 34px 34px; opacity: 0.12; }}
.ctab {{ position: absolute; left: 60px; right: 60px; top: 150px; color: {INK}; }}
.ctk {{ font-size: 40px; font-weight: 700; }}
.cta h2 {{ margin-top: 20px; font-size: 104px; font-weight: 800; line-height: 1.0; letter-spacing: -0.02em; }}
.cta h2 em {{ font-style: normal; background: #fff; border: 5px solid {INK}; border-radius: 18px; padding: 0 16px; box-shadow: 6px 6px 0 {INK}; display: inline-block; }}
.steps {{ margin-top: 70px; display: flex; flex-wrap: nowrap; align-items: center; gap: 8px; }}
.steps span {{ background: #fff; border: 4px solid {INK}; border-radius: 40px; padding: 10px 16px; font-size: 27px; font-weight: 700; }}
.steps i {{ font-style: normal; font-size: 30px; font-weight: 800; }}
.ctabtn {{ margin-top: 120px; background: {INK}; color: #fff; border-radius: 26px; padding: 34px 40px; font-size: 48px; line-height: 1.2; }} .ctabtn b {{ color: #FFD447; font-size: 64px; }}
.foot.big {{ bottom: 60px; padding: 16px 24px; }} .foot.big img {{ width: 90px; height: 90px; }} .foot.big .fn {{ font-size: 34px; }} .foot.big .fp {{ font-size: 32px; }} .foot.big .wa {{ width: 32px; height: 32px; }}
</style></head><body>
{w1()}{w2()}{w3()}{w4()}{w5()}{w6()}
</body></html>"""
(HERE / 'slides.html').write_text(page)
print('slides.html')
