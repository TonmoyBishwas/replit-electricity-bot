#!/usr/bin/env python3
"""
Test the fixed scraper with SSL bypass options
"""

import os
import sys
from datetime import datetime

def test_fixed_scraper():
    print("🔧 TESTING FIXED SCRAPER WITH SSL BYPASS")
    print("=" * 50)
    
    try:
        from scraper import ElectricityMeterScraper
        
        print("Creating scraper with SSL bypass...")
        scraper = ElectricityMeterScraper()
        
        print("Setting up Chrome driver...")
        success = scraper.setup_driver()
        
        if success:
            print("✅ Chrome driver created successfully!")
            
            website_url = "https://prepaid.desco.org.bd/customer/#/customer-login"
            print(f"Testing navigation to: {website_url}")
            
            scraper.driver.get(website_url)
            print(f"✅ Page loaded successfully!")
            print(f"Page title: {scraper.driver.title}")
            print(f"Current URL: {scraper.driver.current_url}")
            
            scraper.driver.quit()
            print("✅ SSL bypass fix successful!")
            return True
        else:
            print("❌ Failed to create Chrome driver")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_single_account():
    print("\n🧪 TESTING SINGLE ACCOUNT SCRAPE")
    print("=" * 50)
    
    try:
        from scraper import ElectricityMeterScraper
        
        scraper = ElectricityMeterScraper()
        website_url = "https://prepaid.desco.org.bd/customer/#/customer-login"
        
        print("Testing scrape for account 37226784 (Ayon)...")
        
        # Test just the first account to see if it works
        data = scraper.scrape_account('37226784', website_url)
        
        if data:
            print("✅ Account scraping successful!")
            print(f"Account: {data.get('account_number')} ({data.get('nickname')})")
            print(f"Status: {data.get('status')}")
            print(f"Balance: {data.get('remaining_balance', 'N/A')}")
            print(f"Numeric balance: {data.get('balance_numeric')}")
            print(f"Recently recharged: {data.get('recently_recharged', False)}")
            return True
        else:
            print("❌ Account scraping failed")
            return False
            
    except Exception as e:
        print(f"❌ Single account test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing the SSL-fixed scraper...")
    
    if test_fixed_scraper():
        print("\n🎯 SSL FIX WORKS!")
        print("Now testing actual account scraping...")
        
        if test_single_account():
            print("\n🎉 SUCCESS! The bot should now work in Replit!")
            print("Try running: python main.py")
        else:
            print("\n⚠️ SSL fix works but scraping has other issues")
    else:
        print("\n❌ SSL fix didn't work")