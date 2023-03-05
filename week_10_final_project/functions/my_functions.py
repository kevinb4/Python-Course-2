import os.path
import shutil
import time
import json

def add_customer(db, customer):
    """Adds the customer to both databases
    Arguments:
        customer [dict] -- data containing customer information"""
    # try adding to the mailings table
    try:
        # use the build functions to execute the necessary items
        db.executeQuery(f"INSERT INTO mailings (name, company, address) VALUES ({build_values(3)});", [build_name(customer), customer['company'], build_address(customer)])
        db.conn.commit()
        print("Successfully added customer to the mailings database\n")
    except:
        print("Failed to add customer to the mailings database\n")

    # rename the customer name values to match the crm_data table attributes
    customer['f_name'] = customer.pop('first_name')
    customer['l_name'] = customer.pop('last_name')

    items = list(customer.keys()) # get the list of attributes
    values = list(customer.values()) # get the list of values entered

    # try adding to the crm_data table
    try:
        # use the build functions to execute the necessary items
        db.executeQuery(f"INSERT INTO crm_data ({build_list(items)}) VALUES ({build_values(len(customer))});", values)
        db.conn.commit()
        print("Successfully added customer to the crm database\n")
    except:
        print("Failed to add customer to the crm database\n")

def build_address(customer):
    """Returns a string of concatenated address information
    Arguments:
        customer [dict] -- the customer dict containing all the customer data
    Returns:
        address [string] -- formatted address as written on a letter"""
    return f"{customer['address']}, {customer['city']}, {customer['state']} {customer['zip']}"

def build_list(items):
    """Builds a string that contains the items in a list
    Arguments:
        items [list] -- a list of items to write out
    Returns:
        msg [string] -- a formatted string containing all the passed items"""
    msg = ""

    try:
        for item in items:
            msg += f"{str(item)}, "

        return msg[:-2] # remove last comma and space
    except:
        print("Unable to convert the input to a string")

def build_name(customer):
    """Returns a string of a customer's full name (first and last)
    Arguments:
        customer [dict] -- the customer dict containing all the customer data
    Returns:
        name [string] -- formatted first and last name"""
    return f"{customer['first_name']} {customer['last_name']}"

def build_values(amount):
    """Builds a string that contains a specified number of %s to use for a query
    Arguments:
        amount [int] -- used for the loop
    Returns:
        msg [string] -- a formatted string containing the specified number of %s"""
    msg = ""

    try:
        for count in range(amount):
            msg += "%s, "

        return msg[:-2] # remove last comma and space
    except:
        print("Unable to convert the input to a string")

def backup_file(path):
    """Checks to see if the file exists and if it does, add the date so the file does not get overwritten
    Arguments:
        path [string] -- the path to the file"""
    if os.path.exists(path):
        shutil.copy2(path, f"{path}.backup{str(time.time())}")

def import_data():
    """Imports data from a text file dump
    Returns:
        data_list/false [list/bool] -- either returns the data if successful or false if not"""
    data_list = []
    emails = []

    try:
        with open("text_files/customer_export.txt") as file:
            for line in file:
                data = line.replace("##", "").strip().split("|") # remove the pound signs, remove any extra spaces, and split the data up
                data_dict = {"first_name": data[0], "last_name": data[1], "company": data[2], "address": data[3], "city": data[4], "county": data[5], "state": data[6], "zip": data[7], "primary_phone": data[8], "secondary_phone": data[9], "email": data[10]}
                
                if not data[10] in emails: # use emails to keep track of duplicates
                    emails.append(data[10])
                    data_list.append(data_dict)

        return data_list[1:] # remove the header
    except:
        return False

def get_input(data_type, required = True):
    """Obtains the data and verifies it
    Arguments:
        data_type [string] -- the type of data to get
        required [boolean] -- whether or not the type of data is required
    Returns:
        data [string] -- the verified data"""
    msg = f"Enter the customer's {underscore_remove(data_type)}"

    if not required:
        msg += " (optional): "
    else:
        msg += ": "

    data = input(msg)
    data_ok = False

    while not data_ok:
        if not required and not data:
            # if the input is not required and nothing was passed, then the check will pass
            data_ok = True
        elif data_type == "first_name" or data_type == "last_name":
            data_ok = validate_char(data, data_type, "allowed")
        elif data_type == "company":
            data_ok = validate_input(data)
        elif data_type == "address":
            data_ok = validate_char(data, data_type, "disallowed")
        elif data_type == "city":
            data_ok = validate_char(data, data_type, "allowed")
        elif data_type == "state":
            data_ok = validate_state(data)
        elif data_type == "zip":
            data_ok = validate_zipcode(data)
        elif data_type == "primary_phone" or data_type == "secondary_phone":
            data_ok = validate_char(data, data_type, "allowed")
        elif data_type == "email":
            data_ok = validate_char(data, data_type, "disallowed")

        if not data_ok:
            data = input(f"\"{data}\" is not valid for the {underscore_remove(data_type)}, please try again: ")

    return data

def print_db(db, table):
    """Prints out all rows in the database table"""
    results = db.executeSelectQuery(f"SELECT * FROM {table};")
    print("") # padding

    if len(results) == 0: # let the user know none are found instead of printing nothing
        print("No entries found in the database")
    elif table == "crm_data":
        for result in results:
            print(f"\nEntry #{result['crm_id']}\n-----------------------")
            print(f"First Name: {result['first_name']}")
            print(f"Last Name: {result['last_name']}")
            print(f"Address: {result['address']}")
            print(f"City: {result['city']}")
            print(f"State: {result['state']}")
            print(f"Zip Code: {result['zip']}")
            if result["company"]: # company is optional in this table but not mailings?
                print(f"Company: {result['company']}")
            print(f"Primary Phone: {result['primary_phone']}")
            if result["secondary_phone"]:
                print(f"Secondary Phone: {result['secondary_phone']}")
            if result["email_address"]:
                print(f"Email Address: {result['email_address']}")
    elif table == "mailings":
        for result in results:
            print(f"\nEntry #{result['mail_id']}\n-----------------------")
            print(f"Name: {result['name']}")
            print(f"Company: {result['company']}")
            print(f"Address: {result['address']}")
    else:
        print("Table not found.")

    print("") # padding

