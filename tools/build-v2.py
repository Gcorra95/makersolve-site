#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MakerSolve — generatore delle pagine interne in stile v2.

Genera i file `index.html` di ogni pagina interna a partire da un template
condiviso (nav, footer, head, CTA finale) piu' il contenuto specifico definito
qui sotto in PAGES.

Uso:
    python tools/build-v2.py

Le pagine home (/index.html) e contatti (/contatti/index.html) sono
scritte a mano e NON vengono toccate da questo script.

NB: le pagine prodotte sono generate. Se preferisci modificarle a mano,
cancella questo script e da quel momento le pagine diventano la fonte unica.
"""

import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEL = "346 608 8830"
TEL_HREF = "+393466088830"
MAIL = "giulio.corazzari@gmail.com"

# ---------------------------------------------------------------- componenti

def nav(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return '      <a href="%s"%s>%s</a>' % (href, cur, label)
    links = "\n".join([
        a('/#servizi', 'Servizi', 'servizi'),
        a('/#metodo', 'Metodo', 'metodo'),
        a('/materiali/', 'Materiali', 'materiali'),
        a('/portfolio/', 'Lavori', 'portfolio'),
        a('/chi-siamo/', 'Chi sono', 'chi-siamo'),
    ])
    return """<nav class="nav" id="nav">
  <div class="wrap">
    <a href="/" class="brand"><span class="dot"></span>MakerSolve</a>
    <div class="navlinks">
%s
    </div>
    <a href="/contatti/" class="btn btn-primary">Richiedi fattibilit&agrave;</a>
  </div>
</nav>""" % links


def hero(eyebrow, h1, lead, crumb_label, img="gen-hero-bg", note=None):
    note = note or "Risposta in 24/48h &middot; Valutazione gratuita &middot; Nessun impegno"
    return """<header class="hero compact">
  <div class="hero-media"><img src="/assets/%s.webp" alt="" aria-hidden="true" fetchpriority="high"></div>
  <div class="hero-scrim"></div>
  <div class="hero-grid"></div>
  <div class="hero-halo"></div>
  <div class="wrap">
    <div class="hero-copy">
      <div class="crumb rv"><a href="/">Home</a><span>/</span>%s</div>
      <span class="eyebrow rv">%s</span>
      <h1 class="rv" data-d="1">%s</h1>
      <p class="lead rv" data-d="2">%s</p>
      <div class="hero-cta rv" data-d="3">
        <a href="/contatti/" class="btn btn-primary btn-lg">Richiedi una valutazione</a>
        <a href="tel:%s" data-site-phone-link class="btn btn-ghost btn-lg">Chiama <span data-site-phone>%s</span></a>
      </div>
      <div class="hero-note rv" data-d="4"><span class="pulse-dot"></span>%s</div>
    </div>
  </div>
</header>""" % (img, crumb_label, eyebrow, h1, lead, TEL_HREF, TEL, note)


def sec_head(eyebrow, h2, lead=None):
    out = '    <div class="sec-head rv">\n      <span class="eyebrow">%s</span>\n      <h2>%s</h2>\n' % (eyebrow, h2)
    if lead:
        out += '      <p class="lead">%s</p>\n' % lead
    return out + '    </div>\n'


def cards(items, cols=3, dark=False):
    cls = "card dark" if dark else "card"
    out = '    <div class="grid-%d">\n' % cols
    for i, (title, body) in enumerate(items):
        d = ' data-d="%d"' % i if i else ''
        out += ('      <div class="%s rv"%s><div class="ico">%02d</div>\n'
                '        <h3>%s</h3>\n        <p>%s</p>\n      </div>\n') % (cls, d, i + 1, title, body)
    return out + '    </div>\n'


def pain(items):
    out = '    <div class="pain">\n'
    for i, (tag, title, body) in enumerate(items):
        d = ' data-d="%d"' % i if i else ''
        out += ('      <div class="rv"%s>\n        <span class="q">%s</span>\n'
                '        <h3>%s</h3>\n        <p>%s</p>\n      </div>\n') % (d, tag, title, body)
    return out + '    </div>\n'


def specs(rows):
    out = '    <dl class="specs rv">\n'
    for dt, dd in rows:
        out += ('      <div class="spec-row">\n        <dt>%s</dt>\n'
                '        <dd>%s</dd>\n      </div>\n') % (dt, dd)
    return out + '    </dl>\n'


def section(inner, cls="", sid=None, bg=None):
    attrs = ''
    if sid:
        attrs += ' id="%s"' % sid
    klass = cls
    if bg:
        klass = (klass + ' has-bg').strip()
    if klass:
        attrs += ' class="%s"' % klass
    bgdiv = ''
    if bg:
        bgdiv = '  <div class="sec-bg"><img src="/assets/%s.webp" alt="" loading="lazy"></div>\n' % bg
    return '<section%s>\n%s  <div class="wrap">\n%s  </div>\n</section>' % (attrs, bgdiv, inner)


MARQUEE = """<div class="marquee on-media" aria-hidden="true">
  <div class="band"><img src="/assets/gen-materials.webp" alt="" loading="lazy"></div>
  <div class="marquee-track">
    <span>PLA</span><span>PETG</span><span>ASA</span><span>ABS</span><span>TPU &middot; FLESSIBILE</span><span>NYLON CF</span><span>NYLON GF</span><span>RESINA</span><span>MATERIALI SPECIALI SU RICHIESTA</span>
    <span>PLA</span><span>PETG</span><span>ASA</span><span>ABS</span><span>TPU &middot; FLESSIBILE</span><span>NYLON CF</span><span>NYLON GF</span><span>RESINA</span><span>MATERIALI SPECIALI SU RICHIESTA</span>
  </div>
