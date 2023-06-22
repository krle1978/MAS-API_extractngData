import re
from bs4 import BeautifulSoup as BS
from datetime import timedelta
import APIMethods
import webbrowser
import json
import pandas
import requests
from datetime import datetime
import SeleniumMethods

import os
os.system('cls')

#url = "http://www.gspns.co.rs/red-voznje-medjumesni"
#df = pandas.read_json(url)
#print(df)

today = datetime.today()
year = today.year
date = today.date()
yesturday = today - timedelta(days=1)
print(f"today: {today}")
print(f"date: {date}")
print(f"Yesturday: {yesturday.date()}")
print("Choose Your Type of transport:\n1. Gradski\n2. Prigradski\n3. Medjunarodni")
choose_type = int(input("Transport type: "))
if choose_type !=3:
    response = requests.get("http://www.gspns.co.rs/red-voznje/prigradski")
    api = APIMethods.APIMethods(response)
    datum = api.get_datum()
    print(f"Datum: {datum}")
dayWeek = input("(R) - workday, (S) - Saturday, (N) - Sonday\nDay: ")
response = ''
match(choose_type):
    case 1:
        response = requests.get(f"http://www.gspns.co.rs/red-voznje/lista-linija?rv=rvg&vaziod={datum}&dan={dayWeek.upper()}")
    case 2:
        response = requests.get(f"http://www.gspns.co.rs/red-voznje/lista-linija?rv=rvp&vaziod={datum}&dan={dayWeek.upper()}")
    case 3:
        response = requests.get("http://www.gspns.co.rs/red-voznje-medjumesni")
if choose_type == 3:
    testing = SeleniumMethods.SeleniumTestingPage(response)
    busLines_list = testing.get_BusLines_List_withBS()
    destination_choose = testing.choose_destination(busLines_list)
    polasci = testing.get_BusTimeTable(destination_choose)
    testing.reading_TimeTable(polasci)
else:
    api = APIMethods.APIMethods(response)
    value = api.choose_busDirection(choose_type)
    match choose_type:
        case 1:
            response = requests.get(f"http://www.gspns.co.rs/red-voznje/ispis-polazaka?rv=rvg&vaziod={datum}&dan={dayWeek.upper()}&linija%5B%5D={value}")
        case 2:
            response = requests.get(f"http://www.gspns.co.rs/red-voznje/ispis-polazaka?rv=rvp&vaziod={datum}&dan={dayWeek.upper()}&linija%5B%5D={value}")
    api = APIMethods.APIMethods(response)
    api.time_table(choose_type)