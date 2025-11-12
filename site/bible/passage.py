from bible.sources import BibleGateway, OremusBibleBrowser, BCPPsalter


class BibleVersions(object):
    """
    Registry of supported Bible translations and their adapters.

    Validates: FR-016 (Support Multiple Bible Translations)

    Provides access to 10 Bible versions:
    - NRSVCE, ESV, RSV, KJV, NABRE, NIV, NASB (via Bible Gateway)
    - AV (via Oremus Bible Browser)
    - Coverdale and Renewed Coverdale Psalters (via BCP Psalter)
    """

    VERSIONS = {
        "nrsvce": {"name": "New Revised Standard Version", "adapter": BibleGateway},
        "esv": {"name": "English Standard Version", "adapter": BibleGateway},
        "rsv": {"name": "Revised Standard Version", "adapter": BibleGateway},
        "kjv": {"name": "King James Version", "adapter": BibleGateway},
        "nabre": {"name": "New American Bible - Revised Edition", "adapter": BibleGateway},
        "niv": {"name": "New International Version", "adapter": BibleGateway},
        "nasb": {"name": "New American Standard Bible", "adapter": BibleGateway},
        "av": {"name": "King James Version", "adapter": OremusBibleBrowser},
        "coverdale": {"name": "Coverdale Psalter (1928)", "adapter": BCPPsalter},
        "renewed_coverdale": {"name": "Renewed Coverdale Psalter (2019)", "adapter": BCPPsalter},
    }


class Passage(object):
    """
    Represents a Bible passage in a specific translation.

    Validates: FR-016 (Support Multiple Bible Translations)
    Validates: FR-020 (Retrieve Scripture from Bible Gateway API)

    Fetches scripture text from external sources (Bible Gateway, Oremus)
    and provides access to formatted text, HTML, and headings.

    Args:
        passage (str): Scripture reference (e.g., "John 3:16", "Genesis 1:1-5")
        source (str): Bible version abbreviation (default: "nrsv")

    Attributes:
        lookup: Adapter instance for fetching scripture
        version_abbreviation (str): Version code (e.g., "esv")
        version_name (str): Full version name (e.g., "English Standard Version")
    """

    def __init__(self, passage, source="nrsv"):
        source = source.lower()
        version = BibleVersions.VERSIONS.get(source, {"name": source, "adapter": BibleGateway})
        adapter = version["adapter"]
        self.lookup = adapter(passage, source)
        self.version_abbreviation = source
        self.version_name = version["name"]

    @property
    def text(self):
        """
        Retrieve plain text of the scripture passage.

        Returns:
            str: Scripture text without formatting
        """
        return self.lookup.get_text()

    @property
    def html(self):
        """
        Retrieve HTML-formatted scripture passage.

        Returns:
            str: Scripture text with HTML markup (paragraphs, verse numbers, etc.)
        """
        return self.lookup.get_html()

    @property
    def headings(self):
        """
        Retrieve section headings within the passage.

        Returns:
            list: Section headings (if available from source)
        """
        return self.lookup.get_headings()
