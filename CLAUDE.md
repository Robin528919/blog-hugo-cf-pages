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
```

> 部署：推送到 GitHub 即可，Cloudflare Pages 自动构建。手动部署备用：`wrangler pages deployment create ./public --project-name blog-hugo-cf-pages`

**提交前必须**：成功运行 `hugo --gc --minify` 确认构建无误。

## 文章 Front Matter 格式

```yaml
---
title: "文章标题"
date: 2026-03-17T10:00:00+08:00
draft: false
tags: ["标签1", "标签2"]
---
```

- `draft: true` 仅在 `hugo server -D` 时可见，不会被生产构建
- 文档类内容如需发布为博客文章，必须放 `content/posts/` 并添加 front matter

## 目录结构与约束

- `content/` — 博客文章与页面，slug 建议 `kebab-case`
- `content/posts/` — 博客文章目录，文章发布后 URL 为 `/posts/<文件名去.md>/`
- `layouts/` — Hugo 模板，基于 baseof.html + block 继承体系
- `themes/` — 主题目录（按需添加，禁止跨目录复制主题实现）
- `static/` — 静态资源
- `docs/` — 架构、运维、流程类技术文档（所有文档必须放此目录，不会被 Hugo 构建）
- `public/` — 构建产物（`.gitignore` 已忽略，禁止手工修改）

**根目录保持精简**：仅保留 `README.md`、`CLAUDE.md`、`AGENTS.md`、`hugo.toml` 等全局入口文件，技术文档一律放 `docs/`。

## 模板架构

- `layouts/_default/baseof.html` — 基础模板骨架，所有页面继承此模板
- `layouts/partials/head.html` — `<head>` 公共内容（CSS 变量、亮暗模式初始化脚本）
- `layouts/partials/header.html` — 顶部导航栏（含主题切换按钮）
- `layouts/partials/footer.html` — 底部（含 `toggleTheme()` 脚本）
- 页面模板通过 `{{ define "main" }}` 和 `{{ define "head" }}` 块扩展 baseof
- **新增页面必须使用 block 继承 baseof，禁止独立定义完整 HTML 结构**
- 亮暗模式：CSS 变量 + `data-theme="light"` 属性 + `localStorage` 持久化

## 分支与部署

- `main` → 生产环境（推送后 Cloudflare Pages 自动构建部署）
- `develop` → 日常开发分支（Preview 预览环境）
- 工作流：在 `develop` 开发提交 → 完成后合并到 `main` → 推送部署
- Hugo 版本通过 Cloudflare 环境变量 `HUGO_VERSION` 固定

## 提交规范

使用轻量前缀：`feat:`、`fix:`、`docs:`、`chore:`、`refactor:`、`perf:`

**禁止在提交信息中出现任何 AI 标识**：包括 `Co-Authored-By: Claude`、`AI-generated`、`ChatGPT`、`Copilot` 等。

## 中国大陆访问优化要点

- 关键资源（字体、JS、CSS）本地化，不依赖第三方海外域名
- 图片使用 WebP/AVIF 压缩
- 减少请求数，关闭不必要脚本
