"""
Unit tests for canticle table lookups and rotation logic (Phase 14).

These tests validate that canticle tables correctly return appropriate
canticles based on liturgical date, season, and day of week.

Test Coverage:
- T166: Unit test DefaultCanticles table lookup
- T167: Unit test BCP1979CanticleTable lookup  
- T168: Unit test REC2011CanticleTable lookup
- T169: Unit test Canticle rotation (traditional/seasonal/daily)

Related FRs:
- FR-008: Display appropriate canticles for each office
- FR-026: Canticle customization options
"""

from django.test import TestCase
from datetime import date as date_class
from unittest.mock import Mock

from office.canticles import (
    DefaultCanticles,
    BCP1979CanticleTable,
    REC2011CanticleTable,
    MP1,
    MP2,
    MP3,
    EP1,
    EP2,
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S8,
    S10,
    O2,
)


def create_mock_calendar_date(date, season_name="Epiphanytide", precedence_rank=10, rank_name="SUNDAY"):
    """Create a mock calendar_date object for testing canticle tables."""
    mock_date = Mock()
    mock_date.date = date
    mock_date.season = Mock()
    mock_date.season.name = season_name
    mock_date.primary = Mock()
    mock_date.primary.rank = Mock()
    mock_date.primary.rank.precedence_rank = precedence_rank
    mock_date.primary.rank.name = rank_name
    mock_date.all = []
    return mock_date


class TestDefaultCanticlesTable(TestCase):
    """T166: Unit test DefaultCanticles table lookup."""

    def test_morning_prayer_canticle_1_outside_lent(self):
        """DefaultCanticles should return Te Deum (MP1) outside Lent."""
        date = date_class(2024, 1, 14)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = DefaultCanticles()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP1)
        self.assertEqual(result.english_name, "We Praise You, O God")

    def test_morning_prayer_canticle_1_during_lent(self):
        """DefaultCanticles should return MP2 during Lent."""
        date = date_class(2024, 2, 14)
        calendar_date = create_mock_calendar_date(date, season_name="Lent")
        canticles = DefaultCanticles()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP2)
        self.assertEqual(result.english_name, "A Song of Praise")

    def test_morning_prayer_canticle_2_always_benedictus(self):
        """DefaultCanticles should always return Benedictus (MP3) for MP canticle 2."""
        seasons = ["Christmastide", "Lent", "Eastertide", "Epiphanytide"]
        canticles = DefaultCanticles()

        for season in seasons:
            date = date_class(2024, 1, 15)
            calendar_date = create_mock_calendar_date(date, season_name=season)
            result = canticles.get_mp_canticle_2(calendar_date)

            self.assertEqual(result, MP3)
            self.assertEqual(result.english_name, "The Song of Zechariah")

    def test_evening_prayer_canticle_1_always_magnificat(self):
        """DefaultCanticles should always return Magnificat (EP1) for EP canticle 1."""
        seasons = ["Christmastide", "Lent", "Eastertide", "Epiphanytide"]
        canticles = DefaultCanticles()

        for season in seasons:
            date = date_class(2024, 1, 15)
            calendar_date = create_mock_calendar_date(date, season_name=season)
            result = canticles.get_ep_canticle_1(calendar_date)

            self.assertEqual(result, EP1)
            self.assertEqual(result.english_name, "The Song of Mary")

    def test_evening_prayer_canticle_2_always_nunc_dimittis(self):
        """DefaultCanticles should always return Nunc Dimittis (EP2) for EP canticle 2."""
        seasons = ["Christmastide", "Lent", "Eastertide", "Epiphanytide"]
        canticles = DefaultCanticles()

        for season in seasons:
            date = date_class(2024, 1, 15)
            calendar_date = create_mock_calendar_date(date, season_name=season)
            result = canticles.get_ep_canticle_2(calendar_date)

            self.assertEqual(result, EP2)
            self.assertEqual(result.english_name, "The Song of Simeon")


