import csv
from car import cars, get_damage, best_choice, decision, create, delet, day, record_data
from GRAPH import graph
import time
import threading
import random
import keyboard
import os



systam_map = ["O", "A", "B", "C"]

#-1 代表維修區,當設備發生問題時會暫時移到這邊

class Node:
  def __init__(self, value, next_node=None, prev_node=None):
    self.value = value
    self.next_node = next_node
    self.prev_node = prev_node
    
  def set_next_node(self, next_node):
    self.next_node = next_node
    
  def get_next_node(self):
    return self.next_node

  def set_prev_node(self, prev_node):
    self.prev_node = prev_node
    
  def get_prev_node(self):
    return self.prev_node
  
  def get_value(self):
    return self.value


class DoublyLinkedList:
  def __init__(self):
    self.head_node = None
    self.tail_node = None
    self.dic = {}
  
  def add_to_head(self, new_value):
    new_head = Node(new_value)
    current_head = self.head_node

    if current_head != None:
      current_head.set_prev_node(new_head)
      new_head.set_next_node(current_head)

    self.head_node = new_head

    if self.tail_node == None:
      self.tail_node = new_head

  def add_to_tail(self, new_value):
    new_tail = Node(new_value)
    current_tail = self.tail_node

    if current_tail != None:
      current_tail.set_next_node(new_tail)
      new_tail.set_prev_node(current_tail)

    self.tail_node = new_tail

    if self.head_node == None:
      self.head_node = new_tail

  def remove_head(self):
    removed_head = self.head_node

    if removed_head == None:
      return None

    self.head_node = removed_head.get_next_node()

    if self.head_node != None:
      self.head_node.set_prev_node(None)

    if removed_head == self.tail_node:
      self.remove_tail()

    return removed_head.get_value()

  def remove_tail(self):
    removed_tail = self.tail_node

    if removed_tail == None:
      return None

    self.tail_node = removed_tail.get_prev_node()

    if self.tail_node != None:
      self.tail_node.set_next_node(None)

    if removed_tail == self.head_node:
      self.remove_head()

    return removed_tail.get_value()

  def remove_by_value(self, value_to_remove):
    node_to_remove = None
    current_node = self.head_node

    while current_node != None:
      if current_node.get_value() == value_to_remove:
        node_to_remove = current_node
        break

      current_node = current_node.get_next_node()

    if node_to_remove == None:
      return None

    if node_to_remove == self.head_node:
      self.remove_head()
    elif node_to_remove == self.tail_node:
      self.remove_tail()
    else:
      next_node = node_to_remove.get_next_node()
      prev_node = node_to_remove.get_prev_node()
      next_node.set_prev_node(prev_node)
      prev_node.set_next_node(next_node)

    return node_to_remove

  def stringify_list(self):
    string_list = ""
    current_node = self.head_node
    print("\nHere is the system map !\n[next_station, maintenance_stat]")
    while current_node:       
      print_list = self.dic[current_node.get_value()]
      string_list += str(current_node.get_value()) + "\n[{} {}]".format(print_list[0], print_list[1]) + "\n"
      current_node = current_node.get_next_node()      
    return string_list
  
  def get_next_list(self, current_station, mainten=None):
    current_node = self.head_node
    next_list  = []     
    while current_node :
      if current_node.get_value() ==  current_station:
        break  
      current_node = current_node.get_next_node()
    
    cn = current_node.get_next_node()
    if cn is None:
      cn = self.head_node
      
    if current_station == self.head_node:
      self.dic[current_node.get_value()] = cn.get_value(), None
      
    else:
      self.dic[current_node.get_value()] = cn.get_value(), mainten

g_n = None
g_l = "O"
g_m = 1  
g_d = 0
paused = False
r_mode = False
can_not_choose = []




      
      
