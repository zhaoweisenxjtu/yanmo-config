#!/usr/bin/env python3
"""
CodeBuddy Web Search Skill — Streamable HTTP + ACP protocol
"""
import os, sys, json, time, uuid, requests

API_KEY = "ck_fn3pyichksu8.pl8i-Kss-DRFCc496IJFG34Y7V5ea2o9DIQsLVKAg6U"
BASE_URL = "https://www.codebuddy.cn/v2/agentos"

def log(*args):
    print(*args, file=sys.stderr, flush=True)

def headless_main(query):
    # 1. Create Runtime
    manifest = {
        "id": f"ws-{uuid.uuid4().hex[:6]}",
        "name": "搜索", "manifestVersion": "1.0.0",
        "system_prompt": "你是搜索助手，用 web_search 搜索信息，用中文回答。",
        "skills": [{"name": "web_search"}],
        "secrets": [{"key": "CODEBUDDY_API_KEY", "value": API_KEY}]
    }
    
    h = {"Content-Type": "application/json", "X-Api-Key": API_KEY, "X-Source-App": "cloud-agent"}
    resp = requests.post(f"{BASE_URL}/runtimes", json={
        "runtimeName": f"搜:{query[:15]}", "agentManifest": manifest, "sandboxType": "CS",
    }, headers=h, timeout=30)
    rid = resp.json().get("data", {}).get("id")
    log(f"[Runtime] {rid}")
    
    # 2. Poll for ACP
    acp_url = token = None
    for i in range(15):
        time.sleep(5)
        r = requests.get(f"{BASE_URL}/runtimes/{rid}", headers=h, timeout=10)
        if r.status_code != 200: continue
        d = r.json().get("data", {})
        l = d.get("links", {}).get("acpLink", {})
        if l.get("url"):
            acp_url, token = l["url"], l["token"]
            break
        log(f"  wait ({i+1}/15)")
    if not acp_url:
        return {"error": "沙箱超时"}
    log(f"[ACP] 就绪")
    
    # 3. ACP: Streamable HTTP 协议
    # Step 1: POST /acp with initialize (POST creates the connection)
    # Ref: https://spec.modelcontextprotocol.io/specification/basic/
    # Actually ACP is similar to MCP's Streamable HTTP
    
    # Send initialize via POST
    init_body = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "0.1.0",
            "capabilities": {},
            "clientInfo": {"name": "openclaw-search", "version": "1.0.0"}
        }
    })
    
    # POST with both Accept headers
    resp = requests.post(acp_url, data=init_body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/event-stream",
    }, timeout=30)
    
    log(f"[ACP] Init: {resp.status_code}")
    if resp.status_code != 200:
        return {"error": f"ACP初始化失败: {resp.status_code} {resp.text[:200]}"}
    
    init_result = resp.json()
    log(f"[ACP] Init result: {json.dumps(init_result, ensure_ascii=False)[:200]}")
    
    if "error" in init_result:
        # Maybe need SSE connection first
        log("[ACP] 初始化失败，尝试SSE先连...")
        
        # Step 1b: GET SSE to establish connectionId
        sse = requests.get(acp_url, stream=True, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "text/event-stream",
        }, timeout=30)
        
        conn_id = None
        for line in sse.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                try:
                    d = json.loads(line[6:])
                    conn_id = d.get("connectionId", d.get("data", {}).get("connectionId"))
                except: pass
            if conn_id: break
        
        log(f"[ACP] ConnectionId: {conn_id}")
        
        # Now send POST with session/new
        sn = json.dumps({
            "jsonrpc": "2.0", "id": 2,
            "method": "session/new",
            "params": {"cwd": "/workspace", "mcpServers": []}
        })
        resp2 = requests.post(acp_url, data=sn, stream=True, timeout=120, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept": "application/json, text/event-stream",
            "Acp-Connection-Id": conn_id,
        })
        log(f"[ACP] session/new: {resp2.status_code}")
        result2 = resp2.json()
        log(f"[ACP] sess result: {json.dumps(result2, ensure_ascii=False)[:200]}")
        
        sid = result2.get("sessionId") or result2.get("result", {}).get("sessionId")
        if not sid:
            return {"error": f"Session创建失败", "detail": str(result2)[:300]}
        
        # Prompt
        prompt = json.dumps({
            "jsonrpc": "2.0", "id": 3,
            "method": "session/prompt",
            "params": {
                "session_id": sid,
                "prompt": [{"role": "user", "content": [{"type": "text", "text": query}]}],
            }
        })
        resp3 = requests.post(acp_url, data=prompt, stream=True, timeout=300, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept": "application/json, text/event-stream",
            "Acp-Connection-Id": conn_id,
        })
        
        log(f"[ACP] Prompt: {resp3.status_code}")
        result_text = ""
        for line in resp3.iter_lines(decode_unicode=True):
            if not line: continue
            if line.startswith("data: "):
                try:
                    d = json.loads(line[6:])
                    if "error" in d:
                        log(f"[ACP] Error: {d['error']}")
                        break
                    # Chunks come as notifications
                except: pass
            elif line.startswith("event: "):
                pass
        
        result_text = resp3.text if not result_text else result_text
        if not result_text:
            try:
                result_text = json.dumps(resp3.json(), ensure_ascii=False)
            except:
                result_text = resp3.text[:5000]
        
        sse.close()
        return {"query": query, "result": result_text[:10000], "source": "codebuddy"}
    
    # If init worked directly, proceed...
    sid = init_result.get("sessionId")
    if not sid:
        # Normal flow: send session/new
        pass
    
    return {"error": "需要更多调试"}

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "2025年全球人工智能市场规模"
    from concurrent.futures import ThreadPoolExecutor
    result = headless_main(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
