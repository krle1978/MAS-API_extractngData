import requests
from bs4 import BeautifulSoup as BS
import re

class APIMethods:
    def __init__(self, response) -> None:
        self.resp = response
    
    def choose_busDirection(self, choose):
        soup = BS(self.resp.text, 'html.parser')
        #print(soup.prettify())
        directions = ''
        match choose:
            case 1:
                directions = soup.find_all("option")
            case 2:
                directions = soup.find_all("option")
            case 3:
                directions = soup.find_all("option")
                timetable = []
                keys = []
                values = []
                i = 1
                th_tags = soup.select("tbody tr th")
                for th_key in th_tags:
                    print(f"key[{i}]: {th_key.text}")
                    keys.append(th_key.text.strip("\t"))
                    i += 1
                tr_tags = soup.select("tbody tr")
                for i in range(1,len(tr_tags)):
                    value_lokal = []
                    print(f"value:\n {tr_tags[i].children}")
                    for child in tr_tags[i].children:
                        if child.text != '\n':
                            value_lokal.append(child.text.strip())
                    values.append(value_lokal)
                print()
                for j in range(len(values)):
                    timetable_lokal = []
                    for i in range(len(keys)):
                        timetable_lokal.append({keys[i]:values[j][i]})
                    timetable.append(timetable_lokal)
                    print(f"Dictionary has {len(timetable)} elements.")
                print()
                for dict in timetable:
                    print(f"dictinary: {dict}")
                return timetable
        for direction in directions:
            print(f"value: {direction['value']} \tText: {direction.text}")
        bus_choice = input("Choose Your bus direction: ")
        my_directions = []
        for direction in directions:
            output = re.search(str(bus_choice).upper(), direction.text)
            if output != None:
                my_directions.append([direction['value'], direction.text])
        if len(my_directions) == 1:
            return my_directions[0][0]
        else:
            print("Choose a number: ")
            print("value \t Bus line")
            for direction in my_directions:
                print(f"{direction[0]} \t {direction[1]}")
            choose = input("Your Choice: ")
            return choose
        
    def time_table(self,choose_type):
        soup = BS(self.resp.text, 'html.parser')
        #print(soup.prettify())
        timetable = []
        keys = []
        values = []
        i = 1
        match choose_type:
            case 1:
                th_tags = soup.select("tr th")
                td_tags = soup.select("tr td")
            case 2:
                th_tags = soup.select("table th")
                td_tags = soup.select("table td")

        for th_key in th_tags:
            print(f"key[{i}]: {th_key.text}")
            keys.append(th_key.text.strip("\t"))
            i += 1
        i = 1
        for tag in td_tags:
            print(f"value[{i}]: {tag.text.strip()}")
            values.append(tag.text.strip())
            i += 1
        print()
        index=0
        for i in range(0,len(keys)):
            timetable.append({keys[i]:values[i]})
            index = i + 1
        if len(keys) < len(values):
            timetable.append({'commentar':values[index]})
        print(f"Dictionary has {len(timetable)} elements.")
        print()
        for dict in timetable:
            print(f"dictinary: {dict}")
        return timetable
    
    def get_datum(self):
        soup = BS(self.resp.text, 'html.parser')
        select_tags = soup.find("select", {"id":"vaziod"})
        datum = select_tags.select("option")
        print()
        print(f"option tag:\n {datum}")
        datum_tag = datum[0].text.strip()
        day = datum_tag.split('.')[0]
        mont = datum_tag.split('.')[1]
        year = datum_tag.split('.')[2]
        datum_return = f"{year}-{mont}-{day}"
        return datum_return