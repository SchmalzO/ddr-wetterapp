"""
Modulname: main.py
Beschreibung:
    Einstiegspunkt der DDR-Wetterapp.

Autor: Oleg Schmalz
Datum: Juni 2026
"""

from daten.datenbank import initialisieren


def main():
    """
    Initialisiert die Datenbank.
    """
    initialisieren()
    print("DDR-Wetterapp erfolgreich initialisiert.")


if __name__ == "__main__":
    main()