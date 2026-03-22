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

---

## wechat-publish.yml — 微信公众号自动发布

将 Hugo 博客文章自动转换为微信兼容格式并创建公众号草稿。

### 触发条件

- `main` 分支推送且 `content/posts/**` 有变更
- 手动触发（`workflow_dispatch`，可选"发布全部未发布文章"）

### 流程

1. Checkout 代码（`fetch-depth: 2` 用于 git diff）
2. 安装系统依赖（`libcairo2-dev`，SVG→PNG 转换所需）
3. 安装 Python 3.12 + `scripts/wechat/requirements.txt` 依赖
4. 运行 `publish.py`：检测变更文章 → Markdown 转微信 HTML → 上传图片素材 → 创建草稿
5. 自动提交 `wechat_published.json` 发布状态

### 所需 Secrets

| Secret | 说明 |
|--------|------|
| `WECHAT_APP_ID` | 微信公众号 AppID |
| `WECHAT_APP_SECRET` | 微信公众号 AppSecret |

### 核心脚本

- `scripts/wechat/publish.py` — 主脚本（Markdown 转换 + 微信 API 调用）
- `scripts/wechat/wechat_style.py` — inline CSS 样式映射
- `scripts/wechat/wechat_published.json` — 发布状态追踪（自动生成）

### 注意事项

- 个人订阅号仅能创建草稿，需手动确认发布
- 微信不支持 SVG，脚本自动转 PNG 后上传
- 微信过滤外链，脚本自动将链接转为脚注
- 需在微信后台配置 IP 白名单（GitHub Actions runner IP 段）
- `wechat_published.json` 不在 `content/posts/` 路径下，不会循环触发工作流
