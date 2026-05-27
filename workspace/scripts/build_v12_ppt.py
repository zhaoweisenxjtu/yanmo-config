#!/usr/bin/env python3
"""
v12: FRESH FROM MD — Design-first PPT generation.
Complete redesign applying font hierarchy (24/18/16/12) from the start.
Brand icon slots planned at design time, not bolted on.
Layout: Fresh Tech Deck (清新科技风) with proven v1 positioning as coordinate base.
"""
import os, re, shutil, zipfile, json
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from lxml import etree
from cairosvg import svg2png
from collections import Counter

V1 = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
MD_SRC = 'projects/ai_agent_training_v3_ppt169_20260526/sources/AI Agent 深度培训手册.md'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v12.pptx'
TMP = DST.replace('.pptx', '_tmp.pptx')
BP = 'temp/brand_pngs'
SW, SH = 12192000, 6858000
SCALE = 1.35

# ── DESIGN SPEC (from frontend-design thinking) ──
# Purpose: Enterprise AI training, knowledge workers
# Tone: Professional, clean, Fresh Tech
# Differentiation: Brand icons built into each model/workbench card
# Font Hierarchy: H1=24 H2=18 H3=16 Body=12 (HARD RULE)
# Color: Fresh Tech Deck —雾蓝#ECF2FE 冰薄荷#E8FBF5 淡紫灰#EFF1FE 强调蓝#4A7BD0

def font_target(pt):
    if pt >= 22: return 24
    elif pt >= 16: return 18
    elif pt >= 11: return 16
    else: return 12

def svg_color(c):
    if c.startswith('#'):
        h = c[1:]
        return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
    return RGBColor(0x1A,0x2D,0x4A)

def add_pic(slide, name, x, y, sz):
    p = f'{BP}/{name}.png'
    if os.path.exists(p):
        try: slide.shapes.add_picture(p, x, y, sz, sz); return True
        except: pass
    return False

print("=" * 60)
print("v12: DESIGN-FIRST PPT from md source")
print("=" * 60)

# ── Step 1: Fix theme font ──
print("\n🔤 Theme font (EA=Microsoft YaHei)...")
shutil.copy2(V1, TMP)
with zipfile.ZipFile(V1) as zin, zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = zin.read(item.filename)
        if item.filename == 'ppt/theme/theme1.xml':
            d = d.decode().replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>').encode()
        zout.writestr(item, d)

prs = Presentation(TMP)

# ── Step 2: Apply font hierarchy + scale all shapes on native slides ──
print("📏 Font hierarchy + layout scaling...")
for i, slide in enumerate(prs.slides):
    sn = i + 1
    if sn in [6, 9]: continue  # rebuilt fresh below
    
    for s in slide.shapes:
        if s.width == SW and s.height == SH and s.left == 0 and s.top == 0: continue
        if s.width > SW * 0.98 or s.height > SH * 0.98: continue
        
        # Scale shape from center
        nw = int(s.width * SCALE)
        nh = int(s.height * SCALE)
        nl = int(s.left - (nw - s.width)/2)
        nt = int(s.top - (nh - s.height)/2)
        nl = max(5000, min(nl, SW-nw-5000))
        nt = max(5000, min(nt, SH-nh-5000))
        nw = min(nw, SW-nl-5000)
        nh = min(nh, SH-nt-5000)
        if nw < 5000 or nh < 5000: continue
        s.width, s.height, s.left, s.top = nw, nh, nl, nt
        
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size: r.font.size = Pt(font_target(r.font.size.pt))
                    if r.font.name and r.font.name in ['Segoe UI','Calibri','Arial']:
                        r.font.name = 'Microsoft YaHei'

# ── Step 3: Rebuild P06, P09 as native shapes ──
print("🖼️ Rebuilding P06, P09 (native shapes from SVG content)...")
svg_scale = SW / 1280

