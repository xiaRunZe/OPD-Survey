#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_update.py — 自动拉取 arXiv 上与 OPD/OPSD 相关的最新论文。

改用 arxiv.py 库（参考知乎 Realcat 方案），更稳定 + 拿全 abstract。

用法:
    python3 scripts/auto_update.py [--days N] [--keywords ...] [--out OUT]

工作流:
    1. 用 arxiv.Search 拉最新论文（按 submittedDate 倒序）
    2. 关键词过滤（标题 + abstract 至少命中 1 个关键词）
    3. 启发式分类（基于 abstract 关键词）
    4. 输出 Markdown 表格 + 详细 abstract 列表
    5. （可选）追加到 daily-updates/{date}.md

参考:
    - arxiv.py: https://github.com/lukasschwab/arxiv.py
    - Realcat 知乎文章（arXiv API + GitHub Actions 方案）
"""
import argparse
import os
import re
import sys
import time
import urllib.error
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import arxiv
except ImportError:
    print("ERROR: arxiv not installed. Run: pip install arxiv", file=sys.stderr)
    sys.exit(1)

import urllib.parse
import urllib.request

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ARXIV_SEARCH_URL = "https://arxiv.org/search/?query={q}&searchtype=all&start={start}&order=-announced_date_first"


# 默认关键词（强 → 弱匹配）
DEFAULT_KEYWORDS = [
    "on-policy distillation", "OPSD", "on-policy self-distillation",
    "self-distilled policy", "self-teaching", "self-distilled reasoner",
    "policy distillation", "DAgger", "self-distillation",
    "self-rewarding", "on-policy imitation", "token-level distillation",
    "policy optimization self-distill", "self-distill policy gradient",
    "RL with self-distill", "distill from teacher", "self-distill",
    "policy self-distill", "policy gradient self-distill",
]

# 分类启发式：标题/abstract 命中越多 → 越倾向该类
CATEGORY_HINTS = {
    "白盒 OPD / 隐藏层空间": ["hidden state", "representation distill", "logit distill", "feature distill"],
    "白盒 OPD / 细粒度": ["filter", "reweight", "token-level", "trajectory-level", "localized", "entropy"],
    "白盒 OPD / 安全性": ["safety", "align", "constitutional", "harmful", "jailbreak"],
    "白盒 OPD / 混合": ["hybrid policy", "FKL", "RKL", "forward cross", "reverse KL"],
    "OPSD / 调度": ["temporal", "refresh", "consolidation", "teacher schedule", "teacher update"],
    "OPSD / 理论": ["monotonic", "regret", "forward cross-entropy", "divergence"],
    "OPSD + RL 混合": ["policy gradient", "GRPO", "RL with self-distill", "verifier"],
    "OPSD / 持续学习": ["continual", "memory", "sleep", "self-modify"],
    "多模态 OPD": ["multimodal", "visual", "vision-language", "VLM", "image"],
    "多模态 OPSD": ["symbolic state", "modality-gap", "visual planning", "visual cue"],
    "多语言": ["cross-lingual", "multilingual", "low-resource", "verbalizer", "African"],
    "Agent 应用": ["agent", "tool", "web search", "GUI", "VLA", "robot"],
    "扩散模型 / 视觉": ["diffusion", "image generation", "denoising"],
}

# 中文分类标签（用于 daily-update）
CATEGORY_TAG_CN = {
    "白盒 OPD / 隐藏层空间": "🔬 白盒OPD",
    "白盒 OPD / 细粒度": "🔬 白盒OPD",
    "白盒 OPD / 安全性": "🔬 白盒OPD",
    "白盒 OPD / 混合": "🔬 白盒OPD",
    "OPSD / 调度": "♻️ OPSD",
    "OPSD / 理论": "♻️ OPSD",
    "OPSD + RL 混合": "♻️ OPSD+RL",
    "OPSD / 持续学习": "♻️ OPSD",
    "多模态 OPD": "🖼️ 多模态",
    "多模态 OPSD": "🖼️ 多模态",
    "多语言": "🌐 多语言",
    "Agent 应用": "🤖 Agent",
    "扩散模型 / 视觉": "🖼️ 多模态",
    "其他 / 待人工分类": "📌 其他",
}


@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    authors: list[str] = field(default_factory=list)
    primary_category: str = ""
    published: str = ""
    url: str = ""
    category: str = ""
    matched_keyword: str = ""


def normalize_id(arxiv_id: str) -> str:
    """Strip version suffix: 2606.06021v2 -> 2606.06021"""
    return re.sub(r"v\d+$", "", arxiv_id)


def match_keywords(p: Paper, keywords: list[str]) -> str:
    """Return first matching keyword (case-insensitive), or empty string."""
    text = (p.title + " " + p.abstract).lower()
    for kw in keywords:
        if kw.lower() in text:
            return kw
    return ""


def classify(p: Paper) -> str:
    """Heuristic category assignment based on title + abstract keywords."""
    text = (p.title + " " + p.abstract).lower()
    scores: dict[str, int] = {}
    for cat, kws in CATEGORY_HINTS.items():
        scores[cat] = sum(1 for kw in kws if kw.lower() in text)
    if not scores or max(scores.values()) == 0:
        return "其他 / 待人工分类"
    return max(scores, key=scores.get)


def search_arxiv(query: str, max_results: int = 100, use_api: bool = False) -> list[Paper]:
    """
    Pull up to max_results papers from arXiv.

    - use_api=True: 用 arxiv.py 库（更稳定，但限流严，~3 req/min）
    - use_api=False (默认): 用 HTML search（限流宽松，但 abstract 截断）

    两者都失败时抛 RuntimeError。
    """
    if use_api:
        return _search_arxiv_api(query, max_results)
    return _search_arxiv_html(query, max_results)


def _search_arxiv_api(query: str, max_results: int) -> list[Paper]:
    """Use arxiv.py library."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    client = arxiv.Client(page_size=min(50, max_results), delay_seconds=10.0, num_retries=5)
    papers: list[Paper] = []
    for r in client.results(search):
        arxiv_id = normalize_id(r.entry_id.rsplit("/", 1)[-1])
        papers.append(Paper(
            arxiv_id=arxiv_id,
            title=r.title.strip().replace("\n", " "),
            abstract=r.summary.strip().replace("\n", " "),
            authors=[a.name for a in r.authors],
            primary_category=r.primary_category,
            published=r.published.strftime("%Y-%m-%d") if r.published else "",
            url=r.entry_id,
        ))
    return papers


