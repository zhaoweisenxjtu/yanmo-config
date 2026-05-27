#!/usr/bin/env python3
"""
v11: FRESH DESIGN from md — font hierarchy hard-coded, brand-icon slots reserved at design time.
All shapes scaled to accommodate 24/18/16/12 fonts. P06/P09 native shapes. No SVG baking.

Font hierarchy (HARD RULE, per AGENTS.md):
  H1=24pt  H2=18pt  H3=16pt  Body=12pt  Caption=10pt
  Font = Noto Sans CJK SC / Microsoft YaHei via EA theme
"""
import os, re, shutil, zipfile, math
from pptx import Presentation
from pptx.util import Pt, Emu, Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from lxml import etree
from cairosvg import svg2png
from collections import Counter

V1 = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v11.pptx'
TMP = DST.replace('.pptx', '_tmp.pptx')
BP = 'temp/brand_pngs'
SW, SH = 12192000, 6858000

# ── Font hierarchy (HARD RULE) ──
def font_target(pt):
    """Map ANY input size to the approved hierarchy"""
    if pt >= 22: return 24  # H1
    elif pt >= 16: return 18  # H2
    elif pt >= 11: return 16  # H3
    elif pt >= 8: return 12   # Body
    else: return 12           # Body (minimum, per user spec)

# ── Step 1: Fix theme font EA → Microsoft YaHei ──
print("🔤 Theme font (EA=Microsoft YaHei)...")
shutil.copy2(V1, TMP)
with zipfile.ZipFile(V1) as zin, zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = zin.read(item.filename)
        if item.filename == 'ppt/theme/theme1.xml':
            d = d.decode().replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>').encode()
        zout.writestr(item, d)

prs = Presentation(TMP)

# ── Step 2: Apply font hierarchy + scale shapes on ALL slides ──
print("📏 Font hierarchy + shape scaling...")
cx, cy = SW/2, SH/2

for i, slide in enumerate(prs.slides):
    sn = i + 1
    count = 0
    
    for s in slide.shapes:
        # Skip full-slide backgrounds
        if s.width == SW and s.height == SH and s.left == 0 and s.top == 0:
            continue
        if s.width > SW * 0.98 or s.height > SH * 0.98:
            continue
        
        # Scale shape (grow from center)
        new_w = int(s.width * 1.35)
        new_h = int(s.height * 1.35)
        new_l = int(s.left - (new_w - s.width) / 2)
        new_t = int(s.top - (new_h - s.height) / 2)
        new_l = max(5000, min(new_l, SW - new_w - 5000))
        new_t = max(5000, min(new_t, SH - new_h - 5000))
        new_w = min(new_w, SW - new_l - 5000)
        new_h = min(new_h, SH - new_t - 5000)
        
        if new_w < 5000 or new_h < 5000:
            continue
        
        s.width, s.height = new_w, new_h
        s.left, s.top = new_l, new_t
        count += 1
        
        # Apply font hierarchy to text runs
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size:
                        r.font.size = Pt(font_target(r.font.size.pt))
                    # Force font to Microsoft YaHei for EA
                    if r.font.name and r.font.name == 'Segoe UI':
                        r.font.name = 'Microsoft YaHei'
    
    if count > 0:
        print(f'  P{sn}: {count} shapes')

# ── Step 3: Rebuild P06, P09 from SVG content as native shapes (design-time brand slots) ──
print("\n🖼️ Rebuilding P06, P09 as native shapes (with brand-icon slots)...")

def svg_color(c):
    if c.startswith('#'):
        h = c[1:]
        return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
    return RGBColor(0x1A,0x2D,0x4A)

svg_scale = SW / 1280  # SVG coord → EMU

def map_svg_font(sz):
    if sz >= 20: return 24
    elif sz >= 14: return 18
    elif sz >= 11: return 16
    else: return 12

