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
    
    def ExtractingWithBS(self):
        req = requests.get(self.html_code).text
        soup = BeautifulSoup(req, 'lxml')
        destination_list = []
        body_tag = soup.find("body")
        i=1
        for child in body_tag.children:
           print(f"Child ({i}):\n {child}")
           i+=1
        print()
                
        linije_tags = soup.select("select[name='linija[]']")
        i=1
        for line in linije_tags:
            for option in line.stripped_strings:
                print(f"Option ({i}):\n {option}")
                destination_list.append(option)
                i+=1
        print(f"\nCount: {len(destination_list)}")
        print()
        print(f"First: {destination_list[0]}\n10: {destination_list[9]}\n20: {destination_list[19]}")
        print()
        return destination_list
    
    def get_destination(self,bus_lines):
        print("\nSelenium find:")
        chromeOptions = Options()
        chromeOptions.add_argument("--kiosk")
        driver = webdriver.Chrome(options=chromeOptions)
        driver.get(self.html_code)
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='linija']/option")))
        options_tags = driver.find_elements(By.XPATH,"//select[@id='linija']/option")
        linie = input("Bus Linija: ")
        for bus_line in bus_lines:
            linie_str = str(linie).upper()
            output = re.search(linie_str, bus_line[0])
            #print(f"output: {output}")
            if output != None:
                bus_line[1].click()
                print("Destination found and clicked!")
                btn_prikaz = driver.find_element(By.CSS_SELECTOR, "button[onclick='ispis_polazaka()']")
                btn_prikaz.click()
                break
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        body_text = soup.find_all("tbody tr")
        i = 0
        print(10*"---")
        for tag in body_text:
            print(f"\ntext {i}: {tag.text}")
            i+=1
        print(10*"---")
        th_tags = soup.select("tbody th")
        td_tags = soup.select("tbody tr td")
        polasci = []
        names_list = []
        vremena_polaska = []
        i = 0
        for th_tag in th_tags:
            names_list.append(th_tag.text)
            vremena_polaska.append(td_tags[i].text.strip('\n').split(' '))
            i+=1
        for i in range(len(th_tags)):
            polasci.append([names_list[i],vremena_polaska[i]])
        polasci.append(td_tags[i+1].text.strip())
        return polasci
           
    def get_selenium_List(self, choos):
        print("\nSelenium find:")
        chromeOptions = Options()
        chromeOptions.add_argument("--kiosk")
        driver = webdriver.Chrome(options=chromeOptions)
        driver.get(self.html_code)
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='linija']/option")))
        options_tags = driver.find_elements(By.XPATH,"//select[@id='linija']/option")
        for tag in options_tags:
            print(tag.text)
        linie = input("Bus Linija: ")
        for destination in options_tags:
            dest_str = str(destination.text)
            linie_str = str(linie).upper()
            output = re.search(linie_str, dest_str)
            #print(f"output: {output}")
            if output != None:
                destination.click()
                print("Destination found and clicked!")
                btn_prikaz = driver.find_element(By.CSS_SELECTOR, "button[onclick='ispis_polazaka()']")
                btn_prikaz.click()
        time.sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        print(10*"-----")
        print()
        for child in soup.tbody.children:
            print(f"\nChild:\n{child}")
        print(10*"---")
        print(f"{len(list(soup.tbody.children))} Children!")
        print(f"TBODY:\n{soup.tbody.text}")
        print(2*"-------")
        th_tags = soup.select("tbody th")
        print("\n'th' tags are:")
        for th_tag in th_tags:
            print(f"th: {th_tag.text}")
        print(f"Count:{len(th_tags)}")
        tr_tags = soup.select("tbody tr")
        print("\n'tr' tags are:")
        for tr_tag in tr_tags:
            print(f"tr: {tr_tag}")
        td_tags = soup.select("tbody tr td")
        print("\n'td' tags are:")
        for td_tag in td_tags:
            print(f"td: {td_tag}\nText: {td_tag.text.strip()}")
        print(10*"____")
        #span_tag = soup.select("tbody tr span")
        i=1
        for tag in td_tags:
            print(f"'td' tag ({i}): {tag.text.strip()}")
            i+=1
        #print("Span tags are:")
        #i=1
        #for tag in span_tag:
        #    print(f"span ({i}): {tag}")
        #    i+=1
        print(10*"---")
        polasci = []
        names_list = []
        vremena_polaska = []
        i = 0
        for th_tag in th_tags:
            names_list.append(th_tag.text)
            vremena_polaska.append(td_tags[i].text.strip('\n').split(' '))
            i+=1
        for i in range(len(th_tags)):
            polasci.append([names_list[i],vremena_polaska[i]])
        polasci.append(td_tags[i+1].text.strip())
        print()
        print("TestingPage printed:")
        print(f"names_list : {names_list}\nVremena: {vremena_polaska}")
        print()
        #polasci = [[names_list[0], vremena_polaska[0]],[names_list[1],vremena_polaska[1]],vremena_polaska[2]]
        return polasci
 
    def get_LokalBusLines_List(self):
            print("\nSelenium find:")
            chromeOptions = Options()
            chromeOptions.add_argument("--kiosk")
            driver = webdriver.Chrome(options=chromeOptions)
            driver.get(self.html_code)
            element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='linija']/option")))
            options_tags = driver.find_elements(By.XPATH,"//select[@id='linija']/option")
            bus_lines = []
            for tag in options_tags:
                print(tag.text)
                bus_lines.append(tag.text)
            return bus_lines
    
    def get_LokalBusLines_List_wintBS(self):
        driver = webdriver.Chrome()
        driver.get(self.html_code)
        print("\nBeautiful Soup found:")
        #req = requests.get(self.html_code).text
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tags = soup.select("select[id='linija']")
        print("\n'select' tags are:")
        for tag in tags:
            print(f"td: {tag}\n-----\nText: {tag.text.strip()}")
        print(10*"____")
        linije_tags = soup.select("select[id='linija']")
        i=0
        bus_lines = []
        for line in linije_tags:
            for option in line.stripped_strings:
                print(f"Option[{i}]: {option}")
                bus_lines.append([option,i])
                i+=1
        print(f"\nCount: {len(bus_lines)}")
        print()
        #print(f"First: {bus_lines[0]}\n10: {bus_lines[9]}\n20: {bus_lines[19]}")
        print()
        return bus_lines
      
    def get_InternationalBusLines_List(self):
            print("\nSelenium find:")
            chromeOptions = Options()
            chromeOptions.add_argument("--kiosk")
            driver = webdriver.Chrome(options=chromeOptions)
            driver.get(self.html_code)
            element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//select[@name='linija[]']/option")))
            options_tags = driver.find_elements(By.XPATH,"//select[@name='linija[]']/option")
            bus_lines = []
            i=0
            for tag in options_tags:
                print(f"tag[{i}]: {tag.text}")
                bus_lines.append([tag.text,i])
            return bus_lines
    
    def get_InternationalBusLines_List_withBS(self):
            print("\nBeautiful Soup found:")
            driver = webdriver.Chrome()
            driver.get(self.html_code)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            linije_tags = soup.select("select[name='linija[]']")
            i=1
            bus_lines = []
            for line in linije_tags:
                for option in line.stripped_strings:
                    print(f"Option ({i}):\n {option}")
                    bus_lines.append([option, i])
                    i+=1
            print(f"\nCount: {len(bus_lines)}")
            print()
            print(f"First: {bus_lines[0]}\n10: {bus_lines[9]}\n20: {bus_lines[19]}")
            print()
            return bus_lines

    def get_BusLines_List_withBS(self):
        driver = webdriver.Chrome()
        driver.get(self.html_code.url)
        print("\nBeautiful Soup found:")
        #req = requests.get(self.html_code).text
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        tags = soup.select("select[name='linija[]']")
        linije_tags = tags
        
        print("\n'select' tags are:")
        #for tag in tags:
        #    print(f"td: {tag}\n-----\nText: {tag.stripped_strings.text.strip()}")
        #print(10*"____")
        i=1
        bus_lines = []
        for line in linije_tags:
            for option in line.stripped_strings:
                #print(f"Option[{i}]: {option}")
                print(f"{option}")
                bus_lines.append([option,i])
                i+=1
        print(f"\nCount: {len(bus_lines)}")
        print()
        #print(f"First: {bus_lines[0]}\n10: {bus_lines[9]}\n20: {bus_lines[19]}")
        print()
        return bus_lines
    
    def choose_destination(self, busLines_list):
        for line in busLines_list:
            my_destination = input("Choose destination: ")
            for line in busLines_list:
                if my_destination == line[0]:
                    return line
                
    def get_BusTimeTable(self, bus_line):
        driver = webdriver.Chrome()
        driver.get(self.html_code.url)
        #print(f"Choossed City: {bus_line[0]}\nIndex: {bus_line[1]}")
        xPath_str = "//select[@name='linija[]']/option"
        
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xPath_str)))
        option_select = driver.find_element(By.XPATH,f"{xPath_str}[{bus_line[1]}]")
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

        
    def reading_TimeTable(self, timeTable):
        i = 1
        if len(timeTable) > 3:
            for table in timeTable:
                #print(table)
                print(f"Line {i}:")
                for dict in table:
                    print(dict)
                i += 1
        else:
            for dict in timeTable:
                print(dict)