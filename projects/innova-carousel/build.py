"""Innova vs Dubai carousel (reuses the Binghatti / Arts District slides).
Original docstring: Binghatti carousel. Slide 1: "RIP" hook with three tombstones, then the offer in the white tweet card.

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

import math
import random


def stars_svg(seed=7, n=150):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, 1080), rnd.uniform(0, 760) ** 1.0
        r = rnd.choice([1.2, 1.5, 1.8, 2.2, 2.8, 3.4])
        o = rnd.uniform(0.45, 1)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{o:.2f}"/>')
    for x, y, sz in [(150, 120, 16), (560, 70, 12), (930, 330, 14), (300, 230, 10)]:   # sparkle stars
        out.append(f'<path d="M{x} {y-sz} L{x+sz*0.22} {y-sz*0.22} L{x+sz} {y} L{x+sz*0.22} {y+sz*0.22} L{x} {y+sz} L{x-sz*0.22} {y+sz*0.22} L{x-sz} {y} L{x-sz*0.22} {y-sz*0.22} Z" fill="#fff"/>')
    out.append('<path d="M640 150 L820 60" stroke="url(#shoot)" stroke-width="4" stroke-linecap="round"/>')   # shooting star
    return ('<svg class="stars" viewBox="0 0 1080 1350"><defs><linearGradient id="shoot" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient></defs>'
            + ''.join(out) + '</svg>')


def splat_svg(seed, w=240, h=240):
    """Blood splatter: a smooth irregular blob (Catmull-Rom through jittered points), droplets and drips."""
    rnd = random.Random(seed)
    cx, cy, R = w * 0.5, h * 0.42, 46
    pts = []
    n = 16
    for k in range(n):
        a = k / n * 2 * math.pi
        r = R * rnd.uniform(0.82, 1.22)
        pts.append((cx + r * math.cos(a), cy + r * 0.85 * math.sin(a)))
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    drops = ''.join(f'<circle cx="{cx + math.cos(a) * dist:.0f}" cy="{cy + math.sin(a) * dist * 0.85:.0f}" r="{r:.1f}"/>'
                    for a, dist, r in ((rnd.uniform(0, 6.28), rnd.uniform(62, 112), rnd.uniform(3, 10)) for _ in range(18)))
    drips = ''.join(f'<path d="M{x-6} {cy+20} L{x-4} {cy+20+L} Q{x} {cy+32+L} {x+4} {cy+20+L} L{x+6} {cy+20} Z"/>'
                    for x, L in ((cx + rnd.uniform(-30, 30), rnd.uniform(35, 80)) for _ in range(3)))
    return f'<svg class="splat" viewBox="0 0 {w} {h}"><g fill="#A3101E"><path d="{d} Z"/>{drops}{drips}</g></svg>'


SKULL = ('<svg viewBox="0 0 100 100"><path fill="#E9E4D8" d="M50 6C27 6 12 22 12 44c0 13 6 22 14 27v13c0 4 3 7 7 7h34c4 0 7-3 7-7V71c8-5 14-14 14-27C88 22 73 6 50 6z"/>'
         '<ellipse cx="34" cy="48" rx="11" ry="12" fill="#1A1D26"/><ellipse cx="66" cy="48" rx="11" ry="12" fill="#1A1D26"/>'
         '<path d="M50 60l-6 11h12z" fill="#1A1D26"/><path d="M36 84v7M44 84v8M52 84v8M60 84v7" stroke="#1A1D26" stroke-width="3"/></svg>')
BONE = ('<svg viewBox="0 0 120 40"><g fill="#E9E4D8"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="28" r="10"/>'
        '<circle cx="108" cy="12" r="10"/><circle cx="108" cy="28" r="10"/><rect x="12" y="13" width="96" height="14" rx="6"/></g></svg>')
HAND = ('<svg viewBox="0 0 120 200"><g fill="#E9E4D8"><rect x="50" y="110" width="20" height="90" rx="8"/>'
        '<rect x="30" y="70" width="60" height="50" rx="16"/><rect x="28" y="20" width="13" height="58" rx="6"/>'
        '<rect x="46" y="8" width="13" height="68" rx="6"/><rect x="64" y="14" width="13" height="62" rx="6"/>'
        '<rect x="82" y="32" width="12" height="48" rx="6"/><rect x="8" y="70" width="30" height="13" rx="6" transform="rotate(-35 20 76)"/></g></svg>')


def tomb(x, rot, line1, line2, fs=84, cls='', seed=1):
    return f'''<div class="tomb" style="left:{x}px;transform:rotate({rot}deg)">{splat_svg(seed)}<div class="rip">RIP</div>
      <div class="t1 {cls}" style="font-size:{fs}px">{line1}</div><div class="t2">{line2}</div></div>'''


def slide1():
    tombs = (tomb(28, -4, '1%', 'payment plans', 110, '', 3) + tomb(370, 1.5, 'AED 800K', 'for a studio', 62, '', 11)
             + tomb(712, 4, '&ldquo;Dubai is<br>too<br>expensive&rdquo;', '', 56, 'quote', 21))
    bones = (f'<div class="skull" style="left:120px;top:1160px;transform:rotate(-12deg)">{SKULL}</div>'
             f'<div class="skull sm" style="left:860px;top:1190px;transform:rotate(14deg)">{SKULL}</div>'
             f'<div class="bone" style="left:250px;top:1235px;transform:rotate(18deg)">{BONE}</div>'
             f'<div class="bone" style="left:700px;top:1250px;transform:rotate(-10deg)">{BONE}</div>'
             f'')
    return f'''
<section class="slide s1">
  {stars_svg()}
  <div class="moon"></div>
  <div class="glow"></div>
  {tombs}
  <div class="ground"></div>
  {bones}
  <div class="swipe">Swipe &rarr;</div>
</section>'''


def slide2():
    clouds = ''.join(f'<div class="cloud" style="left:{x}px;top:{y}px;transform:scale({k})"></div>' for x, y, k in [(60, 470, 1), (700, 520, 0.8), (380, 600, 0.6)])
    return f'''
<section class="slide s2">
  <div class="sun"></div>
  <div class="s2head">Because now,<br>from <span>Binghatti</span>&hellip;</div>
  <div class="s2sub">The developer that has collaborated with<div class="brands"><span>Bugatti</span><i>&amp;</i><span>Mercedes&#8209;Benz</span></div></div>
  <div class="card c2">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <div class="prices big">
      <div><span>Studio</span><em>from</em><b>AED 499K</b></div>
      <div><span>1 bed</span><em>from</em><b>AED 799K</b></div>
      <div><span>2 bed</span><em>from</em><b>AED 1.2M</b></div>
    </div>
    <div class="deal big"><div><b>20%</b><span>down payment</span></div><div class="plus">&amp;</div><div><b>AED 2,500</b><span>a month</span></div></div>
    <p class="fine">*Prices shown are after the 7% discount offered during the EOI stage.</p>
  </div>
</section>'''


def slide3():
    chip = lambda name, mins, x, y, side='l': (f'<div class="mchip {side}" style="{"right" if side == "l" else "left"}:{x}px;top:{y}px">'
                                              f'<span>{name}</span><b>{mins} min</b></div>')
    return f'''
<section class="slide s3">
  <div class="s3head">
    <div class="who light"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div><div class="pill">The location</div></div>
    <h1>Next to <span>Dubai Silicon Oasis</span><br>&amp; <span>Academic City</span></h1>
    <p class="s3sub">Dubai's next district for the arts, by Binghatti.</p>
  </div>
  <div class="map3" style="background-image:url('img/map_location.jpg')">
    {chip('Downtown Dubai', 17, 700, 135)}
    {chip('DXB Airport', 15, 760, 110, 'r')}
    {chip('Dubai Creek Harbour', 14, 625, 232, 'r')}
    {chip('Meydan', 10, 680, 294)}
    <div class="mlab" style="right:556px;top:519px">Dubai Silicon Oasis</div>
    <div class="mlab" style="right:492px;top:640px">Academic City</div>
    <div class="proj" style="left:612px;top:579px">The Arts District</div>
  </div>
</section>'''


def slide4():
    stat = lambda n, l: f'<div class="st4"><b>{n}</b><span>{l}</span></div>'
    return f'''
<section class="slide s4" style="background-image:url('img/map_location.jpg')">
  <div class="s4shade"></div>
  <div class="s3head s4head">
    <div class="who light"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div><div class="pill">The potential</div></div>
    <h1>Why this location is <span>about to boom</span></h1>
  </div>
  <div class="zone dso">
    <div class="zt"><i></i>Dubai Silicon Oasis</div>
    <p>One of the <b>5 main urban centres</b> in the Dubai 2040 Urban Master Plan. Coming next: <b>District IO</b>, a future-tech district.</p>
    <div class="stats4">{stat('AED 11B', 'investment')}{stat('70,000+', 'jobs in 10 years')}{stat('6,500+', 'companies')}</div>
  </div>
  <div class="zone dac">
    <div class="zt"><i></i>Academic City</div>
    <p>Dubai's university hub, right next door. Students, faculty and staff all need homes nearby.</p>
    <div class="stats4">{stat('38,500+', 'students today')}{stat('+40%', 'more students by 2030')}</div>
  </div>
  <div class="zone metro">
    <div class="zt"><i></i>Metro Blue Line</div>
    <p>Dubai Metro's new line will have stations at <b>Dubai Silicon Oasis</b> and <b>Academic City</b>.</p>
    <div class="stats4">{stat('2029', 'opening')}{stat('30 km', 'new line')}{stat('14', 'stations')}</div>
  </div>
  <div class="take">Thousands of new jobs + students next door =<br><b>strong rental demand</b></div>
</section>'''


def slide5():
    return f'''
<section class="slide s5">
  <div class="s5photo" style="background-image:url('img/plaza-000.jpg')"></div>
  <div class="s5fade"></div>
  <div class="s5tag">The Arts District by Binghatti</div>
  <div class="card c5">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <p class="lead5">Student rooms next to Academic City already rent for:</p>
    <div class="rooms">
      <div><i style="background-image:url('img/room_single.jpg')"></i><span>Single room</span><b>AED 6,550<small>/month</small></b></div>
      <div><i style="background-image:url('img/room_twin.jpg')"></i><span>Shared twin room · 200 sq ft</span><b>AED 4,699<small>/month</small></b></div>
    </div>
    <p class="src5">Source: listed rents on a student-housing website, Nov 2026</p>
    <p class="body5">A basic room. <b>No pool, no gym, no community.</b></p>
    <div class="imagine">Now imagine the demand for a <b>studio by a top developer</b>, in a community with <b>world-class amenities</b>.</div>
  </div>
</section>'''


def slide6():
    return f'''
<section class="slide s6">
  <div class="collage">
    <div class="t big" style="background-image:url('img/plaza-000.jpg')"></div>
    <div class="t a" style="background-image:url('img/aerial.jpg')"></div>
    <div class="t b" style="background-image:url('img/violin.jpg')"></div>
    <div class="t c" style="background-image:url('img/kids.jpg')"></div>
    <div class="tag6">The Arts District by Binghatti</div>
  </div>
  <div class="card c6">
    <div class="who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <div class="facts6">
      <div class="f"><b>60/40</b><span>payment plan</span></div>
      <div class="f k"><b>This weekend</b><span>EOI opens</span></div>
    </div>
    <div class="disc">Book at the EOI stage and get an <b>extra 7% discount</b></div>
  </div>
</section>'''


def slide7():
    return f'''
<section class="slide s7" style="background-image:url('img/aerial.jpg')">
  <div class="s7shade"></div>
  <div class="s7box">
    <div class="who s7who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}</div><div class="handle">{HANDLE}</div></div></div>
    <div class="s7q">Want more details?</div>
    <div class="s7c">Comment <mark>ARTS DISTRICT</mark></div>
    <div class="s7d">or DM me</div>
  </div>
</section>'''


RATE_NOTE = "1 AED = ₹25.30 (25 Nov 2026)"


def n1():
    return f'''
<section class="slide n1">
  <div class="n1photo" style="background-image:url('img/innova.jpg')"></div>
  <div class="n1shade"></div>
  <div class="n1top">The new <b>Innova Hycross</b> facelift<br>just launched at <span>₹19.59 lakh*</span></div>
  <div class="stop">DON'T BUY IT YET</div>
  <div class="n1foot">*Ex-showroom starting price</div>
  <div class="swipe">Swipe &rarr;</div>
  {foot()}
</section>'''


def gauge(mins, maxm=30):
    """Dashboard gauge: 240-degree arc, needle at mins/maxm."""
    import math
    cx, cy, r = 110, 110, 88
    def pt(frac, rr=r):
        ang = math.radians(150 + 240 * frac)
        return cx + rr * math.cos(ang), cy + rr * math.sin(ang)
    x0, y0 = pt(0); x1, y1 = pt(1); xm, ym = pt(mins / maxm)
    big = 1 if 240 * mins / maxm > 180 else 0
    ticks = ''.join(f'<line x1="{pt(k/6, 94)[0]:.1f}" y1="{pt(k/6, 94)[1]:.1f}" x2="{pt(k/6, 80)[0]:.1f}" y2="{pt(k/6, 80)[1]:.1f}" stroke="#555" stroke-width="3"/>' for k in range(7))
    nx, ny = pt(mins / maxm, 70)
    return (f'<svg viewBox="0 0 220 200" class="gsvg"><path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 1 1 {x1:.1f} {y1:.1f}" stroke="#2A2A2E" stroke-width="14" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {big} 1 {xm:.1f} {ym:.1f}" stroke="#E0182D" stroke-width="14" fill="none" stroke-linecap="round"/>{ticks}'
            f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="9" fill="#fff"/></svg>')


def kicker(t):
    return f'<div class="kick"><i></i>{t}</div>'


WA_ICON = '<svg class="wa" viewBox="0 0 24 24"><path fill="#25D366" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/><path fill="#fff" d="M16.5 14.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
PHONE = '+971 56 837 6676'


def foot():
    return (f'<div class="nfoot"><img src="img/avatar.png" alt=""><div class="fn"><div><b>{NAME}</b>{TICK}<strong>(Dubai Property Consultant)</strong></div>'
            f'<div class="fp">{WA_ICON}{PHONE}</div></div></div>')


def n2():
    return f'''
<section class="slide nk">
  {kicker('Same ₹25 lakh. Two choices.')}
  <h2 class="nh">For the price of the car,<br>own a <em>₹1.26 crore</em><br>home in Dubai.</h2>
  <div class="tix">
    <div class="tk car"><div class="tl">Option 1</div><div class="tt">Innova Hycross</div><div class="tp">₹25 L</div><div class="ts">Gone. The car is yours, the money is spent.</div><div class="x">&#10005;</div></div>
    <div class="tk home"><div class="tl">Option 2</div><div class="tt">Binghatti studio, Dubai</div><div class="tp">₹1.26 Cr <small>home</small></div>
      <div class="pay"><div><b>₹25.25 L</b><span>20% down payment</span></div><div class="pl">+</div><div><b>AED 2,500</b><span>a month (&asymp; ₹63,000)</span></div></div></div>
  </div>
  <p class="nfine">Studio from AED 499K after the 7% EOI discount. 20% = AED 99,800 &middot; {RATE_NOTE}</p>
  {foot()}
</section>'''


def n3():
    row = lambda k, v, e='': f'<div class="sr"><span>{k}</span><b>{v}</b><em>{e}</em></div>'
    return f'''
<section class="slide nk n3s">
  <div class="n3img" style="background-image:url('img/violin.jpg')"></div>
  <div class="n3grad"></div>
  {kicker('Spec sheet')}
  <h2 class="nh n3h">The Arts District<br><em>by Binghatti</em></h2>
  <div class="spec">
    {row('Developer', 'Binghatti', 'Bugatti &amp; Mercedes-Benz collabs')}
    {row('Studio', 'AED 499K', '&asymp; ₹1.26 Cr')}
    {row('1 bedroom', 'AED 799K', '&asymp; ₹2.02 Cr')}
    {row('2 bedroom', 'AED 1.2M', '&asymp; ₹3.04 Cr')}
    {row('Payment', '20% + AED 2,500/mo', '&asymp; ₹63K a month')}
    {row('EOI offer', 'Extra 7% off', 'prices above include it')}
  </div>
  {foot()}
</section>'''


def n4():
    g = lambda m, place: f'<div class="gg">{gauge(m)}<div class="gm"><b>{m}</b><span>min</span></div><div class="gp">{place}</div></div>'
    return f'''
<section class="slide nk">
  {kicker('Location')}
  <h2 class="nh">Next to <em>Dubai Silicon Oasis</em><br>&amp; <em>Academic City</em></h2>
  <div class="gauges">{g(10, 'Meydan')}{g(14, 'Dubai Creek Harbour')}{g(15, 'DXB Airport')}{g(17, 'Downtown Dubai')}</div>
  <div class="mapstrip" style="background-image:url('img/map_location.jpg')"><div class="pin">The Arts District</div></div>
  {foot()}
</section>'''


def n5():
    step = lambda when, what, detail: f'<div class="tlr"><div class="tw">{when}</div><div class="td"><b>{what}</b><span>{detail}</span></div></div>'
    return f'''
<section class="slide nk">
  {kicker('What is coming next door')}
  <h2 class="nh">This area is<br><em>about to change</em></h2>
  <div class="tline">
    {step('Today', '38,500+ students', 'at Academic City &amp; Dubai Knowledge Park')}
    {step('2029', 'Metro Blue Line opens', 'stations at Dubai Silicon Oasis &amp; Academic City')}
    {step('2030', '+40% more students', 'forecast growth in Dubai higher education')}
    {step('Next 10 yrs', 'District IO at DSO', 'AED 11B investment &middot; 70,000+ jobs')}
    {step('2040', 'A main urban centre', 'DSO in the Dubai 2040 Urban Master Plan')}
  </div>
  {foot()}
</section>'''


def n6():
    li = lambda t: f'<li>{t}</li>'
    return f'''
<section class="slide nk">
  {kicker('Fast forward 5 years')}
  <h2 class="nh">Where will your<br><em>₹25 lakh</em> be?</h2>
  <div class="ff">
    <div class="fc down"><div class="fa">&#8600;</div><div class="ft">The car</div><ul>{li('Worth less every year')}{li('Fuel, insurance and service bills')}{li('Ready to be replaced')}</ul></div>
    <div class="fc up"><div class="fa">&#8599;</div><div class="ft">The Dubai home</div><ul>{li('Handed over and ready to rent')}{li('Next to new jobs, students and a metro line')}{li('An asset by a top developer')}</ul></div>
  </div>
  <div class="nquote">Drive the car you have. <b>Let your ₹25 lakh work for you.</b></div>
  {foot()}
</section>'''


def n7():
    return f'''
<section class="slide nk n7s">
  <div class="n7img" style="background-image:url('img/kids.jpg')"></div>
  <div class="n7grad"></div>
  <div class="n7box">
    <div class="n7who"><img src="img/avatar.png" alt=""><div><div class="name">{NAME}{TICK}<strong class="cons">(Dubai Property Consultant)</strong></div><div class="handle n7ph">{WA_ICON}{PHONE}</div></div></div>
    <div class="n7q">Your ₹25 lakh.<br>Your choice.</div>
    <div class="n7c">Comment <b>ARTS DISTRICT</b></div>
    <div class="n7d">or DM me for the price list &amp; payment plan</div>
  </div>
</section>'''


face = lambda w: f"@font-face{{font-family:Outfit;font-weight:{w};src:url('file://{FONTS}/outfit-latin-{w}-normal.woff2') format('woff2')}}"
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{face(400)}{face(500)}{face(600)}{face(700)}{face(800)}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #111; font-family: Outfit, sans-serif; }}
.slide {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; }}
.s1 {{ background: radial-gradient(70% 45% at 75% 8%, #3A4766 0%, #151B2C 45%, #07090F 100%); }}
.s1::before {{ content: ''; position: absolute; inset: 0; background: none; }}
.s1 .glow {{ position: absolute; left: 50%; top: 600px; width: 1200px; height: 700px; transform: translate(-50%,-50%); background: radial-gradient(closest-side, rgba(200,215,255,0.28), transparent); }}
.moon {{ position: absolute; right: 110px; top: 70px; width: 120px; height: 120px; border-radius: 50%; background: #F3EBD3; box-shadow: 0 0 60px rgba(243,235,211,0.5); }}
.tomb {{ position: absolute; top: 210px; width: 340px; height: 920px; border-radius: 170px 170px 12px 12px; background: linear-gradient(180deg, #E4E8EF, #A9B1BF);
  box-shadow: inset 0 -20px 40px rgba(0,0,0,0.25), 0 20px 40px rgba(0,0,0,0.5); text-align: center; padding-top: 200px; color: #1F2430; }}
.rip {{ position: relative; font-weight: 800; font-size: 140px; line-height: 1; letter-spacing: 0.02em; text-shadow: 0 2px 0 rgba(255,255,255,0.6), 0 -2px 0 rgba(0,0,0,0.25); color: #1F232C; }}
.t1 {{ position: relative; margin-top: 60px; font-weight: 800; font-size: 72px; line-height: 1.12; white-space: nowrap; color: #000; }}
.t2 {{ position: relative; margin-top: 16px; font-weight: 800; font-size: 42px; line-height: 1.1; color: #000; }}
.ground {{ position: absolute; left: 0; right: 0; top: 1080px; height: 280px; background: linear-gradient(180deg, #1B2A1E, #07090F); border-radius: 50% 50% 0 0 / 30px 30px 0 0; }}
.t1.quote {{ font-style: italic; color: #000; }}
.stars {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.splat {{ position: absolute; left: 120px; top: 540px; width: 250px; height: 250px; opacity: 0.92; }}
.skull, .bone, .hand {{ position: absolute; filter: drop-shadow(0 6px 10px rgba(0,0,0,0.6)); }}
.skull {{ width: 110px; height: 110px; }} .skull.sm {{ width: 80px; height: 80px; }}
.bone {{ width: 130px; height: 44px; }} .hand {{ width: 90px; height: 150px; }}
.swipe {{ position: absolute; left: 50%; bottom: 70px; transform: translateX(-50%); padding: 14px 34px; border-radius: 40px; background: #FFD43B; color: #111;
  font-weight: 800; font-size: 34px; letter-spacing: 0.04em; }}
.s2 {{ background: linear-gradient(180deg, #1F7FD6 0%, #4AA3EC 40%, #9FD3F7 75%, #D9F0FD 100%); }}
.sun {{ position: absolute; right: -60px; top: -60px; width: 420px; height: 420px; border-radius: 50%;
  background: radial-gradient(circle, #FFFBE6 0%, #FFE680 30%, rgba(255,230,128,0.35) 50%, rgba(255,230,128,0) 70%); }}
.cloud {{ position: absolute; width: 300px; height: 90px; background: #fff; border-radius: 60px; opacity: 0.9; transform-origin: left top; }}
.cloud::before, .cloud::after {{ content: ''; position: absolute; background: #fff; border-radius: 50%; }}
.cloud::before {{ width: 130px; height: 130px; left: 50px; top: -65px; }} .cloud::after {{ width: 100px; height: 100px; left: 150px; top: -45px; }}
.s2sub {{ position: absolute; left: 70px; right: 70px; top: 360px; color: #fff; font-size: 46px; line-height: 1.22; font-weight: 500; text-shadow: 0 3px 16px rgba(0,40,90,0.45); }}
.s2sub b {{ font-weight: 800; }}
.brands {{ display: flex; align-items: center; gap: 16px; margin-top: 30px; }}
.brands span {{ background: #fff; color: #0B1530; border-radius: 20px; padding: 20px 34px; font-weight: 800; font-size: 64px; letter-spacing: 0.01em; text-shadow: none;
  box-shadow: 0 10px 30px rgba(0,40,90,0.3); }}
.brands i {{ font-style: normal; font-weight: 800; font-size: 60px; }}
.s2head {{ position: absolute; left: 70px; right: 70px; top: 90px; color: #fff; font-weight: 800; font-size: 92px; line-height: 1.05; letter-spacing: -0.01em;
  text-shadow: 0 6px 24px rgba(0,40,90,0.45); }}
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
.fine {{ margin-top: 16px; font-size: 22px; color: #6B7280; text-align: center; }}
.body.big {{ margin-top: 24px; font-size: 32px; }}
.deal.big .plus {{ font-size: 56px; }}
.s3 {{ background: #0B1226; }}
.s3head {{ height: 460px; padding: 44px 50px 0; background: linear-gradient(180deg, #1F7FD6, #4AA3EC); color: #fff; }}
.who.light {{ margin-bottom: 20px; }} .who.light .handle {{ color: #DCEBFA; }}
.who.light img {{ width: 84px; height: 84px; }} .who.light .name {{ font-size: 34px; }} .who.light .handle {{ font-size: 25px; }}
.pill {{ margin-left: auto; padding: 8px 22px; border-radius: 30px; background: #FFD43B; color: #111; font-weight: 800; font-size: 24px; white-space: nowrap; }}
.s3head h1 {{ margin-top: 30px; font-size: 70px; font-weight: 800; line-height: 1.08; text-shadow: 0 4px 20px rgba(0,40,90,0.35); }}
.s3head h1 span {{ color: #FFD43B; }}
.s3sub {{ margin-top: 18px; font-size: 36px; font-weight: 500; color: #EAF4FF; }}
.map3 {{ position: relative; width: 1080px; height: 890px; background-size: cover; background-position: center top; }}
.mchip {{ position: absolute; display: flex; align-items: center; gap: 12px; padding: 8px 10px 8px 18px; border-radius: 14px; background: rgba(10,16,32,0.9);
  border: 1.5px solid rgba(120,200,230,0.6); color: #fff; font-weight: 600; font-size: 26px; white-space: nowrap; transform: translateY(-50%); }}
.mchip b {{ background: #FFD43B; color: #111; border-radius: 9px; padding: 4px 12px; font-weight: 800; }}
.mlab {{ position: absolute; padding: 8px 18px; border-radius: 12px; background: rgba(40,20,60,0.9); border: 1.5px solid rgba(199,125,255,0.8); color: #fff;
  font-weight: 700; font-size: 28px; white-space: nowrap; transform: translateY(-50%); }}
.proj {{ position: absolute; padding: 12px 24px; border-radius: 14px; background: #FFD43B; color: #111; font-weight: 800; font-size: 36px; white-space: nowrap;
  transform: translateY(-50%); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
.s4 {{ background-color: #0B1226; background-size: cover; background-position: center 60%; }}
.s4shade {{ position: absolute; inset: 0; background: rgba(6,10,24,0.72); }}
.s4head {{ position: relative; height: 250px; }} .s4head h1 {{ font-size: 52px; white-space: nowrap; margin-top: 20px; }}
.zone {{ position: relative; margin: 28px 50px 0; background: #fff; border-radius: 24px; padding: 22px 30px 24px; color: #111; }}
.zt {{ display: flex; align-items: center; gap: 14px; font-size: 38px; font-weight: 800; }}
.zt i {{ width: 22px; height: 22px; border-radius: 50%; background: #C77DFF; box-shadow: 0 0 0 6px rgba(199,125,255,0.25); }}
.zone p {{ margin-top: 8px; font-size: 27px; line-height: 1.3; color: #2A2F38; }} .zone p b {{ color: #111; font-weight: 700; }}
.stats4 {{ display: flex; gap: 10px; margin-top: 12px; }}
.st4 {{ flex: 1; background: #111; border-radius: 14px; padding: 12px 18px; }}
.st4 b {{ display: block; font-size: 42px; font-weight: 800; color: #FFC940; line-height: 1; white-space: nowrap; }}
.st4 span {{ display: block; margin-top: 4px; font-size: 21px; font-weight: 600; color: #E8ECF4; }}
.take {{ position: absolute; left: 50px; right: 50px; bottom: 30px; background: #FFD43B; color: #111; border-radius: 20px; padding: 16px 26px;
  font-size: 30px; line-height: 1.25; text-align: center; font-weight: 500; }} .take b {{ font-weight: 800; }}
.zone.metro .zt i {{ background: #2F7BFF; box-shadow: 0 0 0 6px rgba(47,123,255,0.25); }}
.s5 {{ background: #0B1226; }}
.s5photo {{ position: absolute; left: 0; right: 0; top: 0; height: 640px; background-size: cover; background-position: center; }}
.s5fade {{ position: absolute; left: 0; right: 0; top: 400px; height: 260px; background: linear-gradient(rgba(11,18,38,0), #0B1226); }}
.s5tag {{ position: absolute; left: 50px; top: 50px; padding: 10px 22px; border-radius: 30px; background: rgba(10,16,32,0.75); color: #fff; font-weight: 700; font-size: 26px; }}
.c5 {{ bottom: 50px; padding: 34px 42px 38px; }}
.c5 .who img {{ width: 80px; height: 80px; }} .c5 .name {{ font-size: 32px; }} .c5 .handle {{ font-size: 24px; }}
.lead5 {{ font-size: 34px; line-height: 1.25; font-weight: 600; }}
.rooms {{ display: flex; gap: 12px; margin-top: 16px; }}
.rooms div {{ flex: 1; background: #F1F2F5; border-radius: 16px; padding: 16px 20px 14px; }}
.rooms i {{ display: block; height: 170px; margin: -6px -10px 12px; border-radius: 12px; background-size: cover; background-position: center; }}
.rooms span {{ display: block; font-size: 22px; font-weight: 600; color: #5B6470; }}
.rooms b {{ display: block; margin-top: 6px; font-size: 46px; font-weight: 800; white-space: nowrap; }} .rooms small {{ font-size: 22px; font-weight: 600; color: #5B6470; }}
.src5 {{ margin-top: 8px; font-size: 20px; color: #8A9099; }}
.body5 {{ margin-top: 12px; font-size: 32px; color: #2A2F38; }} .body5 b {{ color: #111; }}
.imagine {{ margin-top: 18px; background: #FFD43B; border-radius: 18px; padding: 20px 24px; font-size: 34px; line-height: 1.28; }} .imagine b {{ font-weight: 800; }}
.s6 {{ background: #0B1226; }}
.collage {{ position: absolute; left: 30px; right: 30px; top: 30px; height: 860px; display: grid; grid-template-columns: 1.3fr 1fr 1fr; grid-template-rows: 1.15fr 1fr; gap: 12px; }}
.collage .t {{ background-size: cover; background-position: center; border-radius: 18px; }}
.collage .big {{ grid-column: 1 / 4; grid-row: 1; }}
.collage .a {{ grid-column: 1; grid-row: 2; }}
.collage .b {{ grid-column: 2; grid-row: 2; background-position: 45% 40%; }}
.collage .c {{ grid-column: 3; grid-row: 2; background-position: center 55%; }}
.tag6 {{ position: absolute; left: 20px; top: 20px; padding: 10px 22px; border-radius: 30px; background: rgba(10,16,32,0.78); color: #fff; font-weight: 700; font-size: 26px; }}
.c6 {{ left: 30px; right: 30px; bottom: 30px; padding: 26px 38px 30px; }}
.c6 .who {{ margin-bottom: 18px; }} .c6 .who img {{ width: 76px; height: 76px; }} .c6 .name {{ font-size: 32px; }} .c6 .handle {{ font-size: 24px; }}
.facts6 {{ display: flex; gap: 12px; }}
.facts6 .f {{ flex: 1; background: #FFD43B; border-radius: 18px; padding: 18px 22px; }}
.facts6 .f.k {{ background: #111; color: #fff; }} .facts6 .f.k b {{ color: #FFC940; }}
.facts6 b {{ display: block; font-size: 52px; font-weight: 800; line-height: 1; white-space: nowrap; }}
.facts6 span {{ display: block; margin-top: 8px; font-size: 26px; font-weight: 600; }}
.disc {{ margin-top: 14px; border: 3px dashed #E0182D; background: #FFF0F1; color: #111; border-radius: 18px; padding: 18px 24px; font-size: 34px; text-align: center; line-height: 1.25; }}
.disc b {{ color: #C8102E; font-weight: 800; }}
.s7 {{ background-size: cover; background-position: center; }}
.s7shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.35) 50%, rgba(0,0,0,0.75) 100%); }}
.s7box {{ position: absolute; left: 60px; right: 60px; bottom: 90px; background: #fff; border-radius: 36px; padding: 44px 46px 54px; text-align: center; color: #111; }}
.s7who {{ justify-content: center; margin-bottom: 28px; }} .s7who img {{ width: 90px; height: 90px; }} .s7who .name {{ font-size: 36px; }} .s7who .handle {{ font-size: 26px; text-align: left; }}
.s7q {{ font-size: 60px; font-weight: 800; }}
.s7c {{ margin-top: 20px; font-size: 62px; font-weight: 700; white-space: nowrap; }}
.s7c mark {{ background: #FFD43B; color: #111; padding: 0 18px; border-radius: 16px; font-weight: 800; }}
.s7d {{ margin-top: 16px; font-size: 48px; font-weight: 600; color: #3A414C; }}
.n1 {{ background: #05070D; }}
.n1photo {{ position: absolute; left: 0; right: 0; top: 200px; height: 720px; background-size: cover; background-position: center; }}
.n1shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, #05070D 0%, rgba(5,7,13,0) 24%, rgba(5,7,13,0) 56%, #05070D 70%); }}
.n1top {{ position: absolute; left: 60px; right: 60px; top: 70px; color: #fff; font-size: 58px; font-weight: 600; line-height: 1.15; text-align: center; }}
.n1top b {{ font-weight: 800; }} .n1top span {{ color: #FFD43B; font-weight: 800; }}
.stop {{ position: absolute; left: 50%; top: 880px; transform: translateX(-50%) rotate(-4deg); white-space: nowrap; background: #E0182D; color: #fff; font-weight: 800; font-size: 92px;
  letter-spacing: 0.03em; padding: 18px 44px; border-radius: 22px; border: 8px solid #fff; box-shadow: 0 20px 50px rgba(224,24,45,0.5); }}
.n1foot {{ position: absolute; left: 60px; bottom: 176px; color: #8A9099; font-size: 22px; }}
.n1 .swipe {{ left: auto; right: 60px; transform: none; bottom: 160px; }}
.n2 {{ background: linear-gradient(180deg, #0B1530 0%, #1F3A7A 100%); }}
.c2n {{ top: 60px; bottom: 60px; left: 60px; right: 60px; padding: 44px 50px; display: flex; flex-direction: column; justify-content: center; }}
.n2a {{ font-size: 46px; line-height: 1.28; color: #2A2F38; }} .n2a b {{ color: #111; font-weight: 800; }}
.big25 {{ font-size: 176px; font-weight: 800; line-height: 1; margin: 12px 0 30px; color: #111; }}
.vs {{ display: flex; align-items: stretch; gap: 14px; margin-top: 34px; }}
.vs > div:not(.vmid) {{ flex: 1; border-radius: 20px; padding: 22px 24px; }}
.vcar {{ background: #F1F2F5; }} .vhome {{ background: #FFD43B; }}
.vs span {{ display: block; font-size: 27px; font-weight: 600; color: #3A414C; }}
.vs b {{ display: block; font-size: 64px; font-weight: 800; margin-top: 6px; white-space: nowrap; }}
.vs em {{ display: block; font-style: normal; font-size: 26px; font-weight: 700; margin-top: 4px; }}
.vmid {{ align-self: center; font-size: 64px; font-weight: 800; color: #111; }}
.c2n .fine {{ margin-top: 22px; font-size: 22px; }}
.prices.big.inr b small {{ display: block; font-size: 22px; font-weight: 600; color: #6B7280; margin-top: 2px; }}
.prices.big.inr div {{ padding: 12px 0; }}
.n3 .s2head {{ top: 60px; font-size: 84px; }}
.n3 .s2sub {{ top: 290px; }}
.n3 .c2 {{ bottom: 40px; padding: 28px 40px 30px; }}
.n3 .c2 .who {{ margin-bottom: 4px; }}
.n6 {{ background: #0B1226; }}
.n6head {{ height: 300px; padding: 40px 50px 0; background: linear-gradient(180deg, #1F7FD6, #4AA3EC); color: #fff; }}
.n6head h1 {{ margin-top: 26px; font-size: 76px; font-weight: 800; text-shadow: 0 4px 20px rgba(0,40,90,0.35); }} .n6head h1 span {{ color: #FFD43B; }}
.cmp {{ margin: 34px 40px 0; background: #fff; border-radius: 26px; padding: 18px 26px 10px; }}
.ch, .cr {{ display: grid; grid-template-columns: 200px 1fr 1fr; gap: 16px; align-items: center; }}
.ch {{ padding: 10px 0 14px; }}
.cr {{ padding: 30px 0; border-top: 2px solid #E6E8EC; }}
.ck {{ font-size: 24px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.04em; }}
.cl {{ font-size: 31px; color: #3A414C; line-height: 1.25; }}
.cv {{ font-size: 31px; color: #111; font-weight: 700; line-height: 1.25; background: #FFF6D6; border-radius: 12px; padding: 10px 14px; }}
.cl.hd {{ font-size: 30px; font-weight: 800; color: #111; }} .cv.hd {{ font-size: 30px; font-weight: 800; background: #FFD43B; }}
.n6t {{ bottom: 44px; }}
.nk {{ background: radial-gradient(90% 60% at 80% 0%, #2A0A10 0%, #0A0A0C 55%, #050506 100%); color: #fff; padding: 70px 60px 0; }}
.kick {{ display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: #FF5A6A; }}
.kick i {{ width: 46px; height: 6px; background: #E0182D; border-radius: 3px; }}
.nh {{ margin-top: 24px; font-size: 76px; font-weight: 800; line-height: 1.05; letter-spacing: -0.01em; }}
.nh em {{ font-style: normal; color: #FFD43B; }}
.nfoot {{ position: absolute; left: 60px; right: 60px; bottom: 44px; display: flex; align-items: center; gap: 12px; font-size: 26px; color: #fff; border-top: 2px solid #26262B; padding-top: 22px; }}
.nfoot img {{ width: 72px; height: 72px; border-radius: 50%; border: 2px solid #FFD43B; }}
.fn > div:first-child {{ display: flex; align-items: center; gap: 8px; font-size: 28px; }}
.fn .tick {{ width: 26px; height: 26px; }} .fn strong, .cons {{ font-weight: 800; color: #FFD43B; margin-left: 6px; }}
.fp, .n7ph {{ display: flex; align-items: center; gap: 8px; margin-top: 4px; font-size: 26px; font-weight: 700; color: #fff; letter-spacing: 0.02em; }}
.wa {{ width: 28px; height: 28px; }}
.tix {{ margin-top: 48px; display: grid; gap: 22px; }}
.tk {{ position: relative; border-radius: 24px; padding: 28px 32px; }}
.tk.car {{ background: #18181C; border: 2px solid #2A2A30; color: #8A8F99; }}
.tk.car .tp {{ text-decoration: line-through; text-decoration-color: #E0182D; text-decoration-thickness: 6px; color: #C9CDD3; }}
.tk .x {{ position: absolute; right: 30px; top: 26px; width: 64px; height: 64px; border-radius: 50%; background: #E0182D; color: #fff; display: grid; place-items: center; font-size: 34px; font-weight: 800; }}
.tk.home {{ background: linear-gradient(135deg, #FFE27A, #FFC940); color: #111; box-shadow: 0 20px 60px rgba(255,201,64,0.25); }}
.tl {{ font-size: 22px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.8; }}
.tt {{ font-size: 40px; font-weight: 700; margin-top: 4px; }}
.tp {{ font-size: 84px; font-weight: 800; line-height: 1.05; margin-top: 6px; }} .tp small {{ font-size: 36px; font-weight: 700; }}
.ts {{ font-size: 28px; margin-top: 6px; }}
.pay {{ display: flex; align-items: center; gap: 14px; margin-top: 18px; }}
.pay > div:not(.pl) {{ flex: 1; background: #111; color: #fff; border-radius: 16px; padding: 14px 18px; }}
.pay b {{ display: block; font-size: 46px; font-weight: 800; color: #FFD43B; line-height: 1; }} .pay span {{ display: block; margin-top: 6px; font-size: 22px; font-weight: 600; }}
.pl {{ font-size: 44px; font-weight: 800; }}
.nfine {{ margin-top: 18px; font-size: 21px; color: #8A8F99; }}
.n3img {{ position: absolute; inset: 0; background-size: cover; background-position: center 30%; }}
.n3grad {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,5,6,0.88) 0%, rgba(5,5,6,0.35) 30%, rgba(5,5,6,0.75) 52%, #050506 70%); }}
.n3s > *:not(.n3img):not(.n3grad):not(.nfoot) {{ position: relative; }}
.n3h {{ font-size: 80px; }}
.spec {{ margin-top: 330px; background: rgba(15,15,18,0.85); border: 2px solid #2A2A30; border-radius: 24px; padding: 8px 30px; backdrop-filter: blur(6px); }}
.sr {{ display: grid; grid-template-columns: 200px 1fr auto; gap: 16px; align-items: baseline; padding: 15px 0; border-bottom: 1.5px solid #2A2A30; }}
.sr:last-child {{ border-bottom: none; }}
.sr span {{ font-size: 22px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #FF5A6A; }}
.sr b {{ font-size: 38px; font-weight: 800; white-space: nowrap; }} .sr em {{ font-style: normal; font-size: 24px; color: #C9CDD3; text-align: right; }}
.n3s .nfoot {{ position: absolute; }}
.gauges {{ margin-top: 44px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.gg {{ position: relative; background: #121215; border: 2px solid #26262B; border-radius: 22px; padding: 14px 10px 18px; text-align: center; }}
.gsvg {{ width: 200px; height: 182px; }}
.gm {{ margin-top: -40px; }} .gm b {{ font-size: 64px; font-weight: 800; line-height: 1; }} .gm span {{ display: inline !important; margin-left: 6px; }} .gm span {{ display: block; font-size: 22px; color: #8A8F99; font-weight: 700; letter-spacing: 0.1em; }}
.gp {{ margin-top: 6px; font-size: 28px; font-weight: 700; }}
.mapstrip {{ position: relative; margin-top: 20px; height: 200px; border-radius: 20px; background-size: cover; background-position: center 70%; border: 2px solid #26262B; }}
.mapstrip .pin {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); background: #FFD43B; color: #111; font-weight: 800; font-size: 30px; padding: 10px 22px; border-radius: 12px; }}
.tline {{ margin-top: 64px; position: relative; padding-left: 10px; }}
.tline::before {{ content: ''; position: absolute; left: 189px; top: 18px; bottom: 30px; width: 4px; background: linear-gradient(#E0182D, #FFD43B); border-radius: 2px; }}
.tlr {{ display: grid; grid-template-columns: 160px 1fr; gap: 50px; align-items: start; margin-bottom: 52px; position: relative; }}
.tlr::before {{ content: ''; position: absolute; left: 170px; top: 10px; width: 22px; height: 22px; border-radius: 50%; background: #fff; border: 5px solid #E0182D; }}
.tw {{ font-size: 30px; font-weight: 800; color: #FFD43B; text-align: right; padding-top: 2px; white-space: nowrap; }}
.td b {{ display: block; font-size: 46px; font-weight: 800; }} .td span {{ display: block; margin-top: 6px; font-size: 29px; color: #C9CDD3; }}
.ff {{ margin-top: 46px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.fc {{ border-radius: 24px; padding: 34px 30px 40px; }}
.fc.down {{ background: #18181C; border: 2px solid #3A1A1F; }} .fc.up {{ background: linear-gradient(160deg, #FFE27A, #FFC940); color: #111; }}
.fa {{ width: 80px; height: 80px; border-radius: 50%; display: grid; place-items: center; font-size: 50px; font-weight: 800; }}
.down .fa {{ background: #E0182D; color: #fff; }} .up .fa {{ background: #111; color: #FFD43B; }}
.ft {{ margin-top: 22px; font-size: 48px; font-weight: 800; }}
.fc ul {{ margin-top: 20px; padding-left: 1.1em; display: grid; gap: 22px; font-size: 34px; line-height: 1.25; }}
.down ul {{ color: #C9CDD3; }}
.nquote {{ margin-top: 50px; border-left: 8px solid #E0182D; padding: 8px 0 8px 26px; font-size: 40px; line-height: 1.25; }} .nquote b {{ color: #FFD43B; }}
.n7s {{ padding: 0; }}
.n7img {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
.n7grad {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,5,6,0.1) 20%, rgba(5,5,6,0.85) 62%, #050506 85%); }}
.n7box {{ position: absolute; left: 60px; right: 60px; bottom: 80px; }}
.n7who {{ display: flex; align-items: center; gap: 18px; }} .n7who img {{ width: 84px; height: 84px; border-radius: 50%; border: 3px solid #FFD43B; }}
.n7who .name {{ font-size: 34px; display: flex; align-items: center; gap: 8px; }} .n7who .cons {{ font-size: 28px; }} .n7ph {{ font-size: 28px; color: #fff !important; }} .n7who .handle {{ color: #C9CDD3; font-size: 24px; }}
.n7q {{ margin-top: 26px; font-size: 92px; font-weight: 800; line-height: 1.02; }}
.n7c {{ margin-top: 30px; display: inline-block; background: #E0182D; color: #fff; font-size: 60px; font-weight: 700; padding: 16px 32px; border-radius: 20px; }} .n7c b {{ font-weight: 800; color: #FFD43B; }}
.n7d {{ margin-top: 20px; font-size: 34px; color: #E8ECF4; }}
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
{n1()}
{n2()}
{n3()}
{n4()}
{n5()}
{n6()}
{n7()}
</body></html>'''
(HERE / 'slides.html').write_text(page)
print('slides.html')
