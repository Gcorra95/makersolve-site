from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
changed = []
for path in root.rglob("index.html"):
    if path == root / "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    old = text
    text = text.replace('/assets/ms.css?v=2', '/assets/ms-tw.css?v=3')
    text = text.replace('/assets/ms.js?v=2', '/assets/ms-tw.js?v=3')
    if 'space-grotesk-latin-var.woff2' not in text:
        marker = '<link rel="icon" type="image/png" href="/assets/logo.png">'
        preload = marker + '\n<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/space-grotesk-latin-var.woff2" crossorigin>\n<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/inter-latin-var.woff2" crossorigin>'
        text = text.replace(marker, preload, 1)
    text = text.replace('<div class="hero-halo"></div>', '<div id="halo" class="hero-halo"></div>')
    text = re.sub(r'(<div class="hero-media"><img)(?![^>]*class=)', r'\1 class="tint-copper parallax"', text)
    text = re.sub(r'(<div class="sec-bg"><img)(?![^>]*class=)', r'\1 class="tint-copper parallax"', text)
    if text != old:
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(root).as_posix())
print(f"Updated {len(changed)} pages")
for p in changed:
    print(p)
