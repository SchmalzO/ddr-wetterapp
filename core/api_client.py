"""
Modulname: api_client.py
Beschreibung:
    API-Aufruf und Datenaufbereitung für die DDR-Wetterapp.
    Ruft Wetterdaten von Open-Meteo ab und übersetzt
    WMO-Wettercodes in DDR-Wetterlagen.

Autor: Oleg Schmalz
Datum: Juni 2026
"""

import requests

# --------------------------------------------------
# API-Konfiguration
# --------------------------------------------------

URL = "https://api.open-meteo.com/v1/forecast"

# --------------------------------------------------
# Wettercode-Tabelle
# --------------------------------------------------

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
        "hinweis": "Feuchte Bedingungen begleiten den heutigen Arbeitstag.",
    },
    55: {
        "lage": "Kräftiger Nieselregen im Republikmaßstab",
        "hinweis": "Wetterfeste Kleidung wird empfohlen.",
    },
    61: {
        "lage": "Leichter Niederschlag zur Unterstützung der Landwirtschaft",
        "hinweis": "Günstige Bedingungen für Felder und Gärten.",
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
        "hinweis": "Nicht notwendige Wege sollten verschoben werden.",
    },
    71: {
        "lage": "Leichter Schneefall über den Bezirken der Republik",
        "hinweis": "Winterfeste Kleidung wird empfohlen.",
    },
    73: {
        "lage": "Planmäßiger Schneefall",
        "hinweis": (
            "Verkehrsverzögerungen können nicht "
            "ausgeschlossen werden."
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
            "Mit feuchter Witterung während des gesamten "
            "Tages ist zu rechnen."
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
        "hinweis": "Aufenthalte auf freiem Feld sind zu vermeiden.",
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
            "Die örtlichen Anweisungen der zuständigen "
            "Stellen sind zu beachten."
        ),
    },
}


def wettercode_uebersetzen(code: int) -> dict:
    """
    Übersetzt einen WMO-Wettercode in eine
    DDR-Wetterlage mit Hinweis.

    Parameter:
        code: WMO-Wettercode

    Rückgabe:
        Dictionary mit lage und hinweis
    """
    return WETTERCODES.get(
        code,
        {
            "lage": "Meteorologische Lage unbekannt",
            "hinweis": (
                "Für diesen Wetterzustand liegen derzeit "
                "keine Empfehlungen vor."
            ),
        },
    )


def get_wetter_aktuell(
    breitengrad: float,
    laengengrad: float
) -> dict | None:
    """
    Ruft aktuelle Wetterdaten von Open-Meteo ab.

    Parameter:
        breitengrad: Geografische Breite
        laengengrad: Geografische Länge

    Rückgabe:
        Dictionary mit temperature, windspeed,
        weathercode, time oder None bei Fehler
    """
    params = {
        "latitude": breitengrad,
        "longitude": laengengrad,
        "current_weather": True,
    }

    try:
        antwort = requests.get(URL, params=params, timeout=10)
        antwort.raise_for_status()
        return antwort.json()["current_weather"]

    except requests.exceptions.ConnectionError:
        print("FEHLER: Keine Verbindung zum meteorologischen Netz.")
        return None

    except requests.exceptions.Timeout:
        print("FEHLER: Zeitlimit überschritten.")
        return None

    except requests.exceptions.HTTPError as fehler:
        print(f"HTTP-FEHLER: {fehler}")
        return None

    except Exception as fehler:
        print(f"UNBEKANNTER FEHLER: {fehler}")
        return None