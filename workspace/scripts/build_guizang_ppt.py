#!/usr/bin/env python3
"""Generate guizang Swiss-style HTML PPT from template."""
import re

TEMPLATE = "/tmp/template_clean.html"
OUTPUT = "/root/.openclaw/workspace/deliverables/guizang-ppt/ppt/index.html"

INDIGO_THEME = """    /* ============ 主题色(🌊 靛蓝瓷 · 科技/研究/AI) ============ */
    --paper:#fafaf8;
    --paper-rgb:250,250,248;
    --ink:#0a0a0a;
    --ink-rgb:10,10,10;
    --grey-1:#f0f0ee;
    --grey-2:#d4d4d2;
    --grey-3:#737373;
    --accent:#0a1f3d;
    --accent-rgb:10,31,61;
    --accent-on:#ffffff;"""

SLIDES = """
<!-- ======== Slide 1: Cover ======== -->
<section class="slide accent" data-animate="hero" data-layout="S01">
  <div class="canvas-card">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min">
      <div class="l">AI AGENT 深度培训手册 · FIELD NOTE</div>
      <div class="r">01 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.6vh">
      <div data-anim="kicker" class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">DEEP TRAINING · AI AGENT</div>
      <h1 data-anim="title" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(11.6vw,19vh);line-height:.94;letter-spacing:-.025em;color:#fff">AI Agent <span style="font-style:italic;font-weight:300">深度培训</span><br/>手册</h1>
      <div data-anim="bottom" style="display:grid;grid-template-rows:auto auto;gap:1.6vh;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh">
        <div data-anim="lead" class="lead" style="max-width:52ch;color:rgba(255,255,255,.86)">大模型 · Agent 架构 · 工作台对比 · 场景配置 · 系统掌握 AI Agent 技术栈</div>
        <div style="display:flex;justify-content:space-between;align-items:end">
          <div class="t-meta" style="color:rgba(255,255,255,.6)">研墨 ResearchInk · 2026-05-22 · 数据截止 2026-05-22</div>
          <div class="t-meta" style="color:rgba(255,255,255,.6)">→ swipe / arrow keys</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 2: Development Milestones ======== -->
<section class="slide dark" data-animate="vertical-timeline" data-layout="S02">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">MILESTONES</div>
      <div class="r">02 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:3vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 01</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">大模型发展里程碑</h2>
        <div class="rule thick" style="opacity:.85;margin-top:1vh"></div>
      </div>
      <div data-anim="timeline" class="timeline-v" style="display:flex;flex-direction:column;gap:0">
        <div class="tl-node" style="display:grid;grid-template-columns:12vw 1fr;gap:2vw;align-items:start;padding:1.8vh 0;border-top:1px solid rgba(255,255,255,.16)">
          <div class="dot" style="width:12px;height:12px;background:var(--accent);border-radius:0;margin-top:.6vh;position:relative">
            <div style="position:absolute;left:20px;top:-4px;font-family:var(--mono);font-size:max(14px,1vw);letter-spacing:.1em;white-space:nowrap;color:rgba(255,255,255,.7)">2017</div>
          </div>
          <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);margin-bottom:.4vh">Transformer 架构</h3><p style="font-weight:300;font-size:max(16px,.94vw);color:rgba(255,255,255,.7)">Google 发表 "Attention Is All You Need"</p></div>
        </div>
        <div class="tl-node" style="display:grid;grid-template-columns:12vw 1fr;gap:2vw;align-items:start;padding:1.8vh 0;border-top:1px solid rgba(255,255,255,.16)">
          <div class="dot" style="width:12px;height:12px;background:var(--accent);border-radius:0;margin-top:.6vh;position:relative">
            <div style="position:absolute;left:20px;top:-4px;font-family:var(--mono);font-size:max(14px,1vw);letter-spacing:.1em;white-space:nowrap;color:rgba(255,255,255,.7)">2020</div>
          </div>
          <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);margin-bottom:.4vh">GPT-3 发布 (175B)</h3><p style="font-weight:300;font-size:max(16px,.94vw);color:rgba(255,255,255,.7)">参数规模突破千亿，few-shot 能力被发现</p></div>
        </div>
        <div class="tl-node" style="display:grid;grid-template-columns:12vw 1fr;gap:2vw;align-items:start;padding:1.8vh 0;border-top:1px solid rgba(255,255,255,.16)">
          <div class="dot" style="width:12px;height:12px;background:var(--accent);border-radius:0;margin-top:.6vh;position:relative">
            <div style="position:absolute;left:20px;top:-4px;font-family:var(--mono);font-size:max(14px,1vw);letter-spacing:.1em;white-space:nowrap;color:rgba(255,255,255,.7)">2022</div>
          </div>
          <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);margin-bottom:.4vh">ChatGPT 发布</h3><p style="font-weight:300;font-size:max(16px,.94vw);color:rgba(255,255,255,.7)">LLM 进入大众视野，对话式 AI 爆发</p></div>
        </div>
        <div class="tl-node" style="display:grid;grid-template-columns:12vw 1fr;gap:2vw;align-items:start;padding:1.8vh 0;border-top:1px solid rgba(255,255,255,.16)">
          <div class="dot" style="width:12px;height:12px;background:var(--accent);border-radius:0;margin-top:.6vh;position:relative">
            <div style="position:absolute;left:20px;top:-4px;font-family:var(--mono);font-size:max(14px,1vw);letter-spacing:.1em;white-space:nowrap;color:rgba(255,255,255,.7)">2023</div>
          </div>
          <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);margin-bottom:.4vh">GPT-4 / Claude / Gemini</h3><p style="font-weight:300;font-size:max(16px,.94vw);color:rgba(255,255,255,.7)">多模态、长上下文、Agent 能力涌现</p></div>
        </div>
        <div class="tl-node" style="display:grid;grid-template-columns:12vw 1fr;gap:2vw;align-items:start;padding:1.8vh 0;border-top:1px solid rgba(255,255,255,.16);border-bottom:1px solid var(--accent)">
          <div class="dot" style="width:12px;height:12px;background:var(--accent);border-radius:0;margin-top:.6vh;position:relative">
            <div style="position:absolute;left:20px;top:-4px;font-family:var(--mono);font-size:max(14px,1vw);letter-spacing:.1em;white-space:nowrap;color:rgba(255,255,255,.7)">2024-26</div>
          </div>
          <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);margin-bottom:.4vh;color:var(--accent-bright)">高级推理时代 · Agent 生态爆发</h3><p style="font-weight:300;font-size:max(16px,.94vw);color:rgba(255,255,255,.7)">DeepSeek V4 · GPT-5 · Claude Opus 4 · 自主 Agent 成熟</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 3: Agent Core Formula - Six Cells ======== -->
<section class="slide" data-animate="six-cells" data-layout="S04">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">CORE FORMULA</div>
      <div class="r">03 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 01 · AGENT = LLM + PLANNING + TOOL USE + MEMORY</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">Agent 核心公式</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.6vw;flex:1;align-content:start">
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="brain" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">LLM 大脑</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">核心推理引擎，理解意图、拆解任务、生成回复。GPT-5 · Claude 4 · DeepSeek V4</p>
        </div>
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="list-checks" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">Planning 规划</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">将复杂目标拆解为可执行的步骤序列。ReAct · Plan-and-Execute · ToT</p>
        </div>
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="wrench" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">Tool Use 工具</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">调用外部 API、搜索、计算器。Function Calling · MCP 协议 · 插件系统</p>
        </div>
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="database" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">Memory 记忆</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">存储过往对话、用户偏好、领域知识。向量数据库 · 文件系统 · RAG</p>
        </div>
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="git-branch" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">Function Calling</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">让 LLM 结构化调用预定义函数的机制，Agent 连接外部世界的桥梁</p>
        </div>
        <div class="card-fill" style="padding:2.4vh 2vw;display:flex;flex-direction:column;gap:1.2vh">
          <div style="display:flex;align-items:center;gap:.8vw"><i data-lucide="network" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i><h3 style="font-weight:500;font-size:max(18px,1.4vw);color:var(--accent)">MCP 协议</h3></div>
          <p style="font-weight:300;font-size:max(16px,.9vw);color:var(--text-secondary);line-height:1.5">Model Context Protocol，标准化工具连接协议，让 Agent 即插即用</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 4: Agent Levels ======== -->
<section class="slide grey" data-animate="three-layers" data-layout="S05">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">AGENT LEVELS</div>
      <div class="r">04 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 01 · 自主度分级 L0–L4</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">Agent 自主度分级</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="layers" style="display:grid;grid-template-rows:auto auto auto;gap:1.6vh;flex:1;align-content:start">
        <div style="display:grid;grid-template-columns:4em 4em 1fr;gap:1.2vw;align-items:center;padding:1.4vh 1.6vw;background:var(--paper);border-left:3px solid var(--accent)">
          <div style="font-family:var(--mono);font-size:max(14px,1.2vw);font-weight:600;color:var(--accent)">L0·L1</div>
          <div class="t-meta" style="font-size:max(14px,.9vw)">基础层</div>
          <div><span style="font-weight:400;font-size:max(16px,1vw)">无 Agent / 工具调用 Agent</span><br/><span style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">单轮问答 / LLM + Function Calling · ChatGPT · Assistants API</span></div>
        </div>
        <div style="display:grid;grid-template-columns:4em 4em 1fr;gap:1.2vw;align-items:center;padding:1.4vh 1.6vw;background:var(--paper);border-left:3px solid var(--accent)">
          <div style="font-family:var(--mono);font-size:max(14px,1.2vw);font-weight:600;color:var(--accent)">L2·L3</div>
          <div class="t-meta" style="font-size:max(14px,.9vw)">自动化层</div>
          <div><span style="font-weight:400;font-size:max(16px,1vw)">自主 Agent / 多 Agent 协作</span><br/><span style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">多步规划 + 循环执行 / 多角色分工 · AutoGPT · OpenClaw · CrewAI</span></div>
        </div>
        <div style="display:grid;grid-template-columns:4em 4em 1fr;gap:1.2vw;align-items:center;padding:1.4vh 1.6vw;background:var(--accent);color:var(--accent-on);border-left:3px solid var(--accent)">
          <div style="font-family:var(--mono);font-size:max(14px,1.2vw);font-weight:600">L4</div>
          <div class="t-meta" style="font-size:max(14px,.9vw);color:rgba(255,255,255,.7)">进化层</div>
          <div><span style="font-weight:400;font-size:max(16px,1vw)">自进化 Agent</span><br/><span style="font-weight:300;font-size:max(14px,.84vw);color:rgba(255,255,255,.75)">从经验中学习、自动改进行为 · OpenClaw self-improving · 持续进化</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 5: LLM Capabilities Bar Chart ======== -->
<section class="slide" data-animate="bar-chart" data-layout="S07">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">MODEL CAPABILITIES</div>
      <div class="r">05 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 02 · 模型能力边界</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">LLM 核心能力边界</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="bars" class="bar-chart" style="display:flex;flex-direction:column;gap:1.6vh;justify-content:center;flex:1">
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">自然语言</div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--accent);position:absolute;left:0;top:0;width:98%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">98%</div>
        </div>
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">代码编写</div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--accent);position:absolute;left:0;top:0;width:92%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">92%</div>
        </div>
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">逻辑推理</div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--accent);position:absolute;left:0;top:0;width:85%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">85%</div>
        </div>
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">知识问答</div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--accent);position:absolute;left:0;top:0;width:88%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">88%</div>
        </div>
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">联网搜索</div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--grey-3);position:absolute;left:0;top:0;width:45%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">45%</div>
        </div>
        <div class="bar-row" style="display:grid;grid-template-columns:8em 1fr 3em;gap:1.4vw;align-items:center">
          <div class="bar-label" style="font-family:var(--mono);font-size:max(14px,.84vw);letter-spacing:.1em;opacity:.7">私有知识<br/><span style="letter-spacing:0;font-size:max(12px,.7vw)">(需RAG)</span></div>
          <div class="bar-track" style="height:16px;background:rgba(127,127,127,.12);position:relative"><div class="bar-fill" style="height:100%;background:var(--grey-3);position:absolute;left:0;top:0;width:30%"></div></div>
          <div class="bar-value" style="font-weight:400;font-size:max(16px,1.05vw);text-align:right;font-feature-settings:'tnum'">30%</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 6: LLM KPI Tower ======== -->
<section class="slide dark" data-animate="kpi-tower" data-layout="S06">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">MODEL RANKING</div>
      <div class="r">06 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em;color:rgba(255,255,255,.7)">CHAPTER 02 · 2026 全球主流 LLM</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200;color:var(--paper)">全球大模型排行</h2>
        <div class="rule thick" style="opacity:.85"></div>
      </div>
      <div data-anim="tower" class="kpi-tower-row" style="display:grid;grid-template-columns:repeat(4,1fr);gap:2vw;flex:1;align-items:end;padding-bottom:4vh">
        <div style="display:flex;flex-direction:column;align-items:center;gap:1.2vh">
          <div style="background:var(--accent);width:100%;height:36vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.6vw">
            <div style="font-weight:200;font-size:min(5.6vw,10vh);line-height:.9;color:#fff;margin-bottom:1vh">GPT<br/>5.x</div>
          </div>
          <div class="t-meta" style="font-size:max(14px,.84vw);text-align:center;color:rgba(255,255,255,.6)">OpenAI<br/>多模态旗舰</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:1.2vh">
          <div style="background:var(--accent);width:100%;height:30vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.6vw">
            <div style="font-weight:200;font-size:min(5.6vw,10vh);line-height:.9;color:#fff;margin-bottom:1vh">Claude<br/>Opus 4</div>
          </div>
          <div class="t-meta" style="font-size:max(14px,.84vw);text-align:center;color:rgba(255,255,255,.6)">Anthropic<br/>编码·安全</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:1.2vh">
          <div style="background:var(--accent);width:100%;height:32vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.6vw">
            <div style="font-weight:200;font-size:min(5.6vw,10vh);line-height:.9;color:#fff;margin-bottom:1vh">Deep<br/>Seek V4</div>
          </div>
          <div class="t-meta" style="font-size:max(14px,.84vw);text-align:center;color:rgba(255,255,255,.6)">深度求索<br/>开源领先</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:1.2vh">
          <div style="background:var(--accent);width:100%;height:26vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.6vw">
            <div style="font-weight:200;font-size:min(5.6vw,10vh);line-height:.9;color:#fff;margin-bottom:1vh">Gemini<br/>3</div>
          </div>
          <div class="t-meta" style="font-size:max(14px,.84vw);text-align:center;color:rgba(255,255,255,.6)">Google<br/>长上下文</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 7: AI Workbench Matrix ======== -->
<section class="slide" data-animate="matrix" data-layout="S15">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">WORKBENCH MATRIX</div>
      <div class="r">07 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 03 · 全球 Top AI 工作台</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">AI 工作台能力矩阵</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="matrix-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.6vw;flex:1;align-content:start">
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh;border-top:2px solid var(--accent)">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw);color:var(--accent)">OpenClaw</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">374K ⭐</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary);line-height:1.4">全栈 Agent 框架，L0-L4 全覆盖</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">Dify</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">142K ⭐</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">LLMOps 平台，可视化工作流</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">LangChain</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">137K ⭐</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">LLM 应用开发框架生态</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">AutoGPT</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">184K ⭐</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">自主 Agent 先驱，多步任务自动执行</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">ChatGPT</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">闭源</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">对话AI标杆，Agent 能力逐步开放</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">Claude Code</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">闭源</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">终端原生 Agent，编码利器</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">Cursor</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">闭源</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">AI 原生 IDE，Agent 深入代码</p>
        </div>
        <div class="card-fill" style="padding:2vh 1.6vw;display:flex;flex-direction:column;gap:.6vh">
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">n8n</h3>
          <div class="t-meta" style="font-size:max(12px,.7vw)">189K ⭐</div>
          <p style="font-weight:300;font-size:max(14px,.8vw);color:var(--text-secondary)">工作流自动化，AI 节点扩展</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 8: Memory System Loop ======== -->
<section class="slide grey" data-animate="loop-form" data-layout="S14">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">MEMORY SYSTEM</div>
      <div class="r">08 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 01 · 区分"真 Agent"和"纯聊天机器人"的关键</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">Agent 记忆系统</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="loop" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.6vw;flex:1;align-content:center">
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center">
          <div style="width:6vw;height:6vw;border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;background:var(--paper)">
            <i data-lucide="cpu" style="width:2.5vw;height:2.5vw;stroke-width:1.5;color:var(--accent)"></i>
          </div>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">工作记忆</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">当前会话上下文<br/>+ 检索到的长期记忆</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center">
          <div style="width:6vw;height:6vw;border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;background:var(--grey-1)">
            <i data-lucide="file-text" style="width:2.5vw;height:2.5vw;stroke-width:1.5;color:var(--accent)"></i>
          </div>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">短期记忆</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">当前对话历史<br/>顺序访问，全量加载</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center">
          <div style="width:6vw;height:6vw;border:2px solid var(--accent);display:flex;align-items:center;justify-content:center;background:var(--paper)">
            <i data-lucide="hard-drive" style="width:2.5vw;height:2.5vw;stroke-width:1.5;color:var(--accent)"></i>
          </div>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">长期记忆</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">跨会话持久化<br/>向量数据库 + 文件系统</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center;grid-column:1">
          <div class="t-meta" style="color:var(--accent);font-size:max(14px,.84vw)">← 检索增强</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center">
          <div style="display:flex;gap:.8vw;align-items:center">
            <i data-lucide="arrow-right" style="width:1.5vw;height:1.5vw;stroke-width:2;color:var(--accent)"></i>
            <span class="t-meta" style="font-size:max(14px,.84vw)">RAG 检索</span>
            <i data-lucide="arrow-right" style="width:1.5vw;height:1.5vw;stroke-width:2;color:var(--accent)"></i>
          </div>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary)">文件记忆 · 向量DB · 知识图谱三套方案</p>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.6vh;align-items:center;text-align:center;grid-column:3">
          <div class="t-meta" style="font-size:max(14px,.84vw)">持久化存储 →</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 9: Workflow Patterns Timeline ======== -->
<section class="slide" data-animate="horizontal-timeline" data-layout="S11">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">WORKFLOW PATTERNS</div>
      <div class="r">09 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 01 · 四种 Agent 工作流模式</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">Agent 工作流模式</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="timeline-h" class="timeline-h" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.6vw;flex:1;align-content:start;padding-top:2vh">
        <div style="display:flex;flex-direction:column;gap:1.2vh;padding:2vh 1.6vw;background:var(--grey-1);position:relative">
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);letter-spacing:.16em">PATTERN 01</div>
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">ReAct</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.4">思考(Thought)→行动(Action)→观察(Observation)循环迭代</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--text-helper);margin-top:auto">OpenClaw · LangChain · AutoGPT</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.2vh;padding:2vh 1.6vw;background:var(--grey-1);position:relative">
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);letter-spacing:.16em">PATTERN 02</div>
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">Plan-and-Execute</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.4">先制定完整多步计划，再逐步执行检查</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--text-helper);margin-top:auto">LangGraph · TaskFlow</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.2vh;padding:2vh 1.6vw;background:var(--grey-1);position:relative">
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);letter-spacing:.16em">PATTERN 03</div>
          <h3 style="font-weight:500;font-size:max(16px,1.2vw)">Reflection 反思</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.4">自我评估→发现错误/遗漏→修正→交付</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--text-helper);margin-top:auto">OpenClaw 自改进 · Self-critique</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:1.2vh;padding:2vh 1.6vw;background:var(--accent);color:var(--accent-on);position:relative">
          <div class="t-meta" style="font-size:max(12px,.7vw);color:rgba(255,255,255,.7);letter-spacing:.16em">PATTERN 04</div>
          <h3 style="font-weight:500;font-size:max(16px,1.2vw);color:#fff">Multi-Agent</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:rgba(255,255,255,.78);line-height:1.4">多角色分工协作，各司其职</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:rgba(255,255,255,.6);margin-top:auto">CrewAI · MetaGPT · OpenClaw Sub-agents</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 10: OpenClaw Architecture ======== -->
<section class="slide dark" data-animate="system-diagram" data-layout="S17">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">OPENCLAW ARCHITECTURE</div>
      <div class="r">10 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em;color:rgba(255,255,255,.7)">CHAPTER 04 · OpenClaw 系统架构全景</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200;color:var(--paper)">OpenClaw 架构</h2>
        <div class="rule thick" style="opacity:.85"></div>
      </div>
      <div data-anim="system" style="display:grid;grid-template-rows:auto auto auto;gap:2vh;flex:1;align-content:start">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.6vw">
          <div style="background:rgba(255,255,255,.08);padding:2vh 1.6vw;text-align:center;border-top:2px solid var(--accent)">
            <i data-lucide="message-square" style="width:2vw;height:2vw;stroke-width:1.5;margin-bottom:.8vh;color:var(--accent-bright)"></i>
            <h3 style="font-weight:400;font-size:max(16px,1.2vw);margin-bottom:.4vh">微信 / Telegram</h3>
            <p style="font-weight:300;font-size:max(14px,.84vw);color:rgba(255,255,255,.6)">多渠道消息接入</p>
          </div>
          <div style="background:rgba(255,255,255,.08);padding:2vh 1.6vw;text-align:center;border-top:2px solid var(--accent)">
            <i data-lucide="globe" style="width:2vw;height:2vw;stroke-width:1.5;margin-bottom:.8vh;color:var(--accent-bright)"></i>
            <h3 style="font-weight:400;font-size:max(16px,1.2vw);margin-bottom:.4vh">Discord / Matrix</h3>
            <p style="font-weight:300;font-size:max(14px,.84vw);color:rgba(255,255,255,.6)">多平台消息路由</p>
          </div>
          <div style="background:rgba(255,255,255,.08);padding:2vh 1.6vw;text-align:center;border-top:2px solid var(--accent)">
            <i data-lucide="smartphone" style="width:2vw;height:2vw;stroke-width:1.5;margin-bottom:.8vh;color:var(--accent-bright)"></i>
            <h3 style="font-weight:400;font-size:max(16px,1.2vw);margin-bottom:.4vh">CLI / API</h3>
            <p style="font-weight:300;font-size:max(14px,.84vw);color:rgba(255,255,255,.6)">开发者直接接入</p>
          </div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:1vw">
          <div class="t-meta" style="color:rgba(255,255,255,.5)">用户层</div>
          <i data-lucide="arrow-down" style="width:1.2vw;height:1.2vw;stroke-width:1.5;color:var(--accent)"></i>
          <div style="width:40%;height:1px;background:var(--accent);opacity:.5"></div>
          <i data-lucide="arrow-down" style="width:1.2vw;height:1.2vw;stroke-width:1.5;color:var(--accent)"></i>
          <div class="t-meta" style="color:rgba(255,255,255,.5)">Agent 层</div>
          <i data-lucide="arrow-down" style="width:1.2vw;height:1.2vw;stroke-width:1.5;color:var(--accent)"></i>
          <div style="width:40%;height:1px;background:var(--accent);opacity:.5"></div>
          <i data-lucide="arrow-down" style="width:1.2vw;height:1.2vw;stroke-width:1.5;color:var(--accent)"></i>
          <div class="t-meta" style="color:rgba(255,255,255,.5)">工具层</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:1.6vw">
          <div style="background:var(--accent);padding:1.6vh 1.2vw;text-align:center">
            <i data-lucide="brain" style="width:1.5vw;height:1.5vw;stroke-width:1.5;margin-bottom:.4vh;color:rgba(255,255,255,.9)"></i>
            <h3 style="font-weight:400;font-size:max(14px,.9vw);color:#fff">推理引擎</h3>
            <p style="font-weight:300;font-size:max(12px,.7vw);color:rgba(255,255,255,.7)">DeepSeek V4</p>
          </div>
          <div style="background:var(--accent);padding:1.6vh 1.2vw;text-align:center">
            <i data-lucide="list-checks" style="width:1.5vw;height:1.5vw;stroke-width:1.5;margin-bottom:.4vh;color:rgba(255,255,255,.9)"></i>
            <h3 style="font-weight:400;font-size:max(14px,.9vw);color:#fff">任务编排</h3>
            <p style="font-weight:300;font-size:max(12px,.7vw);color:rgba(255,255,255,.7)">TaskFlow</p>
          </div>
          <div style="background:var(--accent);padding:1.6vh 1.2vw;text-align:center">
            <i data-lucide="hard-drive" style="width:1.5vw;height:1.5vw;stroke-width:1.5;margin-bottom:.4vh;color:rgba(255,255,255,.9)"></i>
            <h3 style="font-weight:400;font-size:max(14px,.9vw);color:#fff">记忆系统</h3>
            <p style="font-weight:300;font-size:max(12px,.7vw);color:rgba(255,255,255,.7)">LanceDB</p>
          </div>
          <div style="background:var(--accent);padding:1.6vh 1.2vw;text-align:center">
            <i data-lucide="tool" style="width:1.5vw;height:1.5vw;stroke-width:1.5;margin-bottom:.4vh;color:rgba(255,255,255,.9)"></i>
            <h3 style="font-weight:400;font-size:max(14px,.9vw);color:#fff">MCP 工具</h3>
            <p style="font-weight:300;font-size:max(12px,.7vw);color:rgba(255,255,255,.7)">万能连接器</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 11: Scenario Config Four Cards ======== -->
<section class="slide" data-animate="four-cards" data-layout="S19">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">SCENARIO CONFIG</div>
      <div class="r">11 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">CHAPTER 05 · 行业场景配置指南</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">场景配置</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="cards" style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.6vw;flex:1;align-content:start">
        <div class="card-fill" style="padding:2.4vh 1.6vw;display:flex;flex-direction:column;gap:1.2vh;border-top:2px solid var(--accent)">
          <i data-lucide="search" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">行业研究</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.5">架构：十层分析体系<br/>工具：web_search + web_fetch<br/>输出：PPT / 研究报告</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);margin-top:auto">深度优先</div>
        </div>
        <div class="card-fill" style="padding:2.4vh 1.6vw;display:flex;flex-direction:column;gap:1.2vh;border-top:2px solid var(--accent)">
          <i data-lucide="presentation" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">PPT 制作</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.5">引擎：pptx-master<br/>风格：现代品牌风<br/>输出：原生可编辑 PPTX</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);margin-top:auto">输出导向</div>
        </div>
        <div class="card-fill" style="padding:2.4vh 1.6vw;display:flex;flex-direction:column;gap:1.2vh;border-top:2px solid var(--accent)">
          <i data-lucide="book-open" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">知识管理</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.5">记忆：LanceDB 向量<br/>存储：MEMORY.md<br/>自动：heartbeat 整理</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);margin-top:auto">持续积累</div>
        </div>
        <div class="card-fill" style="padding:2.4vh 1.6vw;display:flex;flex-direction:column;gap:1.2vh;border-top:2px solid var(--accent)">
          <i data-lucide="bar-chart-3" style="width:2vw;height:2vw;stroke-width:1.5;color:var(--accent)"></i>
          <h3 style="font-weight:500;font-size:max(16px,1.1vw)">数据分析</h3>
          <p style="font-weight:300;font-size:max(14px,.84vw);color:var(--text-secondary);line-height:1.5">引擎：Python 脚本<br/>可视化：SVG 图表<br/>输出：数据报告 + PPT</p>
          <div class="t-meta" style="font-size:max(12px,.7vw);color:var(--accent);margin-top:auto">数据驱动</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 12: Duo Compare ======== -->
<section class="slide grey" data-animate="split-statement" data-layout="S08">
  <div class="canvas-card">
    <div class="chrome-min">
      <div class="l">BEFORE VS AFTER</div>
      <div class="r">12 / 13</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr;gap:2.6vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta" style="letter-spacing:.22em">AGENT 生态的范式转移</div>
        <h2 class="h-xl-zh" style="font-size:min(6.4vw,11.2vh);font-weight:200">AI Agent 带来的变革</h2>
        <div class="rule" style="opacity:.4"></div>
      </div>
      <div data-anim="compare" class="duo-compare" style="display:grid;grid-template-columns:1fr 1fr;gap:2.6vw;flex:1;align-content:start">
        <div style="padding:2.4vh 2vw;background:var(--paper);border-left:3px solid var(--grey-3)">
          <div class="t-meta" style="font-size:max(14px,.9vw);color:var(--text-helper);letter-spacing:.16em;margin-bottom:1.6vh">BEFORE · 传统方式</div>
          <ul style="list-style:none;padding:0">
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="x" style="width:1.2vw;height:1.2vw;stroke-width:2;color:var(--grey-3);flex-shrink:0"></i>手动搜索信息</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="x" style="width:1.2vw;height:1.2vw;stroke-width:2;color:var(--grey-3);flex-shrink:0"></i>逐一阅读分析</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="x" style="width:1.2vw;height:1.2vw;stroke-width:2;color:var(--grey-3);flex-shrink:0"></i>手动制作 PPT</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="x" style="width:1.2vw;height:1.2vw;stroke-width:2;color:var(--grey-3);flex-shrink:0"></i>重复劳动</li>
          </ul>
        </div>
        <div style="padding:2.4vh 2vw;background:var(--paper);border-left:3px solid var(--accent)">
          <div class="t-meta" style="font-size:max(14px,.9vw);color:var(--accent);letter-spacing:.16em;margin-bottom:1.6vh">AFTER · AI Agent 时代</div>
          <ul style="list-style:none;padding:0">
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="check" style="width:1.2vw;height:1.2vw;stroke-width:2.5;color:var(--accent);flex-shrink:0"></i>Agent 自动搜索多源</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="check" style="width:1.2vw;height:1.2vw;stroke-width:2.5;color:var(--accent);flex-shrink:0"></i>结构化分析输出</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="check" style="width:1.2vw;height:1.2vw;stroke-width:2.5;color:var(--accent);flex-shrink:0"></i>一键生成 PPTX</li>
            <li style="padding:.8vh 0;border-top:1px solid var(--border-subtle);font-weight:300;font-size:max(16px,.94vw);color:var(--text-secondary);display:flex;gap:1vw;align-items:center"><i data-lucide="check" style="width:1.2vw;height:1.2vw;stroke-width:2.5;color:var(--accent);flex-shrink:0"></i>聚焦决策而非执行</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ======== Slide 13: Closing ======== -->
<section class="slide split" data-animate="split-statement" data-layout="S10">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min" style="margin-bottom:0;position:relative;z-index:1">
          <div class="l">13 / 13</div>
          <div class="r">CLOSING</div>
        </div>
        <div data-anim="manifesto" style="display:flex;flex-direction:column;gap:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em;margin-bottom:1.6vh">MANIFESTO</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-size:min(8vw,14vh);line-height:.94;letter-spacing:-.025em;font-weight:200;color:#fff">Build Agents.<br/>Run <span style="font-style:italic;font-weight:300">Smarter</span>.</h2>
          <div style="font-family:var(--sans),var(--sans-zh);font-size:max(14px,1vw);line-height:1.6;color:rgba(255,255,255,.82);font-weight:400;max-width:36ch;margin-top:1.4vh">掌握 Agent，把重复交给 AI，聚焦深度分析和决策。</div>
        </div>
        <div data-anim="signature" style="display:flex;justify-content:space-between;align-items:end;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.62)">研墨 ResearchInk</div>
          <div class="t-meta" style="color:rgba(255,255,255,.62)">2026.05.22</div>
        </div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min">
          <div class="l">TAKEAWAYS</div>
          <div class="r">03 RULES</div>
        </div>
        <div data-anim="rules" style="display:flex;flex-direction:column;gap:0">
          <div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle)">
            <div style="font-family:var(--sans);font-weight:200;font-size:min(4.4vw,7.8vh);line-height:.9;color:var(--text-primary)">01</div>
            <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);line-height:1.2;letter-spacing:-.015em;color:var(--text-primary);margin-bottom:1vh">理解 Agent 分级</h3><p style="font-weight:300;font-size:max(16px,.94vw);line-height:1.6;color:var(--text-secondary)">L0→L4 逐级递进，核心是自主度提升和记忆系统的建立</p></div>
          </div>
          <div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle)">
            <div style="font-family:var(--sans);font-weight:200;font-size:min(4.4vw,7.8vh);line-height:.9;color:var(--text-primary)">02</div>
            <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);line-height:1.2;letter-spacing:-.015em;color:var(--text-primary);margin-bottom:1vh">选对工作流模式</h3><p style="font-weight:300;font-size:max(16px,.94vw);line-height:1.6;color:var(--text-secondary)">ReAct 通用框架 + Reflection 自我修正 + Multi-Agent 复杂分工</p></div>
          </div>
          <div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle);border-bottom:2px solid var(--accent)">
            <div style="font-family:var(--sans);font-weight:200;font-size:min(4.4vw,7.8vh);line-height:.9;color:var(--accent)">03</div>
            <div><h3 style="font-weight:400;font-size:max(18px,1.8vw);line-height:1.2;letter-spacing:-.015em;color:var(--accent);margin-bottom:1vh">场景决定配置</h3><p style="font-weight:300;font-size:max(16px,.94vw);line-height:1.6;color:var(--text-secondary)">研究深度优先 → 输出导向 → 持续积累 → 数据驱动，四场景四方案</p></div>
          </div>
        </div>
        <div data-anim="foot" class="t-meta" style="color:var(--text-helper);text-align:right">→ 完 · END OF FIELD NOTE</div>
      </div>
    </div>
  </div>
</section>
"""

