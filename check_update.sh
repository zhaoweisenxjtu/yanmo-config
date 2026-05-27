#!/bin/bash
# 版本检查（给 install.sh 或 cron 调用）
REMOTE_VERSION=$(curl -fsSL https://raw.githubusercontent.com/zhaoweisenxjtu/yanmo-config/main/VERSION 2>/dev/null || echo "0")
LOCAL_VERSION=$(cat ~/.yanmo-config/VERSION 2>/dev/null || echo "0")
if [ "$REMOTE_VERSION" != "$LOCAL_VERSION" ]; then
  echo "新版本可用: $REMOTE_VERSION (当前: $LOCAL_VERSION)"
  echo "更新: yanmo-config update"
else
  echo "已是最新版本: $LOCAL_VERSION"
fi