</div>"""


def cta_band(title, body):
    return """<section class="tight has-bg">
  <div class="sec-bg"><img src="/assets/gen-exploded.webp" alt="" loading="lazy"></div>
  <div class="wrap" style="text-align:center">
    <h2 class="rv" style="max-width:20ch;margin:0 auto 20px">%s</h2>
    <p class="lead rv" data-d="1" style="max-width:58ch;margin:0 auto">%s</p>
    <div class="hero-cta rv" data-d="2" style="justify-content:center">
      <a href="/contatti/" class="btn btn-primary btn-lg">Richiedi una valutazione</a>
      <a href="tel:%s" data-site-phone-link class="btn btn-ghost btn-lg">Chiama <span data-site-phone>%s</span></a>
    </div>
    <p class="rv" data-d="3" style="margin-top:26px;font-size:.86rem;color:var(--fg-dimmer)">
      Officina di progettazione CAD e stampa 3D a <span data-site-city>Mirandola</span>, in provincia di Modena &middot; Spedizioni in tutta Italia
    </p>
  </div>
</section>""" % (title, body, TEL_HREF, TEL)


FOOTER = """<footer>
  <div class="wrap">
    <div class="f-top">
      <div class="f-col">
        <a href="/" class="brand" style="margin-bottom:12px"><span class="dot"></span>MakerSolve</a>
        <p style="max-width:340px;line-height:1.6">
          Progettazione meccanica, reverse engineering e stampa 3D per aziende e professionisti.
          Officina a Mirandola (MO), lavorazioni in tutta Italia.
        </p>
      </div>
      <div class="f-col">
        <h4>Servizi</h4>
        <a href="/servizi/progettazione-cad/">Progettazione CAD</a>
        <a href="/servizi/reverse-engineering/">Reverse engineering</a>
        <a href="/servizi/prototipazione-rapida/">Prototipazione rapida</a>
        <a href="/servizi/componenti-custom/">Componenti custom</a>
        <a href="/stampa-3d-personalizzata/">Stampa 3D personalizzata</a>
        <a href="/materiali/">Materiali</a>
      </div>
      <div class="f-col">
        <h4>Contatti</h4>
        <a href="tel:%s" data-site-phone-link><span data-site-phone>%s</span></a>
        <a href="mailto:%s" data-site-email-link><span data-site-email>%s</span></a>
        <a href="https://www.linkedin.com/company/makersolve" data-site-linkedin-link rel="noopener">LinkedIn</a>
        <a href="/portfolio/">Lavori</a>
        <a href="/chi-siamo/">Chi sono</a>
        <a href="/contatti/">Contatti</a>
      </div>
    </div>
    <div class="f-bot">
      <span>&copy; <span id="yr">2026</span> MakerSolve &mdash; <span data-site-city>Mirandola</span> (MO)<span data-vat-optional> &middot; P.IVA <span data-site-vat></span></span></span>
      <span style="display:flex;gap:18px;flex-wrap:wrap">
        <a href="/privacy-policy/">Privacy</a>
        <a href="/cookie-policy/">Cookie</a>
        <a href="/termini/">Termini</a>
      </span>
    </div>
  </div>
</footer>""" % (TEL_HREF, TEL, MAIL, MAIL)


PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="https://makersolve.com/%(path)s">

<meta property="og:type" content="website">
<meta property="og:title" content="%(ogtitle)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="https://makersolve.com/%(path)s">
<meta property="og:image" content="https://makersolve.com/assets/og-card.jpg">
<meta property="og:locale" content="it_IT">

<link rel="icon" type="image/png" href="/assets/logo.png">
<link rel="stylesheet" href="/assets/ms.css?v=2">
</head>
<body>

%(nav)s

%(hero)s

%(body)s

%(cta)s

%(footer)s

<script type="application/ld+json">
%(jsonld)s
</script>

<script src="/data/site-config.js"></script>
<script src="/assets/site-config-loader.js" defer></script>
<script src="/assets/ms.js?v=2" defer></script>
</body>
</html>
"""


def service_ld(name, desc, path):
    return """{
  "@context":"https://schema.org",
  "@type":"Service",
  "name":"%s",
  "description":"%s",
  "url":"https://makersolve.com/%s",
  "serviceType":"%s",
  "areaServed":{"@type":"Country","name":"Italia"},
  "provider":{
    "@type":"ProfessionalService",
    "name":"MakerSolve",
    "url":"https://makersolve.com/",
    "telephone":"+39 %s",
    "email":"%s",
    "address":{"@type":"PostalAddress","addressLocality":"Mirandola","addressRegion":"MO","addressCountry":"IT"}
  }
}""" % (name, desc, path, name, TEL, MAIL)


# ------------------------------------------------------------------- PAGINE

PAGES = []

