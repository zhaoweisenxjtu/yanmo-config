#!/usr/bin/env node
/**
 * CodeBuddy Web Search Agent — SDK AcpClient 直连
 * 
 * 绕过 Session REST API，直接用 ACP 的 session/new 创建会话
 */
import { CloudAgentClient, ManifestBuilder } from '@tencent-ai/cloud-agent-sdk';
const API_KEY = 'ck_fn3pyichksu8.pl8i-Kss-DRFCc496IJFG34Y7V5ea2o9DIQsLVKAg6U';

async function search(query, timeoutMs = 180000) {
  const client = new CloudAgentClient({ apiKey: API_KEY, logLevel: 'warn', timeoutMs });
  let runtime;

  // 1. Create Runtime
  const manifest = new ManifestBuilder()
    .id(`cb-${Date.now().toString(36)}`).name('S').version('1.0.0')
    .systemPrompt('你是搜索助手，用 web_search 搜索信息，用中文回答并注明来源。')
    .skills('web_search').build();

  runtime = await client.runtimes.create({
    runtimeName: `搜:${query.slice(0,12)}`,
    agentManifest: manifest,
    sandboxType: 'CS',
  });

  const rid = runtime.id;
  for (let i = 0; i < 12; i++) {
    await new Promise(r => setTimeout(r, 5000));
    runtime = await client.runtimes.get(rid);
    if (runtime._acpUrl) break;
  }
  if (!runtime._acpUrl) throw new Error('沙箱启动超时');

  // 2. 创建 Session（通过 REST），然后获取 _acpClient
  const session = await runtime.sessions.create({ sessionName: 's' });
  
  // 先 connect（无论是否成功，_acpClient 会创建）
  try { await Promise.race([session.connect(), new Promise((_,r)=>setTimeout(()=>r('ok'), 10000))]); } catch(e) {}

  if (!session._acpClient) throw new Error('ACP连接失败');

  // 3. 用 ACP 创建新 Session（绕过 loadSession）
  const newSid = await session._acpClient.sessionNew();
  if (!newSid) throw new Error('session/new 失败');
  Object.defineProperty(session, 'id', { value: newSid, writable: true });

  // 4. Prompt + 流式读取
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => { session?.disconnect(); reject(new Error('搜索超时')); }, timeoutMs);
    let result = '';

    session.prompt({
      text: query,
      onChunk: (chunk) => { process.stdout.write(chunk?.text || ''); result += chunk?.text || ''; },
    }).then(resp => {
      clearTimeout(timeout);
      session?.disconnect();
      resolve({ result, stopReason: resp.stopReason });
    }).catch(err => {
      clearTimeout(timeout);
      session?.disconnect();
      reject(err);
    });
  });
}

const q = process.argv.slice(2).join(' ') || '搜索2025年全球人工智能市场规模数据';
search(q).then(r => console.log('\n' + JSON.stringify({ query: q, result: r.result, source: 'codebuddy' })))
  .catch(e => { console.error('\nError:', e.message); console.log(JSON.stringify({ error: e.message })); process.exit(1); });
