from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
urls={}
for p in root.rglob('index.html'):
    s=p.read_text(encoding='utf-8')
    ext=sorted(set(re.findall(r'(?:src|href|action)=["\'](https?://[^"\']+)',s)))
    if ext: urls[str(p.relative_to(root))]=ext
for p,u in urls.items():
    print(p)
    for x in u: print(' ',x)
print('\nFORM CHECK')
s=(root/'contatti/index.html').read_text(encoding='utf-8')
for term in ['api.web3forms.com','privacy policy','type="checkbox" required','name="privacy_ack"']:
    print(term, term in s)
