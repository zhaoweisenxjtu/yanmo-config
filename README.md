# 🦞 研墨配置包 (ResearchInk Config)

> 赵韦森的 OpenClaw 个人配置合集 — 让研墨在新机器上原地复活

## 一键安装

```bash
bash <(curl -fsSL 'https://raw.githubusercontent.com/zhaoweisenxjtu/yanmo-config/main/install.sh')
```

国内 Gitee 加速：

```bash
bash <(curl -fsSL 'https://gitee.com/zhaoweisenxjtu/yanmo-config/raw/main/install.sh')
```

## 安装后

### 1. 配置 API 密钥

```bash
openclaw configure
```

或在 `~/.openclaw/openclaw.json` 中填入:

| 密钥 | 说明 |
|:-----|:-----|
| `plugins.entries.tokenjuice.config.apiKey` | DeepSeek V4 API 密钥 |
| `plugins.entries.kdocs-skill.config.KINGSOFT_DOCS_TOKEN` | 金山文档 Token |
| `plugins.entries.ima-skill.config.IMA_OPENAPI_APIKEY` | IMA 知识库 API 密钥 |
| `~/.openclaw/.env` 的 `TAVILY_API_KEY` | Tavily 搜索 API |

### 2. 重启

```bash
openclaw gateway restart
```

### 3. 更新配置

```bash
yanmo-config update
```

## 包含内容

| 文件 | 作用 |
|:-----|:-----|
| `workspace/AGENTS.md` | 操作指令（十层框架/SOP/字体规范）|
| `workspace/SOUL.md` | 研墨的信条与原则 |
| `workspace/IDENTITY.md` | 身份配置 |
| `workspace/USER.md` | 用户偏好设置 |
| `workspace/TOOLS.md` | 工具链规则 |
| `workspace/HEARTBEAT.md` | 心跳检查清单 |
| `workspace/styles/` | PPT 风格预设（现代品牌风等）|
| `workspace/scripts/` | 工具脚本（fetch_illustration 等）|
| `workspace/deliverables/methodology/` | 十层深度分析框架 |
| `workspace/.learnings/` | 自我改进知识库 |
| `openclaw.json.example` | 主配置模板（填密钥后用）|

## 注意事项

- ⚠️ `openclaw.json` 包含 API 密钥，**不要直接提交到 GitHub**
- 微信渠道 session 认证不能跨机器迁移，需重新 `openclaw configure`
- 建议 fork 后改 `zhaoweisenxjtu` 再使用
