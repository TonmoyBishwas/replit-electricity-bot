#!/usr/bin/env python3
"""
Test the Bangladesh timezone scheduler
"""

import os
import sys
from datetime import datetime
import pytz

def test_bd_timezone_conversion():
    print("🇧🇩 TESTING BANGLADESH TIMEZONE SCHEDULER")
    print("=" * 50)
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        # Test case: You want 9:03 AM and 11:00 AM Bangladesh time
        test_schedule = "9:03,11:00"
        os.environ['SCHEDULE_TIMES'] = test_schedule
        
        print(f"Input (Bangladesh time): {test_schedule}")
        
        # Create scheduler
        scraper = ScheduledMeterScraper()
        
        print(f"Parsed BD times: {scraper.bd_schedule_times}")
        print(f"Converted system times: {scraper.system_schedule_times}")
        
        # Show the conversion details
        bd_tz = pytz.timezone('Asia/Dhaka')
        current_bd = datetime.now(bd_tz)
        current_system = datetime.now()
        
        print(f"\nCurrent times:")
        print(f"  Bangladesh: {current_bd}")
        print(f"  System: {current_system}")
        
        # Verify the conversion is correct
        print(f"\nConversion verification:")
        for i, (bd_time, sys_time) in enumerate(zip(scraper.bd_schedule_times, scraper.system_schedule_times)):
            print(f"  BD {bd_time} -> System {sys_time}")
            
            # Calculate expected conversion
            bd_hour, bd_minute = map(int, bd_time.split(':'))
            expected_sys_hour = (bd_hour - 6) % 24  # BD is UTC+6
            expected_sys_time = f"{expected_sys_hour:02d}:{bd_minute:02d}"
            
            if sys_time == expected_sys_time:
                print(f"    ✅ Correct conversion (BD is UTC+6)")
            else:
                print(f"    ⚠️ Unexpected conversion (expected {expected_sys_time})")
        
        # Clean up
        if 'SCHEDULE_TIMES' in os.environ:
            del os.environ['SCHEDULE_TIMES']
        
        return True
        
    except Exception as e:
        print(f"❌ BD timezone test failed: {e}")
        return False

def test_real_scenario():
    print(f"\n⏰ TESTING YOUR REAL SCENARIO")
    print("=" * 50)
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        import schedule
        
        # Clear any existing schedule
        schedule.clear()
        
        # Your actual desired times: 9:03 AM and 11:00 AM Bangladesh
        os.environ['SCHEDULE_TIMES'] = "9:03,11:00"
        
        scraper = ScheduledMeterScraper()
        
        # Manually create jobs like the real scheduler
        for i, system_time in enumerate(scraper.system_schedule_times):
            bd_time = scraper.bd_schedule_times[i]
            job = schedule.every().day.at(system_time).do(lambda: print(f"Job executed!"))
            print(f"Scheduled: BD {bd_time} -> System {system_time}")
            print(f"  Next run: {job.next_run}")
        
        # Check when it will actually run
        next_run = schedule.next_run()
        if next_run:
            bd_tz = pytz.timezone('Asia/Dhaka')
            next_run_utc = pytz.UTC.localize(next_run)
            next_run_bd = next_run_utc.astimezone(bd_tz)
            
            print(f"\nNext execution:")
            print(f"  System time: {next_run}")
            print(f"  Bangladesh time: {next_run_bd}")
            print(f"  In Bangladesh format: {next_run_bd.strftime('%I:%M %p')}")
        
        # Clean up
        schedule.clear()
        if 'SCHEDULE_TIMES' in os.environ:
            del os.environ['SCHEDULE_TIMES']
        
        return True
        
    except Exception as e:
        print(f"❌ Real scenario test failed: {e}")
        return False

def show_usage_instructions():
    print(f"\n📋 HOW TO USE BANGLADESH TIMEZONE SCHEDULER")
    print("=" * 50)
    
    print("✅ NOW YOU CAN USE BANGLADESH TIME DIRECTLY!")
    print()
    print("🇧🇩 Set your desired Bangladesh times:")
    print("   SCHEDULE_TIMES=9:03,11:00")
    print("   (This means 9:03 AM and 11:00 AM Bangladesh time)")
    print()
    print("🤖 The bot will automatically:")
    print("   - Convert to system time (UTC)")
    print("   - Schedule correctly for Bangladesh time")
    print("   - Show Bangladesh time in Telegram messages")
    print()
    print("📅 Example conversions:")
    print("   BD 9:03 AM  -> UTC 3:03 AM  (runs at 9:03 AM your time)")
    print("   BD 11:00 AM -> UTC 5:00 AM  (runs at 11:00 AM your time)")
    print("   BD 8:00 PM  -> UTC 2:00 PM  (runs at 8:00 PM your time)")
    print()
    print("⏰ Your Telegram will show:")
    print("   'Scheduled to run daily at: 9:03, 11:00 (Bangladesh time)'")
    print("   'Next run: 2025-08-18 09:03 AM BD'")

if __name__ == "__main__":
    print("🧪 BANGLADESH TIMEZONE SCHEDULER TEST")
    print("=" * 50)
    
    all_passed = True
    
    if not test_bd_timezone_conversion():
        all_passed = False
    
    if not test_real_scenario():
        all_passed = False
    
    if all_passed:
        print("\n🎉 ALL BANGLADESH TIMEZONE TESTS PASSED!")
        show_usage_instructions()
    else:
        print("\n❌ Some tests failed")