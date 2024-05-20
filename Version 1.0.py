from car import cars, create, delet
import csv
import time
from system import Node, DoublyLinkedList, print_dots, system, S_map, num_dots, system_main
import os
exist = "exist_cars.csv"   
def Automated_script(shut_down=False, ans=False):
    if shut_down is True:
        if ans is False:
            print("Would you like to execute from the step where the last task was interrupted?\n")
        #提供中斷功能        
        ans = input("\ninput 'Y' for Yes 'N' for not :\n").upper()
        if ans == "Y":
            system_main (mode=True)
        elif ans == "N":
            Automated_script(False)                  
        else:
            print("\nplease add 'Y' or 'N'")
            Automated_script(shut_down=True, ans=True)
            
    elif shut_down is False:        
     
        while True:
            option = input("\nWhich funtion would you like to use? \nYou can use 'h' to see funtion detials and 'se' to see the information about cars :\n").upper()
            if option == "H":
                print ("""
                       \nSE for The names of existing cars
                       \nS for Start the system
                       \nE for Exit
                       \nC for Creat a new car
                       \nD for Delet a existing car
                       """)
                Automated_script(False)      
            elif option == "S":
                print(S_map.stringify_list())
                print_dots(num_dots)
                system_main()        
                
            elif option == "E":
                print ("goodbye")
                os._exit(0)
            
            elif option == "SE":
                with open (exist, "r", newline = "") as ex:
                    reader = csv.DictReader(ex)
                    for row in reader:
                        car_name = row['car\'s name']
                        distance_to_origin = row['distance to origin']
                        next_distance = row['next\'s distance']
                        state = row['state']
                        damage = row['damage']
                        updated_time = row['updated time']
                        location = row["location"]
                        print("""
                              \nname : {}
                              \ndistance_to_origin : {}
                              \nnext_distance : {}
                              \nstate : {}
                              \ndamage : {}
                              \nlocation : {}
                              \nupdated_time : {}"""
                              .format(car_name, distance_to_origin, next_distance, state, damage, location, updated_time))
                    
            elif option == "C":
                new_n = input("\nWhat's new car's name that will add in the team :\n")
                n = create(new_n)        
                if n is None:
                    time.sleep(1)
                    pass
                else:                       
                    print("\nAdding new car : {} ......".format(new_n))
                    time.sleep(3)
                    print("\nAddition completed")

            elif option == "D":
                de = input("\nwhich car is about to be deleted from exist_cars ? :")
                d = delet(de)
                if d is None:
                    time.sleep(1)
                    pass
                else:                            
                    print("\nDeleting car : {} ....".format(de))
                    time.sleep(3)
                    print("\nDeletion completed")
            
            else:
                print("\nplease reply s、e、se、c or d") 


       
    
Automated_script(True)