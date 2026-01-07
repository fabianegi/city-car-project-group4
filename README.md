# CITY-CAR Funnel-Analyse

## Projektziel
Analyse des Kunden-Funnels der Ride-Sharing-App CITY-CAR (Download → Signup → Request → Fahrt → Zahlung → Review). Fokus: reproduzierbare Kennzahlen für Warm-up und Grundlage für spätere Business-Fragen.

## Daten (kurz, gemäß Data Dictionary)
- app_downloads.csv: app_download_key (PK), platform, download_ts
- signups.csv: user_id (PK), session_id (FK→app_download_key), signup_ts, age_range
- ride_requests.csv: ride_id (PK), user_id, driver_id, request_ts, accept_ts, pickup_ts, dropoff_ts, cancel_ts
- transactions.csv: transaction_id (PK), ride_id, purchase_amount_usd, charge_status, transaction_ts
- reviews.csv: review_id (PK), ride_id, user_id, driver_id, rating, review

## Projektstruktur
- src/main.py – CLI (Warm-up via --warmup)
- src/funnel_utility.py – Laden, Validieren, Kennzahlen
- Daten/ – CSVs (Standardpfad; via --data-dir überschreibbar)
- outputs/ – Platz für Charts/Exports
- TEAM_TODO.md – Rollen & Tickets
- requirements.txt – Abhängigkeiten (pandas, numpy)

## Setup & Run
1) Python 3.11
2) `python -m venv .venv && source .venv/bin/activate`
3) `pip install -r requirements.txt`
4) Warm-up ausführen:
```bash
python -m src.main --warmup --data-dir Daten
```
(--data-dir weglassen, wenn Daten/ genutzt wird)

## Warm-up Definitionen (je Kennzahl)
1) App-Downloads: Zeilen in app_downloads.csv
2) Signups: Zeilen in signups.csv
3) Ride Requests: Zeilen in ride_requests.csv
4) Abgeschlossene Fahrten: dropoff_ts not null AND cancel_ts is null
5) Ride Requests & eindeutige User: Zeilen & distinct user_id in ride_requests.csv
6) Ø Dauer: (dropoff_ts - pickup_ts) in Minuten, nur Fahrten aus (4)
7) Akzeptierte Fahrten: accept_ts not null
8) Erfolgreich abgerechnet & Umsatz: charge_status == "Approved", Summe purchase_amount_usd
9) Ride Requests pro Plattform: ride_requests → signups (user_id→session_id) → app_downloads (app_download_key)
10) Drop-off Signup→Request: Anteil der Signups ohne eine einzige Fahrtanfrage

## Reproduzierbarkeit
- pathlib-Pfade, kein Hardcoding absoluter Wege
- Schema-Checks je CSV (Pflichtspalten, Fehlermeldung sonst)
- Deterministische Berechnung mit pandas

## Hinweise
- Prozent des Vorherigen: Übergangsquote Schritt→Schritt
- Prozent der Gesamtheit: Anteil relativ zum Funnel-Einstieg