S_map = DoublyLinkedList()
S_map.add_to_head("C")
S_map.add_to_head("B")
S_map.add_to_head("A")
S_map.add_to_head("O")
S_map.get_next_list("O")
S_map.get_next_list("A", "A_1")
S_map.get_next_list("B", "B_1")
S_map.get_next_list("C", "C_1")
#print(S_map.stringify_list())
def print_dots(num_dots, interval=1):
    for _ in range(num_dots):
        print(".", end=" ", flush=True)
        time.sleep(interval)
num_dots = 3
#print_dots(num_dots)





def system ():  
  global g_n, g_l, g_m, g_d, paused, r_mode
  can_not_choose = []
  ne = "exist_cars.csv"
  if r_mode is True:
    with open("record.csv", "r", newline="") as rc:
      reader = csv.DictReader(rc)
      rl = list(reader)
    
    for i in rl:
      print ("day : {}    Location : {}    Mission : {}    Excute_car : {}\n"
             .format(i["day"], i["Location"], i["Mission"], i["Excute_car"]))
    while True:
      choose_day = str(input("\nWhich data would you like to choose? :\n"))
      match = False
      for value in rl:
        if choose_day != value["day"]:
          continue
        else:
          match = True
          break
      if match is True:
        break
      else:
        print ("There is no data match the day you input ! \n")
        

    for i in rl:
      if i["day"] == choose_day:
        current_location = i["Location"]
        choose_car = i["Excute_car"]
        mission = int(i["Mission"])
        dis = int(i["distance"])
        if choose_car == "r":
          best = best_choice(lo=current_location, distance=dis, mode=False)
          if type(best) == list:
              print("\nAll car are in the same condition\nYou can choose anyone\n")
              
          elif best is None:
            print("\nThere are no cars available !!")
            choose_car = decision(l=current_location, d=dis, rl=current_location, rm=mission, rc=choose_car)
          else:
            choose_car = best
    
    R_car = cars(choose_car)
    next_map = S_map.dic[current_location]
    car_damage = R_car.get_car_damage()
    car_state = R_car.get_car_state()  
    ready = True

    print("\nContinue record mission\n")
    time.sleep(1)
    print_dots(3, 1)
    
    
  else:   
    if r_mode is False: 
      print("\nwhich car would you choose to execute this task ?\n")
      with open (ne, "r", newline = "") as ex:
        reader = csv.DictReader(ex)
        listex = list(reader)
      for row in listex:
        car_name = row['car\'s name']
        if row["state"] == "OFF":
          print("{} is not ready".format(car_name))
          can_not_choose.append(row["car\'s name"])
        else:
          print("name : {}".format(car_name))  
      #打印所有的車輛，如果state是off那會顯示他還沒準備好
      
      best_car = best_choice(lo="O")
      best = True 
      
      while True: 
        if type(best_car) == list:
          print("\nAll car are in the same condition\nYou can choose anyone\n")
          
        elif best_car is None:
          print("\nThere are no cars available !!")
          best = False
          break
              
        else:
          print ("\nWe suggest {} excute this task\n".format(best_car))
        # 找到成功率最高的車輛
          while True:     
            choose_car = input("input car's name : \n")
            if not any(n["car\'s name"] == choose_car for n in listex):
              print("\nThere is no car you are looking for")
            elif choose_car in can_not_choose:
              print("plz choose another one")
            else:
              print("You choosed {}".format(choose_car))
              break
          break
            
      if best is False:
        choose_car = decision()
        if choose_car == "exit":
          create(choose_car)
          print("\nStart")
          time.sleep(1)
          print_dots(3, 1)
        else:
          print("\nStart")
          time.sleep(1)
          print_dots(3, 1)
      else:
        print("\nStart")
        time.sleep(1)
        print_dots(3, 1)
          
      
    R_car = cars(choose_car)
    current_location = S_map.head_node.get_value()
    next_map = S_map.dic[current_location]
    car_damage = R_car.get_car_damage()
    car_state = R_car.get_car_state()  
    mission = 1
    ready = True
    R_car.set_next_and_distance(current_location, next_l=next_map[1], mode=True)
  
  while True:
    g_n = R_car.name
    g_l = current_location
    g_m = mission   
    while paused:
      pass
    
    if R_car.name == "exit":
      print_dots(3, 1)
      print("\nbye")
      delet(R_car.name, False)
      day("all")
      os._exit(0)
        
    elif car_state == "ON" and car_damage > 0 :
      R_car.get_distance(current_location, already=ready) 
      R_car.locat(current_location)
      distance = R_car.get_to_o_dis()
      g_d = distance
      

      now_mission = "\nLocation : {}  To O distance: {}  Mission 10/{}   Excutor : {}  mission".format(current_location, distance, mission, R_car.name)
      result = random.randint(0, car_damage)       
      ready = False
      #模擬用
      if result <= 1:
        print(now_mission + " : fail")
        time.sleep(1)          
        R_car.c_damage()
        car_damage = R_car.get_car_damage()
        
      else:
        print(now_mission + " : complete")
        time.sleep(1)
      mission += 1
      
      if mission == 11:          
        current_location = next_map[0]         
        next_map = S_map.dic[current_location]
        #print(next_map)
        R_car.set_next_and_distance(current_location, next_l=next_map[0])
        
        print("Switch to the {} ....\n".format(current_location))
        
        time.sleep(1)
        print_dots(3, 1)
        mission = 1
        ready = True 
        
      #進到下個地點
      
      if car_damage <= 0:
        R_car.d_zero()       
        R_car.need_to_fix()
        next_map = S_map.dic[current_location]      
        #print(next_map)    
        R_car.set_next_and_distance(current_location, next_l=next_map[0], mode=False)
  
        fix_location = next_map[1]
        
        R_car.locat(fix_location)
        time.sleep(1)         
        
        origin_car = R_car.name
        R_car.get_distance(current_location, already=True, mode=True) 
        new_car = R_car.switch_car(current_location, distance)
        
        print("\n{} has been moved to the maintenance area, and {} will take over the task.".format(origin_car, new_car))
        car_damage = R_car.get_car_damage()
        R_car.set_next_and_distance(current_location, next_l=next_map[0], mode=False)
        print_dots(3, 1)

        if R_car.name is None:
          print("\nThere are no cars available !!\n")
          current_name = decision(current_location, rl=current_location, rm=mission, rc=R_car.name)
          R_car.name = current_name
          if current_name == "exit":
            create(R_car.name)
          car_damage = R_car.get_car_damage()
          car_state = R_car.get_car_state()                      
                    
                 
    else:
      if R_car.name is None or R_car.name == "r":
        print("\nThere are no cars available !!\n")
        R_car.name = decision(current_location, rl=current_location, rm=mission, rc=R_car.name)
        
      elif R_car.state == "OFF":
          origin_car = R_car.name
          distance = R_car.To_O_distance
          new_car = R_car.switch_car(current_location, distance)          
          print("\n{} has been moved to the maintenance area, and {} will take over the task.".format(origin_car, new_car))
          car_damage = R_car.get_car_damage()
          car_state = R_car.get_car_state()  
              
      
    #print(str(current_location))
    #print(str(next_map))

def system_main(mode=False):
  global g_n, g_l, g_m, g_d, paused, r_mode
  if mode is True:
    r_mode = True
  thread1 = threading.Thread(target=system)
  thread1.start()

  while True:
    if keyboard.is_pressed('esc'):
      paused = not paused
      stop_system (g_l, g_m, g_n, g_d)
      paused = not paused
      



def stop_system (location, mission, excute_car="r", d=0):
  global pasued
  while True:
    ans = input("\nWould you like to exit ? input Y for Yes, N for No \n").upper()
    if ans == "Y" :
      while True:
        ans2 = input("\nWould you like to record ? input Y for Yes, N for No \n").upper()
        if ans2 == "Y" :
          record_data(location, mission, excute_car, d)
          os._exit(0)
        elif ans2 == "N":
          os._exit(0)
        else:
          print("Please input Y or N")
    elif ans == "N":
     break
    


#system_main()