"""
Funnel utility functions for the CITY-CAR warm-up analysis.
Handles data loading, validation, and metric calculations.
"""

from pathlib import Path
from typing import Dict, Tuple
import pandas as pd

# Expected schemas for validation
REQUIRED_SCHEMAS: Dict[str, set[str]] = {
    "app_downloads.csv": {"app_download_key", "platform", "download_ts"},
    "signups.csv": {"user_id", "session_id", "signup_ts", "age_range"},
    "ride_requests.csv": {
        "ride_id",
        "user_id",
        "driver_id",
        "request_ts",
        "accept_ts",
        "pickup_location",
        "dropoff_location",
        "pickup_ts",
        "dropoff_ts",
        "cancel_ts",
    },
    "transactions.csv": {"transaction_id", "ride_id", "purchase_amount_usd", "charge_status", "transaction_ts"},
    "reviews.csv": {"review_id", "ride_id", "user_id", "driver_id", "rating", "review"},
}


def _ensure_required_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {label}: {sorted(missing)}")


def _load_csv(path: Path, required: set[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    df = pd.read_csv(path)
    _ensure_required_columns(df, required, path.name)
    return df


def load_all(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load and validate all required CSVs from the given data directory."""
    data_dir = data_dir.expanduser().resolve()
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    frames: Dict[str, pd.DataFrame] = {}
    for fname, schema in REQUIRED_SCHEMAS.items():
        frames[fname] = _load_csv(data_dir / fname, schema)
    return frames


# Metric helpers -------------------------------------------------------------

def count_app_downloads(app_downloads: pd.DataFrame) -> int:
    return len(app_downloads)


def count_signups(signups: pd.DataFrame) -> int:
    return len(signups)


def count_ride_requests(ride_requests: pd.DataFrame) -> int:
    return len(ride_requests)


def count_completed_rides(ride_requests: pd.DataFrame) -> int:
    completed = ride_requests[
        ride_requests["dropoff_ts"].notna() & ride_requests["cancel_ts"].isna()
    ]
    return completed.shape[0]


def ride_requests_and_unique_users(ride_requests: pd.DataFrame) -> Tuple[int, int]:
    return len(ride_requests), ride_requests["user_id"].nunique()


def average_ride_duration_minutes(ride_requests: pd.DataFrame) -> float:
    """Average duration in minutes for completed rides (dropoff_ts not null, cancel_ts null)."""
    subset = ride_requests[
        ride_requests[["pickup_ts", "dropoff_ts"]].notna().all(axis=1)
        & ride_requests["cancel_ts"].isna()
    ].copy()
    subset["pickup_ts"] = pd.to_datetime(subset["pickup_ts"], errors="coerce")
    subset["dropoff_ts"] = pd.to_datetime(subset["dropoff_ts"], errors="coerce")
    subset = subset[subset[["pickup_ts", "dropoff_ts"]].notna().all(axis=1)]
    if subset.empty:
        return float("nan")
    durations = (subset["dropoff_ts"] - subset["pickup_ts"]).dt.total_seconds() / 60
    return durations.mean()


def count_accepted_rides(ride_requests: pd.DataFrame) -> int:
    return ride_requests[ride_requests["accept_ts"].notna()].shape[0]


def charged_rides_and_revenue(transactions: pd.DataFrame) -> Tuple[int, float]:
    approved = transactions[transactions["charge_status"] == "Approved"].copy()
    approved["purchase_amount_usd"] = pd.to_numeric(approved["purchase_amount_usd"], errors="coerce")
    return approved.shape[0], float(approved["purchase_amount_usd"].sum())


def ride_requests_per_platform(
    ride_requests: pd.DataFrame, signups: pd.DataFrame, app_downloads: pd.DataFrame
) -> pd.Series:
    """
    Map ride requests to platform via signup.session_id == app_download_key.
    Returns value counts per platform (including NaN for unknown).
    """
    merged = ride_requests.merge(signups[["user_id", "session_id"]], on="user_id", how="left")
    merged = merged.merge(
        app_downloads[["app_download_key", "platform"]],
        left_on="session_id",
        right_on="app_download_key",
        how="left",
    )
    counts = merged["platform"].value_counts(dropna=False)
    counts.index = counts.index.fillna("unknown")
    return counts


def dropoff_signup_to_request(signups: pd.DataFrame, ride_requests: pd.DataFrame) -> Tuple[int, int, float]:
    total_signups = len(signups)
    users_with_request = ride_requests["user_id"].nunique()
    dropoff_rate = ((total_signups - users_with_request) / total_signups) * 100 if total_signups else float("nan")
    return total_signups, users_with_request, dropoff_rate