# ---------------------------------------------------------- 1. CHI SONO
PAGES.append(dict(
    path="chi-siamo/",
    nav_active="chi-siamo",
    title="Chi sono &mdash; Giulio Corazzari | MakerSolve Mirandola (MO)",
    ogtitle="Chi sono &mdash; MakerSolve",
    desc="Progettista meccanico con officina propria a Mirandola (MO): progettazione CAD, reverse engineering e stampa 3D di componenti su misura per aziende. Interlocutore tecnico diretto.",
    hero=hero(
        "Chi sono",
        "Progettazione e produzione<br><span class=\"grad\">seguite dalla stessa persona.</span>",
        "Sono Giulio Corazzari e MakerSolve &egrave; la mia officina di progettazione meccanica e stampa 3D. "
        "Chi risponde al telefono &egrave; la stessa persona che redige il modello CAD e segue la produzione del componente.",
        "Chi sono",
        note="Interlocutore tecnico unico &middot; Risposta in 24/48 ore",
    ),
    body="\n\n".join([
        section(
            sec_head("Approccio", "Meccanica applicata, non esercizio di stile.",
                     "Il criterio di valutazione non &egrave; l'eleganza del modello 3D, ma il comportamento del componente una volta montato e messo in funzione.")
            + cards([
                ("Il requisito precede la geometria",
                 "La prima analisi non riguarda la forma del pezzo, ma la sua funzione: quale carico sostiene, in quale ambiente opera e quali sono le conseguenze di un cedimento. Materiale, spessori e processo discendono da queste risposte."),
                ("Un solo interlocutore tecnico",
                 "Non esiste un passaggio commerciale che raccoglie la richiesta e un tecnico che la interpreta. Il confronto avviene direttamente con chi esegue il lavoro, senza dispersione di informazioni."),
                ("Valutazione preventiva dei limiti",
                 "Quando la stampa 3D non &egrave; la tecnologia appropriata, o la richiesta esula dall'ambito di competenza, la valutazione lo segnala in fase preliminare anzich&eacute; a lavorazione avviata."),
            ], cols=3, dark=True),
            cls="",
        ),
        section(
            sec_head("Contesto operativo", "Un'officina a Mirandola, in provincia di Modena.",
                     "L'attivit&agrave; si svolge in un territorio in cui la meccanica di precisione rappresenta lo standard di riferimento quotidiano.")
            + specs([
                ("Ambito di attivit&agrave;", "Progettazione CAD di componenti su misura, reverse engineering da campione fisico, attrezzature di reparto, prototipi funzionali e integrazione di piccola elettronica."),
                ("Destinatari", "Aziende, officine, reparti di manutenzione e uffici tecnici. Le richieste di privati vengono valutate quando presentano un contenuto tecnico definito."),
                ("Modalit&agrave; di contatto", "Telefono, posta elettronica o modulo di richiesta. Per la zona di Mirandola &egrave; possibile il ritiro diretto; per il resto d'Italia la lavorazione procede su file e fotografie, con spedizione del componente finito."),
                ("Ambiti esclusi", "Parti di sicurezza, componenti strutturali critici e dispositivi soggetti a certificazione. Su questi ambiti &egrave; possibile un supporto in fase di studio, non la produzione."),
            ]),
            cls="paper-2",
        ),
        MARQUEE,
        section(
            sec_head("Metodo di lavoro", "Quattro fasi, applicate a ogni commessa.")
            + pain([
                ("FASE 01", "Acquisizione dei dati", "Fotografie, misure, campione fisico o file esistente. Anche una documentazione parziale &egrave; sufficiente ad avviare la valutazione: le informazioni mancanti vengono ricostruite in fase di rilievo."),
                ("FASE 02", "Valutazione di fattibilit&agrave;", "Entro 24/48 ore ricevi l'esito tecnico: fattibilit&agrave;, materiale indicato e condizioni di realizzazione. In caso di esito negativo, la motivazione tecnica viene esplicitata."),
                ("FASE 03", "Progettazione e produzione", "Modellazione CAD e realizzazione del componente. Sui pezzi di maggiore complessit&agrave; il modello viene condiviso prima della produzione, per consentire correzioni a monte anzich&eacute; su un pezzo gi&agrave; realizzato."),
                ("FASE 04", "Validazione e consegna", "Il componente viene verificato in funzione. Eventuali scostamenti comportano una correzione del modello e una nuova realizzazione: &egrave; il vantaggio di una produzione che non richiede stampi."),
            ]),
        ),
    ]),
    cta=cta_band("Hai un componente da valutare?",
                 "Invia una fotografia e le misure di massima: ricevi entro 24/48 ore una valutazione di fattibilit&agrave;, senza costi n&eacute; impegno."),
    jsonld="""{
  "@context":"https://schema.org",
  "@type":"AboutPage",
  "url":"https://makersolve.com/chi-siamo/",
  "mainEntity":{
    "@type":"Person",
    "name":"Giulio Corazzari",
    "jobTitle":"Progettista meccanico",
    "worksFor":{"@type":"ProfessionalService","name":"MakerSolve","url":"https://makersolve.com/"},
    "knowsAbout":["Progettazione CAD","Reverse engineering","Stampa 3D FDM","Stampa 3D a resina","Prototipazione rapida"]
  }
}""",
))

