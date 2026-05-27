#!/usr/bin/env python3
"""
v7: Brand icons only (no illustrations) — small, placed next to brand text.
Strategy: find brand-name text shapes on each slide, place 2.5% icon to left.
Slides 6&9: full-page SVG renders (system fonts) + brand icons overlaid.
All illustrations removed.
"""
import os, shutil, zipfile, re
from pptx import Presentation
from pptx.util import Emu
from cairosvg import svg2png

V1 = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v7.pptx'
TMP = DST.replace('.pptx', '_tmp.pptx')
BP = 'temp/brand_pngs'
SW, SH = 12192000, 6858000
ICON_SZ = int(SW * 0.025)  # 2.5% of slide width = ~305K EMU

def add_pic(slide, name, x, y, w, h):
    p = f'{BP}/{name}'
    if os.path.exists(p):
        try: slide.shapes.add_picture(p, x, y, w, h); return True
        except: pass
    return False

# ── Step 1: Fix theme font ──
print("Fixing theme font...")
shutil.copy2(V1, TMP)
with zipfile.ZipFile(V1) as zin, zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = zin.read(item.filename)
        if item.filename == 'ppt/theme/theme1.xml':
            d = d.decode().replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>').encode()
        zout.writestr(item, d)

prs = Presentation(TMP)

# ── Step 2: Brand icon mapping: (slide_num, brand_name, x%, y%, w%, h%) ──
# Positions derived from text shape coordinates in v1 slides
# Icons placed to the LEFT of each brand name text (at same y-center)
# Size: 2.5% width, 2.5% height (roughly square)

brands_map = [
    # Slide 8: 评测排行 — left column models
    (8, 'openai', 14.5, 21.0, 2.5, 2.5),
    (8, 'anthropic', 14.5, 27.0, 2.5, 2.5),
    (8, 'google', 14.5, 33.0, 2.5, 2.5),
    (8, 'deepseek', 14.5, 39.0, 2.5, 2.5),
    (8, 'meta', 14.5, 45.0, 2.5, 2.5),
    (8, 'xai', 14.5, 51.0, 2.5, 2.5),
    (8, 'alibaba', 14.5, 57.0, 2.5, 2.5),
    (8, 'cohere_badge', 14.5, 63.0, 2.5, 2.5),
    (8, 'ibm', 14.5, 69.0, 2.5, 2.5),
    # Slide 8: right column models
    (8, 'mistral', 49.0, 21.0, 2.5, 2.5),
    (8, 'alibaba', 49.0, 27.0, 2.5, 2.5),
    (8, 'baidu', 49.0, 33.0, 2.5, 2.5),
    (8, 'bytedance', 49.0, 39.0, 2.5, 2.5),
    (8, 'tencent', 49.0, 45.0, 2.5, 2.5),
    (8, 'kimi_badge', 49.0, 51.0, 2.5, 2.5),
    (8, 'yi_badge', 49.0, 57.0, 2.5, 2.5),

    # Slide 10: 中国模型全景
    (10, 'deepseek', 5.0, 38.0, 2.5, 2.5),
    (10, 'alibaba', 5.0, 50.0, 2.5, 2.5),
    (10, 'baidu', 5.0, 62.0, 2.5, 2.5),
    (10, 'bytedance', 50.0, 38.0, 2.5, 2.5),
    (10, 'tencent', 50.0, 50.0, 2.5, 2.5),
    (10, 'kimi_badge', 50.0, 62.0, 2.5, 2.5),

    # Slide 11: 全球AI工作台
    (11, 'github', 2.5, 42.0, 2.5, 2.5),
    (11, 'anthropic', 25.5, 42.0, 2.5, 2.5),
    (11, 'cursor', 48.5, 42.0, 2.5, 2.5),
    (11, 'dify', 71.5, 42.0, 2.5, 2.5),
    (11, 'coze', 87.5, 42.0, 2.5, 2.5),

    # Slide 12: 中国AI工作台
    (12, 'dify', 5.5, 42.0, 2.5, 2.5),
    (12, 'coze', 33.5, 42.0, 2.5, 2.5),
    (12, 'autogpt_badge', 59.5, 42.0, 2.5, 2.5),
    (12, 'lovable_badge', 19.5, 68.0, 2.5, 2.5),
    (12, 'bolt_badge', 45.5, 68.0, 2.5, 2.5),
    (12, 'v0_badge', 71.5, 68.0, 2.5, 2.5),

    # Slide 13: OpenClaw架构 — small GitHub icon in corner
    (13, 'github', 82.0, 3.0, 2.0, 2.0),

    # Slide 9: 第一梯队 (SVG background, icons overlay on matching areas)
    (9, 'openai', 7.0, 22.0, 3.0, 3.0),
    (9, 'anthropic', 7.0, 42.0, 3.0, 3.0),
    (9, 'google', 7.0, 62.0, 3.0, 3.0),
    (9, 'deepseek', 72.0, 22.0, 3.0, 3.0),
]

# ── Step 3: Add brand icons ──
print("Adding brand icons...")
for sn, name, xp, yp, wp, hp in brands_map:
    slide = prs.slides[sn-1]
    x = int(SW * xp / 100)
    y = int(SH * yp / 100)
    w = int(SW * wp / 100)
    h = int(SH * hp / 100)
    ok = add_pic(slide, f'{name}.png', x, y, w, h)
    if not ok:
        # Try badge variant
        ok = add_pic(slide, f'{name}.png', x, y, w, h)
        if not ok:
            print(f'  P{sn} {name}: MISSING')

# ── Step 4: Fill empty slides 6, 9 with SVG content (fixed fonts) ──
print("Filling empty slides...")
with zipfile.ZipFile(SVG_SRC) as z:
    for sn in [6, 9]:
        svg = z.read(f'ppt/media/image{sn}.svg').decode()
        # Fix font to system-available fonts
        svg = svg.replace(
            "font-family=\"'Noto Sans SC','Microsoft YaHei',sans-serif\"",
            "font-family=\"'Noto Sans CJK SC','WenQuanYi Micro Hei',sans-serif\""
        )
        # Fix duplicate attributes
        svg = re.sub(r'(\w+)="([^"]*)"(\s+\1="[^"]*")+', lambda m: f'{m.group(1)}="{m.group(2)}"', svg)
        png = svg2png(bytestring=svg.encode(), scale=2, output_width=2560, output_height=1440)
        pp = f'/tmp/s{sn}.png'
        open(pp, 'wb').write(png)
        slide = prs.slides[sn-1]
        pic = slide.shapes.add_picture(pp, 0, 0, SW, SH)
        # Send to back (icons overlay on top)
        spTree = slide.shapes._spTree
        spTree.remove(pic._element)
        spTree.insert(2, pic._element)
        print(f'  P{sn}: full-page ({len(png)}B)')

# ── Step 5: Save ──
print("\nSaving...")
prs.save(DST)
os.remove(TMP)

# Verify
p = Presentation(DST)
pics = sum(1 for s in p.slides for sh in s.shapes if sh.shape_type == 13)
empty = sum(1 for s in p.slides if len(list(s.shapes)) <= 1)
font_runs = set()
for s in p.slides:
    for sh in s.shapes:
        if hasattr(sh, 'text_frame') and sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.name: font_runs.add(r.font.name)
print(f"Slides: {len(p.slides)}, Pics: {pics}, Near-empty: {empty}")
print(f"Fonts: {font_runs}")
print(f"Size: {os.path.getsize(DST):,}B")
print(f"Done: {DST}")
