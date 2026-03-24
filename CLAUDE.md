# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**亿思 (E.S)** — Hugo 博客站点，部署在 Cloudflare Pages。目标：国际访问稳定、优化中国大陆访问体验、全流程自动化发布。

- 品牌：亿思 (E.S)，域名 es007
- 站点地址：`https://blog.es007.com/`
- 语言：中文 (`zh-cn`)
- 当前状态：初始骨架阶段，尚无主题，使用自定义 `layouts/index.html` 作为首页

## 常用命令

```bash
# 本地开发预览（含草稿）
hugo server -D

# 生产构建
hugo --gc --minify

# 微信公众号发布 dry-run 测试（不调用 API，生成预览 HTML）
pip install -r scripts/wechat/requirements.txt
python scripts/wechat/publish.py --all --dry-run --project-root .
```

> 部署：推送到 GitHub 即可，Cloudflare Pages 自动构建。手动部署备用：`wrangler pages deployment create ./public --project-name blog-hugo-cf-pages`
> 检查 Cloudflare 部署状态：`npx wrangler pages deployment list --project-name blog-hugo-cf-pages`

**提交前必须**（按顺序执行）：
1. `find static/images -name "*.svg" | while read svg; do png="${svg%.svg}.png"; if [ ! -f "$png" ] || [ "$svg" -nt "$png" ]; then rsvg-convert -w 900 "$svg" -o "$png"; fi; done` — SVG→PNG 预渲染（防止微信 emoji 乱码）
2. `hugo --gc --minify` — 确认构建无误
3. `git add` 时包含生成的 `.png` 文件

## 文章 Front Matter 格式

```yaml
---
title: "文章标题"
date: 2026-03-17T10:00:00+08:00
draft: false
description: "150字以内的文章摘要，用于 SEO meta description 和社交分享"
tags: ["标签1", "标签2"]
---
```

- `draft: true` 仅在 `hugo server -D` 时可见，不会被生产构建
- `date` 必须早于当前时间，Hugo 默认不构建未来日期的文章（无需设 `buildFuture`，直接用过去的时间）
- 文档类内容如需发布为博客文章，必须放 `content/posts/` 并添加 front matter

## 目录结构与约束

- `scripts/wechat/` — 微信公众号自动发布脚本（Python），含 Markdown→微信HTML 转换、SVG→PNG、API 调用
- `content/` — 博客文章与页面，slug 建议 `kebab-case`
- `content/posts/` — 博客文章目录，文章发布后 URL 为 `/posts/<文件名去.md>/`
- `layouts/` — Hugo 模板，基于 baseof.html + block 继承体系
- `themes/` — 主题目录（按需添加，禁止跨目录复制主题实现）
- `static/` — 静态资源
- `static/images/<文章slug>/` — 文章配图目录，每篇文章的图片独立子目录
- `docs/` — 架构、运维、流程类技术文档（所有文档必须放此目录，不会被 Hugo 构建）
- `public/` — 构建产物（`.gitignore` 已忽略，禁止手工修改）

**根目录保持精简**：仅保留 `README.md`、`CLAUDE.md`、`AGENTS.md`、`hugo.toml` 等全局入口文件，技术文档一律放 `docs/`。

## 模板架构

- `layouts/_default/baseof.html` — 基础模板骨架，所有页面继承此模板
- `layouts/partials/head.html` — `<head>` 公共内容（CSS 变量、亮暗模式初始化脚本、SEO 标签）
- `head.html` 已内置 SEO：meta description、canonical、Open Graph、Twitter Card、Article JSON-LD 结构化数据
- JSON-LD 输出使用 `printf + safeHTML` 绕过 Hugo minifier 转义（直接用 `jsonify` 会被 minifier 二次转义为字符串）
- `layouts/partials/header.html` — 顶部导航栏（含主题切换按钮）
- `layouts/partials/footer.html` — 底部（含 `toggleTheme()` 脚本）
- 页面模板通过 `{{ define "main" }}` 和 `{{ define "head" }}` 块扩展 baseof
- **新增页面必须使用 block 继承 baseof，禁止独立定义完整 HTML 结构**
- 亮暗模式：CSS 变量 + `data-theme="light"` 属性 + `localStorage` 持久化

## 分支与部署