# Read template
with open(TEMPLATE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace theme
old_theme_start = html.find('/* ============ 主题色(默认:')
old_theme_end = html.find('--accent-on:#ffffff;', old_theme_start) + len('--accent-on:#ffffff;')
html = html[:old_theme_start] + INDIGO_THEME + html[old_theme_end:]

# Fix accent-bright for dark bg
html = html.replace('--accent-bright:#5B7BFF;', '--accent-bright:#4A7BD0;')

# 2. Replace title
html = html.replace('[必填] 替换为 PPT 标题 · Deck Title', 'AI Agent 深度培训手册 · 研墨 ResearchInk')

# 3. Replace SLIDES_HERE with our slides
placeholder = '<!-- SLIDES_HERE · 在此处粘贴 <section class="slide ..."> 页面块'
placeholder_end = html.find(placeholder)
if placeholder_end > 0:
    # Find the end of the closing </div> after the example slides
    slides_end = html.find('</div>', placeholder_end)
    slides_end = html.find('</div>', slides_end + 6)  # The deck div
    # Actually, find all example slides and replace with ours
    # The placeholder is followed by example slides and then </div> for deck
    # Let's find the actual deck closing div
    deck_close = html.find('</div>', html.find('<div id="deck">'))
    
    # Replace everything between SLIDES_HERE comment and deck closing </div>
    html = html[:placeholder_end] + "\n" + SLIDES + "\n" + html[deck_close:]

# 4. Add Lucide CDN and icon init (if not already there)
if 'lucide.createIcons' not in html:
    # Add before </body> or at end of script
    html = html.replace('</body>', 
        '<script src="https://unpkg.com/lucide@latest"></script>\n<script>lucide.createIcons();</script>\n</body>')

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {OUTPUT}")
print(f"Size: {len(html)} chars, {len(html.encode('utf-8'))} bytes")

# Check for [必填] placeholders
remaining = html.count('[必填]')
print(f"Remaining [必填] placeholders: {remaining}")
