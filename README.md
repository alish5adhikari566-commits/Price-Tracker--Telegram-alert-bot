 Daraz Price Drop Alert Bot
   A Python script that monitors product prices on Daraz Nepal and sends a Telegram notification when a price drop is         detected.

 
Features
 1)Fetches live product listings from Daraz via its internal JSON API
 2)Stores prices locally in a CSV file for historical comparison
 3)Detects price drops by comparing current vs. previously recorded prices
 4)Sends instant Telegram alerts when a drop is found


Project Structure
├── main.py          # Core script
├── Botinfo.py       # Telegram bot credentials (not committed)
├── prices.csv       # Auto-generated price history log
└── README.md

Requirements
 Python 3.8+
 Dependencies:

bashpip install requests python-telegram-bot

Configuration
Create a Botinfo.py file in the project root with your Telegram bot credentials:
	pythonbot_api  = "YOUR_TELEGRAM_BOT_TOKEN"
	username = "YOUR_BOT_USERNAME"

To get a bot token, message @BotFather on Telegram.
You also need to update the chat_id in send_telegram_message() to your own Telegram user ID. You can find it by messaging @userinfobot.

Usage
 Run the script directly:
 bashpython main.py
 The script will:
	1)Fetch the current prices for pen drives listed on Daraz Nepal
	2)Compare them against prices saved in prices.csv
	3)Send a Telegram message — either a price drop alert or a "No drop yet" notice

To monitor a different product, change the search query in ReadJSONAPI():
pythonurl = "https://www.daraz.com.np/catalog/?ajax=true&q=YOUR_PRODUCT_HERE"


How It Works

FunctionDescriptionReadJSONAPI()Fetches product listings from Daraz's catalog APIWriting_in_CSV()Appends current prices to prices.csvloading_past_prices()Reads previously saved prices from CSVcompair_prices()Compares old vs. new prices, returns drop infosend_telegram_message()Sends an async message via Telegram Bot APIsend_msg()Orchestrates the full check-and-alert flow

Known Limitations

	1)Daraz may block or throttle requests over time — consider adding delays or rotating user agents
	2)The CSV grows indefinitely; no cleanup logic is currently implemented
 	3)Only detects the first price drop found per run, then exits
	4)prices.csv must exist or be created before the first comparison works correctly


License
	MIT — free to use and modify.
