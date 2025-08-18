#!/usr/bin/env python3
"""
Test the fixed scheduler with a time very close to now
"""

import os
import schedule
import time
from datetime import datetime, timedelta

def test_job():
    print(f"✅ TEST JOB EXECUTED at {datetime.now().strftime('%H:%M:%S')}")

def test_scheduler_precision():
    print("🕐 TESTING SCHEDULER PRECISION")
    print("=" * 40)
    
    # Clear any existing jobs
    schedule.clear()
    
    # Get current time and schedule for 2 minutes from now
    now = datetime.now()
    future_time = now + timedelta(minutes=2)
    test_time = future_time.strftime('%H:%M')
    
    print(f"Current time: {now.strftime('%H:%M:%S')}")
    print(f"Scheduling test job for: {test_time}")
    
    # Schedule the job
    schedule.every().day.at(test_time).do(test_job)
    
    print(f"Next run scheduled for: {schedule.next_run()}")
    print("Waiting for job to execute...")
    print("(This test will run for 3 minutes)")
    
    # Run the scheduler loop (similar to your bot)
    start_time = time.time()
    while time.time() - start_time < 180:  # Run for 3 minutes
        pending_jobs = [job for job in schedule.jobs if job.should_run]
        if pending_jobs:
            print(f"Found {len(pending_jobs)} pending jobs at {datetime.now().strftime('%H:%M:%S')}")
        
        schedule.run_pending()
        
        # Log current time every 30 seconds
        elapsed = time.time() - start_time
        if int(elapsed) % 30 == 0 and elapsed > 0:
            current = datetime.now().strftime('%H:%M:%S')
            next_run = schedule.next_run()
            print(f"Status check - Current: {current} | Next run: {next_run}")
        
        time.sleep(15)  # Check every 15 seconds (like the fixed scheduler)
    
    print("Test completed.")

if __name__ == "__main__":
    test_scheduler_precision()