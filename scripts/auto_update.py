#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_update.py — 自动拉取 arXiv 上与 OPD/OPSD 相关的最新论文。

用法:
    python3 scripts/auto_update.py [--days N] [--keywords ...] [--out OUT]

工作流:
    1. 用 arXiv search (HTML) 拉最新论文列表（按 announced_date_first 倒序）
    2. 用 regex 解析 ID + 标题 + abstract
    3. 关键词过滤（标题 + abstract 至少命中 1 个关键词）
    4. 输出去重 Markdown 表格，方便人工 review
    5. （可选）调用本地 LLM 写中文简评（未实现，留 hook）

参考:
    - arXiv search URL: https://arxiv.org/search/?query=...&order=-announced_date_first
    - papers.cool 单篇: https://papers.cool/arxiv/{ID}
    - 单篇 API: https://arxiv.org/abs/{ID}
"""
import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ARXIV_SEARCH = "https://arxiv.org/search/?query={q}&searchtype=all&start={start}&order=-announced_date_first"
ARXIV_ABS = "https://arxiv.org/abs/{id}"

# 默认关键词（强 → 弱）
DEFAULT_KEYWORDS = [
    "on-policy distillation", "OPSD", "self-distillation", "on-policy self-distillation",
    "self-distilled policy", "self-teaching", "privileged context", "self-distilled",
    "policy distillation", "distributional DAgger", "DAgger",
    "reverse KL policy", "self-rewarding", "on-policy imitation", "token-level distillation",
    "policy optimization self-distill", "SDPO",
    "self-distill policy gradient", "RL with self-distill", "distill from teacher",
]

CATEGORY_HINTS = {
    "白盒 OPD / 隐藏层空间": ["hidden state", "representation distill", "logit distill"],
    "白盒 OPD / 轨迹 + token 粒度": ["filter", "reweight", "token-level", "trajectory-level"],
    "白盒 OPD / 安全性": ["safety", "align", "constitutional", "harmful"],
    "OPSD / 调度": ["temporal", "refresh", "consolidation", "teacher schedule"],
    "OPSD / 理论": ["monotonic", "regret", "forward cross-entropy", "forward KL", "forward CE"],
    "OPSD + RL 混合": ["policy gradient", "GRPO", "RL with self-distill"],
    "OPSD / 持续学习": ["continual", "consolidation", "self-modify", "memory", "sleep"],
    "多模态 OPD": ["multimodal", "visual", "vision-language", "VLM"],
    "多模态 OPSD": ["symbolic state", "modality-gap", "visual planning"],
    "多语言": ["cross-lingual", "multilingual", "low-resource", "verbalizer"],
}


@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    authors: list[str] = field(default_factory=list)
    subjects: list[str] = field(default_factory=list)
    published: str = ""
    category: str = ""
    matched_keyword: str = ""


def fetch(url: str, retries: int = 3, delay: float = 5.0) -> str:
    """Fetch URL with retries and exponential backoff."""
    last_err = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:
            last_err = e
            if i < retries - 1:
                time.sleep(delay * (i + 1))
    raise RuntimeError(f"fetch failed: {url} :: {last_err}")


def parse_arxiv_search(html: str) -> list[Paper]:
    """Parse arXiv search HTML; return list of Paper objects."""
    papers: list[Paper] = []
    # 每个条目格式（实测）: arxiv.org/abs/ID...<p class="title is-5 mathjax"> TITLE </p>
    # 用一个不太严格的正则匹配
    pattern = re.compile(
        r'arxiv\.org/abs/(\d{4}\.\d{4,5})[^>]*>.*?'
        r'class="title is-5 mathjax">\s*(.*?)\s*</p>.*?'
        r'class="abstract-full[^"]*"[^>]*>\s*(.*?)\s*</span>.*?'
        r'class="search-hit[^"]*"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    # Fallback: 更宽松
    loose_pat = re.compile(
        r'arxiv\.org/abs/(\d{4}\.\d{4,5})[^\n]*?\n.*?'
        r'class="title is-5 mathjax">\s*(.*?)\s*</p>',
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        arxiv_id, title, abstract, _author_chunk = m.groups()
        # 清理 HTML 标签
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title)).strip()
        abstract = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", abstract)).strip()
        # 截止 abstract 段落（arXiv 有省略号）
        abstract = abstract.split("△ Less")[0].strip()
        papers.append(Paper(arxiv_id=arxiv_id, title=title, abstract=abstract))
    return papers


def fetch_abstract(arxiv_id: str) -> str:
    """Get full abstract from /abs/ page (search results are truncated)."""
    html = fetch(ARXIV_ABS.format(id=arxiv_id))
    m = re.search(r'<blockquote class="abstract[^"]*">\s*Abstract:\s*(.*?)\s*</blockquote>', html, re.DOTALL)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def classify(p: Paper) -> str:
    """Heuristic category assignment based on title + abstract keywords."""
    text = (p.title + " " + p.abstract).lower()
    scores: dict[str, int] = {}
    for cat, kws in CATEGORY_HINTS.items():
        scores[cat] = sum(1 for kw in kws if kw.lower() in text)
    if not scores or max(scores.values()) == 0:
        return "其他 / 待人工分类"
    return max(scores, key=scores.get)


def match_keywords(p: Paper, keywords: list[str]) -> str:
    """Return first matching keyword (case-insensitive), or empty string."""
    text = (p.title + " " + p.abstract).lower()
    for kw in keywords:
        if kw.lower() in text:
            return kw
    return ""


def search_arxiv(query: str, max_results: int = 200) -> list[Paper]:
    """Pull up to max_results papers from arXiv search."""
    all_papers: list[Paper] = []
    start = 0
    page_size = 50  # arXiv search page size
    while len(all_papers) < max_results:
        url = ARXIV_SEARCH.format(q=urllib.parse.quote_plus(query), start=start)
        html = fetch(url)
        page = parse_arxiv_search(html)
        if not page:
            break
        all_papers.extend(page)
        if len(page) < page_size:
            break
        start += page_size
        time.sleep(3.0)  # 避免限流
    # 去重
    seen = set()
    unique = []
    for p in all_papers:
        if p.arxiv_id not in seen:
            seen.add(p.arxiv_id)
            unique.append(p)
    return unique[:max_results]


def filter_papers(papers: list[Paper], keywords: list[str], full_abstract: bool = True) -> list[Paper]:
    """Filter by keywords; optionally enrich with full abstract from /abs/."""
    out = []
    for p in papers:
        kw = match_keywords(p, keywords)
        if not kw:
            continue
        if full_abstract and (not p.abstract or len(p.abstract) < 200):
            try:
                p.abstract = fetch_abstract(p.arxiv_id)
                time.sleep(1.0)
            except Exception:
                pass
        p.matched_keyword = kw
        p.category = classify(p)
        out.append(p)
    return out


def to_markdown(papers: list[Paper], title: str = "📚 arXiv 新论文（自动拉取）") -> str:
    """Format papers as a Markdown table for human review."""
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M GMT+8")
    lines = [f"# {title}\n", f"> 拉取时间：{today}\n", ""]
    if not papers:
        lines.append("_未发现匹配论文。_")
        return "\n".join(lines)
    lines.append(f"**共 {len(papers)} 篇**\n")
    lines.append("| # | arXiv | 标题 | 类别 | 匹配关键词 |")
    lines.append("|---|-------|------|------|-----------|")
    for i, p in enumerate(papers, 1):
        title_short = p.title[:80] + ("…" if len(p.title) > 80 else "")
        lines.append(f"| {i} | [{p.arxiv_id}](https://arxiv.org/abs/{p.arxiv_id}) | {title_short} | {p.category} | {p.matched_keyword} |")
    lines.append("\n---\n")
    for p in papers:
        lines.append(f"## {p.title}\n")
        lines.append(f"- **arXiv**: [{p.arxiv_id}](https://arxiv.org/abs/{p.arxiv_id})")
        lines.append(f"- **类别**: {p.category}")
        lines.append(f"- **匹配关键词**: {p.matched_keyword}")
        lines.append(f"\n### Abstract\n{p.abstract}\n")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=30, help="只看最近 N 天（仅显示，arXiv search 不直接支持）")
    ap.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS, help="自定义关键词")
    ap.add_argument("--max", type=int, default=200, help="最多拉取多少篇")
    ap.add_argument("--no-full-abstract", action="store_true", help="不从 /abs/ 抓全文（快）")
    ap.add_argument("--query", default="on-policy distillation", help="arXiv 搜索 query")
    ap.add_argument("--out", default="daily-updates/auto-latest.md", help="输出文件")
    args = ap.parse_args()

    print(f"[1/3] searching arXiv: query={args.query!r}, max={args.max}")
    papers = search_arxiv(args.query, max_results=args.max)
    print(f"      fetched {len(papers)} papers")

    print(f"[2/3] keyword filter: {len(args.keywords)} keywords")
    filtered = filter_papers(papers, args.keywords, full_abstract=not args.no_full_abstract)
    print(f"      matched {len(filtered)} papers")

    print(f"[3/3] writing markdown: {args.out}")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(to_markdown(filtered), encoding="utf-8")
    print(f"      done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
