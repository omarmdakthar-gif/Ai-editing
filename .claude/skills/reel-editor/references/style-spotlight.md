# Spotlight style

Studied from ref01, ref02, ref03, ref06, ref07 and ref09. A real estate professional, or the property itself, is the hero. Oversized words appear to live in the scene with them. It reads as expensive because the footage is clean and the type interacts with depth.

## Variants

| Variant | Refs | When to use | Footage |
|---|---|---|---|
| Walk and talk | 01, 06, 09 | Authority, results, opinion | Slow walk toward camera, full body to mid shot, gimbal |
| Seated authority | 07 | Market takes, Q&A | Office, two angles, desk and laptop in frame |
| Property tour | 02 | Listings | Wide lens, fast glides through rooms, drone, almost no speech |
| Deal breakdown | 03 | Numbers, ROI, leverage | Dark background, person in the lower half, graphics above |

## Fonts
Closest free matches, chosen by eye. The exact originals can't be confirmed from video.
- **Small words:** Sora 300, thin geometric, around 58px on 1080 wide.
- **Big words:** Sora 800, around 130px, very tight letter spacing.
- **Accent words:** Playfair Display italic for elegance, as in ref07's "Real estate", or handwritten marker for deal diagrams in ref03.
- **Numbers:** the biggest thing on screen. They can be 200px or more.

## Colour
- Words are white by default, with one vivid accent per caption: cyan `#39E6E0`, orange `#FF8A1E`, yellow `#FFE14D` or magenta `#E23FD0`.
- Pick the accent from the location or wardrobe. Ref09 used a pale yellow that matched the dress. Ref06 rotated bright colours against a green street.
- Accent words often carry a moving colour or gradient fill.
- Footage is clean and bright, with real colour contrast between skin, sky and interior wood.

## Captions
- Placed around the chest or upper torso, 35–50% down the frame, not along the bottom.
- Appear one word at a time, on the spoken word, with a soft blur-in over about 6 frames.
- Stack 2–4 words as a small word overlapping a big word. Lines nearly touch.
- One key word per thought goes huge. Filler words stay small or show alone, such as "yard." or "lender" in thin white.
- Hide the caption during silent gaps.

## Depth text (the signature)
The headline sits behind the person, so their head overlaps it. Use it in the first few seconds and on 2–3 key words later, such as "156 HOMES SOLD", "tell you", "deals" or "buyer".
Use `depthHeadlines` with `personVideo` from `tools/matte.py`. Refs also use extruded 3D numbers that fill with sky or texture, like ref02's "1890". Build those in HyperFrames when a reel earns it.

## Motion graphics
- Floating glass pills for short phrases, like "Video Content" and "Fast pre-approvals".
- Small 3D objects that orbit or appear near the speaker, such as a logo card or home photo.
- Line charts that draw on beside the speaker, like the interest rate curve in ref06.
- Stat reveal with a counting number, like "$46.3M".
- Contact bubble with photo and phone number during the call to action, as in ref01.
- Deal breakdown: building image fills with colour by share of money, handwritten arrows and underlines draw on, and each number arrives as it's spoken.

## Cutting
- Measured average shot: 1.9s for tours, 2.8–5.5s for talking reels. Ref03 ran 18s with graphics providing the change instead of cuts.
- Change location or angle every few seconds. Ref01 and ref06 stay in the same outfit across several locations.
- Hide cuts with fast whip blurs, flash exposure or a person passing through frame.
- Slow push-in between cuts, so no shot is ever still.

## Sound
- Music plays under everything and stays present. Tours are music-led.
- 67–100% of cuts have a rising high end just before them, which suggests a whoosh. These are measured estimates from the audio and can't fully separate effects from music.
- 62–89% of cuts in most of these reels have a low impact after the cut.
- Tours cut on the beat more than half the time. Talking reels don't need to.
- Master around -17 LUFS.

## Ending
Name, handle and contact on a blurred or black card. Ref01 shows phone number, photo and business card. Ref07 asks viewers to DM, then names exactly what they'll get. For leads, always say the specific reason to reach out.

## Standing elements
Handle with a small Instagram icon, at top right around 25% down. It sometimes moves to the left side. Keep it small.
