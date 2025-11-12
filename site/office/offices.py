import datetime
import logging
import time
from typing import Dict, List, Any, Optional, Tuple

from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe, SafeString

from office.models import HolyDayOfficeDay, StandardOfficeDay, ThirtyDayPsalterDay
from office.utils import passage_to_citation

# Performance monitoring logger
logger = logging.getLogger(__name__)


class Office(object):
    """
    Base class for all Daily Office types in the BCP 2019 tradition.
    
    Provides core functionality for office generation including:
    - Date handling and liturgical calendar integration
    - Psalm and reading assignments
    - Navigation between office types and dates
    - Performance monitoring
    
    Validates: FR-001, FR-002, FR-003, FR-004 (Office Types)
    Validates: FR-007 (Use Proper Readings for Feast Days and Sundays)
    Validates: FR-012 (View Offices for Any Date)
    Validates: FR-013 (Navigation Between Office Types)
    Validates: SC-001 (Office Load Time < 3 seconds)
    
    Attributes:
        name (str): Human-readable name of the office type
        modules (list): Ordered list of OfficeSection instances comprising the office
        date (CalendarDate): Liturgical calendar date for this office
        office_readings (OfficeDay): Assigned readings for this date
        thirty_day_psalter_day (ThirtyDayPsalterDay): Psalm assignments for this calendar day
        title (str): Full page title for SEO and browser display
    """
    name = "Daily Office"
    modules = []

    def get_formatted_date_string(self) -> str:
        """
        Format the office date for human-readable display.
        
        Returns:
            str: Date formatted as "Wednesday January 1, 2025"
        """
        return "{dt:%A} {dt:%B} {dt.day}, {dt.year}".format(dt=self.date.date)

    def __init__(self, date: Any) -> None:
        """
        Initialize Office for any valid date.
        
        Validates: FR-007 (Use Proper Readings for Feast Days and Sundays)
        Validates: FR-012 (View Offices for Any Date)
        Validates: SC-001 (Office Load Time < 3 seconds) - Performance monitoring
        """
        # Performance monitoring: Track office initialization time
        start_time = time.time()
        
        from churchcal.calculations import get_calendar_date
        from churchcal.models import FerialCommemoration

        self.date = get_calendar_date(date)

        # FerialCommemoration instances are not saved to the database (managed=False)
        # so we cannot query HolyDayOfficeDay with them. For ferias, use StandardOfficeDay.
        # FR-007: Feast days override standard readings via HolyDayOfficeDay
        if isinstance(self.date.primary, FerialCommemoration):
            self.office_readings = StandardOfficeDay.objects.get(month=self.date.date.month, day=self.date.date.day)
        else:
            try:
                self.office_readings = HolyDayOfficeDay.objects.get(commemoration=self.date.primary)
            except HolyDayOfficeDay.DoesNotExist:
                self.office_readings = StandardOfficeDay.objects.get(month=self.date.date.month, day=self.date.date.day)

        self.thirty_day_psalter_day = ThirtyDayPsalterDay.objects.get(day=self.date.date.day)

        primary_feast_name = (
            self.date.primary_evening.name
            if self.name == "Evening Prayer" or self.name == "Compline"
            else self.date.primary.name
        )
        self.title = "{} for {}: {} | The Daily Office according to The Book of Common Prayer (2019)".format(
            self.name, self.get_formatted_date_string(), primary_feast_name
        )
        
        # Performance monitoring: Log initialization time
        init_duration = (time.time() - start_time) * 1000  # Convert to ms
        logger.debug(
            f"Office.__init__ completed in {init_duration:.2f}ms "
            f"(office={self.name}, date={date}, commemoration={primary_feast_name})"
        )

    @cached_property
    def links(self) -> Dict[str, Any]:
        """
        Generate navigation links for office types and dates.
        
        Validates: FR-013 (Navigation Between Office Types)
        """
        today = self.date.date
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)

        return {
            "yesterday": {
                "label": yesterday.strftime("%a"),
                "link": reverse(self.office, args=[yesterday.year, yesterday.month, yesterday.day]),
            },
            "tomorrow": {
                "label": tomorrow.strftime("%a"),
                "link": reverse(self.office, args=[tomorrow.year, tomorrow.month, tomorrow.day]),
            },
            "morning_prayer": {
                "label": "Morning",
                "link": reverse("morning_prayer", args=[today.year, today.month, today.day]),
            },
            "midday_prayer": {
                "label": "Midday",
                "link": reverse("midday_prayer", args=[today.year, today.month, today.day]),
            },
            "evening_prayer": {
                "label": "Evening",
                "link": reverse("evening_prayer", args=[today.year, today.month, today.day]),
            },
            "compline": {"label": "Compline", "link": reverse("compline", args=[today.year, today.month, today.day])},
            "family_morning_prayer": {
                "label": "Morning",
                "link": reverse("family_morning_prayer", args=[today.year, today.month, today.day]),
            },
            "family_midday_prayer": {
                "label": "Midday",
                "link": reverse("family_midday_prayer", args=[today.year, today.month, today.day]),
            },
            "family_early_evening_prayer": {
                "label": "Early Evening",
                "link": reverse("family_early_evening_prayer", args=[today.year, today.month, today.day]),
            },
            "family_close_of_day_prayer": {
                "label": "Close of Day",
                "link": reverse("family_close_of_day_prayer", args=[today.year, today.month, today.day]),
            },
            "current": self.office,
            "date": f"{today:%B} {today.day}, {today.year}",
        }


