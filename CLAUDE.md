# Note per Claude — progetto "Spese"

PWA personale per iPhone per il tracciamento delle spese. Tutto in **un solo file `index.html`**
(vanilla JS + CSS, nessuna dipendenza, nessun build). Lingua dell'interfaccia: **italiano**.
Pubblicata su GitHub Pages, installata dalla schermata Home di Safari (modalità standalone).

## Primo setup con l'utente

1. Aiutalo a creare un repo pubblico su GitHub con questi file e ad attivare GitHub Pages (branch `main`, root).
2. Link da aprire: `https://UTENTE.github.io/REPO/index.html` (con `/index.html`: `start_url` del manifest è `./index.html`).
3. Facoltativo: chiave API Anthropic (lettura scontrini) e backup GitHub (repo privato + token fine-grained
   limitato a quel solo repo, Contents read/write, con scadenza). Entrambi si inseriscono in ⚙️ dall'app.
4. Non chiedere mai all'utente di incollare chiave o token in chat: vanno inseriti solo nell'app.

## Struttura del codice

- **Dati**: `localStorage["spese.data"]` → `D = { v, cats, tx, opt, learn, names, updated }`.
  - `cats[]`: `{ id, name, color (0–7 = palette del tema, oppure "#hex"), icon, type: "out"|"in", budget (centesimi), fallback, subs: [{ id, name }] }`
  - `tx[]`: `{ id, type, cat, sub, amt (centesimi), date "YYYY-MM-DD", note, ts, items?, sc? }`
    - `items[]` (prodotti dello scontrino): `{ n nome, r testo grezzo, p prezzo pagato in centesimi, sc, c categoria prodotto }`
    - `sc`: sconti totali dello scontrino in centesimi, **scritti dall'utente** (non letti dall'IA).
  - `learn`: nome prodotto normalizzato → categoria prodotto. `names`: riga grezza dello scontrino → `{ n, c }`.
  - `migrate()` porta i dati vecchi alla versione corrente; `save()` aggiorna `D.updated` e pianifica il backup.
- **Altre chiavi localStorage**: `spese.theme`, `spese.look`, `spese.ai` (chiave Anthropic), `spese.gh` (token GitHub).
- **Stato UI**: oggetto `S` (scheda, mese, viste). `render()` ridisegna la scheda attiva:
  `vTx` Movimenti, `vReport` Report (mese/anno), `vShop` Spesa (prodotti), `vCats` Categorie.
  I fogli a tutto schermo (`.sheet`) si aprono con `open("#id")` e si chiudono con `close()` (il più in alto).
- **Click**: un unico listener su `document` che legge i `data-*` dei bottoni e lo `switch (d.act)`.
- **Temi**: `data-theme` su `<html>` (`oled`, `carta`); **stili del testo**: `data-look` (`morbido` predefinito,
  `chiaro`, `editoriale`, `tecnico`, `deciso`; `classico` = nessun attributo). Font da Google Fonts, caricati su richiesta.
- **Colori categorie**: palette Flat UI in `--c1…--c8` (uguale in tutti i temi).
- **Scontrini con IA**: `aiReceiptSmart` → `aiReceipt` chiama `api.anthropic.com/v1/messages` direttamente dal browser
  (header `anthropic-dangerous-direct-browser-access`), con tool `scontrino`. Modelli in `AI_MODELS`
  (modalità eco/top/auto). Accetta foto (ritagliate a strisce ad alta risoluzione) e PDF.
  Dopo la lettura: procedura guidata per i prodotti poco chiari, poi l'utente scrive totale e sconti.
- **Backup GitHub**: `ghCheck`, `backupNow`, `scheduleBackup`, `ghRestore` (API Contents, file `spese.json`).
- **Auto-aggiornamento**: costante `BUILD` in `index.html` + `version.json` (`{"v": BUILD}`).
  **Ogni volta che modifichi l'app aggiorna entrambi con lo stesso valore** (es. data e ora `AAAAMMGGhhmmss`),
  altrimenti il telefono non si aggiorna.

## iPhone: cose già risolte, da non rompere

- Status bar `black` (non translucent) e altezza con `100dvh`; `fitApp()` calcola `--bot` (spazio sotto) con un elemento sonda.
- L'utente originale usa lo **Zoom schermo** di iOS: la larghezza utile è **320 px**. Prova sempre anche a 320×645
  (c'è una media query `max-width:360px` per gli schermi stretti).
- Input con `font-size:16px` per evitare lo zoom automatico di Safari. Tastierino numerico interno per gli importi.

## Sicurezza: da sistemare (segnalato da una revisione, non ancora corretto)

1. **XSS da backup**: in vari punti gli id finiscono negli attributi senza `esc()` (`data-cat="${c.cat.id}"`,
   `data-tx`, `data-del`, `data-pick`, `data-psub`, `data-id`…), e `applyData()`/`restore()` controllano solo che
   `cats` e `tx` siano array. Correzione: passare tutti gli id da `esc()` e **validare/sanificare** ogni backup
   (id `^[a-z0-9_-]+$` altrimenti rigenerati con riferimenti aggiornati, date `YYYY-MM-DD`, importi interi,
   `type` in/out, colori numero 0–7 o `#rrggbb`, campi sconosciuti scartati), anche per i dati già salvati.
   Includere `learn` e `names` nel ripristino (oggi vanno persi).
2. **CSP** in un `<meta>`: `connect-src 'self' https://api.anthropic.com https://api.github.com`, font da Google.
3. Chiavi in localStorage: tutte le app pubblicate sotto lo stesso `utente.github.io` condividono l'origine.
   Per isolarla serve un dominio/sottodominio dedicato.

## Come lavorare

- Modifiche piccole e mirate con il resto del file intatto; dopo ogni modifica verifica che lo script sia valido
  e prova le schermate (Movimenti, Report, Spesa, Categorie, nuova spesa, impostazioni) in entrambi i temi.
- Testi rivolti all'utente in italiano, brevi e chiari.
