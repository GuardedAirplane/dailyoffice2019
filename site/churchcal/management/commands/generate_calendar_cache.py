from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

from churchcal.calculations import ChurchYear

DEFAULT_CALENDAR = getattr(settings, "DEFAULT_CALENDAR", "ACNA_BCP2019")


class Command(BaseCommand):
    help = "Generates and caches calendar data for specified years"

    def add_arguments(self, parser):
        parser.add_argument("years", nargs="+", type=int, help="Calendar years to generate (e.g. 2025 2026)")
        parser.add_argument(
            "--calendar",
            default=DEFAULT_CALENDAR,
            help="Calendar abbreviation to build (default: %(default)s)",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=60 * 60 * 24 * 365,
            help="Cache timeout in seconds (default: 1 year)",
        )

    def handle(self, *args, **options):
        years = options["years"]
        calendar = options["calendar"]
        timeout = options["timeout"]

        church_years_to_generate = set()
        for year in years:
            church_years_to_generate.update({year - 1, year})

        sorted_years = sorted(church_years_to_generate)

        if not sorted_years:
            self.stdout.write(self.style.WARNING("No years provided."))
            return

        for year in sorted_years:
            self.stdout.write(f"Generating Church Year starting Advent {year} for {calendar}...")
            church_year = ChurchYear(year, calendar)

            cache_key = f"{year}_{calendar}"
            cache.set(cache_key, church_year, timeout)

            if calendar == DEFAULT_CALENDAR:
                cache.set(str(year), church_year, timeout)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully generated and cached Church Year {year} (key={cache_key}, timeout={timeout}s)"
                )
            )
