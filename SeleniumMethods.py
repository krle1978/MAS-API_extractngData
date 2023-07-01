from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser
import requests
import re
from bs4 import BeautifulSoup
import os

os.system('cls')

class SeleniumTestingPage:
    def __init__(self, html_code):
        self.html_code = html_code
    
    def Get_BeutifulSoup(self):
        req = requests.get(self.html_code).text
        soup = BeautifulSoup(req, 'lxml')
        return soup
    
    def reading_HTML(self):
        req = requests.get(self.html_code).text
        soup = BeautifulSoup(req, 'lxml')
        print(f"New tab is:\n{soup.prettify()}")
        return soup
        
    def choose_destination(self, busLines_list):
        my_destination = input("Choose destination: ")
        my_directions = []
        my_directions_dict = {}
        for key_direct, value_direct in busLines_list.items():
            output = re.search(str(my_destination).upper(), value_direct)
            if output != None:
                my_directions_dict.update({key_direct:value_direct})
        if len(my_directions_dict) == 1:
            return my_directions_dict
        else:
            print("Choose a number: ")
            print("Key: \t Bus line")
            for key_dir, value_dir in my_directions_dict.items():
                print(f"{key_dir} \t {value_dir}")
            choose = input("Your Choice: ")
            return choose
            
    def get_BusTimeTable(self, bus_line):
        driver = webdriver.Chrome()
        driver.get(self.html_code.url)
        #print(f"Choossed City: {bus_line[0]}\nIndex: {bus_line[1]}")
        xPath_str = "//select[@name='linija[]']/option"
        line_index = 0
        for key, value in bus_line.items():
            line_index = key
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xPath_str)))
        option_select = driver.find_element(By.XPATH,f"{xPath_str}[{line_index}]")
        option_select.click()
        time.sleep(2)
        #Selenium.click():
        btn_prikaz = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        btn_prikaz.click()
        time.sleep(5)
        #BeautifulSoup4 take page source:
        soup = BeautifulSoup(driver.page_source,'lxml')
        #print(10*"----++")
        driver.close()
        #print("FINDING ELEMENTS:")
        #print(soup.prettify())
        #table_tag = soup.select("table")
        #print(f"TABLE: {table_tag}")
        tbody_tag = soup.select("tbody")
        #print(f"TBODY:\n{tbody_tag}")
        polasci = []
        if len(tbody_tag) == 0:
            table_class = soup.select("div.table-title")
            for table_tags in table_class:
                for tag in table_tags.stripped_strings:
                    #print(tag)
                    polasci.append(tag)
            return polasci
        
        timetable_dict = {}
        timetable = []
        titles = []
        keys = []
        
        i = 1
        table_title = soup.select("div.table-title h3")
        for title_tag in table_title:
            #print(f"title {i}: {title_tag}")
            titles.append(title_tag.text)
            #i += 1
        tbody_tags = soup.select("tbody")
        indexTitle = 0
        for tbody in tbody_tags:
            keys_local = []
            values = []
            i = 1
            key_th_tags = tbody.select("tr th")
            for th_key in key_th_tags:
                #print(f"key[{i}]: {th_key.text}")
                keys_local.append(th_key.text.strip("\t"))
                i += 1
            #keys.append(keys_local)
            #i = 1
            tr_values = tbody.select("tr")
            for indexx in range(1,len(tbody.select("tr"))):
                value_local = []
                for value in tr_values[indexx].stripped_strings:
                    #print(f"value[{i}]: {value}")
                    value_local.append(value)
                    #i += 1
                if len(value_local)<7:
                    value_local.append("<empty>")
                values.append(value_local)
            lenght_values = len(values)
            lenght_keys = len(keys_local)
            timetable_list = []
            for j in range(lenght_values):
                timetable_lokal = {}
                for i in range(lenght_keys):
                    timetable_lokal.update({str(keys_local[i]):values[j][i]})
                timetable_list.append(timetable_lokal)
            timetable_dict.update({titles[indexTitle]:timetable_list})
            indexTitle += 1
        return timetable_dict
