#!/usr/bin/env python3
"""Generate guizang magazine-style (Style A) HTML PPT from training manual."""
import re

TEMPLATE = "/tmp/template_clean.html"
OUTPUT = "/root/.openclaw/workspace/deliverables/guizang-ppt/ppt/index.html"

# Style A template is at:
import os, shutil
# Copy and clean
with open("/root/.openclaw/workspace/skills/guizang-ppt-skill/assets/template.html", "rb") as f:
    data = f.read()
text = data.decode("utf-8", errors="replace")
with open("/tmp/template_style_a.html", "w", encoding="utf-8") as f:
    f.write(text)

TEMPLATE = "/tmp/template_style_a.html"

INDIGO_THEME = """    /* ============ 主题色(🌊 靛蓝瓷 · 科技/研究/AI) ============ */
    --ink:#0a1f3d;
    --ink-rgb:10,31,61;
    --paper:#f1f3f5;
    --paper-rgb:241,243,245;
    --paper-tint:#e4e8ec;
    --ink-tint:#152a4a;"""

SLIDES = """
<!-- ======== Page 1: Cover ======== -->
<section class="slide hero dark">
  <div class="chrome">
    <div>DEEP TRAINING · AI AGENT</div>
    <div>Vol.01</div>
  </div>
  <div class="frame" style="display:grid; gap:4vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>研墨 ResearchInk · 2026-05-22</div>
    <h1 class="h-hero" data-anim>AI Agent<br>深度培训手册</h1>
    <h2 class="h-sub" data-anim>大模型 · Agent 架构 · 工作台对比 · 场景配置</h2>
    <p class="lead" style="max-width:60vw" data-anim>
      系统掌握 AI Agent 技术栈并应用于行业研究、客户研究、解决方案制作、PPT 制作等场景。
    </p>
    <div class="meta-row" data-anim>
      <span>研墨 ResearchInk</span><span>·</span><span>数据截止 2026-05-22</span>
    </div>
  </div>
  <div class="foot">
    <div>系统理解 AI Agent 技术栈</div>
    <div>— Vol.01 —</div>
  </div>
</section>

<!-- ======== Page 2: Chapter Cover ======== -->
<section class="slide hero light">
  <div class="chrome">
    <div>第一幕 · 基础知识</div>
    <div>Act I · 02 / 11</div>
  </div>
  <div class="frame" style="display:grid; gap:6vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Act I</div>
    <h1 class="h-hero" style="font-size:8.5vw" data-anim>LLM 与 AI Agent 基础</h1>
    <p class="lead" style="max-width:55vw" data-anim>
      从 Transformer 到自主 Agent · 理解 AI 的进化主线。
    </p>
  </div>
  <div class="foot">
    <div>第一幕引子 · 大模型基础</div>
    <div>— · —</div>
  </div>
</section>

<!-- ======== Page 3: Big Data - LLM Milestones ======== -->
<section class="slide light">
  <div class="chrome">
    <div>LLM 发展 · 关键里程碑</div>
    <div>Act I · 03 / 11</div>
  </div>
  <div class="frame" style="padding-top:6vh">
    <div class="kicker" data-anim>Milestones · 2017–2026</div>
    <h2 class="h-xl" data-anim>大模型发展里程碑</h2>
    <p class="lead" style="margin-bottom:4vh" data-anim>从 Transformer 到 Agent 生态爆发。</p>

    <div class="grid-3" style="margin-top:4vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">2017 · Transformer</div>
        <div class="stat-nb" style="font-size:2.8vw">Attention<br>Is All You Need</div>
        <div class="stat-note">Google 提出 Transformer 架构</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">2020 · GPT-3</div>
        <div class="stat-nb" style="font-size:2.8vw">175B</div>
        <div class="stat-note">参数规模突破千亿，few-shot 能力</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">2022 · ChatGPT</div>
        <div class="stat-nb" style="font-size:2.8vw">对话式 AI</div>
        <div class="stat-note">LLM 进入大众视野</div>
      </div>
    </div>
    <div class="grid-3" style="margin-top:3vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">2023 · GPT-4 / Claude</div>
        <div class="stat-nb" style="font-size:2.8vw">多模态涌现</div>
        <div class="stat-note">长上下文、多模态、Agent 能力</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">2024-25 · DeepSeek V4</div>
        <div class="stat-nb" style="font-size:2.8vw">开源逼近</div>
        <div class="stat-note">开源模型逼近闭源水平</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">2026 · Agent 生态</div>
        <div class="stat-nb" style="font-size:2.8vw">高级推理</div>
        <div class="stat-note">Agent 生态爆发，自主 Agent 成熟</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>LLM 进化简史 · 十年六阶段</div>
    <div>Act I · Milestones</div>
  </div>
</section>

<!-- ======== Page 4: Left Text + Right Image - Agent Formula ======== -->
<section class="slide dark">
  <div class="chrome">
    <div>核心公式 · Core Formula</div>
    <div>Act I · 04 / 11</div>
  </div>
  <div class="frame grid-2-7-5" style="padding-top:6vh">
    <div style="display:flex; flex-direction:column; justify-content:space-between; gap:3vh">
      <div>
        <div class="kicker" data-anim>Andrew Ng 定义</div>
        <h2 class="h-xl" data-anim>Agent 核心公式</h2>
        <p class="lead" style="margin-top:3vh" data-anim>
          Agent = LLM（大脑）+ Planning（规划）+ Tool Use（工具）+ Memory（记忆）
        </p>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:2vh">
        <div style="padding:1.6vh 1.2vw; background:rgba(255,255,255,.08); border-left:2px solid rgba(255,255,255,.3)">
          <div style="font-family:var(--serif-en); font-size:max(14px,1.4vw); font-weight:600; opacity:.9">🧠 LLM 大脑</div>
          <div style="font-size:max(13px,.84vw); opacity:.65; margin-top:.4vh">GPT-5 · Claude 4 · DeepSeek V4</div>
        </div>
        <div style="padding:1.6vh 1.2vw; background:rgba(255,255,255,.08); border-left:2px solid rgba(255,255,255,.3)">
          <div style="font-family:var(--serif-en); font-size:max(14px,1.4vw); font-weight:600; opacity:.9">📋 Planning 规划</div>
          <div style="font-size:max(13px,.84vw); opacity:.65; margin-top:.4vh">ReAct · Plan-and-Execute · ToT</div>
        </div>
        <div style="padding:1.6vh 1.2vw; background:rgba(255,255,255,.08); border-left:2px solid rgba(255,255,255,.3)">
          <div style="font-family:var(--serif-en); font-size:max(14px,1.4vw); font-weight:600; opacity:.9">🔧 Tool Use 工具</div>
          <div style="font-size:max(13px,.84vw); opacity:.65; margin-top:.4vh">Function Calling · MCP 协议</div>
        </div>
        <div style="padding:1.6vh 1.2vw; background:rgba(255,255,255,.08); border-left:2px solid rgba(255,255,255,.3)">
          <div style="font-family:var(--serif-en); font-size:max(14px,1.4vw); font-weight:600; opacity:.9">💾 Memory 记忆</div>
          <div style="font-size:max(13px,.84vw); opacity:.65; margin-top:.4vh">向量数据库 · 文件系统 · RAG</div>
        </div>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; justify-content:center; gap:1.6vh; padding:2.4vh 1.6vw; background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.12)">
      <div class="stat-card" style="text-align:center" data-anim>
        <div class="stat-label" style="color:rgba(255,255,255,.6)">Agent 分级</div>
        <div class="stat-nb" style="font-size:3.2vw; color:#fff">L0 → L4</div>
        <div class="stat-note" style="color:rgba(255,255,255,.5)">从无 Agent 到自进化</div>
      </div>
      <div class="stat-card" style="text-align:center" data-anim>
        <div class="stat-label" style="color:rgba(255,255,255,.6)">关键技术栈</div>
        <div class="stat-nb" style="font-size:2.4vw; color:#fff">MCP · RAG</div>
        <div class="stat-note" style="color:rgba(255,255,255,.5)">工具连接 + 知识检索</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Andrew Ng · Agent 核心公式</div>
    <div>Act I · Formula</div>
  </div>
</section>

<!-- ======== Page 5: Pipeline - Workflow Patterns ======== -->
<section class="slide light" data-animate="pipeline">
  <div class="chrome">
    <div>工作流 · Workflow</div>
    <div>Act I · 05 / 11</div>
  </div>
  <div class="frame">
    <div class="kicker">Pipeline · Agent 工作流</div>
    <h2 class="h-xl">四种工作流模式</h2>

    <div class="pipeline-section">
      <div class="pipeline-label">ReAct · 思考→行动→观察</div>
      <div class="pipeline">
        <div class="step" data-anim="step">
          <div class="step-nb">01</div>
          <div class="step-title">Thought</div>
          <div class="step-desc">分析需求，确定下一步</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">02</div>
          <div class="step-title">Action</div>
          <div class="step-desc">调用工具/搜索/计算</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">03</div>
          <div class="step-title">Observation</div>
          <div class="step-desc">评估工具返回的结果</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">04</div>
          <div class="step-title">Loop</div>
          <div class="step-desc">循环直至得出最终答案</div>
        </div>
      </div>
    </div>

    <div class="pipeline-section" style="margin-top:3.6vh">
      <div class="pipeline-label">Plan-and-Execute · 先计划后执行</div>
      <div class="pipeline">
        <div class="step" data-anim="step">
          <div class="step-nb">01</div>
          <div class="step-title">Plan</div>
          <div class="step-desc">生成完整多步计划</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">02</div>
          <div class="step-title">Execute</div>
          <div class="step-desc">逐步执行检查结果</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">03</div>
          <div class="step-title">Adapt</div>
          <div class="step-desc">根据结果调整计划</div>
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 05 · Agent 工作流模式</div>
    <div>Workflow</div>
  </div>
</section>

<!-- ======== Page 6: Chapter Cover 2 ======== -->
<section class="slide hero light">
  <div class="chrome">
    <div>第二幕 · 模型与平台</div>
    <div>Act II · 06 / 11</div>
  </div>
  <div class="frame" style="display:grid; gap:6vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Act II</div>
    <h1 class="h-hero" style="font-size:8.5vw" data-anim>大模型排行与 AI 工作台</h1>
    <p class="lead" style="max-width:55vw" data-anim>
      全球 LLM 能力对比 · 主流 AI 平台全景。
    </p>
  </div>
  <div class="foot">
    <div>第二幕引子 · 模型与平台</div>
    <div>— · —</div>
  </div>
</section>

<!-- ======== Page 7: Big Data - LLM Capabilities ======== -->
<section class="slide light">
  <div class="chrome">
    <div>模型能力 · Capabilities</div>
    <div>Act II · 07 / 11</div>
  </div>
  <div class="frame" style="padding-top:6vh">
    <div class="kicker" data-anim>Benchmark · 能力边界</div>
    <h2 class="h-xl" data-anim>LLM 核心能力边界</h2>
    <p class="lead" style="margin-bottom:5vh" data-anim>模型在哪些场景强，哪些场景仍需工具辅助。</p>

    <div class="grid-3" style="margin-top:4vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">自然语言理解</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink)">✅</div>
        <div class="stat-note">核心强项，理解复杂意图</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">代码编写与调试</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink)">✅</div>
        <div class="stat-note">多语言编程能力成熟</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">逻辑推理</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink)">✅</div>
        <div class="stat-note">高级推理模型显著提升</div>
      </div>
    </div>
    <div class="grid-3" style="margin-top:3vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">联网搜索</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink-tint); opacity:.55">❌ → 需工具</div>
        <div class="stat-note">超出知识截止日期的事</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">私有领域知识</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink-tint); opacity:.55">❌ → 需 RAG</div>
        <div class="stat-note">非公开数据需检索增强</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">精确数据处理</div>
        <div class="stat-nb" style="font-size:4vw; color:var(--ink-tint); opacity:.55">❌ → 需工具</div>
        <div class="stat-note">调用计算器/代码执行</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>LLM 能做与不能做的边界</div>
    <div>Act II · Capabilities</div>
  </div>
</section>

<!-- ======== Page 8: Image Grid - AI Workbench ======== -->
<section class="slide light">
  <div class="chrome">
    <div>工作台 · Workbenches</div>
    <div>Act II · 08 / 11</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker" data-anim>Comparison · 全球 Top AI 工作台</div>
    <h2 class="h-xl" data-anim>AI 工作台能力矩阵</h2>

    <div class="grid-4" style="margin-top:4vh">
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">OpenClaw</div>
        <div class="stat-note">374K ⭐ · 全栈 Agent 框架<br>L0-L4 全覆盖</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">Dify</div>
        <div class="stat-note">142K ⭐ · LLMOps<br>可视化工作流编排</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">LangChain</div>
        <div class="stat-note">137K ⭐ · LLM 框架<br>Agent 开发生态</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">AutoGPT</div>
        <div class="stat-note">184K ⭐ · 自主 Agent<br>多步任务自动执行</div>
      </div>
    </div>
    <div class="grid-4" style="margin-top:2vh">
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">ChatGPT</div>
        <div class="stat-note">闭源 · 对话 AI 标杆<br>Agent 逐步开放</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">Claude Code</div>
        <div class="stat-note">闭源 · 终端 Agent<br>编码深度集成</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">Cursor</div>
        <div class="stat-note">闭源 · AI 原生 IDE<br>Agent 深入代码</div>
      </div>
      <div class="stat-card" data-anim style="padding:1.6vh">
        <div class="stat-nb" style="font-size:2.2vw">n8n</div>
        <div class="stat-note">189K ⭐ · 工作流自动化<br>AI 节点扩展</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 08 · AI 工作台对比</div>
    <div>Act II · Matrix</div>
  </div>
</section>

<!-- ======== Page 9: Before/After - AI Transform ======== -->
<section class="slide light" data-animate="directional">
  <div class="chrome">
    <div>变革 · Transformation</div>
    <div>Act II · 09 / 11</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker" data-anim>Before / After · 范式转变</div>
    <h2 class="h-xl" style="margin-bottom:4vh" data-anim>AI Agent 带来的变革</h2>

    <div class="grid-2-6-6" style="gap:5vw 4vh">
      <div data-anim="left" style="padding:3vh 2vw; border-left:3px solid currentColor; opacity:.55">
        <div class="kicker" style="opacity:.9">Before · 传统方式</div>
        <h3 class="h-md" style="margin-top:2vh">手动 · 线性 · 重复</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-zh); font-size:max(14px,1.1vw); line-height:1.55">
          <li>手动搜索信息</li>
          <li>逐一阅读分析</li>
          <li>手动制作 PPT 和报告</li>
          <li>重复劳动，聚焦执行而非决策</li>
        </ul>
      </div>
      <div data-anim="right" style="padding:3vh 2vw; border-left:3px solid currentColor">
        <div class="kicker" style="opacity:.9">After · AI Agent 时代</div>
        <h3 class="h-md" style="margin-top:2vh">自动 · 并行 · 智能</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-zh); font-size:max(14px,1.1vw); line-height:1.55">
          <li>Agent 自动多源搜索</li>
          <li>结构化分析输出</li>
          <li>一键生成 PPTX</li>
          <li>聚焦决策而非执行</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 09 · AI Agent 带来的变革</div>
    <div>Before / After</div>
  </div>
</section>

<!-- ======== Page 10: Big Quote - Core Insight ======== -->
<section class="slide dark" data-animate="quote">
  <div class="chrome">
    <div>核心金句 · Takeaway</div>
    <div>10 / 11</div>
  </div>
  <div class="frame" style="display:grid; gap:5vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Quote · 总结</div>
    <blockquote style="font-family:var(--serif-zh); font-weight:700; font-size:5.2vw; line-height:1.25; letter-spacing:-.01em; max-width:72vw">
      <span data-anim="line" style="display:block">"理解 Agent 分级，</span>
      <span data-anim="line" style="display:block">选对工作流模式，</span>
      <span data-anim="line" style="display:block">场景决定配置。"</span>
    </blockquote>
    <p class="lead" style="max-width:55vw; opacity:.65" data-anim>
      L0→L4 逐级递进 · ReAct 通用框架 · 研究/PPT/知识/数据四场景
    </p>
    <div class="meta-row" data-anim>
      <span>研墨 ResearchInk</span><span>·</span><span>2026.05.22</span>
    </div>
  </div>
  <div class="foot">
    <div>Page 10 · 核心金句</div>
    <div>— · —</div>
  </div>
</section>

<!-- ======== Page 11: Closing ======== -->
<section class="slide hero dark">
  <div class="chrome">
    <div>CLOSING · 收束</div>
    <div>11 / 11</div>
  </div>
  <div class="frame" style="display:grid; gap:6vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Takeaway</div>
    <h1 class="h-hero" style="font-size:7vw; line-height:1.15">
      <span data-anim style="display:block">把重复交给 AI，</span>
      <span data-anim style="display:block">聚焦深度分析和决策。</span>
    </h1>
    <p class="lead" style="max-width:50vw" data-anim>
      Build Agents. Run Smarter. —— 掌握 Agent，让 AI 成为你的深度搭档。
    </p>
  </div>
  <div class="foot">
    <div>研墨 ResearchInk · 2026-05-22</div>
    <div>— END —</div>
  </div>
</section>
"""

