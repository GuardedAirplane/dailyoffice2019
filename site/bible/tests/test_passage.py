"""
Unit tests for bible.passage module.

Tests: T130 - Passage.lookup supports all 9 translations

Validates: FR-016 (Multiple Bible Translations)
"""

import pytest
from unittest.mock import patch, Mock
from bible.passage import Passage, BibleVersions


class TestBibleVersions:
    """Tests for BibleVersions configuration.
    
    Validates: FR-016 (Multiple Bible Translations)
    """
    
    def test_bible_versions_contains_all_translations(self):
        """All 9 Bible translations should be defined."""
        expected_versions = [
            'nrsvce', 'esv', 'rsv', 'kjv', 'nabre', 
            'niv', 'nasb', 'av', 'coverdale', 'renewed_coverdale'
        ]
        
        for version in expected_versions:
            assert version in BibleVersions.VERSIONS, \
                f"Version {version} should be in VERSIONS"
    
    def test_bible_versions_have_name_and_adapter(self):
        """Each Bible version should have name and adapter."""
        for version_key, version_config in BibleVersions.VERSIONS.items():
            assert 'name' in version_config, \
                f"Version {version_key} should have 'name'"
            assert 'adapter' in version_config, \
                f"Version {version_key} should have 'adapter'"
            assert version_config['name'], \
                f"Version {version_key} name should not be empty"
            assert version_config['adapter'], \
                f"Version {version_key} adapter should not be None"
    
    def test_nrsvce_configuration(self):
        """NRSVCE should be properly configured."""
        nrsvce = BibleVersions.VERSIONS['nrsvce']
        assert nrsvce['name'] == 'New Revised Standard Version'
        assert nrsvce['adapter'].__name__ == 'BibleGateway'
    
    def test_esv_configuration(self):
        """ESV should be properly configured."""
        esv = BibleVersions.VERSIONS['esv']
        assert esv['name'] == 'English Standard Version'
        assert esv['adapter'].__name__ == 'BibleGateway'
    
    def test_kjv_configuration(self):
        """KJV should be properly configured."""
        kjv = BibleVersions.VERSIONS['kjv']
        assert kjv['name'] == 'King James Version'
        assert kjv['adapter'].__name__ == 'BibleGateway'
    
    def test_coverdale_psalter_configuration(self):
        """Coverdale Psalter should use BCPPsalter adapter."""
        coverdale = BibleVersions.VERSIONS['coverdale']
        assert coverdale['name'] == 'Coverdale Psalter (1928)'
        assert coverdale['adapter'].__name__ == 'BCPPsalter'