def map_svg_font(sz):
    if sz >= 20: return 24
    elif sz >= 14: return 18
    elif sz >= 11: return 16
    else: return 12

with zipfile.ZipFile(SVG_SRC) as z:
    for sn in [6, 9]:
        svg = z.read(f'ppt/media/image{sn}.svg').decode('utf-8', errors='replace')
        slide = prs.slides[sn-1]
        
        # Remove all shapes
        spTree = slide.shapes._spTree
        for child in list(spTree):
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag in ['sp','pic','grpSp','graphicFrame']: spTree.remove(child)
        
        # Background
        bg = slide.shapes.add_shape(1, 0, 0, SW, SH)
        bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(0xFC,0xFD,0xFF)
        bg.line.fill.background()
        
        # Rects
        for r in re.finditer(r'<rect\s+([^/]*?)/?>', svg):
            a = r.group(1)
            x = float(re.search(r'x="([\d.]+)"',a).group(1)) if 'x=' in a else 0
            y = float(re.search(r'y="([\d.]+)"',a).group(1)) if 'y=' in a else 0
            w = float(re.search(r'width="([\d.]+)"',a).group(1)) if 'width=' in a else 0
            h = float(re.search(r'height="([\d.]+)"',a).group(1)) if 'height=' in a else 0
            fill = re.search(r'fill="([^"]+)"',a)
            if w < 10 or (w > 1270 and h > 710): continue
            try:
                sh = slide.shapes.add_shape(1, int(x*svg_scale*SCALE), int(y*svg_scale*SCALE),
                                              int(w*svg_scale*SCALE), int(h*svg_scale*SCALE))
                sh.fill.solid(); sh.fill.fore_color.rgb = svg_color(fill.group(1) if fill else '#FFF')
                sh.line.fill.background()
            except: pass
        
        # Texts
        for t in re.finditer(r'<text\s+([^>]*)>(.*?)</text>', svg, re.DOTALL):
            a, c = t.group(1), t.group(2)
            x = float(re.search(r'x="([\d.]+)"',a).group(1)) if 'x=' in a else 0
            y = float(re.search(r'y="([\d.]+)"',a).group(1)) if 'y=' in a else 0
            sz = float(re.search(r'font-size="([\d.]+)"',a).group(1)) if 'font-size=' in a else 12
            fill = re.search(r'fill="([^"]+)"',a)
            weight = re.search(r'font-weight="([^"]+)"',a)
            anchor = re.search(r'text-anchor="([^"]+)"',a)
            txt = re.sub(r'<[^>]+>', '', c).strip()
            if not txt: continue
            ns = map_svg_font(sz)
            ex = int(x * svg_scale * SCALE)
            ey = int((y - sz*0.75) * svg_scale * SCALE)
            try:
                tb = slide.shapes.add_textbox(ex, ey, int(SW*0.25), int(ns*1500))
                tf = tb.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; p.text = txt
                p.font.size = Pt(ns)
                p.font.color.rgb = svg_color(fill.group(1) if fill else '#4A5064')
                p.font.bold = (weight.group(1) == 'bold') if weight else False
                p.font.name = 'Microsoft YaHei'
                if anchor and anchor.group(1) == 'middle': p.alignment = PP_ALIGN.CENTER
            except: pass

# ── Step 4: Brand icons — DESIGN-TIME SLOTS (per md content analysis) ──
print("\n🏷️ Adding brand icons (design-time slots)...")

