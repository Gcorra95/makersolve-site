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
    desc="Sono Giulio: progetto e produco componenti su misura, attrezzature e prototipi funzionali. Officina a Mirandola (MO), interlocutore tecnico diretto senza passaggi commerciali.",
    hero=hero(
        "Chi sono",
        "Parli con chi<br><span class=\"grad\">progetta e produce.</span>",
        "Sono Giulio. MakerSolve &egrave; la mia officina: progettazione meccanica, reverse engineering e stampa 3D. "
        "Chi risponde al telefono &egrave; la stessa persona che disegna il pezzo e lo tira fuori dalla macchina.",
        "Chi sono",
        note="Nessun intermediario commerciale &middot; Risposta in 24/48h",
    ),
    body="\n\n".join([
        section(
            sec_head("Approccio", "Meccanica pratica, non teoria.",
                     "Il mio metro di giudizio non &egrave; se il modello 3D &egrave; elegante. &Egrave; se il pezzo, montato, fa quello che deve fare.")
            + cards([
                ("Parto dal problema, non dal file",
                 "La prima domanda non &egrave; &laquo;che forma ha&raquo; ma &laquo;cosa deve fare, dove lavora e cosa succede se cede&raquo;. Da l&igrave; discendono materiale, spessori e processo."),
                ("Interlocutore unico",
                 "Non c'&egrave; un commerciale che raccoglie la richiesta e un tecnico che la interpreta. Parli direttamente con chi esegue: le informazioni non si perdono per strada."),
                ("Ti dico di no quando serve",
                 "Se la stampa 3D non &egrave; la tecnologia giusta, o se il pezzo &egrave; fuori dal mio ambito, te lo dico subito. Un no in 24 ore vale pi&ugrave; di un preventivo che ti fa perdere due settimane."),
            ], cols=3, dark=True),
            cls="",
        ),
        section(
            sec_head("Contesto", "Un'officina a Mirandola.",
                     "Lavoro in provincia di Modena, dentro un territorio dove la meccanica di precisione &egrave; la norma e non l'eccezione. &Egrave; il contesto in cui mi confronto ogni giorno.")
            + specs([
                ("Cosa faccio", "Progettazione CAD di componenti su misura, reverse engineering da pezzo fisico, attrezzature di reparto, prototipi funzionali e piccola elettronica integrata."),
                ("Per chi lavoro", "Aziende, officine, manutenzione e reparti tecnici. Anche privati, quando la richiesta ha senso tecnico."),
                ("Come mi trovi", "Telefono, email o form. Se sei in zona Mirandola puoi passare in officina; per il resto d'Italia si lavora su file e foto e si spedisce."),
                ("Cosa non faccio", "Parti di sicurezza, componenti strutturali critici e dispositivi certificati. Su quelli posso supportare la fase di studio, non la produzione."),
            ]),
            cls="paper-2",
        ),
        MARQUEE,
        section(
            sec_head("Come lavoro", "Quattro passaggi, sempre gli stessi.")
            + pain([
                ("PASSO 01", "Mi mandi il materiale", "Foto, misure, un campione fisico o un file. Anche parziale: il resto lo ricostruisco io."),
                ("PASSO 02", "Valuto la fattibilit&agrave;", "Entro 24/48h ti dico se si fa, con quale materiale e a quali condizioni. Se non si fa, ti spiego perch&eacute;."),
                ("PASSO 03", "Progetto e produco", "Modellazione CAD e stampa. Sui pezzi complessi ti mostro il modello prima, cos&igrave; correggiamo su schermo e non su un pezzo gi&agrave; fatto."),
                ("PASSO 04", "Provi e correggo", "Il pezzo si valida in funzione. Se qualcosa non torna si interviene sul modello e si ristampa: &egrave; il vantaggio di lavorare senza stampi."),
            ]),
        ),
    ]),
    cta=cta_band("Hai un pezzo da valutare?",
                 "Mandami una foto e due misure. Ti dico in 24/48h se si pu&ograve; fare, senza costi e senza impegno."),
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
    title="Materiali stampa 3D: PLA, PETG, ASA, ABS, TPU, Nylon | Mirandola e Modena",
    ogtitle="Materiali &mdash; MakerSolve",
    desc="Come scelgo il materiale in base a carico, temperatura e ambiente d'esercizio. PLA, PETG, ASA, ABS, TPU, nylon caricato fibra e resina. Mirandola (MO).",
    hero=hero(
        "Materiali",
        "Il materiale giusto<br><span class=\"grad\">non &egrave; il pi&ugrave; costoso.</span>",
        "&Egrave; quello adatto al carico che il pezzo deve reggere, alla temperatura a cui lavora e all'ambiente in cui sta. "
        "Un nylon caricato fibra su un pezzo che non porta nulla &egrave; solo spesa in pi&ugrave;.",
        "Materiali",
        img="gen-materials",
        note="Materiali speciali reperibili su richiesta",
    ),
    body="\n\n".join([
        section(
            sec_head("Criterio", "Quattro domande prima di scegliere.",
                     "Rispondere a queste, nella richiesta, accorcia di parecchio la conversazione.")
            + cards([
                ("Che carico regge?", "Un pezzo estetico e uno che lavora sotto sforzo non hanno nulla in comune: cambiano materiale, spessori, orientamento di stampa e riempimento."),
                ("A che temperatura lavora?", "Vicino a un motore, a una fonte di calore o dentro un'auto d'estate: il PLA &egrave; fuori discussione, e met&agrave; delle altre opzioni pure."),
                ("Sta al sole o all'aperto?", "L'esposizione a UV e intemperie esclude diversi materiali e porta dritti verso l'ASA."),
                ("Deve flettere o restare rigido?", "Se il pezzo deve deformarsi e tornare in posizione si va sul TPU. Se deve restare fermo, serve l'opposto."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Disponibili", "Cosa tengo e quando lo uso.",
                     "Nessuno di questi &egrave; &laquo;il migliore&raquo;. Ognuno risolve un problema diverso.")
            + specs([
                ("PLA", "Il pi&ugrave; semplice da stampare, buona definizione. Va bene per prove dimensionali, mock-up, modelli e pezzi estetici. <b>Non regge il calore</b>: perde forma gi&agrave; a temperature che si raggiungono in un'auto al sole."),
                ("PETG", "Pi&ugrave; tenace del PLA e meno fragile. &Egrave; la scelta di default per supporti, contenitori e parti funzionali che non vedono temperature alte."),
                ("ASA", "Resistente a UV e intemperie. &Egrave; il materiale giusto per qualsiasi cosa stia stabilmente all'aperto."),
                ("ABS", "Buona resistenza termica e meccanica per componenti tecnici, carter e scocche che lavorano in ambienti caldi."),
                ("TPU", "Flessibile ed elastico. Protezioni, piedini antivibranti, paracolpi, inserti morbidi e guarnizioni non critiche."),
                ("Nylon caricato fibra di carbonio (CF)", "Rigidit&agrave; elevata e buona stabilit&agrave; dimensionale. Per staffe e attrezzature che devono restare in quota sotto carico."),
                ("Nylon caricato fibra di vetro (GF)", "Simile al CF come impiego, con un compromesso diverso tra rigidit&agrave;, tenacit&agrave; e costo."),
                ("Resina", "Stampa a resina per dettagli fini e geometrie piccole, dove l'FDM non arriva. Attenzione: in genere pi&ugrave; fragile, non &egrave; un materiale da carico."),
            ]),
            cls="paper-2",
        ),
        section(
            pain([
                ("ONEST&Agrave;", "Non esiste il materiale perfetto per tutto",
                 "Un materiale pi&ugrave; costoso non &egrave; automaticamente migliore: deve essere adatto al pezzo, alla geometria e all'uso reale. Se il PETG basta, ti propongo il PETG."),
                ("LIMITE", "Il materiale non salva una geometria sbagliata",
                 "Un pezzo progettato male si rompe anche in nylon caricato. Prima viene il disegno &mdash; orientamento, raccordi, spessori, dove passano gli sforzi &mdash; poi la scelta del materiale."),
            ]),
        ),
    ]),
    cta=cta_band("Non sai quale materiale ti serve?",
                 "&Egrave; normale, ed &egrave; parte del lavoro. Descrivimi dove lavora il pezzo e te lo dico io."),
    jsonld=service_ld("Stampa 3D con materiali tecnici",
                      "Selezione del materiale di stampa 3D in base a carico, temperatura d'esercizio e ambiente: PLA, PETG, ASA, ABS, TPU, nylon caricato fibra e resina.",
                      "materiali/"),
))

