# Hugo 博客部署方案（兼顾国际访问 / 尽量优化中国大陆访问）

## 1. 方案概览

- 技术栈：`Hugo` + `GitHub` + `Cloudflare Pages` + `Cloudflare CDN`
- 目标：
  - 海外访问稳定、延迟低
  - 中国大陆访问尽可能优化（在不使用中国大陆节点托管的前提下）
  - 自动化发布，降低运维成本

架构链路：

1. 本地使用 Hugo 编写与构建站点。
2. 代码推送到 GitHub 仓库。
3. Cloudflare Pages 监听仓库分支并自动构建部署。
4. Cloudflare CDN 负责全球缓存与加速分发。

---

## 2. 前置准备

- GitHub 账号与仓库（建议公开仓库，私有仓库也可）
- Cloudflare 账号
- 一个自有域名（建议放在 Cloudflare 托管 DNS）
- 本地环境：
  - `hugo`（建议 Extended 版本）
  - `git`

---

## 3. Hugo 项目初始化

```bash
hugo new site my-blog
cd my-blog
git init
```

添加主题（示例）：

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

在 `hugo.toml` 中配置主题与基础信息（示例）：

```toml
baseURL = "https://blog.example.com/"
languageCode = "zh-cn"
title = "My Hugo Blog"
theme = "PaperMod"
```

本地预览：

```bash
hugo server -D
```

---

## 4. GitHub 仓库与分支策略

推荐：

- `main`：生产分支（Cloudflare Pages 生产环境）
- `develop`：开发分支（Cloudflare Pages 预览环境）

首次提交：

```bash
git add .
git commit -m "init hugo blog"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

---

## 5. Cloudflare Pages 部署

在 Cloudflare Dashboard 中：

1. `Workers & Pages` -> `Create` -> `Pages` -> `Connect to Git`
2. 选择 GitHub 仓库
3. 构建设置：
   - Framework preset：`Hugo`
   - Build command：`hugo --gc --minify`
   - Build output directory：`public`
   - Environment variable（可选）：
     - `HUGO_VERSION=0.152.2`（按你的版本调整）
4. 选择生产分支：`main`
5. 完成部署

---

## 6. 自定义域名与 HTTPS

1. 在 Cloudflare Pages 项目中添加自定义域名：`blog.example.com`
2. 将域名 DNS 托管到 Cloudflare（推荐）
3. DNS 配置：
   - 使用 Cloudflare 自动生成记录，保持橙云（代理）开启
4. SSL/TLS：
   - 模式建议 `Full (strict)`
   - 开启 `Always Use HTTPS`
   - 开启 `Automatic HTTPS Rewrites`

---

## 7. Cloudflare CDN 缓存策略（重点）

目标：提升重复访问速度，降低回源开销。

建议规则（Cache Rules）：

- 对静态资源路径（如 `/js/*`, `/css/*`, `/images/*`, `/fonts/*`）：
  - `Cache Everything`
  - Edge TTL：`1 month` 或更长
  - Browser TTL：`1 week`~`1 month`
- 对 HTML 页面：
  - Edge TTL：`5 min`~`30 min`（按更新频率）
  - 开启 `ETag` / `Last-Modified`（由平台自动处理为主）

发布策略：

- Hugo 默认带指纹（fingerprint）时，静态资源可长期缓存。
- 每次发布后仅需关注 HTML 缓存刷新，资源文件通常无需强制清除。

---

## 8. 中国大陆访问优化建议（务实版）

说明：Cloudflare 全球网络对海外表现很好，但中国大陆访问质量受跨境链路影响，无法保证始终稳定低延迟。

可执行优化：

1. 站点瘦身
   - 压缩图片（WebP/AVIF）
   - 减少第三方脚本与外链字体
   - 开启 Hugo 最小化：`hugo --gc --minify`
2. 关键静态资源前置
   - CSS/字体等关键资源使用本地托管，不依赖境外第三方 CDN
3. Cloudflare 功能
   - 开启 Brotli 压缩
   - 开启 HTTP/3（兼容则启用）
   - 合理配置缓存规则
4. 双域名策略（可选）
   - 主域名：`blog.example.com`（Cloudflare Pages）
   - 大陆优化域名（可选，独立部署到中国大陆合规服务）
   - 通过导航提示用户选择更快入口
5. 合规与备案
   - 若要在中国大陆云厂商使用公网 Web 服务，通常需要备案（按当地法规执行）

---

## 9. CI/CD 最小实践建议

- 推送到 `main` 自动发布生产环境
- Pull Request 自动生成预览链接（Cloudflare Pages Preview）
- 发布前检查清单：
  - 链接检查（内部链接、404）
  - 图片体积检查
  - Lighthouse 基础评分检查

---

## 10. 常见问题排查

1. 构建失败
   - 检查 Hugo 版本与主题要求是否一致
   - 检查 `hugo.toml` 配置语法
2. 页面样式丢失
   - 检查 `baseURL` 是否正确
   - 检查主题子模块是否拉取完整
3. 更新后用户仍看到旧页面
   - 检查 HTML 缓存 TTL
   - 必要时执行 Cloudflare 缓存清理（仅清理受影响路径）
4. 大陆访问慢
   - 优先减少资源体积与请求数
   - 避免依赖海外第三方资源

---

## 11. 推荐落地配置（简版）

- 构建命令：`hugo --gc --minify`
- 输出目录：`public`
- 分支：`main`（生产）、`develop`（预览）
- DNS：Cloudflare 托管 + 代理开启
- 缓存：
  - 静态资源长期缓存
  - HTML 短缓存
- 资源策略：所有关键静态资源本地化

此方案在“低运维成本、全球可用、尽量改善中国大陆访问体验”之间取得了较好的平衡，适合个人博客与中小内容站点。
