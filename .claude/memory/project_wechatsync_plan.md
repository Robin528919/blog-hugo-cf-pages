---
name: Wechatsync 多平台同步计划
description: Wechatsync 同步微信会丢失图片不可用，仅考虑用于其他平台；微信继续用 publish.py
type: project
---

评估了 https://github.com/wechatsync/Wechatsync 多平台同步工具。

**微信公众号：不可用**
- Wechatsync 同步到微信公众号会丢失图片，效果不合格
- 微信公众号继续使用现有 `scripts/wechat/publish.py` 方案（自动上传图片到微信素材库）

**其他平台：待评估**
- 可考虑用于知乎、掘金、CSDN 等平台的文章同步
- Chrome 应用商店已搜不到，需从 GitHub 源码手动安装浏览器扩展

**Why:** Wechatsync 使用浏览器本地登录态同步，微信对外链图片有严格过滤，导致图片丢失。现有 publish.py 方案先将图片上传为微信素材再引用，能正确保留图片。

**How to apply:** 微信发布需求必须走 publish.py，不要用 Wechatsync。其他平台同步需求可重新评估 Wechatsync。
