# Guida all'Utilizzo - SongStructurer

## Indice
1. [Interfaccia Principale](#interfaccia-principale)
2. [Caricamento File Audio](#caricamento-file-audio)
3. [Analisi Automatica dei Segmenti](#analisi-automatica-dei-segmenti)
4. [Riproduzione Audio](#riproduzione-audio)
5. [Modifica dei Segmenti](#modifica-dei-segmenti)
6. [Controlli di Navigazione](#controlli-di-navigazione)
7. [Esportazione Dati](#esportazione-dati)
8. [Suggerimenti Avanzati](#suggerimenti-avanzati)

## Interfaccia Principale

L'interfaccia è divisa in diverse sezioni:

### Barra dei Controlli Superiori
- **Progress Bar**: Mostra l'avanzamento della riproduzione
- **Etichetta Tempo**: Display del tempo corrente e totale
- **Slider di Trasporto**: Navigazione interattiva nel segmento

### Pannello dei Pulsanti
- `Carica file audio` - Apri un file audio
- `Analizza segmenti` - Analisi automatica della struttura
- `Ascolta segmento` - Riproduci il segmento selezionato
- `Ferma riproduzione` - Interrompi la riproduzione
- `Rinomina segmento` - Modifica il nome del segmento
- `Unisci segmenti selezionati` - Combina più segmenti
- `Esporta segmenti CSV` - Salva i dati dei segmenti
- `Esporta immagine PNG` - Salva l'immagine del waveform

### Visualizzazione Waveform
- **Onda sonora**: Visualizzazione grafica dell'audio
- **Segmenti colorati**: Aree arancioni che rappresentano i segmenti
- **Linee blu**: Bordi dei segmenti modificabili
- **Cursore rosso**: Posizione corrente durante la riproduzione

### Lista Segmenti
- Elenco di tutti i segmenti identificati
- Selezione multipla possibile con Ctrl+Click

## Caricamento File Audio

### Procedura
1. Clicca il pulsante **"Carica file audio"**
2. Seleziona un file MP3, WAV o FLAC dal browser
3. Attendi il caricamento e la visualizzazione del waveform

### Note
- I file di grandi dimensioni potrebbero richiedere qualche secondo per il caricamento
- La waveform viene automaticamente ridimensionata per ottimizzare le prestazioni
- L'intera durata del file viene visualizzata inizialmente

## Analisi Automatica dei Segmenti

### Funzionamento
1. Clicca **"Analizza segmenti"** dopo il caricamento
2. L'algoritmo analizza il ritmo e i beat della traccia
3. I segmenti vengono creati con lunghezza minima di 8 secondi
4. I segmenti vengono visualizzati come aree arancioni sul waveform

### Personalizzazione
- I segmenti vengono automaticamente denominati "segment_0", "segment_1", ecc.
- È possibile rinominarli successivamente
- I bordi dei segmenti possono essere spostati tramite drag-and-drop

## Riproduzione Audio

### Ascolto di un Segmento
1. Seleziona un segmento dalla lista
2. Clicca **"Ascolta segmento"**
3. Utilizza i controlli di trasporto per navigare

### Controlli di Riproduzione
- **Progress Bar**: Mostra l'avanzamento nel segmento
- **Slider**: Trascina per cercare posizioni specifiche
- **Pulsante Stop**: Interrompe immediatamente la riproduzione

### Funzionalità Avanzate
- Il cursore rosso si muove in tempo reale durante la riproduzione
- Lo slider è interattivo e permette il seeking preciso
- Il tempo rimanente viene visualizzato in formato MM:SS

## Modifica dei Segmenti

### Rinominare un Segmento
1. Seleziona un segmento dalla lista
2. Clicca **"Rinomina segmento"**
3. Inserisci il nuovo nome nella finestra di dialogo
4. Conferma con OK

### Unire Segmenti
1. Seleziona più segmenti dalla lista (Ctrl+Click)
2. Clicca **"Unisci segmenti selezionati"**
3. Inserisci un nome per il nuovo segmento unito
4. I segmenti selezionati verranno combinati in uno solo

### Modifica Manuale dei Bordi
1. Posiziona il mouse sul bordo di un segmento (linea blu)
2. Quando il cursore cambia, clicca e trascina
3. Rilascia per confermare la nuova posizione

### Limitazioni
- I segmenti non possono sovrapporsi
- La lunghezza minima di un segmento è di 0.01 secondi
- I segmenti adiacenti mantengono un margine di sicurezza

## Controlli di Navigazione

### Zoom
- **Slider Zoom**: Regola lo zoom da 1% a 10000%
- **Campo di Input**: Inserisci valori precisi e premi Invio
- **Scroll Orizzontale**: Naviga quando lo zoom è attivo

### Scorciatoie
- Utilizza lo slider orizzontale sotto il waveform per panoramizzare
- Clicca e trascina sul waveform per un controllo più fine (se implementato)

### Reset Visualizzazione
- Il pulsante "Carica file audio" resetta anche la visualizzazione
- Lo zoom torna automaticamente al 100% al caricamento

## Esportazione Dati

### Esportazione CSV
1. Clicca **"Esporta segmenti CSV"**
2. Scegli la cartella di destinazione
3. Assegna un nome al file
4. I dati includono: Inizio, Fine, Etichetta per ogni segmento

### Formato CSV
```csv
Start,End,Label
00:00,01:30,intro
01:30,03:15,verse
```
### Esportazione Immagine PNG
1. Clicca **"Esporta immagine PNG"**
2. Scegli la cartella di destinazione e assegna un nome al file
3. Conferma l'operazione
4. L'applicazione esporterà automaticamente un'immagine dell'intero waveform

### Caratteristiche dell'Esportazione PNG
- **Risoluzione**: Immagine ad alta risoluzione basata sulle dimensioni del canvas
- **Contenuto**: Tutti i segmenti identificati con le relative etichette
- **Visualizzazione**: Mostra l'intera durata del file audio con la segmentazione completa
- **Formato**: PNG a piena risoluzione per stampe e documentazione professionale

## Suggerimenti Avanzati

### Ottimizzazione Prestazioni
- **File Lunghi**: Per brani superiori a 10 minuti, utilizza lo zoom per navigare più velocemente
- **Analisi Ritmica**: L'analisi è più precisa su brani con beat marcato (pop, rock, elettronica)
- **Formati Audio**: I file WAV generalmente processano più velocemente dei MP3 compressi
- **Memoria RAM**: Chiudi altre applicazioni pesanti durante l'analisi di file di grandi dimensioni

### Best Practices per il Lavoro
- **Nomenclatura Segmenti**: Usa nomi standard come "intro", "verse", "chorus", "bridge", "outro"
- **Verifica Manuale**: Controlla sempre l'accuratezza dell'analisi automatica con l'ascolto
- **Backup Regolari**: Esporta periodicamente i dati CSV per non perdere le modifiche
- **Organizzazione**: Crea una cartella dedicata per ogni progetto musicale

### Risoluzione Problemi Comuni

**Problema**: L'analisi automatica non trova segmenti
- **Soluzione**: Il brano potrebbe avere ritmo poco definito o tempo variabile
- **Alternativa**: Prova con un file diverso o crea i segmenti manualmente trascinando i bordi

**Problema**: La riproduzione audio non funziona
- **Soluzione**: Verifica che l'audio di sistema sia attivo e il volume non sia muto
- **Controllo**: Assicurati che i driver audio siano aggiornati e funzionanti

**Problema**: L'applicazione diventa lenta con file grandi
- **Soluzione**: Riduci lo zoom al 100% e utilizza lo scroll per navigare
- **Ottimizzazione**: Chiudi altre applicazioni per liberare memoria RAM

**Problema**: Impossibile salvare i file esportati
- **Soluzione**: Verifica i permessi di scrittura nella cartella selezionata
- **Workaround**: Prova a salvare in un'altra cartella (es. Desktop o Documenti)

**Problema**: I segmenti non si muovono correttamente
- **Soluzione**: Assicurati di cliccare esattamente sulle linee blu dei bordi
- **Precisione**: Usa lo zoom per posizionarti con maggiore accuratezza

### Suggerimenti Creativi e Professionali

**Analisi Strutturale**
- Identifica pattern ripetuti nella canzone per strutturare arrangiamenti
- Confronta la struttura di diverse versioni dello stesso brano
- Analizza l'evoluzione della struttura in album consecutivi

**Applicazioni Pratiche**
- **Produzione Musicale**: Esporta i segmenti per usarli in DAW (Digital Audio Workstation)
- **Analisi Accademica**: Studia le strutture formali di generi musicali diversi
- **DJ Set**: Prepara cue points basati sulla struttura del brano
- **Didattica**: Insegna struttura musicale attraverso esempi concreti

**Workflow Ottimizzato**
1. Carica il brano e analizza automaticamente
2. Ascolta ogni segmento per verificarne l'accuratezza
3. Rinomina i segmenti secondo la nomenclatura standard
4. Regola manualmente i bordi per precisione millimetrica
5. Esporta CSV per uso in altri software
6. Esporta PNG per documentazione e presentazioni

**Integrazione con Altri Software**
- **DAW**: Importa i timestamp CSV come marker di sessione
- **Notazione**: Usa la struttura per analisi armoniche e melodiche
- **Video**: Sincronizza editing video con la struttura musicale identificata

### Manutenzione e Aggiornamenti

**Pulizia File Temporanei**
- L'applicazione gestisce automaticamente i file temporanei
- Alla chiusura, tutti i file temporanei vengono eliminati
- In caso di crash, verifica la cartella temp di sistema

**Aggiornamenti Futuri**
- Controlla periodicamente nuove versioni per funzionalità aggiuntive
- Segnala bug o suggerimenti per migliorare il software

---

*SongStructurer - Strumento professionale per l'analisi della struttura musicale*