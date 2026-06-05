# DDR-Wetterapp 🌦️
## Wetterdienst der Deutschen Demokratischen Republik

Eine satirische Datenanwendung, die aktuelle Wetterdaten für alle Orte der ehemaligen
Deutschen Demokratischen Republik abruft und in einer fiktiven DDR-Ästhetik darstellt.

WMO-Wettercodes werden in humorvolle DDR-Wetterlagen übersetzt. Westdeutsche Städte
und kapitalistisches Ausland erhalten stets schlechtes Wetter. Sozialistische Bruderstaaten
werden mit internationalistischer Solidarität bedacht.

---

## Voraussetzungen

- Python 3.10 oder höher
- Internetzugang (für die Open-Meteo API)
- Bibliotheken siehe `requirements.txt`

---

## Installation

1. Repository klonen oder ZIP entpacken:
   ```
   git clone https://github.com/SchmalzO/ddr-wetterapp.git
   cd ddr-wetterapp
   ```

2. Virtuelle Umgebung anlegen:
   ```
   python -m venv .venv
   ```

3. Virtuelle Umgebung aktivieren:
   ```
   # Windows
   .venv\Scripts\activate

   # Linux / Mac
   source .venv/bin/activate
   ```

4. Bibliotheken installieren:
   ```
   pip install -r requirements.txt
   ```

5. Konfiguration anlegen:
   ```
   copy env.example .env
   ```

---

## Datenbank initialisieren

Beim ersten Start wird die Datenbank automatisch angelegt und mit 311 historischen
DDR-Orten befüllt. Alternativ manuell:

```
python -m core.main
```

---

## Anwendung starten

```
streamlit run gui/app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

---

## Bedienung

1. Namen eingeben — sozialistische Begrüßung erscheint
2. Bezirk wählen (DDR-Bezirke, Bruderstaaten oder nichtsozialistisches Ausland)
3. Ort wählen
4. "Wetterlage abrufen" klicken
5. Tab "Statistische Auswertung" für pandas-Auswertung aller bisherigen Abrufe

---

## Projektstruktur

```
DDR-Wetterapp/
├── core/
│   ├── api_client.py       # API-Aufruf und WMO-Wettercode-Übersetzung
│   ├── logik.py            # Geschäftslogik und DDR-Kategorisierung
│   └── main.py             # Einstiegspunkt / Datenbankinitialisierung
├── daten/
│   ├── datenbank.py        # SQLite-Zugriff
│   ├── staedte_ddr.py      # 311 historische DDR-Orte
│   └── wetter.db           # SQLite-Datenbank (wird automatisch erstellt)
├── gui/
│   └── app.py              # Streamlit-Frontend
├── .env                    # Konfiguration (nicht in Git)
├── env.example             # Vorlage für .env
├── requirements.txt
└── README.md
```

---

## Hinweise zum Datenschutz

- Es werden keine personenbezogenen Daten gespeichert
- Die Datenbank liegt ausschließlich lokal unter `daten/wetter.db`
- Es werden nur Koordinaten an die Open-Meteo API übermittelt (keine personenbezogenen Daten)
- Open-Meteo benötigt keinen API-Schlüssel
- Die `.env`-Datei ist in `.gitignore` ausgeschlossen

---

## Online-Version

Die App ist öffentlich erreichbar unter:
**https://ddr-wetterapp.streamlit.app**

Hinweis: Auf Streamlit Cloud wird die Datenbank bei jedem Neustart neu erstellt.
Gespeicherte Wetterdaten sind daher nur innerhalb einer Session verfügbar.

---

## Autor

Oleg Schmalz | Robotron Bildungszentrum Halle | Juni 2026
