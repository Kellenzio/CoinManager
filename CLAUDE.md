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

- **Dati**: `localStorage["spese.data"]` → `D = { v, cats, tx, opt, inv, groups, learn, names, updated }` (versione dati `v` = 3).
  - `cats[]`: `{ id, name, color (0–7 = palette del tema, oppure "#hex"), icon, type: "out"|"in", budget (centesimi), fallback, subs: [{ id, name }] }`
  - `tx[]`: `{ id, type, cat, sub, amt (centesimi), date "YYYY-MM-DD", note, ts, items?, sc? }`
    - `items[]` (prodotti dello scontrino): `{ n nome, r testo grezzo, p prezzo pagato in centesimi, sc, c categoria prodotto }`
    - `sc`: sconti totali dello scontrino in centesimi, **scritti dall'utente** (non letti dall'IA).
  - `learn`: nome prodotto normalizzato → categoria prodotto. `names`: riga grezza dello scontrino → `{ n, c }`.
  - `migrate()` porta i dati vecchi alla versione corrente; `save()` aggiorna `D.updated` e pianifica il backup.
- **Altre chiavi localStorage**: `spese.theme`, `spese.look`, `spese.ai` (chiave Anthropic), `spese.gh` (token GitHub).
- **Stato UI**: oggetto `S` (scheda, mese, viste). `render()` ridisegna la scheda attiva:
  `vTx` Movimenti, `vReport` Report (mese/anno), `vShop` Spesa (prodotti), `vInv` Investi (piani di accumulo), `vCats` Categorie.
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

## Investimenti (scheda «Investi», dal 06/11/2026)

