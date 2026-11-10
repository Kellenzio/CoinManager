# Spese — app personale per le spese

Web app per segnare spese ed entrate, vedere dove vanno i soldi, cosa compri al supermercato e come crescono i tuoi investimenti.
Si installa su telefono o computer come un'app vera (dalla schermata Home o dal browser), senza passare da uno store.
Funziona su iPhone, Android e computer.

## Cosa fa

- **Movimenti**: totale del mese, lista o calendario, scorri a sinistra per eliminare.
  Ogni nuovo inserimento usa il **mese scelto con le frecce** in alto.
  **Selezione multipla**: tieni premuto su un movimento e tocca gli altri; poi elimina a blocco (con «Annulla»),
  assegna una categoria a tutti, cambia la data (o sposta di un mese) o duplicali in un altro mese.
- **Spese a rate**: su qualsiasi spesa scegli «A rate», il numero di rate (2–60) e la cadenza (mensile, bimestrale, trimestrale,
  semestrale, annuale, oppure un numero di mesi a scelta con il tasto **+**). L'app divide il totale e inserisce subito ogni rata nel mese giusto,
  nella categoria scelta. Aprendo una rata puoi cambiarla da sola oppure modificare **tutte le rate** (numero, cadenza, totale): vengono ricalcolate da capo.
- **Investimenti**: scheda dedicata ai piani di accumulo (PAC) in fondi, ETF, obbligazioni o altro. Per ogni piano imposti importo, frequenza
  (mensile, bimestrale, trimestrale, semestrale, annuale o a mano), mese di partenza e versamento iniziale.
  I **versamenti automatici** vengono registrati dall'app nel giorno stabilito, come un addebito della banca, senza raddoppiare ciò che hai inserito a mano.
  Se cambi la cifra, vale **da un mese in poi** e i mesi passati restano com'erano. Vedi totale investito, grafico degli ultimi 12 mesi
  e, se inserisci ogni tanto il valore attuale, guadagno e rendimento. Eliminando un piano spariscono anche i suoi versamenti (con «Annulla»).
- **Report**: mese e anno, «In breve», categorie, grafici, spese più grandi, esportazione PDF/CSV.
- **Spesa**: cosa compri al supermercato, per categoria e per prodotto, e quanto risparmi con gli sconti.
- **Categorie**: macro categorie e sottocategorie personalizzabili, con icona, colore e budget mensile.
  Il **budget condiviso** vale per più categorie insieme (per esempio Svago e Shopping): in ognuna vedi la somma raggiunta sul totale, tipo *270 / 350 €*.
- **Scontrini**: foto, PDF dello scontrino digitale (es. app Coop) o inserimento a mano.
  La lettura usa l'IA di Anthropic (serve una tua chiave API, a pagamento ma costa pochi centesimi).
  I prodotti poco chiari vengono chiesti una volta e poi ricordati.
- **Backup automatico** su un tuo repository GitHub privato (facoltativo), con elenco delle **versioni precedenti** da cui ripristinare.
- **Non perdi quello che stai scrivendo**: se esci dall'app per copiare un testo da un'altra (o il telefono la scarica dalla memoria),
  al ritorno ritrovi la scheda con i campi come li avevi lasciati. L'app non si ricarica mai mentre stai modificando qualcosa.
- **Tasto indietro** del telefono (o gesto indietro): torna al menu precedente; da Movimenti chiede se vuoi uscire dall'app.
- Temi: Nero OLED e Carta. Stili del testo: Morbido, Chiaro, Editoriale, Tecnico, Deciso, Classico.

## Com'è fatta

Un solo file `index.html` (HTML + CSS + JavaScript, niente librerie, niente server).
I dati restano sul dispositivo (localStorage del browser). Le uniche connessioni esterne sono:
api.anthropic.com (lettura scontrini), api.github.com (backup), Google Fonts (caratteri); una Content Security Policy impedisce tutto il resto.
Ogni dato in ingresso (file di backup, backup GitHub, dati già salvati) viene validato e ripulito prima di essere usato.

## Come metterla online (GitHub Pages, gratis)

1. Crea un account su github.com (se non ce l'hai).
2. Crea un repository **pubblico**, per esempio `Spese`, e carica tutti i file di questa cartella.
3. Nel repository: Settings → Pages → Source: "Deploy from a branch" → branch `main`, cartella `/ (root)` → Save.
4. Dopo un paio di minuti l'app è su `https://TUO-UTENTE.github.io/Spese/index.html`.
5. Installala:
   - **iPhone**: apri il link con **Safari** → Condividi → **Aggiungi alla schermata Home**.
   - **Android**: apri il link con **Chrome** → menu ⋮ → **Installa app** (o *Aggiungi a schermata Home*).
   - **Computer** (Chrome o Edge): icona di installazione nella barra degli indirizzi.

Gli aggiornamenti arrivano da soli: l'app controlla `version.json` e, quando c'è una versione nuova, si ricarica
(mai mentre hai una scheda di modifica aperta). Se modifichi `index.html` a mano, esegui poi **`python3 build.py`**:
aggiorna il numero di versione (`BUILD` e `version.json`) **e gli hash della Content Security Policy**.
Senza quel passaggio il browser blocca lo script e l'app resta vuota.

## Primo avvio

- Se vuoi vederla piena, al primo avvio tocca "Prova con dati di esempio" (o in ⚙️ → *I tuoi dati* → "Carica dati di esempio"); poi puoi cancellarli.
- **Lettura scontrini**: crea una chiave su platform.claude.com (Billing → aggiungi credito; API keys → Create key)
  e incollala in ⚙️ → *Lettura scontrini*. Consiglio: imposta un limite di spesa basso sulla chiave.
- **Backup su GitHub** (facoltativo): crea un repository **privato** `spese-backup`, poi un token
  *fine-grained* che può accedere **solo** a quel repository, permesso *Contents: Read and write*, con scadenza.
  Inseriscili in ⚙️ → *Backup automatico su GitHub*. Le istruzioni sono anche dentro l'app.
  Dopo il collegamento ogni modifica viene copiata da sola; in ⚙️ → *Versioni precedenti* scegli un momento salvato e ripristinalo
  (l'elenco funziona anche col repository privato, senza accedere a GitHub dal browser).
- **Più dispositivi**: collega lo stesso repository di backup anche sull'altro dispositivo e carica i dati già presenti.
  I dati non si sincronizzano in tempo reale: ogni dispositivo li copia nel backup quando li modifichi.

Chiave e token restano solo sul dispositivo e non finiscono mai nel backup.

## Se usi Claude per modificarla

Dai a Claude questa cartella: il file `CLAUDE.md` gli spiega com'è fatta l'app e cosa controllare
(dati, investimenti, rate, budget condivisi, tasto indietro, bozza, sicurezza e `build.py`).
