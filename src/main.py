"""
CLI entrypoint for the CITY-CAR warm-up analysis.
Usage:
    python -m src.main --warmup [--data-dir PATH]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .funnel_utility import (
    average_ride_duration_minutes,
    charged_rides_and_revenue,
    count_accepted_rides,
    count_app_downloads,
    count_completed_rides,
    count_ride_requests,
    count_signups,
    dropoff_signup_to_request,
    load_all,
    ride_requests_and_unique_users,
    ride_requests_per_platform,
)

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "Daten"


def run_warmup(data_dir: Path) -> None:
    frames = load_all(data_dir)

    app_downloads = frames["app_downloads.csv"]
    signups = frames["signups.csv"]
    ride_requests = frames["ride_requests.csv"]
    transactions = frames["transactions.csv"]

    print("=" * 70)
    print("WARM-UP FRAGEN - CITY-CAR FUNNEL-ANALYSE")
    print("=" * 70)

    # 1
    print(f"1. Number of app downloads: {count_app_downloads(app_downloads)}")

    # 2
    print(f"2. Number of signups: {count_signups(signups)}")

    # 3
    print(f"3. Number of ride requests: {count_ride_requests(ride_requests)}")

    # 4
    print(f"4. Number of completed rides: {count_completed_rides(ride_requests)}")

    # 5
    total_requests, unique_request_users = ride_requests_and_unique_users(ride_requests)
    print(f"5. Number of ride requests: {total_requests}")
    print(f"   Number of unique users with ride requests: {unique_request_users}")

    # 6
    avg_duration = average_ride_duration_minutes(ride_requests)
    print(f"6. Average ride duration (pickup to dropoff): {avg_duration:.2f} minutes")

    # 7
    print(f"7. Number of rides accepted by a driver: {count_accepted_rides(ride_requests)}")

    # 8
    charged_count, total_revenue = charged_rides_and_revenue(transactions)
    print(f"8. Number of successfully charged rides: {charged_count}")
    print(f"   Total revenue: ${total_revenue:,.2f}")

    # 9
    platform_counts = ride_requests_per_platform(ride_requests, signups, app_downloads)
    print("9. Ride requests per platform:")
    for platform in ["ios", "android", "web"]:
        if platform in platform_counts:
            print(f"   {platform}: {int(platform_counts[platform])}")
    # print any remaining categories (e.g., unknown)
    for platform, count in platform_counts.items():
        if platform not in {"ios", "android", "web"}:
            print(f"   {platform}: {int(count)}")

    # 10
    total_signups, users_with_request, dropoff_rate = dropoff_signup_to_request(signups, ride_requests)
    print("10. Drop-off from signup to ride request:")
    print(f"    Signups: {total_signups}")
    print(f"    Users with ride requests: {users_with_request}")
    print(f"    Drop-off rate: {dropoff_rate:.2f}%")

    print("=" * 70)
    print("ANALYSE ABGESCHLOSSEN")
    print("=" * 70)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CITY-CAR warm-up analysis")
    parser.add_argument(
        "--warmup",
        action="store_true",
        help="Run the warm-up questions and print answers",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Path to directory containing CSV files (default: ./Daten)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.warmup:
        run_warmup(args.data_dir)
    else:
        parser.error("No mode selected. Use --warmup to run warm-up analysis.")


if __name__ == "__main__":
    main()
