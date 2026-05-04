#!/usr/bin/env python3
"""Index and search Kevin's markdown knowledge base.

Creates a SQLite FTS5 index from markdown files with YAML frontmatter, then searches
metadata + full article text. Designed for semantic-ish keyword search without any
API keys: query expansion, BM25 ranking, snippets, and freshness checks.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_KB = Path(os.environ.get("KB_PATH", "/Users/kevin/projects/cog-config/knowledge-base"))
DEFAULT_DB = Path(os.environ.get("KB_INDEX_DB", str(DEFAULT_KB / ".kb-index.sqlite")))

ALIASES = {
    "evals": ["eval", "evals", "evaluation", "evaluations", "evaluate", "benchmark", "benchmarks", "test", "tests", "regression", "grader", "judge", "llm-as-a-judge", "llm judge", "golden dataset", "golden set"],
    "llm": ["llm", "llms", "language model", "language models", "ai model", "ai models", "model"],
    "agents": ["agent", "agents", "agentic", "ai agent", "ai agents", "workflow", "workflows", "tool use", "orchestrator", "subagent", "sub-agent"],
    "claude": ["claude", "claude code", "anthropic"],
    "startup": ["startup", "startups", "founder", "founders", "company", "companies"],
}

STOPWORDS = {"a", "an", "and", "are", "all", "for", "from", "how", "in", "me", "of", "on", "or", "proper", "related", "the", "this", "to", "with", "you", "find", "articles", "article", "knowledge", "base", "kb"}

@dataclass
class Article:
    path: Path
    relpath: str
    title: str
    author: str
    author_slug: str
    source_platform: str
    format: str
    url: str
    original_date: str
    fetched_at: str
    tags: str
    body: str
    mtime: float


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + len("\n---"):].lstrip()
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data, body


def iter_articles(kb: Path) -> Iterable[Article]:
    for path in sorted(kb.rglob("*.md")):
        if path.name.startswith(".") or any(part.startswith(".") for part in path.relative_to(kb).parts):
            continue
        text = path.read_text(errors="replace")
        fm, body = parse_frontmatter(text)
        rel = str(path.relative_to(kb))
        yield Article(
            path=path,
            relpath=rel,
            title=fm.get("title") or path.stem.replace("-", " "),
            author=fm.get("author", ""),
            author_slug=fm.get("author_slug") or path.parent.name,
            source_platform=fm.get("source_platform", ""),
            format=fm.get("format", ""),
            url=fm.get("url", ""),
            original_date=fm.get("original_date", ""),
            fetched_at=fm.get("fetched_at", ""),
            tags=fm.get("tags", ""),
            body=body,
            mtime=path.stat().st_mtime,
        )


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def rebuild(kb: Path, db: Path) -> int:
    conn = connect(db)
    conn.executescript(
        """
        DROP TABLE IF EXISTS articles;
        DROP TABLE IF EXISTS article_fts;
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            relpath TEXT UNIQUE,
            title TEXT,
            author TEXT,
            author_slug TEXT,
            source_platform TEXT,
            format TEXT,
            url TEXT,
            original_date TEXT,
            fetched_at TEXT,
            tags TEXT,
            body TEXT,
            mtime REAL
        );
        CREATE VIRTUAL TABLE article_fts USING fts5(
            title, author, tags, body, relpath,
            content='articles', content_rowid='id',
            tokenize='unicode61 remove_diacritics 2'
        );
        """
    )
    count = 0
    for a in iter_articles(kb):
        cur = conn.execute(
            """INSERT INTO articles(relpath,title,author,author_slug,source_platform,format,url,original_date,fetched_at,tags,body,mtime)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (a.relpath, a.title, a.author, a.author_slug, a.source_platform, a.format, a.url, a.original_date, a.fetched_at, a.tags, a.body, a.mtime),
        )
        rowid = cur.lastrowid
        conn.execute(
            "INSERT INTO article_fts(rowid,title,author,tags,body,relpath) VALUES (?,?,?,?,?,?)",
            (rowid, a.title, a.author, a.tags, a.body, a.relpath),
        )
        count += 1
    conn.commit()
    return count


def index_stale(kb: Path, db: Path) -> bool:
    if not db.exists():
        return True
    db_mtime = db.stat().st_mtime
    return any(p.stat().st_mtime > db_mtime for p in kb.rglob("*.md"))


