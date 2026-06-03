# MakerSolve — audit SEO e piano implementato

Data: 2026-06-03
Area target: Mirandola, Modena, Emilia-Romagna, Nord Italia
Tipo sito: HTML statico su GitHub Pages
Obiettivo: clienti B2B reali, non traffico generico

## 1. Analisi SEO attuale

### Problemi corretti

- Placeholder eliminati: telefono finto, P.IVA finta, form finto.
- Pagine mancanti create: servizi, materiali, portfolio, chi siamo, contatti, blog, privacy.
- Sitemap aggiornata e coerente con pagine esistenti.
- Robots.txt pulito.
- CSS centralizzato con cache-busting.
- Logo reale usato nella navbar e come favicon provvisoria.
- Meta title e description riscritti pagina per pagina.
- Canonical inserito in ogni pagina.
- Open Graph base inserito in ogni pagina.

### Problemi ancora aperti

- Manca immagine Open Graph dedicata 1200x630.
- Mancano casi studio reali con foto e dettagli tecnici.
- Blog ancora vuoto: esiste come indice, ma non ha articoli.
- Local SEO completa richiede Google Business Profile e prime citazioni esterne.
- Manca misurazione Search Console.
- Manca una pagina verticale per ciascun caso studio.

## 2. SEO e copy

### Struttura copy corretta

Homepage:
- Messaggio centrale: dal problema tecnico al componente in mano.
- Target: aziende, officine, manutentori, realtà industriali.
- Servizi principali: CAD, reverse engineering, prototipazione rapida, componenti custom.

Pagine servizio:
- Ogni pagina ha H1 specifico.
- H2 orientati a problemi reali, non a slogan.
- CTA orientate a richiesta tecnica.

### Linea editoriale

Tono: tecnico, concreto, moderno.

Da evitare:
- service stampa 3D generico
- frasi tipo “soluzioni innovative a 360°”
- keyword stuffing
- claim non dimostrabili

Da usare:
- componente rotto
- pezzo fuori produzione
- supporto custom
- adattatore tecnico
- prototipo funzionale
- piccolo lotto senza stampi

## 3. Local SEO

### Area principale

- Mirandola
- Modena
- Emilia-Romagna
- Nord Italia

### Pagine già orientate local

- Home
- Progettazione CAD
- Reverse engineering
- Prototipazione rapida
- Componenti custom
- Contatti
- Chi siamo

### Azioni esterne necessarie

1. Creare o aggiornare Google Business Profile quando l'attività è pronta.
2. Usare sempre lo stesso NAP: nome, indirizzo/area, email, telefono se pubblicato.
3. Inserire sito in profili coerenti: LinkedIn, eventuali directory industriali locali, portfolio tecnico.
4. Ottenere primi link reali da partner, fornitori, progetti, profili social.

## 4. Keyword strategy

### Alta priorità

- progettazione CAD Mirandola
- progettazione CAD Modena
- reverse engineering componenti
- reverse engineering pezzi rotti
- prototipazione rapida Modena
- stampa 3D tecnica Modena
- componenti custom stampa 3D
- piccoli lotti stampa 3D
- componenti fuori produzione
- supporti custom industriali

### Media priorità

- laboratorio tecnico Mirandola
- prototipi funzionali stampa 3D
- stampa 3D materiali tecnici
- stampa 3D PA-CF
- stampa 3D ASA componenti tecnici
- dime e attrezzature custom
- adattatori custom CAD
- progettazione componenti plastici

### Blog/content

- quanto costa progettare un componente custom in CAD
- reverse engineering pezzo rotto preventivo
- quando conviene stampa 3D rispetto CNC
- PETG ASA PA-CF quale materiale scegliere
- piccoli lotti senza stampi
- prototipo funzionale vs prototipo estetico

### Local SEO

- stampa 3D Mirandola
- prototipazione Mirandola
- reverse engineering Mirandola
- stampa 3D Modena
- prototipazione rapida Modena
- progettazione CAD Emilia-Romagna
- componenti custom Emilia-Romagna

## 5. Ottimizzazione HTML implementata

Ogni pagina principale ora include:

- title specifico
- meta description specifica
- canonical
- robots index/follow
- Open Graph
- favicon provvisoria
- CSS condiviso
- CTA verso contatti

