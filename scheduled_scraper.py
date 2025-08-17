import schedule
import time
import os
import logging
from datetime import datetime
from scraper import ElectricityMeterScraper
from telegram_bot import TelegramBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class ScheduledMeterScraper:
    def __init__(self):
        self.website_url = os.getenv('METER_WEBSITE_URL', 'https://prepaid.desco.org.bd/customer/#/customer-login')
        self.scraper = ElectricityMeterScraper()
        self.telegram_bot = TelegramBot()
        
    def run_daily_scraping(self):
        try:
            logging.info("Starting multi-meter scraping for all 5 meters...")
            
            # Run the scraper for all meters
            low_balance_warnings, all_data = self.scraper.scrape_all_meters(self.website_url)
            
            if all_data:
                logging.info(f"Scraping completed successfully for {len(all_data)} meters")
                
                # Only send message if there are low balance warnings
                if low_balance_warnings:
                    logging.info(f"Found {len(low_balance_warnings)} meters with low balance")
                    telegram_success = self.telegram_bot.send_low_balance_warnings(low_balance_warnings)
                    
                    if telegram_success:
                        logging.info("Low balance warnings sent to Telegram successfully")
                    else:
                        logging.error("Failed to send warnings to Telegram")
                else:
                    logging.info("All meters have sufficient balance (>= 100 BDT). No notifications sent.")
                
            else:
                logging.error("Scraping failed for all meters")
                # Send error notification to Telegram
                error_msg = f"❌ Electricity meter scraping failed for all meters at {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
                self.telegram_bot.send_message(error_msg)
                
        except Exception as e:
            logging.error(f"Error in daily scraping: {str(e)}")
            error_msg = f"❌ Scraper error: {str(e)}\nTime: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
            self.telegram_bot.send_message(error_msg)
    
    def start_scheduler(self):
        # Schedule the scraping for 8:00 AM daily
        schedule.every().day.at("08:00").do(self.run_daily_scraping)
        
        logging.info("Scheduler started. Will run daily at 8:00 AM")
        logging.info("Next run scheduled for: " + str(schedule.next_run()))
        
        # Send startup notification
        startup_msg = f"🤖 Electricity meter bot started!\n📅 Scheduled to run daily at 8:00 AM\n⏰ Next run: {schedule.next_run()}"
        self.telegram_bot.send_message(startup_msg)
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Import keep_alive for Replit
    try:
        from keep_alive import keep_alive
        keep_alive()  # Start web server to keep Repl alive
        logging.info("Keep-alive server started for Replit")
    except ImportError:
        logging.info("Keep-alive not available (running locally)")
    
    scheduler = ScheduledMeterScraper()
    
    # For testing - run once immediately
    if os.getenv('TEST_RUN', 'false').lower() == 'true':
        logging.info("Running test scraping...")
        scheduler.run_daily_scraping()
    else:
        # Start the scheduler
        scheduler.start_scheduler()