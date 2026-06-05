# 📡 论文抓取指南

> **决策：专注 arXiv 自动化，放弃小红书/知乎抓取**（2026-06-05）
>
> 原因：小红书/知乎反爬严、内容质量参差、arXiv 已是论文一手来源。**等用户主动复制内容**再人工录入。

## 🎯 主要数据源

### 1. arXiv search（首选 ✅，自动化主路径）

- **URL 模板**: `https://arxiv.org/search/?query={KEYWORD}&searchtype=all&order=-announced_date_first&start=0`
- **优势**:
  - HTML 干净，可直接用 regex 解析
  - 按 announced_date_first 倒序 = 最新
  - 不限流（实测：单 IP 每分钟 30-50 次 OK）
- **限制**:
  - abstract 在 search 结果中**截断**（~300 字符）
  - 拿完整 abstract 需要去 `/abs/{ID}` 单独再拉
- **自动脚本**: [`scripts/auto_update.py`](scripts/auto_update.py)
  ```bash
  # 默认 HTML search（限流宽松）
  python3 scripts/auto_update.py --query "on-policy distillation" --max 100
  
  # 备用 API 模式（限流严，但 abstract 完整）
  python3 scripts/auto_update.py --api --max 30
  ```

### 2. arXiv 官方 API（备用 ⚠️，限流严）

