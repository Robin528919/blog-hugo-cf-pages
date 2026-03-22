"""微信公众号 inline CSS 样式映射

微信编辑器会过滤 class 属性和 <style> 标签，
所有样式必须以 inline style 形式写入每个标签。
"""

# 标签 → inline CSS 映射
STYLES = {
    "h1": (
        "font-size: 22px; font-weight: bold; color: #1a1a1a; "
        "margin: 28px 0 14px; padding-bottom: 8px; "
        "border-bottom: 1px solid #eee;"
    ),
    "h2": (
        "font-size: 20px; font-weight: bold; color: #1a1a1a; "
        "margin: 24px 0 12px; padding-left: 10px; "
        "border-left: 4px solid #22c55e;"
    ),
    "h3": (
        "font-size: 18px; font-weight: bold; color: #1a1a1a; "
        "margin: 20px 0 10px;"
    ),
    "p": (
        "font-size: 16px; line-height: 1.8; color: #333; "
        "margin: 12px 0;"
    ),
    "blockquote": (
        "border-left: 3px solid #22c55e; padding: 10px 16px; "
        "background: #f8f9fa; color: #666; margin: 16px 0; "
        "font-size: 15px; line-height: 1.7;"
    ),
    "pre": (
        "background: #1e293b; color: #e2e8f0; padding: 16px; "
        "border-radius: 8px; font-size: 13px; line-height: 1.6; "
        "overflow-x: auto; font-family: Menlo, Consolas, monospace; "
        "margin: 16px 0;"
    ),
    "code_inline": (
        "background: #f3f4f6; color: #e74c3c; padding: 2px 6px; "
        "border-radius: 3px; font-size: 14px; "
        "font-family: Menlo, Consolas, monospace;"
    ),
    "table": (
        "width: 100%; border-collapse: collapse; margin: 16px 0; "
        "font-size: 14px;"
    ),
    "th": (
        "background: #f8f9fa; padding: 8px 12px; "
        "border: 1px solid #ddd; text-align: left; font-weight: bold;"
    ),
    "td": "padding: 8px 12px; border: 1px solid #ddd;",
    "img": (
        "max-width: 100%; height: auto; border-radius: 4px; "
        "margin: 12px auto; display: block;"
    ),
    "a": "color: #22c55e; text-decoration: none; font-weight: 500;",
    "ul": "padding-left: 24px; margin: 12px 0;",
    "ol": "padding-left: 24px; margin: 12px 0;",
    "li": (
        "font-size: 16px; line-height: 1.8; color: #333; margin: 4px 0;"
    ),
    "hr": "border: none; border-top: 1px solid #eee; margin: 24px 0;",
    "strong": "font-weight: bold; color: #1a1a1a;",
    "em": "font-style: italic; color: #555;",
}

# 文章尾部模板
FOOTER_HTML = """
<section style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #eee;">
  <p style="font-size: 14px; color: #999; line-height: 1.6;">
    本文首发于 <strong style="color: #22c55e;">E.S 博客</strong>，
    点击「阅读原文」查看完整版本。
  </p>
</section>
"""
