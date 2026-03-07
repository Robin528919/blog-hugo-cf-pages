# Hugo Blog on Cloudflare Pages

本仓库用于部署 Hugo 博客，目标是：

- 国际访问稳定
- 在不引入复杂运维的前提下尽量优化中国大陆访问体验
- 全流程自动化发布

## Pages 架构

详细设计见：

- [docs/PAGES-架构设计.md](docs/PAGES-架构设计.md)
- [Hugo-博客部署方案.md](Hugo-博客部署方案.md)

## 目录说明

- `content/`：Hugo 文章内容（初始化后创建）
- `themes/`：Hugo 主题（按需）
- `docs/`：部署和架构文档

## 发布流程

1. 本地提交到 GitHub
2. `main` 分支触发 Cloudflare Pages 生产部署
3. Pull Request 自动生成 Preview 预览环境