class TestBCP1979CanticleTable(TestCase):
    """T167: Unit test BCP1979CanticleTable lookup."""

    def test_sunday_morning_canticle_1_advent(self):
        """BCP1979 should return S2 (Surge, Illuminare) for Sunday in Advent."""
        # Sunday (weekday 6)
        date = date_class(2024, 12, 1)
        calendar_date = create_mock_calendar_date(date, season_name="Advent")
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S2)
        self.assertEqual(result.english_name, "Arise, shine, for your light has come")

    def test_sunday_morning_canticle_1_lent(self):
        """BCP1979 should return S3 (Kyrie Pantokrator) for Sunday in Lent."""
        # Sunday
        date = date_class(2024, 2, 18)
        calendar_date = create_mock_calendar_date(date, season_name="Lent")
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S3)
        self.assertEqual(result.english_name, "A Song of Penitence")

    def test_sunday_morning_canticle_1_eastertide(self):
        """BCP1979 should return S5 (Cantemus Domino) for Sunday in Eastertide."""
        # Sunday
        date = date_class(2024, 4, 7)
        calendar_date = create_mock_calendar_date(date, season_name="Eastertide")
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S5)
        self.assertEqual(result.english_name, "The Song of Moses")

    def test_weekday_rotation_monday(self):
        """BCP1979 should return S8 (Ecce, Deus) for Monday."""
        # Monday (weekday 0)
        date = date_class(2024, 1, 8)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S8)
        self.assertEqual(result.english_name, "Surely, it is God who saves me")

    def test_weekday_rotation_saturday(self):
        """BCP1979 should return S10 (Benedicite) for Saturday."""
        # Saturday (weekday 5)
        date = date_class(2024, 1, 13)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S10)
        self.assertEqual(result.english_name, "A Song of Creation")

    def test_feast_day_override_morning_canticle_1(self):
        """BCP1979 should return MP3 (Benedictus) for feast days."""
        # Christmas Day (Principal Feast, rank 1)
        date = date_class(2024, 12, 25)
        calendar_date = create_mock_calendar_date(date, season_name="Christmastide", precedence_rank=1)
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP3)

    def test_feast_day_override_morning_canticle_2(self):
        """BCP1979 should return MP1 (Te Deum) for feast days."""
        # Christmas Day (Principal Feast, rank 1)
        date = date_class(2024, 12, 25)
        calendar_date = create_mock_calendar_date(date, season_name="Christmastide", precedence_rank=1)
        canticles = BCP1979CanticleTable()

        result = canticles.get_mp_canticle_2(calendar_date)

        self.assertEqual(result, MP1)

    def test_evening_canticle_2_rotation(self):
        """BCP1979 should rotate between EP1 and EP2 for evening canticle 2."""
        canticles = BCP1979CanticleTable()

        # Sunday (weekday 6) - should return EP2
        sunday = date_class(2024, 1, 7)
        calendar_date_sun = create_mock_calendar_date(sunday, season_name="Epiphanytide")
        result_sun = canticles.get_ep_canticle_2(calendar_date_sun)
        self.assertEqual(result_sun, EP2)

        # Tuesday (weekday 1) - should return EP1
        tuesday = date_class(2024, 1, 9)
        calendar_date_tue = create_mock_calendar_date(tuesday, season_name="Epiphanytide")
        result_tue = canticles.get_ep_canticle_2(calendar_date_tue)
        self.assertEqual(result_tue, EP1)


