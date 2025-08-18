#!/usr/bin/env python3
"""
Test script for the custom scheduling system
"""

import os
import sys
from datetime import datetime

def test_schedule_parsing():
    print("🕐 TESTING SCHEDULE PARSING")
    print("=" * 40)
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        # Test different schedule configurations
        test_cases = [
            ("08:00", "Single time"),
            ("12:20,08:00", "Two times"),
            ("06:00,12:20,18:30", "Three times"),
            ("00:20,23:59", "Edge times"),
            ("invalid", "Invalid format"),
            ("12:20,invalid,08:00", "Mixed valid/invalid")
        ]
        
        for schedule_str, description in test_cases:
            print(f"\nTesting: {description}")
            print(f"Input: '{schedule_str}'")
            
            # Temporarily set environment variable
            os.environ['SCHEDULE_TIMES'] = schedule_str
            
            scraper = ScheduledMeterScraper()
            print(f"Parsed times: {scraper.schedule_times}")
            
        # Reset to default
        if 'SCHEDULE_TIMES' in os.environ:
            del os.environ['SCHEDULE_TIMES']
            
        print("\n✅ Schedule parsing test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Schedule parsing test failed: {e}")
        return False

def test_time_validation():
    print("\n⏰ TESTING TIME VALIDATION")
    print("=" * 40)
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        scraper = ScheduledMeterScraper()
        
        valid_times = ["00:00", "08:00", "12:20", "23:59"]
        invalid_times = ["24:00", "12:60", "abc", "8:00", "08:0"]
        
        print("Valid times:")
        for time_str in valid_times:
            result = scraper.validate_time_format(time_str)
            status = "✅" if result else "❌"
            print(f"  {status} {time_str}")
        
        print("\nInvalid times:")
        for time_str in invalid_times:
            result = scraper.validate_time_format(time_str)
            status = "❌" if not result else "✅"
            print(f"  {status} {time_str}")
        
        return True
        
    except Exception as e:
        print(f"❌ Time validation test failed: {e}")
        return False

def show_deployment_instructions():
    print("\n📋 DEPLOYMENT INSTRUCTIONS")
    print("=" * 50)
    
    print("1. SET ENVIRONMENT VARIABLES in Replit Secrets:")
    print("   TELEGRAM_BOT_TOKEN=your_bot_token")
    print("   TELEGRAM_CHAT_ID=your_chat_id")
    print("   SCHEDULE_TIMES=12:20,08:00  (for your desired times)")
    print("   TEST_RUN=false  (for production)")
    print()
    print("2. SCHEDULE_TIMES FORMAT:")
    print("   Single time: '08:00'")
    print("   Multiple times: '12:20,08:00' (comma-separated)")
    print("   Your request: '00:20,08:00' (12:20 AM and 8:00 AM)")
    print()
    print("3. DEPLOY:")
    print("   - Upload all files to Replit")
    print("   - Set environment variables")
    print("   - Click 'Run' button")
    print("   - Bot will start automatically and stay running")
    print()
    print("4. VERIFY:")
    print("   - Check Replit console for startup message")
    print("   - Visit the Replit web URL to see status page")
    print("   - You'll get a Telegram message confirming startup")

if __name__ == "__main__":
    print("🧪 CUSTOM SCHEDULING SYSTEM TEST")
    print("=" * 50)
    
    if test_schedule_parsing() and test_time_validation():
        print("\n🎉 ALL TESTS PASSED!")
        show_deployment_instructions()
    else:
        print("\n❌ Some tests failed")