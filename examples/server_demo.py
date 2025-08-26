#!/usr/bin/env python3
"""Demo script for the DeepL HTTP translation server."""

import json
import urllib.request
import urllib.parse
import time


def demo_translation_server():
    """Demonstrate the translation server functionality."""
    base_url = "http://127.0.0.1:3001/api/translate"
    
    print("🌐 DeepL HTTP Translation Server Demo")
    print("=" * 50)
    print("Make sure the server is running with: deepl --server")
    print()
    
    # Test cases
    test_cases = [
        {
            "name": "English to Russian",
            "params": {
                "engine": "deepl",
                "from": "en", 
                "to": "ru",
                "text": "Hello world"
            }
        },
        {
            "name": "English to Japanese",
            "params": {
                "engine": "deepl",
                "from": "en",
                "to": "ja", 
                "text": "hello"
            }
        },
        {
            "name": "Original example from requirements",
            "params": {
                "engine": "google",  # Will use deepl anyway
                "from": "en",
                "to": "ru",
                "text": "some text for translate"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔄 Test {i}: {test_case['name']}")
        
        # Build URL with query parameters
        params = urllib.parse.urlencode(test_case['params'])
        url = f"{base_url}?{params}"
        
        print(f"   URL: {url}")
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"   ✅ Status: {response.status}")
                    print(f"   📝 Response:")
                    print(json.dumps(data, indent=6, ensure_ascii=False))
                else:
                    print(f"   ❌ Status: {response.status}")
                    
        except urllib.error.HTTPError as e:
            print(f"   ❌ HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        
        # Small delay between requests
        if i < len(test_cases):
            time.sleep(1)
    
    print("✨ Demo completed!")
    print("\nAPI Format:")
    print("GET /api/translate?engine=<engine>&from=<lang>&to=<lang>&text=<text>")
    print("\nResponse Format:")
    print(json.dumps({
        "engine": "deepl",
        "detected": "",
        "translated-text": "translated text here",
        "source_language": "en", 
        "target_language": "ru"
    }, indent=2))


if __name__ == "__main__":
    demo_translation_server()