"""
Export database fixtures for testing.

This management command exports the minimal church calendar data needed for tests.
"""

from django.core.management.base import BaseCommand
from django.core import serializers
from churchcal.models import (
    Denomination,
    Calendar,
    CommemorationRank,
    Season,
    Commemoration,
    SanctoraleCommemoration,
    SanctoraleBasedCommemoration,
    TemporaleCommemoration,
    Common,
)
from office.models import StandardOfficeDay, Collect


class Command(BaseCommand):
    help = 'Export test fixtures for church calendar data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='churchcal/fixtures/test_calendar.json',
            help='Output file path for fixtures',
        )

    def handle(self, *args, **options):
        output_file = options['output']

        # Collect all objects to serialize
        objects_to_export = []

        # Export in dependency order
        self.stdout.write('Collecting Denominations...')
        objects_to_export.extend(Denomination.objects.all())

        self.stdout.write('Collecting Calendars...')
        objects_to_export.extend(Calendar.objects.all())

        self.stdout.write('Collecting CommemorationRanks...')
        objects_to_export.extend(CommemorationRank.objects.all())
        
        self.stdout.write('Collecting Collects...')
        # Export Collect objects (needed for Common)
        objects_to_export.extend(Collect.objects.all())
        
        self.stdout.write('Collecting Commons...')
        # Export Common objects (needed for SanctoraleCommemoration)
        objects_to_export.extend(Common.objects.all())

        self.stdout.write('Collecting Commemorations...')
        # Only export commemorations for ACNA calendar to reduce size
        acna_calendar = Calendar.objects.filter(abbreviation='ACNA_BCP2019').first()
        if acna_calendar:
            # Export all Commemoration objects (parent and subclasses)
            objects_to_export.extend(
                Commemoration.objects.filter(calendar=acna_calendar).select_related('rank', 'calendar')
            )
            # Export all SanctoraleCommemoration objects
            objects_to_export.extend(
                SanctoraleCommemoration.objects.filter(calendar=acna_calendar).select_related('rank', 'calendar', 'common')
            )
            # Export all SanctoraleBasedCommemoration objects
            objects_to_export.extend(
                SanctoraleBasedCommemoration.objects.filter(calendar=acna_calendar).select_related('rank', 'calendar')
            )
            # Export all TemporaleCommemoration objects
            objects_to_export.extend(
                TemporaleCommemoration.objects.filter(calendar=acna_calendar).select_related('rank', 'calendar')
            )
            # Note: FerialCommemoration is not exported (has managed=False, no DB table)

        self.stdout.write('Collecting Seasons...')
        if acna_calendar:
            objects_to_export.extend(
                Season.objects.filter(calendar=acna_calendar).select_related('calendar', 'start_commemoration')
            )

        self.stdout.write('Collecting StandardOfficeDays (sample)...')
        # Export a subset of office days for testing
        objects_to_export.extend(StandardOfficeDay.objects.filter(month__in=[1, 12])[:50])

        # Serialize to JSON
        self.stdout.write(f'Serializing {len(objects_to_export)} objects...')
        json_data = serializers.serialize(
            'json',
            objects_to_export,
            indent=2,
            use_natural_foreign_keys=False,
            use_natural_primary_keys=False,
        )

        # Write to file
        with open(output_file, 'w') as f:
            f.write(json_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(objects_to_export)} objects to {output_file}'))
