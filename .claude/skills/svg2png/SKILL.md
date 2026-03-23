---
name: svg2png
description: "【自动触发】在 git add/commit 前自动将 SVG 配图转换为 PNG。无需手动调用。当 Claude 即将执行 git add 或 git commit 时，必须先检查并转换所有新增/修改的 SVG 文件。触发词：svg转png、转换图片、svg2png。"
metadata:
  version: 2.0.0
---

# SVG → PNG 自动预渲染

## 核心规则（CRITICAL）

**在执行任何 `git add` 或 `git commit` 之前，必须自动执行 SVG→PNG 转换。**

这是强制行为，不需要用户提醒。只要会话中涉及以下任一操作，就必须先运行转换：
- 创建/修改了 SVG 文件
- 创建/修改了博客文章（`content/posts/`）
- 用户要求提交代码
- 执行 `git add` 或 `git commit`

## 自动转换脚本

在 `git add` **之前**执行：

```bash
find static/images -name "*.svg" | while read svg; do
  png="${svg%.svg}.png"
  if [ ! -f "$png" ] || [ "$svg" -nt "$png" ]; then
    rsvg-convert -w 900 "$svg" -o "$png" && echo "✓ 转换: $(basename $svg) → $(basename $png)"
  fi
done
```

然后将生成的 PNG 一并加入 `git add`。

## 为什么需要自动预渲染

- 微信公众号不支持 SVG，需要 PNG
- CI 上的 cairosvg 无法渲染 emoji（🦞 显示为 ☒）
- macOS 本地的 `rsvg-convert` 完美支持 emoji 和中文
- 自动化防止遗漏，确保每次提交都包含最新的 PNG

## 前置依赖

```bash
brew install librsvg
```

## 转换规则

- 输出宽度：900px（微信文章最大宽度）
- 文件位置：PNG 与 SVG 同目录同名（`hero.svg` → `hero.png`）
- 跳过条件：PNG 已存在且比 SVG 更新
- `publish.py` 优先使用预渲染 PNG，找不到才回退到 cairosvg

## 完整工作流示例

```
1. Claude 创建/修改了 static/images/xxx/hero.svg
2. 用户说"提交"
3. Claude 自动执行 SVG→PNG 转换（本规则）
4. Claude 执行 git add（包含 .svg 和 .png）
5. Claude 执行 git commit
```
