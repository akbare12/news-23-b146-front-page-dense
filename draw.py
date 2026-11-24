#!/usr/bin/env python3
"""news-23 b146 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)
INK = (20, 20, 20)
RED = (158, 27, 27)
GOLD = (176, 141, 26)
NAVY = (16, 42, 80)
GREEN = (18, 92, 52)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, max_w, min_size=9):
    """Shrink font until text fits max_w; returns (font, text)."""
    size = fnt.size
    f = fnt
    while draw.textlength(text, font=f) > max_w and size > min_size:
        size -= 1
        f = ImageFont.truetype(f.path, size)
    return f


def chip(draw, x, y, label):
    """Draw REPORTED (navy) / CLAIM (red) chip; returns width used."""
    f = font(F_SANSB, 10)
    tw = draw.textlength(label, font=f)
    w = int(tw) + 10
    h = 15
    color = NAVY if label == "REPORTED" else RED
    draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=color)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 8
CW = W - 2 * MX  # 1008

# ---------- masthead ----------
d.text((MX, 2), "THE WORLD TODAY", font=font(F_SERIF, 54), fill=INK)
d.text((W - MX - d.textlength("MONDAY 23 NOVEMBER 2026", font=font(F_SANSB, 17)),
        24), "MONDAY 23 NOVEMBER 2026", font=font(F_SANSB, 17), fill=GOLD)
d.rectangle([MX, 66, W - MX, 69], fill=GOLD)

# ---------- kicker ----------
d.rectangle([MX, 72, W - MX, 94], fill=RED)
kick = "AI rout hits Asia   \u00b7   UN chief urges AI rules   \u00b7   US lead over China at record low   \u00b7   Anthropic IPO $107.3B"
d.text((MX + 6, 77), kick, font=font(F_SANSB, 14), fill=(255, 255, 255))

# ---------- number strip (2 rows x 5) ----------
numbers = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
cell_w = CW // 5
for row in range(2):
    y0 = 98 + row * 44
    for col in range(5):
        val, lab = numbers[row * 5 + col]
        x0 = MX + col * cell_w
        f = fit_text(d, val, font(F_SANSB, 27), cell_w - 10, 18)
        d.text((x0 + 4, y0), val, font=f, fill=INK)
        lf = fit_text(d, lab, font(F_SANS, 10), cell_w - 10, 8)
        d.text((x0 + 4, y0 + 29), lab, font=lf, fill=(90, 90, 90))

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", (16, 42, 80)), ("AMERICAS 8", (158, 27, 27)),
           ("MIDDLE EAST 6", (18, 92, 52)), ("EUROPE 5", (120, 72, 20)),
           ("AFRICA 3", (90, 60, 120)), ("WORLD 2", (90, 90, 90))]
seg_w = CW // 6
for i, (label, col) in enumerate(regions):
    x0 = MX + i * seg_w
    d.rectangle([x0, 188, x0 + seg_w - 2, 208], fill=col)
    f = fit_text(d, label, font(F_SANSB, 12), seg_w - 10, 9)
    d.text((x0 + 6, 192), label, font=f, fill=(255, 255, 255))

# ---------- UTC strip ----------
d.text((MX, 212), "THE DAY IN UTC", font=font(F_SANSB, 11), fill=INK)
utc = "~00:00 Kospi dives   ~05:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles"
d.text((MX + 130, 212), utc, font=font(F_SANS, 11), fill=(80, 80, 80))
d.text((W - MX - d.textlength("~ APPROX", font=font(F_SANS, 10)), 212),
       "~ APPROX", font=font(F_SANS, 10), fill=(120, 120, 120))

# ---------- heroes ----------
hero_w = 330
hero_gap = 9
hero_x = [MX + i * (hero_w + hero_gap) for i in range(3)]
scene_y0, scene_y1 = 230, 322
cap_y0, cap_y1 = 322, 340
head_y = 346
body_y = 388
src_y = 424

heroes = [
    dict(kind="kospi",
         caption="KOSPI 4,708.54  \u00b7  -161 PTS  \u00b7  SAMSUNG -3.1%  \u00b7  HYNIX -2.5%",
         headline="AI ROUT HITS ASIA",
         body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         source="KOREA EXCHANGE", chip="REPORTED"),
    dict(kind="guterres",
         caption="BRIDGETOWN SUMMIT, BARBADOS",
         headline="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         source="UNITED NATIONS", chip="REPORTED"),
    dict(kind="power",
         caption="ASIA POWER INDEX 2026  \u00b7  LOWY INSTITUTE",
         headline="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         source="LOWY INSTITUTE", chip="REPORTED"),
]

for i, h in enumerate(heroes):
    x0 = hero_x[i]
    x1 = x0 + hero_w
    # scene
    if h["kind"] == "kospi":
        d.rectangle([x0, scene_y0, x1, scene_y1], fill=(12, 28, 58))
        # skyline: buildings with lit windows, max height 64 so -3.3% stays clear
        import random
        rnd = random.Random(146 + i)
        bx = x0 + 8
        while bx < x1 - 26:
            bw = rnd.randint(18, 30)
            bh = rnd.randint(30, 64)
            by = scene_y1 - bh
            d.rectangle([bx, by, bx + bw, scene_y1], fill=(30, 55, 95))
            for wy in range(by + 6, scene_y1 - 6, 12):
                for wx in range(bx + 4, bx + bw - 4, 9):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 90))
            bx += bw + 4
        # falling chart line, starting right of the big number
        pts = [(x0 + 150, 246), (x0 + 185, 258), (x0 + 215, 252),
               (x0 + 250, 272), (x0 + 285, 286), (x0 + 318, 306)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.text((x0 + 10, 236), "-3.3%", font=font(F_SANSB, 40), fill=(255, 255, 255))
    elif h["kind"] == "guterres":
        d.rectangle([x0, scene_y0, x1, scene_y1], fill=(14, 74, 42))
        # globe, masked circle
        cx, cy, r = x0 + hero_w - 78, 276, 44
        mask = Image.new("L", (2 * r, 2 * r), 0)
        md = ImageDraw.Draw(mask)
        md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
        globe = Image.new("RGB", (2 * r, 2 * r), (190, 225, 190))
        gd = ImageDraw.Draw(globe)
        gd.ellipse([6, 6, 2 * r - 7, 2 * r - 7], outline=(60, 140, 90), width=2)
        gd.line([r, 6, r, 2 * r - 6], fill=(60, 140, 90), width=2)
        gd.line([6, r, 2 * r - 6, r], fill=(60, 140, 90), width=2)
        gd.arc([14, 14, 2 * r - 14, 2 * r - 14], 200, 340, fill=(60, 140, 90), width=2)
        img.paste(globe, (cx - r, cy - r), mask)
        d.text((x0 + 10, 240), "150", font=font(F_SANSB, 40), fill=(255, 214, 90))
        d.text((x0 + 10, 282), "DELEGATES BACK A", font=font(F_SANSB, 16), fill=(255, 214, 90))
        d.text((x0 + 10, 300), "RISK FRAMEWORK", font=font(F_SANSB, 16), fill=(255, 214, 90))
    else:  # power bars
        d.rectangle([x0, scene_y0, x1, scene_y1], fill=(245, 242, 232))
        d.text((x0 + 10, 234), "NARROWEST SINCE 2018", font=font(F_SANSB, 13), fill=INK)
        f = font(F_SANSB, 11)
        d.text((x0 + hero_w - 14 - d.textlength("GAP 5.3", font=f), 236),
               "GAP 5.3", font=f, fill=RED)
        bars = [("78.9", "US", NAVY, 0.92), ("73.6", "CHINA", RED, 0.86),
                ("40.5", "INDIA", GOLD, 0.52)]
        by = 256
        for val, name, col, frac in bars:
            d.text((x0 + 10, by), val, font=font(F_SANSB, 15), fill=INK)
            bw = int(180 * frac)
            d.rectangle([x0 + 62, by + 2, x0 + 62 + bw, by + 16], fill=col)
            d.text((x0 + 68, by + 3), name, font=font(F_SANSB, 11), fill=(255, 255, 255))
            by += 22
    # caption strip
    d.rectangle([x0, cap_y0, x1, cap_y1], fill=(0, 0, 0))
    cf = fit_text(d, h["caption"], font(F_SANSB, 10), hero_w - 8, 8)
    d.text((x0 + 4, cap_y0 + 3), h["caption"], font=cf, fill=(255, 255, 255))
    # headline (up to 2 lines, shrink to fit)
    hf = font(F_SANSB, 21)
    lines = wrap(d, h["headline"], hf, hero_w - 4)
    while len(lines) > 2 and hf.size > 15:
        hf = ImageFont.truetype(F_SANSB, hf.size - 1)
        lines = wrap(d, h["headline"], hf, hero_w - 4)
    hy = head_y
    for ln in lines[:2]:
        d.text((x0, hy), ln, font=hf, fill=INK)
        hy += hf.size + 2
    # body (2 lines)
    bf = font(F_SANS, 12)
    blines = wrap(d, h["body"], bf, hero_w - 4)
    byy = body_y
    for ln in blines[:2]:
        d.text((x0, byy), ln, font=bf, fill=(40, 40, 40))
        byy += 15
    # source + chip row
    d.text((x0, src_y), h["source"], font=font(F_SANS, 10), fill=(100, 100, 100))
    chip(d, x1 - 72, src_y - 2, h["chip"])

# ---------- cards ----------
d.rectangle([MX, 448, W - MX, 470], fill=(0, 0, 0))
d.text((MX + 6, 453), "MORE OF THE DAY  \u2014  10 STORIES", font=font(F_SANSB, 13), fill=(255, 255, 255))
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
card_w = 196
card_gap = 7
card_h = 82
for idx, (num, cat, head, body, src, ch) in enumerate(cards):
    row, col = divmod(idx, 5)
    x0 = MX + col * (card_w + card_gap)
    y0 = 476 + row * (card_h + 6)
    # number + category
    d.text((x0, y0), num, font=font(F_SANSB, 13), fill=RED)
    d.text((x0 + 20, y0 + 2), cat, font=font(F_SANSB, 10), fill=RED)
    # headline (1 line, shrink)
    hf = fit_text(d, head, font(F_SANSB, 12), card_w - 2, 9)
    d.text((x0, y0 + 16), head, font=hf, fill=INK)
    # body
    d.text((x0, y0 + 34), body, font=font(F_SANS, 11), fill=(60, 60, 60))
    # source + chip
    d.text((x0, y0 + 52), src, font=font(F_SANS, 10), fill=(100, 100, 100))
    chip(d, x0 + card_w - 72, y0 + 50, ch)
    # divider
    d.line([x0, y0 + card_h - 4, x0 + card_w, y0 + card_h - 4], fill=(210, 205, 195), width=1)

# ---------- map + ALSO ----------
d.rectangle([MX, 652, W - MX, 674], fill=(0, 0, 0))
d.text((MX + 6, 657), "WHERE IT HAPPENED", font=font(F_SANSB, 13), fill=(255, 255, 255))
map_x0, map_y0, map_x1, map_y1 = MX, 680, 478, 868
# continent blobs (light green)
americas = [(20, 700), (60, 688), (120, 690), (160, 710), (150, 760),
            (120, 830), (90, 862), (55, 850), (30, 800), (18, 740)]
eurasia = [(190, 700), (260, 688), (360, 692), (460, 700), (472, 730),
           (450, 800), (420, 855), (330, 862), (250, 855), (200, 820), (185, 750)]
d.polygon(americas, fill=(205, 228, 190))
d.polygon(eurasia, fill=(205, 228, 190))
pins = [(420, 736, "1"), (72, 806, "2"), (392, 752, "3"), (96, 748, "4"),
        (118, 730, "5"), (300, 726, "6"), (256, 744, "7"), (240, 722, "8"),
        (286, 716, "9"), (232, 706, "10"), (322, 776, "11"), (314, 792, "12"),
        (288, 818, "13")]
for px, py, n in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    tf = font(F_SANSB, 10)
    d.text((px - d.textlength(n, font=tf) / 2, py - 7), n, font=tf, fill=(255, 255, 255))
# map legend (3 short lines, inside map width)
leg = ["Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington",
       "5 New York \u00b7 6 Kyiv \u00b7 7 Paris \u00b7 8 London \u00b7 9 Warsaw",
       "10 Manchester \u00b7 11 Beirut \u00b7 12 Gaza \u00b7 13 Khartoum"]
ly = 872 - 34
for ln in leg:
    d.text((map_x0 + 2, ly), ln, font=font(F_SANS, 10), fill=(60, 60, 60))
    ly += 12

# ALSO list (2 columns x 9)
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: day after pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: air defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over AI exam chaos",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
ax0 = 492
d.text((ax0, 680), "ALSO ON MONDAY", font=font(F_SANSB, 13), fill=INK)
col_w = 258
for i, item in enumerate(also):
    col, r = divmod(i, 9)
    x = ax0 + col * col_w
    y = 702 + r * 20
    # red [CLAIM] marker handled by drawing item then recoloring bracket part is complex;
    # keep single color but bold the claim items
    if "[CLAIM]" in item:
        base, _ = item.split(" [CLAIM]")
        d.text((x, y), base, font=font(F_SANS, 11), fill=INK)
        bx = x + d.textlength(base + " ", font=font(F_SANS, 11))
        d.text((bx, y), "[CLAIM]", font=font(F_SANSB, 11), fill=RED)
    else:
        d.text((x, y), item, font=font(F_SANS, 11), fill=INK)

# ---------- DATE CHECK ----------
d.rectangle([MX, 884, W - MX, 958], outline=RED, width=2)
d.text((MX + 8, 890), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
       font=font(F_SANSB, 12), fill=RED)
left = "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7  EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)"
llines = wrap(d, left, font(F_SANS, 11), CW - 16)
ly = 908
for ln in llines:
    d.text((MX + 8, ly), ln, font=font(F_SANS, 11), fill=INK)
    ly += 14
ny = "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff"
d.text((MX + 8, ly + 2), ny, font=font(F_SANS, 11), fill=INK)

# ---------- footer ----------
d.text((MX, 966), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=font(F_SANS, 10), fill=(90, 90, 90))
d.text((MX, 980), "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, independently unconfirmed  \u00b7  ONGOING = still developing.",
       font=font(F_SANS, 10), fill=(90, 90, 90))
d.text((MX, 994), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(F_SANS, 10), fill=(90, 90, 90))
d.rectangle([MX, 1006, W - MX, 1008], fill=GOLD)
foot = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(foot, font=font(F_SANSB, 11))) / 2, 1010),
       foot, font=font(F_SANSB, 11), fill=GOLD)

img.save("entry.png")
print("saved entry.png", img.size)
