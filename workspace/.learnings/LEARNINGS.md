# LEARNINGS.md

## Category: best_practice

### 图标/配图获取规则 (2026-05-23)

**规则**: 当用户要求「美观」或涉及图标/配图时，禁止自行生成简约图标。必须：

1. **优先使用 mcp-universal-icons** — 60,000+ 图标库（Lucide/Material/Tabler/Heroicons/Phosphor 等），通过 MCP get_icon 获取真实 SVG
2. **切换多个素材源** — 顺序：
   - mcp-universal-icons (MCP protocol, 实时获取)
   - jsDelivr CDN (lucide-static / tabler-icons)
   - unpkg CDN (npm 包直连)
   - GitHub raw (官方仓库直接下载)
   - Font Awesome / Material Symbols CDN
3. **禁止退而求其次** — 如果某个素材源失败，换下一个，不降级为自绘简约图标
4. **下载成功后再做替换嵌入** — 不要在路经替换阶段出错时退回手写路径

**技术要点**:
- MCP server: `node /root/.openclaw/workspace/skills/mcp-universal-icons/dist/index.js`
- 调用格式: `echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_icon","arguments":{"icon_name":"xxx","collection":"lucide","format":"svg"}}}' | timeout 15 node ...`
- Lucide 图标是 stroke-based，嵌入时需要加 `fill="none" stroke="COLOR" stroke-width="1.5"`
- SVG 嵌入后必须通过 `xml.etree.ElementTree.parse()` 验证 XML 合法性
