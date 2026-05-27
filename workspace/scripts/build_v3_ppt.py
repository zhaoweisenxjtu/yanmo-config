#!/usr/bin/env python3
"""
Build v3: Keep v1 native shapes editable + overlay brand icons + illustrations
Fix: Add EA font (Noto Sans CJK SC) to theme for cross-platform compatibility
"""
import os, copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v3.pptx'
BRAND_PNG = 'temp/brand_pngs'
ILLUSTRATION_PNG = 'temp/illustration_pngs'

# ── Brand icon placement map: {slide_num: [(brand_name, x_emu, y_emu, w_emu, h_emu)]} ──
# Emu positions relative to slide (12192000 x 6858000)
# Brand icons: small badges ~400x400 EMU (~0.44 inch)
BI = 400000  # brand icon size
SI = 200000  # small icon size

BRAND_SLIDES = {
    # Page 8 (slide 8): 全球评测体系+排名格局 - model brands in right column
    8: [
        # Column 1 (left side model cards, x~600000)
        ("openai", 1800000, 1950000, BI, BI),
        ("anthropic", 1800000, 2850000, BI, BI),
        ("google", 1800000, 3750000, BI, BI),
        ("deepseek", 1800000, 4650000, BI, BI),
        ("meta", 1800000, 5550000, BI, BI),
        ("xai", 7800000, 1950000, BI, BI),
        ("alibaba", 7800000, 2850000, BI, BI),
        ("baidu", 7800000, 3750000, BI, BI),
        ("mistral", 7800000, 4650000, BI, BI),
        ("ibm", 7800000, 5550000, BI, BI),
    ],
    # Page 9 (slide 9): 第一梯队模型详解
    9: [
        ("openai", 700000, 1800000, BI, BI),
        ("anthropic", 3400000, 1800000, BI, BI),
        ("google", 6100000, 1800000, BI, BI),
        ("deepseek", 8800000, 1800000, BI, BI),
    ],
    # Page 10 (slide 10): 中国模型全景
    10: [
        ("deepseek", 1600000, 2800000, BI, BI),
        ("alibaba", 1600000, 3800000, BI, BI),
        ("baidu", 1600000, 4800000, BI, BI),
        ("bytedance", 7200000, 2800000, BI, BI),
        ("tencent", 7200000, 3800000, BI, BI),
        ("kimi_badge", 7200000, 4800000, BI, BI),
    ],
    # Page 11 (slide 11): 全球Top5 AI工作台
    11: [
        ("github", 700000, 3100000, BI, BI),
        ("anthropic", 3100000, 3100000, BI, BI),
        ("cursor", 5500000, 3100000, BI, BI),
        ("dify", 7900000, 3100000, BI, BI),
        ("coze", 10300000, 3100000, BI, BI),
    ],
    # Page 12 (slide 12): 中国Top5 + 平台对比
    12: [
        ("dify", 1200000, 3400000, BI, BI),
        ("coze", 4600000, 3400000, BI, BI),
        ("autogpt_badge", 8000000, 3400000, BI, BI),
        ("lovable_badge", 3200000, 5200000, BI, BI),
        ("bolt_badge", 6400000, 5200000, BI, BI),
        ("v0_badge", 9600000, 5200000, BI, BI),
    ],
    # Page 13 (slide 13): OpenClaw架构
    13: [
        ("github", 10500000, 200000, SI, SI),
    ],
}

# ── Illustration placement map ──
# Larger illustrations (decorative, usually right side or bottom)
ILLUSTRATION_SLIDES = {
    # Page 2 (slide 2): 目录/培训路线图
    2: [
        ("Online_Community", 9300000, 4500000, 2500000, 2000000),
    ],
    # Page 3 (slide 3): LLM发展里程碑
    3: [
        ("Artificial_Intelligence", 9800000, 4800000, 2000000, 1800000),
    ],
    # Page 7 (slide 7): 技能+小结
    7: [
        ("MCP_Server", 9500000, 4500000, 2200000, 2000000),
    ],
    # Page 9 (slide 9): 第一梯队
    9: [
        ("AI_Answers", 9200000, 5000000, 2400000, 1600000),
    ],
    # Page 14 (slide 14): Agent循环
    14: [
        ("Server_Status", 200000, 5500000, 2000000, 1200000),
    ],
    # Page 5 (slide 5): Agent工作流
    5: [
        ("Team_up", 9500000, 5000000, 2200000, 1600000),
    ],
}

