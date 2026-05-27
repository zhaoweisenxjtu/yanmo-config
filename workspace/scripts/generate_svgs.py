#!/usr/bin/env python3
"""Generate all 20 SVG slides for AI Agent Training PPT using ppt-master"""
import os, sys

OUT = "/root/.openclaw/workspace/skills/ppt-master/projects/ai-agent-training/output"
os.makedirs(OUT, exist_ok=True)

# === Fresh Tech Color System ===
WHITE = "#FFFFFF"
BLUE_FROST = "#ECF2FE"
BLUE_LIGHT = "#E9F3FF"
BLUE_PALE = "#E5F1FF"
MINT = "#E8FBF5"
MINT_LIGHT = "#E8FBF7"
LAVENDER = "#EFF1FE"
LAVENDER_LIGHT = "#EEF5FF"
HEADER_START = "#F4F8FF"
ACCENT_BLUE = "#4A7BD0"
ACCENT_TEAL = "#5BBFA0"
ACCENT_DARK = "#1A2D4A"
TEXT_PRIMARY = "#1A1F2E"
TEXT_SECONDARY = "#4A5064"
TEXT_MUTED = "#8E93A4"
EDGE_BLUE = "#FAFBFF"

# Brand colors for icons
BRAND_COLORS = {
    "GPT-5.5": "#10A37F", "Claude": "#D97706", "Gemini": "#4285F4",
    "DeepSeek": "#4F46E5", "Grok": "#000000", "Llama": "#0466C8",
    "Qwen": "#FF6A00", "GLM-5": "#8B5CF6", "Kimi": "#F97316",
    "ERNIE": "#2563EB", "OpenClaw": "#E74C3C", "Dify": "#1677FF",
    "Coze": "#E11D48", "AutoGPT": "#7C3AED",
}

