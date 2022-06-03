import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from twilio.rest import Client
import requests
import schedule
import time

load_dotenv()

#Twilio authentication
ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']

CF_URL = "https://www.crossfit.com"
    
def get_and_send_wod():

    cfHomepage = requests.get(CF_URL)      ### Get raw HTML from Crossfit.com homepage

    soup = BeautifulSoup(cfHomepage.content, 'html.parser')    ### Create Beautiful Soup Object 
    results = soup.find("div", class_="_workout-of-the-day-content_18rmn_60")     ### Grab workout area div
    wod = results.find("article")       ### Remove "Workout of the day with comment count, return just the workout"


    client = Client(ACCOUNT_SID, AUTH_TOKEN)     ### Create Twilio client

    message = client.messages.create(         ### Create text message
                                body = f"Workout of the Day \n {wod.text}",
                                from_='+18312492701',
                                to='+18452421708'
                            )

    print(message.sid)

    print(f"Workout of the Day \n {wod.text}")


schedule.every().day.at("08:00").do(get_and_send_wod)   ### Call function every day @ 8am


while True:
    schedule.run_pending()
    time.sleep(1)
