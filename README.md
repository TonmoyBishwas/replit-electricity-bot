# Electricity Meter Bot - Replit Edition

A clean, Replit-optimized version of the electricity meter scraper bot that automatically monitors your DESCO prepaid electricity balance and sends updates via Telegram.

## 🚀 Quick Setup on Replit

### 1. Import to Replit
- Create a new Replit project
- Import this repository from GitHub
- Replit will automatically detect Python and install dependencies

### 2. Environment Variables
Set these environment variables in Replit's "Secrets" tab:

```
ACCOUNT_NUMBER=your_meter_account_number
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
METER_WEBSITE_URL=https://prepaid.desco.org.bd/customer/#/customer-login
TEST_RUN=true
```

### 3. Run the Bot
Click the "Run" button in Replit. The bot will:
- Start with a test run if `TEST_RUN=true`
- Begin daily scheduled monitoring if `TEST_RUN=false`

## 📱 Features

- **Automated Scraping**: Logs into DESCO website and extracts meter data
- **Telegram Integration**: Sends balance updates directly to your Telegram
- **Cloud-Ready**: Optimized specifically for Replit deployment
- **Scheduled Monitoring**: Runs daily at 8 AM Bangladesh time
- **Error Handling**: Robust error handling and logging

## 🛠️ Files

- `main.py` - Entry point for Replit
- `scraper.py` - Web scraping logic (cloud-optimized)
- `scheduled_scraper.py` - Scheduling and coordination
- `telegram_bot.py` - Telegram bot integration
- `keep_alive.py` - Keeps the bot running on Replit
- `.replit` - Replit configuration (uses python3)
- `replit.nix` - System dependencies

## 🔧 How to Get Telegram Credentials

1. **Create Bot**: Message @BotFather on Telegram, use `/newbot`
2. **Get Token**: Save the bot token from BotFather
3. **Get Chat ID**: Message your bot, then visit: `https://api.telegram.org/bot<YourBotToken>/getUpdates`

## 🎯 Usage

### Test Run
Set `TEST_RUN=true` to run once and verify everything works.

### Production Mode
Set `TEST_RUN=false` to enable daily scheduled monitoring at 8 AM.

## 📝 Notes

- All file paths are cloud-optimized (no Windows-specific paths)
- Uses system chromedriver (installed via replit.nix)
- Account number can be set via environment variable for security
- Headless Chrome for cloud compatibility

This version is specifically designed for Replit with no conflicts or merge issues!