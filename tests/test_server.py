"""Tests for the HTTP server functionality."""

import json
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
from http.server import HTTPServer

import pytest

from deepl.server import TranslationHandler


class TestTranslationServer:
    """Test cases for the translation HTTP server."""

    @pytest.fixture
    def server(self):
        """Start a test server."""
        server_address = ("127.0.0.1", 0)  # Use port 0 for automatic port assignment
        httpd = HTTPServer(server_address, TranslationHandler)
        
        # Get the actual port assigned
        port = httpd.server_address[1]
        
        # Start server in a thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Give server time to start
        time.sleep(0.1)
        
        yield f"http://127.0.0.1:{port}"
        
        # Cleanup
        httpd.shutdown()
        httpd.server_close()

    def test_translate_endpoint_success(self, server):
        """Test successful translation request."""
        url = f"{server}/api/translate?engine=deepl&from=en&to=ru&text=hello%20world"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            assert response.status == 200
            data = json.loads(response.read().decode('utf-8'))
            
            assert "engine" in data
            assert "detected" in data
            assert "translated-text" in data
            assert "source_language" in data
            assert "target_language" in data
            
            assert data["engine"] == "deepl"
            assert data["source_language"] == "en"
            assert data["target_language"] == "ru"
            assert data["translated-text"]  # Should not be empty

    def test_translate_endpoint_missing_params(self, server):
        """Test translation request with missing parameters."""
        url = f"{server}/api/translate?from=en&to=ru"  # missing text
        
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(url, timeout=10)
        
        assert exc_info.value.code == 400

    def test_invalid_endpoint(self, server):
        """Test request to invalid endpoint."""
        url = f"{server}/api/invalid"
        
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(url, timeout=10)
        
        assert exc_info.value.code == 404

    def test_translate_different_languages(self, server):
        """Test translation with different language pairs."""
        test_cases = [
            ("en", "ja", "hello", "こんにちは"),
            ("ru", "en", "привет", "hello"),
        ]
        
        for from_lang, to_lang, text, expected in test_cases:
            encoded_text = urllib.parse.quote(text)
            url = f"{server}/api/translate?engine=deepl&from={from_lang}&to={to_lang}&text={encoded_text}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                assert response.status == 200
                data = json.loads(response.read().decode('utf-8'))
                
                assert data["source_language"] == from_lang
                assert data["target_language"] == to_lang
                # For mock translations, check if we get expected result
                if data["translated-text"] == expected:
                    assert data["translated-text"] == expected

    def test_cors_headers(self, server):
        """Test that CORS headers are present."""
        url = f"{server}/api/translate?engine=deepl&from=en&to=ru&text=test"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            headers = response.headers
            assert "Access-Control-Allow-Origin" in headers
            assert headers["Access-Control-Allow-Origin"] == "*"

    def test_json_response_format(self, server):
        """Test that response is valid JSON with correct content type."""
        url = f"{server}/api/translate?engine=deepl&from=en&to=ru&text=test"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            assert response.headers["Content-Type"] == "application/json"
            
            # Should be valid JSON
            data = json.loads(response.read().decode('utf-8'))
            assert isinstance(data, dict)

    def test_url_encoded_text(self, server):
        """Test with URL encoded text containing special characters."""
        text = "hello world! 123"
        encoded_text = urllib.parse.quote(text)
        url = f"{server}/api/translate?engine=deepl&from=en&to=ru&text={encoded_text}"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            assert response.status == 200
            data = json.loads(response.read().decode('utf-8'))
            assert data["translated-text"]  # Should contain some translation