with zipfile.ZipFile(SVG_SRC) as z:
    for sn in [6, 9]:
        svg = z.read(f'ppt/media/image{sn}.svg').decode('utf-8', errors='replace')
        slide = prs.slides[sn-1]
        
        # Remove all existing shapes
        spTree = slide.shapes._spTree
        for child in list(spTree):
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag in ['sp', 'pic', 'grpSp', 'graphicFrame']:
                spTree.remove(child)
        
        # Create background card
        bg = slide.shapes.add_shape(1, 0, 0, SW, SH)
        bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(0xFC,0xFD,0xFF)
        bg.line.fill.background()
        
        rect_count = 0
        for r in re.finditer(r'<rect\s+([^/]*?)/?>', svg):
            a = r.group(1)
            x = float(re.search(r'x="([\d.]+)"', a).group(1)) if 'x=' in a else 0
            y = float(re.search(r'y="([\d.]+)"', a).group(1)) if 'y=' in a else 0
            w = float(re.search(r'width="([\d.]+)"', a).group(1)) if 'width=' in a else 0
            h = float(re.search(r'height="([\d.]+)"', a).group(1)) if 'height=' in a else 0
            fill = re.search(r'fill="([^"]+)"', a)
            rx = float(re.search(r'rx="([\d.]+)"', a).group(1)) if 'rx=' in a else 0
            
            if w < 10 or (w > 1270 and h > 710):
                continue
            
            ex = int(x * svg_scale * 1.35)
            ey = int(y * svg_scale * 1.35)
            ew = int(w * svg_scale * 1.35)
            eh = int(h * svg_scale * 1.35)
            
            try:
                shp = slide.shapes.add_shape(1, ex, ey, ew, eh)
                shp.fill.solid()
                shp.fill.fore_color.rgb = svg_color(fill.group(1) if fill else '#FFFFFF')
                shp.line.fill.background()
                if rx > 5 and min(w,h) > 0:
                    shp.adjustments[0] = rx / min(w,h)
                rect_count += 1
            except: pass
        
        text_count = 0
        for t in re.finditer(r'<text\s+([^>]*)>(.*?)</text>', svg, re.DOTALL):
            a, c = t.group(1), t.group(2)
            x = float(re.search(r'x="([\d.]+)"', a).group(1)) if 'x=' in a else 0
            y = float(re.search(r'y="([\d.]+)"', a).group(1)) if 'y=' in a else 0
            sz = float(re.search(r'font-size="([\d.]+)"', a).group(1)) if 'font-size=' in a else 12
            fill = re.search(r'fill="([^"]+)"', a)
            weight = re.search(r'font-weight="([^"]+)"', a)
            anchor = re.search(r'text-anchor="([^"]+)"', a)
            
            txt = re.sub(r'<[^>]+>', '', c).strip()
            if not txt: continue
            
            new_sz = map_svg_font(sz)
            ex = int(x * svg_scale * 1.35)
            ey = int((y - sz * 0.75) * svg_scale * 1.35)
            ew = int(SW * 0.25)
            eh = int(new_sz * 1500)
            
            try:
                tb = slide.shapes.add_textbox(ex, ey, ew, eh)
                tf = tb.text_frame; tf.word_wrap = True
                p = tf.paragraphs[0]; p.text = txt
                p.font.size = Pt(new_sz)
                p.font.color.rgb = svg_color(fill.group(1) if fill else '#4A5064')
                p.font.bold = (weight.group(1) == 'bold') if weight else False
                p.font.name = 'Microsoft YaHei'
                if anchor and anchor.group(1) == 'middle':
                    p.alignment = PP_ALIGN.CENTER
                text_count += 1
            except: pass
        
        print(f'  P{sn}: {rect_count} cards + {text_count} texts')

# ── Step 4: Brand icons at DESIGN-TIME positions ──
# Icons placed left of brand names; sizes matched to text (12pt, 16pt)
print("\n🏷️ Brand icons (design-time slots)...")

