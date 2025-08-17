#!/usr/bin/env python3
"""
Test script for the multi-meter low balance warning system
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import ElectricityMeterScraper
from telegram_bot import TelegramBot

def test_balance_extraction():
    """Test the balance extraction function"""
    print("=== Testing Balance Extraction ===")
    scraper = ElectricityMeterScraper()
    
    test_cases = [
        "Remaining Balance: 135.25 BDT",
        "Balance: 89.50 BDT",
        "Current Balance: 1,250.00 BDT", 
        "Not found",
        "Error",
        "Balance 45.75 BDT Reading time: 17 Aug 2025"
    ]
    
    for test_case in test_cases:
        numeric_balance = scraper.extract_numeric_balance(test_case)
        print(f"Input: '{test_case}' -> Numeric: {numeric_balance}")
    
    print()

def test_warning_message():
    """Test the warning message formatting"""
    print("=== Testing Warning Message Format ===")
    
    # Create sample warnings
    warnings = [
        {
            'account_number': '37226784',
            'balance_text': 'Remaining Balance: 89.50 BDT',
            'balance_numeric': 89.50,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'account_number': '37202772', 
            'balance_text': 'Balance: 45.20 BDT',
            'balance_numeric': 45.20,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    bot = TelegramBot()
    
    # Test with warnings
    print("Sample warning message:")
    print("=" * 50)
    message = bot.send_low_balance_warnings.__func__(bot, warnings)
    
    # Test with no warnings
    print("\nTesting with no warnings:")
    result = bot.send_low_balance_warnings([])
    print(f"Result for empty warnings: {result}")
    
    print()

def simulate_multi_meter_run():
    """Simulate what happens during a multi-meter run"""
    print("=== Simulating Multi-Meter Run ===")
    
    # Sample data for simulation
    sample_data = [
        {'account_number': '37226784', 'balance_numeric': 150.0, 'status': 'success'},
        {'account_number': '37202772', 'balance_numeric': 89.5, 'status': 'success'},
        {'account_number': '37195501', 'balance_numeric': 250.0, 'status': 'success'},
        {'account_number': '37226785', 'balance_numeric': 45.2, 'status': 'success'},
        {'account_number': '37202771', 'balance_numeric': 300.0, 'status': 'success'}
    ]
    
    warnings = []
    
    print("Checking balances:")
    for data in sample_data:
        account = data['account_number']
        balance = data['balance_numeric']
        
        if balance < 100:
            warnings.append({
                'account_number': account,
                'balance_numeric': balance,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"WARNING: Meter {account}: {balance} BDT (LOW BALANCE)")
        else:
            print(f"OK: Meter {account}: {balance} BDT (SUFFICIENT)")
    
    print(f"\nResult: {len(warnings)} meter(s) need recharging")
    
    if warnings:
        print("Would send warning message to Telegram")
    else:
        print("No warnings to send - all meters have sufficient balance")
    
    return warnings

if __name__ == "__main__":
    print("Multi-Meter System Test")
    print("=" * 40)
    
    test_balance_extraction()
    test_warning_message() 
    warnings = simulate_multi_meter_run()
    
    print("\nTest completed!")
    print(f"System ready to monitor {len(['37226784', '37202772', '37195501', '37226785', '37202771'])} meters")