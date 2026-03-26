# 小红书自动化发布研究文档

**研究时间**: 2026 年 3 月
**研究范围**: 官方 API、第三方工具、浏览器自动化、多平台发布方案

---

## 目录

1. [官方 API 方案](#官方-api-方案)
2. [第三方 Python 库与工具](#第三方-python-库与工具)
3. [浏览器自动化方案](#浏览器自动化方案)
4. [多平台发布工具](#多平台发布工具)
5. [内容规格与限制](#内容规格与限制)
6. [部署建议](#部署建议)

---

## 官方 API 方案

### 官方开放平台

小红书提供了官方开放平台 (Open Platform)，支持开发者进行内容发布、数据查询等操作。

**官方资源**:
- 开放平台首页: https://open.xiaohongshu.com/
- API 文档: https://open.xiaohongshu.com/document/api?apiNavigationId=5&id=24&gatewayId=103&gatewayVersionId=1661&apiId=5719
- ApiFox 开发文档: https://xiaohongshu.apifox.cn/
- 发布服务文档: https://xiaohongshu.apifox.cn/doc-2810945
- 开发者文档中心: https://open.xiaohongshu.com/document/developer/file/1

### 账户注册流程

#### 第一步：开发者账户注册
- 访问 https://open.xiaohongshu.com/
- 使用手机号或邮箱注册开发者账户
- 完成企业或个人身份认证：
  - **企业**: 上传营业执照扫描件
  - **个人**: 上传身份证扫描件

#### 第二步：应用创建与审批
1. 登录开发者控制台
2. 进入 "应用管理" → "新建应用"
3. 填写应用名称和应用类型
4. 审批周期：**1-3 个工作日**

#### 第三步：接口权限申请
1. 应用通过审批后，进入应用管理页面
2. 申请特定接口权限（如 "笔记详情 API" "评论 API" "发布 API"）
3. 权限审批周期：**1-5 个工作日**（二次审核）
4. 审批通过后获得：
   - **App Key**
   - **App Secret**
   - **Access Token**（有效期 2 小时，需 OAuth2.0 刷新）
   - **Refresh Token**（有效期 7 天）

### 令牌有效期

| 令牌类型 | 有效期 | 说明 |
|---------|--------|------|
| Access Token | 2 小时 | 用于 API 调用 |
| Refresh Token | 7 天 | 用于刷新 Access Token |
| 重新授权 | 需要 14 天后 | 令牌过期后需用户重新授权 |

### 官方 API 的优缺点

**优点**：
- 官方支持，接口稳定可靠
- 安全性有保障
- 不易被检测为异常行为
- 支持 OAuth2.0 标准认证

**缺点**：
- 申请周期长（2-8 天）
- 审核严格，企业资质要求较高
- 接口功能受限，可能不支持所有发布选项
- 调用需要签名算法（较复杂）

---

## 第三方 Python 库与工具

### 1. jellyfrank/xiaohongshu (轻量级 SDK)

**GitHub**: https://github.com/jellyfrank/xiaohongshu

**特点**:
- 轻量级 Python SDK
- 仅支持数据查询类 API
- 不支持内容发布

**安装**:
```bash
pip install xiaohongshu
```

**使用示例**:
```python
from xiaohongshu.api.api import ARK

ark = ARK("xhs", "9a539709cafc1efc9ef05838be468a28")
ark.comm.get_express_list()  # 获取物流公司列表
```

**模块结构**:
- `comm`: 公共接口封装
- `order`: 订单相关接口
- `stock`: 库存相关接口
- `product`: 商品相关接口

**不推荐用于**: 自动化发布（不支持）

---

### 2. YYH211/xiaohongshu (AI 驱动的内容生成与发布)

**GitHub**: https://github.com/YYH211/xiaohongshu

**特点**:
- ✅ **完全支持自动发布**
- AI 驱动的内容生成与发布系统
- 四步工作流自动化
- 集成 xiaohongshu-mcp 服务
- 支持批量发布

**核心功能**:
1. **信息检索** - 使用 Jina 或 Tavily 搜索
2. **撰写文章** - 自动生成 800-1200 字内容
3. **格式适配** - 符合小红书要求的格式转换
4. **自动发布** - 直接发布到小红书

**工作流程**:
```
主题输入 → 检索资料 → 撰写文章 → 格式化 → 自动发布
```

**特色**:
- 热点发现：自动获取今日热点并按领域筛选
- URL 提取：输入网页链接自动提取主题
- 任务管理：完整历史记录和进度跟踪
- "检测到发布成功后自动停止迭代"

**依赖**:
- xiaohongshu-mcp (MCP Server)
- AI/LLM 服务（用于内容生成）

**适用场景**: AI 内容自动化团队，需要从采集到发布的全流程自动化

---

### 3. Gikiman/Autoxhs (OpenAI + 内容生成)

**GitHub**: https://github.com/Gikiman/Autoxhs

**特点**:
- 利用 OpenAI API 进行内容生成
- 自动生成图片、标题、文本和标签
- 开源工具

**功能**:
- 自动生成小红书笔记内容
- 智能图像生成
- 标签自动化

**适用场景**: 与 OpenAI 深度集成的内容创作流程

---

### 4. jackwener/xiaohongshu-cli (命令行工具)

**GitHub**: https://github.com/jackwener/xiaohongshu-cli

**特点**:
- 逆向工程的 API 实现
- 支持搜索、阅读、互动、发布
- 具有反检测特性
- CLI 命令行界面

**功能**:
- 搜索笔记
- 读取笔记内容
- 社交互动
- 发布笔记

**优点**: 无需官方 API 审批，功能全面
**风险**: 使用逆向工程 API，可能面临反爬虫限制

---

### 5. TikHub/TikHub-API-Python-SDK (多平台支持)

**GitHub**: https://github.com/TikHub/TikHub-API-Python-SDK

**特点**:
- 支持多个平台 API：
  - 抖音 (Douyin)
  - TikTok
  - 小红书
  - 快手 (Kuaishou)
  - 微博 (Weibo)
  - Instagram
  - YouTube
- 高性能异步 Python SDK
- 集成验证码解决器

**适用场景**: 需要多平台统一发布的场景

---

### 6. BetaStreetOmnis/xhs_ai_publisher (AI 内容发布工具)

**GitHub**: https://github.com/BetaStreetOmnis/xhs_ai_publisher

**特点**:
- PyQt 桌面 UI
- FastAPI 服务后端
- 登录状态复用
- 发布预览功能
- 自动化浏览器工作流

**功能**:
- 内容创作（AI 辅助）
- 预览发布
- 自动化浏览器操作

**适用场景**: 需要 UI 交互的个人博主或小团队

---

## 浏览器自动化方案

### 1. Playwright 自动化方案

**推荐项目**: https://github.com/chenningling/Redbook-Search-Comment-MCP2.0

**特点**:
- 基于 Playwright 开发
- 作为 MCP Server 运行
- 支持 Claude Desktop / Cursor 集成
- 反检测，模拟人类行为
- 支持自动登录、搜索、发布评论

**完整自动发布流程**:
```python
# 初始化浏览器连接（Chrome DevTools Protocol）
browser = await chromium.connect_over_cdp("http://localhost:9222")

# 导航到创作中心
await page.goto("https://www.xiaohongshu.com/create")

# 等待内容编辑界面加载
await page.wait_for_selector("编辑框选择器")

# 填充标题、文本、图片
await page.fill("标题选择器", "笔记标题")
await page.fill("正文选择器", "笔记正文")

# 上传图片
await page.set_input_files("图片上传选择器", ["图片1.jpg", "图片2.jpg"])

# 发布
await page.click("发布按钮选择器")
```

**使用 CDP 优点**:
- 不依赖 Selenium（Playwright 2-3 倍更快）
- 原生支持现代浏览器特性
- 更强的反检测能力

### 2. autoclaw-cc/xiaohongshu-skills (Python CDP 引擎)

**GitHub**: https://github.com/autoclaw-cc/xiaohongshu-skills

**特点**:
- Python CDP 浏览器自动化引擎
- 内置反检测与反爬虫保护
- 支持多账户管理
- 模块化设计，支持 OpenClaw/Claude Code

**核心能力模块**:
1. 身份验证与登录
2. 搜索与浏览
3. **内容发布** ✅
4. 社交互动（评论、点赞）
5. 复合操作

**架构**:
```
用户 (自然语言)
  ↓
AI Agent (意图解析和路由)
  ↓
Skill Module (调用相应功能)
  ↓
Browser CDP (执行浏览器操作)
  ↓
小红书前端
```

**配置管理**:
- CSS 选择器集中在 `selectors.py`
- 平台 DOM 变更时易于维护更新

**安装与使用**:
```bash
git clone https://github.com/autoclaw-cc/xiaohongshu-skills
cd xiaohongshu-skills
uv sync  # 安装依赖
```

**集成 Claude Code**:
这个项目设计为 OpenClaw 的 Skill 格式，可直接集成到 Claude Code 中使用。

---

### 3. Redbook-Search-Comment-MCP (Playwright MCP)

**GitHub**: https://github.com/chenningling/Redbook-Search-Comment-MCP2.0

**文档**: [使用 Playwright MCP 实现小红书全自动发布的完整流程](https://blog.csdn.net/Hogwartstester/article/details/151994183)

**特点**:
- MCP Server 实现
- 支持 Claude Desktop / CherryStudio 等 MCP Client
- 完整的自动化流程支持
- 内置反检测机制

**支持的操作**:
- 自动登录
- 关键词搜索
- 获取笔记内容
- 发布 AI 生成的评论
- ✅ **发布笔记**

---

## 多平台发布工具

### Wechatsync (一键多平台同步)

**官方网站**: https://www.wechatsync.com/

**GitHub**: https://github.com/wechatsync/Wechatsync

**特点**:
- ✅ **完全支持小红书**
- 一键同步到 29+ 平台
- 开源免费 Chrome 浏览器扩展
- 支持微信公众号、知乎、掘金、头条、CSDN、简书、微博、抖音、小红书等

**核心优点**:
- **不是爬虫**，不模拟登录
- 使用你自己的登录态
- 调用平台官方接口
- 数据不离开你的设备
- 自动处理格式转换和图片迁移

**工作流**:
1. 在 Chrome 浏览器中安装扩展
2. 登录所有要发布的平台
3. 在微信公众号打开文章
4. 点击 Wechatsync 按钮，选择目标平台
5. 文章自动同步到各平台草稿箱
6. 各平台后台查看、修改、发布

**发布到小红书的特点**:
- 自动转换 Markdown 格式
- 自动迁移图片
- 发布到草稿箱（用户自己完成最终发布）
- 支持标签、分类等平台特有字段

**适用场景**:
- 从微信公众号同步到多平台
- 已有微信账号和登录态
- 不需要完全自动化（中间需要人工审核）

---

## 内容规格与限制

### 笔记类型

小红书支持两种笔记类型：

| 类型 | 格式 | 字数 | 图片 | 说明 |
|------|------|------|------|------|
| 图文笔记 | 图片 + 文字 | 最多 1000 字 | 最多 9 张 | 推荐 600-1000 字 |
| 视频笔记 | 视频 + 文字 | 配文本 | 可含缩略图 | 信息承载量大（2000-3000 字） |

### 文字规范

| 规范项 | 要求 |
|--------|------|
| 标题 | 20 字以内（个人订阅号约 10 中文字）|
| 短笔记最小字数 | 100 字 |
| 长笔记最小字数 | 600 字 |
| 推荐正文字数 | 600-1000 字 |

### 图片规格

#### 宽高比

小红书整篇笔记仅支持 **一种比例**，不可混用：

| 比例 | 推荐尺寸 | 其他常见尺寸 |
|------|---------|------------|
| **3:4 竖版（推荐）** | 1080×1440 | 720×960, 768×1024, 960×1280 |
| **1:1 方形** | 1080×1080 | - |
| **4:3 横版** | 1200×900 | - |

#### 尺寸限制

- **最小**：640px（宽）× 960px（高）
- **最大**：4000px（宽）× 6000px（高）
- **推荐**：1080px（宽），确保清晰度和加载速度平衡

#### 图片质量建议

- 使用高清、明亮、美观的图片
- **首图很关键**，决定点击率
- 避免模糊、低清、低质量内容
- 整篇笔记建议 6-9 张图片
- 3:4 比例的图片占屏面积最大，视觉效果最好

### 视频笔记规格

- 支持竖屏和横屏
- 一条视频笔记可承载 2000-3000 字信息
- 需要配文本说明

### 其他限制

- **文件格式**：JPG, PNG, WebP, AVIF（推荐压缩格式）
- **摘要长度**（微信公众号）：约 30 字符
- **描述字符**：150 字以内（用于 SEO meta description）

### 反检测与反爬虫

小红书官方开放平台实现了：
- **API 调用限制**：控制每个 API 接口的调用频率
- **请求频率限制**：需合理控制请求间隔
- **异常行为检测**：可能识别机器人操作
- **IP 限制**：频繁请求可能导致 IP 被限制

**规避建议**:
- 使用 Playwright/CDP（浏览器自动化）而非直接 API
- 添加随机延迟（模拟人类行为）
- 使用反检测库（如 autoclaw-cc 提供的）
- 错开发布时间
- 使用代理 IP（如有需要）
- 限制并发任务数量

---

## 部署建议

### 方案对比表

| 方案 | 难度 | 审批时间 | 发布速度 | 可靠性 | 成本 | 适用场景 |
|------|------|---------|---------|--------|------|---------|
| **官方 API** | 高 | 2-8 天 | 快 | 高 | 低 | 企业正式集成 |
| **Playwright MCP** | 中 | 0 天 | 中 | 中 | 低 | 个人自动化 + AI Agent |
| **CDP 自动化** (autoclaw) | 中 | 0 天 | 中 | 中 | 低 | Claude Code 集成 |
| **CLI 工具** (jackwener) | 低 | 0 天 | 快 | 低 | 低 | 快速测试原型 |
| **AI 驱动** (YYH211) | 中 | 0 天 | 快 | 中 | 中 | 内容生成 + 自动发布 |
| **Wechatsync** | 极低 | 0 天 | 慢 | 高 | 免费 | 多平台内容同步 |

### 推荐部署架构

**方案 A: Claude Code + Playwright MCP（推荐用于博客自动化）**

```
Hugo 博客 (本地 MD)
  ↓
Claude Code (内容处理)
  ↓
Playwright MCP (浏览器自动化)
  ↓
小红书（笔记发布）
  ↓
Wechatsync（多平台同步）
```

**优点**:
- 可集成 Claude Code 工作流
- 支持自定义内容处理
- 无需官方 API 审批
- 可结合多平台同步

**部署步骤**:
1. 安装 Playwright MCP Server（或 CDP 自动化方案）
2. 在 Claude Code 中配置 MCP 集成
3. 编写发布脚本（调用 MCP Tools）
4. 设置 GitHub Actions 自动触发
5. 可选：Wechatsync 多平台同步

---

**方案 B: 官方 API（推荐用于企业正式场景）**

```
内容管理系统
  ↓
小红书 API (官方)
  ↓
小红书平台
```

**优点**:
- 官方支持，接口稳定
- 安全性高
- 长期可靠

**缺点**:
- 申请周期长（2-8 天）
- 需要企业资质
- 接口功能有限

---

**方案 C: Wechatsync 多平台同步（推荐用于内容复用）**

```
微信公众号文章
  ↓
Wechatsync Chrome 扩展
  ↓
小红书、知乎、掘金、头条等
```

**优点**:
- 完全免费开源
- 支持 29+ 平台
- 不需要开发
- 自动格式转换和图片迁移

**缺点**:
- 需要人工审核发布
- 依赖浏览器登录态
- 不完全自动化

---

### 针对您的博客场景建议

**目标**: 自动发布博客文章到小红书（类似微信公众号同步）

**推荐方案**: **Playwright MCP + Wechatsync**

1. **第一阶段**: 使用 Wechatsync 多平台同步
   - 文章发布到微信公众号后
   - 一键同步到小红书（+ 知乎、掘金等）
   - 简单易用，无需开发

2. **第二阶段**（可选）: 集成 Playwright MCP
   - 编写 Python 脚本或 Claude Code Skill
   - 直接从 Hugo Markdown 发布到小红书
   - 完全自动化流程

**实现路径**:

```bash
# Step 1: 安装 Wechatsync Chrome 扩展
# 访问 https://www.wechatsync.com/

# Step 2: 发布文章到微信公众号（现有流程）

# Step 3: 在微信文章页面点击 Wechatsync → 选择小红书 → 自动同步到草稿箱

# Step 4（可选）: 在 Claude Code 中集成 Playwright MCP
# 参考: https://github.com/chenningling/Redbook-Search-Comment-MCP2.0
```

---

## 速率限制与最佳实践

### 官方 API 限制

- 每个 API 接口有单独的调用限制
- 需要合理控制请求频率
- 避免在短时间内大量请求

### 浏览器自动化限制

小红书可能通过以下方式检测异常行为：
- 操作速度（鼠标移动、点击、输入速度）
- 用户代理（User Agent）
- 请求间隔（两次操作的时间间隔）
- IP 位置变化

**规避策略**:
- 添加随机延迟：`await page.wait_for_timeout(random.randint(500, 2000))`
- 模拟鼠标移动而非直接点击
- 使用合法 User Agent
- 错开发布时间（避免同时发布多篇）
- 使用代理 IP（如检测到 IP 限制）

### 最佳实践

```python
import asyncio
import random
from playwright.async_api import async_playwright

async def publish_with_delays():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 模拟人类行为
        await page.goto("https://www.xiaohongshu.com/create")

        # 随机延迟
        await asyncio.sleep(random.uniform(1, 3))

        # 填充内容
        await page.fill("标题", "文章标题")
        await asyncio.sleep(random.uniform(0.5, 1.5))

        await page.fill("正文", "文章正文内容")
        await asyncio.sleep(random.uniform(0.5, 2))

        # 上传图片（逐个上传，不并发）
        for img in ["img1.jpg", "img2.jpg"]:
            await page.set_input_files("上传框", img)
            await asyncio.sleep(random.uniform(2, 4))  # 上传间隔

        # 发布
        await page.click("发布按钮")
        await asyncio.sleep(random.uniform(2, 5))

        await browser.close()

# 使用方式
asyncio.run(publish_with_delays())
```

---

## 常见问题

### Q1: 小红书官方 API 现在还在开放吗？

A: 是的，小红书官方开放平台仍在运营（https://open.xiaohongshu.com/），但以下几点需要注意：
- 审批流程相对严格
- 内容发布接口可能需要额外资质
- 建议先咨询官方客服确认您的使用场景是否满足条件

### Q2: 使用浏览器自动化发布会被检测到吗？

A: 风险存在但可控：
- 使用 Playwright + CDP（而非 Selenium）可大幅降低被检测概率
- 使用反检测库（如 autoclaw-cc）进一步增强隐蔽性
- 添加随机延迟和人类行为模拟是关键
- 小红书一般不会对自动化工具作为严格的限制（与抖音不同），只要不过度就可以

### Q3: Wechatsync 完全自动化发布吗？

A: 不是。Wechatsync 的工作流：
1. 文章自动同步到各平台的 **草稿箱**
2. 需要在各平台后台手动审核和发布
3. 优势是自动处理格式转换和跨平台适配

### Q4: 推荐用哪个方案？

A: 根据您的情况：
- **已有微信公众号** → 优先试 Wechatsync（最简单）
- **需要完全自动化** → Playwright MCP 或 CDP 自动化
- **企业正式用途** → 申请官方 API（周期长但最稳定）
- **快速原型验证** → CLI 工具（jackwener）快速测试

### Q5: 能否同时发布到多个平台？

A: 可以，两个思路：
1. **Wechatsync**: 从微信一键同步到小红书、知乎、掘金等 29+ 平台
2. **TikHub SDK**: 使用统一接口发布到小红书、抖音、快手等平台

### Q6: 图片尺寸最重要的是什么？

A: 三点最重要：
1. **使用 3:4 竖版**（1080×1440px）— 占屏面积最大
2. **首图高清美观** — 决定点击率
3. **整篇统一比例** — 避免系统自动裁剪导致显示问题

---

## 参考资源

### 官方文档
- [小红书开放平台](https://open.xiaohongshu.com/)
- [开发者文档中心](https://open.xiaohongshu.com/document/developer/file/1)
- [API 文档](https://xiaohongshu.apifox.cn/)

### 推荐开源项目
- **Playwright MCP**: https://github.com/chenningling/Redbook-Search-Comment-MCP2.0
- **CDP 自动化**: https://github.com/autoclaw-cc/xiaohongshu-skills
- **AI 内容生成**: https://github.com/YYH211/xiaohongshu
- **多平台同步**: https://github.com/wechatsync/Wechatsync
- **Python SDK**: https://github.com/jellyfrank/xiaohongshu

### 学习文档
- [使用 Playwright MCP 实现小红书全自动发布](https://blog.csdn.net/Hogwartstester/article/details/151994183)
- [小红书 API 接口完全指南](https://blog.csdn.net/lovelin_5566/article/details/142362259)
- [小红书内容发布流程与最佳实践](https://blog.csdn.net/jxhaha/article/details/141315550)

---

## 更新日志

- **2026-03-24**: 完成小红书自动化发布全面研究（官方 API、第三方库、浏览器自动化、多平台方案）

---

**文档维护**: 建议每 2-3 个月检查一次官方 API 和热门开源项目的更新，小红书平台迭代较快。
