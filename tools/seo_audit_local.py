from pathlib import Path
import re
from html import unescape

root = Path(__file__).resolve().parents[1]
files = sorted(root.rglob('index.html'))
issues = []
for p in files:
    s = p.read_text(encoding='utf-8', errors='ignore')
    rel = p.relative_to(root).as_posix()
    def one(pattern):
        m = re.search(pattern, s, re.I|re.S)
        return unescape(m.group(1).strip()) if m else ''
    title = one(r'<title>(.*?)</title>')
    desc = one(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']')
    canon = one(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']')
    h1s = re.findall(r'<h1\b', s, re.I)
    noindex = bool(re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex', s, re.I))
    print(f'{rel}\n  title({len(title)}): {title}\n  desc({len(desc)}): {desc}\n  canonical: {canon}\n  h1: {len(h1s)} noindex:{noindex}')
    if not title or not desc or not canon or len(h1s)!=1:
        issues.append(rel)
print('\nFILES', len(files), 'ISSUES', issues)
print('\nrobots.txt:')
print((root/'robots.txt').read_text(encoding='utf-8', errors='ignore') if (root/'robots.txt').exists() else 'MISSING')
print('\nsitemap exists:', (root/'sitemap.xml').exists())
