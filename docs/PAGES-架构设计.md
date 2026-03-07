# Cloudflare Pages 架构设计（Hugo）

## 1. 架构目标

- 生产环境稳定可回滚
- 预览环境和生产隔离
- 静态资源高命中缓存
- 内容更新后快速生效

## 2. 架构拓扑

```text
开发者 -> GitHub(main/develop/PR) -> Cloudflare Pages(Build: Hugo)
      -> 生产域名(blog.example.com) / 预览域名(<hash>.pages.dev)
      -> Cloudflare CDN 缓存 -> 终端用户
```

## 3. 分支与环境映射

- `main` -> Production（正式环境）
- `develop` -> Preview（集成环境）
- `feature/*` 的 PR -> Preview（临时预览）

## 4. 构建与输出

- 框架：Hugo
- 构建命令：`hugo --gc --minify`
- 产物目录：`public`
- 版本固定：通过环境变量 `HUGO_VERSION`

## 5. 域名与证书

- 生产域名：`blog.example.com`（自定义域名）
- 预览域名：`<project>.pages.dev`（Cloudflare 自动提供）
- SSL：`Full (strict)` + `Always Use HTTPS`

## 6. 缓存策略

- 静态资源（`/js/* /css/* /images/*`）：
  - `Cache Everything`
  - Edge TTL：30 天
  - Browser TTL：7~30 天
- HTML 页面：
  - Edge TTL：5~10 分钟
  - 发布后按路径精确清缓存（非全站）

## 7. 中国大陆访问优化策略

- 关键资源本地化（字体、JS、CSS 不依赖第三方海外域名）
- 图片 WebP/AVIF 压缩，降低首屏体积
- 减少请求数，关闭不必要脚本
- 预留“双入口”能力：
  - 国际主入口：Cloudflare Pages
  - 大陆增强入口：可选接入国内合规托管（按需）

## 8. 运维与回滚

- 回滚策略：Cloudflare Pages 切换到上一个成功部署版本
- 监控建议：
  - 按地区观察 TTFB 与可用性
  - 重点跟踪中国大陆用户首屏耗时

