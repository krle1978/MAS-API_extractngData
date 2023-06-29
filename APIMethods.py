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
        if choose == 3:
            linije_tags = soup.select("select[name='linija[]']")
            print("\n'select' tags are:")
            #for tag in tags:
            #    print(f"td: {tag}\n-----\nText: {tag.stripped_strings.text.strip()}")
            #print(10*"____")
            i=1
            bus_lines = []
            for line in linije_tags:
                for option in line.stripped_strings:
                    print(f"{option}")
                    #print(f"Option[{i}]: {option}")
                    bus_lines.append([option,i])
                    i+=1
            print(f"\nCount: {len(bus_lines)}")
            print()
            #print(f"First: {bus_lines[0]}\n10: {bus_lines[9]}\n20: {bus_lines[19]}")
            print()
            return bus_lines
        else :
            directions = soup.find_all("option") 
            for direction in directions:
                print(f"{direction.text}")
                #print(f"value: {direction['value']:<10} {direction.text}")
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
        timetable = {}
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
            #print(f"key[{i}]: {th_key.text}")
            keys.append(th_key.text.strip("\t"))
            i += 1
        i = 1
        for tag in td_tags:
            #print(f"value[{i}]: {tag.text.strip()}")
            values.append(tag.text.strip())
            i += 1
        print()
        index=0
        for i in range(0,len(keys)):
            timetable.update({keys[i]:values[i]})
            index = i + 1
        if len(keys) < len(values):
            timetable.update({'commentar':values[index]})
        #print(f"Dictionary has {len(timetable)} elements.")
        print()
        return timetable
    
    def reading_TimeTable(self,timeTable):
        i = 1
        print(f"Time table is: {type(timeTable)} Type.")
        if type(timeTable) == list:
            for dictionary in timeTable:
                #print(f"[{i}]: {dictionary}")
                print(f"--- Line {i} ---")
                for key, value in dictionary.items():
                    print(f"{key: <20}:{value}")
                i += 1
        elif type(timeTable) == dict:
            print(f"--- Line: {i} ---")
            for key, value in timeTable.items():
                print(f"{key: <10}:{value}")
                i += 1
        else:
            print("No transport found !")

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