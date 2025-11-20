from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

from churchcal.calculations import ChurchYear
from churchcal.utils import advent

DEFAULT_CALENDAR = getattr(settings, "DEFAULT_CALENDAR", "ACNA_BCP2019")


class Command(BaseCommand):
    help = "Ensures calendar cache exists for at least one year in the past and one year in the future"

    def add_arguments(self, parser):
        parser.add_argument(
            "--calendar",
            default=DEFAULT_CALENDAR,
            help="Calendar abbreviation to check (default: %(default)s)",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=60 * 60 * 24 * 365,
            help="Cache timeout in seconds (default: 1 year)",
        )

    def handle(self, *args, **options):
        calendar = options["calendar"]
        timeout = options["timeout"]

        # Determine current church year
        today = datetime.now().date()
        advent_start = advent(today.year)
        current_church_year = today.year if today >= advent_start else today.year - 1

        # We need cache for:
        # - Two years ago (for last calendar year)
        # - One year ago (for current calendar year start)
        # - Current year (for current calendar year end and next calendar year start)
        # - Next year (for next calendar year end)
        required_church_years = [
            current_church_year - 2,
            current_church_year - 1,
            current_church_year,
            current_church_year + 1,
        ]

        generated_count = 0
        for year in required_church_years:
            cache_key = f"{year}_{calendar}"
            church_year = cache.get(cache_key)

            if not church_year:
                self.stdout.write(f"Generating missing Church Year starting Advent {year} for {calendar}...")
                church_year = ChurchYear(year, calendar)
                cache.set(cache_key, church_year, timeout)

                # Also set default calendar format for backward compatibility
                if calendar == DEFAULT_CALENDAR:
                    cache.set(str(year), church_year, timeout)

                self.stdout.write(
                    self.style.SUCCESS(f"✓ Cached Church Year {year} (key={cache_key}, timeout={timeout}s)")
                )
                generated_count += 1
            else:
                self.stdout.write(f"✓ Church Year {year} already cached (key={cache_key})")

        if generated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\nGenerated {generated_count} church year(s). Cache is ready for use.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("\nAll required church years are already cached."))
