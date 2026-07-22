from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
s = p.read_text(encoding="utf-8")

s = s.replace('''    <div class="ml-auto hidden lg:flex gap-8 text-[.9rem] text-bone-dim">
      <a href="#richieste" class="hover:text-bone transition-colors duration-200">Cosa faccio</a>
      <a href="#metodo"   class="hover:text-bone transition-colors duration-200">Metodo</a>
      <a href="#capacita" class="hover:text-bone transition-colors duration-200">Capacità tecniche</a>
      <a href="#lavori"   class="hover:text-bone transition-colors duration-200">Lavori</a>
      <a href="#ambiti"   class="hover:text-bone transition-colors duration-200">Ambiti</a>
    </div>''','''    <div class="ml-auto hidden lg:flex gap-8 text-[.9rem] text-bone-dim">
      <a href="#servizi" class="hover:text-bone transition-colors duration-200">Servizi</a>
      <a href="/materiali/" class="hover:text-bone transition-colors duration-200">Materiali</a>
      <a href="/portfolio/" class="hover:text-bone transition-colors duration-200">Lavori</a>
      <a href="#metodo" class="hover:text-bone transition-colors duration-200">Metodo</a>
      <a href="/chi-siamo/" class="hover:text-bone transition-colors duration-200">Chi sono</a>
    </div>''')

s = s.replace('''      <a href="#richieste" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Cosa faccio</a>
      <a href="#metodo"   class="py-2.5 text-bone-dim hover:text-bone transition-colors">Metodo</a>
      <a href="#capacita" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Capacità tecniche</a>
      <a href="#lavori"   class="py-2.5 text-bone-dim hover:text-bone transition-colors">Lavori</a>
      <a href="#ambiti"   class="py-2.5 text-bone-dim hover:text-bone transition-colors">Ambiti</a>''','''      <a href="#servizi" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Servizi</a>
      <a href="/materiali/" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Materiali</a>
      <a href="/portfolio/" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Lavori</a>
      <a href="#metodo" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Metodo</a>
      <a href="/chi-siamo/" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Chi sono</a>
      <a href="/contatti/" class="py-2.5 text-bone-dim hover:text-bone transition-colors">Contatti</a>''')

cards = [
('''      <div class="card rv">
        <div class="w-11 h-11 rounded-xl grid place-items-center bg-copper/10 text-copper font-mono text-[.85rem] font-semibold mb-5">01</div>
        <h3 class="text-[1.2rem] mb-2.5">Disegno 3D (CAD)</h3>
        <p class="text-[.95rem]">Il disegno tridimensionale del pezzo, costruito su misure e ingombri. Ti consegno anche il file, se ti serve portarlo altrove.</p>
      </div>''','''      <a href="/servizi/progettazione-cad/" class="card rv block group" aria-label="Scopri il servizio di progettazione CAD">
        <div class="w-11 h-11 rounded-xl grid place-items-center bg-copper/10 text-copper font-mono text-[.85rem] font-semibold mb-5">01</div>
        <h3 class="text-[1.2rem] mb-2.5">Disegno 3D (CAD)</h3>
        <p class="text-[.95rem]">Il disegno tridimensionale del pezzo, costruito su misure e ingombri. Ti consegno anche il file, se ti serve portarlo altrove.</p>
        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Scopri il servizio →</span>
      </a>'''),
('''      <div class="card rv" data-d="1">
        <div class="w-11 h-11 rounded-xl grid place-items-center bg-copper/10 text-copper font-mono text-[.85rem] font-semibold mb-5">02</div>
        <h3 class="text-[1.2rem] mb-2.5">Copia di un pezzo esistente</h3>
        <p class="text-[.95rem]">Misuro il pezzo che mi porti e ne ricostruisco il disegno. Funziona anche se è rotto, purché resti abbastanza da misurare.</p>
      </div>''','''      <a href="/servizi/reverse-engineering/" class="card rv block group" data-d="1" aria-label="Scopri il servizio di reverse engineering">
        <div class="w-11 h-11 rounded-xl grid place-items-center bg-copper/10 text-copper font-mono text-[.85rem] font-semibold mb-5">02</div>
        <h3 class="text-[1.2rem] mb-2.5">Copia di un pezzo esistente</h3>
        <p class="text-[.95rem]">Misuro il pezzo che mi porti e ne ricostruisco il disegno. Funziona anche se è rotto, purché resti abbastanza da misurare.</p>
        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Scopri il servizio →</span>
      </a>'''),
('''      <div class="card rv" data-d="2">''','''      <a href="/servizi/componenti-custom/" class="card rv block group" data-d="2" aria-label="Scopri dime e componenti su misura">'''),
('''      </div>
      <div class="card rv" data-d="3">''','''        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Scopri il servizio →</span>
      </a>
      <a href="/servizi/prototipazione-rapida/" class="card rv block group" data-d="3" aria-label="Scopri la prototipazione rapida">'''),
('''      </div>
      <div class="card rv" data-d="4">''','''        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Scopri il servizio →</span>
      </a>
      <a href="/stampa-3d-personalizzata/" class="card rv block group" data-d="4" aria-label="Scopri la stampa 3D personalizzata">'''),
('''      </div>
      <div class="card rv" data-d="5">''','''        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Scopri il servizio →</span>
      </a>
      <a href="/contatti/" class="card rv block group" data-d="5" aria-label="Contattami per elettronica e sensori">'''),
('''        <p class="text-[.95rem]">Piccoli sistemi con sensori, cablaggi o comandi quando il componente deve integrare anche una funzione elettronica.</p>
      </div>
    </div>''','''        <p class="text-[.95rem]">Piccoli sistemi con sensori, cablaggi o comandi quando il componente deve integrare anche una funzione elettronica.</p>
        <span class="mt-5 inline-flex items-center gap-2 text-[.84rem] font-medium text-copper transition-transform duration-300 group-hover:translate-x-1">Parliamone →</span>
      </a>
    </div>

    <div class="mt-10 flex flex-wrap gap-3 rv" data-d="2">
      <a href="/materiali/" class="btn btn-ghost">Confronta i materiali</a>
      <a href="/portfolio/" class="btn btn-ghost">Vedi i lavori reali</a>
      <a href="/stampa-3d-mirandola/" class="btn btn-ghost">Stampa 3D a Mirandola</a>
    </div>''')]
for old,new in cards:
    if old not in s:
        print("missing", old[:70])
    s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")
print("updated",p)
