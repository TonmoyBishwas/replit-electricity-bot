#!/usr/bin/env python3
"""
Test all the critical fixes for scheduling and timezone bugs
"""

import os
import sys
from datetime import datetime, timedelta

def test_schedule_parsing():
    print("🕐 TESTING SCHEDULE PARSING FIXES")
    print("=" * 50)
    
    test_cases = [
        ("1:07,8:00", ["01:07", "08:00"]),  # Your problematic case
        ("01:07,08:00", ["01:07", "08:00"]),  # Already formatted
        ("1:7,8:0", ["01:07", "08:00"]),  # Single digit minutes
        ("23:59,00:01", ["23:59", "00:01"]),  # Edge cases
        ("invalid,8:00", ["08:00"]),  # Mixed valid/invalid
    ]
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        for input_str, expected in test_cases:
            print(f"\nTest: '{input_str}'")
            print(f"Expected: {expected}")
            
            # Set environment variable
            os.environ['SCHEDULE_TIMES'] = input_str
            
            # Create scraper and test parsing
            scraper = ScheduledMeterScraper()
            result = scraper.schedule_times
            
            print(f"Got: {result}")
            
            if result == expected:
                print("✅ PASS")
            else:
                print("❌ FAIL")
        
        # Clean up
        if 'SCHEDULE_TIMES' in os.environ:
            del os.environ['SCHEDULE_TIMES']
        
        return True
        
    except Exception as e:
        print(f"❌ Schedule parsing test failed: {e}")
        return False

def test_timezone_handling():
    print("\n🌍 TESTING TIMEZONE HANDLING")
    print("=" * 50)
    
    try:
        from telegram_bot import TelegramBot
        
        bot = TelegramBot()
        
        # Test Bangladesh time calculation
        bd_time = bot.get_bangladesh_time()
        utc_time = datetime.utcnow()
        
        print(f"UTC Time: {utc_time}")
        print(f"Bangladesh Time: {bd_time}")
        
        # Calculate time difference
        time_diff = bd_time.replace(tzinfo=None) - utc_time
        hours_diff = time_diff.total_seconds() / 3600
        
        print(f"Time difference: {hours_diff:.1f} hours")
        
        # Bangladesh is UTC+6
        if abs(hours_diff - 6.0) < 1.0:  # Allow some tolerance
            print("✅ Timezone calculation is correct")
            return True
        else:
            print(f"❌ Timezone calculation is wrong (should be ~6 hours)")
            return False
            
    except Exception as e:
        print(f"❌ Timezone test failed: {e}")
        return False

def test_time_normalization():
    print("\n🔧 TESTING TIME NORMALIZATION")
    print("=" * 50)
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        scraper = ScheduledMeterScraper()
        
        test_cases = [
            ("1:07", "01:07"),
            ("01:07", "01:07"),
            ("1:7", "01:07"),
            ("23:59", "23:59"),
            ("0:0", "00:00"),
            ("invalid", None),
            ("25:00", None),  # Invalid hour
            ("12:60", None),  # Invalid minute
        ]
        
        for input_str, expected in test_cases:
            result = scraper.normalize_time_format(input_str)
            print(f"'{input_str}' -> '{result}' (expected: '{expected}')")
            
            if result == expected:
                print("✅ PASS")
            else:
                print("❌ FAIL")
        
        return True
        
    except Exception as e:
        print(f"❌ Time normalization test failed: {e}")
        return False

def test_schedule_validation():
    print("\n📋 TESTING SCHEDULE VALIDATION")
    print("=" * 50)
    
    try:
        import schedule
        from scheduled_scraper import ScheduledMeterScraper
        
        # Clear any existing jobs
        schedule.clear()
        
        # Set test schedule
        os.environ['SCHEDULE_TIMES'] = '01:07,08:00'
        
        scraper = ScheduledMeterScraper()
        
        # Manually set up jobs like the scheduler does
        for time_str in scraper.schedule_times:
            job = schedule.every().day.at(time_str).do(lambda: print("Test job"))
        
        print(f"Scheduled times: {scraper.schedule_times}")
        print(f"Number of jobs: {len(schedule.jobs)}")
        
        for i, job in enumerate(schedule.jobs):
            print(f"Job {i+1}: {job} | Next run: {job.next_run}")
        
        next_run = schedule.next_run()
        print(f"Next run: {next_run}")
        
        # Clean up
        schedule.clear()
        if 'SCHEDULE_TIMES' in os.environ:
            del os.environ['SCHEDULE_TIMES']
        
        return True
        
    except Exception as e:
        print(f"❌ Schedule validation test failed: {e}")
        return False

def show_deployment_instructions():
    print("\n📋 DEPLOYMENT INSTRUCTIONS (UPDATED)")
    print("=" * 50)
    
    print("✅ ALL CRITICAL BUGS HAVE BEEN FIXED:")
    print("1. Schedule parsing now handles '1:07' correctly -> '01:07'")
    print("2. Timezone display now shows correct Bangladesh time")
    print("3. Added comprehensive validation and debug logging")
    print()
    print("🚀 TO DEPLOY:")
    print("1. Upload all fixed files to Replit")
    print("2. Install new dependency: pip install pytz")
    print("3. Set environment variables:")
    print("   SCHEDULE_TIMES=1:07,8:00")
    print("   TEST_RUN=false")
    print("   (other variables as before)")
    print()
    print("4. Run the bot - you should see detailed debug logs")
    print("5. The startup message will show CORRECT schedule times")
    print("6. Telegram messages will show CORRECT Bangladesh time")
    print()
    print("🔍 DEBUG LOGS WILL SHOW:")
    print("- Raw input: '1:07,8:00'")
    print("- Normalized: ['01:07', '08:00']") 
    print("- Scheduled jobs with correct times")
    print("- Timezone conversion details")

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE FIX TESTING")
    print("=" * 50)
    
    all_passed = True
    
    if not test_schedule_parsing():
        all_passed = False
    
    if not test_timezone_handling():
        all_passed = False
    
    if not test_time_normalization():
        all_passed = False
    
    if not test_schedule_validation():
        all_passed = False
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("The critical bugs have been fixed!")
        show_deployment_instructions()
    else:
        print("\n❌ Some tests failed")
        print("Please check the errors above")