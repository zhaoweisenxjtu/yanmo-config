#!/usr/bin/env python3
"""
fetch_illustration.py — 一键搜索下载免费矢量插画 (SVG)

三大数据源自动搜索，统一输出可导入 PPT 的 SVG 文件。
用法:
  python3 scripts/fetch_illustration.py 关键词 [选项]
  python3 scripts/fetch_illustration.py business meeting
  python3 scripts/fetch_illustration.py 人工智能 -c 5 -o ./ppt_images
  python3 scripts/fetch_illustration.py data center --auto  (自动下载前10个)

选项:
  --count N, -c N      展示/下载数量 (默认 10)
  --output-dir DIR, -o DIR  保存目录 (默认 ./downloads/关键词)
  --auto, -a           非交互模式自动下载
  --help, -h           显示帮助

依赖: 仅 Python 3 标准库 (urllib, json, re, os)
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# ── 配置 ──────────────────────────────────────────────────────
REQUEST_TIMEOUT = 15          # 单次请求超时秒数
MAX_RESULTS_PER_SOURCE = 15   # 每个来源最多返回结果数
CACHE_DIR = None              # 缓存目录 (None=不缓存)
DEFAULT_COUNT = 10            # 默认展示几个
OUTPUT_DIR = None             # 自动用关键词命名

# ── 辅助函数 ──────────────────────────────────────────────────

def _req(url, headers=None):
    """发起 GET 请求，返回 (data, final_url)"""
    h = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchInk/1.0; +https://github.com)",
        "Accept": "text/html,application/json,*/*",
    }
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read(), resp.geturl()


def green(msg): return f"\033[32m{msg}\033[0m"
def cyan(msg): return f"\033[36m{msg}\033[0m"
def yellow(msg): return f"\033[33m{msg}\033[0m"
def red(msg): return f"\033[31m{msg}\033[0m"
def bold(msg): return f"\033[1m{msg}\033[0m"


# ═════════════ 数据源 ═════════════

class Illustration:
    """统一的结果条目"""
    def __init__(self, title, source, svg_url, page_url, license_note=""):
        self.title = title.strip()
        self.source = source          # undraw | openclipart | storyset
        self.svg_url = svg_url        # 可直接下载的 SVG URL
        self.page_url = page_url      # 来源页面
        self.license = license_note

    def __repr__(self):
        return f"[{self.source}] {self.title}"


def _undraw_search(keyword):
    """unDraw 搜索：REST API → JSON"""
    # 短关键词补全，避免 API 400
    query = keyword.strip()
    if len(query) < 3:
        query = query + " " + query  # 如 ai → "ai ai" 让 API 正常工作
    url = f"https://undraw.co/api/search?q={urllib.parse.quote(query)}"
    try:
        data, _ = _req(url, {"Accept": "application/json"})
        body = json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 400:
            # API 不支持的短词或不识别词，跳过
            pass
        else:
            print(f"  {yellow('⚠ unDraw API 请求失败:')} {e}")
        return []
    except Exception as e:
        print(f"  {yellow('⚠ unDraw API 请求失败:')} {e}")
        return []
    results = []
    for item in body.get("results", [])[:MAX_RESULTS_PER_SOURCE]:
        svg = item.get("media", "")
        slug = item.get("newSlug", "")
        page = f"https://undraw.co/illustrations#{slug}" if slug else ""
        results.append(Illustration(
            title=item.get("title", ""),
            source="undraw",
            svg_url=svg,
            page_url=page,
            license_note="开源免费可商用 (unDraw License)"
        ))
    return results


def _openclipart_search(keyword):
    """Openclipart 搜索：解析搜索结果页 → 提取 SVG 下载链接"""
    url = f"https://openclipart.org/search/?query={urllib.parse.quote(keyword)}"
    try:
        html, _ = _req(url)
        text = html.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  {yellow('⚠ Openclipart 请求失败:')} {e}")
        return []

    # 提取形如 /detail/351527/cycle-of-technology 的链接
    detail_pattern = re.compile(r'(/detail/\d+/[^"\'\\s]+)')
    matches = detail_pattern.findall(text)
    # 去重保留顺序
    seen = set()
    links = []
    for m in matches:
        full = "https://openclipart.org" + m
        if full not in seen:
            seen.add(full)
            links.append(full)

    # 提取标题
    titles = re.findall(r'alt="([^"]*)"', text)

    results = []
    for i, page_url in enumerate(links[:MAX_RESULTS_PER_SOURCE]):
        # 构造下载 URL: /detail/351527/... → /download/351527/...svg
        download = page_url.replace("/detail/", "/download/") + ".svg"
        title = titles[i] if i < len(titles) and titles[i].strip() else page_url.split("/")[-1]
        results.append(Illustration(
            title=title,
            source="openclipart",
            svg_url=download,
            page_url=page_url,
            license_note="CC0 公共领域 — 无需署名，自由商用"
        ))
    return results


def _storyset_search(keyword):
    """Storyset 搜索：解析搜索结果页 → 详情页 → 提取 SVG CDN 链接"""
    search_url = f"https://storyset.com/search?q={urllib.parse.quote(keyword)}"
    try:
        html, _ = _req(search_url)
        text = html.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  {yellow('⚠ Storyset 请求失败:')} {e}")
        return []

    # 提取形如 /illustration/xxx/yyy 的链接
    detail_pattern = re.compile(r'(/illustration/[^"\'\\s/]+/[^"\'\\s/]+)')
    matches = detail_pattern.findall(text)
    seen = set()
    paths = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            paths.append(m)

    results = []
    for i, path in enumerate(paths[:MAX_RESULTS_PER_SOURCE]):
        detail_url = f"https://storyset.com{path}"
        try:
            time.sleep(0.3)  # 礼貌间隔
            html2, _ = _req(detail_url)
            detail_text = html2.decode("utf-8", errors="replace")
            # 提取 freepiklabs SVG CDN URL
            cdn_pattern = re.compile(r'https://stories\.freepiklabs\.com/storage/[^"\'\\s]+\.svg')
            svg_matches = cdn_pattern.findall(detail_text)
            if svg_matches:
                svg_url = svg_matches[0]
                # 提取标题
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', detail_text)
                title = title_match.group(1).strip() if title_match else path.split("/")[-1]
                # 清理标题中的 "Customizable ... Illustrations" 后缀和其他杂音
                title = re.sub(r'\s+(Customizable|Free|Illustrations?|Flat|Semi\s*Flat|Cartoon|\w+\s*Style)\s*', '', title, flags=re.IGNORECASE).strip()
                title = re.sub(r'[|/]', ' · ', title).strip()
                results.append(Illustration(
                    title=title,
                    source="storyset",
                    svg_url=svg_url,
                    page_url=detail_url,
                    license_note="Freepik License — 免费商用需署名"
                ))
        except Exception as e:
            continue

    return results


# ═════════════ 核心功能 ═════════════

def search(keyword):
    """三源并行搜索，返回统一结果列表 (已排序)"""
    keyword = keyword.strip()
    if not keyword:
        print(red("❌ 请输入搜索关键词"))
        return []

    print(f"\n{bold(f'🔍 搜索矢量插画: {keyword}')}\n{'─' * 50}")

    all_results = []

    # 1. unDraw (API 最快)
    print(f"  {cyan('⟳ unDraw 搜索中...')}")
    all_results.extend(_undraw_search(keyword))

    # 2. Openclipart
    print(f"  {cyan('⟳ Openclipart 搜索中...')}")
    all_results.extend(_openclipart_search(keyword))

    # 3. Storyset
    print(f"  {cyan('⟳ Storyset 搜索中...')}")
    all_results.extend(_storyset_search(keyword))

    # 去重：相同 SVG URL 只保留一个
    seen_urls = set()
    deduped = []
    for r in all_results:
        if r.svg_url not in seen_urls:
            seen_urls.add(r.svg_url)
            deduped.append(r)

    return deduped


def display_results(results, count=DEFAULT_COUNT):
    """打印结果表格"""
    if not results:
        print(f"\n{red('❌ 未找到任何插画，请换关键词重试')}")
        return

    total = len(results)
    show = results[:count]
    print(f"\n{green(f'✔ 共找到 {total} 个插画 (展示前 {len(show)} 个)')}\n")

    for i, r in enumerate(show, 1):
        source_tag = {
            "undraw": "unDraw  ",
            "openclipart": "OpenClip",
            "storyset": "Storyset",
        }.get(r.source, r.source)

        print(f"  {bold(f'[{i}]')} {green(source_tag)} │ {r.title}")
        print(f"      {yellow('SVG:')} {r.svg_url[:100]}{'…' if len(r.svg_url) > 100 else ''}")
        print(f"      {yellow('Web:')} {r.page_url[:100]}")
        print(f"      {yellow('许可:')} {r.license}")
        print()

    if total > count:
        print(f"  {yellow(f'… 还有 {total - count} 个未显示 (加 --count N 查看更多)')}")
    return show


def download(result, output_dir="."):
    """下载单个 SVG 文件到本地"""
    os.makedirs(output_dir, exist_ok=True)

    # 安全文件名
    safe_name = re.sub(r'[^\w\-_\. ]', '', result.title).strip().replace(" ", "_")
    if not safe_name:
        safe_name = f"illustration_{hash(result.svg_url) & 0xFFFFFF:06x}"
    filename = f"{safe_name}.svg"
    filepath = os.path.join(output_dir, filename)

    # 防重复
    counter = 1
    while os.path.exists(filepath):
        name_base = f"{safe_name}_{counter}"
        filepath = os.path.join(output_dir, f"{name_base}.svg")
        counter += 1

    try:
        data, _ = _req(result.svg_url)
        # 验证确为 SVG
        header = data[:200].decode("utf-8", errors="replace").strip().lower()
        if not (header.startswith("<?xml") or header.startswith("<svg") or "<svg" in header[:500]):
            print(f"    {red('✗ 返回内容非 SVG，跳过')}")
            return None

        with open(filepath, "wb") as f:
            f.write(data)
        size_kb = len(data) / 1024
        print(f"    {green(f'✔ 已保存: {filepath} ({size_kb:.1f} KB)')}")
        return filepath
    except Exception as e:
        print(f"    {red(f'✗ 下载失败: {e}')}")
        return None


def batch_download(results, output_dir, selection=None):
    """批量下载。selection=None 下载全部，否则下载指定索引列表（1-based）"""
    if selection is not None:
        targets = [results[i - 1] for i in selection if 1 <= i <= len(results)]
    else:
        targets = results

    if not targets:
        print(yellow("⚠ 没有选定要下载的插画"))
        return []

    print(f"\n{bold('⬇ 开始下载...')}\n{'─' * 50}")
    saved = []
    for r in targets:
        print(f"  [{r.source}] {r.title}")
        fp = download(r, output_dir)
        if fp:
            saved.append(fp)
    return saved


# ═════════════ CLI 入口 ═════════════

def print_banner():
    banner = """
