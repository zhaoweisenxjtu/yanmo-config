#!/usr/bin/env python3
"""Generate AI Agent Training PPT using python-pptx with Fresh Tech style"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import io

# ============================================================
# COLOR SYSTEM - Fresh Tech Deck
# ============================================================
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
NEAR_WHITE = RGBColor(0xFC, 0xFD, 0xFF)
BLUE_FROST = RGBColor(0xEC, 0xF2, 0xFE)
BLUE_LIGHT = RGBColor(0xE9, 0xF3, 0xFF)
BLUE_PALE = RGBColor(0xE5, 0xF1, 0xFF)
MINT = RGBColor(0xE8, 0xFB, 0xF5)
MINT_LIGHT = RGBColor(0xE8, 0xFB, 0xF7)
LAVENDER = RGBColor(0xEF, 0xF1, 0xFE)
LAVENDER_LIGHT = RGBColor(0xEE, 0xF5, 0xFF)
HEADER_START = RGBColor(0xF4, 0xF8, 0xFF)
EDGE_BLUE = RGBColor(0xFA, 0xFB, 0xFF)

TEXT_PRIMARY = RGBColor(0x1A, 0x1F, 0x2E)
TEXT_SECONDARY = RGBColor(0x4A, 0x50, 0x64)
TEXT_MUTED = RGBColor(0x8E, 0x93, 0xA4)
ACCENT_BLUE = RGBColor(0x4A, 0x7B, 0xD0)
ACCENT_TEAL = RGBColor(0x5B, 0xBF, 0xA0)
ACCENT_DARK = RGBColor(0x1A, 0x2D, 0x4A)

FONT_NAME = 'Microsoft YaHei'

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def set_slide_bg(slide, color):
    """Set slide background to solid color"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, fill_color=None, line_color=None):
    """Add a rectangle shape"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    return shape

def add_rounded_rect(slide, left, top, width, height, fill_color=None):
    """Add a rounded rectangle"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    return shape

