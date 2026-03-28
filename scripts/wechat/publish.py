#!/usr/bin/env python3
"""Hugo 博客文章自动发布到微信公众号草稿箱

流程：检测变更文章 → Markdown 转微信 HTML → 上传图片 → 创建草稿
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import frontmatter
import markdown
import requests
from bs4 import BeautifulSoup
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

from wechat_style import STYLES, FOOTER_HTML

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── 微信 API ───────────────────────────────────────────────

# 默认走服务器代理，本地调试可通过环境变量切回直连
WECHAT_API = os.environ.get(
    "WECHAT_PROXY_URL",
    "http://182.92.95.178/wechat-api",
)
STATE_FILE = "wechat_published.json"

# 代理验证 Header（直连微信时不需要）
_proxy_key = os.environ.get("WECHAT_PROXY_KEY", "")
PROXY_HEADERS = {"X-Proxy-Key": _proxy_key} if _proxy_key else {}


def _api_get(url: str, **kwargs) -> requests.Response:
    """带代理 Header 的 GET 请求"""
    headers = {**PROXY_HEADERS, **kwargs.pop("headers", {})}
    return requests.get(url, headers=headers, **kwargs)


def _api_post(url: str, **kwargs) -> requests.Response:
    """带代理 Header 的 POST 请求"""
    headers = {**PROXY_HEADERS, **kwargs.pop("headers", {})}
    return requests.post(url, headers=headers, **kwargs)


def get_access_token(app_id: str, app_secret: str) -> str:
    """获取微信 access_token，最多重试 3 次"""
    url = f"{WECHAT_API}/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret,
    }
    for attempt in range(1, 4):
        resp = _api_get(url, params=params, timeout=10)
        data = resp.json()
        if "access_token" in data:
            log.info("获取 access_token 成功")
            return data["access_token"]
        log.warning("第 %d 次获取 token 失败: %s", attempt, data)
        time.sleep(2)
    raise RuntimeError(f"获取 access_token 失败: {data}")


def upload_image(token: str, img_path: str) -> dict:
    """上传永久图片素材，返回 {media_id, url}"""
    url = f"{WECHAT_API}/material/add_material"
    params = {"access_token": token, "type": "image"}
    with open(img_path, "rb") as f:
        files = {"media": (Path(img_path).name, f, "image/png")}
        resp = _api_post(url, params=params, files=files, timeout=30)
    data = resp.json()
    if "media_id" not in data:
        raise RuntimeError(f"上传图片失败 [{img_path}]: {data}")
    log.info("上传图片成功: %s → %s", Path(img_path).name, data["url"])
    return {"media_id": data["media_id"], "url": data["url"]}


def create_draft(token: str, article: dict) -> str:
    """创建草稿，返回 media_id"""
    url = f"{WECHAT_API}/draft/add"
    params = {"access_token": token}
    payload = {"articles": [article]}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = _api_post(
        url, params=params, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = resp.json()
    if "media_id" not in data:
        raise RuntimeError(f"创建草稿失败: {data}")
    log.info("草稿创建成功，media_id: %s", data["media_id"])
    return data["media_id"]


def update_draft(token: str, media_id: str, article: dict):
    """更新已有草稿（覆盖第一篇文章）"""
    url = f"{WECHAT_API}/draft/update"
    params = {"access_token": token}
    payload = {"media_id": media_id, "index": 0, "articles": article}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = _api_post(
        url, params=params, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        raise RuntimeError(f"更新草稿失败: {data}")
    log.info("草稿更新成功，media_id: %s", media_id)


def delete_draft(token: str, media_id: str):
    """删除草稿"""
    url = f"{WECHAT_API}/draft/delete"
    params = {"access_token": token}
    body = json.dumps({"media_id": media_id}, ensure_ascii=False).encode("utf-8")
    resp = _api_post(
        url, params=params, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        log.warning("删除草稿失败: %s", data)
    else:
        log.info("已删除旧草稿: %s", media_id)


def freepublish(token: str, media_id: str) -> str | None:
    """发布草稿（自由发布），返回 publish_id"""
    url = f"{WECHAT_API}/freepublish/submit"
    params = {"access_token": token}
    body = json.dumps({"media_id": media_id}, ensure_ascii=False).encode("utf-8")
    resp = _api_post(
        url, params=params, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        log.warning("自由发布失败: %s", data)
        return None
    publish_id = data.get("publish_id")
    log.info("自由发布成功，publish_id: %s", publish_id)
    return publish_id


def declare_original(token: str, media_id: str):
    """声明原创（通过 freepublish/markasoriginal）"""
    url = f"{WECHAT_API}/freepublish/markasoriginal"
    params = {"access_token": token}
    body = json.dumps({
        "media_id": media_id,
        "index": 0,
    }, ensure_ascii=False).encode("utf-8")
    resp = _api_post(
        url, params=params, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        log.warning("原创声明失败（个人订阅号可能无权限）: %s", data)
    else:
        log.info("原创声明成功")


# ─── 文章检测 ───────────────────────────────────────────────


def get_changed_posts(project_root: str, base_ref: str) -> list[str]:
    """通过 git diff 获取变更的文章文件列表"""
    posts_dir = os.path.join(project_root, "content", "posts")
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, "HEAD", "--", "content/posts/"],
            capture_output=True,
            text=True,
            cwd=project_root,
            check=True,
        )
        files = [
            os.path.join(project_root, f.strip())
            for f in result.stdout.strip().split("\n")
            if f.strip().endswith(".md") and not f.strip().endswith(".wechat.md")
        ]
        return [f for f in files if os.path.exists(f)]
    except subprocess.CalledProcessError:
        log.warning("git diff 失败，回退到扫描全部文章")
        return [str(p) for p in Path(posts_dir).glob("*.md") if not str(p).endswith(".wechat.md")]


def get_all_posts(project_root: str) -> list[str]:
    """获取所有文章文件（排除 .wechat.md 适配版）"""
    posts_dir = os.path.join(project_root, "content", "posts")
    return [str(p) for p in Path(posts_dir).glob("*.md") if not str(p).endswith(".wechat.md")]


def load_state(project_root: str) -> dict:
    """读取发布状态"""
    state_path = os.path.join(project_root, "scripts", "wechat", STATE_FILE)
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(project_root: str, state: dict):
    """写入发布状态"""
    state_path = os.path.join(project_root, "scripts", "wechat", STATE_FILE)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    log.info("发布状态已保存: %s", state_path)


def get_slug(filepath: str) -> str:
    """从文件路径提取 slug"""
    return Path(filepath).stem


# ─── Markdown → 微信 HTML ───────────────────────────────────


def md_to_wechat_html(md_content: str) -> str:
    """将 Markdown 转为微信兼容的 inline-style HTML"""
    # Markdown → HTML（代码高亮直接输出 inline style）
    extensions = [
        TableExtension(),
        FencedCodeExtension(),
        CodeHiliteExtension(
            noclasses=True,
            pygments_style="monokai",
            guess_lang=False,
        ),
        "nl2br",
    ]
    html = markdown.markdown(md_content, extensions=extensions)

    # BeautifulSoup 后处理：注入 inline CSS
    soup = BeautifulSoup(html, "html.parser")

    # 注入标签样式
    for tag_name, style in STYLES.items():
        if tag_name == "code_inline":
            continue  # 单独处理
        for tag in soup.find_all(tag_name):
            existing = tag.get("style", "")
            if existing:
                tag["style"] = f"{existing} {style}"
            else:
                tag["style"] = style

    # 处理 inline code（不在 <pre> 内的 <code>）
    for code in soup.find_all("code"):
        parent = code.parent
        if parent and parent.name == "pre":
            continue  # 代码块内的 code 跳过
        code["style"] = STYLES["code_inline"]

    # 移除所有 class 属性（微信会过滤）
    for tag in soup.find_all(True):
        if tag.get("class"):
            del tag["class"]

    # 处理外链：微信不支持外链，转为文本 + 脚注
    footnotes = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href", "")
        if href and href.startswith("http"):
            footnotes.append(href)
            idx = len(footnotes)
            sup = soup.new_tag("sup")
            sup.string = f"[{idx}]"
            sup["style"] = "color: #999; font-size: 12px;"
            a_tag.replace_with(a_tag.get_text(), sup)

    # 添加脚注列表
    if footnotes:
        fn_section = soup.new_tag("section")
        fn_section["style"] = (
            "margin-top: 24px; padding-top: 12px; "
            "border-top: 1px solid #eee; font-size: 12px; color: #999;"
        )
        fn_title = soup.new_tag("p")
        fn_title["style"] = "font-weight: bold; margin-bottom: 4px;"
        fn_title.string = "参考链接"
        fn_section.append(fn_title)
        for i, link in enumerate(footnotes, 1):
            fn_item = soup.new_tag("p")
            fn_item["style"] = (
                "margin: 2px 0; word-break: break-all; line-height: 1.4;"
            )
            fn_item.string = f"[{i}] {link}"
            fn_section.append(fn_item)
        soup.append(fn_section)

    return str(soup)


# ─── 图片处理 ───────────────────────────────────────────────


def extract_images(md_content: str) -> list[str]:
    """提取 Markdown 中的图片引用路径"""
    pattern = r"!\[.*?\]\((/images/[^\)]+)\)"
    return re.findall(pattern, md_content)


def convert_svg_to_png(svg_path: str, output_dir: str) -> str:
    """SVG → PNG 转换（替换字体为 Noto Sans CJK SC 确保中文渲染）"""
    import cairosvg

    # 读取 SVG 并替换 macOS 专属字体为 Linux 可用的中文字体
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
    svg_content = re.sub(
        r'font-family\s*[:=]\s*["\']?[^"\'>;]*(?:system-ui|-apple-system|BlinkMacSystemFont|PingFang|Microsoft YaHei|Helvetica Neue)[^"\'>;]*["\']?',
        'font-family="Noto Sans CJK SC, Noto Sans SC, sans-serif"',
        svg_content,
    )

    png_name = Path(svg_path).stem + ".png"
    png_path = os.path.join(output_dir, png_name)
    cairosvg.svg2png(
        bytestring=svg_content.encode("utf-8"),
        write_to=png_path,
        output_width=900,
        dpi=144,
    )
    log.info("SVG 转 PNG: %s → %s", Path(svg_path).name, png_name)
    return png_path


def process_images(
    md_content: str,
    project_root: str,
    token: str | None,
    dry_run: bool = False,
) -> tuple[str, str | None]:
    """处理文章中的所有图片，返回 (替换后的HTML内容, 封面图media_id)

    在 dry_run 模式下跳过上传，保留原始路径。
    """
    image_paths = extract_images(md_content)
    if not image_paths:
        return md_content, None

    cover_media_id = None
    url_mapping = {}  # 原始路径 → 微信 URL

    with tempfile.TemporaryDirectory() as tmp_dir:
        for img_path in image_paths:
            local_path = os.path.join(project_root, "static", img_path.lstrip("/"))
            if not os.path.exists(local_path):
                log.warning("图片不存在: %s", local_path)
                continue

            # SVG 需要转 PNG
            if local_path.endswith(".svg"):
                # 优先使用本地预渲染的 PNG（由 /svg2png 技能生成）
                prerendered = local_path.replace(".svg", ".png")
                if os.path.exists(prerendered):
                    upload_path = prerendered
                    log.info("使用预渲染 PNG: %s", Path(prerendered).name)
                else:
                    try:
                        upload_path = convert_svg_to_png(local_path, tmp_dir)
                    except Exception as e:
                        log.warning("SVG 转换失败 [%s]: %s", local_path, e)
                        continue
            else:
                upload_path = local_path

            if dry_run:
                log.info("[dry-run] 跳过上传: %s", Path(upload_path).name)
                continue

            # 上传到微信
            try:
                result = upload_image(token, upload_path)
                url_mapping[img_path] = result["url"]
                if cover_media_id is None:
                    cover_media_id = result["media_id"]
            except RuntimeError as e:
                log.warning("图片上传失败: %s", e)

    # 替换图片 URL
    for original, wechat_url in url_mapping.items():
        md_content = md_content.replace(original, wechat_url)

    return md_content, cover_media_id


# 缓存默认封面 media_id，避免重复上传
_placeholder_media_id: str | None = None


def _get_placeholder_cover(project_root: str, token: str) -> str | None:
    """生成并上传一张默认封面图（900x383 品牌色），缓存 media_id"""
    global _placeholder_media_id
    if _placeholder_media_id:
        return _placeholder_media_id
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        # 无 Pillow 时用纯 PNG 生成（1x1 像素）
        log.warning("Pillow 未安装，使用最小占位图")
        import struct
        import zlib

        # 生成 900x383 纯色 PNG
        width, height = 900, 383
        raw = b""
        for _ in range(height):
            raw += b"\x00" + b"\x22\xc5\x5e" * width  # 品牌绿
        png_data = b"\x89PNG\r\n\x1a\n"
        # IHDR
        ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        png_data += _png_chunk(b"IHDR", ihdr)
        # IDAT
        compressed = zlib.compress(raw)
        png_data += _png_chunk(b"IDAT", compressed)
        # IEND
        png_data += _png_chunk(b"IEND", b"")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png_data)
            tmp_path = f.name
        try:
            result = upload_image(token, tmp_path)
            _placeholder_media_id = result["media_id"]
            return _placeholder_media_id
        finally:
            os.unlink(tmp_path)

    # 使用 Pillow 生成封面
    img = Image.new("RGB", (900, 383), color=(34, 197, 94))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img.save(f, "PNG")
        tmp_path = f.name
    try:
        result = upload_image(token, tmp_path)
        _placeholder_media_id = result["media_id"]
        return _placeholder_media_id
    finally:
        os.unlink(tmp_path)


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """构建 PNG chunk"""
    import struct
    import zlib

    chunk = chunk_type + data
    return struct.pack(">I", len(data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)


# ─── 主流程 ─────────────────────────────────────────────────


def _resolve_wechat_path(filepath: str) -> str:
    """优先使用 .wechat.md 微信适配版，不存在则回退到原文"""
    wechat_path = filepath.replace(".md", ".wechat.md")
    if os.path.exists(wechat_path):
        return wechat_path
    return filepath


def publish_post(
    filepath: str,
    project_root: str,
    token: str | None,
    state: dict,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    """发布单篇文章到微信草稿箱，返回是否成功

    force=True 时即使已发布也会删除旧草稿并重新创建（用于文章内容更新）。
    """
    slug = get_slug(filepath)
    log.info("─── 处理文章: %s ───", slug)

    # 优先使用微信适配版 .wechat.md
    actual_path = _resolve_wechat_path(filepath)
    if actual_path != filepath:
        log.info("使用微信适配版: %s", os.path.basename(actual_path))

    # 解析 front matter
    post = frontmatter.load(actual_path)
    if post.get("draft", False):
        log.info("跳过草稿: %s", slug)
        return False
    if slug in state and not force:
        log.info("跳过已发布: %s（使用 --force 强制更新）", slug)
        return False

    title = post.get("title", slug)
    # 微信个人订阅号标题限制严格（实测约 10 个中文字符安全）
    if len(title) > 10:
        title = title[:9] + "…"
        log.info("标题截断为: %s (%d字符)", title, len(title))
    description = post.get("description", "")
    body = post.content

    # Markdown → 微信 HTML
    body_for_html, cover_media_id = process_images(
        body, project_root, token, dry_run
    )
    wechat_html = md_to_wechat_html(body_for_html)
    wechat_html += FOOTER_HTML

    if dry_run:
        # 输出预览到临时文件
        preview_path = os.path.join(
            project_root, "scripts", "wechat", f"preview_{slug}.html"
        )
        preview_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>body {{ max-width: 677px; margin: 40px auto; padding: 0 16px; font-family: -apple-system, sans-serif; }}</style>
</head><body>{wechat_html}</body></html>"""
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(preview_html)
        log.info("[dry-run] 预览已生成: %s", preview_path)
        return True

    # 创建草稿
    original_url = f"https://blog.es007.com/posts/{slug}/"
    article = {
        "title": title,
        "author": "E.S",
        "digest": description[:30] if description else "",
        "content": wechat_html,
        "content_source_url": original_url,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }
    # 封面图：微信要求必须有 thumb_media_id
    if not cover_media_id and not dry_run:
        # 无图片文章：生成一张纯色占位封面
        placeholder = _get_placeholder_cover(project_root, token)
        if placeholder:
            cover_media_id = placeholder
    if cover_media_id:
        article["thumb_media_id"] = cover_media_id

    # 已有草稿则先删除旧的（微信 draft/update 不支持更新封面图）
    if slug in state and "media_id" in state[slug]:
        old_media_id = state[slug]["media_id"]
        log.info("检测到已有草稿，删除旧版: %s", old_media_id)
        delete_draft(token, old_media_id)

    media_id = create_draft(token, article)

    # 尝试声明原创（个人订阅号可能无权限，失败不影响流程）
    declare_original(token, media_id)

    # 更新状态
    tags = post.get("tags", [])
    state[slug] = {
        "media_id": media_id,
        "title": title,
        "tags": tags,
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }
    log.info("文章 [%s] 草稿创建成功 ✓", title)
    return True