def save_to_crm_db(db, data):
    """Saves the passed data to the CRM database"""
    # first we need to empty the current table
    db.executeQuery("TRUNCATE TABLE crm_data;")
    db.conn.commit()

    # make it one single query for better performance
    query = "INSERT INTO crm_data (f_name, l_name, address, city, state, zip, company, primary_phone, secondary_phone, email_address)\nVALUES"
    values = []

    for line in data:
        # now we need to add all the data from the dict
        query += f"({build_values(10)}),\n" # add %s for sanitization for every row + value
        values += [line['first_name'], line['last_name'], line['address'], line['city'], line['state'], line['zip'], line['company'], line['primary_phone'], line['secondary_phone'], line['email']] # add all relavent values

    query = f"{query[:-2]};" # remove the last comma and line break + add semicolin

    try: # try to add the data
        db.executeQuery(query, values)
        db.conn.commit()
    except:
        print("There was an issue saving the values to the drm_data database.")

def save_to_CSV(path, data):
    """Saves the data passed to a csv file"""
    csv = ""

    for item in data[0]: # build the header row using the keys in the dict
        csv += f"{item},"
    
    csv = csv[:-1] # remove the last comma

    for data_dict in data: # loop through the entire dict
        csv += "\n" # add a new line for each row
        for item in data_dict.values(): # for each row in the data, add each value with a comma
            csv += f"{item},"

        csv = csv[:-1] # remove the last comma

    backup_file(path) # make sure not to overwrite the file
    with open(path, "w") as csv_output:
        csv_output.write(csv)

def save_to_JSON(path, data):
    """Saves the passed data to a JSON file"""
    backup_file(path) # make sure not to overwrite the file
    with open(path, "w") as json_output:
        json.dump(data, json_output)

def save_to_mailings_db(db, data):
    """Saves the passed data to the mailings database"""
    # first we need to empty the current table
    db.executeQuery("TRUNCATE TABLE mailings;")
    db.conn.commit()

    # make it one single query for better performance
    query = "INSERT INTO mailings (name, company, address)\nVALUES"
    values = []

    for line in data:
        # now we need to add all the data from the dict
        query += f"({build_values(3)}),\n" # add %s for sanitization for every row + value
        values += [build_name(line), line['company'], f"{build_address(line)}\n"] # add all relavent values

    query = f"{query[:-2]};" # remove the last comma and line break + add semicolin

    try: # try to add the data
        db.executeQuery(query, values)
        db.conn.commit()
    except:
        print("There was an issue saving the values to the mailings database.")

def underscore_add(data):
    """A small function to replace spaces with underscores
    Arguments:
        data [string] -- the passed string to modify
    Returns:
        data [string] -- the passed string that has underscores instead of spaces"""
    return data.replace(' ', '_')

def underscore_remove(data):
    """A small function to replace underscores with spaces
    Arguments:
        data [string] -- the passed string to modify
    Returns:
        data [string] -- the passed string that has spaces instead of underscores"""
    return data.replace('_', ' ')

def validate_char(passed_input, data_type, check_type):
    """Validates date or time
    Arguments:
        data [string] -- the user inputted data to test
        data_type [string] -- the type of data to test
        check_type [string] -- whether the char list is run against allowed characters or disallowed characters
    Returns:
        boolean -- whether the test passed or not"""
    passed = False
    char_list = []

    if data_type == "address":
        char_list = ['!', '"', '\'', '@', '$', '%', '^', '&', '*', '_', '=', '+', '<', '>', '?', ';', '[', ']', '{', '}']
    elif data_type == "city":
        char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '-']
    elif data_type == "email":
        char_list = ['!', '"', '\'', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\']
    elif data_type == "first_name" or data_type == "last_name":
        char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '\'', '-']
    elif data_type == "primary_phone" or data_type == "secondary_phone":
        char_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
    else: # this shouldn't happen but it's good to have a safety net
        print("Failed to get character list")
        return False

    if check_type == "disallowed":
        for char in passed_input:
            if char in char_list:
                passed = False
                break # stop if a bad char is found or else it could be set to true from the next char
            else:
                passed = True
    elif check_type == "allowed":
        for char in passed_input:
            if char.lower() in char_list:
                # we only want the characters that are in the list
                passed = True
            else:
                passed = False
                break # stop if a bad char is found or else it could be set to true from the next char
    else: # just in case
        passed = False

    return passed

def validate_input(data):
    """Validates that data was entered
    Arguments:
        data [string] -- passed user input
    Returns:
        true/false [boolean] -- returns true if the user entered something, false if not"""
    if data:
        return True
    else:
        return False
    
def validate_state(data):
    """Validates the user entered two uppercase letters
    Arguments:
        data [string] -- passed user input
    Returns:
        true/false [boolean] -- returns true if the user entered a valid state"""
    if data.isalpha() and data.isupper() and len(data) == 2:
        return True
    else:
        return False
    
def validate_zipcode(data):
    """Validates the user entered a valid four or five digit zip code
    Arguments:
        data [string] -- passed user input
    Returns:
        true/false [boolean] -- returns true if the user entered a valid zip code"""
    if data.isnumeric() and (len(data) == 4 or len(data) == 5):
        return True
    else:
        return False