class TestREC2011CanticleTable(TestCase):
    """T168: Unit test REC2011CanticleTable lookup."""

    def test_sunday_morning_canticle_1_always_te_deum(self):
        """REC2011 should return MP1 (Te Deum) for Sunday."""
        # Sunday (weekday 6)
        date = date_class(2024, 1, 14)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP1)
        self.assertEqual(result.english_name, "We Praise You, O God")

    def test_advent_seasonal_canticle(self):
        """REC2011 should return S1 (Magna et Mirabilia) during Advent."""
        # Monday in Advent (weekday 0)
        date = date_class(2024, 12, 2)
        calendar_date = create_mock_calendar_date(date, season_name="Advent")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S1)
        self.assertEqual(result.english_name, "The Song of the Redeemed")

    def test_epiphanytide_seasonal_canticle(self):
        """REC2011 should return S2 (Surge, Illuminare) during Epiphanytide."""
        # Monday in Epiphanytide (weekday 0)
        date = date_class(2024, 1, 8)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S2)
        self.assertEqual(result.english_name, "Arise, shine, for your light has come")

    def test_lent_seasonal_canticle(self):
        """REC2011 should return MP2 (Benedictus es, Domine) during Lent."""
        # Wednesday in Lent (weekday 2)
        date = date_class(2024, 2, 21)
        calendar_date = create_mock_calendar_date(date, season_name="Lent")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP2)
        self.assertEqual(result.english_name, "A Song of Praise")

    def test_eastertide_seasonal_canticle(self):
        """REC2011 should return S5 (Cantemus Domino) during Eastertide."""
        # Monday in Eastertide (weekday 0)
        date = date_class(2024, 4, 8)
        calendar_date = create_mock_calendar_date(date, season_name="Eastertide")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S5)
        self.assertEqual(result.english_name, "The Song of Moses")

    def test_season_after_pentecost_ecce_deus(self):
        """REC2011 should return S8 (Ecce, Deus) during Season After Pentecost."""
        # Monday after Pentecost (weekday 0)
        date = date_class(2024, 6, 3)
        calendar_date = create_mock_calendar_date(date, season_name="Season After Pentecost")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S8)
        self.assertEqual(result.english_name, "Surely, it is God who saves me")

    def test_season_after_pentecost_saturday_benedicite(self):
        """REC2011 should return S10 (Benedicite) on Saturday after Pentecost."""
        # Saturday after Pentecost (weekday 5)
        date = date_class(2024, 6, 8)
        calendar_date = create_mock_calendar_date(date, season_name="Season After Pentecost")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, S10)
        self.assertEqual(result.english_name, "A Song of Creation")

    def test_morning_canticle_2_always_benedictus(self):
        """REC2011 should return MP3 (Benedictus) for morning canticle 2, except April 29."""
        # Regular day
        date = date_class(2024, 1, 15)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_2(calendar_date)

        self.assertEqual(result, MP3)
        self.assertEqual(result.english_name, "The Song of Zechariah")

    def test_april_29_jubilate(self):
        """REC2011 should return O2 (Jubilate) on April 29."""
        # April 29
        date = date_class(2024, 4, 29)
        calendar_date = create_mock_calendar_date(date, season_name="Eastertide")
        canticles = REC2011CanticleTable()

        result = canticles.get_mp_canticle_2(calendar_date)

        self.assertEqual(result, O2)
        self.assertEqual(result.english_name, "Be Joyful")

    def test_evening_canticle_1_always_magnificat(self):
        """REC2011 should return EP1 (Magnificat) for evening canticle 1, except November 13."""
        # Regular day
        date = date_class(2024, 1, 15)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = REC2011CanticleTable()

        result = canticles.get_ep_canticle_1(calendar_date)

        self.assertEqual(result, EP1)
        self.assertEqual(result.english_name, "The Song of Mary")

    def test_feast_day_override_evening_canticle_2(self):
        """REC2011 should return EP2 (Nunc Dimittis) for feast days."""
        # Christmas Day (Principal Feast, rank 1)
        date = date_class(2024, 12, 25)
        calendar_date = create_mock_calendar_date(date, season_name="Christmastide", precedence_rank=1)
        canticles = REC2011CanticleTable()

        result = canticles.get_ep_canticle_2(calendar_date, None)

        self.assertEqual(result, EP2)

    def test_sunday_evening_canticle_2_nunc_dimittis(self):
        """REC2011 should return EP2 (Nunc Dimittis) for Sunday evening."""
        # Sunday (weekday 6)
        date = date_class(2024, 1, 14)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")
        canticles = REC2011CanticleTable()

        result = canticles.get_ep_canticle_2(calendar_date, None)

        self.assertEqual(result, EP2)


