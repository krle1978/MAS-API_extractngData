import requests
from colorama import Back, Fore, Style
from bs4 import BeautifulSoup as BS
import re

class APIMethods:
    def __init__(self, response) -> None:
        self.resp = response
    
    def get_BusLines_List_withBS(self):
        soup = BS(self.resp.text, 'html.parser')
        tags = soup.select("select[name='linija[]']")
        linije_tags = tags
        i=1
        bus_lines = []
        bus_lines_dict = {}
        for line in linije_tags:
            for option in line.stripped_strings:
                #print(f"Option[{i}]: {option}")
                print(f"{option}")
                bus_lines.append([option,i])
                bus_lines_dict.update({i:option})
                i+=1
        print(f"\nCount: {len(bus_lines)}")
        print()
        #print(f"First: {bus_lines[0]}\n10: {bus_lines[9]}\n20: {bus_lines[19]}")
        print()
        return bus_lines_dict
        
       
    def choose_busDirection(self, choose):
        soup = BS(self.resp.text, 'html.parser')
        directions = ''
        directions = soup.find_all("option") 
        for direction in directions:
            print(f"{direction.text}")
            #print(f"value: {direction['value']:<10} {direction.text}")
        bus_choice = input("Choose Your bus direction: ")
        my_directions = []
        my_directions_dict = {}
        for direction in directions:
            output = re.search(str(bus_choice).upper(), direction.text)
            if output != None:
                my_directions_dict.update({direction['value'] : direction.text})
        if len(my_directions_dict) == 1:
            for key, value in my_directions_dict.items():
                return key
        else:
            print("Choose a number: ")
            print("value \t Bus line")
            for key_dir, value_dir in my_directions_dict.items():
                print(f"{key_dir} \t {value_dir}")
            choose = input("Your Choice: ")
            return choose
            
    def get_timeTable_WithTitle(self,choose_type):
        soup = BS(self.resp.text, 'html.parser')
        #print(soup.prettify())
        timetable = {}
        titles = []
        keys = []
        values = []
        i = 1
        table_title = soup.select("div.table-title")
        for title_tag in table_title:
            #print(f"title {i}: {title_tag.text.strip()}")
            titles.append(title_tag.text.strip())
        match choose_type:
            case 1:
                th_tags = soup.select("tr th")
                td_tags = soup.select("tr td")
            case 2:
                th_tags = soup.select("table th")
                td_tags = soup.select("table td")

        for th_key in th_tags:
            #print(f"key[{i}]: {th_key.text}")
            keys.append(th_key.text.strip("\t"))
            i += 1
        i = 1
        for tag in td_tags:
            #print(f"value[{i}]: {tag.text.strip()}")
            values.append(tag.text.strip())
            i += 1
        print()
        timeTable_dict = {}
        for title in titles:
            index=0
            for i in range(0,len(keys)):
                timetable.update({keys[i]:values[i]})
                index = i + 1
            if len(keys) < len(values):
                timetable.update({'commentar':values[index]})
            #print(f"Dictionary has {len(timetable)} elements.")
            timeTable_dict.update({title:timetable})
        print()
        return timeTable_dict
            
    def reading_TimeTableWithTitle(self,timeTable):
        print()
        #print(f"Time table is: {type(timeTable)} Type.")
        if type(timeTable) == list:
            i = 1
            for dictionary in timeTable:
                #print(f"[{i}]: {dictionary}")
                print(f"--- Line {i} ---")
                i += 1
                if type(dictionary) == dict:
                    for key, value in dictionary.items():
                        print(f"{key: <20}:{value}")
                elif type(dictionary) == list:
                    for element in dictionary:
                        print(f"{element}")
                else:
                    break
            for element in timeTable:
                print(element)
        elif type(timeTable) == dict:
            for key_title, value_bus in timeTable.items():
                print(f"---{Fore.YELLOW} {key_title} {Style.RESET_ALL} ---")
                print()
                #print(f"value_bus is: {type(value_bus)} type.")
                if type(value_bus) == list:
                    i = 1
                    for bus_line in value_bus:
                        print(f"--- Line: {i} ---")
                        for key_bus, value_bus in bus_line.items():
                            out = re.search('cena', key_bus.lower())
                            if out != None:
                                print(f"{key_bus:<15}: {Fore.GREEN + value_bus + Fore.RESET}")
                            else:
                                print(f"{key_bus:<15}: {value_bus}")
                        print()
                        i += 1
                elif type(value_bus) == dict:
                    for key_direction, value_time in value_bus.items():
                        if key_direction == 'commentar' and str(value_time) != '<empty>':
                            print(f"{key_direction:<15}: {Fore.GREEN}{value_time}{Style.RESET_ALL}")
                        else:
                            print(f"{Back.RED}{key_direction:<15}{Style.RESET_ALL}: {value_time}")
                        print()
                else:
                    print("No readable value. Must be a dictionary or list.")
        else:
            print("No transport found !")
        print(Style.RESET_ALL)

    def get_datum(self):
        soup = BS(self.resp.text, 'html.parser')
        select_tags = soup.find("select", {"id":"vaziod"})
        datum = select_tags.select("option")
        print()
        #print(f"option tag:\n {datum}")
        datum_tag = datum[0].text.strip()
        day = datum_tag.split('.')[0]
        mont = datum_tag.split('.')[1]
        year = datum_tag.split('.')[2]
        datum_return = f"{year}-{mont}-{day}"
        return datum_return