# Brand icon placement: (slide, icon_name, x%, y%, font_pt)
# Positions chosen to sit immediately left of brand-name text at same vertical level
brands = [
    # P08 - Global Model Rankings
    # Left column models: y≈21-69% with icons at x≈14%
    (8, 'openai', 14.5, 24, 12), (8, 'anthropic', 14.5, 31, 12),
    (8, 'google', 14.5, 38, 12), (8, 'deepseek', 14.5, 45, 12),
    (8, 'meta', 14.5, 52, 12), (8, 'xai', 14.5, 59, 12),
    (8, 'alibaba', 14.5, 66, 12), (8, 'cohere_badge', 14.5, 73, 10),
    (8, 'ibm', 14.5, 80, 10),
    # Right column: y≈21-57% with icons at x≈49%
    (8, 'mistral', 49, 24, 12), (8, 'alibaba', 49, 31, 12),
    (8, 'baidu', 49, 38, 12), (8, 'bytedance', 49, 45, 12),
    (8, 'tencent', 49, 52, 12), (8, 'kimi_badge', 49, 59, 12),
    (8, 'yi_badge', 49, 66, 12),
    
    # P09 - First-tier models (designed with 4 icon slots)
    (9, 'openai', 7, 25, 16), (9, 'anthropic', 7, 45, 16),
    (9, 'google', 7, 65, 16), (9, 'deepseek', 72, 25, 16),
    
    # P10 - China Model Panorama
    (10, 'deepseek', 5, 42, 12), (10, 'alibaba', 5, 56, 12),
    (10, 'baidu', 5, 70, 12), (10, 'bytedance', 50, 42, 12),
    (10, 'tencent', 50, 56, 12), (10, 'kimi_badge', 50, 70, 12),
    
    # P11 - Global AI Workbenches
    (11, 'github', 2.5, 46, 12), (11, 'anthropic', 25.5, 46, 12),
    (11, 'cursor', 48.5, 46, 12), (11, 'dify', 71.5, 46, 12),
    (11, 'coze', 87.5, 46, 12),
    
    # P12 - China AI Workbenches
    (12, 'dify', 5.5, 46, 12), (12, 'coze', 33.5, 46, 12),
    (12, 'autogpt_badge', 59.5, 46, 10),
    (12, 'lovable_badge', 19.5, 75, 10), (12, 'bolt_badge', 45.5, 75, 10),
    (12, 'v0_badge', 71.5, 75, 10),
    
    # P13 - OpenClaw Architecture
    (13, 'github', 82, 4, 10),
]

added = 0
for sn, name, xp, yp, font_pt in brands:
    sl = prs.slides[sn-1]
    sz = int(font_pt * 12700)
    x = int(SW * xp / 100); y = int(SH * yp / 100)
    p = f'{BP}/{name}.png'
    if os.path.exists(p):
        try:
            sl.shapes.add_picture(p, x, y, sz, sz)
            added += 1
        except: pass

print(f'  {added} icons added')

# ── Step 5: Verify ──
prs.save(DST)
os.remove(TMP)

p = Presentation(DST)
pics = sum(1 for s in p.slides for sh in s.shapes if sh.shape_type == 13)
empty = sum(1 for s in p.slides if len(list(s.shapes)) <= 1)

sizes = Counter()
for s in p.slides:
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size: sizes[int(r.font.size.pt)] += 1

print(f"\n📊 Slides: {len(p.slides)}, Empty: {empty}, Pics: {pics}")
print(f"📏 Fonts: {dict(sorted(sizes.items()))}")
# Check for non-CJK fonts
bad_fonts = set()
for s in p.slides:
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.name and r.font.name in ['Segoe UI', 'Calibri', 'Arial']:
                        bad_fonts.add(r.font.name)
if bad_fonts:
    print(f"⚠️  Non-CJK fonts found: {bad_fonts}")
else:
    print("✅ All fonts CJK-compatible")

print(f"📦 Size: {os.path.getsize(DST):,}B")
print(f"✅ Done: {DST}")
