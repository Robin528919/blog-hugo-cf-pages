---
name: 国内站双端部署（已实施）
description: 国内站 blog.es007.cn 已通过 rsync + ECS Nginx 部署，域名待 ICP 备案
type: project
---

国内镜像站已上线，架构为 GitHub Actions → Hugo 构建 → rsync → 阿里云 ECS Nginx。

具体配置：
- 国内站域名：`https://blog.es007.cn`（域名 `es007.cn` 待 ICP 备案）
- 服务器：182.92.95.178，Nginx 静态文件服务
- Nginx 配置：`/etc/nginx/conf.d/blog.conf`，根目录 `/var/www/blog/`
- HTTPS：Let's Encrypt certbot 自动续期（证书到期 2026-06-22）
- Workflow：`.github/workflows/deploy-china.yml`
- GitHub Secret：`DEPLOY_SSH_KEY`

**Why:** 微信对未备案域名拦截严格，blog.es007.com 在微信内被封禁。最初计划用 OSS，但 OSS 默认 Bucket 域名不支持网页浏览（只下载），且绑定自定义域名需先完成备案，因此改为直接部署到 ECS。

**How to apply:** 部署、CI/CD 相关工作参考此架构。服务器同时承担微信 API 反向代理角色。
