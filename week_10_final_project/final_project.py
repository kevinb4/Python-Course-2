from classes.database_access import DB_Connect
from functions.my_functions import *

# my current db was setup with a password so change if necessary
db = DB_Connect('root', '1234', 'python_final')

ask = True

while ask:
    response = input("What would you like to do? Enter the number of the item you want:\n1. Import a new data file\n2. Show data currently in a database\n3. Add a record to the databases\n4. Edit a record\n5. Remove a record\n6. Exit program\n> ")

    if response == "1":
        data = import_data()

        if data:
            save_to_CSV("text_files/customer_export.csv", data)
            save_to_JSON("text_files/customer_export.json", data)
            save_to_crm_db(db, data)
            save_to_mailings_db(db, data)

            print("\nData has been imported successfully!\n")
        else:
            print("\nThere was an issue reading the file. Please make sure the customer_export.txt is located in the text_files folder.\n")
    elif response == "2":
        table = get_database() # get the table the user would like to print
        
        print_db(db, table)
    elif response == "3":
        required = ["first_name", "last_name", "company", "address", "city", "state", "zip", "primary_phone"]
        fields = list(required) + ["secondary_phone", "email"]
        customer = {}
        
        for item in fields: # loop through all possible fields
            data = get_input(item, item in required)
            
            if data: # don't add optional items that weren't entered
                customer[item] = data

        add_customer(db, customer)
    elif response == "4":
        required = {"crm_data": ["first_name", "last_name", "company", "address", "city", "state", "zip", "primary_phone"], "mailings": ["name", "company", "address"]}
        table = get_database() # get the table the user would like to edit
        customer_dict = get_customer(db, table) # get the customer object from the specified table
        data_type = get_attribute(customer_dict) # get the attribute the user wants to modify
        data = get_input(data_type, data_type in required[table]) # get the data the user wants to modify

        modify_customer(db, customer_dict['id'], table, data_type, data)
    elif response == "5":
        table = get_database() # get the table the user would like to edit
        customer_dict = get_customer(db, table) # get the customer object from the specified table
        response = input("Are you sure you want to delete this customer? (Y/N): ")

        if response.lower() == "y":
            remove_customer(db, customer_dict['id'], table)
        else:
            print("The customer was not removed\n")
    elif response == "6":
        ask = False
    else:
        print("\nInvalid response. Please enter a number 1-6.\n")