class TestPassageInstantiation:
    """Tests for Passage class instantiation.
    
    Validates: FR-016 (Multiple Bible Translations)
    """
    
    def test_passage_instantiates_with_defaults(self):
        """Passage should instantiate with default NRSV version."""
        passage = Passage("John 3:16")
        assert passage.version_abbreviation == "nrsv"
        # Default uses lowercase source as version name when not found in VERSIONS
        assert passage.version_name is not None
    
    def test_passage_accepts_nrsvce_version(self):
        """Passage should accept NRSVCE version."""
        passage = Passage("John 3:16", source="nrsvce")
        assert passage.version_abbreviation == "nrsvce"
        assert passage.version_name == "New Revised Standard Version"
    
    def test_passage_accepts_esv_version(self):
        """Passage should accept ESV version."""
        passage = Passage("John 3:16", source="esv")
        assert passage.version_abbreviation == "esv"
        assert passage.version_name == "English Standard Version"
    
    def test_passage_accepts_kjv_version(self):
        """Passage should accept KJV version."""
        passage = Passage("John 3:16", source="kjv")
        assert passage.version_abbreviation == "kjv"
        assert passage.version_name == "King James Version"
    
    def test_passage_accepts_nabre_version(self):
        """Passage should accept NABRE version."""
        passage = Passage("John 3:16", source="nabre")
        assert passage.version_abbreviation == "nabre"
        assert passage.version_name == "New American Bible - Revised Edition"
    
    def test_passage_accepts_niv_version(self):
        """Passage should accept NIV version."""
        passage = Passage("John 3:16", source="niv")
        assert passage.version_abbreviation == "niv"
        assert passage.version_name == "New International Version"
    
    def test_passage_accepts_nasb_version(self):
        """Passage should accept NASB version."""
        passage = Passage("John 3:16", source="nasb")
        assert passage.version_abbreviation == "nasb"
        assert passage.version_name == "New American Standard Bible"
    
    def test_passage_accepts_rsv_version(self):
        """Passage should accept RSV version."""
        passage = Passage("John 3:16", source="rsv")
        assert passage.version_abbreviation == "rsv"
        assert passage.version_name == "Revised Standard Version"
    
    def test_passage_accepts_av_version(self):
        """Passage should accept AV version with OremusBibleBrowser."""
        passage = Passage("John 3:16", source="av")
        assert passage.version_abbreviation == "av"
        assert passage.version_name == "King James Version"
    
    def test_passage_accepts_coverdale_version(self):
        """Passage should accept Coverdale Psalter version."""
        passage = Passage("Psalm 23", source="coverdale")
        assert passage.version_abbreviation == "coverdale"
        assert passage.version_name == "Coverdale Psalter (1928)"
    
    def test_passage_accepts_renewed_coverdale_version(self):
        """Passage should accept Renewed Coverdale Psalter version."""
        passage = Passage("Psalm 23", source="renewed_coverdale")
        assert passage.version_abbreviation == "renewed_coverdale"
        assert passage.version_name == "Renewed Coverdale Psalter (2019)"
    
    def test_passage_source_case_insensitive(self):
        """Passage source parameter should be case-insensitive."""
        passage_lower = Passage("John 3:16", source="esv")
        passage_upper = Passage("John 3:16", source="ESV")
        passage_mixed = Passage("John 3:16", source="Esv")
        
        assert passage_lower.version_abbreviation == "esv"
        assert passage_upper.version_abbreviation == "esv"
        assert passage_mixed.version_abbreviation == "esv"
    
    def test_passage_fallback_for_unknown_version(self):
        """Passage should fall back to BibleGateway for unknown versions."""
        # Unknown versions will use the source string as version name
        # This test validates the fallback mechanism exists
        with patch("bible.sources.requests.get") as mock_get:
            # Mock a successful response for unknown version
            mock_response = Mock()
            mock_response.status_code = 200
            # text property must return a string
            mock_response.text = """
                <html>
                    <div class="passage-text">
                        <div class="result-text-style-normal">
                            <h3><span class="text John-3-16">Section Heading</span></h3>
                            <p><span class="text John-3-16">For God so loved the world...</span></p>
                        </div>
                    </div>
                </html>
            """
            mock_get.return_value = mock_response
            
            passage = Passage("John 3:16", source="unknown")
            assert passage.version_abbreviation == "unknown"
            assert passage.version_name == "unknown"
            # Should still have a lookup adapter
            assert passage.lookup is not None


class TestPassageProperties:
    """Tests for Passage property methods."""
    
    def test_passage_has_text_property(self):
        """Passage should have text property."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'text')
    
    def test_passage_has_html_property(self):
        """Passage should have html property."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'html')
    
    def test_passage_has_headings_property(self):
        """Passage should have headings property."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'headings')
    
    def test_passage_has_lookup_attribute(self):
        """Passage should have lookup attribute."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'lookup')
    
    def test_passage_has_version_abbreviation(self):
        """Passage should have version_abbreviation attribute."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'version_abbreviation')
    
    def test_passage_has_version_name(self):
        """Passage should have version_name attribute."""
        passage = Passage("John 3:16", source="esv")
        assert hasattr(passage, 'version_name')
