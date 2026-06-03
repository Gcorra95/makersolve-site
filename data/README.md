# MakerSolve — dati modificabili

Questa cartella contiene i dati ricorrenti del sito.

## File principale

Modifica questo file:

```txt
data/site-config.js
```

## Campi utili

```js
email: "info@makersolve.com"
```

Cambia qui la mail mostrata nelle pagine e nei link email.

```js
phoneDisplay: ""
phoneHref: ""
```

Per mostrare il telefono:

```js
phoneDisplay: "+39 333 1234567"
phoneHref: "+393331234567"
```

Se lasci entrambi vuoti, il blocco telefono viene nascosto automaticamente dove previsto.

```js
vatNumber: ""
```

Per mostrare la P.IVA:

```js
vatNumber: "01234567890"
```

Se lasci vuoto, la P.IVA viene nascosta dove previsto.

```js
city: "Mirandola"
province: "MO"
region: "Emilia-Romagna"
serviceArea: "Mirandola, Modena, Emilia-Romagna, Nord Italia"
```

Questi campi aggiornano i riferimenti visibili al territorio.

## Nota importante SEO

Questa configurazione aggiorna i dati visibili nel sito tramite JavaScript.

Per dati SEO critici come `title`, `meta description`, `canonical` e JSON-LD, al momento i valori restano scritti direttamente nelle singole pagine HTML. È meglio così su GitHub Pages senza sistema di build, perché Google legge più chiaramente i dati già presenti nell'HTML.
