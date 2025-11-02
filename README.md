# Mastodon Hashtag Analyzer

Ein Python-Tool zur Analyse von Mastodon-Archiven, das alle verwendeten Hashtags extrahiert und deren Häufigkeit in einer CSV-Datei exportiert.

## Features

- 📊 Extrahiert alle Hashtags aus Mastodon JSON-Archiven
- 🔢 Zählt die Verwendungshäufigkeit jeder Hashtag
- 💾 Exportiert Ergebnisse in CSV-Format
- 🎯 Unterstützt große Archive (mehrere GB)
- 🔍 Zeigt Top-Hashtags direkt in der Konsole
- 🌍 Mehrere Encoding-Optionen für verschiedene Programme
- 🐛 Debug-Ausgaben zur Umlaut-Analyse

## Voraussetzungen

- Python 3.6 oder höher
- Keine externen Bibliotheken erforderlich (nur Python Standard-Bibliothek)

## Installation

1. Repository klonen oder Datei herunterladen:
```bash
git clone <repository-url>
cd mastodon-hashtag-analyzer
```

2. Skript ausführbar machen (Linux/macOS):
```bash
chmod +x mastodon_hashtag_analyzer.py
```

## Verwendung

### Basis-Verwendung

```bash
python mastodon_hashtag_analyzer.py /pfad/zum/archiv.json
```

### Erweiterte Optionen

```bash
# Benutzerdefinierte Output-Datei
python mastodon_hashtag_analyzer.py archive.json -o meine-hashtags.csv

# Top 50 Hashtags anzeigen statt 20
python mastodon_hashtag_analyzer.py archive.json --top 50

# Für deutsche Excel-Versionen (Semikolon als Trennzeichen)
python mastodon_hashtag_analyzer.py archive.json --delimiter ";"

# Mit spezifischem Encoding
python mastodon_hashtag_analyzer.py archive.json --encoding windows-1252

# Ganzes Verzeichnis analysieren
python mastodon_hashtag_analyzer.py /pfad/zum/mastodon-archiv-ordner/
```

### Alle Optionen

```bash
python mastodon_hashtag_analyzer.py --help
```

**Verfügbare Parameter:**
- `archive` - Pfad zur JSON-Datei oder zum Archiv-Verzeichnis (erforderlich)
- `-o, --output` - Output CSV-Datei (Standard: `mastodon_hashtags.csv`)
- `--top` - Anzahl der Top-Hashtags zur Anzeige (Standard: 20)
- `--encoding` - Encoding für CSV (Standard: `utf-8-sig`)
  - Optionen: `utf-8-sig`, `utf-8`, `iso-8859-15`, `windows-1252`
- `--delimiter` - CSV-Trennzeichen (Standard: `,`)

## Mastodon-Archiv exportieren

1. In Mastodon einloggen
2. Einstellungen → Import und Export → Datenexport
3. "Archiv anfordern"
4. Warten auf E-Mail mit Download-Link
5. ZIP-Datei entpacken
6. `outbox.json` im entpackten Ordner verwenden

## CSV-Datei öffnen

### Mit Excel (Windows)

**Option 1: Import-Funktion (empfohlen)**
1. Excel öffnen (leere Arbeitsmappe)
2. Daten → Aus Text/CSV
3. CSV-Datei auswählen
4. Dateiursprung: "1252: Westeuropäisch (Windows)" oder "65001: Unicode (UTF-8)"
5. Laden

**Option 2: Mit Semikolon exportieren**
```bash
python mastodon_hashtag_analyzer.py archive.json --encoding windows-1252 --delimiter ";"
```
Dann normale Doppelklick-Öffnung sollte funktionieren.

### Mit LibreOffice Calc

1. Datei → Öffnen
2. Zeichensatz: "Unicode (UTF-8)" wählen
3. OK

### Mit Texteditoren

Alle modernen Texteditoren (VS Code, Notepad++, Kate, etc.) öffnen die CSV korrekt mit UTF-8.

## Bekannte Besonderheiten

### Umlaute in Hashtags

Mastodon normalisiert Hashtags für URL-Kompatibilität:
- `#München` wird zu `#muenchen`
- `#Köln` wird zu `#koeln`  
- `#Gemüse` wird zu `#gemuese`
- **ABER:** `#Straße` bleibt `#straße` (ß wird nicht ersetzt)

Das bedeutet: In deiner CSV-Datei siehst du die Hashtags **exakt so, wie sie im Mastodon-Archiv gespeichert sind**. Die Umlaute ä, ö, ü wurden bereits von Mastodon zu ae, oe, ue konvertiert.

## Beispiel-Ausgabe

```
📂 Lese Archiv: outbox.json
📄 Gefundene JSON-Dateien: 1
   Verarbeite: outbox.json... ✓ (1234 Posts mit Hashtags)

✅ Verarbeitet: 1234 Posts mit Hashtags
📊 Gefunden: 567 unterschiedliche Hashtags

🏆 Top 20 Hashtags:
--------------------------------------------------
 1. #photography                   156x
 2. #mastodon                      142x
 3. #nature                        128x
...

💾 Exportiere nach: mastodon_hashtags.csv
   Encoding: utf-8-sig, Trennzeichen: ','
✅ Export abgeschlossen!
```

## CSV-Format

Die exportierte CSV-Datei hat folgendes Format:

```csv
Hashtag,Anzahl
photography,156
mastodon,142
nature,128
...
```

- Sortiert nach Häufigkeit (absteigend)
- Hashtag ohne `#`-Zeichen
- Anzahl der Verwendungen


## Lizenz

Dieses Tool ist Open Source und kann frei verwendet werden.

## Autor

Michael Karbacher