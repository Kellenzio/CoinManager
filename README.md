# Spese — app personale per le spese (iPhone)

Web app per segnare spese ed entrate, vedere dove vanno i soldi e cosa compri al supermercato.
Si installa sull'iPhone come un'app vera (dalla schermata Home), senza App Store.

## Cosa fa

- **Movimenti**: totale del mese, lista o calendario, scorri a sinistra per eliminare.
- **Report**: mese e anno, "In breve", categorie, grafici, spese più grandi, esportazione PDF/CSV.
- **Spesa**: cosa compri al supermercato, per categoria e per prodotto, e quanto risparmi con gli sconti.
- **Categorie**: macro categorie e sottocategorie personalizzabili, con icona, colore e budget.
- **Scontrini**: foto, PDF dello scontrino digitale (es. app Coop) o inserimento a mano.
  La lettura usa l'IA di Anthropic (serve una tua chiave API, a pagamento ma costa pochi centesimi).
  I prodotti poco chiari vengono chiesti una volta e poi ricordati.
- **Backup automatico** su un tuo repository GitHub privato (facoltativo).
- Temi: Nero OLED e Carta. Stili del testo: Morbido, Chiaro, Editoriale, Tecnico, Deciso, Classico.

## Com'è fatta

Un solo file `index.html` (HTML + CSS + JavaScript, niente librerie, niente server).
I dati restano sul telefono (localStorage del browser). Le uniche connessioni esterne sono:
api.anthropic.com (lettura scontrini), api.github.com (backup), Google Fonts (caratteri).

## Come metterla online (GitHub Pages, gratis)

1. Crea un account su github.com (se non ce l'hai).
2. Crea un repository **pubblico**, per esempio `Spese`, e carica tutti i file di questa cartella.
3. Nel repository: Settings → Pages → Source: "Deploy from a branch" → branch `main`, cartella `/ (root)` → Save.
4. Dopo un paio di minuti l'app è su `https://TUO-UTENTE.github.io/Spese/index.html`.
5. Sull'iPhone aprila con **Safari** → Condividi → **Aggiungi alla schermata Home**.

Gli aggiornamenti arrivano da soli: quando cambi `index.html`, cambia anche il numero in `const BUILD = "…"`
e scrivi lo stesso numero in `version.json`; l'app se ne accorge e si ricarica.

## Primo avvio

- Se vuoi vederla piena, al primo avvio tocca "Prova con dati di esempio" (o in ⚙️ → *I tuoi dati* → "Carica dati di esempio"); poi puoi cancellarli.
- **Lettura scontrini**: crea una chiave su platform.claude.com (Billing → aggiungi credito; API keys → Create key)
  e incollala in ⚙️ → *Lettura scontrini*. Consiglio: imposta un limite di spesa basso sulla chiave.
- **Backup su GitHub** (facoltativo): crea un repository **privato** `spese-backup`, poi un token
  *fine-grained* che può accedere **solo** a quel repository, permesso *Contents: Read and write*, con scadenza.
  Inseriscili in ⚙️ → *Backup automatico su GitHub*. Le istruzioni sono anche dentro l'app.

Chiave e token restano solo sul telefono e non finiscono mai nel backup.

## Se usi Claude per modificarla

Dai a Claude questa cartella: il file `CLAUDE.md` gli spiega com'è fatta l'app e cosa controllare.
