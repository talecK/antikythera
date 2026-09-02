#!/usr/bin/env python3
"""Render a paper draft (reports/paper{1,2}_draft.md) to a self-contained
HTML page for phone review (Claude artifact), figures embedded as data
URIs. The markdown file is the source of record; this script only
renders it.

Usage: render_paper_html.py paper1|paper2 --out /path/to/file.html
"""
import argparse
import base64
import html
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "reports", "figures")
DATA_DOI = "10.5281/zenodo.22262036"
CODE_URL = "https://github.com/talecK/antikythera"

PAPERS = {
    "paper1": dict(
        md="reports/paper1_draft.md",
        title="Ideas That Never Meet",
        eyebrow="Antikythera · Paper 1 · final results, awaiting author prose pass",
        accent=("#3d4f7d", "#333f66", "#96a8e0", "#aab9e8"),
        companion=("Watching the Walls Go Up",
                   "https://claude.ai/code/artifact/34b0ab8e-c6bd-48b2-af90-8d5874de0ba7"),
    ),
    "paper2": dict(
        md="reports/paper2_draft.md",
        title="Watching the Walls Go Up",
        eyebrow="Antikythera · Paper 2 · registered study, conforming run",
        accent=("#0e5f6b", "#0b4d57", "#58b7c4", "#7fc9d4"),
        companion=("Ideas That Never Meet",
                   "https://claude.ai/code/artifact/b6e82250-dc7e-42d1-9421-64eff6faeda9"),
    ),
}

