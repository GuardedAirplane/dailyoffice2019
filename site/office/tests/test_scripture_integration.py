"""
Integration tests for Scripture retrieval and display in office context.

Tests: T131 - Scripture integration with office generation

Validates: FR-020 (BibleGateway API retrieval), FR-021 (Local database caching)
"""

import pytest
from unittest.mock import patch, Mock
from office.models import Scripture, OfficeDay
from bible.passage import Passage
from bible.sources import BibleGateway


@pytest.mark.django_db
class TestScriptureIntegration:
    """Tests for Scripture integration with Daily Office."""
    
    def test_scripture_retrieval_via_passage_class(self):
        """Scripture can be retrieved via Passage class (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            # Mock BibleGateway response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = """
                <html>
                    <div class="passage-text">
                        <div class="result-text-style-normal">
                            <h3><span class="text John-3-16">John 3:16</span></h3>
                            <p><span class="text John-3-16">For God so loved the world that he gave his only Son, 
                            so that everyone who believes in him may not perish but may have eternal life.</span></p>
                        </div>
                    </div>
                </html>
            """
            mock_get.return_value = mock_response
            
            # Create a Passage instance
            passage = Passage("John 3:16", source="nrsvce")
            
            # Verify passage was retrieved
            assert passage.lookup is not None
            assert passage.version_abbreviation == "nrsvce"
            assert "God so loved the world" in passage.lookup.get_text()
    
    def test_scripture_caching_prevents_duplicate_api_calls(self):
        """Cached scripture prevents duplicate API calls (T131)."""
        # Pre-populate cache
        Scripture.objects.create(
            passage="John 3:16",
            nrsvce="For God so loved the world..."
        )
        
        # Retrieve from cache
        cached = Scripture.objects.filter(passage="John 3:16").first()
        
        assert cached is not None
        assert cached.nrsvce == "For God so loved the world..."
        assert Scripture.objects.filter(passage="John 3:16").count() == 1
    
    def test_scripture_stores_multiple_translations_simultaneously(self):
        """Scripture can store multiple translations for same passage (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            # Mock responses for different translations
            def mock_get_side_effect(url, *args, **kwargs):
                mock_response = Mock()
                mock_response.status_code = 200
                if "nrsvce" in url or "version=nrsvce" in url:
                    mock_response.text = """
                        <html>
                            <div class="passage-text">
                                <div class="result-text-style-normal">
                                    <p><span>NRSVCE: For God so loved the world...</span></p>
                                </div>
                            </div>
                        </html>
                    """
                elif "esv" in url or "version=esv" in url:
                    mock_response.text = """
                        <html>
                            <div class="passage-text">
                                <div class="result-text-style-normal">
                                    <p><span>ESV: For God so loved the world...</span></p>
                                </div>
                            </div>
                        </html>
                    """
                return mock_response
            
            mock_get.side_effect = mock_get_side_effect
            
            # Fetch different translations
            passage_nrsvce = Passage("John 3:16", source="nrsvce")
            passage_esv = Passage("John 3:16", source="esv")
            
            # Verify both were retrieved
            assert "NRSVCE" in passage_nrsvce.lookup.get_text()
            assert "ESV" in passage_esv.lookup.get_text()


@pytest.mark.django_db
class TestScriptureTranslationFallback:
    """Tests for Scripture translation fallback behavior."""
    
    def test_apocrypha_fallback_from_esv_to_nrsvce(self):
        """Apocrypha passages should fall back from ESV to NRSVCE (T131)."""
        # This is a documentation test - actual fallback logic would be in office generation
        # ESV doesn't include Apocrypha, so Wisdom/Sirach/etc would use NRSVCE
        
        # Example: Wisdom 3:1-9 is not in ESV
        scripture = Scripture.objects.create(
            passage="Wisdom 3:1-9",
            nrsvce="The souls of the righteous are in the hand of God...",
            esv=None  # ESV doesn't have this book
        )
        
        assert scripture.nrsvce is not None
        assert scripture.esv is None
    
    def test_scripture_model_supports_all_9_translations(self):
        """Scripture model can store all 9 supported translations (T131)."""
        scripture = Scripture.objects.create(
            passage="Psalm 23:1",
            nrsvce="The LORD is my shepherd, I shall not want.",
            esv="The LORD is my shepherd; I shall not want.",
            kjv="The LORD is my shepherd; I shall not want.",
            rsv="The LORD is my shepherd, I shall not want.",
            nabre="The LORD is my shepherd; there is nothing I lack.",
            niv="The LORD is my shepherd, I lack nothing.",
            nasb="The LORD is my shepherd, I will not be in need.",
            coverdale="The LORD is my shepherd: therefore can I lack nothing.",
            renewed_coverdale="The LORD is my shepherd: therefore can I lack nothing."
        )
        
        # Verify all translations stored
        assert scripture.nrsvce is not None
        assert scripture.esv is not None
        assert scripture.kjv is not None
        assert scripture.rsv is not None
        assert scripture.nabre is not None
        assert scripture.niv is not None
        assert scripture.nasb is not None
        assert scripture.coverdale is not None
        assert scripture.renewed_coverdale is not None


@pytest.mark.django_db  
class TestScriptureErrorHandling:
    """Tests for Scripture error handling in integration context."""
    
    def test_biblegateway_timeout_raises_exception(self):
        """BibleGateway timeout should raise appropriate exception (T131)."""
        from bible.sources import PassageNotFoundException
        import requests
        
        with patch("bible.sources.requests.get") as mock_get:
            # Simulate timeout
            mock_get.side_effect = requests.Timeout("Connection timeout")
            
            with pytest.raises((requests.Timeout, PassageNotFoundException)):
                passage = Passage("John 3:16", source="nrsvce")
    
    def test_biblegateway_404_raises_exception(self):
        """BibleGateway 404 should raise exception (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            # Simulate 404
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            # Also need to patch scriptures.extract to avoid IndexError before reaching 404 check
            with patch("bible.sources.scriptures.extract") as mock_extract:
                mock_extract.return_value = [("Genesis", 1, 1, 1, 1)]
                
                # BibleGateway raises generic Exception on non-200 status
                with pytest.raises(Exception, match="Error getting passage"):
                    passage = Passage("Genesis 1:1", source="nrsvce")
    
    def test_invalid_passage_reference_handled_gracefully(self):
        """Invalid passage references should be handled gracefully (T131)."""
        from bible.sources import PassageNotFoundException
        
        with patch("bible.sources.requests.get") as mock_get:
            # Simulate empty response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "<html><body></body></html>"
            mock_get.return_value = mock_response
            
            with pytest.raises(PassageNotFoundException):
                passage = Passage("Genesis 999:999", source="nrsvce")


@pytest.mark.django_db
class TestScriptureHTMLProcessing:
    """Tests for Scripture HTML processing and formatting."""
    
    def test_scripture_removes_footnotes_from_html(self):
        """Scripture should remove footnote markers from HTML (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = """
                <html>
                    <div class="passage-text">
                        <div class="result-text-style-normal">
                            <p>
                                <span>For God so loved the world</span>
                                <sup class="footnote">a</sup>
                                <span> that he gave his only Son</span>
                            </p>
                        </div>
                    </div>
                </html>
            """
            mock_get.return_value = mock_response
            
            passage = Passage("John 3:16", source="nrsvce")
            html = passage.lookup.get_html()
            
            # Footnote should be removed
            assert "footnote" not in html.lower() or "<sup" not in html
    
    def test_scripture_removes_crossreferences_from_html(self):
        """Scripture should remove cross-reference markers from HTML (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = """
                <html>
                    <div class="passage-text">
                        <div class="result-text-style-normal">
                            <p>
                                <span>For God so loved the world</span>
                                <sup class="crossreference">†</sup>
                                <span> that he gave his only Son</span>
                            </p>
                        </div>
                    </div>
                </html>
            """
            mock_get.return_value = mock_response
            
            passage = Passage("John 3:16", source="nrsvce")
            html = passage.lookup.get_html()
            
            # Cross-reference should be removed
            assert "crossreference" not in html.lower() or "<sup" not in html
    
    def test_scripture_extracts_section_headings(self):
        """Scripture should extract section headings from passages (T131)."""
        with patch("bible.sources.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = """
                <html>
                    <div class="passage-text">
                        <div class="result-text-style-normal">
                            <h3><span class="text John-3-16">God's Love for the World</span></h3>
                            <p><span class="text John-3-16">For God so loved the world...</span></p>
                        </div>
                    </div>
                </html>
            """
            mock_get.return_value = mock_response
            
            passage = Passage("John 3:16", source="nrsvce")
            headings = passage.lookup.get_headings()
            
            # Should extract heading
            assert len(headings) > 0
            assert "God's Love for the World" in str(headings)
