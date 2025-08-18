import schedule
import time
import os
import logging
from datetime import datetime, timedelta
import pytz
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
        
        # Set up timezone handling
        self.bd_timezone = pytz.timezone('Asia/Dhaka')
        self.system_timezone = None  # Will be determined at runtime
        
        # Get custom schedule times from environment variables  
        # Format: "9:03,11:00" (Bangladesh time) - will be converted to system time
        schedule_times_str = os.getenv('SCHEDULE_TIMES', '08:00')  # Default to 8 AM BD time
        self.bd_schedule_times = self.parse_schedule_times(schedule_times_str)
        self.system_schedule_times = self.convert_bd_to_system_time(self.bd_schedule_times)
        
    def parse_schedule_times(self, times_str):
        """Parse schedule times from string like '1:07,8:00' or '12:20'"""
        try:
            logging.info(f"Raw schedule times input: '{times_str}'")
            
            # Split by comma and clean up each time
            times = [time.strip() for time in times_str.split(',')]
            logging.info(f"Split times: {times}")
            
            # Validate and normalize each time format
            valid_times = []
            for time_str in times:
                normalized_time = self.normalize_time_format(time_str)
                if normalized_time and self.validate_time_format(normalized_time):
                    valid_times.append(normalized_time)
                    logging.info(f"Accepted time: '{time_str}' -> '{normalized_time}'")
                else:
                    logging.warning(f"Invalid time format: '{time_str}'")
            
            if not valid_times:
                logging.warning("No valid schedule times found, using default 08:00")
                return ['08:00']
            
            logging.info(f"Final parsed schedule times: {valid_times}")
            return valid_times
        except Exception as e:
            logging.error(f"Error parsing schedule times: {e}")
            return ['08:00']  # Fallback to default
    
    def normalize_time_format(self, time_str):
        """Normalize time format from '1:07' to '01:07'"""
        try:
            # Handle formats like '1:07', '01:07', '1:7', etc.
            if ':' not in time_str:
                logging.warning(f"Time string missing colon: '{time_str}'")
                return None
            
            parts = time_str.split(':')
            if len(parts) != 2:
                logging.warning(f"Time string has wrong format: '{time_str}'")
                return None
            
            hour_str, minute_str = parts
            
            # Convert to integers and validate ranges
            hour = int(hour_str)
            minute = int(minute_str)
            
            if not (0 <= hour <= 23):
                logging.warning(f"Invalid hour: {hour}")
                return None
            
            if not (0 <= minute <= 59):
                logging.warning(f"Invalid minute: {minute}")
                return None
            
            # Format with zero padding
            normalized = f"{hour:02d}:{minute:02d}"
            logging.info(f"Normalized '{time_str}' to '{normalized}'")
            return normalized
            
        except ValueError as e:
            logging.warning(f"Could not parse time '{time_str}': {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error normalizing time '{time_str}': {e}")
            return None
    
    def convert_bd_to_system_time(self, bd_times):
        """Convert Bangladesh time to system time for scheduling"""
        try:
            system_times = []
            
            # Get current time to determine timezone offset
            bd_now = datetime.now(self.bd_timezone)
            system_now = datetime.now()
            
            # Calculate offset between BD time and system time
            # This handles the timezone conversion automatically
            offset_hours = (bd_now.replace(tzinfo=None) - system_now).total_seconds() / 3600
            
            logging.info(f"Timezone conversion - BD: {bd_now}, System: {system_now}")
            logging.info(f"BD to System offset: {offset_hours:.1f} hours")
            
            for bd_time_str in bd_times:
                try:
                    # Parse BD time
                    bd_hour, bd_minute = map(int, bd_time_str.split(':'))
                    
                    # Create a BD datetime for today
                    today = bd_now.date()
                    bd_datetime = self.bd_timezone.localize(
                        datetime.combine(today, datetime.min.time().replace(hour=bd_hour, minute=bd_minute))
                    )
                    
                    # Convert to UTC (system timezone for Replit)
                    utc_datetime = bd_datetime.astimezone(pytz.UTC)
                    system_time_str = utc_datetime.strftime('%H:%M')
                    
                    system_times.append(system_time_str)
                    
                    logging.info(f"Converted BD {bd_time_str} -> UTC {system_time_str}")
                    logging.info(f"  BD datetime: {bd_datetime}")
                    logging.info(f"  UTC datetime: {utc_datetime}")
                    
                except Exception as e:
                    logging.error(f"Error converting time {bd_time_str}: {e}")
                    # Fallback: assume 6-hour difference (BD is UTC+6)
                    bd_hour, bd_minute = map(int, bd_time_str.split(':'))
                    system_hour = (bd_hour - 6) % 24
                    system_time_str = f"{system_hour:02d}:{bd_minute:02d}"
                    system_times.append(system_time_str)
                    logging.warning(f"Using fallback conversion: BD {bd_time_str} -> System {system_time_str}")
            
            return system_times
            
        except Exception as e:
            logging.error(f"Error in timezone conversion: {e}")
            # Fallback to original times
            return bd_times
    
    def validate_time_format(self, time_str):
        """Validate time format HH:MM"""
        try:
            from datetime import datetime
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
        
    def run_daily_scraping(self):
        try:
            logging.info("Starting multi-meter scraping for all 5 meters...")
            
            # Run the scraper for all meters
            low_balance_warnings, recently_recharged, all_data = self.scraper.scrape_all_meters(self.website_url)
            
            if all_data:
                logging.info(f"Scraping completed successfully for {len(all_data)} meters")
                
                # Send message if there are low balance warnings OR recently recharged meters
                if low_balance_warnings or recently_recharged:
                    logging.info(f"Found {len(low_balance_warnings)} meters with low balance and {len(recently_recharged)} recently recharged")
                    telegram_success = self.telegram_bot.send_meter_status_update(low_balance_warnings, recently_recharged)
                    
                    if telegram_success:
                        logging.info("Meter status update sent to Telegram successfully")
                    else:
                        logging.error("Failed to send status update to Telegram")
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
        # Comprehensive validation and debug logging
        current_system_time = datetime.now()
        current_bd_time = datetime.now(self.bd_timezone)
        
        logging.info(f"=== BANGLADESH TIMEZONE SCHEDULER DEBUG ===")
        logging.info(f"Current system time (UTC): {current_system_time}")
        logging.info(f"Current Bangladesh time: {current_bd_time}")
        logging.info(f"Environment SCHEDULE_TIMES: '{os.getenv('SCHEDULE_TIMES', 'NOT_SET')}' (Bangladesh time)")
        logging.info(f"Parsed BD schedule times: {self.bd_schedule_times}")
        logging.info(f"Converted system schedule times: {self.system_schedule_times}")
        
        # Schedule the scraping using SYSTEM times (converted from BD times)
        scheduled_jobs = []
        for i, system_time_str in enumerate(self.system_schedule_times):
            bd_time_str = self.bd_schedule_times[i]
            job = schedule.every().day.at(system_time_str).do(self.run_daily_scraping)
            scheduled_jobs.append(job)
            logging.info(f"✅ Scheduled BD time {bd_time_str} as system time {system_time_str}")
            logging.info(f"   Job details: {job}")
        
        # Validate that jobs were scheduled correctly
        all_jobs = schedule.jobs
        logging.info(f"Total scheduled jobs: {len(all_jobs)}")
        for i, job in enumerate(all_jobs):
            bd_time = self.bd_schedule_times[i] if i < len(self.bd_schedule_times) else "N/A"
            logging.info(f"   Job {i+1}: BD {bd_time} -> System {job.next_run}")
        
        # Calculate and validate next run time
        next_run = schedule.next_run()
        logging.info(f"Next run calculated as: {next_run} (system time)")
        
        # Convert next run to Bangladesh time for display
        if next_run:
            # Convert system time to BD time for user-friendly display
            next_run_bd = None
            try:
                next_run_utc = pytz.UTC.localize(next_run)
                next_run_bd = next_run_utc.astimezone(self.bd_timezone)
                logging.info(f"Next run in Bangladesh time: {next_run_bd}")
            except:
                logging.warning("Could not convert next run to Bangladesh time")
            
            time_until_next = next_run - current_system_time
            logging.info(f"Time until next run: {time_until_next}")
            
            if time_until_next.total_seconds() < 0:
                logging.warning("⚠️ Next run is in the past! This indicates a scheduling bug.")
            elif time_until_next.total_seconds() < 300:  # Less than 5 minutes
                logging.info(f"✅ Next run is soon: {int(time_until_next.total_seconds()/60)} minutes")
            else:
                logging.info(f"⏰ Next run in: {time_until_next}")
        
        bd_times_display = ", ".join(self.bd_schedule_times)
        logging.info(f"Scheduler started. Will run daily at: {bd_times_display} (Bangladesh time)")
        logging.info("=== END SCHEDULER DEBUG ===")
        
        # Send startup notification showing Bangladesh times (user-friendly)
        startup_msg = f"🤖 Electricity meter bot started!\n"
        startup_msg += f"📅 Scheduled to run daily at: {bd_times_display} (Bangladesh time)\n"
        if next_run_bd:
            startup_msg += f"⏰ Next run: {next_run_bd.strftime('%Y-%m-%d %I:%M %p')} BD\n"
        else:
            startup_msg += f"⏰ Next run: {next_run}\n"
        startup_msg += f"🏠 Monitoring 5 meters: Ayon, Arif, Payel, Piyal, Solo"
        
        telegram_success = self.telegram_bot.send_message(startup_msg)
        if telegram_success:
            logging.info("✅ Startup notification sent to Telegram")
        else:
            logging.error("❌ Failed to send startup notification to Telegram")
        
        # Keep the script running
        while True:
            # Check for pending jobs
            pending_jobs = [job for job in schedule.jobs if job.should_run]
            if pending_jobs:
                logging.info(f"Found {len(pending_jobs)} pending jobs, executing...")
            
            schedule.run_pending()
            
            # Log next run time every 10 minutes
            current_time = datetime.now()
            if current_time.minute % 10 == 0 and current_time.second < 30:
                next_run = schedule.next_run()
                logging.info(f"Current time: {current_time.strftime('%H:%M:%S')} | Next run: {next_run}")
            
            time.sleep(15)  # Check every 15 seconds for better precision

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