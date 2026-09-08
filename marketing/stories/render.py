"""Render draft Instagram story frames (1080x1920) for Soul Events' launch week.

Every photograph is the studio's own, pulled from the event decks in
~/Downloads (extracted into the scratchpad as pdfimg/<slug>/). Stickers are
drawn as mock-ups of Instagram's native ones so the client can see where each
sits; the real sticker is added in the Instagram app when posting.

    python3 marketing/stories/render.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import json, glob, os

SP   = "/private/tmp/claude-501/-Users-4bhinav-devroar-soul-client-soulevents/d049d142-8131-4be0-8201-1ea72e35e394/scratchpad"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT  = os.path.join(REPO, "marketing", "stories", "frames"); os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
STICKERS = False   # the client adds every sticker in the Instagram app; frames stay clean

# ---- palette (the site's tokens) ----
PORC  = (248, 247, 244); INK = (26, 26, 34); INKP = (46, 34, 40)
PLUM  = (123, 59, 84);   PLUMD = (90, 42, 63); PLUMS = (169, 107, 133)
BLUE  = (197, 214, 233); BLUSH = (246, 220, 227); HAIR = (231, 229, 224)

def F(name, size, weight=None):
    f = ImageFont.truetype(f"{SP}/fonts/{name}.ttf", size)
    if weight:
        try: f.set_variation_by_name(weight)
        except Exception: pass
    return f
def DISPLAY(s): return F("Marcellus", s)
def ITAL(s):    return F("InstrumentSerif-Italic", s)
def SANS(s, w="Medium"): return F("SpaceGrotesk", s, w)
def MONO(s):    return F("SpaceMono", s)

def src(slug, i): return sorted(glob.glob(f"{SP}/pdfimg/{slug}/*"))[i - 1]

def cover(im, w, h, focus=(0.5, 0.5)):
    im = im.convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = round((im.width - w) * focus[0]); y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))

def vgrad(w, h, c, a_top, a_bot):
    g = Image.new("RGBA", (w, h)); px = g.load()
    for y in range(h):
        a = round(a_top + (a_bot - a_top) * y / max(1, h - 1))
        for x in range(w): px[x, y] = (*c, a)
    return g

def wash(canvas, top_a=40, bot_a=170, tint=INKP):
    canvas.alpha_composite(vgrad(W, H, tint, top_a, bot_a)); return canvas

def wrap(text, font, maxw):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10))); out = []; cur = ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def brand_bar(d, canvas, light=True, y=112):
    mark = Image.open(f"{REPO}/assets/brand/soul-mark.png").convert("RGBA")
    mark = mark.resize((64, round(64 * mark.height / mark.width)), Image.LANCZOS)
    canvas.alpha_composite(mark, (88, y - 8))
    ink = INKP if light else PORC
    d.text((168, y - 2), "SOUL", font=F("Marcellus", 40), fill=ink)
    d.text((300, y + 12), "events", font=MONO(22), fill=PLUM if light else BLUSH)
    d.text((W - 88 - d.textlength("@souleventsindia", font=MONO(22)), y + 8), "@souleventsindia", font=MONO(22), fill=ink)

# ---------------- sticker mock-ups ----------------
def sticker_poll(canvas, d, y, q, opts, w=760):
    if not STICKERS: return y
    x = (W - w) // 2
    box = (x, y, x + w, y + 92 + 100 * len(opts) + 24)
    rrect(d, box, 34, fill=(255, 255, 255, 255))
    d.text((x + 44, y + 34), q, font=SANS(32, "SemiBold"), fill=INK)
    yy = y + 100
    for i, o in enumerate(opts):
        rrect(d, (x + 32, yy, x + w - 32, yy + 78), 20, fill=(*BLUSH, 255) if i == 0 else (*PORC, 255), outline=(*HAIR, 255), width=2)
        d.text((x + 64, yy + 22), o, font=SANS(30, "Medium"), fill=INK); yy += 100
    return box[3]

def sticker_slider(canvas, d, y, q, w=760):
    if not STICKERS: return y
    x = (W - w) // 2
    rrect(d, (x, y, x + w, y + 210), 34, fill=(255, 255, 255, 255))
    d.text((x + 44, y + 34), q, font=SANS(32, "SemiBold"), fill=INK)
    d.rounded_rectangle((x + 44, y + 130, x + w - 44, y + 150), radius=10, fill=(*HAIR, 255))
    cx = x + 44 + int((w - 88) * .68)
    d.rounded_rectangle((x + 44, y + 130, cx, y + 150), radius=10, fill=(*PLUMS, 255))
    d.ellipse((cx - 34, y + 106, cx + 34, y + 174), fill=(255, 255, 255, 255), outline=(*PLUM, 255), width=3)
    d.text((cx - 14, y + 122), "◆", font=SANS(28), fill=PLUM)
    return y + 210

def sticker_quiz(canvas, d, y, q, opts, correct, w=760):
    if not STICKERS: return y
    x = (W - w) // 2
    rrect(d, (x, y, x + w, y + 100 + 92 * len(opts) + 20), 34, fill=(*INKP, 255))
    d.text((x + 44, y + 34), q, font=SANS(32, "SemiBold"), fill=PORC)
    yy = y + 104
    for i, o in enumerate(opts):
        ok = (i == correct)
        rrect(d, (x + 32, yy, x + w - 32, yy + 72), 18, fill=(*BLUE, 255) if ok else (72, 60, 66, 255), outline=(104, 90, 96, 255), width=1)
        d.text((x + 60, yy + 18), f"{'ABCD'[i]}   {o}", font=SANS(28, "Medium"), fill=INK if ok else PORC); yy += 92
    return yy + 20

def sticker_question(canvas, d, y, q, w=760):
    if not STICKERS: return y
    x = (W - w) // 2
    rrect(d, (x, y, x + w, y + 220), 34, fill=(255, 255, 255, 255))
    d.text((x + 44, y + 34), q, font=SANS(32, "SemiBold"), fill=INK)
    rrect(d, (x + 32, y + 110, x + w - 32, y + 190), 20, fill=(*PORC, 255), outline=(*HAIR, 255), width=2)
    d.text((x + 64, y + 134), "Type something...", font=SANS(28), fill=(150, 146, 152))
    return y + 220

def sticker_countdown(canvas, d, y, label, w=680):
    if not STICKERS: return y
    x = (W - w) // 2
    rrect(d, (x, y, x + w, y + 236), 34, fill=(*PLUMD, 255))
    d.text((x + 44, y + 30), label.upper(), font=MONO(24), fill=BLUSH)
    dd = d.textlength("02 : 19 : 40", font=DISPLAY(88))
    d.text((x + (w - dd) / 2, y + 74), "02 : 19 : 40", font=DISPLAY(88), fill=PORC)
    lab = "DAYS     HRS      MIN"
    d.text((x + (w - d.textlength(lab, font=MONO(22))) / 2, y + 176), lab, font=MONO(22), fill=BLUSH)
    return y + 236

def sticker_link(canvas, d, y, text="souleventsindia.com"):
    if not STICKERS: return y
    f = SANS(30, "SemiBold"); tw = d.textlength(text, font=f) + 150; x = (W - tw) // 2
    rrect(d, (x, y, x + tw, y + 84), 26, fill=(255, 255, 255, 255))
    d.ellipse((x + 26, y + 20, x + 70, y + 64), fill=(*PLUM, 255))
    d.text((x + 38, y + 24), "↗", font=SANS(30, "Bold"), fill=PORC)
    d.text((x + 96, y + 24), text, font=f, fill=INK)
    return y + 84

def sticker_addyours(canvas, d, y, text, w=760):
    if not STICKERS: return y
    x = (W - w) // 2
    rrect(d, (x, y, x + w, y + 150), 34, fill=(255, 255, 255, 255))
    d.text((x + 44, y + 30), "ADD YOURS", font=MONO(22), fill=PLUM)
    d.text((x + 44, y + 74), text, font=SANS(32, "SemiBold"), fill=INK)
    return y + 150

# ---------------- grounds ----------------
def base_photo(slug, i, focus=(0.5, 0.5), top_a=30, bot_a=190):
    c = cover(Image.open(src(slug, i)), W, H, focus).convert("RGBA")
    return wash(c, top_a, bot_a)

def base_porcelain():
    c = Image.new("RGBA", (W, H), (*PORC, 255))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((-500, -600, 800, 700), fill=(*BLUSH, 120))
    gd.ellipse((500, 1300, 1600, 2400), fill=(243, 226, 225, 130))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(160))); return c

def base_ink():
    c = Image.new("RGBA", (W, H), (*INK, 255))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((-300, -500, 900, 500), fill=(246, 196, 214, 46))
    gd.ellipse((500, -300, 1500, 500), fill=(197, 214, 233, 40))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(180))); return c

def lotus_on(c, h=900, right=0, bottom=120, alpha=255):
    lo = Image.open(f"{REPO}/assets/brand/hero-lotus.png").convert("RGBA")
    lo = lo.resize((round(h * lo.width / lo.height), h), Image.LANCZOS)
    if alpha < 255: lo.putalpha(lo.split()[3].point(lambda v: v * alpha // 255))
    c.alpha_composite(lo, (W - lo.width - right, H - lo.height - bottom))

def headline(d, y, lines, size=112, fill=INK, ital_last=False, align="left", x=88):
    f = DISPLAY(size)
    for k, ln in enumerate(lines):
        last = ital_last and k == len(lines) - 1
        ff = ITAL(int(size * 1.02)) if last else f
        col = (PLUMD if fill == INK else BLUSH) if last else fill
        w = d.textlength(ln, font=ff)
        d.text((x if align == "left" else (W - w) / 2, y), ln, font=ff, fill=col); y += size
    return y

def eyebrow(d, y, text, fill=PLUM, x=88, align="left"):
    f = MONO(24); w = d.textlength(text, font=f)
    d.text((x if align == "left" else (W - w) / 2, y), text, font=f, fill=fill); return y + 44

def para(d, y, text, size=34, fill=INK, maxw=820, x=88, font=None, lh=1.4, align="left"):
    f = font or SANS(size)
    for ln in wrap(text, f, maxw):
        w = d.textlength(ln, font=f)
        d.text((x if align == "left" else (W - w) / 2, y), ln, font=f, fill=fill); y += size * lh
    return y

def save(c, name):
    im = c.convert("RGB")
    im.save(f"{OUT}/{name}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    im.resize((540, 960), Image.LANCZOS).save(f"{OUT}/{name}-web.jpg", "JPEG", quality=80, optimize=True, progressive=True)

FRAMES = []
def frame(id, day, bucket, title, sticker, copy, note, build):
    FRAMES.append(dict(id=id, day=day, bucket=bucket, title=title, sticker=sticker, copy=copy, note=note))
    save(build(), id); print("rendered", id)

# ---------- DAY 1 · TEASE ----------
def d1_1():
    c = base_porcelain(); d = ImageDraw.Draw(c)
    lotus_on(c, h=1150, right=-40, bottom=-60, alpha=150); brand_bar(d, c, True)
    eyebrow(d, 560, "THIS WEEK")
    y = headline(d, 620, ["Something", "is", "blooming."], 132, ital_last=True)
    para(d, y + 40, "Twenty years in. A new home for everything we make. Keep an eye on this space.", 34, fill=INKP, maxw=700)
    sticker_countdown(c, d, 1420, "New home opens in"); return c
frame("d1-1", 1, "Tease", "Something is blooming", "Countdown · add in Instagram, set to launch morning",
      "Something is blooming.",
      "Countdown sticker set to launch morning. Viewers can tap to get reminded. The lotus from the site's hero, faded, on the porcelain ground. First time the new palette shows.", d1_1)

def d1_2():
    c = base_photo("mehendi_taj", 13, (0.5, 0.5), 80, 200).filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(c)
    brand_bar(d, c, False)
    eyebrow(d, 500, "GUESS", fill=BLUSH, align="center")
    headline(d, 560, ["What are we", "up to?"], 112, fill=PORC, align="center")
    sticker_poll(c, d, 1040, "Take a guess", ["A new website", "A new city", "A new service", "All of the above"]); return c
frame("d1-2", 1, "Tease", "What are we up to?", "Poll · add in Instagram: A new website / A new city / A new service / All of the above",
      "What are we up to?",
      "Their own mehendi decor, blurred so it stays a tease. Poll results give a reason to post again tomorrow. Correct answer is revealed on Day 2.", d1_2)

def d1_3():
    c = base_photo("recepbrunch", 44, (0.5, 0.5), 20, 170); d = ImageDraw.Draw(c)
    brand_bar(d, c, False)
    eyebrow(d, 1180, "HONEST QUESTION", fill=BLUSH)
    headline(d, 1230, ["How excited", "should you be?"], 96, fill=PORC)
    sticker_slider(c, d, 1520, "Slide it"); return c
frame("d1-3", 1, "Tease", "How excited should you be?", "Emoji slider · add in Instagram",
      "How excited should you be?",
      "A lit floral arch after dark, no people. Slider is the lowest-effort tap on Instagram, which is what a tease needs.", d1_3)

# ---------- DAY 2 · REVEAL ----------
def d2_1():
    c = base_porcelain(); d = ImageDraw.Draw(c)
    mark = Image.open(f"{REPO}/assets/brand/soul-mark.png").convert("RGBA")
    mark = mark.resize((420, round(420 * mark.height / mark.width)), Image.LANCZOS)
    c.alpha_composite(mark, ((W - mark.width) // 2, 560)); y = 560 + mark.height + 60
    f = F("Marcellus", 150); d.text(((W - d.textlength("SOUL", font=f)) / 2, y), "SOUL", font=f, fill=INKP)
    d.text(((W - d.textlength("events", font=MONO(40))) / 2, y + 170), "events", font=MONO(40), fill=PLUMD)
    headline(d, y + 330, ["Same soul.", "New home."], 96, ital_last=True, align="center"); return c
frame("d2-1", 2, "Reveal", "Same soul. New home.", "None (reaction bar)",
      "Same soul. New home.",
      "Logo reveal, no sticker. This is the frame people screenshot, so keep it clean.", d2_1)

def d2_2():
    c = base_photo("recep_leela", 10, (0.5, 0.5), 60, 200); d = ImageDraw.Draw(c)
    brand_bar(d, c, False)
    eyebrow(d, 560, "POP QUIZ", fill=BLUSH, align="center")
    headline(d, 610, ["Which of these", "have we done?"], 100, fill=PORC, align="center")
    sticker_quiz(c, d, 960, "Pick one", ["A wedding on a beach in Goa", "A brunch beside a pool", "A Holi party for a whole office", "All of the above"], 3); return c
frame("d2-2", 2, "Reveal", "Which of these have we done?", "Quiz · add in Instagram: A. A wedding on a beach in Goa · B. A brunch beside a pool · C. A Holi party for a whole office · D. All of the above (correct: D)",
      "Pop quiz: which of these have we done?",
      "Every option is a real event from the decks. The answer is all of them, which is the point.", d2_2)

def d2_3():
    c = base_porcelain(); d = ImageDraw.Draw(c)
    lotus_on(c, h=1000, right=-30, bottom=80, alpha=210); brand_bar(d, c, True)
    eyebrow(d, 520, "SOULEVENTSINDIA.COM")
    headline(d, 640, ["Occasions", "that are personal", "& bespoke."], 108, ital_last=True)
    sticker_countdown(c, d, 1500, "Doors open"); return c
frame("d2-3", 2, "Reveal", "Tomorrow, 10:00", "Countdown · add in Instagram, set to launch morning",
      "Occasions that are personal & bespoke.",
      "The site's own hero, rebuilt as a story. Anyone who tapped the Day 1 countdown gets a nudge from this one too.", d2_3)

# ---------- DAY 3 · LAUNCH ----------
def d3_1():
    c = base_ink(); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    ph_w, ph_h = 640, 1300
    shot = Image.open(f"{REPO}/marketing/stories/phone-hero.png").convert("RGB")
    shot = shot.resize((ph_w - 24, round((ph_w - 24) * shot.height / shot.width)), Image.LANCZOS)
    screen = Image.new("RGB", (ph_w - 24, ph_h - 24), PORC); screen.paste(shot.crop((0, 0, shot.width, min(shot.height, ph_h - 24))), (0, 0))
    ph = Image.new("RGBA", (ph_w, ph_h), (0, 0, 0, 0)); pd = ImageDraw.Draw(ph)
    pd.rounded_rectangle((0, 0, ph_w, ph_h), radius=64, fill=(*INKP, 255), outline=(*PLUMS, 255), width=3)
    mask = Image.new("L", screen.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *screen.size), radius=52, fill=255)
    ph.paste(screen, (12, 12), mask); c.alpha_composite(ph, ((W - ph_w) // 2, 240))
    headline(d, 1600, ["We're live."], 120, fill=PORC, align="center"); return c
frame("d3-1", 3, "Launch", "We're live", "Link · add in Instagram: souleventsindia.com",
      "We're live.",
      "Launch frame. A real screenshot of the live site at phone width, in a phone. Add the link sticker below the headline.", d3_1)


def d3_3():
    c = base_photo("brunch_marriott", 1, (0.5, 0.5), 60, 210); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 380, "NINE KINDS OF OCCASION", fill=BLUSH); y = 430
    for cat in ["Weddings", "Receptions", "Haldi", "Mehendi", "Brunches", "Milestone Birthdays", "Children's Birthdays", "Anniversaries", "Table Decor"]:
        d.text((88, y), cat, font=DISPLAY(58), fill=PORC); y += 66
    return c
frame("d3-3", 3, "Launch", "Nine kinds of occasion", "Link · add in Instagram",
      "Nine kinds of occasion.",
      "The gallery's nine categories as they appear on the site, as a plain listing.", d3_3)

def d3_4():
    c = base_photo("recepbrunch", 17, (0.5, 0.5), 60, 200); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1080, "YOUR TURN", fill=BLUSH)
    headline(d, 1130, ["Show us your", "favourite", "Soul moment."], 92, fill=PORC, ital_last=True)
    sticker_addyours(c, d, 1520, "Your favourite Soul moment"); return c
frame("d3-4", 3, "Launch", "Show us your favourite Soul moment", "Add Yours · add in Instagram: “Your favourite Soul moment”",
      "Show us your favourite Soul moment.",
      "Add Yours chains follower photos onto the launch. Any moment, not a specific occasion. Reshare the good ones through the week.", d3_4)

# ---------- DAY 4 · THE WORK ----------
def d4_1():
    c = Image.new("RGBA", (W, H), (*PORC, 255))
    c.paste(cover(Image.open(src("soulevents", 19)), W, 800), (0, 0))
    c.paste(cover(Image.open(src("recep_namrata", 4)), W, 800), (0, H - 800))
    d = ImageDraw.Draw(c); d.rectangle((0, 800, W, H - 800), fill=PORC)
    d.text((88, 60), "A", font=DISPLAY(96), fill=PORC); d.text((88, H - 800 + 60), "B", font=DISPLAY(96), fill=PORC)
    eyebrow(d, 846, "THIS OR THAT", align="center")
    headline(d, 892, ["Under a roof,", "or under the trees?"], 64, align="center")
    sticker_poll(c, d, 1290, "Pick a side", ["A  Under a roof", "B  Under the trees"], w=640); return c
frame("d4-1", 4, "The Work", "Under a roof or under the trees?", "Poll · add in Instagram: A / B",
      "This or that: under a roof, or under the trees?",
      "Split frame, two of their own mandaps: the red timber-pavilion one and the Namrata & Ashwin garden canopy. This-or-that is Instagram's most answered format.", d4_1)

def d4_2():
    c = base_photo("mehendi_taj", 11, (0.5, 0.55), 30, 180); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1160, "THE TAJ · MEHENDI", fill=BLUSH)
    headline(d, 1210, ["Swing-", "worthy?"], 110, fill=PORC)
    sticker_slider(c, d, 1560, "How much"); return c
frame("d4-2", 4, "The Work", "Swing-worthy?", "Emoji slider · add in Instagram",
      "The Taj, Mehendi. Swing-worthy?",
      "The jhoola from the Taj mehendi. One word question, one slider. Location in the eyebrow is a quiet flex.", d4_2)

def d4_3():
    c = base_photo("brunch_marriott", 8, (0.5, 0.5), 40, 190); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1100, "THE MARRIOTT · BRUNCH", fill=BLUSH)
    headline(d, 1150, ["Brunch by the pool,", "or on the lawn?"], 76, fill=PORC)
    sticker_poll(c, d, 1440, "Where would you sit?", ["By the pool", "On the lawn"]); return c
frame("d4-3", 4, "The Work", "By the pool or on the lawn?", "Poll · add in Instagram: By the pool / On the lawn",
      "The Marriott, brunch. By the pool, or on the lawn?",
      "The cabana table beside the pool. Second poll of the day, different photo, same rhythm.", d4_3)

def d4_4():
    c = base_photo("brunch_marriott", 9, (0.5, 0.5), 20, 200); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1140, "TABLE DECOR", fill=BLUSH)
    headline(d, 1190, ["What's on your", "dream table?"], 84, fill=PORC)
    sticker_question(c, d, 1500, "Tell us"); return c
frame("d4-4", 4, "The Work", "What's on your dream table?", "Question box · add in Instagram",
      "Table decor. What's on your dream table?",
      "First open question of the week. Replies are content for Day 6 and leads for Day 7. Answer a few publicly.", d4_4)

# ---------- DAY 5 · THE TWO OF US ----------
def d5_1():
    c = base_ink(); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 420, "03 · THE TWO OF US", fill=BLUSH)
    y = para(d, 470, "We found it easier to introduce each other than ourselves.", 60, fill=PORC, maxw=880, font=ITAL(60), lh=1.15)
    y = para(d, y + 80, "“Chelna is a magician. She easily understands what people want and is an expert in transforming their dreams into reality. In short, she makes things happen.”", 44, fill=PORC, maxw=860, font=DISPLAY(44), lh=1.36)
    d.text((88, y + 40), "RAMESH, ON CHELNA", font=MONO(24), fill=BLUSH)
    d.text((88, y + 90), "Chelna Lekhi · Designer & Planner · “The Magician”", font=SANS(28), fill=PLUMS); return c
frame("d5-1", 5, "The Two of Us", "Chelna, by Ramesh", "None (reaction bar)",
      "We found it easier to introduce each other than ourselves. “Chelna is a magician...” Ramesh, on Chelna.",
      "The founders section, verbatim. Ink ground so it reads as a page from the site. If Chelna sends a portrait it goes behind this text.", d5_1)

def d5_2():
    c = base_ink(); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 420, "03 · THE TWO OF US", fill=BLUSH)
    y = para(d, 470, "“Always fun, often witty, and never dull. Even after anchoring over a thousand events, he still manages to surprise his audience.”", 46, fill=PORC, maxw=860, font=DISPLAY(46), lh=1.36)
    d.text((88, y + 40), "CHELNA, ON RAMESH", font=MONO(24), fill=BLUSH)
    d.text((88, y + 90), "Ramesh Sadhwani · Anchor · 1000+ events · “The Event Energizer”", font=SANS(26), fill=PLUMS); return c
frame("d5-2", 5, "The Two of Us", "Ramesh, by Chelna", "None (reaction bar)",
      "“Always fun, often witty, and never dull...” Chelna, on Ramesh.",
      "Pair to the previous frame. Post them back to back so they read as one spread.", d5_2)

def d5_3():
    c = base_photo("soulevents", 41, (0.45, 0.4), 40, 200); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1060, "OPEN FLOOR", fill=BLUSH)
    headline(d, 1110, ["Ask Chelna", "& Ramesh", "anything."], 96, fill=PORC, ital_last=True)
    sticker_question(c, d, 1530, "Go on"); return c
frame("d5-3", 5, "The Two of Us", "Ask Chelna & Ramesh anything", "Question box · add in Instagram",
      "Open floor. Ask Chelna & Ramesh anything.",
      "The Q&A. Ramesh with a mic is the right photo for it. Answers get posted as frames on Day 6. Confirm the photo is Ramesh before using it; swap for the stage frame if not.", d5_3)

def d5_4():
    c = base_photo("holi", 5, (0.5, 0.5), 40, 210); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 560, "BY THE NUMBERS", fill=BLUSH, align="center")
    headline(d, 610, ["How many events", "have we done?"], 84, fill=PORC, align="center")
    sticker_quiz(c, d, 920, "Take a guess", ["150", "300", "450+", "1000"], 2); return c
frame("d5-4", 5, "The Two of Us", "How many events have we done?", "Quiz · add in Instagram: 150 / 300 / 450+ / 1000 (correct: 450+)",
      "By the numbers. How many events have we done?",
      "Turns the stats section into a quiz. Photo is from the Holi party deck; check it reads well at story size or swap for a brunch wide.", d5_4)

# ---------- DAY 6 · VOICES ----------
def d6_1():
    c = base_porcelain(); d = ImageDraw.Draw(c); brand_bar(d, c, True)
    eyebrow(d, 420, "07 · VOICES")
    y = para(d, 470, "“You made a dead location so lively and swanky that even the owner was awestruck with the ambience and decor. Everybody was talking about the party which lasted till 6 in the morning.”", 50, fill=INK, maxw=880, font=DISPLAY(50), lh=1.34)
    d.text((88, y + 40), "ANAND JAIN", font=MONO(24), fill=PLUM)
    lotus_on(c, h=520, right=-20, bottom=60, alpha=120); return c
frame("d6-1", 6, "Voices", "Till 6 in the morning", "None (reaction bar)",
      "“...the party which lasted till 6 in the morning.” Anand Jain",
      "Verbatim from the site's testimonials. Porcelain ground, lotus faded in the corner. No sticker; let the quote sit.", d6_1)

def d6_2():
    c = base_porcelain(); d = ImageDraw.Draw(c); brand_bar(d, c, True)
    eyebrow(d, 420, "07 · VOICES")
    y = para(d, 470, "“The decor, the musicians, performers, flowers, the minute detailing, the sangeet, the doli, and the vidai were all picture perfect. You have done everything as though it was a wedding from your own family.”", 46, fill=INK, maxw=880, font=DISPLAY(46), lh=1.34)
    d.text((88, y + 40), "KALPANA RAO, DUBAI", font=MONO(24), fill=PLUM)
    lotus_on(c, h=520, right=-20, bottom=60, alpha=120); return c
frame("d6-2", 6, "Voices", "As though it was our own family", "None (reaction bar)",
      "“...as though it was a wedding from your own family.” Kalpana Rao, Dubai",
      "Second voice. Same frame, so the two read as a set. Both are on the site word for word.", d6_2)

def d6_3():
    c = base_ink(); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 420, "YOU ASKED", fill=BLUSH)
    headline(d, 470, ["You asked,", "we answered."], 100, fill=PORC, ital_last=True)
    rrect(d, (88, 760, W - 88, 900), 30, fill=(255, 255, 255, 255))
    d.text((128, 800), "How far ahead should we book you?", font=SANS(32, "SemiBold"), fill=INK)
    para(d, 960, "For a wedding, six to nine months. For a birthday or a brunch, six weeks is plenty. For a Tuesday, call us Monday.", 40, fill=PORC, maxw=860, font=DISPLAY(40), lh=1.36)
    d.text((88, 1400), "TEMPLATE · ONE FRAME PER ANSWER", font=MONO(22), fill=PLUMS); return c
frame("d6-3", 6, "Voices", "You asked, we answered", "Question response · reshare a reply from the D5-3 box",
      "You asked, we answered. (One frame per answer, reusing the question sticker.)",
      "Template for the Day 5 Q&A replies. Instagram lets you reshare a question response with your answer over it; this is the layout to answer in. The example answer here is a placeholder, write the real ones.", d6_3)

def d6_4():
    c = base_photo("recepbrunch", 34, (0.5, 0.5), 40, 200); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1140, "QUICK ONE", fill=BLUSH)
    headline(d, 1190, ["Have we planned", "one of yours?"], 80, fill=PORC)
    sticker_poll(c, d, 1480, "Be honest", ["Yes, and it was a night", "Not yet"]); return c
frame("d6-4", 6, "Voices", "Have we planned one of yours?", "Poll · add in Instagram: Yes, and it was a night / Not yet",
      "Quick one. Have we planned one of yours?",
      "Sorts the audience into past clients and prospects. The “Not yet” voters are who Day 7 talks to.", d6_4)

# ---------- DAY 7 · INVITE ----------
def d7_1():
    c = base_photo("recep_namrata", 10, (0.5, 0.5), 40, 210); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1040, "PLANNING SOMETHING?", fill=BLUSH)
    headline(d, 1090, ["Tell us the date,", "the city, and", "the feeling."], 80, fill=PORC, ital_last=True)
    sticker_question(c, d, 1500, "Start here"); return c
frame("d7-1", 7, "Invite", "Tell us the date, the city, and the feeling", "Question box · add in Instagram",
      "Planning something? Tell us the date, the city, and the feeling.",
      "The contact section's own line. Question box replies land in DMs, which is where a lead should land.", d7_1)

def d7_2():
    c = base_porcelain(); d = ImageDraw.Draw(c); brand_bar(d, c, True)
    eyebrow(d, 420, "02 · BY THE NUMBERS"); y = 500
    for n, l in [("20", "Years since formation"), ("450+", "Events executed"), ("47", "Years of collective experience"), ("450+", "Happy clients")]:
        d.text((88, y), n, font=DISPLAY(150), fill=INK); d.text((88, y + 160), l, font=DISPLAY(34), fill=INKP)
        y += 270; d.line((88, y - 40, W - 88, y - 40), fill=HAIR, width=2)
    return c
frame("d7-2", 7, "Invite", "By the numbers", "None (reaction bar)",
      "20 years since formation. 450+ events. 47 years of collective experience. 450+ happy clients.",
      "The stats section as a story. Instagram lets you animate each number in, so post this as one frame and let the app do the reveal.", d7_2)

def d7_3():
    c = base_ink(); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 640, "09 · CONTACT", fill=BLUSH); f = DISPLAY(120)
    d.text((88, 700), "Just", font=f, fill=PORC); d.text((88, 830), "let us", font=f, fill=BLUE); d.text((88, 960), "step in.", font=f, fill=BLUE)
    para(d, 1140, "A phone call is usually the fastest way to begin. WhatsApp works too.", 32, fill=PORC, maxw=760, font=SANS(32), lh=1.4)
    sticker_link(c, d, 1440, "souleventsindia.com"); sticker_link(c, d, 1560, "WhatsApp +91 93422 83539"); return c
frame("d7-3", 7, "Invite", "Just let us step in", "Link ×2 · add in Instagram: souleventsindia.com and wa.me",
      "Just let us step in. A phone call is usually the fastest way to begin. WhatsApp works too.",
      "The contact headline in the site's blue on ink. Two link stickers: site, and wa.me. Confirm the number is theirs before this goes up.", d7_3)

def d7_4():
    c = base_photo("soulevents", 36, (0.5, 0.5), 40, 200); d = ImageDraw.Draw(c); brand_bar(d, c, False)
    eyebrow(d, 1120, "IN CASE YOU MISSED IT", fill=BLUSH)
    headline(d, 1170, ["We have a", "new home."], 104, fill=PORC, ital_last=True)
    sticker_link(c, d, 1520); return c
frame("d7-4", 7, "Invite", "In case you missed it", "Link · add in Instagram: souleventsindia.com",
      "In case you missed it: we have a new home.",
      "Closer. Pin this and the Day 3 launch frame to a “New home” highlight so the link outlives the week.", d7_4)

json.dump(FRAMES, open(f"{OUT}/frames.json", "w"), indent=1, ensure_ascii=False)
print(len(FRAMES), "frames")
