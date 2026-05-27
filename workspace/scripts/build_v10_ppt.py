#!/usr/bin/env python3
"""
v10: Comprehensive scaling — ALL shapes scaled uniformly (1.35x from slide center).
Slides 6 & 9: SVG → native shapes (editable text), no more baked PNGs.
Also: theme font fix, brand icons at text-matched size.
"""
import os, shutil, zipfile, re, math
from pptx import Presentation
from pptx.util import Pt, Emu, Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from lxml import etree
from cairosvg import svg2png

V1 = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v10.pptx'
TMP = DST.replace('.pptx', '_tmp.pptx')
BP = 'temp/brand_pngs'
SW, SH = 12192000, 6858000
SCALE = 1.35  # uniform scale factor for all shapes

def add_pic(slide, name, x, y, w, h):
    p = f'{BP}/{name}'
    if os.path.exists(p):
        try: slide.shapes.add_picture(p, x, y, w, h); return True
        except: pass
    return False

# ── Step 1: Fix theme font ──
print("🔤 Theme font fix...")
shutil.copy2(V1, TMP)
with zipfile.ZipFile(V1) as zin, zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = zin.read(item.filename)
        if item.filename == 'ppt/theme/theme1.xml':
            d = d.decode().replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>').encode()
        zout.writestr(item, d)

prs = Presentation(TMP)

# ── Step 2: Scale ALL shapes on NOEMPTY slides (1-5,7-8,10-20) ──
# Scale from slide center: positions + dimensions × SCALE
print(f"📏 Scaling ALL shapes {SCALE}x from slide center...")
cx, cy = SW/2, SH/2  # slide center

for i, slide in enumerate(prs.slides):
    sn = i + 1
    # Skip SVG-fill slides (6,9) — they'll be rebuilt from scratch
    if sn in [6, 9]:
        continue
    
    count = 0
    for s in slide.shapes:
        # Skip full-slide backgrounds
        if s.width == SW and s.height == SH and s.left == 0 and s.top == 0:
            continue
        
        # Skip elements that are already at full-slide width (decorative bars)
        if s.width > SW * 0.95 or s.height > SH * 0.95:
            continue
        
        # Scale: enlarge dimensions in-place (no position shift)
        # This avoids shapes going off-slide or overlapping
        new_w = int(s.width * SCALE)
        new_h = int(s.height * SCALE)
        
        # Move position so center stays same
        new_l = int(s.left - (new_w - s.width) / 2)
        new_t = int(s.top - (new_h - s.height) / 2)
        
        # Clamp to slide bounds
        new_l = max(10000, min(new_l, SW - new_w - 10000))
        new_t = max(10000, min(new_t, SH - new_h - 10000))
        new_w = min(new_w, SW - new_l - 5000)
        new_h = min(new_h, SH - new_t - 5000)
        
        # Skip if invalid
        if new_w < 10000 or new_h < 10000:
            continue
        
        s.width, s.height = new_w, new_h
        s.left, s.top = new_l, new_t
        count += 1
        
        # Map font sizes to hierarchy: 24/18/16/12
        def map_font(pt):
            if pt >= 22: return 24
            elif pt >= 16: return 18
            elif pt >= 11: return 16
            else: return 12
        
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size:
                        old_sz = r.font.size.pt
                        new_sz = map_font(old_sz)
                        if new_sz != old_sz:
                            r.font.size = Pt(new_sz)
                # Set line spacing consistent with font size
                avg_sz = 12
                if any(r.font.size for r in p.runs):
                    avg_sz = max(r.font.size.pt for r in p.runs if r.font.size)
                p.line_spacing = Pt(avg_sz * 1.5) if avg_sz else None
    
    if count > 0:
        print(f'  P{sn}: {count} shapes scaled')

# ── Step 3: Rebuild slides 6 & 9 from SVG → native shapes ──
print("\n🖼️ Rebuilding slides 6, 9 as native shapes...")

svg_pt_to_emu = SW / 1280  # SVG 1280x720 → EMU

def svg_color_to_rgb(color_str):
    """Convert SVG color like #1A2D4A to RGBColor"""
    if color_str.startswith('#'):
        h = color_str[1:]
        return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
    return RGBColor(0x1A, 0x2D, 0x4A)

