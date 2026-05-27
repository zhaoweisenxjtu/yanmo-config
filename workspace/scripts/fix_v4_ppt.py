#!/usr/bin/env python3
"""
Fix v4: 
1. Remove overlapping large illustrations from dense content slides
2. Fill empty slides 6 & 9 with SVG版 rendered content
3. Keep brand icons intact
"""
import os, base64, zipfile, re
from pptx import Presentation
from pptx.util import Emu
from cairosvg import svg2png
from io import BytesIO

V3 = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v3.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v4.pptx'

print("=" * 60)
print("Fixing v4: remove overlapping illustrations, fill empty slides")
print("=" * 60)

prs = Presentation(V3)
sw = prs.slide_width
sh = prs.slide_height

# ── Step 1: Remove large illustrations (not brand icons) from all slides ──
print("\n🗑️ Removing overlapping illustrations...")
removed = 0
for slide in prs.slides:
    shapes_to_remove = []
    for shape in slide.shapes:
        if shape.shape_type == 13 and shape.width > 1000000:
            # This is a large illustration (not a brand icon)
            shapes_to_remove.append(shape)
    
    for shape in shapes_to_remove:
        # python-pptx doesn't have a direct remove method in all versions
        # Use XML manipulation
        sp = shape._element
        sp.getparent().remove(sp)
        removed += 1

print(f"  Removed {removed} large illustrations")

# ── Step 2: Render SVG版 slides 6 and 9 as full-page PNGs ──
print("\n🖼️ Adding content to empty slides 6 and 9...")

# Get SVG content from SVG版 for slides 6 and 9 (1-indexed = slides 6 and 9)
with zipfile.ZipFile(SVG_SRC, 'r') as z:
    for slide_num in [6, 9]:  # 1-indexed slide numbers
        svg_content = z.read(f'ppt/media/image{slide_num}.svg').decode('utf-8', errors='replace')
        
        # Fix: replace fill="#EFF1FE" fill="#4A7BD0" → fill="#4A7BD0" (keep last value)
        import re
        svg_fixed = re.sub(r'(\w+)="([^"]*)"(\s+\1="[^"]*")+', lambda m: f'{m.group(1)}="{m.group(2)}"', svg_content)
        
        # Render to high-res PNG
        png_data = svg2png(bytestring=svg_fixed.encode(), scale=2, output_width=2560, output_height=1440)
        
        # Add to slide as full background image
        slide_idx = slide_num - 1  # 0-indexed
        slide = prs.slides[slide_idx]
        
        # Save PNG to temp
        png_path = f'/tmp/slide{slide_num}_content.png'
        with open(png_path, 'wb') as f:
            f.write(png_data)
        
        # Add as full-slide picture
        pic = slide.shapes.add_picture(png_path, 0, 0, sw, sh)
        
        # Send to back (behind any existing shapes like brand icons)
        # Move XML element to be the first child of spTree
        spTree = slide.shapes._spTree
        spTree.remove(pic._element)
        spTree.insert(2, pic._element)  # Insert after cSld and nvGrpSpPr
        
        print(f"  ✅ Slide {slide_num}: added rendered content ({len(png_data):,} bytes)")

# ── Step 3: Save ──
print(f"\n💾 Saving to {DST}...")
prs.save(DST)

# Verify
prs2 = Presentation(DST)
print(f"  Slides: {len(prs2.slides)}")
pics = 0
empty = 0
for i, slide in enumerate(prs2.slides):
    n = len(list(slide.shapes))
    if n == 0:
        empty += 1
        print(f"  ⚠️  Slide {i+1}: EMPTY ({n} shapes)")
    for s in slide.shapes:
        if s.shape_type == 13:
            pics += 1

print(f"  Total pictures: {pics}")
print(f"  Empty slides: {empty}")
print(f"  Size: {os.path.getsize(DST):,} bytes")
print(f"\n✅ Done! Saved to {DST}")