def svg_header(title="AI Agent 深度培训手册"):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
<defs>
<style>@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');
text,tspan {{ font-family: 'Noto Sans SC', 'Microsoft YaHei', 'PingFang SC', sans-serif; }}</style>
</defs>'''

def svg_footer():
    return '</svg>'

def rect(x, y, w, h, fill, rx="0"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}" ry="{rx}"/>'

def text(x, y, txt, size="16", color=TEXT_PRIMARY, weight="normal", align="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}px" fill="{color}" font-weight="{weight}" text-anchor="{align}">{txt}</text>'

def top_bar():
    return rect(0, 0, 1280, 40, HEADER_START) + rect(0, 40, 1280, 3, BLUE_FROST)

def bottom_bar():
    return rect(0, 710, 1280, 2, BLUE_FROST)

def slide_title(txt):
    return text(60, 80, txt, "28", ACCENT_DARK, "bold")

def slide_subtitle(txt):
    return text(60, 108, txt, "15", TEXT_MUTED)

def card(x, y, w, h, fill, title, items):
    """Card with title and bullet items"""
    r = fill
    out = rect(x, y, w, h, r, "8")
    out += text(x+18, y+35, title, "17", ACCENT_DARK, "bold")
    for i, item in enumerate(items):
        out += text(x+22, y+60+i*28, f"· {item}", "13", TEXT_SECONDARY)
    return out

def brand_icon_svg(bg_color, label, size=28):
    """SVG circle with initial"""
    r = size//2
    cx, cy = r+2, r+2
    fs = size*0.45
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg_color}"/>' \
           f'<text x="{cx}" y="{cy+fs*0.35}" text-anchor="middle" fill="#FFF" font-size="{fs}px" font-weight="bold">{label}</text>'

# =====================================================
# SLIDE 1: Cover
# =====================================================
svg = svg_header()
svg += rect(0, 0, 1280, 720, WHITE)
svg += rect(0, 0, 1280, 310, HEADER_START)
svg += text(640, 130, "AI Agent 深度培训手册", "44", ACCENT_DARK, "bold", "middle")
svg += text(640, 190, "大模型 · Agent 框架 · AI 工作台 · 场景配置指南", "22", ACCENT_BLUE, "normal", "middle")
svg += text(640, 270, "研墨 ResearchInk  ·  2026-05-22", "15", TEXT_MUTED, "normal", "middle")
svg += rect(540, 290, 200, 4, ACCENT_TEAL)
svg += text(640, 340, "#LLM  #Agent  #RAG  #OpenClaw  #MCP  #AI工作台", "14", TEXT_SECONDARY, "normal", "middle")
svg += svg_footer()
with open(f"{OUT}/slide_01_cover.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 2: Agent Core Formula
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Agent 核心公式与自主度分级")
svg += slide_subtitle("Agent = LLM（大脑）+ Planning（规划）+ Tool Use（工具）+ Memory（记忆）")

quads = [
    (60, 140, BLUE_FROST, "🧠 LLM (大脑)", "核心推理引擎\n理解意图·拆解任务\n生成回复（GPT/Claude/DeepSeek）"),
    (340, 140, MINT, "📋 Planning (规划)", "复杂目标拆解\nReAct/Plan-and-Execute\nTree-of-Thought 推理"),
    (620, 140, LAVENDER, "🔧 Tool Use (工具)", "调用外部API/搜索\n代码执行/MCP协议\nFunction Calling"),
    (900, 140, BLUE_LIGHT, "💾 Memory (记忆)", "短期（对话历史）\n长期（知识库/向量库）\n文件记忆 MEMORY.md"),
]
for x, y, col, title, desc in quads:
    svg += rect(x, y, 260, 150, col, "8")
    svg += text(x+15, y+30, title, "16", ACCENT_DARK, "bold")
    for i, line in enumerate(desc.split("\n")):
        svg += text(x+18, y+55+i*25, f"· {line}", "13", TEXT_SECONDARY)

# L0-L4 levels
svg += text(60, 320, "Agent 自主度分级", "17", ACCENT_DARK, "bold")
levels = [("L0", "无 Agent", "单轮问答", "#E5F1FF"), ("L1", "工具调用", "LLM+FC", "#ECF2FE"),
          ("L2", "自主 Agent", "多步规划", "#E8FBF5"), ("L3", "多 Agent", "分工协作", "#EFF1FE"),
          ("L4", "自进化", "自我改进", "#EEF5FF")]
for i, (lv, nm, desc, col) in enumerate(levels):
    x = 60+i*240
    svg += rect(x, 350, 220, 75, col, "8")
    svg += text(x+12, 375, lv, "14", ACCENT_BLUE, "bold")
    svg += text(x+55, 375, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+12, 400, desc, "11", TEXT_SECONDARY)
    if i < len(levels)-1:
        svg += text(x+228, 373, "→", "16", ACCENT_BLUE, "bold")

# Examples
svg += text(60, 460, "典型代表", "17", ACCENT_DARK, "bold")
ex = [("L1 OpenAI API", "GPT-4 Function Calling", BLUE_FROST),
      ("L2 AutoGPT/OpenClaw", "多步规划循环执行", MINT),
      ("L3 CrewAI/MetaGPT", "多Agent角色协作", LAVENDER),
      ("L4 OpenClaw", "自进化记忆系统", BLUE_LIGHT)]
for i, (nm, desc, col) in enumerate(ex):
    x = 60+i*300
    svg += rect(x, 495, 275, 50, col, "6")
    svg += text(x+12, 518, nm, "13", ACCENT_DARK, "bold")
    svg += text(x+12, 538, desc, "11", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_02_formula.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 3: Workflow Patterns
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Agent 工作流模式")
svg += slide_subtitle("三种核心推理框架的流程对比与适用场景")

for i, (title, steps, tip, col) in enumerate([
    ("ReAct 模式\n(Reason + Act)", "思考(Thought)\n↓\n行动(Action)\n↓\n观察(Observation)\n↓\n循环至终→输出", "最通用框架，适用多数场景", BLUE_LIGHT),
    ("Plan-and-Execute", "制定完整计划\n↓\n逐步执行 Step 1\n↓\n检查结果\n↓\n继续执行 Step 2\n↓\n全部完成 → 输出", "适合复杂多步骤任务", MINT),
    ("Reflection 模式", "生成回答\n↓\n自我评估/批评\n↓\n发现错误/遗漏\n↓\n修正优化\n↓\n交付最终版本", "适合写作/报告审查", LAVENDER),
]):
    x = 50+i*410
    svg += rect(x, 140, 390, 380, col, "10")
    svg += text(x+20, 175, title, "20", ACCENT_DARK, "bold")
    for j, line in enumerate(steps.split("\n")):
        svg += text(x+25, 210+j*35, line, "14", TEXT_SECONDARY)
    svg += rect(x+20, y:=210+len(steps.split("\n"))*35, 350, 2, ACCENT_BLUE) if False else ""
    svg += rect(x+20, 390, 350, 2, ACCENT_BLUE)
    svg += text(x+25, 415, "💡 "+tip, "13", TEXT_MUTED)

# Comparison table at bottom
svg += text(60, 560, "框架对比小结", "17", ACCENT_DARK, "bold")
svg += rect(60, 580, 1160, 30, ACCENT_DARK, "6")
for i, h in enumerate(["框架", "核心思想", "适用场景", "代表实现"]):
    svg += text(80+i*290, 600, h, "13", WHITE, "bold")
rows = [("ReAct", "思考→行动→观察循环", "多数场景通用", "OpenClaw / LangChain / AutoGPT"),
        ("Plan-and-Execute", "先计划后执行", "复杂多步骤任务", "LangGraph / TaskFlow"),
        ("Reflection", "自我评估修正", "写作/报告/代码审查", "OpenClaw / Self-critique")]
for j, (a,b,c,d) in enumerate(rows):
    bg = WHITE if j%2==0 else BLUE_FROST
    svg += rect(60, 610+j*35, 1160, 35, bg, "4")
    for i, val in enumerate([a,b,c,d]):
        svg += text(80+i*290, 632+j*35, val, "12", TEXT_PRIMARY, "bold" if i==0 else "normal")

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_03_workflows.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 4: Memory System
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Agent 记忆系统架构")
svg += slide_subtitle("短期 · 长期 · 工作记忆三层体系 + 技术实现栈")

# Three-layer architecture
svg += rect(200, 145, 880, 110, ACCENT_DARK, "8")
svg += text(220, 175, "🧠 工作记忆 (Working Memory)", "18", WHITE, "bold")
svg += text(220, 210, "当前会话上下文 + 从短期/长期记忆中检索到的相关信息  |  容量：上下文窗口限制", "14", "#CCD5E8")
svg += text(640, 270, "▼", "16", TEXT_MUTED, "normal", "middle")

svg += rect(200, 290, 880, 90, BLUE_FROST, "8")
svg += text(220, 318, "📝 短期记忆 (Short-term Memory)", "17", ACCENT_DARK, "bold")
svg += text(220, 348, "当前对话历史 · 中间推理结果 · 临时上下文（会话级别，用完即释）", "14", TEXT_SECONDARY)
svg += text(640, 395, "▼", "16", TEXT_MUTED, "normal", "middle")

svg += rect(200, 410, 880, 110, LAVENDER, "8")
svg += text(220, 440, "📚 长期记忆 (Long-term Memory) — 持久化跨会话存储", "17", ACCENT_DARK, "bold")
ltm = [("📌 事实记忆", "用户偏好/知识条目"), ("⚙️ 程序记忆", "工作流/技能"), ("📅 情景记忆", "历史事件/项目状态")]
for i, (nm, desc) in enumerate(ltm):
    svg += text(240+i*290, 472, nm, "14", ACCENT_DARK, "bold")
    svg += text(240+i*290, 498, desc, "12", TEXT_SECONDARY)

# Tech stack
svg += text(60, 560, "记忆技术实现栈", "17", ACCENT_DARK, "bold")
techs = [("向量数据库", "LanceDB/Chroma\n语义相似搜索", BLUE_FROST),
         ("文件记忆", "MEMORY.md + memory/\n每日笔记持久化", MINT),
         ("混合检索", "Hybrid Search\n向量+关键词匹配", LAVENDER),
         ("梦境系统", "后台自动整合\n短期→长期提升", BLUE_LIGHT),
         ("上下文窗口", "Compaction 压缩\n控制 Token 消耗", BLUE_PALE)]
for i, (nm, desc, col) in enumerate(techs):
    x = 60+i*234
    svg += rect(x, 595, 220, 80, col, "8")
    svg += text(x+12, 622, nm, "15", ACCENT_DARK, "bold")
    svg += text(x+12, 648, desc.replace("\n", " · "), "11", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_04_memory.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 5: RAG
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("RAG 检索增强生成流程")
svg += slide_subtitle("外部知识 + LLM 生成 = 减少幻觉，突破知识截止")

# 5-step flow
steps = [("① 查询向量化", "用户问题→文本嵌入\n转语义向量查询", BLUE_FROST),
         ("② 检索文档", "向量数据库搜索\n返回 Top-K 相似", MINT),
         ("③ 重排序", "精排检索结果\n提高上下文质量", LAVENDER),
         ("④ Prompt 拼接", "问题+检索文档\n+系统指令→LLM", BLUE_LIGHT),
         ("⑤ 生成回答", "基于检索内容生成\n附带来源引用", "#D8FBF5")]
for i, (nm, desc, col) in enumerate(steps):
    x = 30+i*245
    svg += rect(x, 145, 220, 145, col, "8")
    svg += text(x+12, 170, nm, "15", ACCENT_DARK, "bold")
    svg += text(x+12, 200, desc.replace("\n", " · "), "13", TEXT_SECONDARY)
    if i < len(steps)-1:
        svg += text(x+230, 205, "→", "20", ACCENT_BLUE, "bold")

# Key Components
svg += text(60, 325, "关键组件", "17", ACCENT_DARK, "bold")
comps = [("文档切分", "Chunking", "Recursive\nCharacterSplitter"),
         ("向量嵌入", "Embedding", "OpenAI/BGE/E5\njina-embeddings"),
         ("向量数据库", "Vector DB", "LanceDB/Chroma\nPinecone/Milvus"),
         ("重排序", "Reranking", "Cohere/BGE\nJina Reranker"),
         ("混合检索", "Hybrid Search", "语义+关键词\n中文分词支持")]
for i, (nm, eng, detail) in enumerate(comps):
    x = 60+i*234
    svg += rect(x, 360, 220, 100, BLUE_FROST, "8")
    svg += text(x+12, 385, nm, "15", ACCENT_DARK, "bold")
    svg += text(x+12, 408, eng, "12", TEXT_MUTED)
    svg += text(x+12, 435, detail.replace("\n", " · "), "11", TEXT_SECONDARY)

# Evolution
svg += text(60, 500, "RAG 演进路线", "17", ACCENT_DARK, "bold")
evos = [("朴素 RAG", "单次检索+生成", BLUE_FROST), ("Agentic RAG", "Agent自主决定检索", MINT),
        ("Graph RAG", "知识图谱增强检索", LAVENDER), ("Multi-hop RAG", "多步链条检索", BLUE_LIGHT),
        ("自查询 RAG", "LLM自动生成查询", BLUE_PALE)]
for i, (nm, desc, col) in enumerate(evos):
    x = 60+i*234
    svg += rect(x, 535, 220, 65, col, "8")
    svg += text(x+12, 558, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+12, 582, desc, "11", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_05_rag.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 6: Skills + MCP
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Agent 技能分层架构与 MCP 协议")
svg += slide_subtitle("从基础工具到复合技能，MCP 成为 Agent-工具集成的事实标准")

# Pyramid layers (bottom up)
layers = [("MCP 协议层", "Model Context Protocol — 标准化接口\n被 Cursor/Windsurf/Claude Code/OpenClaw 采用", "#E5F1FF", TEXT_MUTED),
          ("基础工具层", "网页搜索 · 文件读写 · 代码执行\n通用能力，所有 Agent 共享", "#ECF2FE", TEXT_PRIMARY),
          ("专业工具层", "知识库检索 · 文档处理 · 数据分析 · 邮件日历\n调用专业 API 执行领域特定任务", "#E8FBF5", TEXT_PRIMARY),
          ("复合技能层", "行业研究 · 客户画像 · PPT 自动生成\n组合多个工具完成复杂业务任务", "#D8FBF5", ACCENT_DARK)]
for i, (nm, desc, col, tc) in enumerate(layers):
    h = [80, 100, 120, 130][i]
    y_pos = 550 - sum([80, 100, 120, 130][:i+1]) - i*6
    svg += rect(160, y_pos, 960, h, col, "8")
    svg += text(185, y_pos+28, nm, "17", ACCENT_DARK, "bold")
    svg += text(185, y_pos+55, desc.replace("\n", " · "), "13", tc if tc != TEXT_PRIMARY else TEXT_SECONDARY)

# MCP details
svg += text(60, 570, "MCP 双角色实现", "17", ACCENT_DARK, "bold")
mcp_roles = [("MCP Server", "暴露工具给 Agent\n如文件系统/数据库", BLUE_FROST),
             ("MCP Client", "动态发现和调用工具\n消费方", MINT),
             ("OpenClaw 实现", "serve 暴露渠道\nlist/set 管理外部MCP", LAVENDER),
             ("标准协议", "Anthropic 提出\n跨平台互操作", BLUE_LIGHT)]
for i, (nm, desc, col) in enumerate(mcp_roles):
    x = 60+i*295
    svg += rect(x, 605, 275, 65, col, "8")
    svg += text(x+12, 628, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+12, 652, desc.replace("\n", " · "), "11", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_06_skills.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 7: Multi-Agent
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Multi-Agent 协作模式")
svg += slide_subtitle("多个 AI 各司其职，协同完成复杂任务")

for i, (nm, desc, col) in enumerate([
    ("🎯 主-从模式", "主 Agent 调度多个子 Agent\n适合任务分发/并行执行\n代表：OpenClaw Sub-agents", BLUE_FROST),
    ("👥 团队模式", "多角色协同各司其职\n研究员+写作者+审核\n代表：CrewAI / MetaGPT", MINT),
    ("🔗 流水线模式", "A→B→C→D 串行处理\n每环节负责一个子任务\n代表：LangGraph / TaskFlow", LAVENDER),
    ("🏆 竞争模式", "多方案并行求解\nAgent A 和 B 各自输出\n择优选择或综合", BLUE_LIGHT),
]):
    x = 40+i*305
    svg += rect(x, 145, 285, 210, col, "8")
    svg += text(x+15, 175, nm, "18", ACCENT_DARK, "bold")
    svg += rect(x+15, 188, 250, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+18, 215+j*28, line, "13", TEXT_SECONDARY)

# Use cases
svg += text(60, 390, "组合使用场景", "17", ACCENT_DARK, "bold")
uses = [("行业研究", "主-从派发子方向\n团队撰写最终报告", BLUE_FROST),
        ("软件开发", "流水线：需求→设计\n→编码→测试→部署", MINT),
        ("内容创作", "团队：策划→写稿\n→配图→审核→发布", LAVENDER),
        ("数据分析", "竞争：多模型各自分析\n→综合最优结论", BLUE_LIGHT)]
for i, (nm, desc, col) in enumerate(uses):
    x = 60+i*295
    svg += rect(x, 425, 275, 110, col, "8")
    svg += text(x+15, 450, nm, "15", ACCENT_DARK, "bold")
    svg += text(x+15, 478, desc.replace("\n", " · "), "12", TEXT_SECONDARY)

# Multi-Agent + tools
svg += text(60, 570, "关键协议", "17", ACCENT_DARK, "bold")
protos = [("MCP", "工具集成标准", BLUE_FROST), ("A2A", "Agent间通信", MINT),
          ("Function Calling", "模型工具调用", LAVENDER), ("SKILL.md", "技能定义规范", BLUE_LIGHT)]
for i, (nm, desc, col) in enumerate(protos):
    x = 60+i*295
    svg += rect(x, 605, 275, 60, col, "8")
    svg += text(x+15, 628, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+130, 628, desc, "12", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_07_multagent.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 8: Global LLM Rankings
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("全球 Top 10 大模型排行榜")
svg += slide_subtitle("LMSYS Chatbot Arena Elo 排名 + MMLU-Pro + OpenCompass 综合（2026年5月）")

# Table header
svg += rect(50, 145, 1180, 38, ACCENT_DARK, "6")
cols = [(80, 60, "排名"), (140, 220, "模型"), (360, 160, "公司"), (520, 360, "定位与特长"), (880, 100, "开源"),
        (1000, 220, "代表图标")]
for x, w, t in cols:
    svg += text(x+10, 170, t, "13", WHITE, "bold")

models = [
    ("🥇 1", "GPT-5.5", "OpenAI", "综合能力最强，多模态领先", "❌"),
    ("🥇 2", "Claude Opus 4.7", "Anthropic", "推理深度最强，代码/长文极强", "❌"),
    ("🥇 3", "Gemini 3 Pro", "Google", "多模态最强，超长上下文", "❌"),
    ("🥇 4", "DeepSeek V4", "深度求索", "开源标杆，推理达 GPT 水平，价格 1/40", "✅"),
    ("🥈 5", "Grok 4", "xAI", "实时社交数据，风格独特", "❌"),
    ("🥈 6", "Llama 4 Scout", "Meta", "最强开源基础模型，1M+上下文", "✅"),
    ("🥉 7", "Qwen 3", "阿里巴巴", "多语言优秀，中文最强", "✅"),
    ("🥉 8", "GLM-5", "智谱 AI", "中英双语，学术背景深厚", "✅"),
    ("🥉 9", "Kimi K2.5", "月之暗面", "超长上下文 2M tokens", "❌"),
    ("🥉 10", "ERNIE 5.0", "百度", "中文知识理解，搜索生态", "❌"),
]
for i, (rank, model, company, desc, oss) in enumerate(models):
    y = 188+i*45
    bg = WHITE if i%2==0 else BLUE_FROST
    svg += rect(50, y, 1180, 42, bg, "4")
    clrs = [ACCENT_BLUE, ACCENT_DARK, TEXT_SECONDARY, TEXT_PRIMARY, TEXT_MUTED]
    for j, (val, x, w) in enumerate([(rank, 80, 60), (model, 140, 220), (company, 360, 160),
                                      (desc, 520, 360), (oss, 880, 100)]):
        svg += text(x+10, y+26, str(val), "12", clrs[j], "bold" if j<2 else "normal", "start" if j<4 else "middle")

# Brand icons
for i, (name, y_pos, label) in enumerate([("GPT-5.5", 195, "G"), ("Claude Opus 4.7", 240, "C"), ("Gemini 3 Pro", 285, "G"),
    ("DeepSeek V4", 330, "D"), ("Grok 4", 375, "G"), ("Llama 4 Scout", 420, "L"),
    ("Qwen 3", 465, "Q"), ("GLM-5", 510, "G"), ("Kimi K2.5", 555, "K"), ("ERNIE 5.0", 600, "E")]):
    # Skip getting exact y, just use computed
    pass

# Brand color dots
brand_dots_data = [(225, "#10A37F", "G"), (270, "#D97706", "C"), (315, "#4285F4", "G"),
                   (360, "#4F46E5", "D"), (405, "#000000", "G"), (450, "#0466C8", "L"),
                   (495, "#FF6A00", "Q"), (540, "#8B5CF6", "G"), (585, "#F97316", "K"), (630, "#2563EB", "E")]
for y_pos, bg_col, label in brand_dots_data:
    svg += f'<circle cx="1020" cy="{y_pos+6}" r="10" fill="{bg_col}"/>'
    svg += text(1020, y_pos+11, label, "10", "#FFF", "bold", "middle")

svg += text(60, 690, "数据来源: LMSYS Chatbot Arena · MMLU-Pro · OpenCompass · Artificial Analysis", "10", TEXT_MUTED)
svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_08_global_llm.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 9: Chinese LLMs
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("中国主流大模型全景")
svg += slide_subtitle("综合能力 · 开源度 · 价格 · 场景适应性 — 八大模型全面对比")

# Top 4 cards
cns = [("DeepSeek V4", "深度求索", "开源✅", "推理/数学/代码\n全球开源第一梯队", "#4F46E5"),
       ("Qwen 3", "阿里巴巴", "开源✅", "多语言全系列\n0.5B→72B+覆盖", "#FF6A00"),
       ("GLM-5", "智谱 AI", "开源✅", "中英双语\n学术研究/AI Agent", "#8B5CF6"),
       ("Kimi K2.5", "月之暗面", "闭源❌", "超长上下文\n2M tokens 全球领先", "#F97316")]
for i, (nm, co, oss, desc, bg_col) in enumerate(cns):
    x = 40+i*305
    svg += rect(x, 145, 285, 160, BLUE_FROST, "10")
    svg += f'<circle cx="{x+22}" cy="{y+22}" r="18" fill="{bg_col}"/>' if False else ""
    svg += text(x+15, 172, nm, "18", ACCENT_DARK, "bold")
    svg += text(x+15, 198, f"{co}  |  {oss}", "12", TEXT_MUTED)
    svg += rect(x+15, 208, 250, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+18, 232+j*25, f"· {line}", "13", TEXT_SECONDARY)
    # Brand dot
    svg += f'<circle cx="{x+260}" cy="162" r="12" fill="{bg_col}"/>'
    svg += text(x+260, 167, nm[0], "10", "#FFF", "bold", "middle")

# More models
svg += text(60, 340, "其他重要模型", "17", ACCENT_DARK, "bold")
others = [("ERNIE 5.0", "百度", "中文知识/搜索生态", "#2563EB"),
          ("讯飞星火 5.0", "科大讯飞", "语音/教育场景", "#059669"),
          ("MiniMax M2.1", "MiniMax", "语音合成/AI陪伴", "#06B6D4"),
          ("Baichuan 3", "百川智能", "医疗/法律垂直", "#0891B2"),
          ("豆包大模型", "字节跳动", "C端用户量最大", "#E11D48")]
for i, (nm, co, desc, bg_col) in enumerate(others):
    x = 60+i*235
    svg += rect(x, 375, 215, 85, LAVENDER, "8")
    svg += f'<circle cx="{x+18}" cy="392" r="8" fill="{bg_col}"/>'
    svg += text(x+35, 400, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+35, 420, co, "11", TEXT_MUTED)
    svg += text(x+18, 445, desc, "11", TEXT_SECONDARY)

# Selection guide
svg += text(60, 500, "模型选择速查", "17", ACCENT_DARK, "bold")
picks = [("💡 推理/数学", "DeepSeek V4"), ("🌐 多语言", "Qwen 3"), ("📄 超长文本", "Kimi K2.5"),
         ("🔤 中文", "ERNIE 5.0"), ("💰 性价比", "DeepSeek V4"), ("🏗️ 私有化", "Qwen 3/GLM-5")]
for i, (scene, model) in enumerate(picks):
    x = 60+i*200
    svg += rect(x, 535, 180, 45, BLUE_PALE, "6")
    svg += text(x+12, 558, scene, "12", ACCENT_BLUE)
    svg += text(x+12, 575, f"→ {model}", "12", ACCENT_DARK, "bold")

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_09_chinese_llm.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 10: Model Selection Guide  
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("模型选择指南")
svg += slide_subtitle("按场景 × 按成本，找到最适合的模型")

# By Scenario
svg += text(60, 150, "按场景选择", "19", ACCENT_DARK, "bold")
scenarios = [("行业研究/深度分析", "DeepSeek V4 Pro / Claude Opus", BLUE_FROST),
             ("PPT 制作/报告撰写", "DeepSeek V4 / Claude Sonnet", MINT),
             ("编程开发",  "Claude Sonnet/Opus / GPT-5.x", LAVENDER),
             ("多模态分析", "Gemini 3 Pro / GPT-5.x", BLUE_LIGHT),
             ("超长文档", "Kimi K2.5 / Gemini 3", BLUE_PALE),
             ("中文创作", "Qwen 3 / DeepSeek V4", BLUE_FROST),
             ("高并发低预算", "DeepSeek V4 Flash", MINT),
             ("私有化部署", "Llama 4 / Qwen 3", LAVENDER)]
for i, (scene, model, col) in enumerate(scenarios):
    x = 60+(i%2)*600
    y = 185+(i//2)*60
    svg += rect(x, y, 575, 50, col, "6")
    svg += text(x+15, 212, scene, "13", ACCENT_DARK, "bold")
    svg += text(x+15, 228, f"→ {model}", "12", ACCENT_BLUE)

# By Cost
svg += text(60, 460, "按成本选择", "19", ACCENT_DARK, "bold")
costs = [("DeepSeek V4 Flash", "💰 极低 (≈$0.1/M)", "#5BBFA0"),
         ("Qwen 3", "💰 低", "#7DCFB0"),
         ("Claude Sonnet", "💰 中 ($3/15/M)", "#6B9DD8"),
         ("GPT-5", "💰 高 ($10-30/M)", "#4A7BD0"),
         ("Claude Opus", "💰 最高 ($15+/M)", "#1A2D4A")]
bar_x = 700
for i, (nm, cost, col) in enumerate(costs):
    y = 165+i*55
    w = 500-(i*60)
    svg += rect(bar_x, y, w, 42, col, "6")
    svg += text(bar_x+15, y+27, nm, "14", "#FFF", "bold")
    svg += text(bar_x+w-80, y+27, cost, "12", "#FFF" if i>2 else TEXT_SECONDARY)

# Key takeaway
svg += rect(60, 650, 1160, 50, MINT, "8")
svg += text(80, 677, "💡 策略：日常用 DeepSeek V4 Flash（极低成本），深度研究切 DeepSeek V4 Pro，关键交付物用 Claude Opus / GPT-5 把关",
            "13", TEXT_PRIMARY, "bold")

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_10_selection.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 11: Global Top 5 Workbenches
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("全球 Top 5 AI 工作台")
svg += slide_subtitle("社区认可度 × 行业影响力 — 综合排名")

wbs = [("🥇 OpenClaw", "374K ⭐ GitHub", "自托管 AI Agent 网关\n多渠道 25+ · 持久化 Agent\nTaskFlow · Sub-agents", "#E74C3C"),
       ("🥈 ChatGPT Codex", "闭源 · OpenAI", "云端原生 Agent 运行时\nGPT-5.x 最强模型驱动\n深度代码理解", "#10A37F"),
       ("🥉 Claude Code", "闭源 · Anthropic", "终端原生 CLI Agent\nMCP 协议发起者\n自主能力最强", "#D97706"),
       ("④ AutoGPT", "184K ⭐ GitHub", "Agent 概念定义者\n自主目标分解\n互联网操作", "#7C3AED"),
       ("⑤ Dify", "142K ⭐ GitHub", "可视化 Agent 编排\nRAG 引擎 · 知识库\n增长最快平台", "#1677FF")]
for i, (nm, badge, desc, col) in enumerate(wbs):
    x = 25+i*250
    svg += rect(x, 145, 235, 320, BLUE_FROST, "10")
    svg += f'<rect x="{x+10}" y="155" width="12" height="12" rx="6" fill="{col}"/>'
    svg += text(x+30, 168, nm, "18", ACCENT_DARK, "bold")
    svg += text(x+15, 195, badge, "12", TEXT_MUTED)
    svg += rect(x+15, 205, 200, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+18, 232+j*28, f"· {line}", "13", TEXT_SECONDARY)
    # Stats
    stats = [("374K", "142K", "184K", "52K", "51K")][0]
    svg += text(x+15, 350, "GitHub ⭐" if i != 1 else "用户量", "11", TEXT_MUTED)
    svg += text(x+15, 378, badge.split("⭐")[0].strip() if "⭐" in badge else "最大", "24", col, "bold")
    svg += text(x+15, 415, f"形态: {['守护进程','云端 Agent','CLI Agent','Python框架','Web平台'][i]}", "11", TEXT_SECONDARY)

svg += text(60, 500, "核心趋势", "17", ACCENT_DARK, "bold")
trends = [("2024-2026", "所有平台从\n代码补全→Agent化", BLUE_FROST),
          ("开源崛起", "OpenClaw 374K ⭐\nDify 142K ⭐", MINT),
          ("MCP 标准化", "成为 Agent 工具\n集成的事实标准", LAVENDER),
          ("低代码趋势", "Dify/Flowise 增长\n超过纯框架", BLUE_LIGHT)]
for i, (t, desc, col) in enumerate(trends):
    x = 60+i*295
    svg += rect(x, 535, 275, 90, col, "8")
    svg += text(x+15, 557, t, "14", ACCENT_DARK, "bold")
    svg += text(x+15, 585, desc.replace("\n", " · "), "11", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_11_global_wb.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 12: China Top 5 Workbenches
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("中国 Top 5 AI 工作台")
svg += slide_subtitle("从编码助手到 Agent 平台，大厂生态各占一方")

wbs_cn = [("🥇 Dify", "langgenius · 142K ⭐", "全球最成功中国AI项目\n低代码 Agent + RAG 引擎\n企业应用模板", "#1677FF"),
          ("🥈 Coze (扣子)", "字节跳动", "中国市场 Bot 构建第一\n零代码 Agent 编排\n多发布渠道 (微信/飞书)", "#E11D48"),
          ("🥉 通义灵码", "阿里巴巴", "Gartner 挑战者象限\n编程智能体 · 200+语言\n阿里云深度集成", "#FF6A00")]
for i, (nm, badge, desc, col) in enumerate(wbs_cn):
    x = 40+i*410
    svg += rect(x, 145, 385, 250, BLUE_FROST, "10")
    svg += f'<rect x="{x+12}" y="155" width="14" height="14" rx="7" fill="{col}"/>'
    svg += text(x+34, 170, nm, "20", ACCENT_DARK, "bold")
    svg += text(x+15, 200, badge, "13", TEXT_MUTED)
    svg += rect(x+15, 215, 350, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+18, 242+j*30, f"· {line}", "14", TEXT_SECONDARY)

# Others
svg += text(60, 430, "其他重要平台", "17", ACCENT_DARK, "bold")
others_cn = [("百度超级助理", "百度 · ERNIE 驱动", "AI 办公助手 + 企业知识库", "#2563EB"),
             ("腾讯 WorkBuddy", "腾讯 · 混元驱动", "桌面级智能体 + 企业微信协同", "#06B6D4"),
             ("华为 CodeArts", "华为 · 盘古驱动", "AI 代码审查 + DevOps 全链路", "#E11D48"),
             ("豆包", "字节跳动", "C 端 AI 助手 · 用户量最大", "#FF6A00"),
             ("ChatGPT", "OpenAI", "全球通用入口", "#10A37F")]
for i, (nm, badge, desc, col) in enumerate(others_cn):
    x = 60+i*235
    svg += rect(x, 465, 215, 105, LAVENDER, "8")
    svg += f'<circle cx="{x+18}" cy="482" r="8" fill="{col}"/>'
    svg += text(x+34, 490, nm, "14", ACCENT_DARK, "bold")
    svg += text(x+34, 510, badge, "11", TEXT_MUTED)
    svg += text(x+15, 538, desc, "11", TEXT_SECONDARY)

# Key distinction
svg += rect(60, 610, 1160, 45, MINT, "8")
svg += text(80, 637, "中国平台「垂直切割」更明显：编码类/办公类/Bot 类各有霸主，各自绑定大厂生态。Dify 是唯一全球化成功的中国 Agent 平台。",
            "13", TEXT_PRIMARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_12_cn_wb.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 13: Core Comparison Matrix
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("AI 工作台核心差异对比")
svg += slide_subtitle("8 维度 × 5 平台对比矩阵")

# Header
svg += rect(50, 148, 1180, 40, ACCENT_DARK, "6")
col_x = [55, 200, 410, 620, 830, 1040]
col_w = [140, 205, 205, 205, 205, 195]
for i, h in enumerate(["维度", "OpenClaw", "Dify", "Coze", "Claude Code", "ChatGPT Codex"]):
    svg += text(col_x[i]+10, 175, h, "13", WHITE, "bold")

matrix = [
    ["形态", "守护进程+CLI", "Web 应用", "网页+API", "终端 CLI", "云端 Agent"],
    ["Agent 模式", "ReAct+持久化", "可视化编排", "可视化编排", "CLI 自主 Agent", "原生 Agent"],
    ["记忆系统", "✅ 自进化", "✅ 知识库", "✅ 知识库", "✅ 项目记忆", "✅ 会话记忆"],
    ["多渠道", "✅ 25+ 渠道", "✅ API/Web", "✅ 微信/飞书", "❌ 仅终端", "❌ 仅 Web"],
    ["持久任务", "✅ Cron+TaskFlow", "✅ 后台任务", "❌", "❌", "❌"],
    ["MCP", "✅ Server+Client", "❌ 支持有限", "❌", "✅ Client", "✅ Client"],
    ["开源", "✅ MIT", "✅ Apache 2.0", "❌ 闭源", "❌ 闭源", "❌ 闭源"],
    ["易用性", "中 (需配置)", "高 (拖拽)", "高 (零代码)", "低 (需 CLI)", "低 (需 API)"],
]
for j, row in enumerate(matrix):
    y = 193+j*48
    bg = WHITE if j%2==0 else BLUE_FROST
    svg += rect(50, y, 1180, 45, bg, "4")
    for i, val in enumerate(row):
        bold = i == 0
        svg += text(col_x[i]+10, y+27, val, "12", ACCENT_DARK if bold else TEXT_PRIMARY, "bold" if bold else "normal")

svg += rect(60, 595, 1160, 80, BLUE_FROST, "8")
svg += text(80, 622, "📍 OpenClaw 填补了一个独特空白：在「深度自动化 + 持久化 + 多 Agent 编排 + 开源」交叉点", "14", ACCENT_DARK, "bold")
svg += text(80, 650, "没有其他平台同时具备持久任务 (Cron)、多渠道输出 (25+)、MCP Server+Client 双角色、自进化记忆 这四项能力", "13", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_13_comparison.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 14: OpenClaw Architecture
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("OpenClaw 系统架构")
svg += slide_subtitle("Gateway → Provider → Agent Runtime → 编排层 → 渠道层 五层体系")

layers = [
    ("Gateway 守护进程", "单进程长驻 · WebSocket 通信 · Canvas 可视化 · 配置热重载", ACCENT_DARK, "#FFF"),
    ("Provider 模型层 (35+)", "DeepSeek·Anthropic·OpenAI·Google·阿里·腾讯·MiniMax·Ollama·vLLM…\n故障转移链 · Auth Profile 轮转 · Runtime 分离", "#D0E4F7", TEXT_PRIMARY),
    ("Agent 运行时 (PI Core)", "Agent ReAct 循环 · 会话管理 · 记忆引擎 · 技能加载 · Hook 系统\n串行化执行 → 模型推理 → 工具执行 → 流式回复 → 持久化", "#E8FBF5", TEXT_PRIMARY),
    ("自动化编排层", "Cron 定时调度 · TaskFlow 工作流 · Sub-agents 并行 · Heartbeat 心跳\n持久状态 + SQLite 注册表 + 故障恢复", "#ECF2FE", TEXT_PRIMARY),
    ("渠道层 (25+)", "微信 · Telegram · Slack · Discord · Signal · WhatsApp · iMessage · 飞书 · …\n多账号管理 · 多 Agent 路由 · 统一 WebSocket API", "#EFF1FE", TEXT_PRIMARY),
]
y = 145
for nm, desc, bg, tc in layers:
    svg += rect(80, y, 1120, 90, bg, "8")
    svg += text(105, y+28, nm, "17", ACCENT_DARK, "bold")
    svg += text(105, y+55, desc.replace("\n", " · "), "12", TEXT_SECONDARY)
    if y < 580:
        svg += text(640, y+98, "▼", "14", TEXT_MUTED, "normal", "middle")
    y += 105

# Also add the unique capabilities
svg += rect(60, 660, 1160, 40, MINT, "8")
svg += text(80, 686, "⚡ 独特能力：持久化 Agent（业界独有）· Cron 定时 · 自进化记忆 · MCP Server+Client 双角色 · 完全开源 MIT", "13", ACCENT_DARK, "bold")

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_14_architecture.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 15: OpenClaw Core Capabilities
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("OpenClaw 核心能力")
svg += slide_subtitle("一个网关连接 25+ 渠道到 AI Agent，持久化深度自动化")

caps = [
    ("🔌 35+ Provider", "多模型自由切换\n故障转移链自动回退\nAuth Profile 轮转", BLUE_FROST),
    ("📡 25+ 渠道", "微信/Telegram/Slack/Discord\nSignal/WhatsApp/iMessage\n多渠道统一管理", MINT),
    ("💾 三层记忆", "MEMORY.md 长期记忆\nmemory/ 每日笔记\n向量数据库 Hybrid Search", LAVENDER),
    ("⚙️ 编排系统", "Cron 定时 · TaskFlow 工作流\nSub-agents 并行执行\nHeartbeat 心跳检查", BLUE_LIGHT),
    ("🎯 MCP 双角色", "Server: 暴露渠道能力\nClient: 调用外部工具\n业界唯一双角色", BLUE_PALE),
    ("🔄 自进化", "梦境系统自动整合记忆\nSelf-improving 机制\n.learnings/ 体系", BLUE_FROST),
]
for i, (nm, desc, col) in enumerate(caps):
    x = 30+(i%3)*410
    y = 145+(i//3)*210
    svg += rect(x, y, 390, 190, col, "10")
    svg += text(x+18, y+35, nm, "19", ACCENT_DARK, "bold")
    svg += rect(x+18, y+48, 350, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+20, y+78+j*30, f"· {line}", "14", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_15_capabilities.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 16: Hermes
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("Hermes 简介与 OpenClaw 关系")
svg += slide_subtitle("将自然语言愿望转化为可靠自动化的 AI Agent 框架")

# Two-column layout
svg += rect(50, 145, 570, 380, BLUE_FROST, "10")
svg += text(80, 180, "Hermes Agent 框架", "24", ACCENT_DARK, "bold")
svg += text(80, 218, "核心定位", "16", ACCENT_BLUE, "bold")
svg += text(80, 245, "将用户用自然语言描述的「需求」自动转化为", "14", TEXT_SECONDARY)
svg += text(80, 265, "结构化、可靠的自动化流程", "14", ACCENT_DARK, "bold")
svg += text(80, 300, "工作原理", "16", ACCENT_BLUE, "bold")
svg += text(80, 328, "① 意图理解 → ② 流程生成 → ③ 安全执行 → ④ 交付", "14", TEXT_SECONDARY)
svg += text(80, 365, "关键差异", "16", ACCENT_BLUE, "bold")
svg += text(80, 393, "比 AutoGPT/CrewAI 更注重「可靠性」而非探索性", "14", TEXT_SECONDARY)
svg += text(80, 418, "比 LangChain 更「面向终端用户」而非开发者", "14", TEXT_SECONDARY)
svg += text(80, 443, "比 Dify 更注重「代码级别」的可控性", "14", TEXT_SECONDARY)

svg += rect(660, 145, 570, 380, LAVENDER, "10")
svg += text(690, 180, "OpenClaw vs Hermes", "24", ACCENT_DARK, "bold")

# Comparison table
svg += rect(690, 210, 520, 30, ACCENT_DARK, "4")
svg += text(700, 231, "维度", "13", WHITE, "bold")
svg += text(770, 231, "OpenClaw", "13", WHITE, "bold")
svg += text(950, 231, "Hermes", "13", WHITE, "bold")
    
h_compare = [("定位", "AI Agent 网关+工作台", "NL→自动化流程"),
             ("核心", "多渠道+持久化编排", "可靠性流程"),
             ("开源", "✅ MIT", "✅ 开源"),
             ("重点", "Agent 全生命周期", "NL→稳定执行"),
             ("场景", "个人/企业深度自动化", "生产级流程")]
for i, (dim, o, h) in enumerate(h_compare):
    y = 245+i*32
    bg = WHITE if i%2==0 else "#E5E9F8"
    svg += rect(690, y, 520, 30, bg, "2")
    svg += text(700, y+20, dim, "11", ACCENT_BLUE, "bold")
    svg += text(770, y+20, o, "11", TEXT_PRIMARY)
    svg += text(950, y+20, h, "11", TEXT_SECONDARY)

# Bottom
svg += rect(60, 560, 1160, 65, MINT, "8")
svg += text(80, 588, "💡 共同点：都开源 · 都强调持久化和可靠性 · 都兼容 AgentSkills", "15", ACCENT_DARK, "bold")
svg += text(80, 612, "差异点：OpenClaw 侧重多渠道 Agent 编排和系统集成；Hermes 侧重自然语言到稳定自动化的转化", "14", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_16_hermes.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 17: Industry Research Config
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("行业场景配置 — 行业研究 & 客户研究")
svg += slide_subtitle("端到端的 AI Agent 配置方案")

# Two columns
svg += rect(50, 145, 570, 300, BLUE_FROST, "10")
svg += text(80, 180, "📊 行业研究", "22", ACCENT_DARK, "bold")
svg += text(80, 218, "模型配置", "16", ACCENT_BLUE, "bold")
svg += text(80, 245, "primary: deepseek/deepseek-v4-flash", "14", TEXT_SECONDARY)
svg += text(80, 265, "fallback: deepseek-v4-pro → claude-sonnet-4-5", "14", TEXT_SECONDARY)
svg += text(80, 300, "技能安装", "16", ACCENT_BLUE, "bold")
svg += text(80, 328, "· web-search（多引擎搜索）", "14", TEXT_SECONDARY)
svg += text(80, 348, "· web-fetch（网页内容提取）", "14", TEXT_SECONDARY)
svg += text(80, 368, "· browser-automation（浏览器自动化）", "14", TEXT_SECONDARY)
svg += text(80, 395, "工作流", "16", ACCENT_BLUE, "bold")
svg += text(80, 423, "sessions_spawn 并行派发研究子任务", "14", TEXT_SECONDARY)

svg += rect(660, 145, 570, 300, MINT, "10")
svg += text(690, 180, "🎯 客户研究", "22", ACCENT_DARK, "bold")
svg += text(690, 218, "四层画像框架", "16", ACCENT_BLUE, "bold")
svg += text(690, 245, "Layer 1 — 基本信息：营收/员工/产品", "14", TEXT_SECONDARY)
svg += text(690, 265, "Layer 2 — 战略动态：并购/投资/组织", "14", TEXT_SECONDARY)
svg += text(690, 285, "Layer 3 — 竞争格局：对标/份额/差异", "14", TEXT_SECONDARY)
svg += text(690, 305, "Layer 4 — 合作切入点：痛点/机会", "14", TEXT_SECONDARY)
svg += text(690, 340, "最佳实践", "16", ACCENT_BLUE, "bold")
svg += text(690, 368, "· MECE 结构输出 · 多源交叉验证", "14", TEXT_SECONDARY)
svg += text(690, 388, "· 写入 client-xxx.md 记忆库", "14", TEXT_SECONDARY)
svg += text(690, 408, "· 设置 Cron 定期刷新动态", "14", TEXT_SECONDARY)

# Cron example
svg += rect(50, 470, 1180, 85, LAVENDER, "8")
svg += text(80, 502, "Cron 定时任务示例", "16", ACCENT_DARK, "bold")
svg += rect(70, 515, 1140, 30, WHITE, "4")
svg += text(90, 536, "openclaw cron add --every 30d --mode isolated \"刷新客户 [公司名] 的最新动态并更新记忆\"", "13", TEXT_SECONDARY)

# Quick config
svg += rect(50, 575, 1180, 90, BLUE_PALE, "8")
svg += text(80, 605, "快速启动清单", "16", ACCENT_DARK, "bold")
svg += text(80, 632, "① 明确范围/受众/问题 → ② 裁剪框架出 Outline → ③ 确认后并行搜索 → ④ MECE 整理 → ⑤ 交叉验证 → ⑥ 质量检查后输出", "13", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_17_research.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 18: Solution Design & PPT Scenarios
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("行业场景配置 — 解决方案 & PPT 制作")
svg += slide_subtitle("从研究到交付的完整 Pipeline")

# Solutions
svg += rect(50, 145, 570, 280, BLUE_FROST, "10")
svg += text(80, 180, "🔧 解决方案制作", "22", ACCENT_DARK, "bold")
svg += text(80, 218, "工作流程", "16", ACCENT_BLUE, "bold")
svg += text(80, 245, "① 需求拆解：痛点→需求→非功能", "14", TEXT_SECONDARY)
svg += text(80, 265, "② 方案设计：架构+技术栈+逻辑", "14", TEXT_SECONDARY)
svg += text(80, 285, "③ 技术选型：对比表+评估维度", "14", TEXT_SECONDARY)
svg += text(80, 305, "④ 成本估算：资源×单价×总量", "14", TEXT_SECONDARY)
svg += text(80, 325, "⑤ 路线图：阶段+里程碑+交付物", "14", TEXT_SECONDARY)
svg += text(80, 360, "最佳实践", "16", ACCENT_BLUE, "bold")
svg += text(80, 388, "· solutions/ 模板库复用", "14", TEXT_SECONDARY)
svg += text(80, 408, "· 分层输出（投资层 vs 技术层）", "14", TEXT_SECONDARY)

# PPT Making
svg += rect(660, 145, 570, 280, MINT, "10")
svg += text(690, 180, "📑 PPT 制作", "22", ACCENT_DARK, "bold")
svg += text(690, 218, "默认技能", "16", ACCENT_BLUE, "bold")
svg += text(690, 245, "ppt-master（SVG 内容生成系统）", "14", TEXT_SECONDARY)
svg += text(690, 275, "备选技能", "16", ACCENT_BLUE, "bold")
svg += text(690, 303, "· pptx-master（PDF/DOCX→原生 PPTX）", "14", TEXT_SECONDARY)
svg += text(690, 323, "· frontend-slides（HTML 动画演示稿）", "14", TEXT_SECONDARY)
svg += text(690, 343, "· mckinsey-generator（咨询风数据报告）", "14", TEXT_SECONDARY)
svg += text(690, 380, "风格文件", "16", ACCENT_BLUE, "bold")
svg += text(690, 408, "styles/default-brand-deck.md （现代品牌风）", "14", TEXT_SECONDARY)
svg += text(690, 428, "styles/fresh-tech-deck.md （清新科技风）", "14", TEXT_SECONDARY)

# PPT Pipeline
svg += rect(50, 450, 1180, 100, LAVENDER, "8")
svg += text(80, 480, "PPT 制作 Pipeline", "16", ACCENT_DARK, "bold")
pipe_steps = [("数据收集", "→", "骨架确定", "→", "风格选择", "→", "并行制作", "→", "质量检查", "→", "PPTX 输出")]
for i, s in enumerate(pipe_steps):
    x = 80+i*200
    svg += rect(x, 495, 160, 38, BLUE_FROST if s != "→" else MINT, "6")
    if s == "→":
        svg += text(x+75, 523, "→", "20", ACCENT_BLUE, "bold", "middle")
    else:
        svg += text(x+8, 522, s, "13", ACCENT_DARK if s in ["骨架确定","PPTX 输出"] else TEXT_PRIMARY, "bold" if s in ["骨架确定","PPTX 输出"] else "normal")

svg += rect(50, 575, 1180, 55, BLUE_PALE, "8")
svg += text(80, 601, "💡 质量控制", "15", ACCENT_DARK, "bold")
svg += text(80, 622, "来源可追溯 · 数据交叉验证 · 附录不删 · 每页一个核心 message", "13", TEXT_SECONDARY)
svg += text(600, 622, "· 不编造数据 · 不承诺无法交付的质量 ·" + " " + "涉及推测必须标注", "13", TEXT_SECONDARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_18_solution_ppt.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 19: OpenClaw Agent Configuration
# =====================================================
svg = svg_header() + top_bar()
svg += slide_title("OpenClaw 配置文件全景")
svg += slide_subtitle("SOUL.md + AGENTS.md + Skills + 模型路由 + Cron — 五大配置支柱")

pillars = [
    ("🧠 SOUL.md", "定义 Agent 人格", "行业研究专家\n深度办公 AI\n不编数据·不虚构来源", BLUE_FROST),
    ("📋 AGENTS.md", "定义工作流程", "需求确认→信息收集\n→分析整理→输出\n十层分析框架", MINT),
    ("🛠️ Skills", "工具能力体系", "web-search/fetch\nfrontend-slides\nkdocs / office-toolkit", LAVENDER),
    ("🎯 模型路由", "智能分派策略", "简单→Flash\n复杂→Pro\n关键→Claude Opus", BLUE_LIGHT),
    ("⏰ Cron+Task", "自动化编排", "定时刷新研究\n后台任务执行\nSub-agents 并行", BLUE_PALE),
]
for i, (nm, role, desc, col) in enumerate(pillars):
    x = 30+i*245
    svg += rect(x, 145, 230, 200, col, "10")
    svg += text(x+15, 175, nm, "17", ACCENT_DARK, "bold")
    svg += text(x+15, 200, role, "13", ACCENT_BLUE)
    svg += rect(x+15, 212, 200, 2, ACCENT_BLUE)
    for j, line in enumerate(desc.split("\n")):
        svg += text(x+18, 237+j*28, f"· {line}", "13", TEXT_SECONDARY)

# Model config detail
svg += text(60, 380, "推荐模型配置模板", "17", ACCENT_DARK, "bold")
svg += rect(60, 400, 1160, 90, BLUE_FROST, "8")
svg += text(80, 428, 'agents: { defaults: { model: { primary: "deepseek/deepseek-v4-flash", fallbacks:["deepseek/deepseek-v4-pro","anthropic/claude-sonnet-4-5"] } } }', "13", TEXT_SECONDARY)
svg += text(80, 455, "渠道: wechat/telegram/slack/discord  |  技能白名单: github/web-search/kdocs/frontend-slides  |  Heartbeat: 2h", "12", TEXT_MUTED)

# Skills list
svg += text(60, 520, "推荐安装技能清单", "17", ACCENT_DARK, "bold")
skills = [("web-search", "多引擎搜索"), ("web-fetch", "网页提取"), ("browser-automation", "浏览器自动"),
          ("frontend-slides", "HTML 幻灯片"), ("pptx-master", "专业 PPTX"), ("kdocs", "金山文档云")]
for i, (s, desc) in enumerate(skills):
    x = 60+i*200
    svg += rect(x, 550, 185, 50, LAVENDER, "8")
    svg += text(x+12, 574, s, "13", ACCENT_DARK, "bold")
    svg += text(x+12, 592, desc, "11", TEXT_MUTED)

# Or use pip install
svg += rect(60, 625, 1160, 45, MINT, "8")
svg += text(80, 652, "💡 一句话配置哲学：SOUL.md 定义人格 → AGENTS.md 定义工作流 → Skills 定义工具 → 模型路由控制质量 → Cron/Sub-agents 自动化",
            "13", TEXT_PRIMARY)

svg += bottom_bar() + svg_footer()
with open(f"{OUT}/slide_19_configuration.svg", "w") as f: f.write(svg)

# =====================================================
# SLIDE 20: Closing
# =====================================================
svg = svg_header()
svg += rect(0, 0, 1280, 350, HEADER_START)
svg += text(640, 140, "AI Agent 深度培训手册", "40", ACCENT_DARK, "bold", "middle")
svg += text(640, 200, "让 AI 成为你的深度研究搭档", "22", ACCENT_BLUE, "normal", "middle")
svg += rect(540, 215, 200, 4, ACCENT_TEAL)
svg += text(640, 270, "研墨 ResearchInk  ·  2026-05-22", "16", TEXT_MUTED, "normal", "middle")

# Key takeaways
svg += text(640, 340, "核心要点回顾", "20", ACCENT_DARK, "bold", "middle")
takeaways = [
    ("Agent = LLM + Planning + Tool + Memory", "核心公式"),
    ("ReAct 是最通用的 Agent 工作流", "工作流"),
    ("RAG 是解决幻觉的关键技术", "RAG"),
    ("MCP 是 Agent 工具集成的标准协议", "MCP"),
    ("OpenClaw = 持久化 + 多渠道 + 自进化", "OpenClaw"),
]
for i, (point, cat) in enumerate(takeaways):
    x = 210+(i%3)*300
    y = 370+(i//3)*60
    svg += rect(x, y, 280, 50, BLUE_FROST, "8")
    svg += text(x+15, y+20, cat, "11", ACCENT_BLUE, "bold")
    svg += text(x+15, y+42, point, "13", ACCENT_DARK, "bold")

# Resources
svg += text(640, 530, "推荐资源", "17", ACCENT_DARK, "bold", "middle")
resources = [("OpenClaw 文档", "docs.openclaw.ai"), ("LMSYS Arena", "lmarena.ai"),
             ("MCP 协议", "modelcontextprotocol.io"), ("AgentSkills", "agentskills.io")]
for i, (nm, url) in enumerate(resources):
    x = 200+i*230
    svg += rect(x, 550, 210, 40, LAVENDER, "8")
    svg += text(x+15, 573, nm, "13", ACCENT_DARK, "bold")
    svg += text(x+15, 588, url, "11", TEXT_MUTED)

svg += rect(640, 620, 0, 0, WHITE) + bottom_bar() + svg_footer()
with open(f"{OUT}/slide_20_closing.svg", "w") as f: f.write(svg)

print(f"✅ 20 SVGs generated in {OUT}")
print(f"   Files: {os.listdir(OUT)}")