def map_svg_font_size(svg_pt):
    """Map SVG font size to scaled PPTX font size"""
    pt = svg_pt * SCALE
    if pt >= 22: return 24
    elif pt >= 16: return 18
    elif pt >= 12: return 16
    else: return 12

with zipfile.ZipFile(SVG_SRC) as z:
    for sn in [6, 9]:
        svg = z.read(f'ppt/media/image{sn}.svg').decode('utf-8', errors='replace')
        slide = prs.slides[sn-1]
        
        # Remove any existing shapes on this slide
        spTree = slide.shapes._spTree
        for child in list(spTree):
            tag = etree.QName(child.tag).localname if child.tag.startswith('{') else child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag in ['sp', 'pic', 'grpSp', 'graphicFrame']:
                spTree.remove(child)
        
        # 3a: Extract and create rect elements (card backgrounds)
        rects = re.findall(r'<rect\s+([^/]*?)/?>', svg)
        rect_count = 0
        for rect_attrs in rects:
            x = float(re.search(r'x="([\d.]+)"', rect_attrs).group(1)) if re.search(r'x="([\d.]+)"', rect_attrs) else 0
            y = float(re.search(r'y="([\d.]+)"', rect_attrs).group(1)) if re.search(r'y="([\d.]+)"', rect_attrs) else 0
            w = float(re.search(r'width="([\d.]+)"', rect_attrs).group(1)) if re.search(r'width="([\d.]+)"', rect_attrs) else 0
            h = float(re.search(r'height="([\d.]+)"', rect_attrs).group(1)) if re.search(r'height="([\d.]+)"', rect_attrs) else 0
            rx = float(re.search(r'rx="([\d.]+)"', rect_attrs).group(1)) if re.search(r'rx="([\d.]+)"', rect_attrs) else 0
            fill = re.search(r'fill="([^"]*)"', rect_attrs)
            fill_color = fill.group(1) if fill else '#FFFFFF'
            stroke = re.search(r'stroke="([^"]*)"', rect_attrs)
            stroke_w = re.search(r'stroke-width="([\d.]+)"', rect_attrs)
            
            # Skip tiny rects (< 10px) and full-bg rects
            if w < 10 or (w > 1270 and h > 710):
                continue
            
            ex = int(x * svg_pt_to_emu * SCALE)
            ey = int(y * svg_pt_to_emu * SCALE)
            ew = int(w * svg_pt_to_emu * SCALE)
            eh = int(h * svg_pt_to_emu * SCALE)
            
            try:
                shape = slide.shapes.add_shape(
                    1, ex, ey, ew, eh  # MSO_SHAPE.RECTANGLE
                )
                shape.fill.solid()
                shape.fill.fore_color.rgb = svg_color_to_rgb(fill_color)
                shape.line.fill.background()  # no border
                if rx > 0:
                    # Set rounded corners via adjust value
                    shape.adjustments[0] = rx / min(w, h) if min(w, h) > 0 else 0.1
                rect_count += 1
            except:
                pass
        
        # 3b: Extract and create text elements
        texts = re.findall(r'<text\s+([^>]*)>(.*?)</text>', svg, re.DOTALL)
        text_count = 0
        for attrs, content in texts:
            x = re.search(r'x="([\d.]+)"', attrs)
            y = re.search(r'y="([\d.]+)"', attrs)
            sz = re.search(r'font-size="([\d.]+)"', attrs)
            fill = re.search(r'fill="([^"]*)"', attrs)
            weight = re.search(r'font-weight="([^"]*)"', attrs)
            anchor = re.search(r'text-anchor="([^"]*)"', attrs)
            
            xv = float(x.group(1)) if x else 0
            yv = float(y.group(1)) if y else 0
            szv = float(sz.group(1)) if sz else 12
            fillv = fill.group(1) if fill else '#4A5064'
            wtv = weight.group(1) if weight else '400'
            ancv = anchor.group(1) if anchor else 'start'
            
            # Clean content
            txt = re.sub(r'<[^>]+>', '', content).strip()
            if not txt:
                continue
            
            # Position
            ex = int(xv * svg_pt_to_emu * SCALE)
            ey = int((yv - szv * 0.75) * svg_pt_to_emu * SCALE)  # SVG y is baseline
            new_sz = map_svg_font_size(szv)
            text_w = min(int(len(txt) * new_sz * 800), SW - ex - 10000)
            text_h = int(new_sz * 1500)
            
            try:
                txBox = slide.shapes.add_textbox(ex, ey, text_w, text_h)
                tf = txBox.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = txt
                p.font.size = Pt(new_sz)
                p.font.color.rgb = svg_color_to_rgb(fillv)
                p.font.bold = (wtv == 'bold')
                
                # Alignment
                if ancv == 'middle':
                    p.alignment = PP_ALIGN.CENTER
                elif ancv == 'end':
                    p.alignment = PP_ALIGN.RIGHT
                    
                text_count += 1
            except:
                pass
        
        print(f'  P{sn}: {rect_count} rects + {text_count} text elements converted to native shapes')

