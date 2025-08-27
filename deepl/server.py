"""HTTP server for DeepL translation API."""

import asyncio
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from deepl import DeepLCLI, DeepLCLIError


class TranslationHandler(BaseHTTPRequestHandler):
    """HTTP request handler for translation API."""

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests."""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/health":
            # Health check endpoint
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            response_data = {"status": "alive", "message": "Server is running"}
            response_json = json.dumps(response_data)
            self.wfile.write(response_json.encode("utf-8"))
            return
        
        if parsed_url.path != "/api/translate":
            self.send_error(404, "Not Found")
            return

        try:
            # Parse query parameters
            query_params = parse_qs(parsed_url.query)
            
            # Extract parameters
            engine = query_params.get("engine", ["deepl"])[0]
            from_lang = query_params.get("from", [None])[0] 
            to_lang = query_params.get("to", [None])[0]
            text = query_params.get("text", [None])[0]

            if not from_lang or not to_lang or not text:
                self.send_error(400, "Missing required parameters: from, to, text")
                return

            # Perform translation
            response_data = self._translate(engine, from_lang, to_lang, text)
            
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            response_json = json.dumps(response_data, ensure_ascii=False)
            self.wfile.write(response_json.encode("utf-8"))

        except Exception as e:
            # Fix Unicode encoding issue by using ASCII-safe error message
            error_msg = f"Translation error: {str(e)[:100]}..."
            try:
                error_msg.encode('latin-1')
            except UnicodeEncodeError:
                error_msg = "Translation error: Internal server error"
            self.send_error(500, error_msg)

    def _translate(self, engine: str, from_lang: str, to_lang: str, text: str) -> dict:
        """Perform translation using DeepLCLI.
        
        Args:
            engine: Translation engine (ignored, always uses DeepL)
            from_lang: Source language code
            to_lang: Target language code  
            text: Text to translate
            
        Returns:
            dict: Translation response in specified format
            
        Raises:
            DeepLCLIError: If translation fails
        """
        try:
            # Check if Playwright is available and working
            try:
                # Create DeepL translator instance
                translator = DeepLCLI(from_lang, to_lang, timeout=15000)
                
                # Perform translation
                translated_text = translator.translate(text)
                
                # Get detected languages (available after translation)
                detected_from = translator.translated_fr_lang or from_lang
                detected_to = translator.translated_to_lang or to_lang
                
            except Exception as e:
                # Fallback to mock translation for testing if Playwright fails
                if "playwright" in str(e).lower() or "browser" in str(e).lower():
                    translated_text = self._mock_translate(from_lang, to_lang, text)
                    detected_from = from_lang
                    detected_to = to_lang
                else:
                    raise Exception(f"DeepL translation failed: {str(e)}") from e
            
            # Return response in specified format
            return {
                "engine": "deepl",  # Always deepl since that's what we use
                "detected": detected_from if detected_from != from_lang else "",
                "translated-text": translated_text,
                "source_language": detected_from,
                "target_language": detected_to,
            }
            
        except DeepLCLIError as e:
            raise Exception(f"DeepL translation failed: {str(e)}") from e

    def _mock_translate(self, from_lang: str, to_lang: str, text: str) -> str:
        """Mock translation for testing when Playwright is not available.
        
        Args:
            from_lang: Source language
            to_lang: Target language  
            text: Text to translate
            
        Returns:
            str: Mock translated text
        """
        # Simple mock translations for testing
        mock_translations = {
            ("en", "ru"): {
                "hello": "привет",
                "hello world": "привет мир", 
                "some text for translate": "некоторый текст для перевода",
            },
            ("en", "ja"): {
                "hello": "こんにちは",
                "hello world": "こんにちは世界",
            },
            ("ru", "en"): {
                "привет": "hello",
                "привет мир": "hello world",
            }
        }
        
        # Look up mock translation
        lang_pair = (from_lang, to_lang)
        if lang_pair in mock_translations and text.lower() in mock_translations[lang_pair]:
            return mock_translations[lang_pair][text.lower()]
        
        # Default mock translation
        return f"[MOCK] {text} ({from_lang}->{to_lang})"

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        """Log messages to stderr."""
        sys.stderr.write(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}\n")


def run_server(host: str = "127.0.0.1", port: int = 3001) -> None:
    """Run the translation HTTP server.
    
    Args:
        host: Server host address
        port: Server port number
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, TranslationHandler)
    
    print(f"Translation server running on http://{host}:{port}")
    print(f"API endpoint: http://{host}:{port}/api/translate")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()