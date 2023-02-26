from classes.database_access import DB_Connect
from functions.my_functions import *

# my current db was setup with a password so change if necessary
db = DB_Connect('root', '1234', 'dealership')

ask = True

while ask:
    response = input("What would you like to do? Enter the number of the item you want:\n1. Show all vehicles\n2. Add a vehicle\n3. Edit a vehicle\n4. Remove a vehicle\n5. Exit program\n> ")

    if response == "1":
        long_list_vehicles(db)
    elif response == "2":
        vehicle = {}

        vehicle['make'] = get_input("make")
        vehicle['model'] = get_input("model")
        vehicle['vin'] = get_input("vin")
        
        previous_owner = get_input("previous_owner", False)
        if previous_owner: # only add if it was entered
            vehicle['previous_owner'] = previous_owner

        price_paid = get_input("price_paid", False)
        if price_paid: # only add if it was entered
            vehicle['price_paid'] = price_paid

        vehicle['sale_price'] = get_input("sale_price")
        vehicle['description'] = get_input("description")

        add_vehicle(db, vehicle)
    elif response == "3":
        required_items = ['make', 'model', 'vin', 'sale_price', 'description']
        vehicle_dict = get_vehicle(db) # get which vehicle the user wants to edit
        data_type = get_attribute(vehicle_dict) # proceed with the next prompt of which attribute to edit
        data = get_input(data_type, data_type in required_items) # get the input for the type

        modify_vehicle(db, vehicle_dict['id'], data_type, data)
    elif response == "4":
        vehicle_dict = get_vehicle(db) # get which vehicle the user wants to edit
        response = input("Are you sure you want to delete this vehicle? (Y/N): ") # make sure the user wants to remove it

        if response.lower() == "y":
            remove_vehicle(db, vehicle_dict['id'])
        else:
            print("The vehicle was not removed\n")
    elif response == "5":
        ask = False
    else:
        print("Invalid response. Please enter a number 1-5.")