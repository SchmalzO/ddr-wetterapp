"""
Modulname: datenbank.py
Beschreibung:
    SQLite-Datenbankzugriff fuer die DDR-Wetterapp.
    Legt Tabellen an, befuellt Grunddaten und stellt
    Funktionen zum Lesen und Schreiben bereit.

Autor: Oleg Schmalz
Datum: Juni 2026
"""

import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from staedte_ddr import DDR_ORTE

DB_PFAD = os.path.join(os.path.dirname(__file__), "wetter.db")


def verbinden() -> sqlite3.Connection:
    """
    Oeffnet eine Verbindung zur SQLite-Datenbank.

    Rueckgabe:
        sqlite3.Connection-Objekt
    """
    return sqlite3.connect(DB_PFAD)


def tabellen_anlegen():
    """
    Legt alle benoedigten Tabellen an, falls sie noch nicht existieren.
    Wird einmalig beim Programmstart aufgerufen.
    """
    with verbinden() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS staedte (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                bezirk        TEXT,
                breitengrad   REAL    NOT NULL,
                laengengrad   REAL    NOT NULL,
                angelegt_am   TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wetter_historie (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                stadt_id            INTEGER NOT NULL,
                temperatur          REAL,
                windgeschwindigkeit REAL,
                wettercode          INTEGER,
                abgerufen_am        TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (stadt_id) REFERENCES staedte(id)
            )
        """)
        conn.commit()


def orte_eintragen():
    """
    Traegt alle Orte aus staedte_ddr.py ein,
    falls die Tabelle noch leer ist.
    """
    with verbinden() as conn:
        anzahl = conn.execute(
            "SELECT COUNT(*) FROM staedte"
        ).fetchone()[0]

        if anzahl == 0:
            conn.executemany(
                """INSERT INTO staedte
                   (name, bezirk, breitengrad, laengengrad)
                   VALUES (?, ?, ?, ?)""",
                DDR_ORTE
            )
            conn.commit()
            print(f"{len(DDR_ORTE)} Orte erfolgreich eingetragen.")
        else:
            print(f"Datenbank bereits befuellt ({anzahl} Orte vorhanden).")


def alle_orte() -> list[dict]:
    """
    Gibt alle Orte aus der Datenbank zurueck,
    sortiert nach Bezirk und Name.

    Rueckgabe:
        Liste von Dictionaries mit id, name, bezirk,
        breitengrad, laengengrad
    """
    with verbinden() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT id, name, bezirk, breitengrad, laengengrad
               FROM staedte
               ORDER BY bezirk, name"""
        ).fetchall()
        return [dict(row) for row in rows]


def orte_nach_bezirk() -> dict[str, list[dict]]:
    """
    Gibt alle Orte gruppiert nach Bezirk zurueck.
    Nuetzlich fuer die Darstellung im Streamlit-Selectbox.

    Rueckgabe:
        Dictionary: Bezirksname -> Liste von Ort-Dictionaries
    """
    orte = alle_orte()
    gruppiert = {}
    for ort in orte:
        bezirk = ort["bezirk"] or "Unbekannt"
        if bezirk not in gruppiert:
            gruppiert[bezirk] = []
        gruppiert[bezirk].append(ort)
    return gruppiert


def ort_nach_id(stadt_id: int) -> dict | None:
    """
    Gibt einen einzelnen Ort anhand seiner ID zurueck.

    Parameter:
        stadt_id: ID des Ortes

    Rueckgabe:
        Dictionary mit Ortsdaten oder None
    """
    with verbinden() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """SELECT id, name, bezirk, breitengrad, laengengrad
               FROM staedte WHERE id = ?""",
            (stadt_id,)
        ).fetchone()
        return dict(row) if row else None


def ort_suchen(suchbegriff: str) -> list[dict]:
    """
    Sucht Orte anhand eines Namensbestandteils.

    Parameter:
        suchbegriff: Teilstring des Ortsnamens

    Rueckgabe:
        Liste passender Orte
    """
    with verbinden() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT id, name, bezirk, breitengrad, laengengrad
               FROM staedte
               WHERE name LIKE ?
               ORDER BY name""",
            (f"%{suchbegriff}%",)
        ).fetchall()
        return [dict(row) for row in rows]


def wetter_speichern(
    stadt_id: int,
    temperatur: float,
    wind: float,
    wettercode: int
):
    """
    Speichert einen Wetterdatensatz in der Historie.

    Parameter:
        stadt_id:   ID der Stadt
        temperatur: Temperatur in Grad Celsius
        wind:       Windgeschwindigkeit in km/h
        wettercode: WMO-Wettercode
    """
    with verbinden() as conn:
        conn.execute(
            """INSERT INTO wetter_historie
               (stadt_id, temperatur, windgeschwindigkeit, wettercode)
               VALUES (?, ?, ?, ?)""",
            (stadt_id, temperatur, wind, wettercode)
        )
        conn.commit()


def wetter_historie_laden(stadt_id: int) -> list[dict]:
    """
    Gibt die gespeicherte Wetterhistorie fuer einen Ort zurueck.

    Parameter:
        stadt_id: ID der Stadt

    Rueckgabe:
        Liste von Dictionaries mit temperatur, windgeschwindigkeit,
        wettercode, abgerufen_am - neueste Eintraege zuerst
    """
    with verbinden() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT temperatur, windgeschwindigkeit,
                      wettercode, abgerufen_am
               FROM wetter_historie
               WHERE stadt_id = ?
               ORDER BY abgerufen_am DESC
               LIMIT 100""",
            (stadt_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def initialisieren():
    """
    Fuehrt alle Schritte zur Ersteinrichtung der Datenbank durch:
    Tabellen anlegen und Grunddaten eintragen.
    Wird von main.py beim Start aufgerufen.
    """
    tabellen_anlegen()
    orte_eintragen()

def wetter_als_dataframe():
    """
    Gibt die gesamte Wetterhistorie als pandas DataFrame zurück.
    Enthält Ortsname, Bezirk, Temperatur, Wind und Zeitpunkt.

    Rückgabe:
        pandas DataFrame oder leerer DataFrame
    """
    import pandas as pd

    with verbinden() as conn:
        df = pd.read_sql_query(
            """SELECT
                s.name        AS Ort,
                s.bezirk      AS Bezirk,
                w.temperatur  AS Temperatur,
                w.windgeschwindigkeit AS Wind,
                w.abgerufen_am AS Zeitpunkt
               FROM wetter_historie w
               JOIN staedte s ON s.id = w.stadt_id
               ORDER BY w.abgerufen_am DESC""",
            conn
        )
    return df    