# ── Step 4: Add brand icons (text-matched size) ──
print("\n🏷️ Brand icons...")

brands_map = [
    # P08: 16 icons at 12pt (most), 10pt (badge)
    (8, 'openai', 14.5, 24, 12), (8, 'anthropic', 14.5, 31, 12),
    (8, 'google', 14.5, 38, 12), (8, 'deepseek', 14.5, 45, 12),
    (8, 'meta', 14.5, 52, 12), (8, 'xai', 14.5, 59, 12),
    (8, 'alibaba', 14.5, 66, 12), (8, 'cohere_badge', 14.5, 73, 10),
    (8, 'ibm', 14.5, 80, 10), (8, 'mistral', 49, 24, 12),
    (8, 'alibaba', 49, 31, 12), (8, 'baidu', 49, 38, 12),
    (8, 'bytedance', 49, 45, 12), (8, 'tencent', 49, 52, 12),
    (8, 'kimi_badge', 49, 59, 12), (8, 'yi_badge', 49, 66, 12),
    # P09: 4 icons at 16pt
    (9, 'openai', 7, 25, 16), (9, 'anthropic', 7, 48, 16),
    (9, 'google', 7, 71, 16), (9, 'deepseek', 72, 25, 16),
    # P10: 6 icons at 12pt
    (10, 'deepseek', 5, 42, 12), (10, 'alibaba', 5, 56, 12),
    (10, 'baidu', 5, 70, 12), (10, 'bytedance', 50, 42, 12),
    (10, 'tencent', 50, 56, 12), (10, 'kimi_badge', 50, 70, 12),
    # P11: 5 icons at 12pt
    (11, 'github', 2.5, 46, 12), (11, 'anthropic', 25.5, 46, 12),
    (11, 'cursor', 48.5, 46, 12), (11, 'dify', 71.5, 46, 12),
    (11, 'coze', 87.5, 46, 12),
    # P12: 6 icons at 10-12pt
    (12, 'dify', 5.5, 46, 12), (12, 'coze', 33.5, 46, 12),
    (12, 'autogpt_badge', 59.5, 46, 10),
    (12, 'lovable_badge', 19.5, 75, 10), (12, 'bolt_badge', 45.5, 75, 10),
    (12, 'v0_badge', 71.5, 75, 10),
    # P13: corner
    (13, 'github', 82, 4, 10),
]

for sn, name, xp, yp, font_pt in brands_map:
    sl = prs.slides[sn-1]
    icon_sz = int(font_pt * 12700)  # font pt → EMU
    x = int(SW * xp / 100)
    y = int(SH * yp / 100)
    add_pic(sl, f'{name}.png', x, y, icon_sz, icon_sz)

# ── Step 5: Save ──
print("\n💾 Saving...")
prs.save(DST)
os.remove(TMP)

# Verify
p = Presentation(DST)
pics = sum(1 for s in p.slides for sh in s.shapes if sh.shape_type == 13)
empty = sum(1 for s in p.slides if len(list(s.shapes)) <= 1)

# Check font sizes
from collections import Counter
sizes = Counter()
for s in p.slides:
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size: sizes[int(r.font.size.pt)] += 1

print(f"Slides: {len(p.slides)}, Pics: {pics}, Near-empty: {empty}")
print(f"Font sizes: {dict(sorted(sizes.items()))}")
print(f"Size: {os.path.getsize(DST):,}B")
print(f"Done: {DST}")