def expand_query(q: str) -> list[str]:
    terms = re.findall(r"[a-zA-Z0-9][a-zA-Z0-9-]*", q.lower())
    expanded: list[str] = []
    for t in terms:
        if t in STOPWORDS:
            continue
        expanded.append(t)
        expanded.extend(ALIASES.get(t, []))
    # Multiword phrases from aliases should be quoted for FTS.
    dedup: list[str] = []
    seen = set()
    for t in expanded:
        t = t.strip().lower()
        if not t or t in seen:
            continue
        seen.add(t)
        dedup.append(t)
    return dedup


def fts_query(terms: list[str]) -> str:
    if not terms:
        return '""'
    parts = []
    for t in terms:
        if " " in t or "-" in t:
            phrase = re.sub(r"[^a-zA-Z0-9_ -]", " ", t).strip()
            if phrase:
                parts.append('"' + phrase.replace('"', ' ') + '"')
        else:
            safe = re.sub(r"[^a-zA-Z0-9_]", "", t)
            if safe:
                parts.append(safe)
    return " OR ".join(parts) if parts else '""'


def search(kb: Path, db: Path, query: str, limit: int) -> list[dict]:
    if index_stale(kb, db):
        rebuild(kb, db)
    conn = connect(db)
    terms = expand_query(query)
    q = fts_query(terms)
    rows = conn.execute(
        """
        SELECT a.*, bm25(article_fts, 3.0, 1.5, 2.0, 1.0, 0.5) AS score,
               snippet(article_fts, 3, '[', ']', ' … ', 28) AS snippet
        FROM article_fts
        JOIN articles a ON a.id = article_fts.rowid
        WHERE article_fts MATCH ?
        ORDER BY score ASC, a.original_date DESC
        LIMIT ?
        """,
        (q, limit),
    ).fetchall()
    results = []
    for r in rows:
        results.append({
            "title": r["title"],
            "author": r["author"],
            "date": r["original_date"],
            "tags": r["tags"],
            "url": r["url"],
            "path": str(kb / r["relpath"]),
            "relpath": r["relpath"],
            "snippet": re.sub(r"\s+", " ", r["snippet"] or "").strip(),
            "score": r["score"],
        })
    return results


def write_markdown_index(kb: Path, db: Path) -> Path:
    if index_stale(kb, db):
        rebuild(kb, db)
    conn = connect(db)
    rows = conn.execute("SELECT * FROM articles ORDER BY author_slug, original_date DESC, title").fetchall()
    out = kb / "INDEX.md"
    lines = ["# Knowledge Base Index", "", "> Auto-generated by `~/.hermes/scripts/kb_search.py --write-index`. Do not hand-edit.", "", f"Total articles: {len(rows)}", ""]
    current = None
    for r in rows:
        if r["author_slug"] != current:
            current = r["author_slug"]
            lines += [f"## {current}", ""]
        title = r["title"] or r["relpath"]
        meta = " · ".join(x for x in [r["original_date"], r["format"], r["tags"]] if x)
        lines.append(f"- [{title}]({r['relpath']}) — {meta}")
    out.write_text("\n".join(lines) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*", help="Search query")
    ap.add_argument("--kb", default=str(DEFAULT_KB))
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--write-index", action="store_true")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    kb = Path(args.kb).expanduser()
    db = Path(args.db).expanduser()
    if not kb.is_dir():
        print(f"KB not found: {kb}", file=sys.stderr)
        return 2
    if args.rebuild:
        count = rebuild(kb, db)
        print(f"Indexed {count} articles into {db}")
    if args.write_index:
        out = write_markdown_index(kb, db)
        print(f"Wrote {out}")
    query = " ".join(args.query).strip()
    if query:
        results = search(kb, db, query, args.limit)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No matching KB articles found.")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['title']}")
                print(f"   author: {r['author']} | date: {r['date']} | tags: {r['tags']}")
                print(f"   path: {r['relpath']}")
                if r['url']:
                    print(f"   url: {r['url']}")
                if r['snippet']:
                    print(f"   match: {r['snippet']}")
    if not (args.rebuild or args.write_index or query):
        ap.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
