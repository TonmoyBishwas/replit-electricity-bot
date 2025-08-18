#!/usr/bin/env python3
"""
Debug the scheduling system
"""

import os
import schedule
from datetime import datetime, timezone
import pytz

def debug_schedule():
    print("🔍 SCHEDULE DEBUG")
    print("=" * 30)
    
    # Current time in different formats
    now = datetime.now()
    print(f"Current local time: {now}")
    print(f"Current UTC time: {datetime.utcnow()}")
    
    # Check timezone
    try:
        import time
        print(f"System timezone: {time.tzname}")
    except:
        print("Could not determine system timezone")
    
    # Check schedule library
    print(f"\nScheduled jobs: {len(schedule.jobs)}")
    for i, job in enumerate(schedule.jobs):
        print(f"  Job {i+1}: {job}")
        print(f"    Next run: {job.next_run}")
        print(f"    Should run: {job.should_run}")
    
    # Check next run
    if schedule.jobs:
        next_run = schedule.next_run()
        print(f"\nNext scheduled run: {next_run}")
        
        # Calculate time until next run
        if next_run:
            time_diff = next_run - now
            print(f"Time until next run: {time_diff}")
            
            if time_diff.total_seconds() < 0:
                print("⚠️ Next run is in the past!")
            elif time_diff.total_seconds() < 3600:  # Less than 1 hour
                print(f"✅ Next run in {int(time_diff.total_seconds()/60)} minutes")
            else:
                print(f"⏰ Next run in {time_diff}")
    
    # Test if schedule is working
    print(f"\nTesting schedule.run_pending()...")
    pending_jobs = [job for job in schedule.jobs if job.should_run]
    print(f"Jobs that should run now: {len(pending_jobs)}")
    
    if pending_jobs:
        print("✅ There are jobs that should run now!")
        for job in pending_jobs:
            print(f"  - {job}")
    else:
        print("❌ No jobs should run now")

if __name__ == "__main__":
    # Set up the same schedule as your bot
    schedule_times = os.getenv('SCHEDULE_TIMES', '00:35,08:00')
    times = [t.strip() for t in schedule_times.split(',')]
    
    print(f"Setting up schedule for times: {times}")
    
    def dummy_job():
        print("Dummy job executed!")
    
    for time_str in times:
        schedule.every().day.at(time_str).do(dummy_job)
    
    debug_schedule()