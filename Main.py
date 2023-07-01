import re
from bs4 import BeautifulSoup as BS
from datetime import timedelta
from APIMethods import APIMethods as API
from colorama import Back, Fore, Style
import webbrowser
import json
import pandas
import requests
from datetime import datetime
from SeleniumMethods import SeleniumTestingPage as STP

import os
os.system('cls')
print(Style.RESET_ALL)
#url = "http://www.gspns.co.rs/red-voznje-medjumesni"
#df = pandas.read_json(url)
#print(df)

today = datetime.today()
year = today.year
date = today.date()
yesturday = today - timedelta(days=1)
#print(f"today: {today}")
#print(f"date: {date}")
#print(f"Yesturday: {yesturday.date()}")
print("Choose Your Type of transport:\n1. Gradski\n2. Prigradski\n3. Medjunarodni")
choose_type = int(input("Transport type: "))
if choose_type !=3:
    response = requests.get("http://www.gspns.co.rs/red-voznje/prigradski")
    apiTest = API(response)
    datum = apiTest.get_datum()
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
    testing = STP(response)
    apiTest = API(response)
    busLines_list = apiTest.get_BusLines_List_withBS()
    destination_choose = testing.choose_destination(busLines_list)
    os.system('cls')
    polasci = testing.get_BusTimeTable(destination_choose)
    os.system('cls')
    apiTest.reading_TimeTableWithTitle(polasci)
else:
    apiTest = API(response)
    value = apiTest.choose_busDirection(choose_type)
    match choose_type:
        case 1:
            response = requests.get(f"http://www.gspns.co.rs/red-voznje/ispis-polazaka?rv=rvg&vaziod={datum}&dan={dayWeek.upper()}&linija%5B%5D={value}")
        case 2:
            response = requests.get(f"http://www.gspns.co.rs/red-voznje/ispis-polazaka?rv=rvp&vaziod={datum}&dan={dayWeek.upper()}&linija%5B%5D={value}")
    apiTest = API(response)
    timeTable = apiTest.get_timeTable_WithTitle(choose_type)
    os.system('cls')
    apiTest.reading_TimeTableWithTitle(timeTable)