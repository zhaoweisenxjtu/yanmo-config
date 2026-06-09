# TOOLS.md

## 金山文档上传规则（硬性）

### 上传流程
1. 搜索：`kdocs-cli drive search-files keyword="<文件名>" parent_id=`
2. 有结果 → 提取 file_id 覆盖更新；无结果 → 新建上传
3. 获取链接并返回用户

### 上传命令
```bash
# 新建
kdocs-cli drive upload-file '{"drive_id":"666377180","parent_id":"sGw3X9j8N1Mj3aCkCeaCrx3mtgVfzkjqe","name":"文件名.pptx"}'
# 覆盖
kdocs-cli drive upload-file '{"file_id":"xxx","content_base64":"..."}'
```

### 清理
- 任务完成后检查 claw 文件夹冗余版本
- 旧版本移入 _旧版本_可删除 文件夹

## 搜索配置

⚠️ 内置 `web_search`（SearXNG）已停用。默认搜索使用 `multi-search-engine` 技能模式。

`web_fetch` 直接调用搜索引擎 URL。见 `skills/web-tools-guide/SKILL.md` 的引擎 URL 表。

**搜索流程**：
1. 无确切 URL → 选搜索引擎 URL 发给 `web_fetch`
2. 有确切 URL → 直接 `web_fetch`
3. 优先顺序：多引擎搜索(web_fetch) > web_fetch(已知URL) > opencli > browser

失败重试：同一个关键词换引擎静默重试，无需告知用户。全部失败再降级。

---

## Tavily Search（仅主动要求时使用）

- **API Key**: 已配置到 `~/.openclaw/.env` `TAVILY_API_KEY`
- **使用条件**: 仅当用户明确要求「用 Tavily 搜索」时才启用，不得自动替代 web_search
- **命令**:
  ```bash
  python3 ~/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py --query "..." --max-results 5 --format bravery
  ```
- **每月统计**: 每次使用后，在 `.tavily_usage.md` 追加记录并更新当月合计

## 设计前置规则（硬性规则）

制作任何视觉交付物（docx/HTML/PPT/前端页面等）前，必须先执行：

```
read skills/anthropic-official-frontend-design/SKILL.md
```

这是 Anthropic 官方（140K⭐）的设计指导技能。在骨架规划后、内容执行前，必须参考它选定设计方向和美学规范。

---

## 工作目录

```
deliverables/     → 最终产物
  methodology/    → 行业研究方法论
temp/             → 临时文件（可清理）
scripts/          → Python 工具库
research/         → 研究资料（按主题分目录）
memory/           → 按日期记忆文件
.learnings/       → 自我改进日志（不动）
```
