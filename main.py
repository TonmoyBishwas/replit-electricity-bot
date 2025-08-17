# Replit Entry Point
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the scheduled scraper
from scheduled_scraper import ScheduledMeterScraper

if __name__ == "__main__":
    print("🚀 Starting Multi-Meter Electricity Bot on Replit...")
    print("📊 Configured to monitor 5 meters: 37226784, 37202772, 37195501, 37226785, 37202771")
    print("⚠️ Will only send warnings for meters with balance < 100 BDT")
    
    scheduler = ScheduledMeterScraper()
    
    # For Replit, run a test first to verify everything works
    test_run = os.getenv('TEST_RUN', 'false').lower() == 'true'
    
    if test_run:
        print("🧪 Running test scraping for all meters...")
        scheduler.run_daily_scraping()
    else:
        print("⏰ Starting daily scheduler (8 AM) for all meters...")
        scheduler.start_scheduler()