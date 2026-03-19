---
title: "白嫖英伟达大模型：OpenClaw 接入 NVIDIA NIM 免费 API 完整指南"
date: 2026-03-19T10:00:00+08:00
draft: false
tags: ["AI", "OpenClaw", "NVIDIA", "免费模型", "智能体"]
---

![NVIDIA × OpenClaw 架构总览](/images/nvidia-openclaw/hero.svg)

英伟达（NVIDIA）通过 [build.nvidia.com](https://build.nvidia.com) 向开发者免费开放了一批顶级大模型的 API 端点，包括 DeepSeek-V3.2、Qwen 3.5、Llama、Nemotron 等。这些模型走的是 **OpenAI 兼容协议**，意味着任何支持自定义 OpenAI 端点的工具都能直接接入——OpenClaw 正好就是。

**TL;DR：** 注册 NVIDIA 开发者账号 → 拿免费 API Key → 在 `openclaw.json` 里加一段 `models.providers` 配置 → 你的 OpenClaw 智能体立刻可以用 DeepSeek-V3.2 等模型对话。全程 5 分钟，零成本。

---

## 一、NVIDIA 免费模型有哪些

NVIDIA 在 [build.nvidia.com](https://build.nvidia.com/models) 上提供两类免费资源：

### 1.1 免费云端 API（Free Endpoint）

这些模型由 NVIDIA 托管，注册即可直接调用，无需 GPU：

![NVIDIA 免费模型能力对比](/images/nvidia-openclaw/model-comparison.svg)

| 模型 | 参数规模 | 特点 | 模型 ID |
|------|---------|------|---------|
| **DeepSeek-V3.2** | 685B | 稀疏注意力、长上下文、内置 Agent 工具调用 | `deepseek-ai/deepseek-v3_2` |
| **DeepSeek-V3.1** | - | 混合推理 | `deepseek-ai/deepseek-v3_1` |
| **DeepSeek-V3.1 Terminus** | - | 终端推理优化 | `deepseek-ai/deepseek-v3_1-terminus` |
| **Qwen 3.5-122B** | 122B MoE（10B 活跃） | 编码、推理、多模态 | `qwen/qwen3.5-122b-a10b` |
| **Nemotron 3 Super** | 120B MoE | 1M 上下文窗口 | `nvidia/nemotron-3-super-120b` |

### 1.2 可下载模型（本地部署）

如果你有 GPU，还能下载蒸馏版模型在本地跑：

- DeepSeek-R1-Distill-Qwen-32B / 14B / 7B
- DeepSeek-R1-Distill-Llama-8B

### 1.3 免费额度

- 注册 NVIDIA 开发者计划即可获得 **1,000 免费推理积分**
- 积分用于 `integrate.api.nvidia.com` 上的所有模型
- 用于开发和测试，足够跑通整套流程

---

## 二、获取 NVIDIA API Key

![接入流程：5 步完成](/images/nvidia-openclaw/setup-flow.svg)

### 步骤

1. 打开 [build.nvidia.com](https://build.nvidia.com/models)
2. 点击任意模型卡片（如 DeepSeek-V3.2）
3. 点击 **Get API Key** 按钮
4. 用邮箱注册 NVIDIA 开发者账号（免费）
5. 生成 API Key，格式类似 `nvapi-xxxxxxxxxxxxxxxxxxxx`

> 也可以在 [NGC API Key 页面](https://org.ngc.nvidia.com/setup/api-keys) 直接创建，选择 "NGC Catalog" 服务即可。

### 验证 Key 是否可用

```bash
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer nvapi-你的KEY" | head -20
```

能看到模型列表就说明 Key 生效了。

---

## 三、OpenClaw 接入配置

### 3.1 设置环境变量

```bash
# 将 API Key 写入环境变量（禁止硬编码到配置文件）
export NVIDIA_API_KEY="nvapi-你的KEY"

# 持久化（写入 shell 配置）
echo 'export NVIDIA_API_KEY="nvapi-你的KEY"' >> ~/.zshrc
source ~/.zshrc
```

### 3.2 编辑 openclaw.json

在你的 OpenClaw 配置文件中添加 NVIDIA 作为自定义提供商：

```json5
{
  // 模型提供商配置
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        apiKey: "${NVIDIA_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "deepseek-ai/deepseek-v3_2",
            name: "DeepSeek V3.2 (685B)",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192
          },
          {
            id: "deepseek-ai/deepseek-v3_1",
            name: "DeepSeek V3.1",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192
          },
          {
            id: "qwen/qwen3.5-122b-a10b",
            name: "Qwen 3.5 122B MoE",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192
          }
        ]
      }
    }
  },

  // 将 NVIDIA 模型设为默认
  agents: {
    defaults: {
      model: {
        primary: "nvidia/deepseek-ai/deepseek-v3_2"
      },
      models: {
        "nvidia/deepseek-ai/deepseek-v3_2": { alias: "DeepSeek" },
        "nvidia/qwen/qwen3.5-122b-a10b": { alias: "Qwen" },
        "nvidia/deepseek-ai/deepseek-v3_1": { alias: "DeepSeekV3.1" }
      }
    }
  }
}
```

**关键配置说明：**

- `baseUrl`：NVIDIA 云端 API 的统一入口，所有模型共用
- `apiKey`：通过 `${NVIDIA_API_KEY}` 引用环境变量，避免泄露
- `api`：设为 `openai-completions`，因为 NVIDIA NIM 是 OpenAI 兼容协议
- `cost`：全部设为 0，因为是免费额度
- 模型 ID 需要带完整的命名空间前缀（如 `deepseek-ai/deepseek-v3_2`）

### 3.3 验证配置

```bash
# 检查模型是否被 OpenClaw 识别
openclaw models list

# 你应该能看到类似输出：
# nvidia/deepseek-ai/deepseek-v3_2  DeepSeek V3.2 (685B)  ✓
# nvidia/qwen/qwen3.5-122b-a10b    Qwen 3.5 122B MoE     ✓
```

---

## 四、实战：用 DeepSeek-V3.2 驱动智能体

### 4.1 单智能体配置

如果你只想让某个特定智能体使用 NVIDIA 模型，在该智能体的工作区目录下创建 `models.json`：

```json
{
  "providers": {
    "nvidia": {
      "baseUrl": "https://integrate.api.nvidia.com/v1",
      "apiKey": "${NVIDIA_API_KEY}",
      "api": "openai-completions",
      "models": [
        {
          "id": "deepseek-ai/deepseek-v3_2",
          "name": "DeepSeek V3.2",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 131072,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

然后在该智能体的 `AGENTS.md` 中指定模型：

```markdown
## 模型配置

- 主模型：nvidia/deepseek-ai/deepseek-v3_2
```

### 4.2 混合模型策略

实际使用中，推荐混合配置——日常对话用免费模型，关键决策用付费模型兜底：

```json5
{
  agents: {
    defaults: {
      model: {
        // 日常用 NVIDIA 免费模型
        primary: "nvidia/deepseek-ai/deepseek-v3_2"
      },
      models: {
        // 免费主力
        "nvidia/deepseek-ai/deepseek-v3_2": { alias: "DeepSeek" },
        "nvidia/qwen/qwen3.5-122b-a10b": { alias: "Qwen" },
        // 付费兜底（需要深度推理时手动切换）
        "anthropic/claude-sonnet-4-5": { alias: "Claude" }
      }
    }
  }
}
```

### 4.3 多智能体分层

对于跨境电商团队等多智能体场景，可以按角色分配不同模型：

![多智能体分层模型策略](/images/nvidia-openclaw/multi-agent-strategy.svg)

| 智能体角色 | 推荐模型 | 理由 |
|-----------|---------|------|
| 日常客服 | DeepSeek-V3.2 (免费) | 通用对话能力强，零成本 |
| 内容创作 | Qwen 3.5-122B (免费) | 中文写作能力优秀 |
| 数据分析 | DeepSeek-V3.1 (免费) | 推理能力强 |
| 战略决策 | Claude Sonnet (付费) | 关键决策需要最强模型 |

---

## 五、直接用 Python/curl 调用（无需 OpenClaw）

如果你只想直接调用 NVIDIA 的 API，不走 OpenClaw：

### Python（OpenAI SDK）

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="nvapi-你的KEY"
)

response = client.chat.completions.create(
    model="deepseek-ai/deepseek-v3_2",
    messages=[
        {"role": "system", "content": "你是一个专业的技术顾问。"},
        {"role": "user", "content": "用 Python 写一个异步 HTTP 请求池"}
    ],
    max_tokens=4096
)

print(response.choices[0].message.content)
```

### curl

```bash
curl -X POST "https://integrate.api.nvidia.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -d '{
    "model": "deepseek-ai/deepseek-v3_2",
    "messages": [
      {"role": "user", "content": "解释 Rust 的所有权机制"}
    ],
    "max_tokens": 2048
  }'
```

---

## 六、常见问题

### Q1：免费额度用完了怎么办？

NVIDIA 提供 1,000 免费推理积分。用完后有几个选择：

- **申请更多额度**：在 build.nvidia.com 点击 "Request More"，可额外获得 4,000 积分
- **切换到其他免费提供商**：OpenRouter（`:free` 后缀模型）、Groq、Google Gemini 都有免费层
- **本地部署**：下载蒸馏版模型通过 Ollama 运行，完全免费且无限制

### Q2：响应速度怎么样？

NVIDIA 的 Free Endpoint 由 Blackwell GPU 驱动，实测延迟在可接受范围内。但由于是共享资源，高峰期可能排队。生产环境建议升级到 NVIDIA AI Enterprise 许可。

### Q3：支持工具调用（Function Calling）吗？

DeepSeek-V3.2 明确支持 "integrated agentic tools"，可以在 OpenClaw 中配合工具调用使用。Qwen 3.5 也支持 Tool Calling。

### Q4：可以同时配置多个免费提供商吗？

可以。OpenClaw 的 `models.providers` 支持同时配置多个提供商，可以为不同智能体分配不同的免费模型源：

```json5
{
  models: {
    providers: {
      nvidia: {
        baseUrl: "https://integrate.api.nvidia.com/v1",
        apiKey: "${NVIDIA_API_KEY}",
        api: "openai-completions",
        models: [/* NVIDIA 模型 */]
      },
      groq: {
        baseUrl: "https://api.groq.com/openai/v1",
        apiKey: "${GROQ_API_KEY}",
        api: "openai-completions",
        models: [/* Groq 模型 */]
      }
    }
  }
}
```

### Q5：模型 ID 怎么查？

访问 [build.nvidia.com/models](https://build.nvidia.com/models)，点击任意模型，在 API 示例代码中可以看到完整的模型 ID。或者用 API 查询：

```bash
curl -s https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  | python3 -m json.tool
```

---

## 七、注意事项

1. **API Key 安全**：永远不要把 Key 硬编码到配置文件或提交到 Git。用环境变量或 systemd env 文件管理
2. **免费层限制**：NVIDIA Free Endpoint 仅限开发和测试用途，不可用于生产环境。生产需购买 NVIDIA AI Enterprise 许可
3. **模型更新**：NVIDIA 会定期更新模型版本和可用列表，建议关注 [NVIDIA 开发者博客](https://developer.nvidia.com/blog)
4. **速率限制**：免费层有请求频率限制，批量调用时注意控制并发
5. **数据隐私**：通过云端 API 调用意味着数据会经过 NVIDIA 服务器，敏感数据请考虑本地部署方案

---

## 延伸阅读

- [NVIDIA NIM API 文档](https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html)
- [NVIDIA API Catalog](https://build.nvidia.com/models)
- [OpenClaw 模型配置文档](https://docs.openclaw.ai/concepts/models)
- [OpenClaw 模型提供商文档](https://docs.openclaw.ai/concepts/model-providers)
- [OpenClaw 对话与角色设置完整指南](/posts/openclaw-agent-setup-guide/)
