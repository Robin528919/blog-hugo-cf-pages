---
name: technical-blog-writing
description: "技术博客写作技能，涵盖文章结构、代码示例和开发者受众规范。包含文章类型、代码格式、讲解深度和开发者内容模式。适用于：技术博客、开发教程、技术写作、开发者内容、文档类文章。触发词：技术博客、开发博客、工程博客、技术写作、开发教程、技术文章、代码教程、编程博客、开发者内容、技术内容、technical blog、dev blog、engineering blog"
allowed-tools: Bash(infsh *)
---

# 技术博客写作

通过 [inference.sh](https://inference.sh) CLI 编写面向开发者的技术博客文章。

## 快速开始

> 需要 inference.sh CLI（`infsh`）。[安装说明](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
infsh login

# 调研主题深度
infsh app run exa/search --input '{
  "query": "building REST API Node.js best practices 2024 tutorial"
}'

# 生成头图
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;padding:60px;font-family:ui-monospace,monospace;color:white\"><div><p style=\"font-size:18px;color:#38bdf8;margin:0\">// engineering blog</p><h1 style=\"font-size:48px;margin:16px 0;font-weight:800;font-family:system-ui;line-height:1.2\">How We Reduced API Latency by 90% with Edge Caching</h1><p style=\"font-size:20px;opacity:0.6;font-family:system-ui\">A deep dive into our CDN architecture</p></div></div>"
}'
```


## 文章类型

### 1. 教程 / 操作指南

逐步教学。读者应能跟着做并构建出成果。

```
结构：
1. 我们要构建什么（附截图/演示）
2. 前置条件
3. 第一步：环境搭建
4. 第二步：核心实现
5. 第三步：...
6. 完整代码（GitHub 链接）
7. 后续拓展 / 进阶方向
```

| 规则 | 原因 |
|------|------|
| 先展示最终效果 | 读者能判断是否值得继续阅读 |
| 明确列出前置条件 | 避免浪费非目标读者的时间 |
| 每个代码块都应可运行 | 复制-粘贴-运行是检验标准 |
| 解释"为什么"而非仅"怎么做" | 讲清原理的教程更容易被分享 |
| 包含错误处理 | 真实代码都有错误处理 |
| 链接到完整代码仓库 | 教程结束后的参考 |

### 2. 深入解析 / 概念讲解

深入解释一个概念、技术或架构决策。

```
结构：
1. [概念]是什么，为什么你应该关注？
2. 工作原理（简化心智模型）
3. 工作原理（详细机制）
4. 实际案例
5. 权衡取舍及何时不该使用
6. 延伸阅读
```

### 3. 事后复盘 / 故障报告

描述出了什么问题、原因以及如何修复。

```
结构：
1. 摘要（发生了什么、影响范围、持续时间）
2. 事件时间线
3. 根因分析
4. 实施的修复方案
5. 预防措施
6. 经验教训
```

### 4. 基准测试 / 对比评测

基于数据的工具、方案或架构对比。

```
结构：
1. 对比了什么以及为什么
2. 测试方法（确保结果可复现）
3. 结果及图表/表格
4. 分析（数据意味着什么）
5. 推荐方案（附注意事项）
6. 原始数据 / 复现步骤
```

### 5. 架构 / 系统设计

解释系统如何构建以及为何做出这些决策。

```
结构：
1. 需要解决的问题
2. 约束条件和需求
3. 考虑过的方案
4. 选定的架构（附架构图）
5. 接受的权衡取舍
6. 成果与经验
```

## 面向开发者的写作规则

### 语气与风格

| 应该 | 不应该 |
|------|--------|
| 直截了当："使用连接池" | "你可能需要考虑使用..." |
| 坦诚权衡："这会增加复杂度" | 假装你的方案完美无缺 |
| 团队决策用"我们" | "我独自一人设计了..." |
| 给出具体数字："p99 从 800ms 降到 90ms" | "显著提升了性能" |
| 引用来源和基准测试 | 做无来源的声明 |
| 承认替代方案的存在 | 假装你的方案是唯一选择 |

### 开发者讨厌的写法

```
❌ "在当今飞速发展的技术世界中..."（废话）
❌ "众所周知..."（既然都知道，你写它干嘛？）
❌ "只需简单地做 X"（如果你在看教程，说明它不简单）
❌ "很容易就能..."（轻视读者的经验）
❌ "显然..."（如果显而易见，就不用写了）
❌ 在技术内容中使用营销话术
❌ 在 3 段背景介绍之后才切入正题
```

### 代码示例

| 规则 | 原因 |
|------|------|
| 每个代码块都必须可运行 | 有 bug 的示例会摧毁信任 |
| 展示完整、可运行的示例 | 没有上下文的代码片段毫无用处 |
| 在代码围栏中标注语言 | 语法高亮 |
| 代码后展示输出/结果 | 读者可以验证理解是否正确 |
| 使用有意义的变量名 | `calculateTotalRevenue` 而非 `foo` |
| 示例中包含错误处理 | 真实代码都有错误处理 |
| 锁定依赖版本 | "适用于 React 18.2" 而非 "React" |

```
好的代码块格式：

