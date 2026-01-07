"""
CITY-CAR Funnel-Analyse - Warm-up Fragen
=========================================
Dieses Skript beantwortet die grundlegenden Fragen zur Datenbank.
"""

import pandas as pd
from datetime import datetime

# Konstanten
DATA_DIR = "Daten"

# CSV-Dateien laden
print("Lade Daten...\n")
app_downloads = pd.read_csv(f"{DATA_DIR}/app_downloads.csv")
signups = pd.read_csv(f"{DATA_DIR}/signups.csv")
ride_requests = pd.read_csv(f"{DATA_DIR}/ride_requests.csv")
transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv")

print("=" * 70)
print("WARM-UP FRAGEN - CITY-CAR FUNNEL-ANALYSE")
print("=" * 70)
print()

# Frage 1: Wie oft wurde die App heruntergeladen?
num_downloads = len(app_downloads)
print(f"1. Number of app downloads: {num_downloads}")
print()

# Frage 2: Wie viele Benutzer haben sich in der App angemeldet?
num_signups = len(signups)
print(f"2. Number of signups: {num_signups}")
print()

# Frage 3: Wie viele Fahrten wurden über die App angefordert?
num_ride_requests = len(ride_requests)
print(f"3. Number of ride requests: {num_ride_requests}")
print()

# Frage 4: Wie viele Fahrten wurden angefordert und abgeschlossen?
# Eine Fahrt ist abgeschlossen, wenn dropoff_ts nicht null ist
completed_rides = ride_requests[ride_requests['dropoff_ts'].notna()]
num_completed_rides = len(completed_rides)
print(f"4. Number of completed rides: {num_completed_rides}")
print()

# Frage 5: Wie viele Fahrten wurden angefordert, und wie viele unterschiedliche Nutzer haben eine Fahrt angefordert?
unique_users_with_requests = ride_requests['user_id'].nunique()
print(f"5. Number of ride requests: {num_ride_requests}")
print(f"   Number of unique users with ride requests: {unique_users_with_requests}")
print()

# Frage 6: Was ist die durchschnittliche Dauer einer Fahrt (Abholung → Absetzung)?
# Nur abgeschlossene Fahrten mit pickup_ts und dropoff_ts
completed_rides_with_times = ride_requests[
    (ride_requests['pickup_ts'].notna()) & 
    (ride_requests['dropoff_ts'].notna())
].copy()

# Zeitstempel in datetime konvertieren
completed_rides_with_times['pickup_ts'] = pd.to_datetime(completed_rides_with_times['pickup_ts'])
completed_rides_with_times['dropoff_ts'] = pd.to_datetime(completed_rides_with_times['dropoff_ts'])

# Dauer berechnen (in Minuten)
completed_rides_with_times['duration_minutes'] = (
    completed_rides_with_times['dropoff_ts'] - completed_rides_with_times['pickup_ts']
).dt.total_seconds() / 60

avg_ride_duration = completed_rides_with_times['duration_minutes'].mean()
print(f"6. Average ride duration (pickup to dropoff): {avg_ride_duration:.2f} minutes")
print()

# Frage 7: Wie viele Fahrten wurden von einem Fahrer angenommen?
# Eine Fahrt wurde angenommen, wenn accept_ts nicht null ist
accepted_rides = ride_requests[ride_requests['accept_ts'].notna()]
num_accepted_rides = len(accepted_rides)
print(f"7. Number of rides accepted by a driver: {num_accepted_rides}")
print()

# Frage 8: Wie viele Fahrten konnten erfolgreich abgerechnet werden und wie hoch ist der Gesamtumsatz?
# Erfolgreich abgerechnete Fahrten haben charge_status = 'Approved'
approved_transactions = transactions[transactions['charge_status'] == 'Approved']
num_approved_transactions = len(approved_transactions)
total_revenue = approved_transactions['purchase_amount_usd'].sum()
print(f"8. Number of successfully charged rides: {num_approved_transactions}")
print(f"   Total revenue: ${total_revenue:,.2f}")
print()

# Frage 9: Wie viele Fahrtanfragen gab es pro Plattform (iOS, Android, Web)?
# Fahrtanfragen mit signups und app_downloads verbinden
# session_id in signups entspricht app_download_key in app_downloads
ride_requests_with_platform = ride_requests.merge(
    signups[['user_id', 'session_id']], 
    on='user_id', 
    how='left'
).merge(
    app_downloads[['app_download_key', 'platform']],
    left_on='session_id',
    right_on='app_download_key',
    how='left'
)

platform_requests = ride_requests_with_platform['platform'].value_counts()
print(f"9. Ride requests per platform:")
for platform, count in platform_requests.items():
    print(f"   {platform}: {count}")
print()

# Frage 10: Wie hoch ist der Drop-off von Anmeldung → Fahrtanfrage?
# Drop-off = (Signups - Unique Users mit Fahrtanfrage) / Signups * 100
dropoff_rate = ((num_signups - unique_users_with_requests) / num_signups) * 100
print(f"10. Drop-off from signup to ride request:")
print(f"    Signups: {num_signups}")
print(f"    Users with ride requests: {unique_users_with_requests}")
print(f"    Drop-off rate: {dropoff_rate:.2f}%")
print()

print("=" * 70)
print("ANALYSE ABGESCHLOSSEN")
print("=" * 70)
