def add_vehicle(db, vehicle):
    """Adds a vehicle to the database
    Arguments:
        db [class] -- the database class to execute the query
        vehicle [dict] -- all attributes tied to the current vehicle"""
    items = list(vehicle.keys()) # get the list of attributes
    values = list(vehicle.values()) # get the list of values entered

    try:
        # use the build functions to execute the necessary items
        db.executeQuery(f"INSERT INTO vehicle ({build_list(items)}) VALUES ({build_values(len(items))});", values)
        db.conn.commit()
        print("Successfully added the vehicle to the database\n")
    except:
        print("Failed to add the vehicle to the database - make sure to enter a unique VIN\n")

def build_dict(items):
    """Builds a string that contains the key and value that contain values
    Attributes:
        items [dict] -- a dictionary of items to write out
    Returns:
        msg [string] -- a formatted string containing all items that aren't empty"""
    msg = ""

    try:
        for key, value in items.items():
            if value != None and value != 0.00: # don't print optional values that weren't entered
                msg += f"{underscore_remove(key)}: {value}, "

        return msg[:-2] # remove last comma and space
    except:
        print("Unable to convert the input to a string")

def build_list(items):
    """Builds a string that contains the items in a list
    Attributes:
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

def build_values(amount):
    """Builds a string that contains a specified number of %s to use for a query
    Attributes:
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

def long_list_vehicles(db):
    """Prints a detailed list of vehiles, one attribute per line
    Attributes:
        db [class] -- the db class used to execute the query"""
    results = db.executeSelectQuery("SELECT * FROM vehicle")

    if len(results) == 0: # let the user know none are found instead of printing nothing
        print("\nNo entries found\n")
    else:
        print("") # padding
        for result in results:
            print(f"Entry #{result['id']}\n-----------------------")
            print(f"Make: {result['make']}")
            print(f"Model: {result['model']}")
            print(f"VIN: {result['vin']}")
            if result["previous_owner"]:
                print(f"Previous Owner: {result['previous_owner']}")
            if result["price_paid"]:
                print(f"Price Paid: {result['price_paid']}")
            print(f"Sales Price: {result['sale_price']}")
            print(f"Vehicle Description: {result['description']}\n")

def get_attribute(vehicle_dict):
    """Gets the selecting from the user of which item they'd like to edit
    Arguments:
        vehicle_dict [dict] -- a dictionary containing information about the vehicle
    Returns:
        data_type [string] -- the valid type of data/attribute to modify"""
    msg = "\n"

    for key, value in vehicle_dict.items():
        if key != 'id': # can't modify the primary key
            msg += f"{underscore_remove(key)}: {value}\n"

    data_type = input(f"{msg[:-1]}\n\nEnter the name of the attribute you'd like to edit (eg. model): ")
    data_type_ok = False

    while not data_type_ok:
        data_type = underscore_add(data_type).lower()
        if data_type in vehicle_dict.keys():
            if data_type != 'id': # can't modify the primary key
                data_type_ok = True
        
        if not data_type_ok:
            data_type = input(f"\"{data_type}\" is not a valid attribute, try again: ")

    return data_type

def get_input(data_type, required = True):
    """Obtains the data and verifies it
    Arguments:
        data_type [string] -- the type of data to get
        required [boolean] -- whether or not the type of data is required
    Returns:
        data [string] -- the verified data"""
    msg = f"Enter the vehicle's {underscore_remove(data_type)}"

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
        elif data_type == "make":
            data_ok = data.isalpha()
        elif data_type == "model":
            data_ok = validate_char(data, data_type, "disallowed")
        elif data_type == "vin":
            data_ok = data.isalnum()
        elif data_type == "previous_owner":
            data_ok = validate_char(data, data_type, "allowed")
        elif data_type == "price_paid" or data_type == "sale_price":
            data_ok = validate_price(data)
        elif data_type == "description":
            data_ok = validate_input(data)

        if not data_ok:
            data = input(f"\"{data}\" is not valid for the {underscore_remove(data_type)}, please try again: ")

    return data

def get_vehicle(db):
    """Allows the user to select which vehicle they want to either modify or remove
    Arguments:
        db [class] -- used to get the list of items in the database
    Returns:
        result [dict] -- returns a dict of the selected vehicle"""
    short_list_vehicles(db) # print out a list of vehicles

    item = input("\nEnter the item number of the item you'd like to select: #")
    item_ok = False

    while not item_ok:
        if item.isdigit():
            result = db.executeSelectQuery("SELECT * FROM vehicle WHERE id = %s", [str(item)])

            if result:
                item_ok = True

        if not item_ok:
            item = input(f"Vehicle with the number {item} was not found, please enter a valid number: #")

    return result[0] # only return the first item since there should only be one

def modify_vehicle(db, id, data_type, data):
    """Modifies the current vehicle
    Arguments:
        db [class] -- used to execute the query
        id [int] -- the primary key of the vehicle
        data_type [string] -- contains the attribute of which item the user is modifying
        data [string] -- the new value for the attribute"""
    try:
        db.executeQuery(f"UPDATE vehicle SET {data_type} = %s WHERE id = %s", [data, id])
        db.conn.commit()

        msg = f"The {underscore_remove(data_type)} has been "

        if data: # if removed, state so instead of printing "None"
            msg += f"modified to \"{data}\"\n"
        else:
            msg += f"removed\n"

        print(msg)
    except:
        print("Error saving modified value to database\n")

def remove_vehicle(db, id):
    """Removes a vehicle from the database
    Arguments:
        db [class] -- used to execute the query
        id [int] -- the primary key of the vehicle"""
    try:
        db.executeQuery("DELETE FROM vehicle WHERE id = %s", [id])
        db.conn.commit()
        print("The vehicle has been removed\n")
    except:
        print("Error removing the vehicle from the database\n")

def short_list_vehicles(db):
    """Prints a list of one vehile per line with attributes
    Attributes:
        db [class] -- the db class used to execute the query"""
    results = db.executeSelectQuery("SELECT * FROM vehicle")

    for result in results:
        id = result.pop("id") # to display the id separately
        print(f"Item #{id} -- {build_dict(result)}")

def underscore_add(data):
    """A small function to replace spaces with underscores
    Attributes:
        data [string] -- the passed string to modify
    Returns:
        data [string] -- the passed string that has underscores instead of spaces"""
    return data.replace(' ', '_')

def underscore_remove(data):
    """A small function to replace underscores with spaces
    Attributes:
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

    if data_type == "model":
        char_list = ['!', '"', '@', '#', '$', '%', '^', '*', '(', ')', '_', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '~', '|', '.']
    elif data_type == "previous_owner":
        char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', ',', '.', '\'', '-']
    else: # this shouldn't happen but it's good to have a safety net
        print("Failed to get character list")
        return False

    # although it could be determined on the type since there's only two, having allowed/disallowed
    # makes it easier to add more types to the fuction without having to make any additional changes
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

def validate_price(price):
    """Validates the price of a vehicle (aka if it's a float value)
    Arguments:
        price [string] -- passed user input
    Returns:
        true/false [boolean] -- if it's a float or not"""
    try:
        float(price)
        return True
    except:
        return False
