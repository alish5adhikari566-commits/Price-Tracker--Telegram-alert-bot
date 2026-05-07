import requests
import csv
import asyncio
import os
from pathlib import Path
from datetime import datetime
from telegram import Bot

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
CHAT_ID = 6282583953
CSV_FILE = "prices.csv"
DARAZ_URL = "https://www.daraz.com.np/catalog/?ajax=true&q=pendrive"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


# --- DATA FETCHING ---

def fetch_current_products() -> list[dict]:
    """Fetch current products from Daraz API. Returns list of {name, price} dicts."""
    try:
        response = requests.get(DARAZ_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["mods"]["listItems"]
    except requests.RequestException as e:
        print(f"[Network Error] {e}")
        return []
    except (KeyError, ValueError) as e:
        print(f"[Parse Error] {e}")
        return []


# --- CSV HELPERS ---


def load_csv() -> dict[str, dict]:
    """
    Load CSV into memory.
    Returns { product_name: { date: price, ... } }
    """
    if not Path(CSV_FILE).exists():
        return {}

    data = {}
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                prices = {col: row[col] for col in row if col != "name" and row[col] != ""}
                data[name] = prices
    except Exception as e:
        print(f"[CSV Read Error] {e}")
    return data


def save_csv(data: dict[str, dict]):
    """
    Save full data back to CSV.
    data = { product_name: { date: price } }
    """
    all_dates = sorted(
        set(date for prices in data.values() for date in prices.keys())
    )
    fieldnames = ["name"] + all_dates

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for name, prices in data.items():
                row = {"name": name}
                row.update(prices)
                writer.writerow(row)
    except Exception as e:
        print(f"[CSV Write Error] {e}")


def append_todays_prices(products: list[dict]) -> tuple[str, dict]:
    """Add today's prices as a new date column and return updated data."""
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_csv()

    for product in products:
        name = product["name"]
        try:
            price = int(product["price"])
        except (ValueError, KeyError):
            continue

        if name not in data:
            data[name] = {}
        data[name][today] = str(price)

    save_csv(data)
    return today, data


# --- PRICE COMPARISON ---

def find_price_drops() -> list[dict]:
    """
    Compare last 2 date columns per product.
    Returns list of drops: [{name, old_price, new_price, drop, old_date, new_date}]
    """
    current_products = fetch_current_products()
    if not current_products:
        return []

    _today, data = append_todays_prices(current_products)

    drops = []
    for name, prices in data.items():
        dates = sorted(prices.keys())

        # Need at least 2 dates to compare
        if len(dates) < 2:
            continue

        old_date, new_date = dates[-2], dates[-1]

        try:
            old_price = int(prices[old_date])
            new_price = int(prices[new_date])
        except ValueError:
            continue

        if new_price < old_price:
            drops.append({
                "name": name,
                "old_price": old_price,
                "new_price": new_price,
                "drop": old_price - new_price,
                "old_date": old_date,
                "new_date": new_date,
            })

    return drops


# --- TELEGRAM ---

async def send_message(text: str):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")


def build_alert_message(drops: list[dict]) -> str:
    if not drops:
        return "✅ Checked prices — no drops found."

    lines = ["🚨 *Price Drops Detected!*\n"]
    for d in drops:
        lines.append(
            f"🔻 *{d['name'][:60]}*\n"
            f"   `{d['old_date']}` Rs {d['old_price']} → "
            f"`{d['new_date']}` Rs {d['new_price']}  (saved Rs {d['drop']})\n"
        )
    return "\n".join(lines)


# --- MAIN ---

def run():
    print("Checking prices...")
    drops = find_price_drops()
    message = build_alert_message(drops)
    print(message)
    asyncio.run(send_message(message))
    print("Done.")


if __name__ == "__main__":
    run()