- **Modello**: la categoria di spesa `invest` («Investimenti», icona `grafico`, non eliminabile; `ensureInvest()` la crea o adotta una
  categoria che si chiama già così). **Ogni piano è una sottocategoria di `invest`**; i versamenti sono normali movimenti
  (`cat:"invest"`, `sub:idPiano`), quindi compaiono in Movimenti, Report e CSV. I dettagli del piano stanno in
  `D.inv.plans[idSottocategoria] = { kind: fondo|etf|obbl|altro, amt (centesimi), freq: m|b|q|s|a|l, start "AAAA-MM", auto?, day?, gen?, hist?, val?, vald?, closed }`
  (`val` = valore attuale scritto dall'utente, per guadagno e rendimento). Un piano senza dettagli ha valori di default.
- **Codice**: blocco «Investimenti» prima di `openTx` (`invPlans`, `renderInv`, `openPlan/drawPlan/savePlan/delPlan`, `invPay`, `invAdd`).
  Il foglio `#sPlan` si apre con `open("#sPlan")`. «Versa» apre il foglio del movimento già compilato (importo, categoria, piano).
  Il pulsante + sulla scheda Investi precompila la categoria Investimenti.
- **PAC automatici**: un piano con `auto: true` (+ `day` 1–31) viene registrato da `autoPac()` (chiamata all'inizio di `render()` e quando l'app torna in primo
  piano): per ogni mese previsto, dal primo versamento fino a oggi, crea un movimento `{auto:true, note:"Versamento automatico"}` nel giorno indicato.
  `plan.gen` = ultimo mese elaborato (un versamento eliminato non torna); non raddoppia ciò che è già stato registrato a mano nello stesso mese.
  Il versamento iniziale è un movimento con `ini:true`: conta nel totale versato ma non come rata del mese. Frequenze: m, b (2 mesi), q, s (6), a (12), l (a mano).
- **Cambio importo**: `plan.hist = [{from:"AAAA-MM", amt}]` (la voce di base ha `from:"0000-01"`); `amtAt(piano, mese)` dà l'importo di ogni mese.
  Il foglio del piano chiede «Se cambi l'importo, vale dal mese»: i movimenti automatici da quel mese in poi si aggiornano, i mesi passati restano invariati.

## Spese a rate (qualsiasi spesa in uscita)

- Nel foglio «Nuova spesa», campo **Pagamento → A rate** (numero di rate 2–60, cadenza mensile/bimestrale/trimestrale/semestrale/annuale; `S.edit.rate`).
  L'importo scritto è il **totale**: `saveTx()` lo divide con `splitRates()` (l'eventuale resto di centesimi va sull'ultima rata) e crea subito tutti i movimenti,
  con date calcolate da `shiftDate()` (stesso giorno, o ultimo del mese se più corto), ciascuno con `inst: { g (gruppo), i, n, tot }`. La prima rata è alla data scelta.
- Le rate future compaiono nei mesi successivi: le frecce del mese arrivano fino all'ultimo mese con movimenti (`lastMonth()`).
  In Movimenti la riga mostra «rata 2/3». Aprendo una rata si modifica solo quella; «Elimina tutte le rate» (`delRate`) cancella l'intero gruppo.
  Non disponibile per le spese con scontrino letto dall'IA.
- **Migrazione**: `migrate()` porta i dati a `v: 3` (aggiunge la categoria e `inv`). `sanitize()` valida anche `inv`
  (i piani esistono solo se esiste la sottocategoria, ids rimappati come per le categorie).
- **Versamenti automatici**: `plan.auto` + `plan.day` (giorno del mese). `autoPac()` (chiamata all'inizio di `render()` e al ritorno in primo piano)
  registra i versamenti dovuti fino a oggi (`tx.auto: true`, nota «Versamento automatico»). `plan.gen` = ultimo mese già elaborato: un versamento
  eliminato a mano non viene ricreato; se nel mese c'è già un versamento manuale non lo raddoppia (aggiunge solo la differenza). Frequenze: m, b, q, s, a, l (a mano).
- **Cambio di importo**: `plan.hist = [{from:"AAAA-MM", amt}]`; `amtAt(piano, mese)` dà l'importo valido in quel mese. Dal foglio del piano si sceglie da quale mese vale la nuova cifra:
  i versamenti automatici da quel mese in poi vengono aggiornati, i mesi passati non si toccano.
- **Movimenti**: nella card in alto compare «Di cui investiti» (gli investimenti restano nel totale delle uscite: sono soldi che escono dal conto).
- **Barra in basso**: 5 schede della stessa larghezza; il + è un pulsante tondo fisso in basso a destra sopra la barra (solo sotto i 900 px;
  su PC resta nella barra laterale). Etichetta «Investi» (corta per i 320 px).

## Spese a rate

- Nel foglio di una **nuova** spesa (non per gli scontrini) c'è «Pagamento: In una volta / A rate». Si sceglie il numero di rate (2–60) e la cadenza
  (mensile, bimestrale, trimestrale, semestrale, annuale). L'importo scritto è il **totale**: `splitRates()` lo divide (il resto dei centesimi va sull'ultima rata)
  e `saveTx()` crea subito tutte le rate come normali movimenti, nella stessa categoria/sottocategoria, a partire dalla data scelta (`shiftDate()`: stesso giorno, ultimo giorno nei mesi corti).
- Ogni rata ha `tx.inst = { g (gruppo), i, n, tot }`; nella riga compare «rata i/n». Nel foglio di una rata si modifica solo quella; «Elimina tutte le rate» cancella l'intero gruppo (`delRate`).
- Le frecce del mese permettono di andare avanti fino all'ultimo mese con movimenti (`lastMonth()`), per vedere le rate future.

## Selezione multipla (scheda Movimenti)

- **Tieni premuto ~0,5 s** su un movimento (`pointerdown` + timer, annullato se il dito si muove) per entrare in `S.sel` (un `Set` di id; `body.selmode`).
  Da lì un tocco seleziona/deseleziona (CSS: spunta sull'icona, riga evidenziata). Barra in alto `#selbar` (✕, conteggio e somma, Tutti/Nessuno) e barra in basso
  `#selact` (Categoria, Data, Duplica, Elimina) sostituiscono header e menu; il + è nascosto. Il click che segue la pressione lunga viene ignorato (`S.noClick`).
- **Azioni**: Elimina (con «Annulla»), Categoria e sottocategoria uguali per tutti (solo se tutti spese o tutte entrate), Data (nuova data per tutti, oppure ±1 mese),
  Duplica in un altro mese (copie come spese normali). Il foglio `#sBulk` (`openBulk`/`drawBulk`/`bulkApply`/`bulkShift`) le gestisce. Esce con ✕, Esc o a fine azione.
- Una tantum compare un suggerimento («Tieni premuto…», `D.opt.seenSel`).

## Mese selezionato

Qualsiasi nuovo inserimento usa il **mese scelto con le frecce** (`S.month`): nuova spesa (primo del mese, oppure oggi se è il mese in corso), piani PAC
(mese di partenza, «vale dal mese», data del versamento iniziale), «Versa». Nelle rate la cadenza può essere personalizzata (+ → ogni N mesi, 1–36).

## Budget condivisi

- `D.groups = [{ id, name, amt (centesimi al mese), cats: [idCategoria] }]` (almeno 2 categorie di spesa, una categoria in un solo gruppo; `sanitize()` e `pruneGroups()` lo garantiscono).
  Per le categorie di un gruppo conta solo il budget del gruppo: `budgetOf(cat, st, amt)` restituisce `{ b, spent, g }` (spent = somma delle spese di tutte le categorie del gruppo nel mese).
  Mostrato come «270 / 350 € di budget» in Categorie, Report (righe «Dove hai speso»), riepilogo categoria, e negli spunti («Oltre il budget»).
- Gestione: Categorie → «Budget condivisi» → foglio `#sGroup` (`openGroup/drawGroup/saveGroup/delGroup`). Nell'editor di una categoria in un gruppo il campo budget è sostituito dal collegamento al gruppo.

## Bozza e aggiornamenti

- `saveDraft()` (a ogni modifica con debounce, ogni 3 s con un foglio aperto, quando l'app va in secondo piano) salva in `localStorage["spese.draft"]` i fogli di modifica aperti
  (movimento, categoria, piano, budget condiviso) con i campi già scritti; `restoreDraft()` li riapre all'avvio (max 12 ore). Non salva mai chiavi/token delle impostazioni.
  La bozza si cancella quando il foglio si chiude (in `render()`).
- `checkUpdate()` **non ricarica la pagina** se c'è un foglio aperto o una selezione in corso: riprova al controllo successivo.
- Eliminare un piano (o la sua sottocategoria in Investimenti) elimina anche tutti i suoi versamenti (con «Annulla» dal foglio del piano).

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
