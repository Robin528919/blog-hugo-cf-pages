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

## 目录结构与约束

- `content/` — 博客文章与页面，slug 建议 `kebab-case`
- `layouts/` — Hugo 模板（当前仅首页模板）
- `themes/` — 主题目录（按需添加，禁止跨目录复制主题实现）
- `static/` — 静态资源
- `docs/` — 架构、运维、流程类技术文档（所有文档必须放此目录）
- `public/` — 构建产物（`.gitignore` 已忽略，禁止手工修改）

**根目录保持精简**：仅保留 `README.md`、`CLAUDE.md`、`AGENTS.md`、`hugo.toml` 等全局入口文件，技术文档一律放 `docs/`。

## 分支与部署

- 推送到 GitHub 后 Cloudflare Pages 自动构建部署，无需手动操作
- `main` → 生产环境
- PR / `develop` → Preview 预览环境
- Hugo 版本通过 Cloudflare 环境变量 `HUGO_VERSION` 固定

## 提交规范

使用轻量前缀：`feat:`、`fix:`、`docs:`、`chore:`、`refactor:`、`perf:`

## 中国大陆访问优化要点

- 关键资源（字体、JS、CSS）本地化，不依赖第三方海外域名
- 图片使用 WebP/AVIF 压缩
- 减少请求数，关闭不必要脚本
