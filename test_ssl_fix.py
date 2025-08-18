#!/usr/bin/env python3
"""
Test SSL fix for the electricity meter website
"""

import os
import sys
import ssl
import requests
from urllib3.packages.urllib3.exceptions import InsecureRequestWarning

def test_ssl_fix():
    print("🔍 TESTING SSL CERTIFICATE FIX")
    print("=" * 40)
    
    website_url = "https://prepaid.desco.org.bd"
    
    print("1. Testing normal connection (should fail)...")
    try:
        response = requests.get(website_url, timeout=10)
        print(f"✅ Normal connection worked: {response.status_code}")
    except Exception as e:
        print(f"❌ Normal connection failed: {e}")
    
    print("\n2. Testing with SSL verification disabled...")
    try:
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        response = requests.get(website_url, verify=False, timeout=10)
        print(f"✅ SSL bypass worked: {response.status_code}")
        print(f"✅ Website is reachable with SSL bypass")
        return True
    except Exception as e:
        print(f"❌ SSL bypass failed: {e}")
        return False

def test_selenium_ssl_fix():
    print("\n3. Testing Selenium with SSL fix...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # Add SSL bypass arguments
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        print("Creating Chrome driver with SSL bypass...")
        driver = webdriver.Chrome(options=options)
        
        print("Testing navigation to Google first...")
        driver.get("https://www.google.com")
        print(f"✅ Google works: {driver.title}")
        
        print("Testing navigation to electricity website...")
        driver.get("https://prepaid.desco.org.bd/customer/#/customer-login")
        print(f"✅ Electricity website works: {driver.title}")
        
        driver.quit()
        print("✅ Selenium SSL bypass successful!")
        return True
        
    except Exception as e:
        print(f"❌ Selenium SSL test failed: {e}")
        return False

if __name__ == "__main__":
    if test_ssl_fix():
        print("\n🎯 SOLUTION FOUND!")
        print("The issue is SSL certificate verification.")
        print("We need to add SSL bypass options to the scraper.")
    else:
        print("\n❌ SSL bypass didn't work either.")
        print("There may be other network issues.")
    
    test_selenium_ssl_fix()