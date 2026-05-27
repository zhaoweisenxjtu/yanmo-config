# 研墨功能建议

> Capabilities requested by the user.
> Log format: [FEAT-YYYYMMDD-XXX] capability_name

---

## 2026-05-26 — fetch_illustration.py 矢量插画一键搜索下载脚本

**能力**：`scripts/fetch_illustration.py` 自动搜索并下载免费可商用 SVG 插画
**数据源**：unDraw (开源API) / Openclipart (CC0) / Storyset (Freepik许可)
**使用方式**：
- 交互式：`python3 scripts/fetch_illustration.py 关键词`
- 自动模式：`python3 scripts/fetch_illustration.py "关键词" --auto --count N -o ./目录`
- SVG 文件可直接拖入 PPT，右键"转换为形状"后改色编辑
**AGENTS.md 已更新**：配图流程新增此步骤，位于插画类（内容页大图）首选