- `main` → 生产环境（推送后 Cloudflare Pages 自动构建部署）
- `main` → 推送后 GitHub Actions 自动构建并 rsync 部署到阿里云 ECS（`.github/workflows/deploy-china.yml`），服务国内站 `https://blog.es007.cn`
- `main` → 推送 `content/posts/` 变更时自动触发微信公众号草稿创建（`.github/workflows/wechat-publish.yml`）
- 阿里云服务器（182.92.95.178）承担两个角色：国内站 Nginx 静态托管 + 微信 API 反向代理中转
- 微信发布需要 GitHub Secrets：`WECHAT_APP_ID`、`WECHAT_APP_SECRET`、`WECHAT_PROXY_KEY`
- 发布状态记录在 `scripts/wechat/wechat_published.json`
- `develop` → 日常开发分支（Preview 预览环境）
- 工作流：在 `develop` 开发提交 → 完成后合并到 `main` → 推送部署
- Hugo 版本通过 Cloudflare 环境变量 `HUGO_VERSION` 固定

## 提交规范

使用轻量前缀：`feat:`、`fix:`、`docs:`、`chore:`、`refactor:`、`perf:`

**禁止在提交信息中出现任何 AI 标识**：包括 `Co-Authored-By: Claude`、`AI-generated`、`ChatGPT`、`Copilot` 等。

## 站点配置（hugo.toml）

- 已开启 sitemap.xml 和 RSS 输出（`[outputs]` 配置）
- OG image 自动提取文章正文第一张图片，也可通过 front matter `image` 字段指定

## 中国大陆访问优化要点

- 关键资源（字体、JS、CSS）本地化，不依赖第三方海外域名
- 图片使用 WebP/AVIF 压缩
- 减少请求数，关闭不必要脚本

## 国内站双端部署（已实施）

`blog.es007.com` 在微信内被拦截（未备案域名），已部署国内镜像站：

- **主站**：继续使用 Cloudflare Pages（`blog.es007.com`）
- **国内站**：`https://blog.es007.cn`，域名 `es007.cn` 需完成 ICP 备案
- **部署方式**：GitHub Actions 构建后 rsync 推送到阿里云 ECS（182.92.95.178），Nginx 提供静态文件服务
- **服务器配置**：Nginx `/etc/nginx/conf.d/blog.conf`，静态文件根目录 `/var/www/blog/`，HTTPS 由 Let's Encrypt certbot 自动续期
- **GitHub Secrets**：`DEPLOY_SSH_KEY`（服务器 SSH 私钥）

## 文章配图规范

- 配图存放：`static/images/<文章slug>/`，引用路径 `/images/<文章slug>/xxx.svg`
- 优先使用 SVG 格式（体积小、矢量清晰、加载快）
- SVG 配图采用暗色主题（`#0f172a` 背景），与博客风格一致
- 技术文章建议至少包含：架构图/流程图 + 对比表/数据可视化
- 正文插图密度：每篇文章至少 3-4 张 SVG 配图（hero + 每个核心章节至少 1 张），避免纯文字长文
- SVG 的 `font-family` 必须避免 macOS 专属字体（`system-ui`/`-apple-system`），CI 上 cairosvg 转 PNG 时会渲染为方块；publish.py 已自动替换为 `Noto Sans CJK SC`
- SVG 中禁止使用 emoji 字符（如 🦞），cairosvg 转 PNG 时会渲染为方块；改用 `<image href="/images/shared/xxx.png">` 引用 PNG 图片
- `static/images/shared/` — 跨文章共享素材（如 OpenClaw 官方像素龙虾 `pixel-lobster.png`）

## 微信公众号发布注意事项（scripts/wechat/）

- 增量模式（push 触发）：自动删除旧草稿并重建，确保内容更新
- 全量模式（workflow_dispatch）：跳过已发布文章，仅处理新文章
- 每篇文章必须有配图（`static/images/<slug>/hero.svg`），否则封面为纯色占位块
- 个人订阅号标题限制约 10 个中文字符，超长自动截断
- `author` 字段不可用（个人订阅号报 45110），已移除
- `digest` 摘要限制约 30 字符
- JSON 序列化必须 `ensure_ascii=False`，否则中文显示为 `\uXXXX` 转义
- 微信不支持 SVG 图片，需转 PNG 后上传到微信素材库
- 微信过滤外链，脚本自动转为脚注

## 微信 API 代理排查

- 代理配置：阿里云 `/etc/nginx/conf.d/wechat-proxy.conf`，`listen 80 default_server` 必须显式声明，否则 Certbot 生成的 `blog.conf` 会按字母序抢占默认 server，IP 直连请求返回 404
- 代理测试：`curl -s 'http://127.0.0.1/wechat-api/token?grant_type=client_credential&appid=test&secret=test' -H 'X-Proxy-Key: <key>'` 应返回 JSON（`invalid appid` 是正常的）
- 微信发布成功但无文章变更时会静默跳过，只有实际检测到 `content/posts/` 变更才会调用 API——因此代理故障可能被掩盖
