"""
Modulname: test_api_wetter.py
Beschreibung:
    Führt einen Verbindungstest zur Open-Meteo-API durch und gibt
    aktuelle Wetterdaten für Berlin aus.

    Die Wettercodes werden in eine fiktive DDR-Wetterlage übersetzt.
    Zusätzlich werden passende Hinweise des Hydrometeorologischen
    Dienstes der DDR ausgegeben.

Autor: Oleg Schmalz
Datum: Juni 2026
"""

import requests

# -------------------------------------------------------------------
# API-Konfiguration
# -------------------------------------------------------------------

URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 52.52,
    "longitude": 13.41,
    "current_weather": True,
}

# -------------------------------------------------------------------
# Wettercode-Tabelle
# -------------------------------------------------------------------
#
# Jeder Wettercode enthält:
# - lage: Beschreibung der Wetterlage
# - hinweis: Empfehlung des Wetterdienstes
#
# Quelle der Wettercodes:
# WMO Weather Interpretation Codes (WW)
#
# -------------------------------------------------------------------

WETTERCODES = {
    0: {
        "lage": "Sozialistisch-klarer Himmel",
        "hinweis": (
            "Optimale Bedingungen für Arbeitseinsätze "
            "und Freizeitaktivitäten im Kollektiv."
        ),
    },
    1: {
        "lage": "Überwiegend heiter im Sinne des Fünfjahresplanes",
        "hinweis": (
            "Günstige Bedingungen für die erfolgreiche "
            "Erfüllung der Tagesnorm."
        ),
    },
    2: {
        "lage": "Heiter bis genossenschaftlich bewölkt",
        "hinweis": (
            "Gelegentliche Wolkenbildung beeinträchtigt "
            "die Planerfüllung nicht."
        ),
    },
    3: {
        "lage": "Geschlossene Wolkendecke über der Republik",
        "hinweis": (
            "Mit eingeschränkter Sonneneinstrahlung "
            "ist zu rechnen."
        ),
    },
    45: {
        "lage": "Nebelbildung im Bereich volkseigener Betriebe",
        "hinweis": (
            "Erhöhte Aufmerksamkeit im Straßen- und "
            "Werkverkehr empfohlen."
        ),
    },
    48: {
        "lage": "Dichter Reifnebel",
        "hinweis": (
            "Sichtverhältnisse erschweren den Verkehr "
            "innerhalb der Republik."
        ),
    },
    51: {
        "lage": "Leichter sozialistischer Nieselregen",
        "hinweis": (
            "Ein Regenschirm aus volkseigener Produktion "
            "wird empfohlen."
        ),
    },
    53: {
        "lage": "Planmäßiger Nieselregen",
        "hinweis": (
            "Feuchte Bedingungen begleiten den heutigen Arbeitstag."
        ),
    },
    55: {
        "lage": "Kräftiger Nieselregen im Republikmaßstab",
        "hinweis": (
            "Wetterfeste Kleidung wird empfohlen."
        ),
    },
    61: {
        "lage": "Leichter Niederschlag zur Unterstützung der Landwirtschaft",
        "hinweis": (
            "Günstige Bedingungen für Felder und Gärten."
        ),
    },
    63: {
        "lage": "Produktionsfördernder Landregen",
        "hinweis": (
            "Positive Auswirkungen auf die Ernteerträge "
            "werden erwartet."
        ),
    },
    65: {
        "lage": "Kräftige Niederschläge über dem Arbeiter-und-Bauern-Staat",
        "hinweis": (
            "Nicht notwendige Wege sollten verschoben werden."
        ),
    },
    71: {
        "lage": "Leichter Schneefall über den Bezirken der Republik",
        "hinweis": (
            "Winterfeste Kleidung wird empfohlen."
        ),
    },
    73: {
        "lage": "Planmäßiger Schneefall",
        "hinweis": (
            "Verkehrsverzögerungen können nicht ausgeschlossen werden."
        ),
    },
    75: {
        "lage": "Erheblicher Schneefall mit Auswirkungen auf den Nahverkehr",
        "hinweis": (
            "Sozialistische Empfehlung: Vorräte prüfen "
            "und unnötige Fahrten vermeiden."
        ),
    },
    80: {
        "lage": "Vereinzelte Niederschlagsereignisse in ausgewählten Bezirken",
        "hinweis": (
            "Kurzfristige Schauer sind möglich. "
            "Regenschutz bereithalten."
        ),
    },
    81: {
        "lage": "Wiederholte Niederschläge über mehreren Bezirken",
        "hinweis": (
            "Mit feuchter Witterung während des gesamten Tages "
            "ist zu rechnen."
        ),
    },
    82: {
        "lage": "Intensive Niederschlagsaktivität im Republikgebiet",
        "hinweis": (
            "Der Aufenthalt im Freien sollte auf das "
            "notwendige Maß beschränkt werden."
        ),
    },
    95: {
        "lage": "Gewitterfront über dem Territorium der Republik",
        "hinweis": (
            "Aufenthalte auf freiem Feld sind zu vermeiden."
        ),
    },
    96: {
        "lage": "Gewitterlage mit Hagelbildung",
        "hinweis": (
            "Fahrzeuge und landwirtschaftliche Geräte "
            "nach Möglichkeit unterstellen."
        ),
    },
    99: {
        "lage": "Schwere Gewitterlage mit erheblichem Hagelschlag",
        "hinweis": (
            "Die örtlichen Anweisungen der zuständigen Stellen "
            "sind zu beachten."
        ),
    },
}


print("Verbinde mit dem Hydrometeorologischen Dienst der DDR ...")

try:
    antwort = requests.get(URL, params=PARAMS, timeout=10)
    antwort.raise_for_status()

    daten = antwort.json()
    wetter = daten["current_weather"]

    temperatur = wetter["temperature"]
    windgeschwindigkeit = wetter["windspeed"]
    wettercode = wetter["weathercode"]
    zeitpunkt = wetter["time"]

    eintrag = WETTERCODES.get(
        wettercode,
        {
            "lage": "Meteorologische Lage unbekannt",
            "hinweis": (
                "Für diesen Wetterzustand liegen derzeit "
                "keine Empfehlungen vor."
            ),
        },
    )

    print()
    print("=== METEOROLOGISCHE INFORMATION ===")
    print()
    print("Herausgeber: Hydrometeorologischer Dienst der DDR")
    print("Beobachtungsort: Hauptstadt der DDR, Berlin")
    print()
    print(f"Temperatur: {temperatur} °C")
    print(f"Windgeschwindigkeit: {windgeschwindigkeit} km/h")
    print(f"Wetterlage: {eintrag['lage']}")
    print(f"Hinweis des Wetterdienstes: {eintrag['hinweis']}")
    print(f"Zeitpunkt der Messung: {zeitpunkt}")

except requests.exceptions.ConnectionError:
    print(
        "FEHLER: Keine Verbindung zum meteorologischen Netz "
        "der Republik, der Klassenfeind hat wohl die Leitung gekappt!"
    )

except requests.exceptions.Timeout:
    print(
        "FEHLER: Zeitlimit überschritten. "
        "Bitte später erneut versuchen, Genossin/Genosse!"
    )

except requests.exceptions.HTTPError as fehler:
    print(f"HTTP-FEHLER: {fehler}")

except Exception as fehler:
    print(f"UNBEKANNTER FEHLER: {fehler}")