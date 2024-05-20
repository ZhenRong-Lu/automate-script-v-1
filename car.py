import csv
import json
from GRAPH import graph, neighbor
import time
from datetime import datetime

exist = "exist_cars.csv"
def print_dots(num_dots, interval=1):
    for _ in range(num_dots):
        print(".", end=" ", flush=True)
        time.sleep(interval)

def get_damage (n):
    add = cars(n)
    return add.get_car_damage()

def best_choice(lo="O", distance=0, mode=False):
    with open (exist, "r", newline = "") as ex:
        reader = csv.DictReader(ex)
        listex = list(reader)                 
    car_name = None
    equal = {}
    o_equal = {}   
    count = 0
    current_d = 0   
    for i in listex:                    
        if mode is False:
            if i["state"] == "ON":
                if lo in neighbor[i["location"]] or lo == i["location"]:
                    #print(i['car\'s name'])
                    equal[i['car\'s name']] = i['distance to origin']
                else:
                    o_equal[i['car\'s name']] = i['distance to origin']
        else:
            if mode is True:
                equal[i['car\'s name']] = i['distance to origin']
    #print(equal)
    if len(equal) == 0 and len(o_equal) == 0:
        return None   
    else:        
        if len(equal) > 0 and len(equal) != 0:
            if len(equal) == 1:
                first = next(iter(equal))
                car_name = first
                return car_name  
            else:
                for key, value in equal.items():              
                    if car_name is None:
                        car_name = key
                        current_d = int(value)          
                    elif distance - int(value) > distance - current_d:
                        car_name = key
                    elif distance - int(value) == distance - current_d:
                        if get_damage(key) > get_damage(car_name):
                            count += 1
                            car_name = key
                        else:
                            continue
                    else:
                        continue
                if len(equal) == count:
                    return listex
                return car_name           
        else:                      
            for key, value in o_equal.items():              
                if car_name is None:
                    car_name = key
                    current_d = int(value)          
                elif distance - int(value) > distance - current_d:
                    car_name = key
                elif distance - int(value) == distance - current_d:
                    if get_damage(key) > get_damage(car_name):
                        count += 1
                        car_name = key
                    else:
                        continue
                else:
                    continue
            if len(o_equal) == count:
                return listex
            return car_name

def decision(l="O", d=0, rl="", rm="", rc=""):
    car = cars("")
    while True:
        decision = input("If you want to exit input 'e', fix input 'f' :\n").upper()
        if decision == "E":
            while True:
                decision= input("\nWould you like to save the record?\nInput 'y' for yes, 'n' for no\n").upper()
                if decision == "Y":
                    record_data(rl, rm, rc, d)
                    break
                elif decision == "N":
                    break
                else:
                    print("please input y or n")                
            car.name = "exit"
            return "exit"
        elif decision == "F":
            car_name = car.finish_fix(l, d)
            return car_name      
        else:
            list = ["Y", "N", "F", "E"]
            if decision not in list:
                print("please imput e or f")           
            

