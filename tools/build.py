#!/usr/bin/env python3
"""Builds the public policy pages from Markdown sources.

    python3 tools/build.py          # regenerate every HTML page
    python3 tools/build.py check    # fail if a page is out of date (used by CI)

Layout
    apps.json                         list of apps (id, name, name_en, documents)
    src/<app-id>/<DOC>.md             Korean source   (DOC = PRIVACY, TERMS, ...)
    src/<app-id>/<DOC>_en.md          English source  (optional)
    <app-id>/<doc>/index.html         generated Korean page   -> /<app-id>/<doc>/
    <app-id>/<doc>/en.html            generated English page  -> /<app-id>/<doc>/en.html
    index.html                        generated list of all apps

No third-party packages: the Markdown subset used by policies (headings, paragraphs,
bullet/numbered lists, **bold**, `code`, links and bare URLs) is converted here.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_SLUG = {"PRIVACY": "privacy", "TERMS": "terms"}
DOC_TITLE = {"PRIVACY": ("개인정보처리방침", "Privacy Policy"), "TERMS": ("이용약관", "Terms of Use")}


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"(?<![\"'>=])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def md_to_html(md: str) -> tuple[str, str]:
    """Returns (title from the first # heading, body HTML)."""
    title, parts, para, lst = "", [], [], None

    def flush_para():
        if para:
            parts.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        nonlocal lst
        if lst:
            tag, items = lst
            parts.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            lst = None

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_list(); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para(); flush_list()
            level = len(m.group(1))
            if level == 1 and not title:
                title = m.group(2).strip()
            parts.append(f"<h{level}>{inline(m.group(2).strip())}</h{level}>")
            continue
        m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para()
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            if lst is None or lst[0] != tag:
                flush_list(); lst = (tag, [])
            lst[1].append(m.group(2).strip())
            continue
        if lst is not None and raw.startswith("  "):
            lst[1][-1] += " " + line.strip()
            continue
        flush_list()
        para.append(line.strip())
    flush_para(); flush_list()
    return title, "\n".join(parts)


STYLE = """
:root{--bg:#ffffff;--fg:#1d2330;--muted:#5d6675;--line:#e3e6eb;--accent:#2f5bd3}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--fg:#e7e9ee;--muted:#9aa3b2;--line:#2a2f37;--accent:#8fb0ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:1.6rem;line-height:1.3;margin:0 0 8px}h2{font-size:1.15rem;margin:32px 0 8px;padding-top:16px;border-top:1px solid var(--line)}
a{color:var(--accent);word-break:break-all}ul,ol{padding-left:1.3em}li{margin:4px 0}
code{background:var(--line);padding:1px 5px;border-radius:4px}
nav{display:flex;gap:12px;justify-content:flex-end;font-size:.9rem;margin-bottom:24px}
.card{border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}.card h2{border:0;margin:0 0 6px;padding:0}
.muted{color:var(--muted);font-size:.9rem}
"""


def page(lang: str, title: str, body: str, nav: str) -> str:
    return (
        f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n<style>{STYLE}</style>\n</head>\n"
        f"<body><main>\n{nav}\n{body}\n</main></body>\n</html>\n"
    )


def outputs() -> dict[Path, str]:
    apps = json.loads((ROOT / "apps.json").read_text(encoding="utf-8"))
    files: dict[Path, str] = {}
    cards = []
    for app in apps:
        app_id = app["id"]
        links = []
        for doc in app["documents"]:
            slug = DOC_SLUG[doc]
            ko_src = ROOT / "src" / app_id / f"{doc}.md"
            en_src = ROOT / "src" / app_id / f"{doc}_en.md"
            has_en = en_src.exists()
            for lang, src, out_name in (("ko", ko_src, "index.html"), ("en", en_src, "en.html")):
                if not src.exists():
                    continue
                title, body = md_to_html(src.read_text(encoding="utf-8"))
                other = ('<a href="en.html">English</a>' if lang == "ko" else '<a href="./">한국어</a>') if has_en else ""
                nav = f'<nav><a href="../../">{"모든 앱" if lang == "ko" else "All apps"}</a>{other}</nav>'
                files[ROOT / app_id / slug / out_name] = page(lang, title, body, nav)
            ko_t, en_t = DOC_TITLE[doc]
            links.append(f'<a href="{app_id}/{slug}/">{ko_t}</a>' + (f' · <a href="{app_id}/{slug}/en.html">{en_t}</a>' if has_en else ""))
        cards.append(
            f'<div class="card"><h2>{html.escape(app["name"])}</h2>'
            f'<div class="muted">{html.escape(app.get("name_en", ""))} · <code>{html.escape(app.get("package", ""))}</code></div>'
            f'<p>{" | ".join(links)}</p></div>'
        )
    index_body = "<h1>앱 정책 문서 · App Policies</h1>\n<p class=\"muted\">gwfaoking이 만든 앱의 개인정보처리방침과 약관입니다.</p>\n" + "\n".join(cards)
    files[ROOT / "index.html"] = page("ko", "앱 정책 문서 · App Policies", index_body, "")
    return files


def main() -> int:
    check = len(sys.argv) > 1 and sys.argv[1] == "check"
    stale = []
    for path, content in outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
            print("wrote", path.relative_to(ROOT).as_posix())
    if stale:
        print("Out of date (run python3 tools/build.py):", *stale, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