# ---------------------------------------------------------- 2. MATERIALI
PAGES.append(dict(
    path="materiali/",
    nav_active="materiali",
    title="Materiali stampa 3D: PLA, PETG, ASA, ABS, TPU | Mirandola e Modena",
    ogtitle="Materiali &mdash; MakerSolve",
    desc="Selezione del materiale di stampa 3D in base a carico, temperatura di esercizio ed esposizione ambientale: PLA, PETG, ASA, ABS, TPU, nylon caricato e resina. Mirandola (MO).",
    hero=hero(
        "Materiali",
        "Selezione del materiale<br><span class=\"grad\">in base all'impiego.</span>",
        "Il materiale appropriato non &egrave; quello di costo superiore, ma quello adeguato al carico previsto, "
        "alla temperatura di esercizio e all'ambiente in cui il componente opera. Un nylon caricato fibra su un pezzo scarico &egrave; solo un costo aggiuntivo.",
        "Materiali",
        img="gen-materials",
        note="Materiali speciali reperibili su richiesta",
    ),
    body="\n\n".join([
        section(
            sec_head("Criteri di selezione", "Quattro parametri determinanti.",
                     "Indicare questi elementi nella richiesta riduce sensibilmente i tempi di valutazione.")
            + cards([
                ("Entit&agrave; del carico", "Un componente estetico e uno sottoposto a sollecitazione non condividono alcun parametro: variano materiale, spessori, orientamento di stampa e percentuale di riempimento."),
                ("Temperatura di esercizio", "In prossimit&agrave; di un motore, di una fonte di calore o all'interno di un veicolo esposto al sole, il PLA &egrave; escluso e con esso buona parte delle alternative."),
                ("Esposizione ambientale", "L'esposizione a raggi UV e agenti atmosferici restringe la scelta e orienta verso l'ASA."),
                ("Comportamento elastico", "Se il componente deve deformarsi e recuperare la posizione originale si adotta il TPU; se deve mantenere la geometria, il requisito &egrave; opposto."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Disponibilit&agrave;", "Materiali trattati e relativo impiego.",
                     "Nessuno di questi materiali &egrave; superiore in assoluto: ciascuno risponde a un requisito specifico.")
            + specs([
                ("PLA", "Processo di stampa semplice e buona definizione superficiale. Indicato per verifiche dimensionali, modelli e componenti estetici. <b>Non presenta resistenza termica</b>: la deformazione avviene gi&agrave; alle temperature raggiunte in un abitacolo esposto al sole."),
                ("PETG", "Superiore al PLA per tenacit&agrave; e minore fragilit&agrave;. Rappresenta la scelta di riferimento per supporti, contenitori e componenti funzionali non esposti a temperature elevate."),
                ("ASA", "Resistente a raggi UV e agenti atmosferici. Materiale indicato per qualunque componente destinato a permanenza stabile in esterno."),
                ("ABS", "Buona resistenza termica e meccanica, adatto a componenti tecnici, carter e scocche operanti in ambienti caldi."),
                ("TPU", "Materiale flessibile ed elastico, impiegato per protezioni, piedini antivibranti, paracolpi, inserti morbidi e guarnizioni non critiche."),
                ("Nylon caricato fibra di carbonio (CF)", "Rigidit&agrave; elevata e buona stabilit&agrave; dimensionale. Indicato per staffe e attrezzature che devono mantenere la quota sotto carico."),
                ("Nylon caricato fibra di vetro (GF)", "Impiego analogo al CF, con un diverso rapporto tra rigidit&agrave;, tenacit&agrave; e costo."),
                ("Resina", "Stampa a resina per dettagli fini e geometrie di piccole dimensioni, oltre i limiti del processo FDM. Da considerare la maggiore fragilit&agrave;: non &egrave; un materiale destinato al carico."),
            ]),
            cls="paper-2",
        ),
        section(
            pain([
                ("CRITERIO", "Non esiste un materiale universale",
                 "Un materiale di costo superiore non &egrave; automaticamente pi&ugrave; adatto: deve risultare coerente con il componente, la geometria e l'impiego effettivo. Quando il PETG soddisfa il requisito, la proposta &egrave; il PETG."),
                ("LIMITE", "Il materiale non compensa una geometria inadeguata",
                 "Un componente progettato in modo non corretto cede anche in nylon caricato. La priorit&agrave; &egrave; il disegno &mdash; orientamento, raccordi, spessori, distribuzione degli sforzi &mdash; e solo successivamente la scelta del materiale."),
            ]),
        ),
    ]),
    cta=cta_band("Non hai definito il materiale?",
                 "&Egrave; una condizione ordinaria e rientra nell'attivit&agrave; di valutazione. Descrivi le condizioni di esercizio del componente e ricevi l'indicazione tecnica."),
    jsonld=service_ld("Stampa 3D con materiali tecnici",
                      "Selezione del materiale di stampa 3D in base a carico, temperatura di esercizio e ambiente: PLA, PETG, ASA, ABS, TPU, nylon caricato fibra e resina.",
                      "materiali/"),
))

# ---------------------------------------------------------- 3. PORTFOLIO
PAGES.append(dict(
    path="portfolio/",
    nav_active="portfolio",
    title="Lavori: casi reali di CAD e stampa 3D | Mirandola e Modena",
    ogtitle="Lavori &mdash; MakerSolve",
    desc="Casi reali di progettazione e stampa 3D: scocca ricostruita attorno a una PCB esistente, posaggio da banco per tubicini flessibili, dima universale per semimanubri da competizione.",
    hero=hero(
        "Lavori",
        "Casi reali di progettazione<br><span class=\"grad\">e produzione.</span>",
        "MakerSolve &egrave; una realt&agrave; recente e non dispone ancora di un portfolio di commesse aziendali. "
        "I lavori riportati di seguito sono interventi effettivamente realizzati in officina, descritti nel loro svolgimento reale.",
        "Lavori",
        img="gen-exploded",
        note="Casi reali &middot; Nessuna immagine di repertorio",
    ),
    body="\n\n".join([
        section(
            """    <div class="work">
      <article class="work-item rv">
        <div class="work-img"><img src="/assets/scocca-telecomando-cancello-stampa-3d-mirandola.png" alt="Scocca per telecomando cancello ricostruita e stampata in 3D" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Reverse engineering</span>
          <h3>Scocca ricostruita attorno a una PCB esistente</h3>
          <p>Involucro originale danneggiato, elettronica ancora funzionante. La scheda &egrave; stata rilevata dimensionalmente e attorno a essa &egrave; stata progettata una nuova scocca, comprensiva di pulsanti, foro portachiavi e nervature interne per il bloccaggio della PCB.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="1">
        <div class="work-img"><img src="/assets/dima.png" alt="Posaggio da banco per tubicini flessibili" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Attrezzatura di reparto</span>
          <h3>Posaggio da banco per tubicini flessibili</h3>
          <p>Attrezzatura per il mantenimento in posizione di tubi di piccolo diametro durante assemblaggio e collaudo. L'obiettivo era rendere ripetibile un posizionamento senza ricorrere alla commissione di un'attrezzatura dedicata.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="2">
        <div class="work-img"><img src="/assets/dima-semimanubri-moto.png" alt="Dima universale per semimanubri da competizione" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Prodotto MakerSolve</span>
          <h3>Dima universale per semimanubri</h3>
          <p>Attrezzatura per il controllo dell'apertura dei semimanubri su motociclette da competizione. La geometria &egrave; stata studiata per l'adattamento a modelli differenti, in sostituzione della misurazione manuale.</p>
        </div>
      </article>
    </div>
"""),
        section(
            sec_head("Elemento comune", "Il percorso seguito in ogni intervento.")
            + pain([
                ("01 &middot; PROBLEMA", "Un componente assente o non funzionante",
                 "Un pezzo danneggiato, un'attrezzatura non disponibile a catalogo, oppure un'operazione la cui riuscita dipende eccessivamente dalla manualit&agrave; dell'operatore."),
                ("02 &middot; VINCOLI", "Rilievo di misure, ingombri e condizioni",
                 "Acquisizione di quote e vincoli: accoppiamenti richiesti, spazio disponibile, sollecitazioni previste e ambiente di esercizio."),
                ("03 &middot; CAD", "Il modello discende dai requisiti",
                 "La geometria deriva dai vincoli rilevati e non da un'impostazione estetica. Ogni raccordo e ogni spessore rispondono a una motivazione tecnica definita."),
                ("04 &middot; VALIDAZIONE", "Verifica in condizioni di esercizio",
                 "Il componente viene montato e provato. Eventuali scostamenti comportano una correzione del modello e una nuova realizzazione: senza stampi, l'iterazione ha un costo contenuto."),
            ]),
            cls="",
        ),
        section(
            sec_head("Ambito", "Tipologie di intervento seguite.",
                     "Se la tua esigenza rientra in una di queste categorie, l'ambito &egrave; quello corretto.")
            + cards([
                ("Scocche e contenitori", "Involucri su misura per elettronica esistente: alloggiamenti per PCB, passaggi cavo, accessi per connettori e organi di comando."),
                ("Supporti e adattatori", "Staffe, raccordi e interfacce tra componenti non progettati per essere accoppiati tra loro."),
                ("Reverse engineering funzionale", "Ricostruzione di componenti a partire dal campione fisico, anche danneggiato: il rilievo viene effettuato sulle porzioni integre."),
            ], cols=3),
            cls="paper",
        ),
    ]),
    cta=cta_band("La tua esigenza rientra in questi casi?",
                 "Invia una fotografia e le misure di massima: ricevi entro 24/48 ore l'esito di fattibilit&agrave; e l'indicazione del materiale."),
    jsonld="""{
  "@context":"https://schema.org",
  "@type":"CollectionPage",
  "name":"Lavori — MakerSolve",
  "url":"https://makersolve.com/portfolio/",
  "description":"Casi reali di progettazione meccanica, reverse engineering e stampa 3D."
}""",
))

# ---------------------------------------------------------- 4. STAMPA 3D PERSONALIZZATA
PAGES.append(dict(
    path="stampa-3d-personalizzata/",
    nav_active="",
    title="Stampa 3D personalizzata su misura a Mirandola e Modena | MakerSolve",
    ogtitle="Stampa 3D personalizzata &mdash; MakerSolve",
    desc="Stampa 3D di componenti e oggetti su misura, con o senza file 3D. Verifica preventiva del file, consulenza su materiale e orientamento di stampa. Mirandola (MO).",
    hero=hero(
        "Stampa 3D personalizzata",
        "Stampa 3D su misura,<br><span class=\"grad\">con verifica preventiva del file.</span>",
        "L'invio di un file a una macchina &egrave; un'operazione elementare. La differenza risiede nella verifica che la precede: "
        "spessori, orientamento di stampa, punti critici e idoneit&agrave; del materiale all'impiego previsto. &Egrave; il passaggio che evita di realizzare due volte lo stesso componente.",
        "Stampa 3D personalizzata",
    ),
    body="\n\n".join([
        section(
            sec_head("Punto di partenza", "Con file 3D o senza.")
            + cards([
                ("Disponi gi&agrave; del file 3D",
                 "Sono accettati i formati STL, STEP, 3MF e OBJ. Prima della produzione vengono verificati scala, spessori minimi, orientamento e criticit&agrave; geometriche, con indicazione delle eventuali modifiche opportune. Gli errori del file emergono in fase preliminare e non a componente consegnato."),
                ("Non disponi del file",
                 "La modellazione CAD rientra nel servizio e pu&ograve; partire da uno schizzo, da una fotografia con riferimento dimensionale o dal componente fisico. Non &egrave; necessaria alcuna competenza di modellazione per ottenere un pezzo su misura."),
            ], cols=2),
            cls="paper",
        ),
        MARQUEE,
        section(
            sec_head("Realizzazioni", "Dal ricambio all'attrezzatura di reparto.")
            + cards([
                ("Ricambi e componenti non reperibili", "Pezzi fuori produzione o privi di fornitore, ricostruiti a partire dall'originale o dalle porzioni residue."),
                ("Supporti ed espositori", "Basi, sostegni, staffe ed espositori progettati su un oggetto specifico anzich&eacute; adattati da un prodotto generico."),
                ("Oggetti personalizzati", "Targhette, loghi tridimensionali e componenti di piccole dimensioni realizzati su misura."),
                ("Adattatori", "Raccordi e interfacce tra componenti non predisposti all'accoppiamento."),
                ("Prototipi", "Componenti destinati alla prova sul campo per la verifica di ingombri, accoppiamenti ed ergonomia."),
                ("Piccoli lotti", "Serie ridotte, per le quali l'attrezzaggio di uno stampo non presenta convenienza economica."),
            ], cols=3),
            cls="paper-2",
        ),
        section(
            pain([
                ("INFORMAZIONE RICHIESTA", "L'impiego effettivo determina le scelte tecniche",
                 "La destinazione del componente &mdash; estetica, funzionale o provvisoria &mdash; determina materiale, spessori e orientamento di stampa. Indicarla nella richiesta &egrave; l'informazione di maggiore utilit&agrave; ai fini della valutazione."),
                ("LIMITE", "La stampa 3D non &egrave; sempre la tecnologia appropriata",
                 "Quando una lavorazione CNC, un taglio laser o un ricambio commerciale risultano pi&ugrave; adeguati, l'indicazione viene fornita in fase di valutazione, prima di qualsiasi impegno di spesa."),
            ]),
        ),
    ]),
    cta=cta_band("Disponi di un file o di una sola idea?",
                 "In entrambi i casi la valutazione pu&ograve; procedere. Invia il materiale disponibile e ricevi una risposta entro 24/48 ore."),
    jsonld=service_ld("Stampa 3D personalizzata",
                      "Stampa 3D di oggetti e componenti su misura, con o senza file 3D, con verifica preventiva di file, materiale e orientamento.",
                      "stampa-3d-personalizzata/"),
))

# ---------------------------------------------------------- 5. PROGETTAZIONE CAD
PAGES.append(dict(
    path="servizi/progettazione-cad/",
    nav_active="servizi",
    title="Progettazione CAD di componenti su misura | Mirandola e Modena",
    ogtitle="Progettazione CAD &mdash; MakerSolve",
    desc="Modellazione CAD di componenti meccanici su misura a partire da idea, schizzo, fotografia o campione fisico. Consegna in formato STEP. Mirandola (MO), lavorazioni in tutta Italia.",
    hero=hero(
        "Progettazione CAD",
        "Progettazione CAD<br><span class=\"grad\">di componenti su misura.</span>",
        "Realizzo il disegno di componenti custom a partire dagli elementi disponibili: un'idea, uno schizzo, una fotografia quotata o il campione fisico. "
        "Il modello viene impostato per essere prodotto, verificato, corretto e utilizzato.",
        "Progettazione CAD",
    ),
    body="\n\n".join([
        section(
            sec_head("Dati di partenza", "Elementi da cui &egrave; possibile procedere.",
                     "Non &egrave; richiesta documentazione tecnica formale. &Egrave; necessario che risulti definita la funzione del componente.")
            + cards([
                ("Idea o schizzo", "Anche redatto a mano. Su questa base vengono definiti congiuntamente vincoli e ingombri."),
                ("Fotografie e misure", "Una fotografia con calibro o metro in campo fornisce il riferimento di scala. Le quote critiche vengono definite in fase di analisi."),
                ("Campione fisico", "Il componente originale, anche danneggiato: il rilievo avviene sulle porzioni integre e la parte mancante viene ricostruita."),
                ("File esistente", "File STEP, STL o 3MF da modificare, correggere o adattare a un nuovo impiego."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Applicazioni", "Casi ricorrenti.")
            + pain([
                ("CASO 01", "Scocche e contenitori", "Involucri progettati attorno a un'elettronica esistente: alloggiamento della scheda, passaggi cavo, accessi per connettori e organi di comando, sistemi di ritegno dei componenti."),
                ("CASO 02", "Supporti e adattatori", "Interfacce tra componenti non predisposti all'accoppiamento, con definizione dei fissaggi e verifica degli ingombri."),
                ("CASO 03", "Prototipi funzionali", "Modelli destinati alla prova sul campo, all'iterazione e alla correzione prima del consolidamento della geometria."),
                ("CASO 04", "Documentazione tecnica trasferibile", "Un modello 3D corretto e un file STEP utilizzabili presso altri fornitori, anche qualora la produzione non venga affidata a MakerSolve."),
            ]),
        ),
        section(
            sec_head("Consegna", "Elementi forniti.")
            + specs([
                ("Modello 3D", "Il componente modellato secondo i requisiti concordati e verificato per il processo produttivo previsto."),
                ("File STEP", "Formato neutro, apribile da qualunque sistema CAD. Il file &egrave; di tua propriet&agrave; e pu&ograve; essere utilizzato presso terzi senza vincoli."),
                ("Revisioni", "Le correzioni derivanti dalla prova del prototipo rientrano nel percorso: il modello viene aggiornato, non ricostruito da principio."),
                ("Tolleranze", "<b>La lavorazione si colloca nell'ordine del millimetro.</b> Il decimo di millimetro, in processo FDM, non rientra tra i risultati garantiti: qualora il componente lo richieda, l'indicazione viene fornita prima dell'avvio."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai un componente da disegnare?",
                 "Invia il materiale disponibile, anche un solo schizzo. Ricevi entro 24/48 ore una valutazione di fattibilit&agrave;."),
    jsonld=service_ld("Progettazione CAD",
                      "Modellazione CAD di componenti meccanici su misura a partire da idea, schizzo, fotografia, quote o campione fisico, con consegna in formato STEP.",
                      "servizi/progettazione-cad/"),
))

# ---------------------------------------------------------- 6. REVERSE ENGINEERING
PAGES.append(dict(
    path="servizi/reverse-engineering/",
    nav_active="servizi",
    title="Reverse engineering pezzi rotti e senza disegno | Mirandola e Modena",
    ogtitle="Reverse engineering &mdash; MakerSolve",
    desc="Ricostruzione CAD di componenti a partire dal campione fisico, anche danneggiato o incompleto: ricambi non più reperibili, scocche, carter. Mirandola (MO).",
    hero=hero(
        "Reverse engineering",
        "Ricostruzione di componenti<br><span class=\"grad\">non pi&ugrave; reperibili.</span>",
        "Ricostruisco componenti a partire dal campione fisico, da una fotografia o dalle porzioni residue di un originale danneggiato. "
        "Quando il ricambio &egrave; fuori produzione e il fornitore non &egrave; raggiungibile, questa &egrave; frequentemente l'unica via per rimettere in servizio una macchina.",
        "Reverse engineering",
    ),
    body="\n\n".join([
        section(
            sec_head("Applicabilit&agrave;", "Quattro casi ricorrenti.")
            + pain([
                ("CASO 01", "Ricambio non reperibile", "Componente fuori produzione, fornitore non raggiungibile, oppure disponibile esclusivamente all'interno di un assieme di costo sproporzionato rispetto al pezzo necessario."),
                ("CASO 02", "Componente danneggiato", "Il rilievo viene effettuato sulle porzioni integre e la parte mancante &egrave; ricostruita per continuit&agrave; geometrica. Un componente rotto conserva quasi sempre informazione sufficiente."),
                ("CASO 03", "Scocche e carter", "Gusci e coperture da riprodurre o da adattare a componenti interni nel frattempo modificati."),
                ("CASO 04", "Riproduzione con modifica", "Non una copia conforme ma una versione corretta: fissaggi differenti, rinforzo nella zona di cedimento, riduzione degli ingombri."),
            ]),
        ),
        section(
            sec_head("Processo", "Fasi della ricostruzione.")
            + cards([
                ("Analisi del componente", "Vengono determinati il funzionamento, i punti di accoppiamento e le cause del cedimento. In assenza di questa fase si replica anche il difetto originale."),
                ("Rilievo dimensionale", "Misurazione diretta di ingombri, diametri, interassi e spessori, con attenzione specifica alle quote di accoppiamento."),
                ("Ricostruzione CAD", "Il modello 3D viene generato dalle quote rilevate, con le correzioni necessarie nei punti in cui la geometria originale costituiva l'elemento debole."),
                ("Prototipo e correzione", "Realizzazione, prova in sede e correzione. La prima versione ha funzione di validazione degli accoppiamenti e non carattere definitivo."),
            ], cols=4, dark=True),
        ),
        section(
            pain([
                ("ESCLUSIONE", "Non applicabile a parti critiche",
                 "Il servizio non viene proposto per componenti strutturali critici, parti di sicurezza o applicazioni soggette a certificazione. Un componente il cui cedimento comporti rischio per persone o impianti richiede un percorso di qualifica non coperto da questa officina."),
                ("VALUTAZIONE", "La riproduzione non &egrave; sempre la soluzione",
                 "Se l'originale era realizzato in metallo e operava sotto carico, la riproduzione in materiale polimerico non risolve il problema ma ne posticipa la manifestazione. In tali casi l'indicazione viene esplicitata e si valutano soluzioni alternative."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Hai un componente da ricostruire?",
                 "Invia una fotografia del pezzo, anche danneggiato, con un riferimento dimensionale in campo. Ricevi entro 24/48 ore l'esito sulla ricostruibilit&agrave;."),
    jsonld=service_ld("Reverse engineering",
                      "Ricostruzione del modello CAD di un componente a partire dal campione fisico, anche danneggiato o incompleto, per ricambi non più reperibili.",
                      "servizi/reverse-engineering/"),
))

# ---------------------------------------------------------- 7. PROTOTIPAZIONE RAPIDA
PAGES.append(dict(
    path="servizi/prototipazione-rapida/",
    nav_active="servizi",
    title="Prototipazione rapida con CAD e stampa 3D | Mirandola e Modena",
    ogtitle="Prototipazione rapida &mdash; MakerSolve",
    desc="Prototipi funzionali per la verifica di ingombri, accoppiamenti e funzione prima dell'investimento in attrezzature definitive. Progettazione CAD e stampa 3D. Mirandola (MO).",
    hero=hero(
        "Prototipazione rapida",
        "Prototipi funzionali<br><span class=\"grad\">per la validazione tecnica.</span>",
        "Un prototipo non ha finalit&agrave; estetiche: deve fornire una risposta verificabile. Il componente entra nello spazio disponibile, si accoppia, sostiene il carico, risulta utilizzabile. "
        "Realizzo prototipi per la verifica di forma, ingombri, fori, fissaggi e montaggio prima che le decisioni comportino costi rilevanti.",
        "Prototipazione rapida",
    ),
    body="\n\n".join([
        section(
            sec_head("Finalit&agrave;", "Quattro verifiche rese possibili da un prototipo.")
            + cards([
                ("Verifica di accoppiamento", "Il componente rientra nello spazio disponibile, i fori risultano in asse e gli interassi trovano riscontro nella realt&agrave; e non solo sul disegno."),
                ("Prova funzionale", "Il comportamento del componente viene verificato in condizioni di montaggio e sollecitazione, non a pezzo isolato."),
                ("Iterazione rapida", "Correzione del modello e nuova realizzazione. In assenza di stampi, una modifica alla terza revisione comporta un costo contenuto."),
                ("Preparazione all'industrializzazione", "Una geometria validata sul campo costituisce la base per valutare consapevolmente le modalit&agrave; di produzione di serie."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Destinatari", "Contesti di maggiore utilit&agrave;.")
            + pain([
                ("PROFILO 01", "Uffici tecnici e R&amp;D", "Strutture che devono validare una soluzione prima di impegnare capitale in stampi o attrezzature definitive, con necessit&agrave; di iterare in giorni anzich&eacute; in settimane."),
                ("PROFILO 02", "Manutenzione e officine", "Contesti in cui &egrave; necessario ripristinare una funzionalit&agrave; e verificare una soluzione prima di adottarla stabilmente."),
                ("PROFILO 03", "Sviluppo prodotto", "Attivit&agrave; che richiedono la verifica diretta di ergonomia, ingombri e percezione d'uso prima del consolidamento del progetto."),
                ("PROFILO 04", "Presentazione interna del progetto", "Un componente fisico disponibile in riunione fornisce elementi di valutazione superiori a qualsiasi rappresentazione grafica."),
            ]),
        ),
        section(
            sec_head("Livelli di servizio", "Estensione dell'intervento.")
            + specs([
                ("Solo prototipo", "Il componente destinato alla prova, realizzato nel materiale pi&ugrave; adatto alla verifica prevista."),
                ("Prototipo e revisione CAD", "Il componente e il modello aggiornato con le correzioni emerse dalla prova: quanto viene consegnato &egrave; una geometria gi&agrave; validata."),
                ("Prototipo e componente definitivo", "A validazione avvenuta si procede alla realizzazione della versione definitiva, eventualmente in materiale differente da quello impiegato per la prova."),
                ("Materiali di riferimento", "PLA per le verifiche esclusivamente dimensionali, PETG e ABS/ASA per le prove funzionali, nylon caricato fibra dove &egrave; richiesta rigidit&agrave;, TPU per le parti soggette a flessione."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai una soluzione da validare?",
                 "Con o senza file 3D. Descrivi la funzione richiesta al componente e ricevi una risposta entro 24/48 ore."),
    jsonld=service_ld("Prototipazione rapida",
                      "Prototipi funzionali con CAD e stampa 3D per verificare forma, ingombri, accoppiamenti e funzione prima della produzione definitiva.",
                      "servizi/prototipazione-rapida/"),
))

# ---------------------------------------------------------- 8. COMPONENTI CUSTOM
PAGES.append(dict(
    path="servizi/componenti-custom/",
    nav_active="servizi",
    title="Componenti su misura: supporti, staffe, dime | Mirandola e Modena",
    ogtitle="Componenti custom &mdash; MakerSolve",
    desc="Componenti su misura quando il pezzo commerciale non esiste, non combacia o non presenta convenienza: supporti, staffe, adattatori, guide, carter, dime e piccoli lotti.",
    hero=hero(
        "Componenti custom",
        "Supporti, staffe, adattatori<br><span class=\"grad\">e dime su misura.</span>",
        "Realizzo componenti custom quando il pezzo commerciale non esiste, non combacia, presenta un costo sproporzionato o richiede una modifica specifica: "
        "supporti, staffe, adattatori, guide, carter, dime, scocche e piccoli lotti.",
        "Componenti custom",
    ),
    body="\n\n".join([
        section(
            sec_head("Tipologie", "Quattro famiglie ricorrenti.")
            + cards([
                ("Supporti e fissaggi", "Staffe e sostegni progettati sull'oggetto reale e sul punto di ancoraggio effettivamente disponibile, non adattati da un prodotto generico."),
                ("Adattatori", "Interfacce tra componenti non predisposti all'accoppiamento: variazione di attacco, di passo, di diametro o di orientamento."),
                ("Scocche e coperture", "Involucri e carter attorno a componenti esistenti, con accessi, passaggi cavo e sistemi di ritegno definiti sul contenuto effettivo."),
                ("Dime e ausili di reparto", "Attrezzature che rendono ripetibile un'operazione la cui riuscita dipende attualmente dalla manualit&agrave; dell'operatore."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Convenienza", "Condizioni di applicabilit&agrave; economica.")
            + pain([
                ("CONDIZIONE 01", "Ricambio non reperibile", "Componente fuori produzione, oppure commercializzato esclusivamente all'interno di un assieme di costo largamente superiore al pezzo necessario."),
                ("CONDIZIONE 02", "Geometria non corrispondente", "Il prodotto commerciale esiste ma non risulta compatibile: attacchi non conformi, ingombri eccedenti, interassi non corrispondenti."),
                ("CONDIZIONE 03", "Necessit&agrave; di verifica preliminare", "La soluzione non &egrave; ancora consolidata e richiede validazione su un componente reale prima dell'adozione definitiva."),
                ("CONDIZIONE 04", "Quantit&agrave; ridotte", "Da un pezzo a poche decine: volumi per i quali l'attrezzaggio di uno stampo &egrave; economicamente escluso."),
            ]),
        ),
        section(
            pain([
                ("CRITERIO", "La stampa 3D non &egrave; sempre la soluzione appropriata",
                 "Quando una lavorazione CNC, un taglio laser, un ricambio commerciale o una soluzione costruttivamente pi&ugrave; semplice risultano pi&ugrave; adeguati, l'indicazione viene fornita in fase di valutazione, anche quando comporta la rinuncia alla commessa."),
                ("QUANTIT&Agrave;", "Dal pezzo singolo alla piccola serie",
                 "Il limite superiore dipende dalla geometria e dal tempo macchina e viene definito sul componente specifico. Qualora i volumi rendano conveniente lo stampaggio, l'indicazione viene fornita anzich&eacute; procedere con un costo superiore."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Ti serve un componente che non esiste?",
                 "Descrivi il problema tecnico, non la soluzione: l'impostazione progettuale rientra nel servizio. Risposta entro 24/48 ore."),
    jsonld=service_ld("Componenti su misura",
                      "Progettazione e produzione di componenti custom: supporti, staffe, adattatori, guide, carter, dime, scocche e piccoli lotti.",
                      "servizi/componenti-custom/"),
))


# ------------------------------------------------------------------- build

def main():
    written = []
    for p in PAGES:
        html = PAGE % dict(
            title=p["title"],
            ogtitle=p["ogtitle"],
            desc=p["desc"],
            path=p["path"],
            nav=nav(p["nav_active"]),
            hero=p["hero"],
            body=p["body"],
            cta=p["cta"],
            footer=FOOTER,
            jsonld=p["jsonld"],
        )
        out = os.path.join(ROOT, p["path"].replace("/", os.sep), "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, "w", encoding="utf-8").write(html)
        written.append(os.path.relpath(out, ROOT).replace(os.sep, "/"))

    for w in written:
        print("scritto  %s" % w)
    print("\n%d pagine generate." % len(written))


if __name__ == "__main__":
    main()
