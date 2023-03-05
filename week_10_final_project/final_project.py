from classes.database_access import DB_Connect
from functions.my_functions import *

# my current db was setup with a password so change if necessary
db = DB_Connect('root', '1234', 'python_final')

ask = True

while ask:
    response = input("What would you like to do? Enter the number of the item you want:\n1. Import a new data file\n2. Show data currently in a database\n3. Add a record to the databases\n4. Edit a record\n5. Exit program\n> ")

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
        response = input("Which database would you like to print out? (c)rm data or (m)ailings? (Enter c or m): ")

        if response.lower() == "c":
            print_db(db, "crm_data")
        elif response.lower() == "m":
            print_db(db, "mailings")
        else:
            print("\nInvalid response, please enter c or m.\n")
    elif response == "3":
        required = ["first_name", "last_name", "company", "address", "city", "state", "zip", "primary_phone"]
        fields = list(required) + ["secondary_phone", "email"]
        customer = {}
        
        for item in fields: # loop through all possible fields
            data = get_input(item, item in required)
            
            if data: # don't add optional items that weren't entered
                customer[item] = data

        add_customer(db, customer)
    # elif response == "4":
        # TODO
    elif response == "5":
        ask = False
    else:
        print("\nInvalid response. Please enter a number 1-5.\n")