CSS = """<style>
:root{
  --bg:#fafbfc; --surface:#f1f4f6; --ink:#1c2126; --muted:#5a6572;
  --rule:#dfe4e9; --accent:ACC_L; --accent-ink:ACC_LI;
  --pass:#1a7f4b; --pass-bg:#e3f2ea; --hot:#a34808; --code-bg:#eceff2;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#14181c; --surface:#1b2127; --ink:#e4e8eb; --muted:#98a3ad;
    --rule:#2a3138; --accent:ACC_D; --accent-ink:ACC_DI;
    --pass:#5cc593; --pass-bg:#173327; --hot:#e8975a; --code-bg:#20272e;
  }
}
:root[data-theme="dark"]{
  --bg:#14181c; --surface:#1b2127; --ink:#e4e8eb; --muted:#98a3ad;
  --rule:#2a3138; --accent:ACC_D; --accent-ink:ACC_DI;
  --pass:#5cc593; --pass-bg:#173327; --hot:#e8975a; --code-bg:#20272e;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--bg); color:var(--ink);
  font-family:"Source Serif 4",Georgia,"Times New Roman",serif; font-size:1.02rem; line-height:1.62}
.page{max-width:44rem; margin:0 auto; padding:2.2rem 1.15rem 4rem}
a{color:var(--accent-ink); text-decoration-color:color-mix(in srgb,var(--accent) 45%,transparent)}
a:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:2px}
.eyebrow{font-family:Archivo,system-ui,sans-serif; font-size:.72rem; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent-ink); margin:0 0 .9rem}
h1{font-family:Archivo,system-ui,sans-serif; font-weight:700; text-wrap:balance;
  font-size:clamp(1.55rem,4.6vw,2.15rem); line-height:1.18; margin:0 0 .9rem; letter-spacing:-.01em}
.byline{font-size:.95rem; color:var(--muted); margin:0 0 1.1rem}
.byline b{color:var(--ink); font-weight:600}
.status{background:var(--surface); border:1px solid var(--rule); border-radius:8px;
  padding:.75rem .95rem; font-size:.88rem; color:var(--muted); line-height:1.5}
.status code{color:var(--ink)}
nav.toc{border-top:1px solid var(--rule); border-bottom:1px solid var(--rule); margin:1.8rem 0 2.4rem; padding:.9rem 0}
nav.toc .toc-label{font-family:Archivo,system-ui,sans-serif; font-size:.7rem; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); margin-bottom:.5rem}
nav.toc ol{margin:0; padding:0; list-style:none; display:flex; flex-wrap:wrap; gap:.35rem .5rem;
  font-family:Archivo,system-ui,sans-serif; font-size:.82rem}
nav.toc a{display:inline-block; padding:.28rem .6rem; border:1px solid var(--rule); border-radius:999px;
  text-decoration:none; color:var(--ink); background:var(--surface)}
nav.toc a:hover{border-color:var(--accent)}
h2{font-family:Archivo,system-ui,sans-serif; font-weight:700; font-size:1.24rem; line-height:1.3;
  margin:2.6rem 0 .9rem; padding-top:1.3rem; border-top:1px solid var(--rule); text-wrap:balance; letter-spacing:-.005em}
h2 .n{color:var(--accent-ink); margin-right:.45rem}
h3{font-family:Archivo,system-ui,sans-serif; font-weight:600; font-size:1.02rem; margin:1.9rem 0 .6rem; text-wrap:balance}
p{margin:0 0 1rem}
ul,ol{margin:0 0 1rem; padding-left:1.25rem}
li{margin-bottom:.5rem}
strong{font-weight:600}
code{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; font-size:.82em; background:var(--code-bg);
  border-radius:4px; padding:.08em .34em}
.abstract{border-left:3px solid var(--accent); padding:.15rem 0 .15rem 1.05rem; margin:1.6rem 0 0}
.abstract p{font-size:.97rem}
.abstract .abs-label{font-family:Archivo,system-ui,sans-serif; font-size:.7rem; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent-ink); margin-bottom:.55rem}
.pass{display:inline-block; font-family:Archivo,system-ui,sans-serif; font-weight:600; font-size:.74rem;
  letter-spacing:.06em; color:var(--pass); background:var(--pass-bg); border-radius:999px; padding:.12rem .55rem; vertical-align:.08em}
.tw{overflow-x:auto; margin:0 0 1.15rem; border:1px solid var(--rule); border-radius:8px}
table{border-collapse:collapse; width:100%; font-size:.84rem; font-family:Archivo,system-ui,sans-serif}
th,td{padding:.42rem .6rem; white-space:nowrap; border-top:1px solid var(--rule); text-align:left}
thead th{border-top:none; font-weight:600; font-size:.76rem; letter-spacing:.03em; color:var(--muted); background:var(--surface)}
td.num,th.num{text-align:right; font-variant-numeric:tabular-nums; font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.8rem}
.figcard{background:var(--surface); border:1px solid var(--rule); border-radius:8px; padding:.85rem 1rem; margin-bottom:.85rem; font-size:.92rem}
.figcard img{max-width:100%; height:auto; border-radius:4px; margin-bottom:.5rem}
footer{margin-top:3rem; border-top:1px solid var(--rule); padding-top:1rem; font-size:.82rem; color:var(--muted);
  font-family:Archivo,system-ui,sans-serif}
@media (prefers-reduced-motion: no-preference){ html{scroll-behavior:smooth} }
</style>"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;'
         '0,8..60,600;1,8..60,400&family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(P[123]) PASS\.\*\*', r'<strong>\1</strong> <span class="pass">PASS</span>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\bz_\{([^}]+)\}', r'z<sub>\1</sub>', s)
    s = re.sub(r'\b([zfE])_([a-z0-9])\b', r'\1<sub>\2</sub>', s)
    s = re.sub(r'(https?://[^\s)<]+)', r'<a href="\1">\1</a>', s)
    return s


def is_num(c):
    c = c.replace('**', '')
    return any(ch.isdigit() for ch in c) and re.fullmatch(r'[+\-~≤≥<>=\d.,eEQ %/()−]+', c) is not None


def blocks_of(md_text):
    blocks, cur = [], []
    for line in md_text.splitlines():
        if line.strip() == '':
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        blocks.append(cur)
    return blocks


def render_list(lines):
    """Bullet list with optional one-level nesting (two-space indented '- ')."""
    items = []  # (text, [subitems])
    for l in lines:
        if l.startswith('- '):
            items.append([l[2:].strip(), []])
        elif l.startswith('  - '):
            items[-1][1].append(l[4:].strip())
        elif items and items[-1][1]:
            items[-1][1][-1] += ' ' + l.strip()
        elif items:
            items[-1][0] += ' ' + l.strip()
    out = ['<ul>']
    for text, subs in items:
        out.append(f'<li>{inline(text)}' +
                   ('<ul>' + ''.join(f'<li>{inline(s)}</li>' for s in subs) + '</ul>' if subs else '') +
                   '</li>')
    out.append('</ul>')
    return ''.join(out)


def render_numbered(lines):
    items = []
    for l in lines:
        if re.match(r'\d+\.\s', l):
            items.append(re.sub(r'^\d+\.\s+', '', l).strip())
        elif items:
            items[-1] += ' ' + l.strip()
    return '<ol>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ol>'


def render_table(lines):
    out = ['<div class="tw"><table>']
    body_open = False
    for i, r in enumerate(l for l in lines if l.startswith('|')):
        cells = [c.strip() for c in r.strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?', c) for c in cells):
            continue
        tag = 'th' if i == 0 else 'td'
        row = ''.join('<%s%s>%s</%s>' % (tag, ' class="num"' if is_num(c) else '', inline(c), tag)
                      for c in cells)
        if i == 0:
            out.append(f'<thead><tr>{row}</tr></thead><tbody>')
            body_open = True
        else:
            out.append(f'<tr>{row}</tr>')
    out.append('</tbody></table></div>' if body_open else '</table></div>')
    return ''.join(out)


def data_uri(name):
    with open(os.path.join(FIG, name), 'rb') as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def render(paper, out_path, preprint=None):
    cfg = PAPERS[paper]
    md_path = os.path.join(ROOT, cfg["md"])
    md = open(md_path).read()
    commit = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%h", "--", cfg["md"]],
                            capture_output=True, text=True).stdout.strip()

    title_line, byline, status = None, None, None
    body, toc = [], []
    in_abstract = False
    sec_n = 0

    for b in blocks_of(md):
        first = b[0]
        if first.startswith('# ') and title_line is None:
            title_line = first[2:].strip()
            continue
        if all(l.strip() == '---' for l in b):
            continue
        if byline is None and first.startswith('**Author:**'):
            byline = re.sub(r'^\*\*Author:\*\*\s*', '', ' '.join(b)).strip()
            continue
        if status is None and first.startswith('**') and ' '.join(b).rstrip().endswith('**') and not body:
            status = ' '.join(l.strip() for l in b).strip('*').strip()
            continue
        if first.startswith('## '):
            if in_abstract:
                body.append('</section>')
                in_abstract = False
            text = ' '.join(l[3:].strip() for l in b)
            sec_n += 1
            sid = f"sec{sec_n}"
            m = re.match(r'(\d+)\.\s+(.*)', text)
            if text.strip().lower().startswith('abstract'):
                body.append(f'<section id="{sid}" class="abstract"><div class="abs-label">Abstract</div>')
                in_abstract = True
                toc.append((sid, 'Abstract'))
            elif m:
                body.append(f'<h2 id="{sid}"><span class="n">{m.group(1)}</span>{inline(m.group(2))}</h2>')
                toc.append((sid, f"{m.group(1)} {re.sub(r'[:(].*', '', m.group(2)).strip()}"))
            else:
                body.append(f'<h2 id="{sid}">{inline(text)}</h2>')
                toc.append((sid, re.sub(r'[:(].*', '', text).strip()))
            continue
        if first.startswith('### '):
            body.append(f'<h3>{inline(" ".join(l[4:].strip() for l in b))}</h3>')
            continue
        if first.startswith('|'):
            body.append(render_table(b))
            continue
        if first.startswith('- '):
            body.append(render_list(b))
            continue
        if re.match(r'\d+\.\s', first):
            body.append(render_numbered(b))
            continue
        text = ' '.join(l.strip() for l in b)
        fm = re.match(r'\*\*Figure (\d+)\*\*\s*\(([\w]+)\.png', text)
        if fm and os.path.exists(os.path.join(FIG, fm.group(2) + '.png')):
            body.append(f'<div class="figcard"><img src="{data_uri(fm.group(2) + ".png")}" '
                        f'alt="Figure {fm.group(1)}">{inline(text)}</div>')
            continue
        body.append(f'<p>{inline(text)}</p>')
    if in_abstract:
        body.append('</section>')

    css = (CSS.replace('ACC_LI', cfg["accent"][1]).replace('ACC_L', cfg["accent"][0])
              .replace('ACC_DI', cfg["accent"][3]).replace('ACC_D', cfg["accent"][2]))
    toc_html = ''.join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t in toc)
    comp_name, comp_url = cfg["companion"]
    if preprint:
        # Public preprint: no review banner, no draft-status block, no
        # contents strip, no private artifact links, no render footer.
        head = (f'<p class="eyebrow">Preprint · {html.escape(preprint)}</p>'
                f'<h1>{inline(title_line or cfg["title"])}</h1>'
                f'<p class="byline"><b>{inline(byline or "")}</b></p>'
                f'<div class="status">Data release: <a href="https://doi.org/{DATA_DOI}">doi:{DATA_DOI}</a>. '
                f'Code and registrations: <a href="{CODE_URL}">{CODE_URL}</a> (public at publication). '
                f'Companion paper: {html.escape(comp_name)} (preprint).</div>')
        tail = ''
    else:
        head = (f'<p class="eyebrow">{html.escape(cfg["eyebrow"])}</p>'
                f'<h1>{inline(title_line or cfg["title"])}</h1>'
                f'<p class="byline"><b>{inline(byline or "")}</b></p>'
                f'<div class="status">{inline(status or "")} Source of record: <code>{cfg["md"]}</code>, commit <code>{commit}</code>. Companion paper: <a href="{comp_url}">{html.escape(comp_name)}</a>.</div>'
                f'<nav class="toc" aria-label="Contents"><div class="toc-label">Contents</div><ol>{toc_html}</ol></nav>')
        tail = f'<footer>Rendered from <code>{cfg["md"]}</code> @ <code>{commit}</code> by eval/render_paper_html.py · Antikythera</footer>'
    page = f'''<title>{html.escape(cfg["title"])}</title>
{FONTS}
{css}
<div class="page">
{head}
{chr(10).join(body)}
{tail}
</div>
'''
    with open(out_path, 'w') as f:
        f.write(page)
    return commit, len(page), [t for _, t in toc]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", choices=sorted(PAPERS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--preprint", default=None, metavar="DATE",
                    help="public preprint mode; DATE is shown in the eyebrow, e.g. 'September 2026'")
    a = ap.parse_args()
    commit, size, toc = render(a.paper, a.out, a.preprint)
    print(f"{a.paper} @ {commit}: {size} bytes; sections: {toc}")
