# TEAM TODO (CITY-CAR)

Rollen (5 Personen):
- Data & Schema
- Warm-up Metrics
- Time & Revenue
- Platform & Drop-off
- QA & Integration

Tickets (DoD = Code/Artefakt erstellt, geprüft, dokumentiert):

1) Data-01: Schema-Check & Laden
   - Lade alle CSVs, prüfe Pflichtspalten laut Data Dictionary
   - DoD: `load_all` läuft ohne Fehler; Fehlermeldung klar bei Missing Columns

2) Data-02: Timestamp-Parsing
   - Einheitliche Parser für request/accept/pickup/dropoff/cancel/transaction
   - DoD: Helper dokumentiert; Smoke-Test erfolgreich

3) Metrics-01: Warm-up KPIs
   - Implementiere Kennzahlen 1–10 in funnel_utility
   - DoD: `python -m src.main --warmup` liefert erwartete Werte

4) Metrics-02: Time & Revenue
   - Prüfe Dauer- und Umsatzberechnung auf NaNs/Typen; definiere Edge Cases
   - DoD: Tests für leere/fehlerhafte Zeilen; Doku im Code

5) Metrics-03: Platform & Drop-off
   - Join-Logik app_downloads → signups → ride_requests robust machen
   - DoD: Platform-Zählungen stimmen; Drop-off-Formel dokumentiert

6) Report-01: Executive Summary Draft
   - One-Pager mit Kontext, Datenbasis, wichtigsten KPIs
   - DoD: Draft im Repo, Review erfolgt

7) Report-02: Detail-Abschnitte
   - Struktur für PDF (8–10 Seiten) mit Platzhaltern für Charts
   - DoD: Skeleton fertig, klare Abschnittstitel

8) QA-01: Reproduzierbarkeit
   - Pfade (pathlib), CLI-Args, Clean Run auf frischem Checkout
   - DoD: README Runbook ok, Testlauf dokumentiert

9) QA-02: Packaging & Versions
   - requirements.txt (pandas, numpy) pin check; optional Lint/Format
   - DoD: Installation ohne Warnungen; CLI-Lauf grün

10) Integration-01: ZIP-Abgabe
    - Sammle PDF, Code, README, outputs in ZIP
    - DoD: Zip erzeugt, Test-Entpacken erfolgreich
