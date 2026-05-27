#!/usr/bin/env python3
"""v5: Correct illustration/brand placement based on whitespace analysis."""
import os, shutil, zipfile, re, base64
from pptx import Presentation
from pptx.util import Emu
from cairosvg import svg2png

V1 = 'deliverables/AI Agent深度培训手册_清新科技风_20页.pptx'
SVG_SRC = 'deliverables/AI Agent深度培训手册_清新科技风_20页_svg版.pptx'
DST = 'deliverables/AI Agent深度培训手册_清新科技风_20页_v5.pptx'
TMP = DST.replace('.pptx', '_tmp.pptx')
BP = 'temp/brand_pngs'
IP = 'temp/illustration_pngs'
SW, SH = 12192000, 6858000  # EMU

def add_pic(slide, name, x, y, w, h):
    for d in [BP, IP]:
        p = f'{d}/{name}'
        if os.path.exists(p):
            try: slide.shapes.add_picture(p, x, y, w, h); return True
            except: pass
    return False

def pct(x,y,w,h):
    return (int(SW*x/100), int(SH*y/100), int(SW*w/100), int(SH*h/100))

# Theme font fix
print("Fixing theme font...")
shutil.copy2(V1, TMP)
with zipfile.ZipFile(V1) as zin, zipfile.ZipFile(TMP,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        d = zin.read(item.filename)
        if item.filename == 'ppt/theme/theme1.xml':
            d = d.decode().replace('<a:ea typeface=""/>', '<a:ea typeface="Microsoft YaHei"/>').encode()
        zout.writestr(item, d)

prs = Presentation(TMP)

# Brand icons
brands = {
    8: [('openai',6.5,22,4,4),('anthropic',6.5,39,4,4),('google',6.5,56,4,4),
        ('deepseek',6.5,73,4,4),('meta',52,22,4,4),('xai',52,39,4,4),('alibaba',52,56,4,4),('mistral',52,73,4,4)],
    9: [('openai',8,20,5,5),('anthropic',8,38,5,5),('google',8,56,5,5),('deepseek',8,74,5,5)],
    10: [('deepseek',7,36,4,4),('alibaba',7,51,4,4),('baidu',7,66,4,4),
         ('bytedance',52,36,4,4),('tencent',52,51,4,4),('kimi_badge',52,66,4,4)],
    11: [('github',5,42,4,4),('anthropic',28,42,4,4),('cursor',51,42,4,4),('dify',74,42,4,4),('coze',90,42,4,4)],
    12: [('dify',8,42,4,4),('coze',36,42,4,4),('autogpt_badge',62,42,4,4),
         ('lovable_badge',22,68,4,4),('bolt_badge',48,68,4,4),('v0_badge',74,68,4,4)],
    13: [('github',82,3,3,3)],
}
print("Adding brand icons...")
for sn, icons in brands.items():
    sl = prs.slides[sn-1]
    for nm, xp, yp, wp, hp in icons:
        x,y,w,h = pct(xp,yp,wp,hp)
        ok = add_pic(sl, f'{nm}.png', x, y, w, h)
        if not ok: print(f'  SN{sn}: {nm} MISSING')

# Illustrations
# Placement based on zone analysis -> right-side free zones and bottom margins
illus = {
    # P02 目录: bottom 22% free -> center-bottom
    2: ('Online_Community', 30, 69, 40, 25),
    # P03 LLM里程碑: bottom 26% free -> center-bottom
    3: ('Artificial_Intelligence', 35, 67, 30, 27),
    # P04 Agent公式: tight, small right decor
    4: ('Team_chat', 78, 50, 18, 25),
    # P05 工作流: right 2/4 + bottom 23% free -> bottom-right
    5: ('Team_up', 68, 55, 28, 35),
    # P06 记忆系统: EMPTY -> small overlay on full-page SVG bg
    6: ('Server_Status', 80, 50, 15, 20),
    # P07 RAG+技能: tight -> center-bottom strip
    7: ('MCP_Server', 30, 72, 40, 22),
    # P08 评测: 4/4 right free (22% margin) -> right column
    8: ('Team_work', 78, 15, 20, 55),
    # P09 第一梯队: EMPTY -> small overlay on full-page SVG bg
    9: ('AI_Answers', 75, 68, 22, 28),
    # P10 中国模型: 3/4 right, 7% margin -> bottom strip
    10: ('AI_Slop', 40, 80, 25, 15),
    # P13 OpenClaw: 2/4 right free (18% margin)
    13: ('Server_Failure', 80, 40, 18, 35),
    # P14 Agent循环: 3/4 right + 16% bottom
    14: ('Connection_lost', 82, 20, 16, 45),
    # P15 行业研究: 4/4 right (21% margin)
    15: ('Cloudflare_Dev', 78, 20, 20, 50),
}
print("Adding illustrations...")
for sn, (nm, xp, yp, wp, hp) in sorted(illus.items()):
    sl = prs.slides[sn-1]
    x,y,w,h = pct(xp,yp,wp,hp)
    ok = add_pic(sl, f'{nm}.png', x, y, w, h)
    st = 'OK' if ok else 'FAIL'
    print(f'  P{sn}: {st} {nm} ({xp}%x{yp}% {wp}x{hp}%)')

# Fill empty slides 6,9 with SVG content
print("Filling empty slides...")
with zipfile.ZipFile(SVG_SRC) as z:
    for sn in [6, 9]:
        svg = z.read(f'ppt/media/image{sn}.svg').decode()
        svg = re.sub(r'(\w+)="([^"]*)"(\s+\1="[^"]*")+', lambda m: f'{m.group(1)}="{m.group(2)}"', svg)
        png = svg2png(bytestring=svg.encode(), scale=2, output_width=2560, output_height=1440)
        pp = f'/tmp/s{sn}_render.png'
        open(pp,'wb').write(png)
        sl = prs.slides[sn-1]
        pic = sl.shapes.add_picture(pp, 0, 0, SW, SH)
        # send to back
        spTree = sl.shapes._spTree
        spTree.remove(pic._element)
        spTree.insert(2, pic._element)
        print(f'  P{sn}: full-page ({len(png)}B)')

# Save
print(f"\nSaving...")
prs.save(DST)
os.remove(TMP)

# Verify
p = Presentation(DST)
pics = sum(1 for s in p.slides for sh in s.shapes if sh.shape_type == 13)
empty = sum(1 for s in p.slides if len(list(s.shapes)) <= 1)
print(f"Slides: {len(p.slides)}, Pics: {pics}, Near-empty: {empty}")
print(f"Size: {os.path.getsize(DST):,}B")
print(f"Done: {DST}")
