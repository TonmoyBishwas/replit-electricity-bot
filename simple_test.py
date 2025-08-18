#!/usr/bin/env python3
"""
Simple test to check what's hanging in Replit
"""

import os
import sys
from datetime import datetime

def test_basic_imports():
    print("=== Testing Basic Imports ===")
    try:
        import selenium
        print("✅ Selenium imported")
        
        import schedule
        print("✅ Schedule imported")
        
        import requests
        print("✅ Requests imported")
        
        from scraper import ElectricityMeterScraper
        print("✅ ElectricityMeterScraper imported")
        
        from telegram_bot import TelegramBot
        print("✅ TelegramBot imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_telegram():
    print("\n=== Testing Telegram ===")
    try:
        from telegram_bot import TelegramBot
        bot = TelegramBot()
        
        print("Sending test message...")
        success = bot.send_message("🧪 Simple test from Replit - " + datetime.now().strftime('%H:%M:%S'))
        
        if success:
            print("✅ Telegram working!")
            return True
        else:
            print("❌ Telegram failed")
            return False
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def test_chrome_basic():
    print("\n=== Testing Chrome (Basic) ===")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("Creating Chrome options...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        print("Attempting to create Chrome driver...")
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver created!")
        
        print("Testing navigation to Google...")
        driver.get("https://www.google.com")
        print(f"✅ Page loaded: {driver.title}")
        
        driver.quit()
        print("✅ Chrome test successful")
        return True
        
    except Exception as e:
        print(f"❌ Chrome error: {e}")
        return False

def test_scraper_creation():
    print("\n=== Testing Scraper Creation ===")
    try:
        from scraper import ElectricityMeterScraper
        
        print("Creating scraper...")
        scraper = ElectricityMeterScraper()
        
        print(f"✅ Scraper created with {len(scraper.all_meters)} meters")
        print(f"✅ Nicknames: {scraper.meter_nicknames}")
        
        return True
    except Exception as e:
        print(f"❌ Scraper creation error: {e}")
        return False

def test_website_access():
    print("\n=== Testing Website Access ===")
    try:
        import requests
        
        website_url = "https://prepaid.desco.org.bd/customer/#/customer-login"
        print(f"Testing basic connection to: {website_url}")
        
        # Just test if we can reach the domain
        response = requests.get("https://prepaid.desco.org.bd", timeout=10)
        print(f"✅ Website reachable - Status: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ Website access error: {e}")
        return False

def main():
    print("🔍 SIMPLE REPLIT TEST")
    print("=" * 40)
    
    # Test each component step by step
    if not test_basic_imports():
        print("❌ Basic imports failed - stopping")
        return
    
    if not test_telegram():
        print("⚠️ Telegram failed but continuing...")
    
    if not test_scraper_creation():
        print("❌ Scraper creation failed - stopping")
        return
    
    if not test_website_access():
        print("⚠️ Website access failed but continuing...")
    
    print("\n" + "=" * 40)
    print("🧪 Now testing Chrome - this is likely where it hangs...")
    
    if test_chrome_basic():
        print("✅ Chrome works! The issue is elsewhere.")
    else:
        print("❌ Chrome failed - this is likely why your bot hangs!")
        print("\n💡 SOLUTION:")
        print("The issue is Chrome/chromedriver in Replit.")
        print("You may need to install Chrome in your Replit environment.")

if __name__ == "__main__":
    main()