def add_textbox(slide, left, top, width, height, text, font_size=14, color=TEXT_PRIMARY, 
                bold=False, alignment=PP_ALIGN.LEFT, font_name=FONT_NAME):
    """Add a text box with formatted text"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_paragraph(text_frame, text, font_size=14, color=TEXT_PRIMARY, bold=False, 
                  alignment=PP_ALIGN.LEFT, space_before=4, space_after=2):
    """Add a paragraph to existing text frame"""
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = FONT_NAME
    p.alignment = alignment
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    return p

def add_top_bar(slide):
    """Add the ice-blue top gradient bar"""
    add_rect(slide, Inches(0), Inches(0), Inches(13.33), Inches(0.5), HEADER_START)
    add_rect(slide, Inches(0), Inches(0.5), Inches(13.33), Inches(0.03), BLUE_FROST)

def add_bottom_bar(slide):
    """Add subtle bottom bar"""
    add_rect(slide, Inches(0), Inches(7.1), Inches(13.33), Inches(0.02), BLUE_FROST)

def add_slide_title(slide, title, subtitle=None):
    """Add standard slide title with optional subtitle"""
    add_top_bar(slide)
    add_textbox(slide, Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.6),
                title, font_size=28, color=ACCENT_DARK, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(1.25), Inches(11.5), Inches(0.35),
                    subtitle, font_size=14, color=TEXT_MUTED)

def add_card(slide, left, top, width, height, title, items, card_color=BLUE_FROST):
    """Add a card with title and bullet items"""
    card = add_rounded_rect(slide, left, top, width, height, card_color)
    # Card title
    add_textbox(slide, left + Inches(0.2), top + Inches(0.12), width - Inches(0.4), Inches(0.35),
                title, font_size=16, color=ACCENT_DARK, bold=True)
    # Items
    y_offset = top + Inches(0.5)
    for item in items:
        txb = add_textbox(slide, left + Inches(0.25), y_offset, width - Inches(0.5), Inches(0.28),
                          f"▸ {item}", font_size=12, color=TEXT_SECONDARY)
        y_offset += Inches(0.28)

def add_icon_card(slide, left, top, width, height, title, items, card_color=BLUE_FROST, icon_text=""):
    """Add card with icon prefix"""
    card = add_rounded_rect(slide, left, top, width, height, card_color)
    # Icon + title
    label = f"{icon_text} {title}" if icon_text else title
    add_textbox(slide, left + Inches(0.2), top + Inches(0.12), width - Inches(0.4), Inches(0.35),
                label, font_size=15, color=ACCENT_DARK, bold=True)
    y_offset = top + Inches(0.48)
    for item in items:
        txb = add_textbox(slide, left + Inches(0.25), y_offset, width - Inches(0.5), Inches(0.26),
                          f"· {item}", font_size=11, color=TEXT_SECONDARY)
        y_offset += Inches(0.26)

def add_section_divider(slide, section_num, section_title, subtitle=""):
    """Create a section divider chapter page"""
    set_slide_bg(slide, WHITE)
    # Top bar
    add_top_bar(slide)
    # Large centered section number
    add_textbox(slide, Inches(0.8), Inches(1.8), Inches(2), Inches(1.2),
                f"0{section_num}", font_size=72, color=ACCENT_BLUE, bold=True)
    # Section title
    add_textbox(slide, Inches(0.8), Inches(3.0), Inches(11), Inches(0.8),
                section_title, font_size=36, color=ACCENT_DARK, bold=True)
    if subtitle:
        add_textbox(slide, Inches(0.8), Inches(3.8), Inches(11), Inches(0.5),
                    subtitle, font_size=16, color=TEXT_MUTED)
    # Bottom accent bar
    add_rect(slide, Inches(0.8), Inches(4.5), Inches(3), Inches(0.06), ACCENT_BLUE)
    add_bottom_bar(slide)

# ============================================================
# CREATE PRESENTATION
# ============================================================
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # blank

# ============================================================
# SLIDE 1: COVER
# ============================================================
slide = prs.slides.add_slide(blank_layout)
set_slide_bg(slide, WHITE)
# Full bg accent
add_rect(slide, Inches(0), Inches(0), Inches(13.33), Inches(3.2), BLUE_FROST)
# Title
add_textbox(slide, Inches(0.8), Inches(1.0), Inches(11.5), Inches(1.2),
            "AI Agent 深度培训手册", font_size=44, color=ACCENT_DARK, bold=True)
# Subtitle
add_textbox(slide, Inches(0.8), Inches(2.2), Inches(11.5), Inches(0.6),
            "大模型 · Agent 框架 · AI 工作台 · 场景配置指南", font_size=22, color=ACCENT_BLUE)
# Author info
add_textbox(slide, Inches(0.8), Inches(3.8), Inches(5), Inches(0.4),
            "研墨 ResearchInk  ·  2026-05-22", font_size=14, color=TEXT_MUTED)
# Bottom decorative line
add_rect(slide, Inches(0.8), Inches(4.5), Inches(4), Inches(0.04), ACCENT_TEAL)
# Tags
tags = ["#LLM", "#Agent", "#RAG", "#OpenClaw", "#AI工作台"]
txb = add_textbox(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.4),
                  "  ".join(tags), font_size=13, color=TEXT_SECONDARY)

# ============================================================
# SLIDE 2: Chapter 1 - LLM & Agent Basics (Section Divider)
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_section_divider(slide, 1, "大模型与 AI Agent 基础知识", "Agent = LLM + Planning + Tool Use + Memory")

# ============================================================
# SLIDE 3: Agent Core Formula
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "Agent 核心公式与自主度分级")
subtitle = "Agent = LLM（大脑）+ Planning（规划）+ Tool Use（工具）+ Memory（记忆）"
add_textbox(slide, Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.35),
            subtitle, font_size=15, color=ACCENT_BLUE, bold=True)

# Four quadrant cards
card_w = Inches(2.6)
card_h = Inches(1.6)
card_y = Inches(1.9)
gap = Inches(0.25)
start_x = Inches(0.6)

quads = [
    ("🧠 LLM (大脑)", "核心推理引擎\n理解意图·拆解任务\n生成回复", BLUE_FROST),
    ("📋 Planning (规划)", "复杂目标拆解\nReAct/Plan-and-Execute\nTree-of-Thought", MINT),
    ("🔧 Tool Use (工具)", "调用外部API/搜索\n计算器/代码执行\nFunction Calling/MCP", LAVENDER),
    ("💾 Memory (记忆)", "短期记忆(对话)\n长期记忆(知识库)\n向量数据库检索", BLUE_LIGHT),
]

for i, (title, desc, color) in enumerate(quads):
    x = start_x + i * (card_w + gap)
    card = add_rounded_rect(slide, x, card_y, card_w, card_h, color)
    add_textbox(slide, x + Inches(0.15), card_y + Inches(0.1), card_w - Inches(0.3), Inches(0.35),
                title, font_size=14, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.18), card_y + Inches(0.5), card_w - Inches(0.35), Inches(1.0),
                desc, font_size=11, color=TEXT_SECONDARY)

# Agent autonomy levels
add_textbox(slide, Inches(0.8), Inches(3.8), Inches(5), Inches(0.3),
            "Agent 自主度分级", font_size=16, color=ACCENT_DARK, bold=True)

# Level diagram
levels = [("L0", "无 Agent", "单轮问答", "#e5f1ff"),
          ("L1", "工具调用", "LLM+Function\nCalling", "#ecf2fe"),
          ("L2", "自主 Agent", "多步规划\n循环执行", "#e8fbf5"),
          ("L3", "多 Agent", "专业分工\n协同工作", "#eff1fe"),
          ("L4", "自进化", "从经验学习\n自我改进", "#eef5ff")]

for i, (level, name, desc, color) in enumerate(levels):
    x = start_x + i * (Inches(2.3) + Inches(0.1))
    y = Inches(4.2)
    card = add_rounded_rect(slide, x, y, Inches(2.3), Inches(1.0), RGBColor.from_string(color[1:]))
    add_textbox(slide, x + Inches(0.1), y + Inches(0.05), Inches(0.5), Inches(0.3),
                level, font_size=13, color=ACCENT_BLUE, bold=True)
    add_textbox(slide, x + Inches(0.5), y + Inches(0.05), Inches(1.6), Inches(0.3),
                name, font_size=13, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.1), y + Inches(0.35), Inches(2.0), Inches(0.5),
                desc, font_size=10, color=TEXT_SECONDARY)

# Arrow progression
for i in range(len(levels)-1):
    x1 = start_x + (i+1) * (Inches(2.3) + Inches(0.1)) - Inches(0.15)
    add_textbox(slide, x1, Inches(4.3), Inches(0.3), Inches(0.3),
                "→", font_size=16, color=ACCENT_BLUE, bold=True)

add_bottom_bar(slide)

# ============================================================
# SLIDE 4: Workflow Patterns
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "Agent 工作流模式", "三种核心推理框架对比")

# Three workflow cards
wf_y = Inches(1.6)
wf_h = Inches(5.0)
wf_w = Inches(3.8)
wf_gap = Inches(0.35)
wf_start = Inches(0.6)

workflows = [
    ("ReAct 模式\n(Reason + Act)", 
     "思考(Thought) → 行动(Action)\n→ 观察(Observation) → 循环",
     "最通用的Agent框架\n适合多数场景",
     BLUE_LIGHT),
    ("Plan-and-Execute",
     "先制定完整计划 →\n逐步执行每一步 →\n检查结果 → 迭代",
     "适合复杂多步骤任务\n需预先规划路径",
     MINT),
    ("Reflection 模式",
     "生成回答 → 自我评估 →\n发现错误/遗漏 →\n修正 → 交付最终版",
     "适合写作/报告/代码审查\n关注输出质量",
     LAVENDER),
]

for i, (title, steps, use, color) in enumerate(workflows):
    x = wf_start + i * (wf_w + wf_gap)
    card = add_rounded_rect(slide, x, wf_y, wf_w, wf_h, color)
    add_textbox(slide, x + Inches(0.2), wf_y + Inches(0.2), wf_w - Inches(0.4), Inches(0.7),
                title, font_size=18, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.25), wf_y + Inches(1.2), wf_w - Inches(0.5), Inches(1.5),
                steps, font_size=12, color=TEXT_SECONDARY)
    add_rect(slide, x + Inches(0.25), wf_y + Inches(2.8), wf_w - Inches(0.5), Inches(0.02), ACCENT_BLUE)
    add_textbox(slide, x + Inches(0.25), wf_y + Inches(3.0), wf_w - Inches(0.5), Inches(1.0),
                f"💡 {use}", font_size=11, color=TEXT_MUTED)

add_bottom_bar(slide)

# ============================================================
# SLIDE 5: Memory System Architecture
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "Agent 记忆系统架构", "短期记忆 · 长期记忆 · 工作记忆三层体系")

# Three-layer architecture diagram
# Working Memory (top)
add_rounded_rect(slide, Inches(1.5), Inches(1.6), Inches(10), Inches(1.2), ACCENT_DARK)
add_textbox(slide, Inches(1.7), Inches(1.65), Inches(4), Inches(0.35),
            "🧠 工作记忆 (Working Memory)", font_size=16, color=WHITE, bold=True)
add_textbox(slide, Inches(1.7), Inches(2.0), Inches(9), Inches(0.5),
            "当前会话上下文 + 从短期/长期记忆中检索到的相关信息", font_size=12, color=RGBColor(0xCC, 0xD5, 0xE8))

# Down arrow
add_textbox(slide, Inches(6.2), Inches(2.85), Inches(1), Inches(0.3),
            "▼", font_size=14, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

# Short-term Memory
add_rounded_rect(slide, Inches(1.5), Inches(3.2), Inches(10), Inches(1.0), BLUE_FROST)
add_textbox(slide, Inches(1.7), Inches(3.25), Inches(4), Inches(0.35),
            "📝 短期记忆 (Short-term)", font_size=16, color=ACCENT_DARK, bold=True)
add_textbox(slide, Inches(1.7), Inches(3.6), Inches(9), Inches(0.4),
            "当前对话历史 · 中间推理结果 · 临时上下文（会话级别，用完即释）", font_size=12, color=TEXT_SECONDARY)

# Down arrow
add_textbox(slide, Inches(6.2), Inches(4.25), Inches(1), Inches(0.3),
            "▼", font_size=14, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

# Long-term Memory - three sub-types
add_rounded_rect(slide, Inches(1.5), Inches(4.6), Inches(10), Inches(0.9), LAVENDER)

ltm_types = [("📌 事实记忆", "用户偏好 · 知识条目"), ("⚙️ 程序记忆", "工作流 · 技能"), ("📅 情景记忆", "历史事件 · 项目状态")]
for i, (title, desc) in enumerate(ltm_types):
    x = Inches(1.8) + i * Inches(3.2)
    add_textbox(slide, x, Inches(4.65), Inches(3), Inches(0.3),
                title, font_size=13, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x, Inches(4.95), Inches(3), Inches(0.3),
                desc, font_size=11, color=TEXT_SECONDARY)

# Bottom: memory tech stack
add_textbox(slide, Inches(0.8), Inches(5.8), Inches(11), Inches(0.3),
            "记忆技术栈", font_size=14, color=ACCENT_DARK, bold=True)

techs = [("向量数据库\nLanceDB/Chroma", BLUE_FROST), ("文件记忆\nMEMORY.md", MINT), 
         ("Hybrid Search\n语义+关键词", LAVENDER), ("梦境系统\n后台自动整合", BLUE_LIGHT)]

for i, (text, color) in enumerate(techs):
    x = Inches(0.8) + i * Inches(3.05)
    card = add_rounded_rect(slide, x, Inches(6.15), Inches(2.8), Inches(0.7), color)
    add_textbox(slide, x + Inches(0.1), Inches(6.18), Inches(2.6), Inches(0.6),
                text, font_size=10, color=TEXT_SECONDARY, alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide)

# ============================================================
# SLIDE 6: RAG Flow
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "RAG 检索增强生成流程", "外部知识检索 + LLM 生成结合，解决幻觉和知识截止")

steps = [
    ("① 查询向量化", "用户问题 → 文本嵌入\n转为语义向量", BLUE_FROST),
    ("② 检索文档", "向量数据库搜索\n返回 Top-K 相似内容", MINT),
    ("③ 重排序", "精排检索结果\n提高上下文相关性", LAVENDER),
    ("④ Prompt 拼接", "用户问题 + 检索文档\n+ 系统指令 → LLM", BLUE_LIGHT),
    ("⑤ 生成回答", "LLM 基于检索内容\n生成+来源引用", E8_FBF5 := RGBColor(216, 251, 245)),
]

for i, (title, desc, color) in enumerate(steps):
    x = Inches(0.5) + i * Inches(2.5)
    card = add_rounded_rect(slide, x, Inches(1.8), Inches(2.2), Inches(1.5), color)
    add_textbox(slide, x + Inches(0.12), Inches(1.85), Inches(1.9), Inches(0.3),
                title, font_size=13, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.12), Inches(2.2), Inches(1.9), Inches(0.8),
                desc, font_size=11, color=TEXT_SECONDARY)
    # Arrow between steps
    if i < len(steps) - 1:
        add_textbox(slide, x + Inches(2.25), Inches(2.3), Inches(0.3), Inches(0.3),
                    "→", font_size=18, color=ACCENT_BLUE, bold=True)

# RAG Components
add_textbox(slide, Inches(0.8), Inches(3.6), Inches(5), Inches(0.3),
            "关键组件", font_size=15, color=ACCENT_DARK, bold=True)

components = [
    ("文档切分", "Chunking"),
    ("向量嵌入", "Embedding"),
    ("向量数据库", "Vector DB"),
    ("重排序", "Reranking"),
    ("混合检索", "Hybrid"),
]
for i, (name, eng) in enumerate(components):
    x = Inches(0.8) + i * Inches(2.35)
    card = add_rounded_rect(slide, x, Inches(3.95), Inches(2.1), Inches(0.8), BLUE_FROST)
    add_textbox(slide, x + Inches(0.1), Inches(3.98), Inches(1.9), Inches(0.3),
                name, font_size=12, color=ACCENT_DARK, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, x + Inches(0.1), Inches(4.25), Inches(1.9), Inches(0.3),
                eng, font_size=10, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

# RAG evolution
add_textbox(slide, Inches(0.8), Inches(5.1), Inches(5), Inches(0.3),
            "RAG 演进路线", font_size=15, color=ACCENT_DARK, bold=True)

evos = [("朴素 RAG", "单次检索+生成"), ("Agentic RAG", "自主决定检索时机"), ("Graph RAG", "知识图谱检索"),
        ("Multi-hop", "多步链条检索"), ("自查询 RAG", "LLM自动生成查询")]
for i, (name, desc) in enumerate(evos):
    x = Inches(0.8) + i * Inches(2.35)
    card = add_rounded_rect(slide, x, Inches(5.45), Inches(2.1), Inches(0.7), LAVENDER)
    add_textbox(slide, x + Inches(0.1), Inches(5.48), Inches(1.9), Inches(0.25),
                name, font_size=12, color=ACCENT_DARK, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, x + Inches(0.1), Inches(5.73), Inches(1.9), Inches(0.3),
                desc, font_size=10, color=TEXT_SECONDARY, alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide)

# ============================================================
# SLIDE 7: Skill Layering + MCP
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "Agent 技能分层架构与 MCP 协议", "从基础工具到复合技能的标准接口")

# Four-layer pyramid (inverted)
layers = [
    ("复合技能层", "行业研究 · 客户画像 · PPT 自动生成\n组合多个工具完成复杂任务", Inches(4.5), E8_FBF5, ACCENT_DARK),
    ("专业工具层", "知识库检索 · 文档处理 · 数据分析\n调用专业 API 执行领域任务", Inches(3.0), MINT, TEXT_PRIMARY),
    ("基础工具层", "网页搜索 · 文件读写 · 代码执行\n通用能力，所有 Agent 共享", Inches(1.8), BLUE_FROST, TEXT_PRIMARY),
    ("MCP 协议层", "Model Context Protocol\nAgent-工具之间的标准化接口", Inches(0.7), LAVENDER, TEXT_MUTED),
]

for i, (name, desc, height, color, text_color) in enumerate(layers):
    y_pos = Inches(1.5) + sum([
        Inches([4.5, 3.0, 1.8, 0.7][j]) + Inches(0.08) for j in range(i)
    ])
    w = Inches(11)
    h = height
    x = Inches(1.15)
    card = add_rounded_rect(slide, x, y_pos, w, h, color)
    add_textbox(slide, x + Inches(0.2), y_pos + Inches(0.1), Inches(5), Inches(0.3),
                name, font_size=15, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.2), y_pos + Inches(0.42), Inches(10), Inches(0.4),
                desc, font_size=11, color=text_color)

# MCP details
add_textbox(slide, Inches(0.8), Inches(5.2), Inches(5), Inches(0.3),
            "MCP（Model Context Protocol）", font_size=15, color=ACCENT_DARK, bold=True)

mcp_cols = [("MCP Server", "暴露工具的模块\n如文件系统/数据库/日历\n→ 工具提供方", BLUE_FROST),
            ("MCP Client", "使用工具的 AI Agent\n动态发现和调用工具\n→ 工具消费方", MINT),
            ("OpenClaw 实现", "双重角色：serve 暴露渠道\nlist/set 管理外部 MCP\n→ 桥接 Gateway", LAVENDER)]

for i, (name, desc, color) in enumerate(mcp_cols):
    x = Inches(0.8) + i * Inches(4.0)
    card = add_rounded_rect(slide, x, Inches(5.55), Inches(3.7), Inches(1.1), color)
    add_textbox(slide, x + Inches(0.15), Inches(5.6), Inches(3.4), Inches(0.25),
                name, font_size=13, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.15), Inches(5.88), Inches(3.4), Inches(0.6),
                desc, font_size=10, color=TEXT_SECONDARY)

add_bottom_bar(slide)

# ============================================================
# SLIDE 8: Multi-Agent Patterns
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "Multi-Agent 协作模式", "多个 AI 各司其职，协同完成复杂任务")

patterns = [
    ("🎯 主-从模式", "主 Agent → 子 Agent 1\n主 Agent → 子 Agent 2\n一个中枢调度多个专家", BLUE_FROST),
    ("👥 团队模式", "研究员 + 写作者 + 审核\n多角色协同，各司其职\n类似真人的项目团队", MINT),
    ("🔗 流水线模式", "Agent A → B → C → D\n串行处理，各负责一环\n上一个的输出是下一个的输入", LAVENDER),
    ("🏆 竞争模式", "Agent A → 方案 A\nAgent B → 方案 B\n多条路径求解，择优输出", BLUE_LIGHT),
]

for i, (title, desc, color) in enumerate(patterns):
    x = Inches(0.5) + i * Inches(3.1)
    card = add_rounded_rect(slide, x, Inches(1.7), Inches(2.85), Inches(2.5), color)
    add_textbox(slide, x + Inches(0.15), Inches(1.75), Inches(2.5), Inches(0.35),
                title, font_size=14, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.15), Inches(2.2), Inches(2.5), Inches(1.5),
                desc, font_size=11, color=TEXT_SECONDARY)

# Representative platforms
add_textbox(slide, Inches(0.8), Inches(4.5), Inches(5), Inches(0.3),
            "代表平台", font_size=15, color=ACCENT_DARK, bold=True)

platforms = [
    ("OpenClaw\nSub-agents", "主-从", BLUE_FROST),
    ("CrewAI\nLangGraph", "团队/流水线", MINT),
    ("MetaGPT\nAutoGen", "团队/竞争", LAVENDER),
]

for i, (name, mode, color) in enumerate(platforms):
    x = Inches(0.8) + i * Inches(4.0)
    card = add_rounded_rect(slide, x, Inches(4.85), Inches(3.7), Inches(1.0), color)
    add_textbox(slide, x + Inches(0.15), Inches(4.88), Inches(2), Inches(0.5),
                name, font_size=12, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(2.5), Inches(4.88), Inches(1), Inches(0.5),
                f"模式: {mode}", font_size=11, color=ACCENT_BLUE)
    add_textbox(slide, x + Inches(0.15), Inches(5.35), Inches(3.5), Inches(0.3),
                f"· {['一个主Agent调度多个子Agent，适合任务分发', '多角色协作完成项目，适合文档/研究任务', '多方案并行输出，择优选择'][i]}",
                font_size=10, color=TEXT_MUTED)

add_bottom_bar(slide)

# ============================================================
# SLIDE 9: Chapter 2 - Global & Chinese LLMs
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_section_divider(slide, 2, "全球与中国主流大模型", "基于 LMSYS Arena / MMLU / OpenCompass 权威排名")

# ============================================================
# SLIDE 10: Global LLM Rankings
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "全球 Top 大模型排行榜", "LMSYS Chatbot Arena Elo 排名（2026年5月）")

# Header row
add_rounded_rect(slide, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.45), ACCENT_DARK)
headers = [("排名", Inches(0.2)), ("模型", Inches(0.5)), ("公司", Inches(0.7)), ("定位与特长", Inches(1.5)), ("开源", Inches(0.4))]
col_starts = [Inches(0.7), Inches(1.8), Inches(4.8), Inches(6.8), Inches(11.5)]
col_widths = [Inches(0.8), Inches(2.8), Inches(1.8), Inches(4.5), Inches(1.0)]
for i, (txt, _) in enumerate(headers):
    if i == 0:
        add_textbox(slide, Inches(0.7), Inches(1.52), Inches(0.8), Inches(0.35),
                    txt, font_size=12, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    else:
        add_textbox(slide, col_starts[i], Inches(1.52), col_widths[i], Inches(0.35),
                    txt, font_size=12, color=WHITE, bold=True)

# Data rows
models_data = [
    ("🥇 1", "GPT-5.5", "OpenAI", "综合能力最强，多模态领先", "❌"),
    ("🥇 2", "Claude Opus 4.7", "Anthropic", "推理深度最强，代码/长文极强", "❌"),
    ("🥇 3", "Gemini 3 Pro", "Google", "多模态最强，超长上下文", "❌"),
    ("🥇 4", "DeepSeek V4", "深度求索", "开源标杆，性价比之王", "✅"),
    ("🥈 5", "Grok 4", "xAI", "实时社交数据，风格独特", "❌"),
    ("🥈 6", "Llama 4", "Meta", "最强开源基础模型，社区最丰富", "✅"),
    ("🥉 7", "Qwen 3 系列", "阿里巴巴", "多语言突出，中文能力顶尖", "✅"),
    ("🥉 8", "GLM-5", "智谱AI", "中英双语，学术背景", "✅"),
    ("🥉 9", "Kimi K2.5", "月之暗面", "超长上下文（2M tokens）", "❌"),
    ("🥉 10", "ERNIE 5.0", "百度", "中文知识理解，搜索生态", "❌"),
]

for i, (rank, model, company, desc, oss) in enumerate(models_data):
    y = Inches(2.0) + i * Inches(0.48)
    bg = WHITE if i % 2 == 0 else BLUE_FROST
    card = add_rounded_rect(slide, Inches(0.5), y, Inches(12.3), Inches(0.45), bg)
    
    idx = 0
    for val in [rank, model, company, desc, oss]:
        add_textbox(slide, col_starts[idx], y + Inches(0.05), col_widths[idx], Inches(0.35),
                    str(val), font_size=10, color=TEXT_PRIMARY if idx != 0 else ACCENT_BLUE,
                    bold=(idx == 0 or idx == 1))
        idx += 1

add_textbox(slide, Inches(0.8), Inches(7.0), Inches(11), Inches(0.3),
            "数据来源: LMSYS Chatbot Arena · MMLU-Pro · OpenCompass · Artificial Analysis", 
            font_size=9, color=TEXT_MUTED)

# ============================================================
# SLIDE 11: Chinese LLMs
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "中国主流大模型全景", "综合能力 · 开源度 · 价格 · 场景适应性")

# Cards for each model
models_cn = [
    ("DeepSeek V4", "深度求索", "开源✅", "推理/数学/代码\n全球开源第一", BLUE_FROST),
    ("Qwen 3", "阿里巴巴", "开源✅", "多语言全系列\n0.5B ~ 70B+", MINT),
    ("GLM-5", "智谱AI", "开源✅", "中英双语\n学术研究/AI Agent", LAVENDER),
    ("Kimi K2.5", "月之暗面", "闭源", "超长上下文\n2M tokens", BLUE_LIGHT),
]

for i, (name, company, oss, desc, color) in enumerate(models_cn):
    x = Inches(0.5) + i * Inches(3.1)
    card = add_rounded_rect(slide, x, Inches(1.6), Inches(2.85), Inches(2.2), color)
    add_textbox(slide, x + Inches(0.15), Inches(1.65), Inches(2.5), Inches(0.35),
                name, font_size=16, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.15), Inches(2.0), Inches(2.5), Inches(0.25),
                f"{company}  |  {oss}", font_size=10, color=TEXT_MUTED)
    add_textbox(slide, x + Inches(0.15), Inches(2.4), Inches(2.5), Inches(0.8),
                desc, font_size=11, color=TEXT_SECONDARY)

# More models list
add_textbox(slide, Inches(0.8), Inches(4.1), Inches(5), Inches(0.3),
            "更多中国大模型", font_size=15, color=ACCENT_DARK, bold=True)

more_models = [
    ("ERNIE 5.0 / 文心一言", "百度", "中文知识/搜索生态"),
    ("讯飞星火 5.0", "科大讯飞", "语音/教育场景"),
    ("MiniMax M2.1", "MiniMax", "语音合成/AI陪伴"),
    ("Baichuan 3", "百川智能", "医疗/法律垂直"),
    ("豆包大模型", "字节跳动", "C端用户量最大"),
]

for i, (name, company, desc) in enumerate(more_models):
    x = Inches(0.5) + (i % 3) * Inches(4.1)
    y = Inches(4.5) + (i // 3) * Inches(0.85)
    card = add_rounded_rect(slide, x, y, Inches(3.85), Inches(0.75), LAVENDER)
    add_textbox(slide, x + Inches(0.12), y + Inches(0.05), Inches(2.2), Inches(0.3),
                name, font_size=12, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(2.3), y + Inches(0.05), Inches(1.4), Inches(0.3),
                company, font_size=10, color=TEXT_MUTED)
    add_textbox(slide, x + Inches(0.12), y + Inches(0.35), Inches(3.5), Inches(0.3),
                desc, font_size=10, color=TEXT_SECONDARY)

add_bottom_bar(slide)

# ============================================================
# SLIDE 12: Model Selection Guide
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "模型选择指南", "按场景与成本选择最佳模型")

# Two-column layout
# Left: By Scenario
add_textbox(slide, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.3),
            "按场景选择", font_size=17, color=ACCENT_DARK, bold=True)

scenarios = [
    ("行业研究/深度分析", "DeepSeek V4 Pro / Claude Opus"),
    ("PPT 制作/报告撰写", "DeepSeek V4 / Claude Sonnet"),
    ("编程开发", "Claude Sonnet/Opus / GPT-5.x"),
    ("多模态分析", "Gemini 3 Pro / GPT-5.x"),
    ("超长文档处理", "Kimi K2.5 / Gemini 3"),
    ("中文内容创作", "Qwen 3 / DeepSeek V4"),
    ("高并发低预算", "DeepSeek V4 Flash"),
    ("企业私有化部署", "Llama 4 / Qwen 3"),
]

for i, (scene, model) in enumerate(scenarios):
    y = Inches(1.9) + i * Inches(0.55)
    bg = WHITE if i % 2 == 0 else BLUE_FROST
    card = add_rounded_rect(slide, Inches(0.5), y, Inches(5.8), Inches(0.5), bg)
    add_textbox(slide, Inches(0.7), y + Inches(0.05), Inches(2.8), Inches(0.35),
                scene, font_size=11, color=TEXT_PRIMARY, bold=True)
    add_textbox(slide, Inches(3.5), y + Inches(0.05), Inches(2.6), Inches(0.35),
                f"→ {model}", font_size=10, color=ACCENT_BLUE)

# Right: Cost Spectrum
add_textbox(slide, Inches(7.0), Inches(1.5), Inches(5.5), Inches(0.3),
            "按成本选择", font_size=17, color=ACCENT_DARK, bold=True)

# Cost bar
cost_bar_y = Inches(2.0)
bar_colors = [("DeepSeek V4", "💰 最低", RGBColor(0x5B, 0xBF, 0xA0), Inches(1.5)),
              ("Qwen 3", "💰 低", RGBColor(0x7D, 0xCF, 0xB0), Inches(1.0)),
              ("Claude Sonnet", "💰 中", RGBColor(0x6B, 0x9D, 0xD8), Inches(0.8)),
              ("GPT-5", "💰 高", ACCENT_BLUE, Inches(0.6)),
              ("Claude Opus", "💰 最高", ACCENT_DARK, Inches(0.4))]

y_pos = cost_bar_y
for name, cost, color, height in bar_colors:
    y_pos += Inches(0.05)
    card = add_rounded_rect(slide, Inches(7.0), y_pos, Inches(5.5), Inches(0.65), LAVENDER)
    add_textbox(slide, Inches(7.15), y_pos + Inches(0.02), Inches(2.5), Inches(0.35),
                f"{name}", font_size=12, color=ACCENT_DARK, bold=True)
    add_textbox(slide, Inches(7.15), y_pos + Inches(0.32), Inches(2.5), Inches(0.25),
                cost, font_size=10, color=TEXT_MUTED)
    # Bar indicator
    bar = add_rounded_rect(slide, Inches(9.8), y_pos + Inches(0.12), Inches(2.5), Inches(0.4), color)
    y_pos += Inches(0.7)

# Key takeaway
add_rounded_rect(slide, Inches(0.5), Inches(6.4), Inches(12.3), Inches(0.55), MINT)
add_textbox(slide, Inches(0.7), Inches(6.43), Inches(11.8), Inches(0.45),
            "💡 策略：日常用 DeepSeek V4 Flash（极低成本），深度研究切 DeepSeek V4 Pro，关键交付物用 Claude Opus / GPT-5 把关质量",
            font_size=12, color=TEXT_PRIMARY)

add_bottom_bar(slide)

# ============================================================
# SLIDE 13: Chapter 3 - AI Workbenches
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_section_divider(slide, 3, "全球与中国 AI 工作台对比", "让大模型能执行任务的 Agent 平台 / 工具")

# ============================================================
# SLIDE 14: Global Top 5 Workbenches
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "全球 Top 5 AI 工作台", "按社区认可度 + 行业影响力综合排名")

wb_global = [
    ("🥇 OpenClaw", "374K ⭐ GitHub", "自托管 AI Agent 网关\n多渠道 · 持久化 Agent\nTaskFlow · Sub-agents", BLUE_FROST),
    ("🥈 ChatGPT Codex", "闭源 · OpenAI", "云端原生 Agent 运行时\n深度代码理解\nGPT-5.x 最强模型", MINT),
    ("🥉 Claude Code", "闭源 · Anthropic", "终端原生 CLI Agent\nMCP 协议发起者\n自主 Agent 能力最强", LAVENDER),
    ("④ AutoGPT", "184K ⭐", "Agent 概念先驱\n自主目标分解\n互联网操作能力", BLUE_LIGHT),
    ("⑤ Dify", "142K ⭐", "可视化 Agent 编排\nRAG 引擎 · 知识库\n增长最快平台", WHITE),
]

for i, (name, badge, desc, color) in enumerate(wb_global):
    x = Inches(0.3) + i * Inches(2.55)
    card = add_rounded_rect(slide, x, Inches(1.6), Inches(2.35), Inches(3.2), color if color != WHITE else LAVENDER)
    add_textbox(slide, x + Inches(0.12), Inches(1.65), Inches(2.1), Inches(0.35),
                name, font_size=15, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.12), Inches(2.0), Inches(2.1), Inches(0.25),
                badge, font_size=9, color=TEXT_MUTED)
    add_rect(slide, x + Inches(0.15), Inches(2.3), Inches(1.9), Inches(0.015), ACCENT_BLUE)
    add_textbox(slide, x + Inches(0.12), Inches(2.4), Inches(2.1), Inches(1.5),
                desc, font_size=10, color=TEXT_SECONDARY)

# Quick comparison text
add_textbox(slide, Inches(0.8), Inches(5.1), Inches(11), Inches(0.3),
            "趋势：纯框架（LangChain）增长放缓，低代码平台（Dify）和 Agent 网关（OpenClaw）成为主流",
            font_size=12, color=ACCENT_BLUE, bold=True)

add_bottom_bar(slide)

# ============================================================
# SLIDE 15: China Top 5 Workbenches
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "中国 Top 5 AI 工作台", "从编码助手到 Agent 平台，大厂生态各据一方")

wb_cn = [
    ("🥇 Dify", "langgenius\n142K ⭐", "全球化最成功的中国 AI 项目\n低代码 Agent + RAG 引擎\n企业级应用模板", BLUE_FROST),
    ("🥈 Coze (扣子)", "字节跳动", "中国市场 Bot 构建第一平台\n零代码 Agent 编排\n多渠道发布(微信/飞书)", MINT),
    ("🥉 通义灵码", "阿里巴巴", "Gartner 挑战者象限（唯一中国厂商）\n编程智能体 · 200+语言\n阿里云深度集成", LAVENDER),
    ("④ 百度超级助理", "百度", "AI 办公助手 · 企业知识库\n文心 ERNIE 驱动\n搜索生态优势", BLUE_LIGHT),
    ("⑤ 腾讯 WorkBuddy", "腾讯", "桌面级智能体工作台\n企业微信/会议/文档打通\nRPA + AI Agent", WHITE),
]

for i, (name, source, desc, color) in enumerate(wb_cn):
    x = Inches(0.3) + i * Inches(2.55)
    bg_color = color if color != WHITE else LAVENDER
    card = add_rounded_rect(slide, x, Inches(1.6), Inches(2.35), Inches(3.3), bg_color)
    add_textbox(slide, x + Inches(0.12), Inches(1.65), Inches(2.1), Inches(0.35),
                name, font_size=15, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.12), Inches(2.0), Inches(2.1), Inches(0.3),
                source, font_size=9, color=TEXT_MUTED)
    add_rect(slide, x + Inches(0.15), Inches(2.35), Inches(1.9), Inches(0.015), ACCENT_BLUE)
    add_textbox(slide, x + Inches(0.12), Inches(2.45), Inches(2.1), Inches(1.8),
                desc, font_size=10, color=TEXT_SECONDARY)

add_textbox(slide, Inches(0.8), Inches(5.2), Inches(11), Inches(0.3),
            "特点：中国平台「垂直切割」明显——编码类/办公类/Bot 类各有霸主，各自绑定大厂生态",
            font_size=12, color=ACCENT_BLUE, bold=True)

add_bottom_bar(slide)

# ============================================================
# SLIDE 16: Core Comparison Matrix
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "AI 工作台核心差异对比")

# Matrix header
headers = ["维度", "OpenClaw", "Dify", "Coze", "Claude Code"]
col_x = [Inches(0.5), Inches(3.0), Inches(5.5), Inches(8.0), Inches(10.5)]
col_w = [Inches(2.3), Inches(2.3), Inches(2.3), Inches(2.3), Inches(2.3)]

# Header row
add_rounded_rect(slide, Inches(0.5), Inches(1.5), Inches(12.3), Inches(0.45), ACCENT_DARK)
for i, h in enumerate(headers):
    add_textbox(slide, col_x[i] + Inches(0.1), Inches(1.52), col_w[i], Inches(0.35),
                h, font_size=11, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# Data rows
rows = [
    ["形态", "守护进程+CLI", "Web应用", "网页+API", "终端 CLI"],
    ["目标用户", "知识工作者+开发者", "非技术+技术团队", "非技术人员", "专业开发者"],
    ["Agent 模式", "ReAct + 持久化", "可视化编排", "可视化编排", "CLI 自主 Agent"],
    ["记忆系统", "✅ 自进化记忆", "✅ 知识库 RAG", "✅ 知识库", "✅ 项目记忆"],
    ["多渠道输出", "✅ 25+ 渠道", "✅ API/Web", "✅ 微信/飞书", "❌ 仅终端"],
    ["持久任务", "✅ Cron/TaskFlow", "✅ 后台", "❌", "❌"],
    ["易用性", "中（需配置）", "高（拖拽）", "高", "低（需 CLI）"],
    ["自定义深度", "极高", "高", "中", "高"],
]

for i, row in enumerate(rows):
    y = Inches(2.0) + i * Inches(0.55)
    bg = WHITE if i % 2 == 0 else BLUE_FROST
    add_rounded_rect(slide, Inches(0.5), y, Inches(12.3), Inches(0.5), bg)
    for j, val in enumerate(row):
        is_bold = (j == 0)
        c = ACCENT_DARK if is_bold else TEXT_PRIMARY
        add_textbox(slide, col_x[j] + Inches(0.08), y + Inches(0.05), col_w[j] - Inches(0.1), Inches(0.35),
                    val, font_size=9, color=c, bold=is_bold, alignment=PP_ALIGN.CENTER)

add_bottom_bar(slide)

# ============================================================
# SLIDE 17: Chapter 4 - OpenClaw & Hermes
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_section_divider(slide, 4, "OpenClaw 与 Hermes 详解", "自托管 AI Agent 网关 · 持久化 Agent 工作台")

# ============================================================
# SLIDE 18: OpenClaw System Architecture
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "OpenClaw 系统架构", "Gateway → Provider → Agent Runtime → Channels 四层结构")

# Architecture layers - top down
arch_layers = [
    ("Gateway 守护进程", "单进程长驻 · WebSocket 通信 · Canvas 可视化 · 热重载", ACCENT_DARK, WHITE),
    ("Provider 模型层", "35+ 内置 Provider · 模型故障转移链 · Auth Profile 轮转 · Runtime 分离", BLUE_LIGHT, TEXT_PRIMARY),
    ("Agent 运行时 (PI Core)", "Agent 循环 · 会话管理 · 记忆引擎 · 技能加载 · 上下文构建器", BLUE_FROST, TEXT_PRIMARY),
    ("自动化与编排层", "Cron 调度 · TaskFlow 工作流 · Sub-agents 并行 · Heartbeat 心跳", MINT, TEXT_PRIMARY),
    ("渠道层 (25+ 渠道)", "微信 · Telegram · Slack · Discord · Signal · WhatsApp · iMessage …", LAVENDER, TEXT_PRIMARY),
]

y_pos = Inches(1.5)
for name, desc, bg_color, text_color in arch_layers:
    card = add_rounded_rect(slide, Inches(1.0), y_pos, Inches(11.3), Inches(0.85), bg_color)
    add_textbox(slide, Inches(1.2), y_pos + Inches(0.08), Inches(4), Inches(0.35),
                name, font_size=15, color=text_color if text_color != WHITE else WHITE, bold=True)
    add_textbox(slide, Inches(1.2), y_pos + Inches(0.42), Inches(11), Inches(0.35),
                desc, font_size=10, color=text_color if text_color != WHITE else RGBColor(0xCC, 0xD5, 0xE8))
    # Down arrow between layers
    if y_pos < Inches(6.0):
        add_textbox(slide, Inches(6.2), y_pos + Inches(0.88), Inches(1), Inches(0.2),
                    "▼", font_size=10, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)
    y_pos += Inches(1.0)

# Right side: key features
add_textbox(slide, Inches(0.8), Inches(6.0), Inches(5), Inches(0.3),
            "独特能力", font_size=14, color=ACCENT_DARK, bold=True)

features = ["持久化 Agent（业界独有）", "Cron 定时任务触发", "自进化记忆系统", "MCP Server + Client 双角色", "完全开源 (MIT)"]
for i, f in enumerate(features):
    x = Inches(0.8) + (i % 3) * Inches(4.0)
    y = Inches(6.35) + (i // 3) * Inches(0.35)
    add_textbox(slide, x, y, Inches(3.8), Inches(0.3),
                f"✓ {f}", font_size=10, color=ACCENT_TEAL)

add_bottom_bar(slide)

# ============================================================
# SLIDE 19: Industry Scenario Configuration
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_slide_title(slide, "行业场景配置指南", "行业研究 · 客户研究 · 解决方案 · PPT 制作")

# Four scenario cards
scenarios = [
    ("📊 行业研究", 
     "模型: DeepSeek V4 Flash/Pro\n框架: 十层深度分析体系\n技能: web-search, web-fetch\n并行: sessions_spawn 研究子任务",
     BLUE_FROST),
    ("🎯 客户研究",
     "模型: DeepSeek V4 Flash\n框架: 四层客户画像\n技能: web-search + opencli\n记忆: 写入 client-xxx.md",
     MINT),
    ("🔧 解决方案",
     "模型: DeepSeek V4 Pro\n流程: 需求→方案→选型→估算→路线图\n输出: 分层版本(投资层/技术层)\n参考: solutions/ 模板库",
     LAVENDER),
    ("📑 PPT 制作",
     "默认技能: pptx-master / ppt-master\n风格: 清新科技风 / 现代品牌风\n流程: 骨架→填充→视觉→QA\n输出: HTML / PPTX 双格式",
     BLUE_LIGHT),
]

for i, (title, content, color) in enumerate(scenarios):
    x = Inches(0.4) + i * Inches(3.15)
    card = add_rounded_rect(slide, x, Inches(1.6), Inches(2.95), Inches(3.2), color)
    add_textbox(slide, x + Inches(0.15), Inches(1.65), Inches(2.6), Inches(0.4),
                title, font_size=16, color=ACCENT_DARK, bold=True)
    add_textbox(slide, x + Inches(0.15), Inches(2.15), Inches(2.6), Inches(2.5),
                content, font_size=10, color=TEXT_SECONDARY)

# Quick config checklist
add_textbox(slide, Inches(0.8), Inches(5.1), Inches(5), Inches(0.3),
            "快速配置清单", font_size=15, color=ACCENT_DARK, bold=True)

checklist = [
    "1. 明确研究范围 / 目标受众 / 核心问题",
    "2. 裁剪研究框架 → 输出 Outline（需确认）",
    "3. 并行搜索多角度覆盖",
    "4. MECE 结构化整理 + 交叉验证",
    "5. 输出前做质量检查（来源可追溯 + 逻辑完整）",
]

for i, item in enumerate(checklist):
    y = Inches(5.45) + i * Inches(0.3)
    add_textbox(slide, Inches(0.8), y, Inches(11), Inches(0.28),
                item, font_size=10, color=TEXT_SECONDARY)

# Model config tip
add_rounded_rect(slide, Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.4), MINT)
add_textbox(slide, Inches(0.7), Inches(7.02), Inches(11.8), Inches(0.35),
            "💡 推荐配置: primary = deepseek/deepseek-v4-flash, fallbacks = [deepseek-v4-pro, claude-sonnet-4-5]",
            font_size=11, color=TEXT_PRIMARY)

# ============================================================
# SLIDE 20: Closing
# ============================================================
slide = prs.slides.add_slide(blank_layout)
set_slide_bg(slide, WHITE)

# Top color block
add_rect(slide, Inches(0), Inches(0), Inches(13.33), Inches(3.5), BLUE_FROST)

add_textbox(slide, Inches(0.8), Inches(1.2), Inches(11.5), Inches(1.0),
            "AI Agent 深度培训手册", font_size=36, color=ACCENT_DARK, bold=True)
add_textbox(slide, Inches(0.8), Inches(2.3), Inches(11.5), Inches(0.5),
            "让 AI 成为你的深度研究搭档", font_size=20, color=ACCENT_BLUE)

# Bottom info
add_textbox(slide, Inches(0.8), Inches(4.0), Inches(11.5), Inches(0.5),
            "编制：研墨 ResearchInk", font_size=16, color=TEXT_PRIMARY, bold=True)
add_textbox(slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(0.4),
            "基于 OpenClaw 平台 · 数据截止 2026-05-22", font_size=13, color=TEXT_MUTED)

# Tags
tags_str = "行业研究  ·  客户分析  ·  解决方案  ·  AI Agent  ·  LLM  ·  RAG  ·  MCP"
add_textbox(slide, Inches(0.8), Inches(5.5), Inches(11.5), Inches(0.3),
            tags_str, font_size=11, color=TEXT_SECONDARY)

add_bottom_bar(slide)

# ============================================================
# SAVE
# ============================================================
output_path = "/root/.openclaw/workspace/deliverables/AI Agent深度培训手册_PPT.pptx"
prs.save(output_path)
print(f"✅ PPT saved: {output_path}")

import os
size = os.path.getsize(output_path)
print(f"   Size: {size/1024:.1f} KB")
print(f"   Slides: {len(prs.slides)}")