# ---------------------------------------------------------- 3. PORTFOLIO
PAGES.append(dict(
    path="portfolio/",
    nav_active="portfolio",
    title="Lavori: casi reali di CAD e stampa 3D | Mirandola e Modena",
    ogtitle="Lavori &mdash; MakerSolve",
    desc="Casi reali usciti dall'officina: scocca ricostruita attorno a una PCB, posaggio da banco per tubicini, dima universale per semimanubri da competizione.",
    hero=hero(
        "Lavori",
        "Tre pezzi,<br><span class=\"grad\">tre problemi diversi.</span>",
        "MakerSolve &egrave; una realt&agrave; giovane e non ho ancora un portfolio aziendale da esibire. "
        "Questi sono lavori reali, raccontati per come sono andati: da dove nasceva il problema e come &egrave; stato risolto.",
        "Lavori",
        img="gen-exploded",
        note="Casi reali &middot; Nessun render di repertorio",
    ),
    body="\n\n".join([
        section(
            """    <div class="work">
      <article class="work-item rv">
        <div class="work-img"><img src="/assets/scocca-telecomando-cancello-stampa-3d-mirandola.png" alt="Scocca per telecomando cancello ricostruita e stampata in 3D" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Reverse engineering</span>
          <h3>Scocca ricostruita attorno a una PCB esistente</h3>
          <p>Il guscio originale era rotto ma l'elettronica funzionava ancora. Ho rilevato la scheda originale e progettato una nuova scocca su misura, con pulsanti, foro portachiavi e nervature interne studiate per tenere ferma la PCB.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="1">
        <div class="work-img"><img src="/assets/dima.png" alt="Posaggio da banco per tubicini flessibili" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Attrezzatura di reparto</span>
          <h3>Posaggio da banco per tubicini flessibili</h3>
          <p>Dima per tenere in posizione piccoli tubi flessibili durante assemblaggio o test. Nasce da un'esigenza semplice: rendere ripetibile un posizionamento senza commissionare un'attrezzatura costosa.</p>
        </div>
      </article>
      <article class="work-item rv" data-d="2">
        <div class="work-img"><img src="/assets/dima-semimanubri-moto.png" alt="Dima universale per semimanubri da competizione" loading="lazy"></div>
        <div class="work-body">
          <span class="tag">Prodotto MakerSolve</span>
          <h3>Dima universale per semimanubri</h3>
          <p>Attrezzatura per controllare l'apertura dei semimanubri sulle moto da competizione. La geometria &egrave; studiata per adattarsi a moto diverse e rendere il controllo pi&ugrave; rapido e ripetibile della misurazione manuale.</p>
        </div>
      </article>
    </div>
"""),
        section(
            sec_head("Il filo comune", "Come nasce un pezzo, ogni volta.")
            + pain([
                ("01 &middot; PROBLEMA", "Qualcosa non c'&egrave; o non funziona",
                 "Un componente rotto, un'attrezzatura che non esiste a catalogo, un'operazione che dipende troppo dalla manualit&agrave; dell'operatore."),
                ("02 &middot; VINCOLI", "Misure, ingombri, condizioni d'uso",
                 "Rilievo di quote e vincoli: cosa deve accoppiarsi con cosa, quanto spazio c'&egrave;, che sforzi vede il pezzo, in che ambiente sta."),
                ("03 &middot; CAD", "Il modello nasce dai vincoli",
                 "La geometria discende dai requisiti, non da un'idea estetica. Ogni raccordo e ogni spessore rispondono a una ragione precisa."),
                ("04 &middot; PROVA", "Si valida in funzione",
                 "Il pezzo si monta e si prova. Se qualcosa non torna si corregge il modello e si ristampa: senza stampi, un'iterazione costa poco."),
            ]),
            cls="",
        ),
        section(
            sec_head("Ambito", "Che tipo di lavori seguo.",
                     "Se il tuo caso somiglia a uno di questi siamo nel campo giusto.")
            + cards([
                ("Scocche e contenitori", "Involucri su misura attorno a elettronica esistente: alloggiamenti PCB, passaggi cavo, accessi per connettori e pulsanti."),
                ("Supporti e adattatori", "Staffe, raccordi e adattatori che collegano due cose nate per non stare insieme."),
                ("Reverse engineering funzionale", "Ricostruzione di componenti a partire dal pezzo fisico, anche quando &egrave; rotto: si rileva dalle zone sane."),
            ], cols=3),
            cls="paper",
        ),
    ]),
    cta=cta_band("Il tuo caso somiglia a uno di questi?",
                 "Mandami una foto e due misure: ti dico in 24/48h se si pu&ograve; fare e con quale materiale."),
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
    desc="Stampa 3D di oggetti e pezzi su misura, con o senza file 3D. Controllo del file prima di stampare, consulenza su materiale e orientamento. Mirandola (MO).",
    hero=hero(
        "Stampa 3D personalizzata",
        "Prima si controlla<br><span class=\"grad\">il pezzo, poi si stampa.</span>",
        "Mandare un file a una macchina lo sanno fare tutti. La differenza la fa il controllo prima: spessori, orientamento, "
        "punti deboli e materiale adatto all'uso reale. &Egrave; il passaggio che evita di pagare due volte lo stesso pezzo.",
        "Stampa 3D personalizzata",
    ),
    body="\n\n".join([
        section(
            sec_head("Due punti di partenza", "Con il file, o senza.")
            + cards([
                ("Hai gi&agrave; il file 3D",
                 "Accetto STL, STEP, 3MF e OBJ. Prima di stampare controllo scala, spessori minimi, orientamento e punti critici, e ti dico se conviene modificare qualcosa. Se il file ha problemi lo scopri prima, non a pezzo consegnato."),
                ("Non hai il file",
                 "Il CAD lo faccio io, partendo da uno schizzo, una foto con una misura di riferimento o il pezzo fisico. Non serve saper modellare per ottenere un pezzo su misura."),
            ], cols=2),
            cls="paper",
        ),
        MARQUEE,
        section(
            sec_head("Cosa realizzo", "Dal ricambio all'attrezzatura.")
            + cards([
                ("Ricambi e pezzi introvabili", "Componenti fuori produzione o senza fornitore, ricostruiti dal pezzo originale o da quello che ne resta."),
                ("Supporti ed espositori", "Basi, sostegni, staffe ed espositori disegnati su un oggetto specifico invece che adattati da un prodotto generico."),
                ("Oggetti personalizzati", "Targhette, loghi tridimensionali, gadget e piccoli oggetti su misura."),
                ("Adattatori", "Raccordi e interfacce tra componenti che non sono nati per accoppiarsi."),
                ("Prototipi", "Pezzi da provare sul campo per verificare ingombri, accoppiamenti ed ergonomia prima di decidere."),
                ("Piccoli lotti", "Serie ridotte, dove attrezzare uno stampo non ha alcun senso economico."),
            ], cols=3),
            cls="paper-2",
        ),
        section(
            pain([
                ("COSA SERVE SAPERE", "L'uso reale decide tutto",
                 "Se il pezzo &egrave; estetico, funzionale o provvisorio cambia materiale, spessori e orientamento di stampa. Dimmelo nella richiesta: &egrave; l'informazione pi&ugrave; utile che puoi darmi."),
                ("LIMITE", "Non tutto va stampato in 3D",
                 "Se una lavorazione CNC, un taglio laser o un ricambio commerciale sono pi&ugrave; adatti al tuo caso, conviene saperlo prima di spendere. Te lo dico in fase di valutazione."),
            ]),
        ),
    ]),
    cta=cta_band("Hai un file o solo un'idea?",
                 "In entrambi i casi si parte. Mandami quello che hai e ti rispondo entro 24/48h."),
    jsonld=service_ld("Stampa 3D personalizzata",
                      "Stampa 3D di oggetti e componenti su misura, con o senza file 3D, con controllo preventivo di file, materiale e orientamento.",
                      "stampa-3d-personalizzata/"),
))

