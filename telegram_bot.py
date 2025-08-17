import requests
import json
import os
from datetime import datetime

class TelegramBot:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message):
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                print("Message sent successfully to Telegram!")
                return True
            else:
                print(f"Failed to send message: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending Telegram message: {str(e)}")
            return False
    
    def format_meter_data(self, data):
        if not data:
            return "❌ Failed to retrieve electricity meter data"
        
        status_emoji = "✅" if data.get('status') == 'success' else "❌"
        
        # Format remaining balance with status indicator
        balance = data.get('remaining_balance', 'N/A')
        balance_emoji = "💰"
        
        if balance != 'N/A' and balance != 'Error':
            try:
                balance_num = float(balance.replace('BDT', '').replace(',', '').strip())
                if balance_num < 100:
                    balance_emoji = "🚨"  # Critical
                elif balance_num < 500:
                    balance_emoji = "⚠️"   # Warning
            except:
                pass
        
        message = f"""
{status_emoji} <b>Electricity Meter Report</b>
📅 <b>Date:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}

{balance_emoji} <b>Remaining Balance:</b> {balance}
⏰ <b>Last Reading:</b> {data.get('reading_time', 'N/A')}

💳 <b>Last Recharge:</b> {data.get('last_recharge_amount', 'N/A')}
📆 <b>Recharge Date:</b> {data.get('last_recharge_date', 'N/A')}

🏠 <b>Account:</b> {data.get('account_number', 'N/A')}
🔄 <b>Updated:</b> {data.get('timestamp', 'N/A')}
"""
        
        # Add low balance warning
        if balance_emoji == "🚨":
            message += "\n⚠️ <b>WARNING: Low balance detected!</b>"
        elif balance_emoji == "⚠️":
            message += "\n💡 <b>Consider recharging soon</b>"
        
        return message.strip()
    
    def send_meter_data(self, data_file_path='data.json'):
        try:
            with open(data_file_path, 'r') as f:
                data = json.load(f)
            
            message = self.format_meter_data(data)
            return self.send_message(message)
            
        except FileNotFoundError:
            error_msg = "❌ No meter data found. Scraper may have failed."
            return self.send_message(error_msg)
        except Exception as e:
            error_msg = f"❌ Error reading meter data: {str(e)}"
            return self.send_message(error_msg)
    
    def send_low_balance_warnings(self, warnings):
        """Send low balance warnings for multiple meters"""
        try:
            if not warnings:
                return True  # No warnings to send
            
            # Create warning message
            message = f"🚨 <b>LOW BALANCE WARNING</b>\n"
            message += f"📅 <b>Date:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n\n"
            
            # Add each warning
            for warning in warnings:
                account = warning['account_number']
                balance = warning['balance_numeric']
                message += f"❌ <b>Meter {account}:</b> {balance:.2f} BDT\n"
            
            # Add summary
            total_meters = 5
            low_balance_count = len(warnings)
            sufficient_count = total_meters - low_balance_count
            
            if sufficient_count > 0:
                message += f"\n✅ <b>{sufficient_count} other meter(s) have sufficient balance</b>\n"
            
            message += f"🔄 <b>Updated:</b> {warnings[0]['timestamp']}"
            
            return self.send_message(message)
            
        except Exception as e:
            error_msg = f"❌ Error sending low balance warnings: {str(e)}"
            return self.send_message(error_msg)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.send_meter_data()