class OfficeSection(object):
    """
    Base class for all modular sections within a Daily Office.
    
    Each OfficeSection represents a distinct liturgical component (e.g., readings,
    psalms, prayers, canticles). Subclasses implement the `data` property to provide
    section-specific content.
    
    Args:
        date (CalendarDate): Liturgical calendar date
        office_readings (OfficeDay, optional): Reading assignments for this date
        thirty_day_psalter_day (ThirtyDayPsalterDay, optional): Psalm assignments
        office (Office, optional): Parent office instance
    
    Attributes:
        date (CalendarDate): Liturgical calendar date for this section
        office_readings (OfficeDay): Reading assignments
        thirty_day_psalter_day (ThirtyDayPsalterDay): Psalm assignments
        office (Office): Parent office instance
    """
    def __init__(self, date: Any, office_readings: Optional[Any] = None, 
                 thirty_day_psalter_day: Optional[Any] = None, office: Optional[Any] = None) -> None:
        self.date = date
        self.office_readings = office_readings
        self.thirty_day_psalter_day = thirty_day_psalter_day
        self.office = office

    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate section-specific liturgical content.
        
        Must be implemented by subclasses to provide the data structure
        required for template rendering.
        
        Returns:
            dict: Section content data
            
        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError


class Reading(OfficeSection):
    """
    Base class for scripture reading sections in Daily Office.
    
    Handles retrieval and formatting of Bible passages including:
    - Main readings (long form)
    - Abbreviated readings (short form)
    - Alternate readings
    - Mass readings (for major feasts)
    
    Validates: FR-006 (Lectionary Integration)
    Validates: FR-007 (Proper Readings for Feast Days)
    Validates: FR-020 (Bible Gateway API Retrieval)
    """
    @staticmethod
    def closing(testament: str) -> Dict[str, str]:
        """
        Generate appropriate closing formula for scripture reading.
        
        Args:
            testament (str): Testament code ('OT', 'NT', 'DC' for Deuterocanon, 'PS' for Psalms)
        
        Returns:
            dict: Reader and people response text
        """
        return {
            "reader": "The Word of the Lord." if testament != "DC" else "Here ends the Reading.",
            "people": "Thanks be to God." if testament != "DC" else "",
        }

    def data(self) -> Dict[str, Any]:
        """
        Compile all reading variants into a unified data structure.
        
        Returns:
            dict: Contains heading, flags for available reading types, and reading content
        """
        return {
            "heading": self.heading,
            "has_main_reading": self.has_main_reading,
            "has_abbreviated_reading": self.has_abbreviated_reading,
            "has_alternate_reading": self.has_alternate_reading,
            "has_alternate_abbreviated_reading": self.has_alternate_abbreviated_reading,
            "has_mass_reading": self.has_mass_reading,
            "has_abbreviated_mass_reading": self.has_abbreviated_mass_reading,
            "main_reading": self.get_main_reading(),
            "abbreviated_reading": self.get_abbreviated_reading(),
            "alternate_reading": self.get_alternate_reading(),
            "alternate_abbreviated_reading": self.get_alternate_abbreviated_reading(),
            "mass_reading": self.get_mass_reading(),
            "abbreviated_mass_reading": self.get_abbreviated_mass_reading(),
            "tag_prefix": self.tag,
        }


