#!/usr/bin/env python3
"""
Force run the meter scraping immediately (for testing)
"""

import os
import sys
from datetime import datetime

def run_now():
    print("🚀 FORCE RUNNING METER SCRAPING NOW")
    print("=" * 40)
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        from scheduled_scraper import ScheduledMeterScraper
        
        scheduler = ScheduledMeterScraper()
        print("Starting immediate scraping run...")
        
        scheduler.run_daily_scraping()
        print("✅ Immediate run completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_now()