```python
# 这段代码的功能（一行说明）
def calculate_retry_delay(attempt: int, base_delay: float = 1.0) -> float:
    """指数退避 + 随机抖动。"""
    delay = base_delay * (2 ** attempt)
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter

# 使用方式
delay = calculate_retry_delay(attempt=3)  # ~8.0-8.8 秒
```
```

### 讲解深度

| 受众信号 | 深度 |
|----------|------|
| "X 入门" | 解释一切，假设没有前置知识 |
| "X 高级模式" | 跳过基础，深入细节和技巧 |
| "X 对比 Y" | 假设读者熟悉两者，聚焦差异 |
| "我们如何构建 X" | 技术读者，可跳过基本概念 |

**在文章开头明确说明假定的读者水平**：

```
"本文假设你熟悉 Docker 和基本的 Kubernetes 概念。
如果你刚接触容器技术，请先阅读[我们的入门文章]。"
```

## 博客文章结构

### 理想结构

```markdown
# 标题（包含核心关键词，说明成果）

[头图或架构图]

**TL;DR：**[2-3 句摘要，包含核心要点]

## 问题 / 为什么重要
[阐述读者为什么应该关心——要具体，不要泛泛而谈]

## 解决方案 / 我们是怎么做的
[核心内容——代码、架构、讲解]

### 第一步：[做什么]
[讲解 + 代码 + 输出]

### 第二步：[做什么]
[讲解 + 代码 + 输出]

## 成果
[数据、基准测试、结果——要具体]

## 权衡与局限
[坦诚不足之处——建立信任]

## 结论
[核心要点 + 下一步行动]

## 延伸阅读
[3-5 个相关链接]
```

### 各类型推荐字数

| 类型 | 字数 | 原因 |
|------|------|------|
| 快速技巧 | 500-800 | 一个概念，一个示例 |
| 教程 | 1,500-3,000 | 逐步讲解需要充分细节 |
| 深入解析 | 2,000-4,000 | 需要全面深入的探讨 |
| 架构文章 | 2,000-3,500 | 图表分担了部分表达 |
| 基准测试 | 1,500-2,500 | 数据和图表承担主要表达 |

## 图表与可视化

### 何时使用图表

| 场景 | 图表类型 |
|------|----------|
| 请求流程 | 时序图 |
| 系统架构 | 方框箭头图 |
| 决策逻辑 | 流程图 |
| 数据模型 | ER 图 |
| 性能对比 | 柱状图/折线图 |
| 前后对比 | 并排展示 |

```bash
# 生成架构图
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:600px;background:#0f172a;display:flex;align-items:center;justify-content:center;padding:40px;font-family:system-ui;color:white\"><div style=\"display:flex;gap:40px;align-items:center\"><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Client</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">React App</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #3b82f6;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Edge</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">CDN Cache</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">API</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">Node.js</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Database</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">PostgreSQL</p></div></div></div>"
}'