# Read template
with open(TEMPLATE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace theme with Indigo Porcelain
old_theme_start = html.find("/* ============ 主题色(默认:")
if old_theme_start < 0:
    old_theme_start = html.find("--ink:#0a0a0b;")
    old_theme_end = html.find("--ink-tint:#18181a;") + len("--ink-tint:#18181a;")
    html = html[:old_theme_start] + INDIGO_THEME + html[old_theme_end:]
else:
    old_theme_end = html.find("--ink-tint:#18181a;", old_theme_start) + len("--ink-tint:#18181a;")
    html = html[:old_theme_start] + INDIGO_THEME + html[old_theme_end:]

# 2. Replace title
html = html.replace("[必填] 替换为 PPT 标题 · Deck Title", "AI Agent 深度培训手册 · 研墨 ResearchInk")

# 3. Replace SLIDES_HERE with our slides
placeholder = "<!-- SLIDES_HERE -->"
if placeholder in html:
    html = html.replace(placeholder, SLIDES)
else:
    # Find the deck div and insert before its closing
    deck_close = html.find("</div>", html.find('<div id="deck">'))
    html = html[:deck_close] + SLIDES + "\n" + html[deck_close:]

# Clean up remaining [必填] in comments only
# (these are harmless CSS comments, not visible)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

# Count slides and check
import re
count = len(re.findall(r'<section class="slide', html))
print(f"Generated: {OUTPUT}")
print(f"Lines: {html.count(chr(10))}")
print(f"Size: {len(html.encode('utf-8'))} bytes")
print(f"Slide sections: {count}")
remaining = html.count("[必填]")
print(f"Placeholders [必填]: {remaining} (in CSS comments)")

# Clean up temp
os.remove(TEMPLATE)