class ThirdReading(Reading):
    """
    Optional third lesson for major feast days (precedence rank ≤ 4).
    
    Used only when mass readings are assigned for a major feast.
    
    Validates: FR-007 (Proper Readings for Feast Days)
    """
    heading = "The Third Lesson"
    tag = "third-"

    @cached_property
    def has_main_reading(self) -> bool:
        return False

    @cached_property
    def has_abbreviated_reading(self) -> bool:
        return False

    @cached_property
    def has_alternate_reading(self) -> bool:
        return False

    @cached_property
    def has_alternate_abbreviated_reading(self) -> bool:
        return False

    @cached_property
    def has_mass_reading(self) -> bool:
        return self.date.primary.rank.precedence_rank <= 4

    @cached_property
    def has_abbreviated_mass_reading(self) -> bool:
        if not self.has_mass_reading:
            return False
        for reading in self.date.mass_readings:
            if reading.reading_number == 4 and reading.short_citation:
                return True
        return False

    def get_main_reading(self) -> None:
        """Third reading has no main reading variant."""
        return None

    def get_abbreviated_reading(self) -> None:
        """Third reading has no abbreviated variant."""
        return None

    def get_alternate_reading(self) -> None:
        """Third reading has no alternate variant."""
        return None

    def get_alternate_abbreviated_reading(self) -> None:
        """Third reading has no alternate abbreviated variant."""
        return None

    def get_mass_reading(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve mass reading for major feasts (reading number 4).
        
        Returns:
            dict or None: Reading data with intro, passage, text, closing
        """
        if not self.has_mass_reading:
            return None
        for reading in self.date.mass_readings:
            if reading.reading_number == 4:
                return {
                    "intro": passage_to_citation(reading.long_citation),
                    "passage": reading.long_citation,
                    "reading": reading.long_text,
                    "closing": self.closing(reading.testament),
                    "tag": "mass-reading",
                    "deuterocanon": reading.testament == "DC",
                }

        return None

    def get_abbreviated_mass_reading(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve abbreviated mass reading for major feasts.
        
        Returns:
            dict or None: Abbreviated reading data
        """
        if not self.has_abbreviated_mass_reading:
            return None
        for reading in self.date.mass_readings:
            if reading.reading_number == 4 and reading.short_citation:
                return {
                    "intro": passage_to_citation(reading.short_citation),
                    "passage": reading.short_citation,
                    "reading": reading.short_text,
                    "closing": self.closing(reading.testament),
                    "tag": "abbreviated-mass-reading",
                    "deuterocanon": reading.testament == "DC",
                }

        return None


class Confession(OfficeSection):
    """
    Confession of Sin section for Daily Office.
    
    Provides confession text with variations for fast days.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate confession section data.
        
        Returns:
            dict: Heading and fast day indicator
        """
        return {"heading": "Confession of Sin", "fast_day": self.date.fast_day}


class Invitatory(OfficeSection):
    """
    Invitatory section with Venite or Jubilate canticle.
    
    Validates: FR-008 (Display Appropriate Canticles)
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate invitatory section data.
        
        Returns:
            dict: Empty dict (content handled by template)
        """
        return {}


class Creed(OfficeSection):
    """
    The Apostles' Creed section.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate creed section data.
        
        Returns:
            dict: Empty dict (content handled by template)
        """
        return {}


class Prayers(OfficeSection):
    """
    The Prayers section including Lord's Prayer.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate prayers section data.
        
        Returns:
            dict: Section heading
        """
        return {"heading": "The Prayers"}


class PandemicPrayers(OfficeSection):
    """
    Special collects for pandemic and election periods (2020).
    
    Rotates through collects on a daily/weekly basis to provide variety.
    Historical implementation for COVID-19 pandemic period.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    election_start_date = datetime.datetime.strptime("2020/10/27 0:00:00", "%Y/%m/%d %H:%M:%S").date()
    election_end_date = datetime.datetime.strptime("2020/11/04 23:59:59", "%Y/%m/%d %H:%M:%S").date()

    def get_collect_1(self) -> Dict[str, str]:
        """
        Retrieve first pandemic-related collect (3-day rotation).
        
        Returns:
            dict: Collect with title, text, response, citation
        """
        collects = [
            {
                "title": "In Time of Great Sickness and Mortality",
                "collect": "O Most mighty and merciful God, in this time of grievous sickness, we flee to you for comfort. Deliver us, we beseech you, from our peril; give strength and skill to all those who minister to the sick; prosper the means made use of for their cure; and grant that, perceiving how frail and uncertain our life is, we may apply our hearts unto that heavenly wisdom which leads to eternal life; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "Book of Common Prayer, 1928 (U.S.)".upper(),
            },
            {
                "title": "In the Time of any Common Plague or Sickness",
                "collect": "O Almighty God, who in your wrath sent a plague upon your own people in the wilderness for their obstinate rebellion against Moses and Aaron, and also in the time of King David, sent a plague of pestilence which killed seventy thousand, but remembering your mercy spared the rest: have pity upon us miserable sinners, who now are visited with great sickness and mortality; and in the same way that you then accepted an atonement and commanded the destroying Angel to cease from punishing: so it may now please you to withdraw from us this plague and grievous sickness, through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "Book of Common Prayer, 1662 (England)".upper(),
            },
            {
                "title": "Prayer for the Great Plague of 1665",
                "collect": "O Most gracious God, Father of mercies and of our Lord Jesus Christ, look down upon us, we beseech you, in much pity and compassion and behold our great misery and trouble. For there is wrath gone out against us, and the plague has begun. That dreadful arrow of yours sticks fast in our flesh, and the venom thereof fires our blood and drinks up our spirits. Should you suffer it to bring us all to the dust of death, we must yet still acknowledge that you are righteous, O Lord, and your judgements are just. For our transgressions multiplied against you, as the sand on the sea-shore might justly bring over us a deluge of your wrath. The cry of our sins that has pierced the very heavens might well return with showers of vengeance upon our heads. While our earth is defiled by the inhabitants of it, what wonder; if you command an evil angel to pour out his vial into our air to fill it with infection and the noisome pestilence and so to turn the very breath of our Life into the savour of death unto us all! But yet we beseech you, O our God, forget not to be gracious: neither shut up your loving kindness in displeasure. For his sake, who himself took our infirmities and bore our sicknesses, have mercy upon us; and say to the destroying Angel, “It is enough”. O let that blood of sprinkling, which speaks better things then that of Abel be upon the Lintel and the two side posts in all our dwellings, that the destroyer may pass by. Let the sweet odor of your blessed Son's all-sufficient sacrifice and intercession (infinitely more prevalent than the typical incense of Aaron) interpose between the living and the dead and be our full and perfect atonement, ever acceptable with you, that the plague may be stayed. O let us live and we will praise your Name, and these your judgments shall teach us to look every man into the plague of his own heart: that being cleansed from all our sins, we may serve you with pure hearts all our days, perfecting holiness in your fear until we come at last where there is no more sickness nor death through your tender mercies in him alone who is our Life, and our health, and our salvation, Jesus Christ, our ever blessed savior and redeemer.",
                "response": "Amen.",
                "citation": "1665, Gilbert Sheldon, Archbishop of Canterbury".upper(),
            },
        ]

        day_of_year = self.date.date.timetuple().tm_yday
        collect_number = day_of_year % 2
        if self.office.office == "morning_prayer":
            return collects[collect_number]
        return collects[1 - collect_number]

    def get_collect_2(self) -> Dict[str, str]:
        """
        Retrieve second pandemic-related collect (7-day weekday rotation).
        
        Returns:
            dict: Collect with title, text, response, citation
        """
        collects = [
            {
                "title": "In Times of Natural Disaster",
                "collect": "Almighty God, by your Word you laid the foundations of the earth, set the bounds of the sea, and still the wind and waves. Surround us with your grace and peace, and preserve us through this plague. By your Spirit, lift up those who have fallen, strengthen those who work to rescue or rebuild, and fill us with the hope of your new creation; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#26, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "In Times of Social Conflict or Unrest",
                "collect": " Increase, O God, the spirit of neighborliness among us, that in peril we may uphold one another, in suffering tend to one another, and in homelessness, loneliness, or exile befriend one another. Grant us brave and enduring hearts that we may strengthen one another, until the disciplines and testing of these days are ended, and you again give peace in our time; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#44, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "For the Recovery of a Sick Person",
                "collect": "Almighty and immortal God, giver of life and health: We implore your mercy for your servants who are sickened by this virus, that by your blessing upon them and upon those who minister to them with your healing gifts, they may be restored to health of body and mind, according to your gracious will, and may give thanks to you in your holy Church; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#61, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "For Civil Authorities",
                "collect": "Almighty God, our heavenly Father, send down on those who hold public office, especially those working to stop the spread of the Coronavirus, the spirit of wisdom, charity, and justice; that with steadfast purpose they may faithfully serve in their offices to promote the well being of all people; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#30, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "For Those Who Serve Others",
                "collect": "O Lord our heavenly Father, whose blessed Son came not to be served, but to serve: We ask you to bless all who, following in his steps, give themselves to the service of others especially those who are laboring in this time of plague; endue them with wisdom, patience, and courage, that they may strengthen the weak and raise up those who fall, and, being inspired by your love, may worthily minister to the suffering, the friendless, and the needy; for the sake of him who laid down his life for us, your Son our Savior Jesus Christ.",
                "response": "Amen.",
                "citation": "#45, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "For the Medical Professions",
                "collect": "Almighty God, whose blessed Son Jesus Christ went about doing good, and healing all manner of sickness and disease among the people: Continue in our hospitals his gracious work among us especially in this time of plague and pandemic; console and heal the sick; grant to the physicians, nurses, and assisting staff wisdom and skill, diligence and patience; prosper their work, O Lord, and send down your blessing upon all who serve the suffering; through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#50, Book of Common Prayer (2019)".upper(),
            },
            {
                "title": "For Trustfulness in Times of Worry and Anxiety",
                "collect": "Most loving Father, you will us to give thanks for all things, to dread nothing but the loss of you, and to cast all our care on the One who cares for us. Preserve us from faithless fears and worldly anxieties, and grant that no clouds of this mortal life may hide from us the light of that love which is immortal, and which you have manifested unto us in your Son, Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#80, Book of Common Prayer (2019)".upper(),
            },
        ]

        if self.office.office == "morning_prayer":
            return collects[self.date.date.weekday()]

        return collects[6 - self.date.date.weekday()]

    def get_collect_3(self) -> Optional[Dict[str, str]]:
        """
        Retrieve election-specific collect (only during Oct 27 - Nov 4, 2020).
        
        Returns:
            dict or None: Collect data if within election period, None otherwise
        """
        if self.date.date >= self.election_start_date and self.date.date <= self.election_end_date:
            return {
                "title": "For an Election",
                "collect": "Almighty God, to whom we must account for all our powers and privileges: Guide and direct, we humbly pray, the minds of all those who are called to elect fit persons to serve in the presidency and offices across the country. Grant that in the exercise of our choice we may promote your glory, and the welfare of this nation. This we ask for the sake of our Lord and Savior Jesus Christ.",
                "response": "Amen.",
                "citation": "#31, Book of Common Prayer (2019)".upper(),
            }
        return None

    def get_collect_4(self) -> Optional[Dict[str, str]]:
        """
        Retrieve national prayer during election period (only during Oct 27 - Nov 4, 2020).
        
        Returns:
            dict or None: Collect data if within election period, None otherwise
        """
        if self.date.date >= self.election_start_date and self.date.date <= self.election_end_date:
            return {
                "title": "For Our Nation",
                "collect": "Almighty God, who hast given us this good land for our heritage: We humbly beseech thee that we may always prove ourselves a people mindful of thy favor and glad to do thy will. Bless our land with honorable industry, sound learning, and pure conduct. Save us from violence, discord, and confusion; from pride and arrogance, and from every evil way. Defend our liberties, and fashion into one united people the multitudes brought hither out of many kindreds and tongues. Endue with the spirit of wisdom those to whom, in thy Name, we entrust the authority of government, that there may be justice and peace at home, and that, through obedience to thy law, we may show forth thy praise among the nations of the earth. In the time of prosperity, fill our hearts with thankfulness, and in the day of trouble, suffer not our trust in thee to fail; all of which we ask through Jesus Christ our Lord.",
                "response": "Amen.",
                "citation": "#39, Book of Common Prayer (2019)".upper(),
            }
        return None

    @cached_property
    def data(self) -> Dict[str, Optional[Dict[str, str]]]:
        """
        Compile all pandemic-related collects.
        
        Returns:
            dict: Up to 4 collects (collect_1 through collect_4)
        """
        return {
            "collect_1": self.get_collect_1(),
            "collect_2": self.get_collect_2(),
            "collect_3": self.get_collect_3(),
            "collect_4": self.get_collect_4(),
        }


class Intercessions(OfficeSection):
    """
    Intercessions and Thanksgivings section.
    
    Rubrics invite the congregation to offer prayers.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, str]:
        """
        Generate intercessions section data.
        
        Returns:
            dict: Heading and rubric text
        """
        return {
            "heading": "Intercessions and Thanksgivings",
            "rubric_1": "The Officiant may invite the People to offer intercessions and thanksgivings.",
            "rubric_2": "A hymn or anthem may be sung.",
        }