# 生成基准测试图表
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(12, 6))\nfig.patch.set_facecolor(\"#0f172a\")\nax.set_facecolor(\"#0f172a\")\n\ntools = [\"Express\", \"Fastify\", \"Hono\", \"Elysia\"]\nrps = [15000, 45000, 62000, 78000]\ncolors = [\"#64748b\", \"#64748b\", \"#3b82f6\", \"#64748b\"]\n\nax.barh(tools, rps, color=colors, height=0.5)\nfor i, v in enumerate(rps):\n    ax.text(v + 1000, i, f\"{v:,} req/s\", va=\"center\", color=\"white\", fontsize=14)\n\nax.set_xlabel(\"Requests per second\", color=\"white\", fontsize=14)\nax.set_title(\"HTTP Framework Benchmark (Hello World)\", color=\"white\", fontsize=18, fontweight=\"bold\")\nax.tick_params(colors=\"white\", labelsize=12)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.spines[\"bottom\"].set_color(\"#334155\")\nax.spines[\"left\"].set_color(\"#334155\")\nplt.tight_layout()\nplt.savefig(\"benchmark.png\", dpi=150, facecolor=\"#0f172a\")\nprint(\"Saved\")"
}'
```

## 内容分发

### 开发者常用阅读平台

| 平台 | 格式 | 发布方式 |
|------|------|----------|
| 个人博客 | 完整文章 | 首发——掌握内容所有权 |
| Dev.to | 转载（canonical URL 指回你的博客） | Markdown 导入 |
| Hashnode | 转载（canonical URL） | Markdown 导入 |
| Hacker News | 链接提交 | 项目用 Show HN，故事用 Tell HN |
| Reddit（r/programming、r/webdev 等） | 链接或讨论帖 | 遵守各版块规则 |
| Twitter/X | 帖子摘要 + 链接 | 参见 twitter-thread-creation 技能 |
| LinkedIn | 改编版本 + 链接 | 参见 linkedin-content 技能 |

```bash
# 同步发帖到 X
infsh app run x/post-create --input '{
  "text": "New blog post: How We Reduced API Latency by 90%\n\nThe short version:\n→ Moved computation to edge\n→ Aggressive cache-control headers\n→ Eliminated N+1 queries\n\np99 went from 800ms to 90ms.\n\nFull deep dive with code: [link]"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|------|------|----------|
| 没有 TL;DR | 忙碌的开发者在获取要点之前就离开了 | 在顶部放 2-3 句摘要 |
| 代码示例有 bug | 彻底摧毁可信度 | 发布前测试每个代码块 |
| 没有锁定版本 | 代码 6 个月后就跑不通了 | "适用于 Node 20、React 18.2" |
| "只需简单地做 X" | 居高临下，令人不快 | 删除"简单"、"只需"、"轻松" |
| 架构文章没有图表 | 大段文字描述系统结构 | 一张图 > 500 字的描述 |
| 营销腔调 | 开发者立刻失去兴趣 | 直接、技术化、诚实 |
| 没有权衡取舍部分 | 读起来像有偏见的营销文 | 始终讨论不足之处 |
| 正文前有大量铺垫 | 读者直接跳出 | 2-3 段内切入正题 |
| 依赖版本未锁定 | 教程对后来的读者失效 | 锁定版本，注明写作日期 |
| 没有"延伸阅读" | 到此结束，没有后续 | 3-5 个链接加深理解 |

## 相关技能

```bash
npx skills add inference-sh/skills@seo-content-brief
npx skills add inference-sh/skills@content-repurposing
npx skills add inference-sh/skills@og-image-design
```

浏览所有应用：`infsh app list`

