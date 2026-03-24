---
title: "OpenClaw 3.22 重磅更新：插件换血、安全大修、GPT-5.4 上位"
date: 2026-03-24T18:00:00+08:00
draft: false
description: "OpenClaw 3.22 版本深度解读：插件系统彻底重构、十余项安全漏洞修复、GPT-5.4 默认上位、Matrix 渠道接入，一文看懂这次架构级大版本。"
tags: ["AI", "OpenClaw", "智能体", "安全"]
---

![OpenClaw 3.22 重磅更新：插件架构换血、安全大修、模型扩军](/images/openclaw-322-major-update/hero.svg)

停更 9 天，OpenClaw 终于憋出了一个大版本——`v2026.3.22-beta.1` 预览版上线，紧接着 3.22 正式版和 3.23 修复版在同一天内连发。

这不是常规的功能堆叠，而是一次深入底层的架构级重构。

**TL;DR：** 插件系统一刀切换新 SDK，ClawHub 成官方首选分发渠道；十余项安全漏洞集中修复（SMB 凭证泄露、沙盒注入、Unicode 伪装）；GPT-5.4 默认上位，Anthropic Vertex 正式接入；Agent 超时从 10 分钟拉到 48 小时。

---

## 一、插件系统大重构：旧时代翻篇

这次 3.22 最核心的变化——OpenClaw 的插件生态，换骨了。

旧的 `openclaw/extension-api` 被彻底移除。没有兼容层，没有过渡期，一刀切。取而代之的是全新的 `openclaw/plugin-sdk/*` 模块化接口。

这意味着：**所有还在用旧 API 的第三方插件，必须迁移。**

### ClawHub 成为首选分发渠道

以前执行 `openclaw plugins install`，系统直接从 npm 拉包。现在 ClawHub 成为首选——只有 ClawHub 上找不到的包，才会回退到 npm。

```bash
# 新的安装流程：优先 ClawHub
openclaw plugins install some-plugin    # ClawHub → npm 回退

# 也可以显式指定来源
openclaw plugins install clawhub:some-plugin
openclaw plugins install npm:some-plugin
```

npm 是通用包管理器，谁都能发包，质量参差不齐。ClawHub 是 OpenClaw 官方维护的插件市场，审核更严、来源更可控。

### 生态兼容性扩展

3.22 新增了对 Claude Code、Codex、Cursor 三大主流开发工具插件包的发现与安装支持，能把外部插件包里的 Skills 自动映射到 OpenClaw 的技能体系中。

以后你在 Cursor 里用的好用插件，有可能直接搬进 OpenClaw 跑起来——从封闭框架到开放平台，这一步迈得果断。

### 原生 Skills 管理

新增 `openclaw skills` 子命令，支持搜索、安装、更新的完整生命周期管理：

```bash
openclaw skills search image-gen
openclaw skills install @openclaw/web-search
openclaw skills update --all
```

---

## 二、安全加固：补的全是要命的洞

如果说插件重构是面向未来的布局，安全修复就是对当下最紧迫的回应。

3.22 一口气打了十多项安全补丁。

### Windows SMB 凭证泄露

攻击者可以通过构造特殊的 `file://` 或 UNC 路径，在媒体加载环节触发 Windows 自动发起 SMB 认证握手——你的 OpenClaw 以为在加载图片，实际上在把 Windows 登录凭证往外送。

3.22 在核心媒体加载和沙盒附件路径中全面拦截了远程路径。

### 执行环境沙盒加固

新版封锁了 `MAVEN_OPTS`、`SBT_OPTS`、`GRADLE_OPTS` 等 JVM 注入路径，堵住了 `GLIBC_TUNABLES` 利用通道，拦截了 `.NET` 的 `DOTNET_ADDITIONAL_DEPS` 依赖劫持。

主流构建工具链的环境变量注入攻击，一次性全堵上了。

### Unicode 零宽字符审批伪装

有人发现可以用不可见的韩文填充码位（Hangul Filler）来伪装执行命令的审批提示，让操作者在审批时看不到真实命令内容。3.22 在网关和 macOS 原生审批界面中全面转义了这类字符。

### Webhook 预认证防护

旧版本允许未认证的调用者以 1MB/30s 的大缓冲窗口消耗服务器资源。新版把预认证的 body 读取限制压到 **64KB/5s**，并限制了单 IP 的并发预认证请求数。

**对公网部署的用户来说，这一版不是「建议更新」，是「必须更新」。**