Homepage include anche JSON-LD LocalBusiness/ProfessionalService.

## 6. GitHub Pages SEO

### Struttura consigliata attuale

```txt
/
  index.html
  CNAME
  robots.txt
  sitemap.xml
  .nojekyll
  assets/
    page.css
    logo.png
    site-config-loader.js
  data/
    site-config.js
    README.md
  servizi/
    progettazione-cad/index.html
    reverse-engineering/index.html
    prototipazione-rapida/index.html
    componenti-custom/index.html
    workflow-ai/index.html
  materiali/index.html
  portfolio/index.html
  chi-siamo/index.html
  contatti/index.html
  blog/index.html
  privacy-policy/index.html
  docs/
    seo-strategy.md
    seo-audit-and-implementation.md
```

### Best practice applicate

- URL descrittivi.
- Cartelle tematiche.
- Sitemap coerente.
- Robots.txt non blocca CSS/JS.
- .nojekyll presente.
- CSS con versione per evitare cache vecchia.

## 7. Conversione clienti

### Cosa funziona

- Messaggio principale chiaro.
- Target B2B tecnico.
- Servizi separati.
- CTA email diretta.
- No form finto.
- No claim eccessivi.

### Cosa manca ancora per convertire meglio

- Foto vere di pezzi.
- Foto laboratorio/stampanti/strumenti.
- 3 casi studio completi.
- Esempi di output: STEP, STL, prototipo, piccolo lotto.
- Prova sociale: prime recensioni, collaborazioni, progetti autorizzati.
- Numero di telefono solo quando vuoi davvero gestirlo.

## 8. Blog e contenuti

Priorità contenuti:

1. Reverse engineering di un pezzo rotto: cosa serve per un preventivo.
2. Quando conviene progettare un componente custom invece di adattare un pezzo commerciale.
3. PETG, ASA o PA-CF: scelta materiale per parti tecniche.
4. Piccoli lotti senza stampi: quando la stampa 3D è conveniente.
5. Prototipo funzionale: cosa validare prima della produzione.
6. Come preparare foto e misure per una richiesta CAD.

Contenuti LinkedIn/reel:

- prima/dopo CAD
- pezzo rotto → modello 3D → prototipo
- confronto materiali
- errori comuni nei pezzi stampati
- mini case study di 30-60 secondi
- “perché questo pezzo non va stampato in PLA”

## 9. Output tecnico pronto

### robots.txt

```txt
User-agent: *
Allow: /

Sitemap: https://makersolve.com/sitemap.xml
```

### Esempio meta pagina servizio

```html
<title>Reverse Engineering Componenti | MakerSolve Mirandola</title>
<meta name="description" content="Reverse engineering a Mirandola per pezzi rotti, ricambi fuori produzione e componenti senza disegno: rilievo quote, CAD e prototipo funzionale.">
<link rel="canonical" href="https://makersolve.com/servizi/reverse-engineering/">
<meta property="og:type" content="website">
<meta property="og:title" content="Reverse engineering componenti | MakerSolve">
<meta property="og:description" content="Ricostruzione CAD e prototipo fisico da campione, foto o componente danneggiato.">
<meta property="og:url" content="https://makersolve.com/servizi/reverse-engineering/">
<meta property="og:image" content="https://makersolve.com/assets/logo.png">
```

### Config centrale

Modificare:

```txt
data/site-config.js
```

Per email, telefono, P.IVA, città, regione, area servita.

## 10. Strategia

Il sito non deve posizionarsi come ecommerce, blog generico o portfolio artistico.

Deve posizionarsi come:

- laboratorio tecnico agile
- partner per prototipazione e problem solving
- supporto a officine, manutentori e aziende
- servizio tecnico per pezzi custom, prototipi e reverse engineering

La leva non è “stampa 3D economica”.

La leva è:

- ridurre fermo
- ottenere un pezzo non disponibile
- validare un prototipo
- produrre un piccolo lotto senza stampi
- avere un tecnico che capisce funzione, montaggio e materiale

## Prossimo step prioritario

Creare tre pagine caso studio:

```txt
/portfolio/refuser-3dx/
/portfolio/supporto-custom/
/portfolio/reverse-engineering-pezzo-rotto/
```

Ogni caso studio deve avere:

- problema
- vincoli
- processo
- materiale
- risultato
- foto
- CTA finale
