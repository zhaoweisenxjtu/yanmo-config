#!/usr/bin/env python3
"""
CodeBuddy Web Search & Fetch Skill
把 CodeBuddy 云端的 CVM Agent 当作搜索/抓取子 Agent 使用
"""
import os, sys, json, time, socket, threading, http.server
import urllib.request, urllib.parse

API_KEY = "ck_fn3pyichksu8.pl8i-Kss-DRFCc496IJFG34Y7V5ea2o9DIQsLVKAg6U"
BASE = "https://copilot.tencent.com"

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 0))
    port = s.getsockname()[1]
    s.close()
    return port

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    result = None
    received = threading.Event()
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        WebhookHandler.result = json.loads(body)
        WebhookHandler.received.set()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')
    
    def log_message(self, fmt, *args):
        pass  # 静默

def create_agent(query, webhook_url, task_type="search"):
    """创建 CodeBuddy BackgroundAgent"""
    if task_type == "fetch":
        prompt = f"""你是一个网页抓取助手。请在 CVM 终端环境中执行以下任务：
使用 curl 或 Python 抓取以下 URL 的内容：
{query}

要求：
1. 抓取网页正文内容
2. 提取有用信息
3. 返回完整结果
请将结果写出来。"""
    else:
        prompt = f"""你是一个搜索助手。请在 CVM 终端环境中执行以下搜索任务：
搜索关键词：{query}

要求：
1. 使用 curl 或 Python 进行搜索
2. 列出找到的结果（标题+链接+摘要）
3. 标注信息来源
4. 用中文返回结果

请直接返回搜索结果。"""
    
    data = json.dumps({
        "prompt": prompt,
        "sessionId": f"websearch_{int(time.time()*1000)}",
        "agentTitle": f"搜索:{query[:30]}",
        "agentOrigin": "openapi",
        "sandboxType": "cvm",
        "webhookUrl": webhook_url,
        "config": {"repoConfig": {"branch": "master"}}
    }).encode()
    
    req = urllib.request.Request(
        f"{BASE}/v2/backgroundagent/agentmgmt/agents",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    )
    
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read())
    return result.get("data", {})

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CodeBuddy Web Search/Fetch Agent")
    parser.add_argument("--query", required=True, help="搜索关键词或 URL")
    parser.add_argument("--type", choices=["search", "fetch"], default="search",
                       help="search=网页搜索, fetch=网页抓取")
    parser.add_argument("--timeout", type=int, default=120, help="等待超时(秒)")
    args = parser.parse_args()
    
    # 1. 启动本地 webhook server
    port = find_free_port()
    WebhookHandler.result = None
    WebhookHandler.received.clear()
    
    server = http.server.HTTPServer(('0.0.0.0', port), WebhookHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    
    public_ip = "124.221.148.237"
    webhook_url = f"http://{public_ip}:{port}/callback"
    
    print(f"[CodeBuddy] 启动 webhook: {webhook_url}", file=sys.stderr)
    
    # 2. 创建 Agent
    try:
        agent = create_agent(args.query, webhook_url, args.type)
        agent_id = agent.get("agentId", "?")
        print(f"[CodeBuddy] Agent 已创建: {agent_id}", file=sys.stderr)
    except Exception as e:
        print(json.dumps({"error": f"创建Agent失败: {str(e)}", "status": "failed"}))
        server.shutdown()
        sys.exit(1)
    
    # 3. 等待 webhook 回调
    print(f"[CodeBuddy] 等待结果 (超时 {args.timeout}s)...", file=sys.stderr)
    
    if not WebhookHandler.received.wait(timeout=args.timeout):
        # 超时 - 尝试轮询 agent 状态
        print(f"[CodeBuddy] webhook 超时, 尝试轮询...", file=sys.stderr)
        for _ in range(6):
            time.sleep(10)
            try:
                req = urllib.request.Request(
                    f"{BASE}/v2/backgroundagent/agentmgmt/agents",
                    headers={"Authorization": f"Bearer {API_KEY}"}
                )
                resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
                for a in resp.get("data", {}).get("agentList", []):
                    if a.get("agentId") == agent_id and a.get("result"):
                        WebhookHandler.result = {"result": a["result"]}
                        WebhookHandler.received.set()
                        break
                if WebhookHandler.received.is_set():
                    break
            except:
                pass
        
        if not WebhookHandler.received.is_set():
            # 最终失败
            req = urllib.request.Request(
                f"{BASE}/v2/backgroundagent/agentmgmt/agents",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            try:
                agents = json.loads(urllib.request.urlopen(req, timeout=10).read())
                for a in agents.get("data", {}).get("agentList", []):
                    if a.get("agentId") == agent_id:
                        WebhookHandler.result = {
                            "error": "webhook 超时",
                            "agent_status": a.get("status"),
                            "last_activity": a.get("lastActivityAt")
                        }
                        WebhookHandler.received.set()
                        break
            except:
                pass
    
    # 4. 返回结果
    server.shutdown()
    
    result = WebhookHandler.result or {"error": "无结果", "status": "timeout"}
    output = {
        "query": args.query,
        "type": args.type,
        "agent_result": result,
        "status": "success" if "error" not in result else "partial"
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