def _fetch_html(url: str, retries: int = 3, delay: float = 5.0) -> str:
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


def _search_arxiv_html(query: str, max_results: int) -> list[Paper]:
    """Use arXiv HTML search (more forgiving rate limit)."""
    papers: list[Paper] = []
    page_size = 50
    start = 0
    while len(papers) < max_results:
        url = ARXIV_SEARCH_URL.format(q=urllib.parse.quote_plus(query), start=start)
        html = _fetch_html(url)
        page = _parse_html_search(html)
        if not page:
            break
        papers.extend(page)
        if len(page) < page_size:
            break
        start += page_size
        time.sleep(3.0)
    # 去重
    seen = set()
    unique = []
    for p in papers:
        if p.arxiv_id not in seen:
            seen.add(p.arxiv_id)
            unique.append(p)
    return unique[:max_results]


def _parse_html_search(html: str) -> list[Paper]:
    """Parse arXiv HTML search results."""
    papers: list[Paper] = []
    # 每个条目以 arxiv.org/abs/ID 开始
    entries = re.split(r'(?=arxiv\.org/abs/\d{4}\.\d{4,5})', html)
    for entry in entries[1:]:  # 跳过 split 之前的部分
        m_id = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', entry)
        m_title = re.search(r'class="title is-5 mathjax">\s*(.*?)\s*</p>', entry, re.DOTALL)
        m_abs = re.search(r'class="abstract-full[^"]*"[^>]*>(.*?)<', entry, re.DOTALL)
        if not (m_id and m_title):
            continue
        arxiv_id = normalize_id(m_id.group(1))
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m_title.group(1))).strip()
        abstract = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m_abs.group(1) if m_abs else "")).strip() if m_abs else ""
        # abstract 截断处理
        abstract = abstract.split("△ Less")[0].strip()
        # authors
        authors = re.findall(r'class="search-hit[^"]*"[^>]*>([^<]+)</a>', entry)
        papers.append(Paper(
            arxiv_id=arxiv_id,
            title=title,
            abstract=abstract,
            authors=authors[:10],
            published="",
        ))
    return papers


def filter_papers(papers: list[Paper], keywords: list[str]) -> list[Paper]:
    """Filter by keywords + assign category."""
    out = []
    for p in papers:
        kw = match_keywords(p, keywords)
        if not kw:
            continue
        p.matched_keyword = kw
        p.category = classify(p)
        out.append(p)
    return out


def to_markdown(papers: list[Paper], title: str = "📚 arXiv 新论文（自动拉取）") -> str:
    """Format papers as a Markdown report."""
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
        cat_tag = CATEGORY_TAG_CN.get(p.category, p.category)
        lines.append(f"| {i} | [{p.arxiv_id}](https://arxiv.org/abs/{p.arxiv_id}) | {title_short} | {cat_tag} | {p.matched_keyword} |")
    lines.append("\n---\n")
    for p in papers:
        cat_tag = CATEGORY_TAG_CN.get(p.category, p.category)
        lines.append(f"## {p.title}\n")
        lines.append(f"- **arXiv**: [{p.arxiv_id}](https://arxiv.org/abs/{p.arxiv_id})")
        lines.append(f"- **类别**: {cat_tag}（{p.category}）")
        lines.append(f"- **匹配关键词**: {p.matched_keyword}")
        lines.append(f"- **作者**: {', '.join(p.authors[:5])}{'等' if len(p.authors) > 5 else ''}")
        lines.append(f"- **提交日期**: {p.published}")
        lines.append(f"- **主分类**: {p.primary_category}")
        lines.append(f"\n### Abstract\n{p.abstract}\n")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=30, help="只显示（信息性）")
    ap.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS, help="自定义关键词列表")
    ap.add_argument("--max", type=int, default=100, help="最多拉取多少篇")
    ap.add_argument("--query", default="on-policy distillation", help="arXiv 搜索 query")
    ap.add_argument("--out", default="daily-updates/auto-latest.md", help="输出文件")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--api", action="store_true", help="用 arxiv API 而非 HTML search（更稳但限流严）")
    args = ap.parse_args()

    print(f"[1/3] searching arXiv: query={args.query!r}, max={args.max}, mode={'API' if args.api else 'HTML'}")
    papers = search_arxiv(args.query, max_results=args.max, use_api=args.api)
    print(f"      fetched {len(papers)} papers")

    print(f"[2/3] keyword filter: {len(args.keywords)} keywords")
    filtered = filter_papers(papers, args.keywords)
    print(f"      matched {len(filtered)} papers")

    print(f"[3/3] writing markdown: {args.out}")
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(to_markdown(filtered), encoding="utf-8")
    print(f"      done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
