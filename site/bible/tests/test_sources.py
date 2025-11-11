"""
Unit tests for bible.sources module.

Tests: T123-T126 - BibleGateway adapter behavior

Validates: FR-020 (Bible Gateway API retrieval), FR-022 (API unavailability handling)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from bible.sources import BibleGateway, PassageNotFoundException, OremusBibleBrowser, BCPPsalter


class TestBibleGatewaySuccess:
    """Tests for BibleGateway adapter successful retrieval.
    
    Validates: FR-020 (Bible Gateway API retrieval)
    """
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_successful_request(self, mock_get):
        """BibleGateway should successfully retrieve passage on 200 response."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        assert adapter.passage == "John 3:16"
        assert adapter.version == "esv"
        assert mock_get.called
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_constructs_correct_url(self, mock_get):
        """BibleGateway should construct correct API URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        # Provide realistic markup with all required elements
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <h3><span class="text John-3-16">Section Heading</span></h3>
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        # Verify URL was constructed correctly
        call_args = mock_get.call_args[0][0]
        assert "biblegateway.com/passage/" in call_args
        assert "search=John 3:16" in call_args or "search=John%203:16" in call_args
        assert "version=esv" in call_args
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_kjv_converts_to_akjv(self, mock_get):
        """BibleGateway should convert KJV to AKJV version code."""
        mock_response = Mock()
        mock_response.status_code = 200
        # Provide realistic markup with all required elements
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <h3><span class="text John-3-16">Section Heading</span></h3>
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "kjv")
        
        assert adapter.version == "akjv"
        call_args = mock_get.call_args[0][0]
        assert "version=akjv" in call_args
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_removes_crossreferences(self, mock_get):
        """BibleGateway should remove crossreference footnotes."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God<sup class="crossreference">a</sup> so loved...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        # Crossreferences should be removed from HTML
        assert '<sup class="crossreference">' not in adapter.html
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_removes_footnotes(self, mock_get):
        """BibleGateway should remove footnote markers."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God<sup class="footnote">b</sup> so loved...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        # Footnotes should be removed from HTML
        assert '<sup class="footnote">' not in adapter.html


class TestBibleGatewayTimeout:
    """Tests for BibleGateway adapter timeout handling.
    
    Validates: FR-022 (API unavailability handling)
    """
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_timeout_raises_exception(self, mock_get):
        """BibleGateway should raise exception on timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(requests.exceptions.Timeout):
            BibleGateway("John 3:16", "esv")
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_connection_error_raises_exception(self, mock_get):
        """BibleGateway should raise exception on connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(requests.exceptions.ConnectionError):
            BibleGateway("John 3:16", "esv")


class TestBibleGatewayRateLimit:
    """Tests for BibleGateway adapter rate limit handling.
    
    Validates: FR-022 (API unavailability handling)
    """
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_rate_limit_429_raises_exception(self, mock_get):
        """BibleGateway should raise exception on 429 rate limit response."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match="Error getting passage"):
            BibleGateway("John 3:16", "esv")
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_server_error_500_raises_exception(self, mock_get):
        """BibleGateway should raise exception on 500 server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match="Error getting passage"):
            BibleGateway("John 3:16", "esv")


class TestBibleGateway404Error:
    """Tests for BibleGateway adapter 404 not found handling.
    
    Validates: FR-022 (API unavailability handling)
    """
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_404_raises_exception(self, mock_get):
        """BibleGateway should raise exception on 404 not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match="Error getting passage"):
            BibleGateway("John 3:16", "esv")
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_invalid_passage_raises_exception(self, mock_get):
        """BibleGateway should raise PassageNotFoundException for invalid markup."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Passage not found</body></html>'
        mock_get.return_value = mock_response
        
        with pytest.raises(PassageNotFoundException):
            BibleGateway("John 3:16", "esv")


class TestBibleGatewayTextProcessing:
    """Tests for BibleGateway text processing and formatting."""
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_has_text_method(self, mock_get):
        """BibleGateway should have get_text method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        assert hasattr(adapter, 'get_text')
        assert callable(adapter.get_text)
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_has_html_method(self, mock_get):
        """BibleGateway should have get_html method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        assert hasattr(adapter, 'get_html')
        assert callable(adapter.get_html)
    
    @patch('bible.sources.requests.get')
    def test_biblegateway_has_headings_method(self, mock_get):
        """BibleGateway should have get_headings method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="passage-text">
                <div class="result-text-style-normal">
                    <p><span class="text John-3-16">For God so loved the world...</span></p>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        adapter = BibleGateway("John 3:16", "esv")
        
        assert hasattr(adapter, 'get_headings')
        assert callable(adapter.get_headings)


class TestOremusBibleBrowser:
    """Tests for OremusBibleBrowser adapter."""
    
    @patch('bible.sources.requests.get')
    def test_oremus_successful_request(self, mock_get):
        """OremusBibleBrowser should successfully retrieve passage."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><div class="bibletext"><p>For God so loved...</p></div></html>'
        mock_get.return_value = mock_response
        
        adapter = OremusBibleBrowser("John 3:16", "av")
        
        assert adapter.version == "av"
        assert adapter.passage == "John 3:16"
    
    @patch('bible.sources.requests.get')
    def test_oremus_constructs_correct_url(self, mock_get):
        """OremusBibleBrowser should construct correct oremus.org URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        # Provide markup with required bibletext div
        mock_response.text = '<html><div class="bibletext"><p>For God so loved...</p></div></html>'
        mock_get.return_value = mock_response
        
        adapter = OremusBibleBrowser("John 3:16", "av")
        
        call_args = mock_get.call_args[0][0]
        assert "bible.oremus.org" in call_args
        assert "version=av" in call_args


class TestBCPPsalter:
    """Tests for BCPPsalter adapter."""
    
    def test_bcp_psalter_instantiates(self):
        """BCPPsalter should instantiate for psalm passages."""
        adapter = BCPPsalter("Psalm 23", "coverdale")
        
        assert adapter.version == "coverdale"
        assert adapter.passage == "Psalm 23"
    
    def test_bcp_psalter_has_required_methods(self):
        """BCPPsalter should have get_html and get_text methods."""
        adapter = BCPPsalter("Psalm 23", "renewed_coverdale")
        
        assert hasattr(adapter, 'get_html')
        assert hasattr(adapter, 'get_text')
        assert callable(adapter.get_html)
        assert callable(adapter.get_text)
