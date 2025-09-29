# SongStructurer

SongStructurer è un piccolo editor grafico per segmentare file audio, ascoltare e modificare sezioni, esportare timestamp e immagine della waveform. È pensato per lavorare con file WAV/MP3/FLAC e sfrutta librerie audio Python comuni per l'analisi e la riproduzione.

Caratteristiche principali
- Analisi automatica dei segmenti tramite beat detection (librosa).
- Modifica visuale dei bordi dei segmenti trascinando le linee.
- Riproduzione di singoli segmenti con cursore di riproduzione sincronizzato.
- Esportazione dei segmenti in CSV e della waveform in PNG.
- Zoom e scorrimento della vista della waveform.
- Interfaccia GUI basata su Tkinter + matplotlib.

Linguaggio: Python 3.8+  
Piattaforma: Windows (testato), Linux e macOS compatibili ma la riproduzione può variare in base a pygame.

Per istruzioni di installazione e build vedi INSTALL.md. Per l'uso dell'app vedi USAGE.md.
