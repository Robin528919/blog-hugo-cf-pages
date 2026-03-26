# 小红书自动化发布 - 实现代码示例

> 提供可复用的代码片段和完整示例

---

## Table of Contents

1. [基础 Playwright 自动化](#基础-playwright-自动化)
2. [Hugo → 小红书 完整管道](#hugo--小红书-完整管道)
3. [GitHub Actions 自动发布](#github-actions-自动发布)
4. [错误处理与日志](#错误处理与日志)
5. [反检测与人类行为模拟](#反检测与人类行为模拟)
6. [批量发布管理](#批量发布管理)

---

## 基础 Playwright 自动化

### 安装依赖

```bash
pip install playwright python-frontmatter pillow python-dotenv
playwright install chromium
```

### 最简单的发布脚本

```python
# scripts/xiaohongshu/basic_publish.py

import asyncio
from playwright.async_api import async_playwright, expect
import os
from dotenv import load_dotenv

load_dotenv()

async def publish_xiaohongshu(title: str, content: str, image_paths: list):
    """发布小红书笔记"""

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)  # headless=True 无界面运行
        page = await browser.new_page()

        # 访问小红书
        await page.goto("https://www.xiaohongshu.com/", wait_until="networkidle")

        # 等待登录（如果需要）
        print("请在浏览器中完成登录，然后按 Enter...")
        input()

        # 导航到创作中心
        await page.goto("https://www.xiaohongshu.com/create", wait_until="networkidle")

        # 点击发布笔记
        await page.click("text=新建笔记")

        # 填写标题
        title_input = page.locator('input[placeholder*="添加标题"]')
        await title_input.fill(title)

        # 填写正文
        content_input = page.locator('textarea[placeholder*="说点什么吧"]')
        await content_input.fill(content)

        # 上传图片
        for img_path in image_paths:
            upload_input = page.locator('input[type="file"]')
            await upload_input.set_input_files(img_path)
            await page.wait_for_timeout(2000)  # 等待上传完成

        # 发布
        publish_button = page.locator("button:has-text('发布')")
        await publish_button.click()

        # 等待发布完成
        await page.wait_for_url("**/content/detail/**")
        url = page.url

        print(f"发布成功！URL: {url}")

        await browser.close()
        return url

# 使用方式
asyncio.run(publish_xiaohongshu(
    title="我的第一篇笔记",
    content="这是笔记内容...",
    image_paths=["image1.jpg", "image2.jpg"]
))
```

### 带登录验证的脚本

```python
# scripts/xiaohongshu/publish_with_login.py

import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def login_xiaohongshu(page, username: str, password: str):
    """登录小红书"""

    # 访问登录页
    await page.goto("https://www.xiaohongshu.com/")

    # 点击登录按钮
    login_btn = page.locator("text=登录")
    await login_btn.click()

    # 等待登录窗口
    await page.wait_for_selector("[placeholder='手机号/邮箱']", timeout=5000)

    # 输入用户名
    username_input = page.locator("[placeholder='手机号/邮箱']")
    await username_input.fill(username)

    # 输入密码
    password_input = page.locator("[type='password']")
    await password_input.fill(password)

    # 点击登录
    login_button = page.locator("button:has-text('登录')")
    await login_button.click()

    # 等待登录完成（需要验证码或生物识别）
    print("请完成验证码或生物识别验证...")
    await page.wait_for_url("**/home**", timeout=30000)

    print("登录成功！")

async def publish_with_login(title: str, content: str, images: list):
    """带登录的完整发布流程"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 登录
        username = os.getenv("XHS_USERNAME")
        password = os.getenv("XHS_PASSWORD")
        await login_xiaohongshu(page, username, password)

        # 导航到创作中心
        await page.goto("https://www.xiaohongshu.com/create", wait_until="networkidle")

        # 点击新建笔记
        new_note_btn = page.locator("text=新建笔记")
        await new_note_btn.click()

        # 填写内容
        await page.wait_for_selector("textarea", timeout=5000)
        textarea = page.locator("textarea").first
        await textarea.fill(content)

        # 填写标题
        title_input = page.locator("input[placeholder*='标题']")
        await title_input.fill(title)

        # 上传图片
        file_inputs = page.locator("input[type='file']")
        for idx, img_path in enumerate(images):
            # 获取最后一个文件输入框
            last_input = file_inputs.last
            await last_input.set_input_files(img_path)
            await page.wait_for_timeout(3000)

        # 点击发布
        publish_btn = page.locator("button:has-text('发布')")
        await publish_btn.click()

        # 等待发布完成
        await page.wait_for_timeout(5000)
        final_url = page.url

        await browser.close()
        return final_url

# 使用
if __name__ == "__main__":
    asyncio.run(publish_with_login(
        title="我的技术笔记",
        content="这是一篇关于技术的分享...",
        images=["img/hero.jpg", "img/diagram.jpg"]
    ))
```

---

## Hugo → 小红书 完整管道

### 方案 1: 从 Markdown 直接发布

```python
# scripts/xiaohongshu/hugo_to_xhs.py

import asyncio
from pathlib import Path
import frontmatter
from PIL import Image
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

class HugoToXiaoHongShu:
    def __init__(self, hugo_root="./"):
        self.hugo_root = Path(hugo_root)
        self.content_dir = self.hugo_root / "content" / "posts"
        self.static_dir = self.hugo_root / "static" / "images"
        self.published_log = self.hugo_root / "scripts" / "xiaohongshu" / "xhs_published.json"

    def read_post(self, post_file: Path) -> dict:
        """读取 Hugo 文章"""
        with open(post_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        return {
            'title': post.metadata.get('title', ''),
            'content': post.content,
            'tags': post.metadata.get('tags', []),
            'description': post.metadata.get('description', ''),
            'date': post.metadata.get('date'),
            'slug': post_file.stem,
        }

    def extract_images(self, slug: str) -> list:
        """提取文章的配图"""
        img_dir = self.static_dir / slug
        if not img_dir.exists():
            return []

        # 优先查找 hero 图和 SVG/PNG
        images = []

        # 首先添加 hero 图
        hero = img_dir / "hero.png"
        if hero.exists():
            images.append(str(hero))
        else:
            hero_svg = img_dir / "hero.svg"
            if hero_svg.exists():
                images.append(str(hero_svg))

        # 添加其他图片（按修改时间排序）
        other_images = sorted(
            [f for f in img_dir.glob("*.png") if f.name != "hero.png"],
            key=lambda x: x.stat().st_mtime
        )
        images.extend([str(img) for img in other_images[:8]])  # 最多 9 张

        return images

    def preprocess_content(self, content: str, max_length: int = 1000) -> str:
        """处理内容以符合小红书规范"""

        # 移除 Markdown 格式
        content = content.replace("# ", "").replace("## ", "").replace("### ", "")
        content = content.replace("**", "").replace("*", "").replace("__", "")

        # 限制长度
        if len(content) > max_length:
            content = content[:max_length]

        # 移除多余空行
        content = "\n".join(line for line in content.split("\n") if line.strip())

        return content.strip()

    def is_published(self, slug: str) -> bool:
        """检查文章是否已发布"""
        if not self.published_log.exists():
            return False

        with open(self.published_log, 'r', encoding='utf-8') as f:
            published = json.load(f)

        return slug in published

    def mark_as_published(self, slug: str, url: str):
        """标记文章为已发布"""
        published = {}
        if self.published_log.exists():
            with open(self.published_log, 'r', encoding='utf-8') as f:
                published = json.load(f)

        published[slug] = {
            'url': url,
            'published_at': datetime.now().isoformat()
        }

        os.makedirs(self.published_log.parent, exist_ok=True)
        with open(self.published_log, 'w', encoding='utf-8') as f:
            json.dump(published, f, ensure_ascii=False, indent=2)

    async def publish_post(self, post_file: Path, dry_run: bool = False):
        """发布单篇文章"""

        # 读取文章
        post = self.read_post(post_file)
        slug = post['slug']

        # 检查是否已发布
        if self.is_published(slug):
            print(f"⏭️  跳过已发布文章: {post['title']}")
            return

        print(f"📝 准备发布: {post['title']}")

        # 提取配图
        images = self.extract_images(slug)
        if not images:
            print(f"⚠️  未找到配图，跳过: {slug}")
            return

        # 预处理内容
        content = self.preprocess_content(post['content'])

        if dry_run:
            print(f"【DRY RUN】")
            print(f"  标题: {post['title']}")
            print(f"  字数: {len(content)}")
            print(f"  标签: {', '.join(post['tags'])}")
            print(f"  图片: {len(images)} 张")
            print()
            return

        # 实际发布（这里调用 Playwright 脚本）
        print(f"🚀 正在发布: {post['title']}")
        # ... 调用发布函数 ...
        # url = await publish_to_xiaohongshu(...)

        # print(f"✅ 发布成功: {url}")
        # self.mark_as_published(slug, url)

    async def run(self, dry_run: bool = False, all_posts: bool = False):
        """运行发布流程"""

        post_files = sorted(self.content_dir.glob("*.md"))

        if not all_posts:
            # 只发布最新的一篇
            post_files = post_files[-1:]

        for post_file in post_files:
            await self.publish_post(post_file, dry_run=dry_run)

# 使用方式
if __name__ == "__main__":
    publisher = HugoToXiaoHongShu(hugo_root="./")

    # Dry run 预览
    asyncio.run(publisher.run(dry_run=True, all_posts=False))

    # 实际发布
    # asyncio.run(publisher.run(dry_run=False, all_posts=False))
```

### 方法 2: 与 Wechatsync 集成

```python
# scripts/xiaohongshu/via_wechatsync.py

import os
from pathlib import Path
import subprocess
import json
from datetime import datetime

class WechatsyncPublisher:
    """通过 Wechatsync 发布到小红书"""

    def __init__(self, hugo_root="./"):
        self.hugo_root = Path(hugo_root)
        self.wechat_draft_log = self.hugo_root / "scripts" / "xiaohongshu" / "wechat_drafts.json"

    def read_wechat_draft_log(self) -> dict:
        """读取微信公众号草稿记录"""
        if self.wechat_draft_log.exists():
            with open(self.wechat_draft_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def log_wechat_draft(self, slug: str, article_title: str):
        """记录要同步的微信草稿"""
        log = self.read_wechat_draft_log()
        log[slug] = {
            'title': article_title,
            'wechat_status': 'draft',
            'logged_at': datetime.now().isoformat(),
            'instruction': 'Open WeChat article → Wechatsync → Select Xiaohongshu'
        }

        os.makedirs(self.wechat_draft_log.parent, exist_ok=True)
        with open(self.wechat_draft_log, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    def generate_sync_instruction(self, slug: str, title: str) -> str:
        """生成同步说明"""
        return f"""
        【Wechatsync 同步说明】

        文章: {title}

        步骤:
        1. 打开微信公众号后台: https://mp.weixin.qq.com/
        2. 找到刚发布的文章: "{title}"
        3. 点击浏览器右上角 Wechatsync 图标
        4. 选择 "小红书"
        5. 确认同步
        6. 等待同步到小红书草稿箱（1-2 分钟）
        7. 登录小红书编辑并发布

        文章 slug: {slug}
        """

# 使用方式
publisher = WechatsyncPublisher()
publisher.log_wechat_draft(
    slug="my-article",
    article_title="我的技术分享文章"
)
print(publisher.generate_sync_instruction("my-article", "我的技术分享文章"))
```

---

## GitHub Actions 自动发布

### 完整 Workflow

```yaml
# .github/workflows/xiaohongshu-auto-publish.yml

name: Auto Publish to Xiaohongshu

on:
  push:
    paths:
      - 'content/posts/**'
    branches:
      - main

jobs:
  detect_changes:
    runs-on: ubuntu-latest
    outputs:
      new_posts: ${{ steps.detect.outputs.new_posts }}
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 2

      - name: Detect new posts
        id: detect
        run: |
          # 比较最近两个 commit
          NEW_POSTS=$(git diff --name-only HEAD~1 HEAD | grep "content/posts/" | tr '\n' ',')
          echo "new_posts=$NEW_POSTS" >> $GITHUB_OUTPUT

  publish:
    needs: detect_changes
    runs-on: ubuntu-latest
    if: needs.detect_changes.outputs.new_posts != ''

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install playwright python-frontmatter pillow python-dotenv
          playwright install chromium

      - name: Publish to Xiaohongshu
        run: |
          python scripts/xiaohongshu/hugo_to_xhs.py \
            --hugo-root . \
            --dry-run false \
            --all-posts false
        env:
          XHS_USERNAME: ${{ secrets.XHS_USERNAME }}
          XHS_PASSWORD: ${{ secrets.XHS_PASSWORD }}

      - name: Update publication log
        if: success()
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add scripts/xiaohongshu/xhs_published.json
          git commit -m "chore: update xiaohongshu publication log" || true
          git push

      - name: Notify on failure
        if: failure()
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Xiaohongshu auto publish failed. Check the workflow logs.'
            })
```

---

## 错误处理与日志

### 完整的错误处理框架

```python
# scripts/xiaohongshu/error_handler.py

import logging
import traceback
from enum import Enum
from typing import Callable, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/xiaohongshu.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    LOGIN_FAILED = "login_failed"
    NETWORK_ERROR = "network_error"
    UPLOAD_FAILED = "upload_failed"
    PUBLISH_FAILED = "publish_failed"
    INVALID_CONTENT = "invalid_content"
    VERIFICATION_REQUIRED = "verification_required"
    UNKNOWN = "unknown"

class XiaoHongShuError(Exception):
    """小红书自动化基础异常"""

    def __init__(self, error_type: ErrorType, message: str, details: dict = None):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def log(self):
        logger.error(f"[{self.error_type.value}] {self.message}")
        if self.details:
            logger.error(f"Details: {self.details}")

async def with_error_handling(
    func: Callable,
    *args,
    max_retries: int = 3,
    **kwargs
) -> Any:
    """带重试机制的错误处理装饰器"""

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_retries}: {func.__name__}")
            return await func(*args, **kwargs)

        except XiaoHongShuError as e:
            e.log()

            if e.error_type == ErrorType.VERIFICATION_REQUIRED:
                logger.warning("需要手动验证，停止重试")
                raise

            if attempt == max_retries:
                logger.error(f"所有重试均失败: {func.__name__}")
                raise

            wait_time = 5 * attempt
            logger.info(f"等待 {wait_time} 秒后重试...")
            await asyncio.sleep(wait_time)

        except Exception as e:
            logger.error(f"未预期的错误: {str(e)}")
            logger.error(traceback.format_exc())
            raise XiaoHongShuError(
                ErrorType.UNKNOWN,
                f"Unexpected error in {func.__name__}",
                {'original_error': str(e)}
            )

# 使用示例
async def example_publish():
    async def publish_task():
        # 发布逻辑
        pass

    try:
        await with_error_handling(
            publish_task,
            max_retries=3
        )
    except XiaoHongShuError as e:
        logger.critical(f"发布失败: {e.message}")
```

---

## 反检测与人类行为模拟

### 人类行为模拟

```python
# scripts/xiaohongshu/anti_detection.py

import asyncio
import random
from playwright.async_api import Page

class HumanBehavior:
    """模拟人类行为"""

    @staticmethod
    async def random_delay(min_ms: int = 500, max_ms: int = 3000):
        """随机延迟"""
        delay = random.uniform(min_ms / 1000, max_ms / 1000)
        await asyncio.sleep(delay)

    @staticmethod
    async def type_like_human(page: Page, selector: str, text: str):
        """像人一样打字（逐字输入）"""
        element = page.locator(selector)
        await element.click()

        # 逐字输入，每个字之间有随机延迟
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))

        await HumanBehavior.random_delay()

    @staticmethod
    async def move_mouse_slowly(page: Page, start_x: int, start_y: int, end_x: int, end_y: int):
        """缓慢移动鼠标"""
        steps = random.randint(10, 20)
        for i in range(steps):
            x = start_x + (end_x - start_x) * (i / steps)
            y = start_y + (end_y - start_y) * (i / steps)
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.02, 0.05))

    @staticmethod
    async def scroll_slowly(page: Page, distance: int = 500):
        """缓慢滚动"""
        steps = random.randint(5, 10)
        step_size = distance / steps

        for _ in range(steps):
            await page.mouse.wheel(0, int(step_size))
            await asyncio.sleep(random.uniform(0.1, 0.3))

    @staticmethod
    async def realistic_fill(page: Page, selector: str, text: str):
        """逼真地填充文本框"""
        await page.locator(selector).click()
        await HumanBehavior.random_delay(300, 800)

        # 先清空现有内容
        await page.keyboard.press("Control+A")
        await asyncio.sleep(0.1)

        # 逐字输入
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.02, 0.1))

        await HumanBehavior.random_delay()

# 使用示例
async def publish_with_human_behavior():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://www.xiaohongshu.com/create")

        # 使用人类行为模拟输入
        await HumanBehavior.realistic_fill(
            page,
            "input[placeholder*='标题']",
            "我的笔记标题"
        )

        await HumanBehavior.realistic_fill(
            page,
            "textarea",
            "这是笔记内容..."
        )

        # 滚动到发布按钮
        await HumanBehavior.scroll_slowly(page, 300)

        # 点击发布
        await page.click("button:has-text('发布')")

        await browser.close()
```

---

## 批量发布管理

### 批量发布队列

```python
# scripts/xiaohongshu/batch_publisher.py

import asyncio
from pathlib import Path
from typing import List
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class PublishTask:
    post_file: Path
    slug: str
    title: str
    images: List[str]
    scheduled_time: datetime = None
    status: str = "pending"  # pending, published, failed
    error_message: str = None

class BatchPublisher:
    def __init__(self, max_concurrent: int = 1, min_interval_minutes: int = 30):
        self.max_concurrent = max_concurrent
        self.min_interval = timedelta(minutes=min_interval_minutes)
        self.tasks = []
        self.published_tasks = []

    def add_task(self, post_file: Path, slug: str, title: str, images: List[str]):
        """添加发布任务"""
        task = PublishTask(
            post_file=str(post_file),
            slug=slug,
            title=title,
            images=images
        )
        self.tasks.append(task)

    def schedule_tasks(self):
        """为任务分配时间表（避免同时发布）"""
        now = datetime.now()
        for idx, task in enumerate(self.tasks):
            task.scheduled_time = now + (self.min_interval * idx)
            print(f"📅 {task.title} 计划于 {task.scheduled_time} 发布")

    async def publish_task(self, task: PublishTask):
        """发布单个任务"""
        try:
            # 等待计划时间
            now = datetime.now()
            if task.scheduled_time > now:
                wait_seconds = (task.scheduled_time - now).total_seconds()
                print(f"⏰ 等待 {wait_seconds:.0f} 秒...")
                await asyncio.sleep(wait_seconds)

            print(f"🚀 正在发布: {task.title}")

            # 实际发布逻辑
            # result = await publish_to_xiaohongshu(...)

            task.status = "published"
            print(f"✅ 发布成功: {task.title}")

        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            print(f"❌ 发布失败: {task.title} - {str(e)}")

        finally:
            self.published_tasks.append(task)

    async def run(self):
        """运行批量发布"""
        self.schedule_tasks()

        # 按顺序发布（受并发限制）
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def with_semaphore(task):
            async with semaphore:
                await self.publish_task(task)

        await asyncio.gather(*[with_semaphore(task) for task in self.tasks])

        # 生成报告
        self.generate_report()

    def generate_report(self):
        """生成发布报告"""
        total = len(self.published_tasks)
        successful = sum(1 for t in self.published_tasks if t.status == "published")
        failed = sum(1 for t in self.published_tasks if t.status == "failed")

        report = {
            'timestamp': datetime.now().isoformat(),
            'total': total,
            'successful': successful,
            'failed': failed,
            'tasks': [asdict(t) for t in self.published_tasks]
        }

        # 保存报告
        report_file = Path("logs/batch_publish_report.json")
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n📊 发布报告: {successful}/{total} 成功")

# 使用示例
async def batch_publish_posts():
    publisher = BatchPublisher(max_concurrent=1, min_interval_minutes=30)

    # 添加任务
    publisher.add_task(
        Path("content/posts/article1.md"),
        "article1",
        "我的第一篇文章",
        ["img/article1/hero.jpg"]
    )
    publisher.add_task(
        Path("content/posts/article2.md"),
        "article2",
        "我的第二篇文章",
        ["img/article2/hero.jpg"]
    )

    # 运行
    await publisher.run()

# 执行
if __name__ == "__main__":
    asyncio.run(batch_publish_posts())
```

---

## 配置文件示例

### .env 配置

```bash
# .env

# 小红书账户
XHS_USERNAME=your_phone_number_or_email
XHS_PASSWORD=your_password

# 浏览器配置
HEADLESS=false
BROWSER_TIMEOUT=30000

# 发布配置
MAX_RETRIES=3
PUBLISH_DELAY_MINUTES=30
DRY_RUN=false
```

### config.json

```json
{
  "xiaohongshu": {
    "username": "${XHS_USERNAME}",
    "password": "${XHS_PASSWORD}",
    "create_url": "https://www.xiaohongshu.com/create",
    "max_retries": 3,
    "timeout_ms": 30000
  },
  "content": {
    "max_title_length": 20,
    "max_content_length": 1000,
    "min_content_length": 100,
    "max_images": 9,
    "recommended_image_ratio": "3:4",
    "recommended_image_size": "1080x1440"
  },
  "publishing": {
    "min_interval_minutes": 30,
    "max_concurrent": 1,
    "enable_dry_run": false,
    "enable_logging": true
  }
}
```

---

**最后更新**: 2026-03-24

所有代码示例都可在 GitHub 项目中找到完整实现参考。