class cars:
    def __init__ (self, car):
        self.name = car
        self.state = "ON"
        self.damage = 10
        self.location = "O"
        self.To_O_distance = 0
        self.next = None
        self.next_distance = 100
        
    def get_car_damage (self):
        exist = "exist_cars.csv"
        with open (exist, "r", newline = "") as ex:
            reader = csv.DictReader(ex)
            for i in reader:
                if i['car\'s name'] == self.name:
                    self.damage = int(i['damage'])
                    return self.damage 
                
    def c_damage(self):
        self.damage -= 1
        with open (exist, "r", newline = "") as ex:
            reader = csv.DictReader(ex)
            rows = list(reader)
            
        with open (exist, "w", newline = "") as ex:
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(ex, fieldnames = fieldnames)  
            writer.writeheader()
                      
            for i in rows:
                if i['car\'s name'] == self.name:
                    i['damage'] = self.damage
                writer.writerow(i)
               
    def d_zero(self):   
        with open (exist, "r", newline = "") as ex:
            Reader = csv.DictReader(ex)
            rows = list(Reader)
            
        with open (exist, "w", newline = "") as ex:
            Reader = csv.DictReader(ex)
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(ex, fieldnames = fieldnames)  
            writer.writeheader()                      
            for i in rows:
                if i['car\'s name'] == self.name:
                    i['damage'] = 0
                writer.writerow(i)
                    
    def get_car_state(self):
        exist = "exist_cars.csv"
        with open (exist, "r", newline = "") as ex:
            reader = csv.DictReader(ex)
            for i in reader:
                if i['car\'s name'] == self.name:
                    self.state = i['state']
                    return i['state']
                
    def need_to_fix(self):        
        self.state = "OFF"
        with open (exist, "r", newline = "") as ex:
            reader = csv.DictReader(ex)
            rows = list(reader)
            
        with open (exist, "w", newline = "") as ex:
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(ex, fieldnames = fieldnames)  
            writer.writeheader()
                      
            for i in rows:
                if i['car\'s name'] == self.name:
                   i['state'] = self.state
                writer.writerow(i)
            
    def finish_fix(self, location='O', distance=0):
        with open (exist, "r", newline = "") as ex:
            reader = csv.DictReader(ex)
            rows = list(reader)      
                    
            for row in rows:
                print(row['car\'s name'])                            
            best_car = best_choice(location, distance, mode=True)       
            
            if type(best_car) == list:
                print("\nAll car are in the same condition\nYou can choose anyone\n")
            else:
                print("\nWe suggest {}".format(best_car))
            time.sleep(1)  
            
            while True:
                fix_car = input("\nwhich car you want to fix?\n") 
                car_names = [i["car's name"] for i in rows]  
                if fix_car in car_names or fix_car == "all":
                    break
                else:
                    print("\nThere's no car with the name you inputted.")
            
            with open (exist, "w", newline = "") as ex:
                fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
                writer = csv.DictWriter(ex, fieldnames=fieldnames)
                writer.writeheader()  
                for i in rows:                     
                    if i['car\'s name'] == fix_car or fix_car == "all":
                        i['damage'] = 10
                        i['state'] = "ON"
                        if int(i['distance to origin']) != 0:
                             i['distance to origin'] = int(i['distance to origin']) - 20  
                        else :
                             i['distance to origin'] = 0                                      
                        self.state = i['state']
                        self.To_O_distance =  int(i["distance to origin"] ) 
                        self.name = i['car\'s name']                                                
                    writer.writerow(i)           
               
        day(fix_car)                       
        print("\nFixing\n")
        print_dots(3, 1)       
        return self.name

    def switch_car(self, lo="O", distance=0,):
        car_name = best_choice(lo, distance)
        if type(car_name) == list:
            self.name = car_name[0]
            return car_name
        elif car_name is None:
            self.name = car_name
            return None
        else:
            self.name = car_name
            return self.name

    def get_distance (self, loca, already=True, mode=False):
        self.location = loca
        dis = self.To_O_distance                
        keys = list(key for key in graph[loca])
        
        if already is True:
            if len(keys) <= 1:
                dis = 0
                self.To_O_distance = dis
            else:
                if mode is True:
                    key = keys[0]           
                    first = graph[loca][key]
                    dis += first
                    self.To_O_distance = dis
                    self.get_to_o_dis()
                    dis -= first
                    self.To_O_distance = dis
                else:
                    key = keys[1]           
                    first = graph[loca][key]
                    dis += first
                    self.To_O_distance = dis
        
            
    def get_to_o_dis(self):
        with open (exist, "r", newline = "") as gd:
            reader = csv.DictReader(gd)
            rows = list(reader)
        with open (exist, "w", newline = "") as gd:
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(gd, fieldnames = fieldnames)
            writer.writeheader()
                      
            for r in rows:
                if r['car\'s name'] == self.name:
                    r['distance to origin'] = self.To_O_distance
                writer.writerow(r)
            
        return self.To_O_distance
   
    def set_next_and_distance (self, loca, next_l=None, mode=False):
        for k in graph[loca]:
            if mode is True:
                self.next = loca
                self.next_distance = 0            
            else:
                if k == next_l:
                    self.next = k
                    self.next_distance = graph[loca][k]
                
        with open (exist, "r", newline = "") as ex:
            Reader = csv.DictReader(ex)
            rows = list(Reader)
                        
        with open (exist, "w", newline = "") as ex:
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(ex, fieldnames = fieldnames)  
            writer.writeheader()                      
            for i in rows:
                if i['car\'s name'] == self.name:
                    i['next\'s distance'] = "TO {} : {}".format(self.next, self.next_distance)
                writer.writerow(i)
    
    def locat (self, location):
        with open (exist, "r", newline = "") as gd:
            reader = csv.DictReader(gd)
            rows = list(reader)
        with open (exist, "w", newline = "") as gd:
            fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
            writer = csv.DictWriter(gd, fieldnames = fieldnames)
            writer.writeheader()
                      
            for r in rows:
                if r['car\'s name'] == self.name:
                    if location is None:
                        location = "O"
                    r['location'] = location
                writer.writerow(r)
        self.location = location
        return self.location
        
