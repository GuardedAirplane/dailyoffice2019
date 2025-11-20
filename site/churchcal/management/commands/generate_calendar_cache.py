from django.core.management.base import BaseCommand
from django.core.cache import cache
from churchcal.calculations import ChurchYear
from website import settings


class Command(BaseCommand):
    help = "Generates and caches calendar data for specified years"

    def add_arguments(self, parser):
        parser.add_argument("years", nargs="+", type=int, help="Years to generate (e.g. 2025 2026)")

    def handle(self, *args, **options):
        years = options["years"]

        # To cover a calendar year, we need the church year starting in the previous year
        # and the church year starting in the current year.
        # e.g. 2025 requires ChurchYear(2024) and ChurchYear(2025)

        church_years_to_generate = set()
        for year in years:
            church_years_to_generate.add(year - 1)
            church_years_to_generate.add(year)

        # Also add the years themselves if they are meant to be church years
        for year in years:
            church_years_to_generate.add(year)

        sorted_years = sorted(list(church_years_to_generate))

        for year in sorted_years:
            self.stdout.write(f"Generating Church Year starting Advent {year}...")
            church_year = ChurchYear(year)

            # Cache for a very long time (e.g. 1 year)
            # The default in calculations.py is 12 hours, but we want this to persist
            # if the user is asking to 'add it to the database' (via cache)
            timeout = 60 * 60 * 24 * 365  # 1 year

            # Cache key format from calculations.py: str(year)
            # Note: calculations.py uses str(year) for the default calendar
            cache.set(str(year), church_year, timeout)

            self.stdout.write(self.style.SUCCESS(f"Successfully generated and cached Church Year {year}"))
