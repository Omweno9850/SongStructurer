# SongStructurer

![SongStructurer Application](https://img.shields.io/badge/Version-1.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**SongStructurer** è un'applicazione desktop interattiva progettata per l'analisi e la segmentazione automatica di file audio musicali. L'applicazione identifica automaticamente le strutture ritmiche di una canzone e permette di modificarle, rinominarle ed esportarle con una interfaccia grafica intuitiva.

## Caratteristiche Principali

- 🎵 **Analisi Automatica dei Segmenti**: Rilevamento automatico delle sezioni musicali basato sul ritmo
- 👆 **Interfaccia Grafica Interattiva**: Visualizzazione dell'onda sonora con editing drag-and-drop
- 🎧 **Riproduzione dei Segmenti**: Ascolto individuale di ogni segmento identificato
- 📊 **Zoom e Navigazione**: Controllo dettagliato della visualizzazione dell'audio
- 💾 **Esportazione Dati**: Esporta i segmenti in formato CSV e l'immagine in PNG
- 🔄 **Modifica in Tempo Reale**: Rinomina, unisci e modifica i segmenti direttamente dalla timeline
- 🎮 **Controlli di Trasporto**: Progress bar interattiva e slider per la navigazione temporale

## Requisiti di Sistema

- **Sistema Operativo**: Windows 10/11 (64-bit)
- **Spazio su Disco**: ~128 MB liberi
- **Memoria RAM**: 4 GB minimo, 8 GB raccomandati
- **Audio**: Scheda audio compatibile con Windows

## Installazione

### Download
Scarica il file `SongStructurer.exe` dalla pagina delle release ed eseguilo direttamente. Non è richiesta alcuna installazione.

### Versione Portable
L'applicazione è completamente portable - puoi eseguirla da qualsiasi cartella senza modifiche al registro di sistema.

## Avvio Rapido

1. **Esegui** il file `SongStructurer.exe`
2. **Carica** un file audio (MP3, WAV, FLAC)
3. **Clicca** "Analizza segmenti" per l'identificazione automatica
4. **Seleziona** un segmento dalla lista per ascoltarlo
5. **Modifica** i segmenti secondo le tue necessità
6. **Esporta** i risultati in CSV o PNG

## Formati Supportati

- **Audio**: MP3, WAV, FLAC
- **Esportazione**: CSV (segmenti), PNG (immagine waveform)

## Sicurezza

Il file .exe è auto-contenuto e non richiede connessioni internet o installazione di dipendenze aggiuntive. È stato creato utilizzando PyInstaller e include tutte le librerie necessarie.

## Supporto

Per problemi o suggerimenti:
1. Controlla che il file audio non sia corrotto
2. Verifica di avere i permessi di scrittura nella cartella di esecuzione
3. Assicurati che il sistema soddisfi i requisiti minimi

## Licenza

Distribuito sotto licenza GNU. Vedi il file LICENSE per maggiori dettagli.