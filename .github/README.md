# CI/CD 流水线

## deploy-oss.yml — 国内站部署

将 Hugo 构建产物同步到阿里云 OSS，服务国内域名 `blog.es007.cn`。

### 触发条件

- `main` 分支推送

### 流程

1. Checkout 代码
2. Hugo 0.157.0 extended 构建（`baseURL` 覆盖为 `https://blog.es007.cn/`）
3. ossutil 同步 `public/` → `oss://es007-blog/`（增量同步 + 删除多余文件）

### 所需 Secrets

| Secret | 说明 |
|--------|------|
| `ALIYUN_ACCESS_KEY_ID` | 阿里云 AccessKey ID |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret |

### 部署架构

```
推送 main
  ├── Cloudflare Pages（自动构建）→ blog.es007.com（国际站）
  └── GitHub Actions → Hugo 构建 → ossutil sync → 阿里云 OSS → blog.es007.cn（国内站）
```

### 注意事项

- Cloudflare Pages 仍由 Cloudflare 自身监听 GitHub 自动构建，不经过此 Actions
- 两站 `baseURL` 不同，各自独立生成 sitemap、canonical、RSS
- OSS 需开启静态网站托管（索引页 `index.html`，错误页 `404.html`）
