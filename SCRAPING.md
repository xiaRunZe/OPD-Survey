# 📡 论文抓取指南

> 总结本调研使用的**抓取入口**和**反爬应对**。后续每日更新都遵循此流程。

## 🎯 主要数据源

### 1. arXiv search（首选 ✅）

- **URL 模板**: `https://arxiv.org/search/?query={KEYWORD}&searchtype=all&order=-announced_date_first&start=0`
- **优势**:
  - HTML 干净，可直接用 regex 解析
  - 按 announced_date_first 倒序，自然就是"最新"
  - 不限流（实测连续拉 50 篇没触发）
- **限制**:
  - 每页 ~50 篇，要翻页用 `&start=50&start=100...`
  - abstract 在 search 结果中是**截断**的，需要去 `/abs/{ID}` 拿完整版
- **自动脚本**: `scripts/auto_update.py`
  ```bash
  python3 scripts/auto_update.py --query "on-policy distillation" --out daily-updates/auto-latest.md
  ```

### 2. papers.cool（辅助 ✅）

- **单篇 URL**: `https://papers.cool/arxiv/{ID}` —— 自带中文 AI 解释（Kimi）
- **首页 URL**: `https://papers.cool/`
- **优势**:
  - 自动生成中文解释（基于 Kimi），对中文用户友好
  - 按 venue（会议/期刊）浏览
- **限制**:
  - **搜索是客户端的**（tantivy 索引，JavaScript 调用）—— 没有可抓 URL
  - 单篇页面可解析，但内容与 arXiv 基本一致
- **用法**:
  - 拿到 arXiv ID 后，**人工浏览** papers.cool 看 Kimi 中文解释
  - 或批量打开：`for id in 2606.06021 2606.05718; do start https://papers.cool/arxiv/$id; done`

### 3. arXiv /abs/ 详情页

- **URL**: `https://arxiv.org/abs/{ID}`
- **用法**:
  - 拿完整 abstract
  - 拿 authors / subjects / comments
  - 看 v1/v2 版本历史
- **限流**: 极严（连续 100 个请求会触发 IP 限流 1-2 小时）。建议 `time.sleep(1.0)` 间隔

### 4. arXiv 官方 API（不推荐 ❌）

- **URL**: `https://export.arxiv.org/api/query?search_query=all:...&sortBy=submittedDate&sortOrder=descending`
- **问题**:
  - rate limit 极严（实测：连续 3 次后就被"Rate exceeded"）
  - 不能精确按"on-policy distillation"这种 phrase 搜（默认是 token 包含）
- **结论**: 用 HTML search 替代 API 反而更稳

---

## 🛡️ 国内受限平台 + 反爬现状

### 5. 知乎（不可直抓 ❌）

- **URL**: `https://www.zhihu.com/...` / `https://zhuanlan.zhihu.com/p/{ID}`
- **反爬**:
  - 前端 JS 加密（`zse-ck` 脚本，2025 年新版本）—— 修改 UA 没用
  - 整个 zhihu.com / zhuanlan.zhihu.com 都 403
- **现状**:
  - 任何 HTTP GET 都拿不到正文
  - 唯一能获取内容的方式：登录后的浏览器自动化
- **应对**:
  - 用 Google 搜索 `site:zhuanlan.zhihu.com p/425670267` 看 snippet（但 Google 中文搜索也限流）
  - 用 archive.org Wayback Machine（**国内连不上** archive.org）
- **建议**:
  - 用户手动浏览知乎文章，把关键内容复制给我
  - 或用浏览器插件（如 Notion Web Clipper）导出 Markdown

### 6. 小红书（不可直抓 ❌）

- **URL**: `https://www.xiaohongshu.com/explore?...`
- **反爬**:
  - 必须登录，否则只返 SPA 框架（HTML 内容为空）
  - 关键字搜索结果需要登录态
- **现状**:
  - 抓到的 HTML 仅有导航元素（"穿搭 / 美食 / 彩妆..."）
  - 没有内容、没有标题、没有作者
- **应对**:
  - **必须**先登录（Cookie + X-Xs-Token）
  - 用 xbrowser（OpenClaw 浏览器自动化 skill）登录后截屏 / 抓 DOM
  - 或手动浏览后复制
- **建议**:
  - 如果你要我做小红书抓取，**先给我一次登录的浏览器会话**（用 xbrowser 启动带登录的 profile）
  - 或你直接复制关键内容到对话里

### 7. 微信公众号（不可抓 ❌）

- 文章 URL `https://mp.weixin.qq.com/s/{ID}` 极严
- 必须登录公众号 + 关注 + 微信内打开
- **建议**: 直接用 wechaty / 微信小程序内的 RSS 订阅

---

## 🔧 抓取工具栈

| 工具 | 用途 | 状态 |
|------|------|------|
| `web_fetch` (OpenClaw built-in) | arXiv search / abs / papers.cool | ✅ 首选 |
| `curl.exe` | 复杂场景（需指定 cookie / header） | ✅ 备用 |
| `scripts/auto_update.py` | arXiv 自动拉取 + 关键词过滤 | ✅ 自建 |
| `xbrowser` (OpenClaw skill) | 登录后的小红书/知乎 | ⚠️ 需用户先登录 |
| 搜索引擎 (Google / Bing / DDG) | 找缓存 / 找替代源 | ❌ 国内基本不可用 |
| `archive.org/wayback` | 历史快照 | ❌ GFW 屏蔽 |

---

## 📋 每日更新流程（推荐）

```bash
# Step 1: 拉取 arXiv 最新
cd C:\Users\小天\.qclaw\workspace-rjtygtk52wdjdqjn\OPD-Survey
python3 scripts/auto_update.py \
    --query "on-policy distillation" \
    --max 100 \
    --out daily-updates/auto-latest.md

# Step 2: 人工 review
# 打开 daily-updates/auto-latest.md
# - 删除明显无关的
# - 把强相关论文的 arXiv ID 记下来

# Step 3: 让 AI 生成中文解读
# 把"待解读论文 ID 列表"贴给 AI（/msg）
# AI 用 web_fetch 抓 abstract，写中文解读
# 写入 daily-updates/{date}.md

# Step 4: 增量更新到 papers/
# AI 把每篇按类别追加到对应 papers/*.md

# Step 5: Git commit + push
git add -A
git commit -m "feat: daily update 2026-06-05 - 12 new papers"
git push
```

---

## 🚧 已知限制 & 后续工作

| 限制 | 影响 | 解决方向 |
|------|------|---------|
| 知乎抓不到 | 看不到中文深度讨论 | 1) 用户复制内容给我；2) 借助 xbrowser 登录态 |
| 小红书抓不到 | 看不到一线算法工程师讨论 | 同上 |
| arXiv API 限流 | 大批量拉取慢 | 用 HTML search + 间隔 sleep |
| Google Scholar 抓不到 | 缺引用图谱 | 用 Semantic Scholar API（需注册 key） |
| 微信公众号 | 完全无法 | 用户手动录入 |

---

## 📚 参考资料

- arXiv search syntax: https://info.arxiv.org/help/find.html
- papers.cool: https://papers.cool/ （基于 kexue.fm + Kimi）
- arXiv API: https://info.arxiv.org/help/api/user-manual.html
- xbrowser (OpenClaw skill): `bundled_skill_dir/xbrowser/SKILL.md`
- 反爬应对: https://github.com/NanmiCoder/MediaCrawler （参考项目）
