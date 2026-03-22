# 多平台内容分发指南

> 博客文章同步发布到国内外各平台的操作手册

## 平台总览

| 序号 | 平台 | 网址 | 区域 | 类型 | Markdown | API | 优先级 |
|------|------|------|------|------|----------|-----|--------|
| 1 | 微信公众号 | https://mp.weixin.qq.com | 国内 | 封闭生态 | ❌ | 有限 | ⭐⭐⭐ |
| 2 | 知乎 | https://zhuanlan.zhihu.com | 国内 | 综合问答 | ✅ | 非官方 | ⭐⭐⭐ |
| 3 | 掘金 | https://juejin.cn | 国内 | 技术社区 | ✅ | 非官方 | ⭐⭐⭐ |
| 4 | CSDN | https://www.csdn.net | 国内 | 技术社区 | ✅ | 非官方 | ⭐⭐ |
| 5 | 博客园 | https://www.cnblogs.com | 国内 | 技术社区 | ✅ | 官方 MetaWeblog | ⭐⭐ |
| 6 | 简书 | https://www.jianshu.com | 国内 | 写作平台 | ✅ | ❌ | ⭐ |
| 7 | SegmentFault | https://segmentfault.com | 国内 | 技术问答 | ✅ | ❌ | ⭐ |
| 8 | 开源中国 (OSChina) | https://www.oschina.net | 国内 | 开源社区 | ✅ | ❌ | ⭐ |
| 9 | 头条号 | https://mp.toutiao.com | 国内 | 综合内容 | ❌ | 官方 | ⭐⭐ |
| 10 | 百家号 | https://baijiahao.baidu.com | 国内 | 综合内容 | ❌ | ❌ | ⭐ |
| 11 | 腾讯云开发者社区 | https://cloud.tencent.com/developer | 国内 | 技术社区 | ✅ | ❌ | ⭐ |
| 12 | 阿里云开发者社区 | https://developer.aliyun.com | 国内 | 技术社区 | ✅ | ❌ | ⭐ |
| 13 | 华为云开发者社区 | https://bbs.huaweicloud.com | 国内 | 技术社区 | ✅ | ❌ | ⭐ |
| 14 | 51CTO | https://blog.51cto.com | 国内 | 技术社区 | ✅ | ❌ | ⭐ |
| 15 | 小红书 | https://www.xiaohongshu.com | 国内 | 图文/短视频 | ❌ | 非官方 | ⭐⭐⭐ |
| 16 | 抖音 | https://www.douyin.com | 国内 | 短视频/图文 | ❌ | 官方 | ⭐⭐ |
| 17 | 快手 | https://www.kuaishou.com | 国内 | 短视频/图文 | ❌ | 官方 | ⭐⭐ |
| 18 | B站（哔哩哔哩） | https://www.bilibili.com | 国内 | 视频/专栏 | ✅ | 非官方 | ⭐⭐⭐ |
| 19 | 微博 | https://weibo.com | 国内 | 社交媒体 | ❌ | 官方 | ⭐⭐ |
| 20 | Dev.to | https://dev.to | 海外 | 技术社区 | ✅ | 官方 REST | ⭐⭐⭐ |
| 21 | Hashnode | https://hashnode.com | 海外 | 技术博客 | ✅ | 官方 GraphQL | ⭐⭐⭐ |
| 22 | Medium | https://medium.com | 海外 | 写作平台 | ✅ | 官方 REST | ⭐⭐⭐ |
| 23 | Substack | https://substack.com | 海外 | Newsletter | ❌ | ❌ | ⭐⭐ |
| 24 | LinkedIn Article | https://www.linkedin.com | 海外 | 职业社交 | ❌ | 官方 | ⭐⭐ |
| 25 | X (Twitter) | https://x.com | 海外 | 社交媒体 | ❌ | 官方 | ⭐⭐ |
| 26 | Reddit | https://www.reddit.com | 海外 | 社区论坛 | ✅ | 官方 | ⭐ |
| 27 | Hacker News | https://news.ycombinator.com | 海外 | 技术资讯 | ❌ | 官方 | ⭐ |
| 28 | Facebook Page | https://www.facebook.com | 海外 | 社交媒体 | ❌ | 官方 | ⭐ |
| 29 | YouTube | https://www.youtube.com | 海外 | 视频平台 | ❌ | 官方 | ⭐⭐ |

