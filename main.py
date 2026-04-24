# importing required modules
import requests
import csv
import asyncio
from telegram import Bot
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from Botinfo import bot_api,username


#Function that reads the daraz link and stores json data as "data".The function returns all the item objects in that page in a JSON format
def ReadJSONAPI() -> list:
 try:
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
 except:
     print("Reading Error")
     return []
 
#opens prices.csv and re writes the new data everytime its called 
def Writing_in_CSV(products):

        with open("prices.csv", "a", newline="", encoding="utf-8") as csvfile:
         fieldnames = ["name", "price"]
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
         for product in products:
            writer.writerow({
                "price": product["price"]
            })

#returns the prices of all the items as a list like[55,660,100,.....]
def loading_past_prices()->list:
 try:
    with open("prices.csv","r") as csvfile:
        File=csv.reader(csvfile)
        past_data=[]
        for line in File:
            past_data.append(line[1])
        return past_data
 except:
     print("loading error")
     return []

#uses loading_past_prices and ReadJsonAPI to get last checked price and current price and returns string respective to what happend
def compair_prices()->list:
 
    Pprices=loading_past_prices()
    Data=ReadJSONAPI()
    Nprices=[]
    Name=[]
    for data in Data[0]:
        Nprices.append(data["price"])
        Name.append(data["name"])
    i=0 
    for Pprice in Pprices:
        
        if Pprice=="price":
           continue
           
        
        if int(Pprice)-int(Nprices[i])>0:
            Writing_in_CSV(Data[0])
            return["+",abs(int(Pprice)-int(Nprices[i])),Name[i]]
            
        i+=1
    return [0,"null","null"]    
 

#A function where it takes message and send that message to a user in the telegram bot
async def send_telegram_message(message):
 
    bot = Bot(token=bot_api)
    await bot.send_message(chat_id=6282583953, text=message)
 
 
#Calls the send_telegram_message function if compair_prices returns "+"
def send_msg():
    result=compair_prices()
    if result[0]=="+":

        asyncio.run(send_telegram_message(
            f"🚨 Price Drop!! of {result[2]} by {result[1]}"
        ))
        print("Alert sent!")
    else:
        asyncio.run(send_telegram_message(
            "No drop yet"
        ))
        print("No drop yet.")


# executing the program
send_msg()

