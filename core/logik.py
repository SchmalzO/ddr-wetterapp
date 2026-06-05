"""
Modulname: logik.py
Beschreibung:
    Geschäftslogik der DDR-Wetterapp.

    Enthält Regeln zur Auswertung von Wetterdaten,
    zur Behandlung von Bruderstaaten und Ausland
    sowie zur Prüfung von DDR-Grenzen.

Autor: Oleg Schmalz
Datum: Juni 2026
"""

import random

# --------------------------------------------------
# Geografische Grenzen der DDR (vereinfacht)
# --------------------------------------------------

DDR_GRENZEN = {
    "lat_min": 50.0,
    "lat_max": 54.0,
    "lon_min": 10.0,
    "lon_max": 15.2,
}

# --------------------------------------------------
# Wetterlagen für das nichtsozialistische Ausland
# --------------------------------------------------

SCHLECHTWETTER_CODES = [
    {
        "lage": "Anhaltende Schlechtwetterlage im nichtsozialistischen Ausland",
        "hinweis": "Der Klassenfeind leidet unter unwirtlichen Verhältnissen.",
        "weathercode": 65,
    },
    {
        "lage": "Dichte Bewölkung über dem westlichen Territorium",
        "hinweis": "Die klimatischen Bedingungen spiegeln die gesellschaftliche Lage wieder.",
        "weathercode": 3,
    },
    {
        "lage": "Gewitterfront über dem kapitalistischen Ausland",
        "hinweis": (
            "Reisen in diese Gebiete sind aus meteorologischen "
            "Gründen nicht empfehlenswert. Staatssicherheit ist informiert."
        ),
        "weathercode": 95,
    },
]

# Hinweise für sozialistische Bruderstaaten

BRUDERSTAATEN_HINWEISE = [
    "Die solidarische Verbundenheit zeigt sich auch im Wetter.",
    "Freundschaftliche Grüße an die Genossinnen und Genossen.",
    "Im Zeichen des sozialistischen Internationalismus.",
]

# Humorvolle Fehlermeldungen

FEHLERMELDUNGEN = [
    "Tja, da kannste nüscht machen – komm später nochmal, Genossin/Genosse!",
    "Det Netz streikt heute. Is halt so in der Republik.",
    "Kein Signal vom Hydrometeorologischen Dienst. Die haben wohl Pause gemacht.",
    "Verbindung weg! Vielleicht hat der Klassenfeind die Leitung gekappt.",
    "Nüscht zu kriegen heute. Schau morgen nochmal rein, Genossin/Genosse!",
]


def ist_in_ddr(
    breitengrad: float,
    laengengrad: float
) -> bool:
    """
    Prüft, ob Koordinaten innerhalb
    des Territoriums der DDR liegen.

    Parameter:
        breitengrad: geografische Breite
        laengengrad: geografische Länge

    Rückgabe:
        True falls innerhalb der DDR,
        sonst False.
    """
    return (
        DDR_GRENZEN["lat_min"] <= breitengrad <= DDR_GRENZEN["lat_max"]
        and
        DDR_GRENZEN["lon_min"] <= laengengrad <= DDR_GRENZEN["lon_max"]
    )


def get_wetter_fuer_anzeige(
    ort: dict,
    wetter_daten: dict | None
) -> dict:
    """
    Bereitet Wetterdaten für die Anzeige auf.

    Parameter:
        ort:
            Ortsdaten aus der Datenbank

        wetter_daten:
            Wetterdaten der API oder None

    Rückgabe:
        Dictionary mit Temperatur,
        Windgeschwindigkeit, Wetterlage,
        Hinweis und Kategorie.
    """

    bezirk = ort.get("bezirk", "")

    # --------------------------------------------------
    # Nichtsozialistisches Ausland
    # --------------------------------------------------

    if bezirk == "Nichtsozialistisches Ausland":
        schlechtwetter = random.choice(SCHLECHTWETTER_CODES)
        return {
            "temperatur": random.randint(-5, 8),
            "windgeschwindigkeit": random.randint(40, 80),
            "lage": schlechtwetter["lage"],
            "hinweis": schlechtwetter["hinweis"],
            "kategorie": "ausland",
        }

    # --------------------------------------------------
    # API nicht erreichbar
    # --------------------------------------------------

    if wetter_daten is None:
        return {
            "temperatur": "-",
            "windgeschwindigkeit": "-",
            "lage": "Nüscht zu machen – Staatssicherheit ist informiert!",
            "hinweis": random.choice(FEHLERMELDUNGEN),
            "kategorie": "fehler",
        }

    # --------------------------------------------------
    # Sozialistische Bruderstaaten
    # --------------------------------------------------

    if bezirk == "Sozialistische Bruderstaaten":
        return {
            "temperatur": wetter_daten["temperature"],
            "windgeschwindigkeit": wetter_daten["windspeed"],
            "lage": "Wetterlage im sozialistischen Bruderstaat",
            "hinweis": random.choice(BRUDERSTAATEN_HINWEISE),
            "kategorie": "bruderstaat",
        }

    # --------------------------------------------------
    # DDR-Orte
    # --------------------------------------------------

    from core.api_client import wettercode_uebersetzen
    eintrag = wettercode_uebersetzen(wetter_daten["weathercode"])
    return {
        "temperatur": wetter_daten["temperature"],
        "windgeschwindigkeit": wetter_daten["windspeed"],
        "lage": eintrag["lage"],
        "hinweis": eintrag["hinweis"],
        "kategorie": "ddr",
    }