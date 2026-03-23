---
name: svg2png
description: 将博客文章配图从 SVG 转换为 PNG。在提交文章前使用，确保微信公众号发布时图片中的 emoji 和中文正常显示。触发词："svg转png"、"转换图片"、"svg2png"、"图片预渲染"、"准备微信图片"。
metadata:
  version: 1.0.0
---

# SVG → PNG 本地预渲染

将 `static/images/` 下的 SVG 配图转换为 PNG，供微信公众号发布使用。

## 为什么需要本地预渲染

- 微信不支持 SVG 格式，需要 PNG
- CI 上的 cairosvg 无法渲染 emoji（🦞 等显示为 ☒）
- macOS 本地的 `rsvg-convert` 使用系统字体，完美支持 emoji 和中文

## 前置依赖

```bash
brew install librsvg
```

## 执行流程

1. 扫描 `static/images/` 下所有 SVG 文件
2. 检查是否已有同名 PNG（跳过未修改的）
3. 使用 `rsvg-convert -w 900` 转换为 PNG
4. 报告转换结果

## 转换命令

对每个 SVG 文件执行：

```bash
rsvg-convert -w 900 <input.svg> -o <output.png>
```

- 输出宽度固定 900px（微信文章最大宽度）
- PNG 与 SVG 同目录同名：`hero.svg` → `hero.png`

## 使用场景

### 场景 1：新增文章配图后

```
用户创建了 static/images/my-post/hero.svg
→ 运行 /svg2png
→ 生成 static/images/my-post/hero.png
→ 提交时带上 .svg 和 .png
```

### 场景 2：修改了已有 SVG

```
用户修改了 static/images/my-post/hero.svg
→ 运行 /svg2png
→ 检测到 SVG 比 PNG 新，重新转换
→ 提交更新后的 .png
```

### 场景 3：提交前批量检查

```
用户说"准备提交"或"检查图片"
→ 自动扫描所有缺少 PNG 的 SVG
→ 批量转换
→ 报告结果
```

## 执行步骤（Claude 需要做的）

1. 检查 `rsvg-convert` 是否安装，未安装则提示 `brew install librsvg`
2. 用 `find static/images -name "*.svg"` 扫描所有 SVG
3. 对每个 SVG：
   - 检查同目录下是否有同名 `.png`
   - 如果 PNG 不存在，或 SVG 比 PNG 更新（`-newer`），则转换
   - 否则跳过
4. 使用 `rsvg-convert -w 900 input.svg -o output.png` 转换
5. 输出转换汇总：已转换 N 个，跳过 M 个
6. 提示用户将 PNG 文件加入 git 提交

## 注意事项

- PNG 文件需要提交到 Git（不在 .gitignore 中）
- `publish.py` 会优先使用已有的 PNG 文件，跳过 cairosvg 转换
- SVG 仍然是博客站点的首选格式（体积小、矢量清晰），PNG 仅用于微信发布
