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
        a('/chi-siamo/', 'Chi siamo', 'chi-siamo'),
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
        <a href="/chi-siamo/">Chi siamo</a>
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

# ---------------------------------------------------------- 1. CHI SIAMO
PAGES.append(dict(
    path="chi-siamo/",
    nav_active="chi-siamo",
    title="Chi siamo &mdash; MakerSolve | Progettazione e stampa 3D a Mirandola",
    ogtitle="Chi siamo &mdash; MakerSolve",
    desc="MakerSolve: officina di progettazione meccanica e stampa 3D a Mirandola (MO). Progettazione CAD, reverse engineering e componenti su misura per aziende. Un solo referente tecnico.",
    hero=hero(
        "Chi siamo",
        "Competenza tecnica,<br><span class=\"grad\">senza intermediari.</span>",
        "MakerSolve &egrave; l'officina di progettazione meccanica e stampa 3D fondata da Giulio Corazzari a Mirandola. "
        "Chi risponde al telefono &egrave; chi redige il modello CAD e segue la produzione.",
        "Chi siamo",
        note="Un solo referente tecnico &middot; Risposta in 24/48 ore",
    ),
    body="\n\n".join([
        section(
            sec_head("Il nostro approccio", "La funzione prima della forma.",
                     "Valutiamo un componente da come si comporta in esercizio, non da come appare a schermo.")
            + cards([
                ("Partiamo dal requisito",
                 "Carico, ambiente, conseguenze di un cedimento. Materiale e geometria discendono da qui."),
                ("Un solo interlocutore",
                 "Nessun passaggio commerciale tra la tua richiesta e chi la esegue. Le informazioni non si perdono."),
                ("Dichiariamo i limiti",
                 "Quando la stampa 3D non &egrave; la tecnologia adatta, lo comunichiamo in fase preliminare."),
            ], cols=3, dark=True),
            cls="",
        ),
        section(
            sec_head("La nostra officina", "Mirandola, nel distretto meccanico modenese.",
                     "Operiamo in un territorio dove la precisione &egrave; lo standard di riferimento.")
            + specs([
                ("Cosa realizziamo", "Progettazione CAD di componenti su misura, reverse engineering da campione fisico, attrezzature di reparto, prototipi funzionali e integrazione di piccola elettronica."),
                ("A chi ci rivolgiamo", "Aziende, officine, reparti di manutenzione e uffici tecnici. Valutiamo anche richieste di privati con contenuto tecnico definito."),
                ("Come lavoriamo", "Telefono, posta elettronica o modulo di richiesta. Ritiro diretto in zona Mirandola; per il resto d'Italia lavoriamo su file e documentazione fotografica, con spedizione del componente finito."),
                ("Cosa non trattiamo", "Parti di sicurezza, componenti strutturali critici e dispositivi soggetti a certificazione. Su questi ambiti offriamo supporto in fase di studio, non produzione."),
            ]),
            cls="paper-2",
        ),
        MARQUEE,
        section(
            sec_head("Il nostro metodo", "Quattro fasi, su ogni commessa.")
            + pain([
                ("FASE 01", "Acquisizione", "Fotografie, misure, campione fisico o file esistente. Anche una documentazione parziale &egrave; sufficiente ad avviare la valutazione."),
                ("FASE 02", "Fattibilit&agrave;", "Entro 24/48 ore ricevi l'esito tecnico: fattibilit&agrave;, materiale e condizioni. In caso negativo, indichiamo la motivazione."),
                ("FASE 03", "Progettazione e produzione", "Modellazione CAD e realizzazione. Sui componenti complessi condividiamo il modello prima della produzione."),
                ("FASE 04", "Validazione", "Verifica in condizioni di esercizio. Eventuali scostamenti comportano correzione del modello e nuova realizzazione: nessuno stampo, nessun costo di riattrezzaggio."),
            ]),
        ),
    ]),
    cta=cta_band("Hai un componente da valutare?",
                 "Inviaci una fotografia e le misure di massima. Ricevi l'esito di fattibilit&agrave; entro 24/48 ore, senza costi n&eacute; vincoli."),
    jsonld="""{
  "@context":"https://schema.org",
  "@type":"AboutPage",
  "url":"https://makersolve.com/chi-siamo/",
  "mainEntity":{
    "@type":"ProfessionalService",
    "name":"MakerSolve",
    "url":"https://makersolve.com/",
    "founder":{"@type":"Person","name":"Giulio Corazzari"},
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
        "Il materiale giusto<br><span class=\"grad\">per l'impiego previsto.</span>",
        "Non il pi&ugrave; costoso: quello adeguato al carico, alla temperatura di esercizio e all'ambiente di lavoro. "
        "Un nylon caricato fibra su un componente scarico &egrave; solo un costo in pi&ugrave;.",
        "Materiali",
        img="gen-materials",
        note="Materiali speciali reperibili su richiesta",
    ),
    body="\n\n".join([
        section(
            sec_head("Criteri", "Quattro parametri, una scelta.",
                     "Indicarli nella richiesta accorcia sensibilmente i tempi di valutazione.")
            + cards([
                ("Carico", "Componente estetico e componente sollecitato non condividono nulla: materiale, spessori, orientamento e riempimento cambiano tutti."),
                ("Temperatura", "Vicino a un motore, a una fonte di calore o in un abitacolo esposto al sole il PLA &egrave; escluso, e con esso buona parte delle alternative."),
                ("Esposizione", "Raggi UV e agenti atmosferici restringono la scelta e orientano verso l'ASA."),
                ("Elasticit&agrave;", "Se il componente deve flettere e recuperare la posizione si adotta il TPU. Se deve mantenere la quota, il requisito &egrave; opposto."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Disponibilit&agrave;", "Materiali trattati e impiego.",
                     "Nessuno &egrave; superiore in assoluto: ciascuno risponde a un requisito preciso.")
            + specs([
                ("PLA", "Stampa semplice, buona definizione superficiale. Per verifiche dimensionali, modelli e componenti estetici. <b>Nessuna resistenza termica</b>: si deforma gi&agrave; alle temperature di un abitacolo al sole."),
                ("PETG", "Pi&ugrave; tenace del PLA e meno fragile. Scelta di riferimento per supporti, contenitori e componenti funzionali non esposti a calore."),
                ("ASA", "Resistente a raggi UV e intemperie. Il materiale per tutto ci&ograve; che resta stabilmente in esterno."),
                ("ABS", "Buona resistenza termica e meccanica. Per componenti tecnici, carter e scocche in ambienti caldi."),
                ("TPU", "Flessibile ed elastico. Protezioni, piedini antivibranti, paracolpi, inserti morbidi e guarnizioni non critiche."),
                ("Nylon caricato carbonio (CF)", "Rigidit&agrave; elevata e stabilit&agrave; dimensionale. Per staffe e attrezzature che devono mantenere la quota sotto carico."),
                ("Nylon caricato vetro (GF)", "Impiego analogo al CF, con diverso rapporto tra rigidit&agrave;, tenacit&agrave; e costo."),
                ("Resina", "Per dettagli fini e geometrie piccole, oltre i limiti dell'FDM. Da considerare la maggiore fragilit&agrave;: non &egrave; un materiale da carico."),
            ]),
            cls="paper-2",
        ),
        section(
            pain([
                ("CRITERIO", "Non esiste un materiale universale",
                 "Un materiale pi&ugrave; costoso non &egrave; automaticamente pi&ugrave; adatto: deve essere coerente con geometria e impiego. Se il PETG soddisfa il requisito, proponiamo il PETG."),
                ("LIMITE", "Il materiale non salva una geometria sbagliata",
                 "Un componente progettato male cede anche in nylon caricato. Prima il disegno &mdash; orientamento, raccordi, spessori, distribuzione degli sforzi &mdash; poi il materiale."),
            ]),
        ),
    ]),
    cta=cta_band("Non hai definito il materiale?",
                 "Rientra nel nostro lavoro. Descrivici le condizioni di esercizio del componente e ti forniamo l'indicazione tecnica."),
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
        "Dal problema tecnico<br><span class=\"grad\">al componente finito.</span>",
        "MakerSolve &egrave; una realt&agrave; recente e non presentiamo un portfolio di commesse che non abbiamo ancora. "
        "Questi sono lavori usciti dalla nostra officina, descritti per come sono andati.",
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
          <h3>Scocca ricostruita su PCB esistente</h3>
          <p>Involucro danneggiato, elettronica funzionante. Abbiamo rilevato la scheda originale e progettato attorno a essa una nuova scocca: pulsanti, foro portachiavi e nervature interne per il bloccaggio della PCB.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="1">
        <div class="work-img"><img src="/assets/dima.png" alt="Posaggio da banco per tubicini flessibili" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Attrezzatura di reparto</span>
          <h3>Posaggio da banco per tubicini</h3>
          <p>Attrezzatura per mantenere in posizione tubi di piccolo diametro durante assemblaggio e collaudo. Obiettivo: rendere ripetibile il posizionamento senza commissionare un'attrezzatura dedicata.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="2">
        <div class="work-img"><img src="/assets/dima-semimanubri-moto.png" alt="Dima universale per semimanubri da competizione" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Prodotto MakerSolve</span>
          <h3>Dima universale per semimanubri</h3>
          <p>Attrezzatura per il controllo dell'apertura dei semimanubri su moto da competizione. Geometria studiata per adattarsi a modelli differenti, in sostituzione della misurazione manuale.</p>
        </div>
      </article>
    </div>
"""),
        section(
            sec_head("Il percorso", "Lo stesso su ogni intervento.")
            + pain([
                ("01 &middot; PROBLEMA", "Un componente assente o inefficace",
                 "Un pezzo danneggiato, un'attrezzatura non a catalogo, un'operazione che dipende troppo dalla manualit&agrave; dell'operatore."),
                ("02 &middot; RILIEVO", "Misure, ingombri, condizioni",
                 "Quote e vincoli: accoppiamenti richiesti, spazio disponibile, sollecitazioni previste, ambiente di esercizio."),
                ("03 &middot; CAD", "La geometria segue i vincoli",
                 "Il modello discende dai requisiti rilevati. Ogni raccordo e ogni spessore rispondono a una ragione tecnica."),
                ("04 &middot; VALIDAZIONE", "Verifica in esercizio",
                 "Il componente si monta e si prova. Scostamenti significano correzione del modello e nuova realizzazione: senza stampi, iterare costa poco."),
            ]),
            cls="",
        ),
        section(
            sec_head("Ambito", "Tipologie che seguiamo.",
                     "Se la tua esigenza rientra qui, l'ambito &egrave; quello corretto.")
            + cards([
                ("Scocche e contenitori", "Involucri su misura per elettronica esistente: alloggiamenti PCB, passaggi cavo, accessi per connettori e comandi."),
                ("Supporti e adattatori", "Staffe, raccordi e interfacce tra componenti non progettati per accoppiarsi."),
                ("Reverse engineering", "Ricostruzione da campione fisico, anche danneggiato: rileviamo sulle porzioni integre."),
            ], cols=3),
            cls="paper",
        ),
    ]),
    cta=cta_band("La tua esigenza rientra in questi casi?",
                 "Inviaci una fotografia e le misure di massima: ricevi l'esito di fattibilit&agrave; e l'indicazione del materiale entro 24/48 ore."),
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
        "Stampa 3D su misura,<br><span class=\"grad\">verificata prima di produrre.</span>",
        "Inviare un file a una macchina lo fanno tutti. La differenza sta nella verifica che precede: "
        "spessori, orientamento, punti critici e idoneit&agrave; del materiale. &Egrave; il controllo che evita di pagare due volte lo stesso componente.",
        "Stampa 3D personalizzata",
    ),
    body="\n\n".join([
        section(
            sec_head("Punto di partenza", "Con file 3D o senza.")
            + cards([
                ("Hai gi&agrave; il file",
                 "Accettiamo STL, STEP, 3MF e OBJ. Prima di produrre verifichiamo scala, spessori minimi, orientamento e criticit&agrave; geometriche, e ti segnaliamo le modifiche opportune. Gli errori emergono prima, non a componente consegnato."),
                ("Non hai il file",
                 "La modellazione CAD rientra nel servizio: partiamo da uno schizzo, da una fotografia con riferimento dimensionale o dal componente fisico. Non serve saper modellare per ottenere un pezzo su misura."),
            ], cols=2),
            cls="paper",
        ),
        MARQUEE,
        section(
            sec_head("Realizzazioni", "Dal ricambio all'attrezzatura.")
            + cards([
                ("Ricambi non reperibili", "Componenti fuori produzione o privi di fornitore, ricostruiti dall'originale o dalle porzioni residue."),
                ("Supporti ed espositori", "Basi, sostegni, staffe ed espositori progettati su un oggetto specifico, non adattati da un prodotto generico."),
                ("Oggetti personalizzati", "Targhette, loghi tridimensionali e componenti di piccole dimensioni su misura."),
                ("Adattatori", "Raccordi e interfacce tra componenti non predisposti all'accoppiamento."),
                ("Prototipi", "Componenti da provare sul campo per verificare ingombri, accoppiamenti ed ergonomia."),
                ("Piccoli lotti", "Serie ridotte, dove attrezzare uno stampo non ha convenienza economica."),
            ], cols=3),
            cls="paper-2",
        ),
        section(
            pain([
                ("INFORMAZIONE UTILE", "L'impiego determina le scelte tecniche",
                 "Estetico, funzionale o provvisorio: la destinazione del componente determina materiale, spessori e orientamento di stampa. Indicarla &egrave; il dato pi&ugrave; utile che puoi darci."),
                ("LIMITE", "La stampa 3D non &egrave; sempre la risposta",
                 "Se una lavorazione CNC, un taglio laser o un ricambio commerciale sono pi&ugrave; adatti, te lo diciamo in fase di valutazione, prima di qualsiasi impegno di spesa."),
            ]),
        ),
    ]),
    cta=cta_band("Hai un file o solo un'idea?",
                 "In entrambi i casi possiamo partire. Inviaci il materiale disponibile e ricevi una risposta entro 24/48 ore."),
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
        "Dall'esigenza tecnica<br><span class=\"grad\">al modello digitale.</span>",
        "Disegniamo componenti su misura partendo da quello che hai: un'idea, uno schizzo, una fotografia quotata o il campione fisico. "
        "Il modello nasce per essere prodotto, verificato e usato.",
        "Progettazione CAD",
    ),
    body="\n\n".join([
        section(
            sec_head("Dati di partenza", "Da cosa possiamo partire.",
                     "Non serve documentazione tecnica formale. Serve che la funzione del componente sia definita.")
            + cards([
                ("Idea o schizzo", "Anche a mano libera. Da l&igrave; definiamo insieme vincoli e ingombri."),
                ("Fotografie e misure", "Una fotografia con calibro o metro in campo d&agrave; il riferimento di scala. Le quote critiche le definiamo in analisi."),
                ("Campione fisico", "Il componente originale, anche rotto: rileviamo sulle porzioni integre e ricostruiamo il resto."),
                ("File esistente", "STEP, STL o 3MF da modificare, correggere o adattare a un nuovo impiego."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Applicazioni", "Casi ricorrenti.")
            + pain([
                ("CASO 01", "Scocche e contenitori", "Involucri progettati attorno a un'elettronica esistente: alloggiamento scheda, passaggi cavo, accessi per connettori e comandi, sistemi di ritegno."),
                ("CASO 02", "Supporti e adattatori", "Interfacce tra componenti non predisposti all'accoppiamento, con fissaggi definiti e ingombri verificati."),
                ("CASO 03", "Prototipi funzionali", "Modelli da provare sul campo, iterare e correggere prima di consolidare la geometria."),
                ("CASO 04", "Documentazione trasferibile", "Un modello 3D pulito e un file STEP utilizzabili presso altri fornitori, anche se la produzione non la affidi a noi."),
            ]),
        ),
        section(
            sec_head("Consegna", "Cosa ricevi.")
            + specs([
                ("Modello 3D", "Il componente modellato secondo i requisiti concordati e verificato per il processo produttivo previsto."),
                ("File STEP", "Formato neutro, apribile da qualunque CAD. &Egrave; tuo: puoi portarlo altrove senza vincoli."),
                ("Revisioni", "Le correzioni emerse dalla prova del prototipo rientrano nel percorso: aggiorniamo il modello, non ricominciamo."),
                ("Tolleranze", "<b>Lavoriamo nell'ordine del millimetro.</b> Il decimo, in FDM, non rientra tra i risultati garantiti: se il componente lo richiede te lo diciamo prima di iniziare."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai un componente da disegnare?",
                 "Inviaci quello che hai, anche solo uno schizzo. Ricevi una valutazione di fattibilit&agrave; entro 24/48 ore."),
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
        "Dal componente reale<br><span class=\"grad\">al modello digitale.</span>",
        "Ricostruiamo componenti dal campione fisico, da una fotografia o da quanto resta di un originale danneggiato. "
        "Quando il ricambio &egrave; fuori produzione e il fornitore non risponde, spesso &egrave; l'unica via per rimettere in servizio una macchina.",
        "Reverse engineering",
    ),
    body="\n\n".join([
        section(
            sec_head("Applicabilit&agrave;", "Quattro casi ricorrenti.")
            + pain([
                ("CASO 01", "Ricambio non reperibile", "Componente fuori produzione, fornitore irraggiungibile, oppure venduto solo dentro un assieme dal costo sproporzionato."),
                ("CASO 02", "Componente danneggiato", "Rileviamo sulle porzioni integre e ricostruiamo il resto per continuit&agrave; geometrica. Un pezzo rotto conserva quasi sempre informazione sufficiente."),
                ("CASO 03", "Scocche e carter", "Gusci e coperture da riprodurre o da adattare a componenti interni nel frattempo modificati."),
                ("CASO 04", "Riproduzione con modifica", "Non una copia conforme ma una versione corretta: fissaggi diversi, rinforzo dove cedeva, ingombri ridotti."),
            ]),
        ),
        section(
            sec_head("Processo", "Come ricostruiamo un componente.")
            + cards([
                ("Analisi", "Determiniamo come lavorava, dove si accoppiava e perch&eacute; ha ceduto. Senza questa fase si replica anche il difetto originale."),
                ("Rilievo", "Misurazione diretta di ingombri, diametri, interassi e spessori, con attenzione alle quote di accoppiamento."),
                ("Ricostruzione CAD", "Il modello nasce dalle quote rilevate, con le correzioni necessarie dove la geometria originale era il punto debole."),
                ("Prototipo", "Realizzazione, prova in sede e correzione. La prima versione valida gli accoppiamenti, non &egrave; definitiva."),
            ], cols=4, dark=True),
        ),
        section(
            pain([
                ("ESCLUSIONE", "Non su parti critiche",
                 "Non trattiamo componenti strutturali critici, parti di sicurezza o applicazioni soggette a certificazione. Un pezzo il cui cedimento comporti rischio per persone o impianti richiede un percorso di qualifica che non copriamo."),
                ("VALUTAZIONE", "La copia non &egrave; sempre la risposta",
                 "Se l'originale era in metallo e lavorava sotto carico, riprodurlo in materiale polimerico non risolve: sposta il problema pi&ugrave; avanti. In quel caso te lo diciamo e valutiamo alternative."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Hai un componente da ricostruire?",
                 "Inviaci una fotografia del pezzo, anche rotto, con un riferimento dimensionale in campo. Ricevi l'esito entro 24/48 ore."),
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
        "Validare l'idea<br><span class=\"grad\">prima di investire.</span>",
        "Un prototipo non deve essere bello: deve dare una risposta verificabile. Entra? Si monta? Tiene? "
        "Realizziamo prototipi funzionali per verificare forma, ingombri, fori, fissaggi e montaggio prima che le decisioni diventino costose.",
        "Prototipazione rapida",
    ),
    body="\n\n".join([
        section(
            sec_head("Finalit&agrave;", "Quattro verifiche in un solo pezzo.")
            + cards([
                ("Accoppiamento", "Il componente entra nello spazio disponibile, i fori sono in asse, gli interassi tornano nella realt&agrave; e non solo sul disegno."),
                ("Prova funzionale", "Il comportamento si verifica montato e sollecitato, non a pezzo fermo su un tavolo."),
                ("Iterazione rapida", "Correzione del modello e nuova stampa. Senza stampi, cambiare idea alla terza revisione costa poco."),
                ("Ponte verso la produzione", "Una geometria validata sul campo &egrave; la base per decidere con cognizione se e come industrializzare."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Destinatari", "Chi ne trae maggiore vantaggio.")
            + pain([
                ("PROFILO 01", "Uffici tecnici e R&amp;D", "Chi deve validare una soluzione prima di impegnare capitale in stampi o attrezzature definitive, e ha bisogno di iterare in giorni anzich&eacute; in settimane."),
                ("PROFILO 02", "Manutenzione e officine", "Chi deve ripristinare una funzionalit&agrave; e vuole verificare la soluzione prima di adottarla stabilmente."),
                ("PROFILO 03", "Sviluppo prodotto", "Chi ha bisogno di verificare ergonomia, ingombri e percezione d'uso prima di consolidare il progetto."),
                ("PROFILO 04", "Presentazione interna", "Un componente fisico che passa di mano in riunione fornisce elementi di valutazione che nessuna immagine sostituisce."),
            ]),
        ),
        section(
            sec_head("Livelli di servizio", "Fin dove vuoi arrivare.")
            + specs([
                ("Solo prototipo", "Il componente da provare, realizzato nel materiale pi&ugrave; adatto alla verifica prevista."),
                ("Prototipo e revisione CAD", "Il componente e il modello aggiornato con le correzioni emerse dalla prova: quello che ricevi &egrave; una geometria gi&agrave; validata."),
                ("Prototipo e pezzo definitivo", "A validazione avvenuta realizziamo la versione definitiva, eventualmente in un materiale diverso da quello di prova."),
                ("Materiali tipici", "PLA per le verifiche dimensionali, PETG e ABS/ASA per le prove funzionali, nylon caricato dove serve rigidit&agrave;, TPU per le parti che devono flettere."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai una soluzione da validare?",
                 "Con o senza file 3D. Descrivici la funzione richiesta al componente e ricevi una risposta entro 24/48 ore."),
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
    desc="Componenti su misura quando il pezzo commerciale non esiste, non combacia o non conviene: supporti, staffe, adattatori, guide, carter, dime e piccoli lotti.",
    hero=hero(
        "Componenti custom",
        "Progettati sul problema,<br><span class=\"grad\">non adattati da un catalogo.</span>",
        "Realizziamo componenti su misura quando il pezzo commerciale non esiste, non combacia, costa troppo o richiede una modifica specifica: "
        "supporti, staffe, adattatori, guide, carter, dime, scocche e piccoli lotti.",
        "Componenti custom",
    ),
    body="\n\n".join([
        section(
            sec_head("Tipologie", "Quattro famiglie ricorrenti.")
            + cards([
                ("Supporti e fissaggi", "Staffe e sostegni progettati sull'oggetto reale e sul punto di ancoraggio disponibile, non adattati da un prodotto generico."),
                ("Adattatori", "Interfacce tra componenti non predisposti all'accoppiamento: cambio di attacco, di passo, di diametro o di orientamento."),
                ("Scocche e coperture", "Involucri e carter attorno a componenti esistenti, con accessi, passaggi cavo e ritegni definiti sul contenuto reale."),
                ("Dime e ausili di reparto", "Attrezzature che rendono ripetibile un'operazione oggi affidata alla manualit&agrave; dell'operatore."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Convenienza", "Quando ha senso economico.")
            + pain([
                ("CONDIZIONE 01", "Il ricambio non si trova", "Fuori produzione, oppure venduto solo dentro un assieme che costa molte volte il pezzo necessario."),
                ("CONDIZIONE 02", "La geometria non corrisponde", "Il commerciale esiste ma non combacia: attacchi diversi, ingombri fuori, interassi che non tornano."),
                ("CONDIZIONE 03", "Serve verificare prima", "La soluzione non &egrave; ancora consolidata e va validata su un componente reale prima dell'adozione."),
                ("CONDIZIONE 04", "Le quantit&agrave; sono ridotte", "Da uno a poche decine di pezzi: volumi per cui attrezzare uno stampo &egrave; economicamente escluso."),
            ]),
        ),
        section(
            pain([
                ("CRITERIO", "La stampa 3D non &egrave; sempre la soluzione",
                 "Se una lavorazione CNC, un taglio laser, un ricambio commerciale o una soluzione pi&ugrave; semplice sono pi&ugrave; adatti, te lo diciamo in fase di valutazione, anche quando significa rinunciare alla commessa."),
                ("QUANTIT&Agrave;", "Dal pezzo singolo alla piccola serie",
                 "Il limite superiore dipende dalla geometria e dal tempo macchina e si definisce sul componente specifico. Se i volumi rendono conveniente lo stampaggio, te lo segnaliamo."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Ti serve un componente che non esiste?",
                 "Descrivici il problema tecnico, non la soluzione: l'impostazione progettuale rientra nel servizio. Risposta entro 24/48 ore."),
    jsonld=service_ld("Componenti su misura",
                      "Progettazione e produzione di componenti custom: supporti, staffe, adattatori, guide, carter, dime, scocche e piccoli lotti.",
                      "servizi/componenti-custom/"),
))



# ---------------------------------------------------------- 9. STAMPA 3D MIRANDOLA (landing locale)
PAGES.append(dict(
    path="stampa-3d-mirandola/",
    nav_active="",
    title="Stampa 3D a Mirandola (MO) | Pezzi su misura e prototipi | MakerSolve",
    ogtitle="Stampa 3D a Mirandola &mdash; MakerSolve",
    desc="Servizio di stampa 3D e progettazione CAD a Mirandola, in provincia di Modena: supporti, staffe, adattatori, scocche, ricambi e prototipi su misura. Ritiro in zona, risposta in 24/48 ore.",
    hero=hero(
        "Stampa 3D locale",
        "Stampa 3D a Mirandola,<br><span class=\"grad\">in provincia di Modena.</span>",
        "La nostra officina &egrave; a Mirandola. Progettiamo e stampiamo supporti, staffe, adattatori, scocche, "
        "piccoli ricambi e prototipi su misura per aziende e professionisti della zona, con ritiro diretto o spedizione.",
        "Stampa 3D a Mirandola",
        note="Ritiro in zona Mirandola &middot; Risposta in 24/48 ore",
    ),
    body="\n\n".join([
        section(
            sec_head("Servizio locale", "Un fornitore raggiungibile.",
                     "Sulle lavorazioni che richiedono verifiche dimensionali, avere l'officina a pochi chilometri accorcia sensibilmente i tempi.")
            + cards([
                ("Ritiro diretto", "Se sei a Mirandola o nei comuni vicini puoi ritirare di persona ed evitare i tempi di spedizione."),
                ("Confronto sul pezzo", "Sulle lavorazioni complesse puoi vedere e provare il componente prima del completamento, con correzioni immediate."),
                ("Consegna del campione", "Puoi portarci direttamente il pezzo rotto o il campione da rilevare, senza rischiare danni nel trasporto."),
            ], cols=3),
            cls="paper",
        ),
        MARQUEE,
        section(
            sec_head("Cosa realizziamo", "Componenti su misura, in zona.")
            + cards([
                ("Supporti e staffe", "Sostegni e fissaggi progettati sull'oggetto reale e sul punto di ancoraggio disponibile."),
                ("Adattatori", "Interfacce tra componenti non predisposti all'accoppiamento: attacchi, passi, diametri."),
                ("Scocche e contenitori", "Involucri su misura per elettronica esistente, con accessi e passaggi cavo definiti sul contenuto reale."),
                ("Ricambi non reperibili", "Componenti fuori produzione ricostruiti dall'originale o dalle porzioni residue."),
                ("Prototipi", "Componenti da provare sul campo per verificare ingombri, accoppiamenti ed ergonomia."),
                ("Attrezzature di reparto", "Dime, posaggi e maschere progettati sul tuo ciclo di lavoro."),
            ], cols=3),
            cls="paper-2",
        ),
        section(
            sec_head("Come partire", "Cosa ci serve per la valutazione.",
                     "Non serve un file 3D: la modellazione CAD la facciamo noi.")
            + pain([
                ("DATO 01", "Funzione del componente", "Cosa deve fare il pezzo e in quale ambiente lavora. &Egrave; l'informazione che determina materiale e processo."),
                ("DATO 02", "Misure principali", "Ingombri massimi, diametri e interassi, anche approssimativi. Una fotografia con un metro accanto &egrave; sufficiente."),
                ("DATO 03", "Quantit&agrave;", "Un pezzo o una piccola serie: cambia la valutazione di convenienza e i tempi."),
                ("DATO 04", "Tempi previsti", "Il termine entro cui ti serve, per verificare la compatibilit&agrave; con il carico di lavoro in corso."),
            ]),
        ),
        section(
            sec_head("Zona servita", "Mirandola e provincia di Modena.")
            + specs([
                ("Ritiro diretto", "Mirandola e comuni limitrofi della Bassa modenese."),
                ("Spedizione", "Provincia di Modena, Emilia-Romagna e resto d'Italia."),
                ("Materiali", "PLA, PETG, ASA, ABS, TPU, nylon caricato fibra di carbonio e di vetro, resina. Materiali speciali su richiesta."),
                ("Tempi di risposta", "24/48 ore per la valutazione tecnica. I tempi di produzione li definiamo in fase di valutazione."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Sei in zona Mirandola?",
                 "Inviaci una fotografia e le misure di massima, oppure chiamaci: rispondiamo entro 24/48 ore, senza costi n&eacute; vincoli."),
    jsonld=service_ld("Stampa 3D a Mirandola",
                      "Servizio di stampa 3D e progettazione CAD a Mirandola, in provincia di Modena: supporti, staffe, adattatori, scocche, ricambi e prototipi su misura.",
                      "stampa-3d-mirandola/"),
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