class GeneralThanksgiving(OfficeSection):
    """
    The General Thanksgiving prayer.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, str]:
        """
        Generate general thanksgiving section data.
        
        Returns:
            dict: Section heading
        """
        return {"heading": "The General Thanksgiving"}


class Chrysostom(OfficeSection):
    """
    Prayer of St. John Chrysostom.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    """
    @cached_property
    def data(self) -> Dict[str, str]:
        """
        Generate Chrysostom prayer section data.
        
        Returns:
            dict: Section heading
        """
        return {"heading": "A PRAYER OF ST. JOHN CHRYSOSTOM"}


class Dismissal(OfficeSection):
    """
    Dismissal section with seasonal variations and grace.
    
    Includes Alleluia during Eastertide and rotating grace formulas.
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    Validates: FR-014 (Calculate Correct Liturgical Season) - Eastertide detection
    """
    def get_fixed_grace(self) -> Dict[str, str]:
        """
        Retrieve standard grace formula (2 Corinthians 13:14).
        
        Returns:
            dict: Officiant text, people response, citation
        """
        return {
            "officiant": "The grace of our Lord Jesus Christ, and the love of God, and the fellowship of the Holy Spirit, be with us all evermore.",
            "people": "Amen.",
            "citation": "2 CORINTHIANS 13:14",
        }

    def get_grace(self) -> Dict[str, str]:
        """
        Retrieve grace formula based on day of week rotation.
        
        Returns:
            dict: Officiant text, people response, citation
        """
        if self.date.date.weekday() in (6, 2, 5):
            return {
                "officiant": "The grace of our Lord Jesus Christ, and the love of God, and the fellowship of the Holy Spirit, be with us all evermore.",
                "people": "Amen.",
                "citation": "2 CORINTHIANS 13:14",
            }
        if self.date.date.weekday() in (0, 3):
            return {
                "officiant": "May the God of hope fill us with all joy and peace in believing through the power of the Holy Spirit. ",
                "people": "Amen.",
                "citation": "ROMANS 15:13",
            }

        if self.date.date.weekday() in (1, 4):
            return {
                "officiant": "Glory to God whose power, working in us, can do infinitely more than we can ask or imagine: Glory to him from generation to generation in the Church, and in Christ Jesus for ever and ever.",
                "people": "Amen.",
                "citation": "EPHESIANS 3:20-21",
            }

    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate dismissal section data with seasonal variations.
        
        Adds "Alleluia, alleluia" during Eastertide.
        
        Returns:
            dict: Heading, officiant/people text, grace formulas
        """
        morning_easter = self.office.office not in ["evening_prayer"] and self.date.season.name == "Eastertide"
        evening_easter = self.office.office in ["evening_prayer"] and self.date.evening_season.name == "Eastertide"

        officiant = "Let us bless the Lord."
        people = "Thanks be to God."

        if morning_easter or evening_easter:
            officiant = "{} Alleluia, alleluia.".format(officiant)
            people = "{} Alleluia, alleluia.".format(people)

        return {
            "heading": "Dismissal",
            "officiant": officiant,
            "people": people,
            "grace": self.get_grace(),
            "fixed_grace": self.get_fixed_grace(),
        }


