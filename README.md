# 🛒 Daraz Price Drop Alert Bot

A Python script that monitors product prices on [Daraz Nepal](https://www.daraz.com.np) and sends a Telegram notification when a price drop is detected.

---

## 📋 Features

- Fetches live product listings from Daraz via its internal JSON API
- Stores prices locally in a CSV file for historical comparison
- Detects price drops by comparing current vs. previously recorded prices
- Sends instant Telegram alerts when a drop is found

---

## 🗂️ Project Structure

```
├── main.py          # Core script
├── Botinfo.py       # Telegram bot credentials (not committed)
├── prices.csv       # Auto-generated price history log
└── README.md
```

---

## ⚙️ Requirements

- Python 3.8+
- Dependencies:

```bash
pip install requests python-telegram-bot
```

---

## 🔧 Configuration

Create a `Botinfo.py` file in the project root with your Telegram bot credentials:

```python
bot_api  = "YOUR_TELEGRAM_BOT_TOKEN"
username = "YOUR_BOT_USERNAME"
```

To get a bot token, message [@BotFather](https://t.me/BotFather) on Telegram.

You also need to update the `chat_id` in `send_telegram_message()` to your own Telegram user ID. You can find it by messaging [@userinfobot](https://t.me/userinfobot).

---

## 🚀 Usage

Run the script directly:

```bash
python main.py
```

The script will:
1. Fetch the current prices for pen drives listed on Daraz Nepal
2. Compare them against prices saved in `prices.csv`
3. Send a Telegram message — either a price drop alert or a "No drop yet" notice

To monitor a different product, change the search query in `ReadJSONAPI()`:

```python
url = "https://www.daraz.com.np/catalog/?ajax=true&q=YOUR_PRODUCT_HERE"
```

---

## 🔁 Automating with a Scheduler

To check prices automatically at regular intervals, you can schedule the script:

**Linux/macOS — cron (every hour):**
```bash
0 * * * * /usr/bin/python3 /path/to/main.py
```

**Windows — Task Scheduler** or use a loop with `time.sleep()` inside the script.

---

## 📦 How It Works

| Function | Description |
|---|---|
| `ReadJSONAPI()` | Fetches product listings from Daraz's catalog API |
| `Writing_in_CSV()` | Appends current prices to `prices.csv` |
| `loading_past_prices()` | Reads previously saved prices from CSV |
| `compair_prices()` | Compares old vs. new prices, returns drop info |
| `send_telegram_message()` | Sends an async message via Telegram Bot API |
| `send_msg()` | Orchestrates the full check-and-alert flow |

---

## ⚠️ Known Limitations

- Daraz may block or throttle requests over time — consider adding delays or rotating user agents
- The CSV grows indefinitely; no cleanup logic is currently implemented
- Only detects the **first** price drop found per run, then exits
- `prices.csv` must exist or be created before the first comparison works correctly

---

## 📄 License

MIT — free to use and modify.