---

## 国内平台详情

### 1. 微信公众号

- **后台地址**：https://mp.weixin.qq.com
- **账号类型**：订阅号（个人可注册）/ 服务号（企业）
- **内容格式**：富文本，不支持 Markdown
- **图片要求**：必须上传到微信服务器，外链图片会被过滤
- **发布限制**：订阅号每天 1 次群发，每次最多 8 篇
- **API 能力**：
  - 认证服务号：可通过 API 创建草稿、上传素材
  - 订阅号：API 权限极有限，基本需手动操作
- **操作流程**：
  1. 用 [doocs/md](https://doocs.github.io/md/) 将 Markdown 转为微信格式
  2. 复制粘贴到公众号后台编辑器
  3. 检查图片是否正常显示（外链图片需手动上传）
  4. 预览 → 发布
- **注意事项**：
  - 文末添加博客原文链接（"阅读原文"功能）
  - 外链仅支持已备案域名或公众号文章互链
  - 代码高亮需通过排版工具预处理

### 2. 知乎

- **发布入口**：https://zhuanlan.zhihu.com/write
- **内容格式**：支持 Markdown（编辑器可切换）
- **图片要求**：支持外链，也可上传
- **发布限制**：无明显频率限制
- **SEO 价值**：高，知乎内容在百度/Google 排名好
- **操作流程**：
  1. 新建文章 → 切换到 Markdown 模式
  2. 粘贴博客 Markdown 内容
  3. 检查格式 → 添加话题标签 → 发布
- **注意事项**：
  - 文末标注"原文发布于 blog.es007.com"
  - 知乎会自动转存外链图片
  - 可同步发布到知乎专栏，获得更多曝光

### 3. 掘金

- **发布入口**：https://juejin.cn/editor/drafts/new
- **内容格式**：原生 Markdown 编辑器
- **图片要求**：支持外链，自动转存到掘金 CDN
- **发布限制**：新号需审核，通过后无明显限制
- **SEO 价值**：高，技术文章排名好
- **操作流程**：
  1. 新建文章 → 直接粘贴 Markdown
  2. 设置标题、分类（前端/后端/运维等）、标签
  3. 上传封面图 → 发布
- **注意事项**：
  - 掘金有内容质量审核，纯搬运可能被拒
  - 建议在文末添加原文链接
  - 优先发布技术深度文章

### 4. CSDN

- **发布入口**：https://editor.csdn.net/md
- **内容格式**：Markdown 编辑器
- **图片要求**：支持外链，自动转存
- **发布限制**：无明显限制
- **SEO 价值**：高（百度权重很高）
- **操作流程**：
  1. 新建博文 → 粘贴 Markdown
  2. 设置分类、标签、摘要
  3. 选择"原创" → 发布
- **注意事项**：
  - CSDN 有大量广告，但百度收录极好
  - 标记"原创"可获得更多推荐
  - 注意 CSDN 会给文章加各种推广模块

### 5. 博客园

- **发布入口**：https://i.cnblogs.com/posts/edit
- **内容格式**：Markdown / 富文本
- **图片要求**：支持外链
- **API**：支持 MetaWeblog API，可自动化发布
- **发布限制**：新用户需申请博客开通
- **操作流程**：
  1. 新建随笔 → 切换 Markdown 编辑器
  2. 粘贴内容 → 设置分类
  3. 发布
- **注意事项**：
  - 社区氛围好，技术讨论质量高
  - MetaWeblog API 可直接集成到发布脚本

### 6. 简书

- **发布入口**：https://www.jianshu.com/writer
- **内容格式**：Markdown
- **图片要求**：需上传到简书服务器
- **发布限制**：每日发文数量有限制
- **操作流程**：
  1. 新建文章 → 粘贴 Markdown
  2. 手动上传图片（不支持外链渲染）
  3. 发布到对应专题
- **注意事项**：
  - 简书近年流量下降，优先级较低
  - 图片外链不渲染，需手动处理

### 7. SegmentFault 思否

- **发布入口**：https://segmentfault.com/write
- **内容格式**：Markdown
- **图片要求**：支持外链
- **发布限制**：无明显限制
- **操作流程**：
  1. 写文章 → 粘贴 Markdown
  2. 添加标签 → 发布
- **注意事项**：
  - 技术社区，适合发布编程类内容
  - 社区活跃度一般

### 8. 开源中国 (OSChina)

- **发布入口**：https://my.oschina.net/u/xxx/blog/write
- **内容格式**：Markdown
- **图片要求**：支持外链
- **操作流程**：粘贴 Markdown → 设置分类 → 发布
- **注意事项**：适合开源项目相关内容

### 9. 头条号

- **发布入口**：https://mp.toutiao.com/profile_v4/graphic/publish
- **内容格式**：富文本编辑器，不支持 Markdown
- **图片要求**：需上传
- **发布限制**：需实名认证
- **操作流程**：
  1. 需将 Markdown 转为富文本后粘贴
  2. 或使用头条号自带编辑器重新排版
  3. 上传封面图 → 发布
- **注意事项**：
  - 头条算法推荐，适合泛技术科普内容
  - 纯代码类文章阅读量可能较低

### 10. 百家号

- **发布入口**：https://baijiahao.baidu.com/builder/rc/edit
- **内容格式**：富文本
- **发布限制**：需实名认证，每日有发文上限
- **操作流程**：富文本粘贴 → 上传图片 → 发布
- **注意事项**：
  - 百度搜索有流量倾斜
  - 内容审核较严格

### 11. 腾讯云开发者社区

- **发布入口**：https://cloud.tencent.com/developer/article/write
- **内容格式**：Markdown
- **操作流程**：粘贴 Markdown → 选择技术分类 → 发布
- **注意事项**：适合云计算、运维相关内容

### 12. 阿里云开发者社区

- **发布入口**：https://developer.aliyun.com/article/new
- **内容格式**：Markdown
- **操作流程**：粘贴 Markdown → 设置标签 → 发布
- **注意事项**：适合云原生、大数据相关内容

### 13. 华为云开发者社区

- **发布入口**：https://bbs.huaweicloud.com/blogs/new
- **内容格式**：Markdown
- **操作流程**：粘贴 Markdown → 选择板块 → 发布

### 14. 51CTO

- **发布入口**：https://blog.51cto.com/blogger/publish
- **内容格式**：Markdown / 富文本
- **操作流程**：粘贴内容 → 设置分类 → 发布
- **注意事项**：运维、网络方向内容受欢迎

### 15. 小红书

- **发布入口**：https://www.xiaohongshu.com（App 为主）/ 网页端：https://creator.xiaohongshu.com
- **内容格式**：图文笔记（图片 + 文字），不支持 Markdown
- **图片要求**：必须有图片，支持最多 18 张，建议竖版 3:4
- **发布限制**：每日有发布上限，新号约 5 篇/天
- **适合内容**：科普图文、技术可视化、教程卡片
- **操作流程**：
  1. 将博客核心内容提炼为图文卡片（建议 5-9 张）
  2. 每张图片包含一个知识点，文字精简
  3. 封面图决定点击率，需精心设计
  4. 正文补充详细说明 + 话题标签
- **注意事项**：
  - 小红书以图文为主，不适合直接搬运长文
  - 需要将博客内容**二次加工**为图文卡片形式
  - 技术科普类内容需通俗易懂，避免大段代码
  - 话题标签很重要，选 3-5 个相关话题
  - App 端发布体验优于网页端

### 16. 抖音

- **发布入口**：App 端 / 创作者平台 https://creator.douyin.com
- **内容格式**：短视频为主，支持图文（类似小红书图文模式）
- **图片要求**：图文模式支持多张图 + 背景音乐
- **API**：抖音开放平台提供视频发布 API
- **适合内容**：技术科普短视频、代码演示录屏、图文讲解
- **操作流程**：
  1. **图文模式**：将博客内容制作为图文卡片 → 上传 → 添加文案和话题
  2. **视频模式**：录制技术讲解/代码演示 → 剪辑 → 上传
- **注意事项**：
  - 图文模式适合搬运博客内容（制作成卡片）
  - 视频推荐算法强大，优质内容可获大量曝光
  - 技术内容需要通俗化，面向泛人群
  - 前 3 秒决定完播率，开头要有吸引力

### 17. 快手

- **发布入口**：App 端 / 创作者平台 https://cp.kuaishou.com
- **内容格式**：短视频、图文
- **API**：快手开放平台提供发布 API
- **适合内容**：技术科普、教程演示
- **操作流程**：
  1. 类似抖音，制作图文卡片或短视频
  2. 上传 → 添加描述和话题标签
- **注意事项**：
  - 快手用户群偏下沉市场，技术内容需更通俗
  - 图文模式与抖音类似
  - 可与抖音内容复用

### 18. B站（哔哩哔哩）

- **发布入口**：
  - 专栏文章：https://member.bilibili.com/article-text/home
  - 视频投稿：https://member.bilibili.com/platform/upload/video/frame
- **内容格式**：专栏支持 Markdown，视频支持各种格式
- **图片要求**：专栏支持外链和上传
- **发布限制**：需实名认证
- **适合内容**：技术教程专栏、代码讲解视频、技术科普
- **操作流程（专栏）**：
  1. 进入创作中心 → 投稿 → 专栏
  2. 粘贴 Markdown 内容
  3. 设置分类（科技 → 计算机技术）
  4. 上传封面 → 发布
- **操作流程（视频）**：
  1. 录制技术讲解/代码演示视频
  2. 上传 → 设置标题、简介、标签、封面
  3. 选择分区 → 发布
- **注意事项**：
  - B站专栏非常适合直接搬运博客 Markdown 文章
  - B站技术区氛围好，年轻开发者多
  - 视频 + 专栏组合效果最佳
  - 专栏 SEO 在百度有一定权重

### 19. 微博

- **发布入口**：https://weibo.com（微博头条文章）
- **内容格式**：富文本（头条文章）/ 短文（微博正文 2000 字以内）
- **图片要求**：支持上传，最多 9 张（普通微博）
- **API**：微博开放平台官方 API
- **适合内容**：技术资讯速报、文章摘要引流
- **操作流程**：
  1. **头条文章**：发布长文 → 富文本编辑器排版
  2. **普通微博**：提取核心观点 + 博客链接 + 配图
- **注意事项**：
  - 微博适合做引流而非全文发布
  - 头条文章打开率较低，普通微博 + 链接更实用
  - 需要积累粉丝才有传播效果
  - 话题标签（#xxx#）可增加曝光

---

## 海外平台详情

### 20. Dev.to

- **发布入口**：https://dev.to/new
- **内容格式**：Markdown（原生支持）
- **图片要求**：支持外链
- **API**：官方 REST API，支持自动发布
  - 文档：https://developers.forem.com/api/v1
  - 认证：API Key（设置页生成）
  - 创建文章：`POST /api/articles`
- **canonical_url**：✅ 支持设置原文链接
- **操作流程**：
  1. 粘贴 Markdown（Front Matter 兼容）
  2. 设置 tags（最多 4 个）
  3. 设置 canonical_url 指向博客原文
  4. 发布
- **注意事项**：
  - 开发者社区活跃度高
  - 支持 RSS 自动导入（Settings → Extensions → RSS）
  - Front Matter 格式：
    ```yaml
    ---
    title: 文章标题
    published: true
    tags: [tag1, tag2]
    canonical_url: https://blog.es007.com/posts/xxx/
    ---
    ```

### 21. Hashnode

- **发布入口**：https://hashnode.com/draft
- **内容格式**：Markdown
- **图片要求**：支持外链
- **API**：GraphQL API，支持自动发布
  - 文档：https://apidocs.hashnode.com
  - 认证：Personal Access Token
- **canonical_url**：✅ 支持
- **自定义域名**：✅ 可绑定自己的域名作为博客
- **操作流程**：
  1. 粘贴 Markdown
  2. 设置 canonical URL
  3. 添加标签 → 发布
- **注意事项**：
  - 支持 GitHub 备份
  - 自带 SEO 优化和 Newsletter 功能
  - 可作为博客的海外镜像站

### 22. Medium

- **发布入口**：https://medium.com/new-story
- **内容格式**：富文本（可导入 Markdown）
- **图片要求**：支持外链，自动缓存
- **API**：官方 REST API
  - 认证：Integration Token
  - 创建文章：`POST /v1/users/{userId}/posts`
  - API 功能有限，仅支持创建，不支持编辑
- **canonical_url**：✅ 支持（API 和手动都可设置）
- **操作流程**：
  1. Import Story → 粘贴博客 URL（自动抓取）
  2. 或粘贴内容手动排版
  3. 设置 canonical link
  4. 添加 tags（最多 5 个）→ 发布
- **注意事项**：
  - Medium 有付费墙，免费文章每月有限
  - 可发布到 Publication 获得更多曝光
  - Import 功能会自动设置 canonical URL

### 23. Substack

- **发布入口**：https://substack.com/publish/post
- **内容格式**：富文本编辑器
- **API**：❌ 无公开 API
- **操作流程**：
  1. 手动粘贴内容排版
  2. 可选择免费/付费投递
  3. 发布后自动发送邮件给订阅者
- **注意事项**：
  - 核心是 Newsletter，适合建立邮件订阅
  - 无 Markdown 支持，需手动排版
  - 适合深度长文和系列文章

### 24. LinkedIn Article

- **发布入口**：LinkedIn → Write Article
- **内容格式**：富文本
- **API**：官方 Marketing API（需审核）
- **操作流程**：
  1. 粘贴内容 → 简单排版
  2. 添加封面图
  3. 发布
- **注意事项**：
  - 适合职业相关、行业分析类内容
  - 文章会出现在个人主页和 Feed 中
  - 专业人脉网络，适合 B2B 内容

### 25. X (Twitter)

- **发布方式**：摘要 + 链接（非全文）
- **API**：官方 API v2
  - 免费版：每月 1500 条推文
  - 认证：OAuth 2.0
- **操作流程**：
  1. 提取文章核心观点（1-2 句话）
  2. 附上博客链接
  3. 可发布 Thread 形式的系列推文
- **注意事项**：
  - 以引流为主，不发全文
  - 配图 + 链接效果更好
  - 使用相关 hashtag 增加曝光

### 26. Reddit

- **发布方式**：链接帖 或 文字帖
- **API**：官方 API
- **适合板块**：r/programming、r/webdev、r/selfhosted 等
- **操作流程**：
  1. 选择合适的 subreddit
  2. 发布链接帖（附博客 URL）
  3. 或发文字帖摘要 + 链接
- **注意事项**：
  - Reddit 反感自我推广，需要参与社区互动
  - 每个 subreddit 有自己的规则，先阅读
  - 过度发链接会被标记为 spam

### 27. Hacker News

- **发布入口**：https://news.ycombinator.com/submit
- **发布方式**：标题 + URL
- **操作流程**：提交标题和博客链接
- **注意事项**：
  - 技术深度文章可能获得大量流量
  - 社区对内容质量要求极高
  - 不适合频繁提交，选择最优质的文章

### 28. Facebook Page

- **发布方式**：摘要 + 链接
- **API**：Graph API（需 Page 权限）
- **操作流程**：在 Page 发布带链接的帖子
- **注意事项**：
  - 以引流为主
  - 适合非技术类内容或科普文

### 29. YouTube

- **发布入口**：https://studio.youtube.com
- **内容格式**：视频为主，支持社区帖子（图文）
- **API**：YouTube Data API v3（官方）
- **适合内容**：技术教程视频、代码演示、技术分享录播
- **操作流程**：
  1. 录制技术讲解视频或代码演示
  2. 上传到 YouTube Studio
  3. 设置标题、描述（含博客链接）、标签、缩略图
  4. 发布
- **注意事项**：
  - 视频描述中放置博客原文链接引流
  - 可将博客内容转化为视频脚本
  - YouTube SEO 在 Google 搜索中权重极高
  - 社区帖子可发图文摘要 + 链接

---

## 分发工具

### Wechatsync（浏览器插件）— 推荐

- **安装**：Chrome/Edge 应用商店搜索 "Wechatsync"
- **支持平台**：微信公众号、知乎、掘金、CSDN、简书、博客园、SegmentFault、头条号、百家号、Medium、WordPress 等
- **使用方式**：
  1. 各平台提前登录
  2. 在微信公众号后台编辑好文章
  3. 点击插件 → 勾选目标平台 → 一键同步
- **GitHub**：https://github.com/AegeanCrew/wechatsync（开源免费）

### doocs/md（Markdown 转微信格式）

- **地址**：https://doocs.github.io/md/
- **用途**：Markdown → 微信公众号富文本
- **使用**：粘贴 Markdown → 选择主题 → 复制到公众号

### mdnice

- **地址**：https://mdnice.com
- **用途**：Markdown 排版，支持多种主题
- **特色**：一键复制到微信、知乎

---

## 发布 SOP（标准操作流程）

### 每篇文章发布检查清单

- [ ] 博客原站已发布并确认可访问
- [ ] 文章底部包含原文链接
- [ ] 准备好封面图（建议 16:9，1200x630px）
- [ ] 准备好文章摘要（150 字以内）
- [ ] 准备好标签/话题（3-5 个）

### 推荐发布顺序

```
第 1 天：博客原站发布（等待搜索引擎收录）
  ↓
第 2 天：分发到各平台
  ↓
  ├─ 1. 微信公众号（doocs/md 排版 → 粘贴发布）
  ├─ 2. 使用 Wechatsync 同步到：知乎、掘金、CSDN、博客园等
  ├─ 3. Dev.to（粘贴 Markdown + canonical_url）
  ├─ 4. Hashnode（粘贴 Markdown + canonical_url）
  ├─ 5. Medium（Import Story 或粘贴 + canonical link）
  └─ 6. X/LinkedIn（发布摘要 + 链接引流）
```

### canonical URL 设置（重要）

所有平台的文章都应指向博客原文，避免 SEO 重复内容惩罚：

```
原文地址格式：https://blog.es007.com/posts/<文章slug>/
```

- Dev.to / Hashnode / Medium：支持 canonical_url 字段
- 知乎 / 掘金 / CSDN 等：在文末注明"本文首发于 blog.es007.com"

---

## 账号注册清单

| 平台 | 注册状态 | 账号/主页 | 备注 |
|------|----------|-----------|------|
| 微信公众号 | ✅ 已注册 | 亿思007小龙虾 | es007_openclaw |
| 知乎 | ⬜ 待注册 | | |
| 掘金 | ⬜ 待注册 | | |
| CSDN | ⬜ 待注册 | | |
| 博客园 | ⬜ 待注册 | | |
| 简书 | ⬜ 待注册 | | |
| SegmentFault | ⬜ 待注册 | | |
| 开源中国 | ⬜ 待注册 | | |
| 头条号 | ⬜ 待注册 | | |
| 百家号 | ⬜ 待注册 | | |
| 腾讯云社区 | ⬜ 待注册 | | |
| 阿里云社区 | ⬜ 待注册 | | |
| 华为云社区 | ⬜ 待注册 | | |
| 51CTO | ⬜ 待注册 | | |
| 小红书 | ⬜ 待注册 | | 图文卡片形式 |
| 抖音 | ⬜ 待注册 | | 图文/短视频 |
| 快手 | ⬜ 待注册 | | 图文/短视频 |
| B站（哔哩哔哩） | ⬜ 待注册 | | 专栏 + 视频 |
| 微博 | ⬜ 待注册 | | 引流为主 |
| Dev.to | ⬜ 待注册 | | |
| Hashnode | ⬜ 待注册 | | |
| Medium | ⬜ 待注册 | | |
| Substack | ⬜ 待注册 | | |
| LinkedIn | ⬜ 待注册 | | |
| X (Twitter) | ⬜ 待注册 | | |
| Reddit | ⬜ 待注册 | | |
| Facebook | ⬜ 待注册 | | |
| YouTube | ⬜ 待注册 | | 视频 + 社区帖子 |
