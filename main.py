# Replit Entry Point
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the scheduled scraper
from scheduled_scraper import ScheduledMeterScraper

if __name__ == "__main__":
    print("🚀 Starting Electricity Meter Bot on Replit...")
    scheduler = ScheduledMeterScraper()
    
    # For Replit, run a test first to verify everything works
    test_run = os.getenv('TEST_RUN', 'false').lower() == 'true'
    
    if test_run:
        print("🧪 Running test scraping...")
        scheduler.run_daily_scraping()
    else:
        print("⏰ Starting daily scheduler (8 AM)...")
        scheduler.start_scheduler()