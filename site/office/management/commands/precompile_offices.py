import json
import os
import concurrent.futures
from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

from office.api.views.index import (
    MorningPrayer,
    EveningPrayer,
    MiddayPrayer,
    Compline,
    FamilyMorningPrayer,
    FamilyMiddayPrayer,
    FamilyEarlyEveningPrayer,
    FamilyCloseOfDayPrayer,
    OfficeSerializer,
)


class MockRequest:
    def __init__(self, query_params=None):
        self.query_params = query_params or {}
        self.GET = self.query_params


def generate_day_worker(args):
    date_obj, output_dir = args
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day

    # Create directory structure: output_dir/YYYY/MM/DD/
    day_dir = os.path.join(output_dir, str(year), f"{month:02d}", f"{day:02d}")
    if not os.path.exists(day_dir):
        try:
            os.makedirs(day_dir)
        except FileExistsError:
            pass

    offices = {
        "morning_prayer": MorningPrayer,
        "evening_prayer": EveningPrayer,
        "midday_prayer": MiddayPrayer,
        "compline": Compline,
        "family_morning_prayer": FamilyMorningPrayer,
        "family_midday_prayer": FamilyMiddayPrayer,
        "family_early_evening_prayer": FamilyEarlyEveningPrayer,
        "family_close_of_day_prayer": FamilyCloseOfDayPrayer,
    }

    request = MockRequest()
    errors = []

    for name, office_class in offices.items():
        try:
            office = office_class(request, year, month, day)
            serializer = OfficeSerializer(office)
            data = serializer.data

            file_path = os.path.join(day_dir, f"{name}.json")
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            errors.append(f"Error generating {name} for {date_obj}: {e}")

    if errors:
        return "\n".join(errors)
    return None


class Command(BaseCommand):
    help = "Pre-compiles Daily Office JSON for deterministic testing"

    def add_arguments(self, parser):
        parser.add_argument("year", type=int, help="Year to generate (e.g. 2025)")
        parser.add_argument(
            "--output-dir",
            default="precompiled",
            help="Directory to save JSON files (default: precompiled)",
        )
        parser.add_argument(
            "--processes",
            type=int,
            default=os.cpu_count() or 4,
            help="Number of processes to use",
        )

    def handle(self, *args, **options):
        year = options["year"]
        output_dir = options["output_dir"]
        processes = options["processes"]

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        delta = timedelta(days=1)

        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append((current_date, output_dir))
            current_date += delta

        self.stdout.write(f"Generating offices for {year} using {processes} processes...")

        # Close DB connections before forking
        connections.close_all()

        with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
            results = executor.map(generate_day_worker, dates)

            for i, result in enumerate(results):
                if result:
                    self.stdout.write(self.style.ERROR(result))

                if (i + 1) % 10 == 0:
                    self.stdout.write(f"Processed {i+1}/{len(dates)} days...")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated offices for {year}"))