# ---------------------------------------------------------- 5. PROGETTAZIONE CAD
PAGES.append(dict(
    path="servizi/progettazione-cad/",
    nav_active="servizi",
    title="Progettazione CAD di componenti su misura | Mirandola e Modena",
    ogtitle="Progettazione CAD &mdash; MakerSolve",
    desc="Modellazione CAD di componenti custom a partire da idea, schizzo, foto o pezzo fisico. Consegna con file STEP. Mirandola (MO), lavorazioni in tutta Italia.",
    hero=hero(
        "Progettazione CAD",
        "Un problema diventa<br><span class=\"grad\">un pezzo reale.</span>",
        "Disegno componenti su misura partendo da quello che hai: un'idea, uno schizzo, una foto con due quote o il pezzo fisico. "
        "Il modello nasce per essere stampato, provato, corretto e usato &mdash; non per fare bella figura in un render.",
        "Progettazione CAD",
    ),
    body="\n\n".join([
        section(
            sec_head("Punto di partenza", "Da cosa posso partire.",
                     "Non serve materiale tecnico. Serve che sia chiaro cosa deve fare il pezzo.")
            + cards([
                ("Un'idea o uno schizzo", "Anche disegnato a mano su un foglio. Da l&igrave; si definiscono insieme vincoli e ingombri."),
                ("Foto e misure", "Una foto con un calibro o un metro accanto d&agrave; la scala. Le quote critiche le prendiamo insieme."),
                ("Un campione fisico", "Il pezzo originale, anche rotto: si rileva dalle zone integre e si ricostruisce il resto."),
                ("Un file esistente", "STEP, STL o 3MF da modificare, correggere o adattare a un nuovo impiego."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Quando serve", "I casi tipici.")
            + pain([
                ("CASO 01", "Scocche e contenitori", "Involucri disegnati attorno a un'elettronica esistente: alloggiamento della scheda, passaggi cavo, accessi per connettori e pulsanti, tenuta dei componenti."),
                ("CASO 02", "Supporti e adattatori", "Interfacce tra componenti che non sono nati per stare insieme, con i fissaggi giusti e gli ingombri verificati."),
                ("CASO 03", "Prototipi funzionali", "Modelli pensati per essere provati sul campo, iterati e corretti prima di congelare la geometria."),
                ("CASO 04", "File tecnici da usare altrove", "Un modello 3D pulito e un STEP che puoi portare a un altro fornitore, anche se poi non produci qui."),
            ]),
        ),
        section(
            sec_head("Consegna", "Cosa ricevi.")
            + specs([
                ("Modello 3D", "Il componente modellato secondo i requisiti concordati, verificato per il processo con cui verr&agrave; prodotto."),
                ("File STEP", "Formato neutro, apribile da qualsiasi CAD. &Egrave; tuo: puoi portarlo altrove senza dipendere da me."),
                ("Revisioni", "Le correzioni che emergono dalla prova del prototipo rientrano nel percorso: il modello si aggiorna, non si ricomincia."),
                ("Tolleranze", "<b>Si lavora nell'ordine del millimetro.</b> Il decimo, in FDM, non &egrave; garantito: se il pezzo lo richiede te lo dico prima di iniziare."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai un componente da disegnare?",
                 "Mandami quello che hai, anche solo uno schizzo. Ti rispondo entro 24/48h con una valutazione di fattibilit&agrave;."),
    jsonld=service_ld("Progettazione CAD",
                      "Modellazione CAD di componenti meccanici su misura a partire da idea, schizzo, foto, quote o pezzo fisico, con consegna in formato STEP.",
                      "servizi/progettazione-cad/"),
))

# ---------------------------------------------------------- 6. REVERSE ENGINEERING
PAGES.append(dict(
    path="servizi/reverse-engineering/",
    nav_active="servizi",
    title="Reverse engineering pezzi rotti e senza disegno | Mirandola e Modena",
    ogtitle="Reverse engineering &mdash; MakerSolve",
    desc="Ricostruzione CAD di componenti a partire dal pezzo fisico, anche rotto o incompleto. Ricambi non pi&ugrave; reperibili, scocche, carter. Mirandola (MO).",
    hero=hero(
        "Reverse engineering",
        "Il pezzo non esiste pi&ugrave;.<br><span class=\"grad\">Il problema s&igrave;.</span>",
        "Ricostruisco componenti partendo dal pezzo fisico, da una foto o da quello che resta di un originale rotto. "
        "Quando il ricambio &egrave; fuori produzione e il fornitore non risponde, questa &egrave; spesso l'unica strada che rimette in moto una macchina.",
        "Reverse engineering",
    ),
    body="\n\n".join([
        section(
            sec_head("Quando ha senso", "I quattro casi tipici.")
            + pain([
                ("CASO 01", "Il ricambio non si trova", "Componente fuori produzione, fornitore irreperibile, oppure venduto solo dentro un assieme che costa dieci volte il pezzo che ti serve."),
                ("CASO 02", "Il pezzo &egrave; rotto", "Si rileva dalle zone integre e si ricostruisce il resto per continuit&agrave; geometrica. Un pezzo rotto conserva quasi sempre abbastanza informazione."),
                ("CASO 03", "Scocche e carter", "Gusci e coperture da riprodurre o da adattare a componenti interni che nel frattempo sono cambiati."),
                ("CASO 04", "Serve una modifica", "Non una copia identica ma una versione corretta: fissaggi diversi, un rinforzo dove cedeva, un ingombro ridotto."),
            ]),
        ),
        section(
            sec_head("Processo", "Come si ricostruisce un pezzo.")
            + cards([
                ("Analisi del pezzo", "Si capisce come lavorava, dove si accoppiava e perch&eacute; ha ceduto. Senza questo passaggio si replica anche il difetto originale."),
                ("Rilievo delle quote", "Misurazione diretta di ingombri, diametri, interassi e spessori, con attenzione alle quote che devono accoppiarsi."),
                ("Ricostruzione CAD", "Il modello 3D nasce dalle quote rilevate, con le correzioni necessarie dove la geometria originale era il punto debole."),
                ("Prototipo e correzione", "Si stampa, si prova sul posto e si corregge. La prima versione serve a validare gli accoppiamenti, non a essere definitiva."),
            ], cols=4, dark=True),
        ),
        section(
            pain([
                ("LIMITE", "Non su parti critiche",
                 "Non propongo reverse engineering per componenti strutturali critici, parti di sicurezza o applicazioni che richiedono certificazioni specifiche. Un pezzo che, cedendo, mette a rischio persone o impianti richiede un percorso di qualifica che questa officina non copre."),
                ("LIMITE", "La copia non &egrave; sempre la risposta",
                 "Se l'originale era in metallo e lavorava sotto carico, riprodurlo in plastica non risolve: sposta il problema pi&ugrave; avanti. In quel caso te lo dico e valutiamo un'altra strada."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Hai un pezzo da ricreare?",
                 "Mandami una foto del pezzo, anche rotto, con un metro accanto. Ti dico in 24/48h se &egrave; ricostruibile."),
    jsonld=service_ld("Reverse engineering",
                      "Ricostruzione del modello CAD di un componente a partire dal pezzo fisico, anche rotto o incompleto, per ricambi non più reperibili.",
                      "servizi/reverse-engineering/"),
))

# ---------------------------------------------------------- 7. PROTOTIPAZIONE RAPIDA
PAGES.append(dict(
    path="servizi/prototipazione-rapida/",
    nav_active="servizi",
    title="Prototipazione rapida con CAD e stampa 3D | Mirandola e Modena",
    ogtitle="Prototipazione rapida &mdash; MakerSolve",
    desc="Prototipi funzionali per verificare ingombri, accoppiamenti e funzione prima di investire in attrezzature definitive. CAD e stampa 3D. Mirandola (MO).",
    hero=hero(
        "Prototipazione rapida",
        "Un prototipo non deve<br><span class=\"grad\">essere bello.</span>",
        "Deve rispondere a una domanda: entra? si monta? tiene? si preme? si usa? "
        "Realizzo prototipi funzionali per verificare forma, ingombri, fori, fissaggi e montaggio prima che le decisioni diventino costose.",
        "Prototipazione rapida",
    ),
    body="\n\n".join([
        section(
            sec_head("A cosa serve", "Quattro domande a cui risponde un prototipo.")
            + cards([
                ("Verifica di accoppiamento", "Il pezzo entra nello spazio disponibile? I fori sono in asse? Gli interassi tornano davvero o solo sul disegno?"),
                ("Prova funzionale", "Il componente fa quello che deve fare quando &egrave; montato e sollecitato, non quando &egrave; fermo su un tavolo."),
                ("Iterazione rapida", "Si corregge il modello e si ristampa. Senza stampi, cambiare idea alla terza versione costa poco."),
                ("Ponte verso la produzione", "Una geometria validata sul campo &egrave; la base per decidere con cognizione se e come industrializzare."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Per chi", "Chi ci guadagna di pi&ugrave;.")
            + pain([
                ("PROFILO 01", "Uffici tecnici e R&amp;D", "Chi deve validare un'idea prima di impegnare capitale in stampi o attrezzature definitive, e ha bisogno di iterare in giorni e non in settimane."),
                ("PROFILO 02", "Manutenzione e officine", "Chi deve rimettere in funzione qualcosa e ha bisogno di provare una soluzione prima di adottarla stabilmente."),
                ("PROFILO 03", "Chi sviluppa un prodotto", "Chi ha bisogno di toccare con mano ergonomia, ingombri e sensazione d'uso prima di congelare il progetto."),
                ("PROFILO 04", "Chi deve convincere qualcuno", "Un pezzo che si passa di mano in riunione sposta pi&ugrave; di venti slide di render."),
            ]),
        ),
        section(
            sec_head("Output", "Fin dove vuoi arrivare.")
            + specs([
                ("Solo prototipo", "Il pezzo da provare, stampato nel materiale pi&ugrave; adatto alla verifica che devi fare."),
                ("Prototipo + revisione CAD", "Il pezzo e il modello aggiornato con le correzioni emerse dalla prova: quello che porti avanti &egrave; una geometria gi&agrave; validata."),
                ("Prototipo + pezzo finale", "Dopo la validazione si produce la versione definitiva, eventualmente in un materiale diverso da quello di prova."),
                ("Materiali tipici", "PLA per le prove puramente dimensionali, PETG e ABS/ASA per le prove funzionali, nylon caricato fibra dove serve rigidit&agrave;, TPU per le parti che devono flettere."),
            ]),
            cls="paper-2",
        ),
    ]),
    cta=cta_band("Hai un'idea da provare?",
                 "Con un file o senza. Mandami cosa deve fare il pezzo e ti rispondo entro 24/48h."),
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
    desc="Componenti su misura quando il pezzo commerciale non esiste, non combacia o costa troppo: supporti, staffe, adattatori, guide, carter, dime e piccoli lotti.",
    hero=hero(
        "Componenti custom",
        "Progettati intorno<br><span class=\"grad\">al tuo problema.</span>",
        "Realizzo componenti su misura quando il pezzo commerciale non esiste, non combacia, costa troppo o richiede una modifica specifica: "
        "supporti, staffe, adattatori, guide, carter, dime, scocche e piccoli lotti.",
        "Componenti custom",
    ),
    body="\n\n".join([
        section(
            sec_head("Cosa realizzo", "Quattro famiglie ricorrenti.")
            + cards([
                ("Supporti e fissaggi", "Staffe e sostegni disegnati sull'oggetto reale e sul punto di ancoraggio disponibile, non adattati da un prodotto generico."),
                ("Adattatori", "Interfacce che collegano due componenti nati per non stare insieme: cambio di attacco, di passo, di diametro o di orientamento."),
                ("Scocche e coperture", "Involucri e carter attorno a componenti esistenti, con accessi, passaggi cavo e ritegni pensati sul contenuto reale."),
                ("Dime e ausili di reparto", "Attrezzature che rendono ripetibile un'operazione oggi affidata alla manualit&agrave; e all'occhio dell'operatore."),
            ], cols=4),
            cls="paper",
        ),
        section(
            sec_head("Quando conviene", "Le condizioni in cui ha senso economico.")
            + pain([
                ("CONDIZIONE 01", "Il ricambio non si trova", "Fuori produzione, oppure venduto solo dentro un assieme che costa molte volte il singolo pezzo che ti serve."),
                ("CONDIZIONE 02", "Serve una geometria diversa", "Il commerciale esiste ma non combacia: attacchi sbagliati, ingombri fuori, interassi che non tornano."),
                ("CONDIZIONE 03", "Serve provare prima", "Non sei ancora sicuro della soluzione e vuoi validarla su un pezzo reale prima di adottarla."),
                ("CONDIZIONE 04", "La quantit&agrave; &egrave; bassa", "Da uno a poche decine di pezzi: numeri in cui attrezzare uno stampo &egrave; fuori discussione."),
            ]),
        ),
        section(
            pain([
                ("APPROCCIO REALISTICO", "Non tutto va stampato in 3D",
                 "Se una lavorazione CNC, un taglio laser, un ricambio commerciale o una soluzione pi&ugrave; semplice sono pi&ugrave; adatti al tuo caso, conviene capirlo prima di spendere. Te lo dico in fase di valutazione, anche quando significa non fare il lavoro."),
                ("QUANTIT&Agrave;", "Dal pezzo singolo alla piccola serie",
                 "Il limite superiore dipende dalla geometria e dal tempo macchina e si valuta sul pezzo specifico. Se i numeri crescono al punto che lo stampaggio conviene, te lo segnalo invece di lasciarti pagare di pi&ugrave;."),
            ]),
            cls="",
        ),
    ]),
    cta=cta_band("Ti serve un pezzo che non esiste?",
                 "Descrivimi il problema, non la soluzione. Al resto ci penso io, e ti rispondo entro 24/48h."),
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