def main():
    parser = argparse.ArgumentParser(description="发布 Hugo 文章到微信公众号草稿箱")
    parser.add_argument(
        "--base-ref", default="HEAD~1", help="git diff 基准 ref（默认 HEAD~1）"
    )
    parser.add_argument("--all", action="store_true", help="扫描全部文章（忽略 git diff）")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument(
        "--dry-run", action="store_true", help="试运行：仅转换 HTML，不调用微信 API"
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    log.info("项目根目录: %s", project_root)

    # 获取待处理文章列表
    if args.all:
        post_files = get_all_posts(project_root)
        log.info("全量扫描模式，共 %d 篇文章", len(post_files))
    else:
        post_files = get_changed_posts(project_root, args.base_ref)
        log.info("增量模式，检测到 %d 篇变更文章", len(post_files))

    if not post_files:
        log.info("没有需要处理的文章，退出")
        return

    # 加载状态
    state = load_state(project_root)

    # 获取 access_token（dry-run 时跳过）
    token = None
    if not args.dry_run:
        app_id = os.environ.get("WECHAT_APP_ID")
        app_secret = os.environ.get("WECHAT_APP_SECRET")
        if not app_id or not app_secret:
            log.error("缺少环境变量 WECHAT_APP_ID 或 WECHAT_APP_SECRET")
            sys.exit(1)
        token = get_access_token(app_id, app_secret)

    # 逐篇发布（增量模式下强制更新变更文章，全量模式跳过已发布）
    is_incremental = not args.all
    success_count = 0
    for filepath in post_files:
        try:
            if publish_post(
                filepath, project_root, token, state,
                args.dry_run, force=is_incremental,
            ):
                success_count += 1
        except Exception as e:
            log.error("文章处理失败 [%s]: %s", filepath, e)

    # 保存状态
    if not args.dry_run and success_count > 0:
        save_state(project_root, state)

    log.info("完成：%d/%d 篇文章处理成功", success_count, len(post_files))


if __name__ == "__main__":
    main()