def add_picture_to_slide(slide, png_path, left, top, width, height):
    """Add a picture to slide if file exists"""
    if not os.path.exists(png_path):
        print(f"  ⚠️  File not found: {png_path}")
        return False
    try:
        pic = slide.shapes.add_picture(png_path, left, top, width, height)
        print(f"  ✅ Added {os.path.basename(png_path)} at ({left},{top}) {width}x{height}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to add {os.path.basename(png_path)}: {e}")
        return False

def fix_theme_font_via_xml(pptx_path, output_path):
    """Directly modify EA font in theme XML within the PPTX ZIP"""
    import shutil, zipfile, os, tempfile
    
    shutil.copy2(pptx_path, output_path)
    
    # We'll use zipfile to directly modify the XML
    with zipfile.ZipFile(pptx_path, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'ppt/theme/theme1.xml':
                    xml = data.decode('utf-8')
                    # Replace ea typeface from empty to 微软雅黑
                    xml = xml.replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>')
                    xml = xml.replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>')
                    data = xml.encode('utf-8')
                zout.writestr(item, data)
    
    # Verify
    with zipfile.ZipFile(output_path, 'r') as z:
        th = z.read('ppt/theme/theme1.xml').decode()
        import re
        ea = re.findall(r'<a:ea[^>]*typeface="([^"]+)"', th)
        print(f'  ✅ Theme EA fonts: {ea}')
    
    return True

def fix_text_run_fonts(prs):
    """Keep Segoe UI — it works on WPS via font linking (font fallback to MS YaHei)"""
    changes = 0
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame') and shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.name and 'Noto' in run.font.name:
                            run.font.name = 'Segoe UI'
                            changes += 1
    print(f"  ✅ Restored {changes} text runs to Segoe UI (font linking handles Chinese)")
    return changes

# ── MAIN ──
print("=" * 60)
print("Building v3 PPT: native shapes + brand icons + illustrations")
print("=" * 60)

# Load v1
prs = Presentation(SRC)
print(f"\n📂 Loaded v1: {len(prs.slides)} slides, {len(prs.slide_masters)} master(s)")

# Step 1: Fix fonts
# Strategy: Keep Segoe UI for text runs (WPS font linking handles CJK fallback),
# but set theme EA font to Microsoft YaHei for proper East Asian defaults.
print("\n🔤 Fixing fonts...")

# 1a: Fix theme EA font directly in XML (python-pptx can't persist theme font changes)
INTERMEDIATE = DST.replace('.pptx', '_tmp.pptx')
fix_theme_font_via_xml(SRC, INTERMEDIATE)

# 1b: Reload from the fixed file and restore text run fonts to Segoe UI
prs = Presentation(INTERMEDIATE)
fix_text_run_fonts(prs)

# Step 3: Add brand icons
print("\n🏷️ Adding brand icons...")
for slide_num, icons in BRAND_SLIDES.items():
    slide = prs.slides[slide_num - 1]  # 0-indexed
    print(f"  Slide {slide_num}:")
    for brand, x, y, w, h in icons:
        # Try brand-specific PNG first, then badge PNG
        png_path = os.path.join(BRAND_PNG, f"{brand}.png")
        if not os.path.exists(png_path):
            png_path = os.path.join(BRAND_PNG, f"{brand}_badge.png")
        add_picture_to_slide(slide, png_path, x, y, w, h)

# Step 4: Add illustrations
print("\n🎨 Adding illustrations...")
for slide_num, illustrations in ILLUSTRATION_SLIDES.items():
    slide = prs.slides[slide_num - 1]
    print(f"  Slide {slide_num}:")
    for name, x, y, w, h in illustrations:
        png_path = os.path.join(ILLUSTRATION_PNG, f"{name}.png")
        add_picture_to_slide(slide, png_path, x, y, w, h)

# Step 5: Save (saves to the fixed-pptx already)
print(f"\n💾 Saving final to {INTERMEDIATE}...")
prs.save(INTERMEDIATE)
os.replace(INTERMEDIATE, DST)
print(f"✅ Done! Saved to {DST}")

# Summary
import os
sz = os.path.getsize(DST)
print(f"📦 File size: {sz:,} bytes ({sz/1024:.1f} KB)")
