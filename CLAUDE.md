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
  **Ogni volta che modifichi l'app esegui `python3 build.py`**: scrive lo stesso valore (`AAAAMMGGhhmmss`) in entrambi
  e aggiorna la CSP, altrimenti il telefono non si aggiorna (o l'app non parte).

## iPhone: cose già risolte, da non rompere

- Status bar `black` (non translucent) e altezza con `100dvh`; `fitApp()` calcola `--bot` (spazio sotto) con un elemento sonda.
- L'utente originale usa lo **Zoom schermo** di iOS: la larghezza utile è **320 px**. Prova sempre anche a 320×645
  (c'è una media query `max-width:360px` per gli schermi stretti).
- Input con `font-size:16px` per evitare lo zoom automatico di Safari. Tastierino numerico interno per gli importi.

## Sicurezza (corretta il 05/11/2026)

- **Validazione**: `sanitize(d)` (prima di `fresh()`) è l'unico punto d'ingresso dei dati: dati già salvati al caricamento,
  file di backup (`restore`), backup GitHub (`ghRead`) e `applyData`. Scarta campi sconosciuti, rigenera gli id non validi
  (`^[a-z0-9_.-]{1,64}$`) aggiornando i riferimenti (cat/sub dei movimenti), controlla date `YYYY-MM-DD` reali, importi,
  `type` in/out, colori (-1…7 o `#rrggbb`), icone presenti in `ICONS`, id categoria prodotto, `learn` e `names`.
  Se i dati salvati sono illeggibili ne resta una copia in `localStorage["spese.data.bad"]` prima di ripartire da zero.
  Un backup GitHub non valido non viene mai applicato (`ghRead` restituisce `bad: true`).
- **Backup**: `snapshot()` e `applyData()` includono anche `learn` e `names` (un vecchio backup senza questi campi li lascia invariati).
- **Attributi HTML**: gli id nei `data-*` e `value` passano da `esc()`. Quando aggiungi un nuovo attributo con un id o un testo
  dei dati, usa sempre `esc()`.
- **CSP** in `<meta>` con gli **hash SHA-256 dei due script inline** (niente `unsafe-inline` per gli script: un handler o uno
  script iniettato non parte). `connect-src` solo `'self'`, api.anthropic.com e api.github.com (+ `data:`/`blob:` per le immagini incollate).
  **Dopo ogni modifica a `index.html` esegui `python3 build.py`**: aggiorna `BUILD`, `version.json` e gli hash della CSP
  (sostituisce la regola "aggiorna BUILD e version.json a mano"). Non usare attributi `onclick=`/`onerror=` né script esterni.
- **Ancora aperto**: le chiavi (`spese.ai`, `spese.gh`) stanno nel localStorage, condiviso da tutte le pagine sotto lo stesso
  `utente.github.io`. Per isolarlo serve un dominio o sottodominio dedicato.

## Come lavorare

- Modifiche piccole e mirate con il resto del file intatto; dopo ogni modifica verifica che lo script sia valido
  e prova le schermate (Movimenti, Report, Spesa, Categorie, nuova spesa, impostazioni) in entrambi i temi.
- Testi rivolti all'utente in italiano, brevi e chiari.