╔══════════════════════════════════════════╗
║     🎨 研墨 · 矢量插画一键获取工具       ║
║     数据源: unDraw / Openclipart / Storyset  ║
╚══════════════════════════════════════════╝
"""
    print(banner)


def interactive_flow(keyword, count, output_dir):
    """搜索 → 展示 → 选择下载 → 完成"""
    results = search(keyword)
    displayed = display_results(results, count)

    if not results:
        return []

    while True:
        try:
            inp = input(f"\n{bold('⬇ 输入序号下载 (如 1,3,5; 或 a=全部; q=退出): ')}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return []

        if inp == "q":
            print(yellow("已退出"))
            return []
        if inp == "a":
            return batch_download(results, output_dir)
        # 解析序号
        try:
            indices = []
            for part in inp.replace("，", ",").split(","):
                part = part.strip()
                if not part:
                    continue
                if "-" in part:
                    start, end = part.split("-")
                    indices.extend(range(int(start), int(end) + 1))
                else:
                    indices.append(int(part))
            indices = sorted(set(indices))
            if all(1 <= i <= len(results) for i in indices):
                return batch_download(results, output_dir, indices)
            else:
                print(red(f"❌ 序号超出范围 (1-{len(results)})"))
        except ValueError:
            print(red("❌ 输入格式错误，示例: 1,3,5 或 1-5 或 a"))


def main():
    print_banner()

    # 解析命令行参数
    args = sys.argv[1:]
    keyword = ""
    count = DEFAULT_COUNT
    output_dir = None

    auto_mode = False
    i = 0
    while i < len(args):
        if args[i] in ("--count", "-c") and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] in ("--output-dir", "-o") and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] in ("--auto", "-a"):
            auto_mode = True
            i += 1
        elif args[i] in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            if keyword:
                keyword += " " + args[i]
            else:
                keyword = args[i]
            i += 1

    if not keyword:
        try:
            keyword = input(f"{bold('请输入搜索关键词: ')}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

    if not keyword:
        print(red("❌ 关键词不能为空"))
        sys.exit(1)

    # 默认输出目录: ./downloads/关键词
    if output_dir is None:
        safe_dir = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', keyword).strip("_") or "illustrations"
        output_dir = os.path.join(os.getcwd(), "downloads", safe_dir)

    if auto_mode:
        results = search(keyword)
        if results:
            saved = batch_download(results[:count], output_dir)
        else:
            saved = []
    else:
        saved = interactive_flow(keyword, count, output_dir)

    if saved:
        print(f"\n{'═' * 50}")
        print(f"{green(f'🎉 成功下载 {len(saved)} 个插画!')}")
        print(f"   {yellow('保存位置:')} {os.path.dirname(saved[0])}/")
        print(f"   {yellow('提示:')} SVG 文件可直接拖入 PPT，右键「转换为形状」即可编辑改色")
        print(f"{'═' * 50}\n")
    else:
        print(f"\n{yellow('没有下载任何文件')}\n")


if __name__ == "__main__":
    main()
