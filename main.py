import requests
import csv
import asyncio
from telegram import Bot
from Botinfo import bot_api,username
def ReadJSONAPI() -> list:
    url = "https://www.daraz.com.np/catalog/?ajax=true&q=pendrive"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers)

    try:
        data = r.json()
    except Exception:
        print("Response is not JSON. Blocking or HTML received.")
        return []

    return [data["mods"]["listItems"]]
    

def Writing_in_CSV(products):
        with open("prices.csv", "w", newline="", encoding="utf-8") as csvfile:
         fieldnames = ["name", "price"]
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
         writer.writeheader()

         for product in products:
            writer.writerow({
                "name": product["name"],
                "price": product["price"]
            })
def loading_past_prices():
    with open("prices.csv","r") as csvfile:
        File=csv.reader(csvfile)
        past_data=[]
        for line in File:
            past_data.append(line[1])
        return past_data
    
def compair_prices():
    Pprices=loading_past_prices()
    Data=ReadJSONAPI()
    Nprices=[]
    for data in Data:
        Nprices.append(data["price"])
    i=0
    for Pprice in Pprices:
        i+=1
        if Pprice-Nprices[i]==0:
            return("same price")
        
        elif Pprice-Nprices[i]>0:
            Writing_in_CSV(Data)
            return"PRICE DROP!!"
            
        elif Pprice-Nprices[i]<0:
             Writing_in_CSV(Data)
             return"price increase"
        
        else:
            return
        




async def send_telegram_message(message):
    bot = Bot(token=bot_api)
    await bot.send_message(chat_id=username, text=message)

def send_msg():
    result=compair_prices()
    if result=="PRICE DROP!!":

        asyncio.run(send_telegram_message(
            "🚨 Price Drop!!!!!!!!!"
        ))
        print("Alert sent!")
    else:
        print("No drop yet.")

