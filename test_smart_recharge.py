#!/usr/bin/env python3
"""
Test script for the smart same-day recharge detection system
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import ElectricityMeterScraper
from telegram_bot import TelegramBot

def test_datetime_parsing():
    """Test datetime parsing from website text"""
    print("=== Testing DateTime Parsing ===")
    scraper = ElectricityMeterScraper()
    
    test_cases = [
        "Reading time: 17 Aug 2025 00:00",
        "Recharge time: 17 Aug 2025 15:16", 
        "Last Recharge: 1,000.00 BDT Recharge time: 17 Aug 2025 15:16",
        "Remaining Balance: -36.3 BDT Reading time: 17 Aug 2025 00:00",
        "10 Jul 2025 13:51",
        "Invalid date format"
    ]
    
    for test_case in test_cases:
        parsed_dt = scraper.parse_datetime_from_text(test_case)
        print(f"Input: '{test_case}'")
        print(f"Parsed: {parsed_dt}\n")

def test_same_day_recharge_logic():
    """Test the same-day recharge detection logic"""
    print("=== Testing Same-Day Recharge Logic ===")
    scraper = ElectricityMeterScraper()
    
    test_scenarios = [
        {
            "name": "Same day, recharge after reading (should detect)",
            "balance_reading": "Reading time: 17 Aug 2025 00:00",
            "recharge_date": "Recharge time: 17 Aug 2025 15:16",
            "expected": True
        },
        {
            "name": "Same day, recharge before reading (should not detect)",
            "balance_reading": "Reading time: 17 Aug 2025 15:00",
            "recharge_date": "Recharge time: 17 Aug 2025 10:00",
            "expected": False
        },
        {
            "name": "Different days (should not detect)",
            "balance_reading": "Reading time: 17 Aug 2025 00:00",
            "recharge_date": "Recharge time: 16 Aug 2025 15:16",
            "expected": False
        },
        {
            "name": "Your actual case - Arif meter",
            "balance_reading": "Reading time: 17 Aug 2025 00:00",
            "recharge_date": "Recharge time: 17 Aug 2025 15:16",
            "expected": True
        }
    ]
    
    for scenario in test_scenarios:
        result = scraper.is_same_day_recharge_after_reading(
            scenario["balance_reading"], 
            scenario["recharge_date"]
        )
        status = "✅ PASS" if result == scenario["expected"] else "❌ FAIL"
        print(f"{status} - {scenario['name']}")
        print(f"  Expected: {scenario['expected']}, Got: {result}\n")

def test_smart_recharge_logic():
    """Test the complete smart recharge logic"""
    print("=== Testing Smart Recharge Logic ===")
    scraper = ElectricityMeterScraper()
    
    # Simulate Arif's meter data (37202772)
    test_data = {
        'account_number': '37202772',
        'nickname': 'Arif',
        'balance_numeric': -36.3,
        'reading_time': 'Reading time: 17 Aug 2025 00:00',
        'last_recharge_date': 'Recharge time: 17 Aug 2025 15:16',
        'last_recharge_amount': 'Last Recharge: 1,000.00 BDT',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print("Input data:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    # Apply smart logic
    result = scraper.apply_smart_recharge_logic(test_data)
    
    print(f"\nResult:")
    print(f"  Recently recharged: {result.get('recently_recharged', False)}")
    print(f"  Recharge amount: {result.get('recharge_amount_numeric')}")
    
    if result.get('recently_recharged'):
        print("✅ SUCCESS: System correctly detected same-day recharge!")
        print("   This meter should NOT trigger a low balance warning.")
    else:
        print("❌ ISSUE: System did not detect same-day recharge.")
        print("   This meter would trigger a false low balance warning.")

def test_telegram_message_format():
    """Test the new Telegram message format"""
    print("\n=== Testing Telegram Message Format ===")
    
    # Test scenario: One low balance warning, one recently recharged
    warnings = [
        {
            'account_number': '37226784',
            'nickname': 'Ayon', 
            'balance_numeric': 89.5,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    recently_recharged = [
        {
            'account_number': '37202772',
            'nickname': 'Arif',
            'recharge_amount': 1000.0,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    bot = TelegramBot()
    
    print("Sample message format:")
    print("=" * 50)
    
    # The method will try to send to Telegram, but we can see the message structure
    # by checking what would be sent
    print("Would send message with:")
    print(f"- {len(warnings)} low balance warning(s)")
    print(f"- {len(recently_recharged)} recently recharged meter(s)")
    print(f"- 3 other meters with sufficient balance")

if __name__ == "__main__":
    print("Smart Recharge Detection System Test")
    print("=" * 50)
    
    test_datetime_parsing()
    test_same_day_recharge_logic()
    test_smart_recharge_logic()
    test_telegram_message_format()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Nicknames: Ayon, Arif, Payel, Piyal, Solo")
    print("- Smart recharge detection for same-day recharges")
    print("- No false warnings for recently recharged meters")
    print("- Enhanced Telegram messages with nicknames and activity")