---

## 三、模型生态再扩张

### GPT-5.4 默认上位

默认 OpenAI 模型正式切换到 GPT-5.4，同时预置了 `gpt-5.4-mini` 和 `gpt-5.4-nano` 的前向兼容支持。

### MiniMax 统一整合

默认模型从 M2.5 升级到 M2.7，此前分离的 API 和 OAuth 两个插件入口合并为单一的 `minimax` 插件，配置复杂度大幅降低。

### Anthropic Vertex 接入

现在可以通过 Google Vertex AI 直接调用 Claude 模型，包括 GCP 认证和自动发现。对已经在 Google Cloud 上跑业务的团队，这条路径的价值不言而喻。

### 其他模型更新

- xAI Grok 目录同步到最新版本
- Z.AI GLM 更新到 4.5/4.6 系列
- Mistral 定价元数据修复，不再显示「零成本」误导信息
- ModelStudio/Qwen 新增标准按量付费 DashScope 端点（v2026.3.23）

---

## 四、多平台体验打磨

这类更新不炸眼球，但用起来最有感。

### Android

深色模式终于来了——从引导页到聊天页到语音页全覆盖。Control UI 新增「圆角滑块」，可自定义界面圆角程度。

### Telegram

- DM 论坛话题自动重命名：首条消息进来后，用 LLM 生成有意义的话题标签
- 静默错误回复模式：机器人报错信息可选择不发通知提示音

### 飞书

- 结构化交互审批卡片和快捷操作启动卡片
- 当前会话的 ACP 和子智能体绑定
- 推理流（Reasoning Stream）渲染——思考过程以 Markdown 引用块实时显示

### 浏览器

旧的 Chrome 扩展中继路径被彻底移除，转而支持通过 `userDataDir` 直接连接 Brave、Edge 等 Chromium 内核浏览器。运行 `openclaw doctor --fix` 可自动迁移配置。

### 新增 Matrix 渠道

基于 `matrix-js-sdk` 的官方 Matrix 插件上线，开源通讯协议终于有了一等公民待遇。

---

## 五、Agent 引擎：压缩更聪明，调度更从容

### 长对话压缩机制迭代

新版在压缩过程中自动延长运行截止时间，避免大型会话压缩到一半被超时杀掉。压缩后自动修复孤立的 `tool_result` 块，空会话的压缩也不会再陷入死循环。

### Agent 超时上限：48 小时

默认 Agent 超时时间从 600 秒直接拉到 **48 小时**。跑长任务的 ACP 会话，不再被 10 分钟的默认限制卡脖子。

### /btw 旁白命令

在对话过程中，随时用 `/btw` 插入一个旁白问题，AI 会快速回答但不影响当前会话的上下文——像跟同事开会时，侧过身低声问一句题外话，问完继续开会。

### 沙盒架构升级

沙盒系统新增可插拔后端支持，首批上线 OpenShell 和 SSH 两个后端，不再绑定 Docker 单一方案。

### 备份与恢复

新增 `openclaw backup create` 和 `openclaw backup verify`，支持 `--only-config`、`--no-include-workspace` 等精细化选项。

---

## 六、升级指南

```bash
# 检查当前版本
openclaw --version

# 升级到最新版
npm update -g openclaw@latest
# 或
openclaw self-update

# 迁移浏览器配置（如使用过旧 Chrome 扩展）
openclaw doctor --fix

# 验证插件兼容性
openclaw plugins list --check-compat
```

如果你的插件还在用 `openclaw/extension-api`，参考官方迁移文档将 import 路径替换为 `openclaw/plugin-sdk/*` 对应的子模块。

---

## 七、怎么看这次更新

9 天，一次大版本。

这种更新节奏说明一件事：OpenClaw 团队已经过了「堆功能冲 Star」的阶段，开始认真做工程了。

从插件 SDK 的断代重构，到十余项安全漏洞的集中封堵，到 Agent 引擎的精细化打磨——这是一款产品在朝着「可信赖的 AI 智能体平台」这个目标做全面收拢。

这些升级可能不会出现在宣传海报上，但它们决定了谁敢把 OpenClaw 拉进生产环境。

**敢用，比好用更难。**

---

## 延伸阅读

- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw 对话与角色设置完整指南](/posts/openclaw-agent-setup-guide/)
- [白嫖英伟达大模型：OpenClaw 接入 NVIDIA NIM 免费 API 完整指南](/posts/openclaw-nvidia-free-models/)