def create(n):
    with open(exist, "r", newline = "") as ex:                
        exlist = [exi['car\'s name'] for exi in csv.DictReader(ex)]
        if n in exlist:
            print("\n{} is already in queue".format (n))
            return None                                   
        else:
            with open(exist, "a", newline = "") as ex:
                fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location", 'updated time']
                writer = csv.DictWriter(ex, fieldnames=fieldnames,  lineterminator='\n')
                writer.writerow({
                    'car\'s name': n, 
                    'distance to origin': 0, 
                    'next\'s distance': "To A : 100", 
                    'state': 'ON', 
                    'damage': '10', 
                    "location" : "O",
                    'updated time': ''
                })
def delet(n, mode=True):
    with open (exist, "r", newline = "") as ex:
        reader = csv.DictReader(ex)
        excars = list(reader)
    if not any(car['car\'s name'] == n for car in excars):
        if mode is True:
            print("\nThere is no car that you are searched for")
        return None 
    else:
        excars = [car for car in excars if car['car\'s name'] != n]
        with open (exist, "w", newline = "") as ex:
            fieldnames = excars[0].keys()
            writer = csv.DictWriter(ex, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(excars)      
def day(name):
    with open (exist, "r", newline="") as ex:
        reader = csv.DictReader(ex)
        rows = list(reader)
    for i in rows:
        if i['car\'s name'] == name or name == "all":
             i['updated time'] = datetime.now().strftime('%Y-%m-%d')
    with open (exist, "w", newline="") as ex:
        fieldnames = ['car\'s name', 'distance to origin', 'next\'s distance', 'state', 'damage', "location",'updated time']
        writer = csv.DictWriter(ex, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(rows)
        
def record_data(location, mission, excute_car="r", distance=0):
    now = datetime.now().strftime('%Y-%m-%d')
    if excute_car is None:
        excute_car = "r"
    data = {"day": now, "Location": location, "Mission": mission, "Excute_car": excute_car, "distance": distance}
    record = "record.csv"
    with open(record, "r", newline="") as ex:
        Reader = csv.DictReader(ex)
        rl = list(Reader)
        count = 1    
        for i in rl :
            while True :                
                if i["day"] == data["day"]:
                    count += 1
                    data = {"day": now + "-" + str(count), "Location": location, "Mission": mission, "Excute_car": excute_car, "distance": distance}
                else:
                    break 
    with open(record, "a", newline="") as ex:
        field =["day", "Location", "Mission", "Excute_car", "distance"]
        writer = csv.DictWriter(ex, fieldnames=field)
        writer.writerow(data)


#best = best_choice(mode=True)
#print(best)
#day("Number_2")
#r = cars("r")
#r.finish_fix()
#record_data(1, 1, 1)