- **URL**: `https://export.arxiv.org/api/query?search_query=all:...&sortBy=submittedDate&sortOrder=descending`
- **包**: `arxiv`（[lukasschwab/arxiv.py](https://github.com/lukasschwab/arxiv.py)）
- **问题**: **HTTP 429 限流很严** —— 连续 3-5 次请求就触发；触发后 5-30 分钟内该 IP 被锁
- **解决**:
  - 默认用 HTML search 避开
  - 用 API 时 `delay_seconds=10`, `num_retries=5`
  - 失败回退到 HTML search
- **安装**: `pip install arxiv`

### 3. arXiv /abs/ 详情页

- **URL**: `https://arxiv.org/abs/{ID}`
- **用法**: 拿完整 abstract、authors、subjects、comments
- **限流**: 较严（连续 100 次会触发 IP 限流 1-2 小时）。间隔 1-3 秒

### 4. papers.cool（中文辅助 ✅，仅浏览）

- **单篇 URL**: `https://papers.cool/arxiv/{ID}` —— 自带中文 Kimi 解释
- **优势**:
  - 自动生成中文 AI 解释（Kimi 摘要），对中文用户友好
  - 按 venue（会议/期刊）浏览
- **限制**:
  - **搜索是客户端的**（tantivy 索引，JavaScript 调用）—— 没有可抓 URL
  - `/search?q=...` 路径 404
  - `/arxiv?q=...` 不带分类也 404
- **用法**:
  - 拿到 arXiv ID 后，**人工浏览** papers.cool 看 Kimi 中文解释
  - 自动化时不做 papers.cool 抓取（用 arXiv abstract 自己生成中文）

---

## 🤖 自动化方案（GitHub Actions）

参考知乎 Realcat 的方案，**用 GitHub Actions 每天自动跑**：

### 配置文件: [`.github/workflows/daily-update.yml`](.github/workflows/daily-update.yml)

```yaml
on:
  workflow_dispatch:        # 手动触发
  schedule:
    - cron: "0 12 * * *"   # 每天 UTC 12:00（北京时间 20:00）触发
```

### 工作流

```
每天 UTC 12:00
  └─ checkout 仓库
  └─ install python 3.11 + arxiv
  └─ python scripts/auto_update.py --max 100
  └─ 写到 daily-updates/auto-latest.md
  └─ 追加到 daily-updates/{date}.md
  └─ git commit + push
```

### 用户操作（一次性）

1. ✅ 我已配置好 workflow 文件
2. ⚠️ 用户需要在 GitHub 仓库 Settings → Actions → General 启用 "Read and write permissions"
3. ⚠️ 第一次跑可以手动触发（Actions tab → Daily arXiv OPD/OPSD Update → Run workflow）

---

## ❌ 已放弃的方案

### 知乎 zhuanlan.zhihu.com（不可直抓）

- **反爬**:
  - 前端 JS 加密（`zse-ck` 脚本，2025 年新版本）—— 修改 UA 没用
  - 整个 zhihu.com / zhuanlan.zhihu.com 都 403
- **应对**:
  - 用 Google 搜索 `site:zhuanlan.zhihu.com p/{ID}` 看 snippet
  - 用 archive.org Wayback Machine（**国内连不上**）
- **决策**:
  - ❌ 不做自动化抓取
  - ✅ 用户手动浏览 + 复制关键内容到对话里

### 小红书 xiaohongshu.com（不可直抓）

- **反爬**:
  - 必须登录，否则只返 SPA 框架
  - 关键字搜索需要登录态
- **应对**:
  - 需要 xbrowser 登录态（需要用户提供登录会话）
  - 或用户手动复制内容
- **决策**:
  - ❌ 不做自动化抓取
  - ❌ 不要求用户提供登录态
  - ✅ 用户手动浏览 + 复制关键内容到对话里

### 微信公众号 mp.weixin.qq.com

- 必须登录公众号 + 微信内打开
- **决策**: 不抓，等用户手动分享

---

## 🔧 工具栈总结

| 工具 | 用途 | 状态 |
|------|------|------|
| [`scripts/auto_update.py`](scripts/auto_update.py) | arXiv 自动拉取 + 关键词过滤 + Markdown 输出 | ✅ **主力** |
| [`arxiv`](https://github.com/lukasschwab/arxiv.py) | arXiv 官方 API 的 Python 封装 | ✅ 备用 |
| `.github/workflows/daily-update.yml` | 每日自动跑 | ✅ **主力** |
| `web_fetch` (OpenClaw built-in) | 手动补抓 | 备用 |
| `papers.cool/arxiv/{ID}` | Kimi 中文解释（人工浏览） | 辅助 |
| xbrowser | ~~小红书/知乎登录态~~ | ❌ 已弃用 |

---

## 📋 每日更新流程

### 自动部分（GitHub Actions）

1. 每天 UTC 12:00 触发
2. 拉 arXiv 30-100 篇
3. 关键词过滤
4. 写 daily-updates/auto-latest.md
5. 追加到 daily-updates/{date}.md
6. 自动 commit + push

### 人工部分（每 1-3 天）

1. 浏览 GitHub Actions 日志
2. 打开 daily-updates/auto-latest.md
3. 对**强相关**论文，调用 AI（OpenClaw）写**中文详细解读**（动机+方法）
4. 追加到对应 `papers/*.md` 文件
5. 在 `daily-updates/{date}.md` 标记 "✅ 已收录"

---

## 🚧 已知限制

| 限制 | 影响 | 解决方向 |
|------|------|---------|
| arXiv API 限流 | 完整 abstract 拉取慢 | 用 HTML search + 间隔 sleep |
| abstract 截断 | 自动化产出 300 字符 abstract | 用户可手动补抓 `/abs/{ID}` |
| GitHub Actions IP 被封 | 偶尔拉取失败 | 等待 5-30 分钟重试 |
| 国内访问 arXiv 偶尔慢 | 超时失败 | retry + fallback HTML search |
| 小红书/知乎 | 无自动化 | 等用户主动录入 |
| 论文质量参差 | 自动匹配可能含弱相关 | 关键词过滤 + 人工 review |

---

## 📚 参考资料

- arXiv search syntax: https://info.arxiv.org/help/find.html
- arxiv.py: https://github.com/lukasschwab/arxiv.py
- arXiv API 文档: https://info.arxiv.org/help/api/user-manual.html
- GitHub Actions cron: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
- 知乎 Realcat 文章: https://zhuanlan.zhihu.com/p/425670267 （**仅参考，不抓**）
- papers.cool: https://papers.cool/ （**仅人工浏览**）
