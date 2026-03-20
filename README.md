# Dreiecksrechner mit Zeichnung

Ein Programm, das Dreiecke nach den Gesetzen der Trigonometrie berechnet und zeichnet. Eingabemasken für Seiten und Winkel, automatische Berechnung fehlender Werte, beschriftete Darstellung und vollständige Werteliste.

## Voraussetzungen

- **Python 3.10+** ([python.org](https://www.python.org/downloads/) oder Microsoft Store)

## Installation

1. **Virtuelle Umgebung anlegen**

   ```powershell
   
   ```

2. **Umgebung aktivieren (Windows PowerShell)**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Falls Ausführungsskripte blockiert sind: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

   **CMD (cmd.exe):**

   ```cmd
   .venv\Scripts\activate.bat
   ```

3. **pip aktualisieren**

   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Abhängigkeiten installieren**

   ```powershell
   pip install -r requirements.txt
   ```

## Start

```powershell
streamlit run app.py
```

Die App öffnet sich im Browser (Standard: 
).

## Nutzung

- Gib **Seiten** (a, b, c) und **Winkel** (α, β, γ) ein – mindestens drei passende Größen.
- Bei **SSA** (zwei Seiten, ein Winkel) können 0, 1 oder 2 Lösungen existieren; beide werden bei Bedarf angezeigt.
- Die Zeichnung zeigt alle Seiten und Winkel beschriftet; darunter steht eine vollständige Wertetabelle.