class TestCanticleRotationLogic(TestCase):
    """T169: Unit test Canticle rotation (traditional/seasonal/daily)."""

    def test_traditional_rotation_te_deum_on_sundays(self):
        """Traditional rotation uses Te Deum on Sundays outside Lent."""
        # Sunday in Epiphanytide
        date = date_class(2024, 1, 14)
        calendar_date = create_mock_calendar_date(date, season_name="Epiphanytide")

        traditional = DefaultCanticles()
        result = traditional.get_mp_canticle_1(calendar_date)

        self.assertEqual(result, MP1)

    def test_seasonal_rotation_varies_by_season(self):
        """Seasonal rotation (REC2011) varies canticles by liturgical season."""
        canticles = REC2011CanticleTable()

        # Advent: S1 (Magna et Mirabilia)
        advent = date_class(2024, 12, 2)
        advent_cal = create_mock_calendar_date(advent, season_name="Advent")
        advent_result = canticles.get_mp_canticle_1(advent_cal)
        self.assertEqual(advent_result, S1)

        # Epiphanytide: S2 (Surge, Illuminare)
        epiphany = date_class(2024, 1, 8)
        epiphany_cal = create_mock_calendar_date(epiphany, season_name="Epiphanytide")
        epiphany_result = canticles.get_mp_canticle_1(epiphany_cal)
        self.assertEqual(epiphany_result, S2)

        # Lent: MP2 (Benedictus es, Domine)
        lent = date_class(2024, 2, 21)
        lent_cal = create_mock_calendar_date(lent, season_name="Lent")
        lent_result = canticles.get_mp_canticle_1(lent_cal)
        self.assertEqual(lent_result, MP2)

        # Eastertide: S5 (Cantemus Domino)
        easter = date_class(2024, 4, 8)
        easter_cal = create_mock_calendar_date(easter, season_name="Eastertide")
        easter_result = canticles.get_mp_canticle_1(easter_cal)
        self.assertEqual(easter_result, S5)

    def test_daily_rotation_varies_by_day_of_week(self):
        """Daily rotation (BCP1979) varies canticles by day of week."""
        canticles = BCP1979CanticleTable()

        # Monday: S8 (Ecce, Deus)
        monday = date_class(2024, 1, 8)
        monday_cal = create_mock_calendar_date(monday, season_name="Epiphanytide")
        monday_result = canticles.get_mp_canticle_1(monday_cal)
        self.assertEqual(monday_result, S8)

        # Tuesday: MP2 (Benedictus es, Domine)
        tuesday = date_class(2024, 1, 9)
        tuesday_cal = create_mock_calendar_date(tuesday, season_name="Epiphanytide")
        tuesday_result = canticles.get_mp_canticle_1(tuesday_cal)
        self.assertEqual(tuesday_result, MP2)

        # Thursday: S5 (Cantemus Domino)
        thursday = date_class(2024, 1, 11)
        thursday_cal = create_mock_calendar_date(thursday, season_name="Epiphanytide")
        thursday_result = canticles.get_mp_canticle_1(thursday_cal)
        self.assertEqual(thursday_result, S5)

        # Saturday: S10 (Benedicite)
        saturday = date_class(2024, 1, 13)
        saturday_cal = create_mock_calendar_date(saturday, season_name="Epiphanytide")
        saturday_result = canticles.get_mp_canticle_1(saturday_cal)
        self.assertEqual(saturday_result, S10)

    def test_rotation_respects_feast_day_precedence(self):
        """All rotation modes should respect feast day precedence."""
        christmas = date_class(2024, 12, 25)
        calendar_date = create_mock_calendar_date(christmas, season_name="Christmastide", precedence_rank=1)

        # BCP1979: Should use MP3 (Benedictus) for feast days
        bcp1979 = BCP1979CanticleTable()
        bcp1979_result = bcp1979.get_mp_canticle_1(calendar_date)
        self.assertEqual(bcp1979_result, MP3)

        # REC2011: Should use MP1 (Te Deum) for feast days
        rec2011 = REC2011CanticleTable()
        rec2011_result = rec2011.get_mp_canticle_1(calendar_date)
        self.assertEqual(rec2011_result, MP1)

    def test_all_rotations_include_gospel_canticles(self):
        """All rotation modes should include traditional Gospel canticles."""
        # Test that all rotations include Benedictus (MP3) for MP canticle 2
        # Use Wednesday for BCP1979 (returns MP3 for MP canticle 2)
        wednesday = date_class(2024, 1, 17)  # Wednesday
        wed_calendar = create_mock_calendar_date(wednesday, season_name="Epiphanytide")

        default = DefaultCanticles()
        bcp1979 = BCP1979CanticleTable()
        rec2011 = REC2011CanticleTable()

        # All rotations include Benedictus (MP3) for MP canticle 2
        self.assertEqual(default.get_mp_canticle_2(wed_calendar), MP3)
        self.assertEqual(bcp1979.get_mp_canticle_2(wed_calendar), MP3)
        self.assertEqual(rec2011.get_mp_canticle_2(wed_calendar), MP3)

        # Test that all rotations include Magnificat (EP1) for EP canticle 1
        # Use Sunday for BCP1979 (returns EP1 for EP canticle 1)
        sunday = date_class(2024, 1, 14)  # Sunday
        sun_calendar = create_mock_calendar_date(sunday, season_name="Epiphanytide")

        # All rotations include Magnificat (EP1) for EP canticle 1 on at least some days
        self.assertEqual(default.get_ep_canticle_1(sun_calendar), EP1)
        self.assertEqual(bcp1979.get_ep_canticle_1(sun_calendar), EP1)
        self.assertEqual(rec2011.get_ep_canticle_1(sun_calendar), EP1)
