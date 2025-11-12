from datetime import date

from django.utils import timezone

import arrow
from delorean import Delorean


def weekday_after(weekday, month, day, year=None, number_after=1):
    if not year:
        year = arrow.utcnow().format("YYYY")

    weekday = weekday.lower()
    direction = "last" if number_after < 1 else "next"
    number_after = abs(number_after)
    d = Delorean(datetime=timezone.datetime(year, month, day), timezone="UTC")
    return d._shift_date(direction, weekday, number_after).date


def easter(year):
    """
    Calculate the date of Easter Sunday for a given year using the Meeus/Jones/Butcher algorithm.
    
    This implements the anonymous Gregorian algorithm published by Jean Meeus (1991),
    refined by John Conway and extended by Spencer Jones. It accurately computes Easter
    for all Gregorian calendar years (1583 onwards).
    
    **Algorithm Explanation:**
    
    Easter is defined as the first Sunday after the first full moon occurring on or after
    the vernal equinox (March 21). This ecclesiastical calculation uses a 19-year Metonic
    cycle and incorporates the Gregorian calendar reform.
    
    **Step-by-Step Calculation:**
    
    1. **Golden Number (a)**: `year % 19`
       - Position in the 19-year Metonic cycle
       - Synchronizes lunar and solar calendars
    
    2. **Century Index (b, c)**: `year // 100`, `year % 100`
       - b: Century number
       - c: Year within century
    
    3. **Lunar Correction (d)**:
       ```
       d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
       ```
       - Accounts for Gregorian calendar leap year exceptions
       - Adjusts for lunar orbit drift (epact correction)
       - The `((b - (b + 8) // 25 + 1) // 3)` term corrects for the moon's orbit
       - Result is the "epact" - age of the moon on January 1
    
    4. **Solar Correction (e)**:
       ```
       e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
       ```
       - Determines the day of the week
       - Accounts for leap years in the Gregorian calendar
       - Result is the number of days from a Sunday to the full moon
    
    5. **Easter Month Calculation (f)**:
       ```
       f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
       ```
       - Combines lunar and solar corrections
       - The `7 * ((a + 11 * d + 22 * e) // 451)` ensures Easter is after March 21
       - Adds 114 to shift into valid month range
    
    6. **Final Date Extraction**:
       ```
       month = f // 31        # 3 = March, 4 = April
       day = f % 31 + 1       # Day of month
       ```
    
    **Historical Context:**
    
    The algorithm was designed to match the tables established by the Council of Nicaea (325 AD)
    and updated for the Gregorian calendar reform (1582). It handles edge cases including:
    - Years divisible by 100 but not 400 (e.g., 1900, 2100)
    - The golden number cycle repeating every 19 years
    - Easter date range: March 22 to April 25
    
    **Accuracy:**
    
    This algorithm is accurate for all years in the Gregorian calendar (1583-∞).
    It matches the official computus tables used by the Catholic Church and
    Anglican Communion.
    
    Args:
        year (int): Gregorian calendar year (1583 or later)
    
    Returns:
        date: Easter Sunday date for the given year
    
    Examples:
        >>> easter(2025)
        datetime.date(2025, 4, 20)
        
        >>> easter(2000)  # Leap year divisible by 400
        datetime.date(2000, 4, 23)
        
        >>> easter(1900)  # Not a leap year (divisible by 100 but not 400)
        datetime.date(1900, 4, 15)
    
    References:
        - Meeus, Jean (1991). "Astronomical Algorithms". Willmann-Bell.
        - Butcher, Samuel (1876). "The Ecclesiastical Calendar".
        - Explanatory Supplement to the Astronomical Almanac (1992).
    
    See Also:
        - https://en.wikipedia.org/wiki/Computus
        - https://www.tondering.dk/claus/cal/easter.php
    """
    # Golden Number: position in 19-year Metonic cycle
    a = year % 19
    
    # Century index and year within century
    b = year // 100
    c = year % 100
    
    # Lunar correction (epact): age of moon on Jan 1
    # Accounts for Gregorian leap year rules and lunar orbit drift
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    
    # Solar correction: day of week adjustment
    # Accounts for Gregorian leap years
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    
    # Easter month calculation
    # Ensures Easter falls after March 21 (vernal equinox)
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    
    # Extract month (3=March, 4=April) and day
    month = f // 31
    day = f % 31 + 1
    
    return date(year, month, day)


def advent(year):
    """
    Calculate the First Sunday of Advent for a given year.
    
    Advent begins on the fourth Sunday before Christmas Day (December 25).
    This marks the start of the liturgical year in Western Christianity.
    
    Validates: FR-014 (Calculate Correct Liturgical Season)
    
    Args:
        year (int): Calendar year
    
    Returns:
        date: First Sunday of Advent (between Nov 27 and Dec 3)
    
    Examples:
        >>> advent(2025)
        datetime.date(2025, 11, 30)  # Fourth Sunday before Dec 25, 2025
        
        >>> advent(2024)
        datetime.date(2024, 12, 1)
    """
    return weekday_after(weekday="sunday", month=12, day=25, year=year, number_after=-4)


week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
