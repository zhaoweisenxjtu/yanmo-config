#!/bin/bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
err()   { echo -e "${RED}[ERR]${NC} $1"; exit 1; }

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  研墨配置包 — 一键安装${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Check OpenClaw
command -v openclaw >/dev/null 2>&1 || err "请先安装 OpenClaw:\n  curl -fsSL https://get.openclaw.ai | bash"
info "✓ OpenClaw 已安装"

# 2. Detect install source (GitHub / Gitee / local)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$SCRIPT_DIR/VERSION" ] && [ -f "$SCRIPT_DIR/workspace/AGENTS.md" ]; then
  info "本地安装模式: $SCRIPT_DIR"
  CONFIG_DIR="$SCRIPT_DIR"
else
  # Remote install — clone the repo
  CONFIG_DIR="${HOME}/.yanmo-config"
  if [ -d "$CONFIG_DIR/.git" ]; then
    info "配置仓库已存在，更新中..."
    cd "$CONFIG_DIR" && git pull --ff-only
  else
    info "克隆配置仓库..."
    GIT_URLS=(
      "https://github.com/zhaoweisenxjtu/yanmo-config.git"
      "https://gitee.com/zhaoweisenxjtu/yanmo-config.git"
    )
    CLONED=false
    for url in "${GIT_URLS[@]}"; do
      if git clone --depth 1 "$url" "$CONFIG_DIR" 2>/dev/null; then
        CLONED=true; break
      fi
    done
    $CLONED || err "无法克隆配置仓库，请检查网络或手动下载"
  fi
fi

cd "$CONFIG_DIR"
VERSION=$(cat VERSION 2>/dev/null || echo "unknown")
info "配置版本: $VERSION"

# 3. Install workspace files
info "安装角色配置文件..."
mkdir -p ~/.openclaw/workspace
for f in workspace/*.md; do
  [ -f "$f" ] && cp "$f" ~/.openclaw/workspace/
done
[ -d workspace/scripts ] && cp -r workspace/scripts ~/.openclaw/workspace/
[ -d workspace/styles ] && cp -r workspace/styles ~/.openclaw/workspace/
[ -d workspace/.learnings ] && cp -r workspace/.learnings ~/.openclaw/workspace/
[ -d workspace/deliverables ] && cp -r workspace/deliverables ~/.openclaw/workspace/
ok "角色配置已安装"

# 4. Install config template (don't overwrite existing keys)
if [ ! -f ~/.openclaw/openclaw.json ]; then
  if [ -f openclaw.json.example ]; then
    cp openclaw.json.example ~/.openclaw/openclaw.json
    info "已创建 openclaw.json 模板，请填入 API 密钥"
  fi
fi

# 5. Install skills from registries
info "安装必备技能..."
SKILLS=(
  "pptx-master"
  "frontend-slides"
  "guizang-ppt-skill"
  "business-plan"
  "academic-deep-research"
  "multi-search-engine"
  "kdocs-skill"
  "tencent-docs"
)
for skill in "${SKILLS[@]}"; do
  echo -n "  → $skill ... "
  if openclaw skill install "$skill" >/dev/null 2>&1; then
    ok "✓"
  elif clawhub install "$skill" >/dev/null 2>&1; then
    ok "✓"
  else
    echo "⚠ 跳过（可能已存在或网络不可达）"
  fi
done

# 6. Install fonts
info "安装中文字体..."
apt install -y fonts-noto-cjk fonts-noto-cjk-extra 2>/dev/null && ok "✓" || \
  yum install -y google-noto-cjk-fonts 2>/dev/null && ok "✓" || \
  echo "  ⚠ 请手动安装: apt install fonts-noto-cjk"

# 7. Register yanmo-config command
mkdir -p ~/.local/bin
if [ ! -f ~/.local/bin/yanmo-config ]; then
  cat > ~/.local/bin/yanmo-config << 'CMD'
#!/bin/bash
case "${1:-}" in
  update)
    echo "更新研墨配置..."
    cd ~/.yanmo-config && git pull && exec bash install.sh
    ;;
  status|version)
    echo "研墨配置版本: $(cat ~/.yanmo-config/VERSION 2>/dev/null || echo unknown)"
    ;;
  help|*)
    echo "用法: yanmo-config {update|status|help}"
    ;;
esac
CMD
  chmod +x ~/.local/bin/yanmo-config
  ok "已注册 yanmo-config 命令"
fi

echo ""
ok "✅ 研墨配置 v${VERSION} 安装完成！"
echo ""
echo "  下一步:"
echo "  1. 配置 API 密钥 → openclaw configure"
echo "  2. 重启生效     → openclaw gateway restart"
echo "  3. 日后更新     → yanmo-config update"