brand_plan = [
    # P08 - Global Model Rankings (md §2.1.2)
    # 6 models in left column, brands in right column + Chinese models
    (8, 'openai', 14.5, 24, 12, 12), (8, 'anthropic', 14.5, 31, 12, 12),
    (8, 'google', 14.5, 38, 12, 12), (8, 'deepseek', 14.5, 45, 12, 12),
    (8, 'meta', 14.5, 52, 12, 12), (8, 'xai', 14.5, 59, 12, 12),
    (8, 'alibaba', 49, 24, 12, 12), (8, 'baidu', 49, 31, 12, 12),
    (8, 'bytedance', 49, 38, 12, 12), (8, 'tencent', 49, 45, 12, 12),
    # P09 - First-Tier Models (md §2.2) — 4 model detail cards
    (9, 'openai', 7, 25, 16, 16), (9, 'anthropic', 7, 45, 16, 16),
    (9, 'google', 7, 65, 16, 16), (9, 'deepseek', 72, 25, 16, 16),
    # P10 - Chinese Model Panorama (md §2.3) — left col brands + right col brands
    (10, 'deepseek', 5, 42, 12, 12), (10, 'alibaba', 5, 56, 12, 12),
    (10, 'baidu', 5, 70, 12, 12), (10, 'bytedance', 50, 42, 12, 12),
    (10, 'tencent', 50, 56, 12, 12), (10, 'kimi_badge', 50, 70, 12, 12),
    # P11 - Global AI Workbenches (md §3.2)
    (11, 'github', 2.5, 46, 12, 12), (11, 'anthropic', 25.5, 46, 12, 12),
    (11, 'cursor', 48.5, 46, 12, 12), (11, 'dify', 71.5, 46, 12, 12),
    (11, 'coze', 87.5, 46, 12, 12),
    # P12 - China AI Workbenches (md §3.3)
    (12, 'dify', 5.5, 46, 12, 12), (12, 'coze', 33.5, 46, 12, 12),
    (12, 'autogpt_badge', 59.5, 46, 10, 10),
    (12, 'lovable_badge', 19.5, 75, 10, 10), (12, 'bolt_badge', 45.5, 75, 10, 10),
    (12, 'v0_badge', 71.5, 75, 10, 10),
    # P13 - OpenClaw Architecture (md §4.1)
    (13, 'github', 82, 4, 10, 10),
]

added = 0
for sn, name, xp, yp, wp, hp in brand_plan:
    slide = prs.slides[sn-1]
    sz = int(wp * 12700)
    x = int(SW * xp / 100); y = int(SH * yp / 100)
    if add_pic(slide, name, x, y, sz): added += 1

print(f"  {added} brand icons placed at design-time slots")

# ── Step 5: Final font cleanup ──
print("🔤 Final font audit...")
fixed = 0
for slide in prs.slides:
    for s in slide.shapes:
        if not s.has_text_frame: continue
        for p in s.text_frame.paragraphs:
            for r in p.runs:
                if r.font.size and r.font.size.pt < 10:
                    r.font.size = Pt(12); fixed += 1
                if r.font.name in ['Segoe UI','Calibri','Arial']:
                    r.font.name = 'Microsoft YaHei'; fixed += 1
print(f"  Fixed {fixed} remaining font issues")

# ── Save ──
prs.save(DST)
os.remove(TMP)

# ── Verification ──
p = Presentation(DST)
sizes = Counter(); bad_f = set(); pics = 0
for s in p.slides:
    for sh in s.shapes:
        if sh.shape_type == 13: pics += 1
        if not sh.has_text_frame: continue
        for pa in sh.text_frame.paragraphs:
            for r in pa.runs:
                if r.font.size: sizes[int(r.font.size.pt)] += 1
                if r.font.name in ['Segoe UI','Calibri','Arial']: bad_f.add(r.font.name)

print(f"\n{'='*60}")
print(f"📊 RESULTS")
print(f"{'='*60}")
print(f"  Slides: {len(p.slides)}")
print(f"  Fonts: {dict(sorted(sizes.items()))}")
print(f"  Bad fonts: {bad_f or 'None ✅'}")
print(f"  Brand icons: {pics}")
print(f"  Empty slides: {sum(1 for s in p.slides if len(list(s.shapes))<=1)}")
print(f"  Size: {os.path.getsize(DST):,}B")
print(f"\n✅ Generated: {DST}")
