"""
Modulname: app.py
Beschreibung: Streamlit-Frontend der DDR-Wetterapp
Autor: Oleg Schmalz
Datum: Juni 2026
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from daten.datenbank import initialisieren, orte_nach_bezirk, wetter_speichern, wetter_als_dataframe
from core.logik import get_wetter_fuer_anzeige

st.set_page_config(page_title="DDR Wetterapp", layout="wide")

initialisieren()

st.title("Wetterdienst der Deutschen Demokratischen Republik")
st.caption("Hydrometeorologischer Dienst der DDR – Meteorologisches Informationssystem")

name = st.text_input(
    "Wie ist Ihr Name, Genossin/Genosse?",
    placeholder="Nachname"
)

if name:
    st.success(
        f"Sozialistische Grüße Genossin/Genosse, {name}! "
        "Hier können Sie die Wetterdaten unserer wundervollen DDR erkunden."
    )

st.divider()

# Tabs

tab1, tab2 = st.tabs(["Wetterabfrage", "Statistische Auswertung"])

# Tab 1: Wetterabfrage

with tab1:

    st.subheader("Wetterabfrage")

    orte_gruppiert = orte_nach_bezirk()
    bezirke = list(orte_gruppiert.keys())

    col1, col2 = st.columns(2)

    with col1:
        bezirk_auswahl = st.selectbox(
            "Bezirk / Kategorie wählen:",
            bezirke
        )

    with col2:
        orte_im_bezirk = orte_gruppiert[bezirk_auswahl]
        ortsnamen = [ort["name"] for ort in orte_im_bezirk]
        ort_auswahl = st.selectbox(
            "Ort wählen:",
            ortsnamen
        )

    gewaehlter_ort = next(
        ort for ort in orte_im_bezirk
        if ort["name"] == ort_auswahl
    )

    if st.button("Wetterlage abrufen"):

        with st.spinner("Verbinde mit dem Hydrometeorologischen Dienst ..."):
            from core.api_client import get_wetter_aktuell
            wetter_daten = get_wetter_aktuell(
                gewaehlter_ort["breitengrad"],
                gewaehlter_ort["laengengrad"]
            )
            ergebnis = get_wetter_fuer_anzeige(gewaehlter_ort, wetter_daten)

        # Wetterdaten in Datenbank speichern
        if wetter_daten is not None:
            wetter_speichern(
                stadt_id=gewaehlter_ort["id"],
                temperatur=wetter_daten["temperature"],
                wind=wetter_daten["windspeed"],
                wettercode=wetter_daten["weathercode"]
            )

        st.divider()
        st.subheader(f"Meteorologische Information für: {gewaehlter_ort['name']}")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("Temperatur", f"{ergebnis['temperatur']} °C")
            st.metric("Windgeschwindigkeit", f"{ergebnis['windgeschwindigkeit']} km/h")

        with col4:
            st.info(f"Wetterlage: {ergebnis['lage']}")
            st.warning(f"Hinweis des Wetterdienstes: {ergebnis['hinweis']}")

        if ergebnis["kategorie"] == "ausland":
            st.error(
                "Achtung, Genossin/Genosse! Dieser Ort liegt außerhalb der Deutschen "
                "Demokratischen Republik. Die Wetterlage ist entsprechend trist. Die Staatssicherheit ist informiert!"
            )
        elif ergebnis["kategorie"] == "bruderstaat":
            st.success(
                "Sozialistischer Bruderstaat – "
                "Internationalistische Solidarität!"
            )
        elif ergebnis["kategorie"] == "fehler":
            st.error(
                "Tja, da kannste nüscht machen! "
                "Das meteorologische Netz der Republik streikt heute."
                "Versuch's später nochmal, Genossin/Genosse!"
            )

# Tab 2: Statistische Auswertung

with tab2:

    st.subheader("Statistische Auswertung der Wetterdaten")

    import pandas as pd

    df = wetter_als_dataframe()

    if df.empty:
        st.info(
            "Noch keine Wetterdaten vorhanden. "
            "Rufe zunächst einige Orte im Tab 'Wetterabfrage' ab."
        )
    else:
        st.caption(f"Insgesamt {len(df)} Messungen gespeichert.")

        # Durchschnittstemperatur pro Bezirk
        st.subheader("Durchschnittstemperatur pro Bezirk")
        temp_pro_bezirk = (
            df.groupby("Bezirk")["Temperatur"]
            .mean()
            .round(1)
            .sort_values()
            .reset_index()
        )
        temp_pro_bezirk.columns = ["Bezirk", "Ø Temperatur (°C)"]
        st.bar_chart(temp_pro_bezirk.set_index("Bezirk"))

        # Durchschnittlicher Wind pro Bezirk
        st.subheader("Durchschnittlicher Wind pro Bezirk")
        wind_pro_bezirk = (
            df.groupby("Bezirk")["Wind"]
            .mean()
            .round(1)
            .sort_values()
            .reset_index()
        )
        wind_pro_bezirk.columns = ["Bezirk", "Ø Wind (km/h)"]
        st.bar_chart(wind_pro_bezirk.set_index("Bezirk"))

        # Minimum, Maximum, Durchschnitt gesamt
        st.subheader("Gesamtübersicht")
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("Wärmster Ort", df.loc[df["Temperatur"].idxmax(), "Ort"],
                      f"{df['Temperatur'].max()} °C")
        with col6:
            st.metric("Kältester Ort", df.loc[df["Temperatur"].idxmin(), "Ort"],
                      f"{df['Temperatur'].min()} °C")
        with col7:
            st.metric("Ø Temperatur gesamt", f"{df['Temperatur'].mean().round(1)} °C")

        # Rohdaten
        st.subheader("Alle gespeicherten Messungen")
        st.dataframe(df, use_container_width=True)