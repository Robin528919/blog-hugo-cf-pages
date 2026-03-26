# 小红书自动化发布 - 快速开始指南

> 针对博客场景的快速部署方案

---

## 30 秒快速选择

您应该用哪个方案？

- **已有微信公众号 + 文章已发布** → [使用 Wechatsync](#方案1-wechatsync-最简单)
- **想要完全自动化发布** → [使用 Playwright MCP](#方案2-playwright-mcp-完全自动)
- **集成 Claude Code 工作流** → [使用 CDP 自动化](#方案3-cdp-自动化)
- **仅做快速原型验证** → [使用 CLI 工具](#方案4-cli-工具快速验证)

---

## 方案 1: Wechatsync（最简单）

### 特点
- 无需编码
- 一键同步到 29+ 平台
- 完全免费开源
- 支持格式自动转换

### 安装步骤

#### 步骤 1: 安装 Chrome 扩展
1. 访问 https://www.wechatsync.com/
2. 点击 "Chrome 扩展" 或直接访问 Chrome Web Store
3. 添加到 Chrome

#### 步骤 2: 登录各平台
1. 在 Chrome 浏览器中登录以下平台：
   - 微信公众号后台（https://mp.weixin.qq.com/）
   - 小红书 (https://www.xiaohongshu.com/)
   - 其他目标平台（知乎、掘金等）

#### 步骤 3: 一键同步
1. 打开微信公众号发布的文章
2. 点击浏览器右上角 Wechatsync 扩展图标
3. 选择 "小红书" 等目标平台
4. 确认→ 自动同步到小红书草稿箱

#### 步骤 4: 发布
1. 登录小红书
2. 进入创作中心 → 草稿
3. 找到同步的文章
4. 审核、修改、发布

### 工作流完整示例

```
1. 在 Hugo 本地写文章 (content/posts/xxx.md)
   ↓
2. 发布到微信公众号（使用现有流程）
   ↓
3. 打开微信文章 → Wechatsync → 选择小红书
   ↓
4. 文章自动到小红书草稿箱
   ↓
5. 登录小红书后台，最后审核 + 发布
```

### 优点
- ✅ 无需开发
- ✅ 完全免费
- ✅ 自动处理格式和图片
- ✅ 可同步到 29+ 平台

### 缺点
- ❌ 不是完全自动化（需人工最后发布）
- ❌ 依赖微信公众号（需提前发布）
- ❌ 依赖浏览器登录态

### 何时使用
- 已有微信公众号
- 可以接受人工审核一次
- 希望最小化学习成本
- 需要同步到多个平台

---

## 方案 2: Playwright MCP（完全自动）

### 特点
- 基于浏览器自动化
- 完全自动化发布
- 支持 Claude Desktop / Cursor
- 可高度定制

### 核心项目

**Redbook-Search-Comment-MCP 2.0**
- GitHub: https://github.com/chenningling/Redbook-Search-Comment-MCP2.0
- 技术: Playwright + MCP Server
- 支持: 登录、搜索、发布、评论

### 快速安装

#### 前置要求
- Python 3.8+
- Chrome/Chromium 浏览器
- Claude Desktop 或 Cursor（可选）

#### 步骤 1: 克隆项目
```bash
git clone https://github.com/chenningling/Redbook-Search-Comment-MCP2.0
cd Redbook-Search-Comment-MCP2.0
```

#### 步骤 2: 安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤 3: 配置小红书账户

编辑 `config.json`：
```json
{
  "xiaohongshu": {
    "username": "你的小红书手机号或邮箱",
    "password": "你的小红书密码"
  }
}
```

#### 步骤 4: 运行 MCP Server
```bash
python main.py
```

#### 步骤 5（可选）: 集成 Claude Desktop

编辑 `~/.claude/claude_desktop_config.json`：
```json
{
  "mcpServers": {
    "xiaohongshu-mcp": {
      "command": "python",
      "args": ["/path/to/main.py"]
    }
  }
}
```

### 在 Claude Code 中使用

```python
# 在 Claude Code 中直接调用
# (MCP Server 自动处理浏览器操作)

from xiaohongshu_mcp import XHS

xhs = XHS()

# 登录
await xhs.login()

# 发布笔记
await xhs.publish(
    title="我的第一篇笔记",
    content="这是笔记内容...",
    images=["image1.jpg", "image2.jpg"],
    tags=["技术", "分享"]
)

# 获取推荐
recommendations = await xhs.get_recommendations(keyword="技术写作")
```

### 发布脚本示例

```python
import asyncio
from pathlib import Path
from xiaohongshu_mcp import XHS
import frontmatter

async def publish_from_markdown(md_file):
    """从 Markdown 文件发布到小红书"""

    # 读取 Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    metadata = post.metadata
    content = post.content

    # 初始化小红书
    xhs = XHS()
    await xhs.login()

    # 发布
    result = await xhs.publish(
        title=metadata.get('title', ''),
        content=content[:1000],  # 小红书限制 1000 字
        images=metadata.get('images', []),
        tags=metadata.get('tags', [])
    )

    print(f"发布成功! URL: {result['url']}")

# 使用
asyncio.run(publish_from_markdown('content/posts/my-article.md'))
```

### GitHub Actions 自动发布

创建 `.github/workflows/xiaohongshu-publish.yml`：

```yaml
name: Publish to Xiaohongshu

on:
  push:
    paths:
      - 'content/posts/**'
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r scripts/xiaohongshu/requirements.txt

      - name: Publish to Xiaohongshu
        run: |
          python scripts/xiaohongshu/publish.py
        env:
          XHS_USERNAME: ${{ secrets.XHS_USERNAME }}
          XHS_PASSWORD: ${{ secrets.XHS_PASSWORD }}

      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add -A
          git commit -m "chore: update xiaohongshu publish status" || true
          git push
```

### 优点
- ✅ 完全自动化
- ✅ 可集成 Claude Code
- ✅ 灵活定制
- ✅ 支持多账户
- ✅ 反检测内置

### 缺点
- ❌ 需要编码能力
- ❌ 需要配置账户密码（安全风险）
- ❌ 浏览器自动化可能被检测

### 何时使用
- 需要完全自动化
- 已有 Python 基础
- 想集成 AI Agent 工作流
- 可接受一定的技术复杂度

---

## 方案 3: CDP 自动化

### 项目

**autoclaw-cc/xiaohongshu-skills**
- GitHub: https://github.com/autoclaw-cc/xiaohongshu-skills
- 技术: Python CDP（Chrome DevTools Protocol）
- 特点: 更强反检测，支持 OpenClaw/Claude Code

### 快速安装

```bash
git clone https://github.com/autoclaw-cc/xiaohongshu-skills
cd xiaohongshu-skills
uv sync  # 或 pip install -r requirements.txt
```

### 与 Claude Code 集成

这个项目原生支持 Claude Code Skill 格式，可直接在 Claude Code 中使用。

### 优点
- ✅ 更强的反检测能力
- ✅ 原生支持 Claude Code
- ✅ 模块化设计
- ✅ 支持多账户

### 何时使用
- 使用 Claude Code 进行自动化
- 需要更强的反检测
- 需要模块化的可复用 Skills

---

## 方案 4: CLI 工具（快速验证）

### 项目

**jackwener/xiaohongshu-cli**
- GitHub: https://github.com/jackwener/xiaohongshu-cli
- 特点: 快速、轻量、无需审批

### 快速开始

```bash
pip install xiaohongshu-cli

# 搜索笔记
xhs search "技术写作"

# 发布笔记
xhs publish \
  --title "我的笔记" \
  --content "笔记内容" \
  --images "img1.jpg,img2.jpg" \
  --tags "技术,分享"

# 获取笔记详情
xhs get <note-id>
```

### 优点
- ✅ 安装最简单
- ✅ 无需繁琐配置
- ✅ 适合快速验证
- ✅ 轻量级

### 缺点
- ❌ 逆向工程 API（风险）
- ❌ 可能被反爬虫检测
- ❌ 长期稳定性未知

### 何时使用
- 快速原型验证
- 想快速看到效果
- 不作为长期方案

---

## 内容规格速查表

### 文字

| 项目 | 规范 |
|------|------|
| 标题 | 20 字以内 |
| 最小正文 | 100 字（短笔记），600 字（长笔记） |
| 推荐正文 | 600-1000 字 |

### 图片

| 项目 | 规范 |
|------|------|
| 宽高比 | 3:4（推荐），1:1，4:3 |
| 推荐尺寸 | 1080×1440px（3:4）|
| 最小尺寸 | 640×960px |
| 最大尺寸 | 4000×6000px |
| 图片数量 | 最多 9 张（整篇一致比例）|
| 质量 | 高清、明亮、美观 |

### 视频

- 支持竖屏和横屏
- 一条视频可承载 2000-3000 字信息
- 需要配文本说明

---

## 部署清单

选定方案后，按照此清单部署：

### Wechatsync 部署清单
- [ ] 安装 Chrome 扩展
- [ ] 登录微信公众号
- [ ] 登录小红书
- [ ] 发送测试文章
- [ ] 验证格式和图片转换

### Playwright MCP 部署清单
- [ ] 克隆项目
- [ ] 安装 Python 依赖
- [ ] 配置 credentials.json
- [ ] 测试登录
- [ ] 发送测试笔记
- [ ] 集成 GitHub Actions（可选）

### CDP 自动化部署清单
- [ ] 克隆项目
- [ ] 安装依赖（uv sync）
- [ ] 配置小红书账户
- [ ] 测试发布
- [ ] 集成 Claude Code（可选）

---

## 常见问题排查

### Q: Playwright 登录失败

**症状**: `selenium.common.exceptions.TimeoutException`

**解决**:
```python
# 添加调试代码
await page.screenshot(path="login_page.png")  # 截图查看

# 增加等待时间
await page.wait_for_selector("验证码框", timeout=10000)

# 手动验证
await page.pause()  # 暂停，手动处理验证码
```

### Q: 图片上传失败

**症状**: `No such file or directory`

**解决**:
```python
# 确保使用绝对路径
from pathlib import Path

img_path = Path("/absolute/path/to/image.jpg").absolute()
await page.set_input_files("上传框", str(img_path))
```

### Q: 检测到异常行为

**症状**: 登录成功但发布时被阻止

**解决**:
- 添加随机延迟: `await page.wait_for_timeout(random.randint(1000, 3000))`
- 使用 CDP 而非 Selenium
- 错开发布时间
- 使用代理 IP

### Q: Wechatsync 扩展无反应

**症状**: 点击扩展无反应

**解决**:
- 重启 Chrome 浏览器
- 检查是否登录了所有目标平台
- 在 Chrome 扩展设置中重新启用
- 查看 Chrome 开发者工具的控制台报错

---

## 安全建议

### 密码管理

**不安全** ❌
```python
# 直接在代码中硬编码密码
xhs.login("username", "your_password_here")
```

**安全** ✅
```python
import os
from dotenv import load_dotenv

load_dotenv()

xhs.login(
    os.getenv("XHS_USERNAME"),
    os.getenv("XHS_PASSWORD")
)
```

### GitHub Secrets 设置

1. 进入项目 Settings → Secrets and variables
2. 添加 `XHS_USERNAME` 和 `XHS_PASSWORD`
3. 在 GitHub Actions 中使用：
   ```yaml
   env:
     XHS_USERNAME: ${{ secrets.XHS_USERNAME }}
     XHS_PASSWORD: ${{ secrets.XHS_PASSWORD }}
   ```

### 图片隐私

- 确保配图中没有个人隐私信息
- 删除 EXIF 数据（位置信息等）

```python
from PIL import Image
from PIL.ExifTags import TAGS

def remove_exif(image_path):
    """移除图片 EXIF 数据"""
    img = Image.open(image_path)
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    image_without_exif.save(image_path)
```

---

## 下一步

1. **选择方案** → 根据需求从上面 4 个方案中选择
2. **快速验证** → 发送一篇测试笔记验证流程
3. **集成现有工作流** → 与 Hugo、GitHub Actions 等集成
4. **监控发布** → 设置日志和告警

---

## 相关文档

- [完整研究指南](./xiaohongshu-publishing-guide.md)
- [Playwright MCP 文档](https://github.com/chenningling/Redbook-Search-Comment-MCP2.0)
- [autoclaw-cc 项目](https://github.com/autoclaw-cc/xiaohongshu-skills)
- [Wechatsync 官方网站](https://www.wechatsync.com/)

---

**最后更新**: 2026-03-24

**建议**: 优先尝试 Wechatsync（最简单），如果需要完全自动化再进阶到 Playwright MCP 或 CDP 方案。
