from pathlib import Path

root = Path(__file__).resolve().parents[1]
old_variants = [
    "Disegno e stampo pezzi su misura per aziende e privati.\n          Officina a Mirandola (MO), spedizioni in tutta Italia.",
    "Progettazione meccanica, reverse engineering e stampa 3D per aziende e professionisti.\n          Officina a Mirandola (MO), lavorazioni in tutta Italia.",
]
new_text = (
    "Progettazione meccanica, reverse engineering e stampa 3D per aziende e professionisti.\n"
    "          Officina a Mirandola (MO), spedizioni in tutta Italia."
)

changed = []
for path in root.rglob("index.html"):
    text = path.read_text(encoding="utf-8")
    updated = text
    for old in old_variants:
        updated = updated.replace(old, new_text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        changed.append(path.relative_to(root))

print(f"CHANGED={len(changed)}")
for path in changed:
    print(path)
