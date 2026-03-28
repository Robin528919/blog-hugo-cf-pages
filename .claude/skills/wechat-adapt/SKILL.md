---
name: wechat-adapt
description: "将博客文章适配为微信公众号版本。读取 content/posts/<slug>.md，生成脱敏、风格适配的 .wechat.md 文件。触发词：微信适配、wechat-adapt、生成微信版、微信脱敏、平台适配"
---

# 微信文章适配

将博客原文适配为微信公众号安全版本，生成 `content/posts/<slug>.wechat.md`。

## 工作流程

### Step 1：确定目标文章

- 如果用户指定了文章 slug，直接处理
- 如果未指定，扫描 `content/posts/*.md`（排除 `.wechat.md`），列出没有对应 `.wechat.md` 的文章，让用户选择
- 支持批量：`/wechat-adapt --all` 处理所有缺少微信版的文章

### Step 2：读取原文并分析

读取 `content/posts/<slug>.md`，识别以下需要适配的内容：

1. **敏感词**：参照 `references/wechat-rules.md` 中的规则
2. **外链**：微信会过滤外链，需转为文字描述或脚注
3. **代码块**：微信排版对长代码不友好，超过 15 行考虑精简
4. **博客内链**：`/posts/xxx/` 格式的链接转为"详见公众号历史文章《xxx》"
5. **语气风格**：微信读者偏好口语化、短段落

### Step 3：生成微信版

生成 `content/posts/<slug>.wechat.md`，遵循以下规则：

#### 3a. Front Matter

保持与原文一致，新增标记字段：

```yaml
---
title: "（与原文相同）"
date: （与原文相同）
draft: false
description: "（与原文相同或微调）"
tags: [（与原文相同）]
wechat_adapted: true
wechat_source: "<slug>.md"
---
```

#### 3b. 内容适配规则（按优先级）

**P0 — 必须处理（会导致发布失败）：**
- 替换所有微信敏感词（见 references/wechat-rules.md）
- 移除或改写涉及竞品/海外平台的直接提及
- 不要机械替换，要理解上下文后整句重写，保持语义自然

**P1 — 应该处理（影响阅读体验）：**
- 博客内链 → "详见公众号历史文章《标题》"或直接移除
- 外部链接 → 保留文字描述，删除 URL
- 超长代码块（>15 行） → 精简为关键片段 + 注释说明

**P2 — 可选优化（提升微信阅读体验）：**
- 长段落拆分（微信屏幕窄，单段落建议不超过 4 行）
- 适当增加口语化表达
- 在关键转折处增加空行，提升移动端可读性

#### 3c. 不能改的

- **文章核心观点和技术内容不能变**
- **配图引用路径不能变**（publish.py 会处理图片上传）
- **Front matter 的 date、tags 不能变**

### Step 4：输出差异摘要

生成完成后，输出一份适配摘要：

```
微信适配摘要：<slug>
━━━━━━━━━━━━━━━━━━━━
- 敏感词替换：X 处
- 外链处理：X 处
- 代码精简：X 处
- 段落调整：X 处
- 文件：content/posts/<slug>.wechat.md
```

### Step 5：验证

运行 dry-run 验证生成的微信版能否正常处理：

```bash
python3 scripts/wechat/publish.py --dry-run --project-root . --all
```

## 批量模式

`/wechat-adapt --all`：
1. 扫描所有 `content/posts/*.md`
2. 跳过已有 `.wechat.md` 的文章（除非加 `--force`）
3. 逐篇生成，输出汇总报告

## 注意事项

- `.wechat.md` 文件需要加入 git 跟踪
- Hugo 已在 `hugo.toml` 中配置 `ignoreFiles` 排除 `.wechat.md`，不会构建到博客
- `publish.py` 优先读取 `.wechat.md`，不存在则回退到 `.md` 原文
- 博客原文 `.md` 始终保持完整，不因微信审核而降级
