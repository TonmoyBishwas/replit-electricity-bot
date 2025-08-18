#!/usr/bin/env python3
"""
Diagnostic script to identify why the bot isn't working in Replit
"""

import os
import sys

def check_environment():
    """Check environment variables and setup"""
    print("=== Environment Check ===")
    
    # Check important environment variables
    test_run = os.getenv('TEST_RUN', 'Not set')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', 'Not set')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', 'Not set')
    website_url = os.getenv('METER_WEBSITE_URL', 'Not set')
    
    print(f"TEST_RUN: {test_run}")
    print(f"TELEGRAM_BOT_TOKEN: {'Set' if bot_token != 'Not set' else 'Not set'}")
    print(f"TELEGRAM_CHAT_ID: {'Set' if chat_id != 'Not set' else 'Not set'}")
    print(f"METER_WEBSITE_URL: {website_url}")
    
    if test_run.lower() != 'true':
        print("❌ TEST_RUN is not set to 'true' - bot will run scheduler instead of test")
    else:
        print("✅ TEST_RUN is set correctly")
    
    print()

def check_imports():
    """Check if all required modules can be imported"""
    print("=== Import Check ===")
    
    try:
        import selenium
        print(f"✅ Selenium: {selenium.__version__}")
    except ImportError as e:
        print(f"❌ Selenium: {e}")
    
    try:
        import schedule
        print(f"✅ Schedule: {schedule.__version__}")
    except ImportError as e:
        print(f"❌ Schedule: {e}")
    
    try:
        import requests
        print(f"✅ Requests: {requests.__version__}")
    except ImportError as e:
        print(f"❌ Requests: {e}")
    
    try:
        from selenium import webdriver
        print("✅ WebDriver import successful")
    except ImportError as e:
        print(f"❌ WebDriver: {e}")
    
    print()

def check_chrome():
    """Check if Chrome/chromedriver is available"""
    print("=== Chrome/WebDriver Check ===")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("Attempting to create Chrome driver...")
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver created successfully")
        
        # Try to navigate to a simple page
        driver.get("https://www.google.com")
        print(f"✅ Navigation successful - title: {driver.title}")
        
        driver.quit()
        print("✅ Chrome driver closed successfully")
        
    except Exception as e:
        print(f"❌ Chrome/WebDriver error: {e}")
        print("This is likely the main issue - Replit may not have Chrome installed")
    
    print()

def check_telegram():
    """Check if Telegram bot can send messages"""
    print("=== Telegram Check ===")
    
    try:
        from telegram_bot import TelegramBot
        
        bot = TelegramBot()
        if not bot.bot_token or not bot.chat_id:
            print("❌ Telegram credentials not set")
            return
        
        print("Attempting to send test message...")
        success = bot.send_message("🧪 Diagnostic test from Replit")
        
        if success:
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Failed to send Telegram message")
            
    except Exception as e:
        print(f"❌ Telegram error: {e}")
    
    print()

def check_scraper_import():
    """Check if scraper modules can be imported"""
    print("=== Scraper Import Check ===")
    
    try:
        from scraper import ElectricityMeterScraper
        scraper = ElectricityMeterScraper()
        print("✅ ElectricityMeterScraper imported successfully")
        print(f"✅ Meter nicknames: {scraper.meter_nicknames}")
        
        from scheduled_scraper import ScheduledMeterScraper
        scheduler = ScheduledMeterScraper()
        print("✅ ScheduledMeterScraper imported successfully")
        
    except Exception as e:
        print(f"❌ Scraper import error: {e}")
    
    print()

def main():
    print("🔍 REPLIT DIAGNOSTIC TOOL")
    print("=" * 50)
    
    check_environment()
    check_imports()
    check_scraper_import()
    check_chrome()
    check_telegram()
    
    print("=" * 50)
    print("📋 SUMMARY:")
    print("If Chrome/WebDriver failed, that's likely why the bot hangs.")
    print("Replit may need additional setup for Chrome browser.")
    print("Check the Replit console for any error messages.")

if __name__ == "__main__":
    main()