class FMCreed(OfficeSection):
    """
    Family Morning Prayer simplified creed section.
    
    Validates: FR-018 (Provide Family Prayer Offices)
    """
    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate family morning creed section data.
        
        Returns:
            dict: Empty dict (content handled by template)
        """
        return {}


class FamilyRubricSection(OfficeSection):
    """
    Introductory rubric for Family Prayer offices.
    
    Explains the simplified structure for families with young children.
    
    Validates: FR-018 (Provide Family Prayer Offices)
    """
    @cached_property
    def data(self) -> Dict[str, SafeString]:
        """
        Generate family prayer rubric section data.
        
        Returns:
            dict: Rubric text with HTML formatting
        """
        return {
            "rubric": mark_safe(
                "<br>These devotions follow the basic structure of the Daily Office of the Church and are particularly appropriate for families with young children.<br><br>The Reading and the Collect may be read by one person, and the other parts said in unison, or in some other convenient manner."
            )
        }


class FamilyIntercessions(OfficeSection):
    """
    Simplified intercessions section for Family Prayer.
    
    Validates: FR-018 (Provide Family Prayer Offices)
    """
    @cached_property
    def data(self) -> Dict[str, str]:
        """
        Generate family intercessions section data.
        
        Returns:
            dict: Heading and rubric text
        """
        return {
            "title": "Intercessions",
            "rubric": mark_safe(
                "A hymn or canticle may be used.<br><br>Prayers may be offered for ourselves and others."
            ),
        }


class GreatLitany(OfficeSection):
    """
    The Great Litany section with saint commemorations.
    
    Includes dynamic saint names and national variations (US/Canada).
    
    Validates: FR-009 (Include Full Text of Prayers and Liturgical Components)
    Validates: FR-011 (Display Commemorations)
    """
    def get_names(self) -> str:
        """
        Retrieve list of saint names for commemoration.
        
        Always includes the Blessed Virgin Mary, plus any additional saints
        commemorated on this date.
        
        Returns:
            str: Comma-separated list of saint names
        """
        feasts = self.date.all_evening if self.office.name == "evening_prayer" else self.date.all
        names = [feast.saint_name for feast in feasts if hasattr(feast, "saint_name") and feast.saint_name]
        names = ["the Blessed Virgin Mary"] + names
        return ", ".join(names)

    def get_leaders(self) -> SafeString:
        """
        Generate national leader names with regional variations.
        
        Includes spans for US/Canada/generic national leaders to allow
        client-side filtering based on user location.
        
        Returns:
            SafeString: HTML spans with country-specific leader names
        """
        parts = [
            '<span class="us">your servant Donald Trump, the President, </span>',
            '<span class="canada">your servants His Majesty King Charles, the Sovereign, and Mark Carney, the Prime Minister, </span>'
            '<span class="national_none">your servants, our national leaders, </span>',
        ]
        return mark_safe("".join(parts))

    def get_weekday_class(self) -> str:
        """
        Generate CSS class for Great Litany placement based on weekday.
        
        Great Litany is appointed for Wednesdays, Fridays, and Sundays.
        
        Returns:
            str: CSS class name for styling/visibility control
        """
        if self.office.office == "evening_prayer":
            start = "litany-ep-"
        else:
            start = "litany-mp-"
        if self.date.date.weekday() in (2, 4, 6):
            return start + "wfs"
        return start + "not-wfs"

    @cached_property
    def data(self) -> Dict[str, Any]:
        """
        Generate Great Litany section data.
        
        Returns:
            dict: Saint names, national leaders, weekday CSS class
        """
        return {"names": self.get_names(), "leaders": self.get_leaders(), "weekday_class": self.get_weekday_class()}
