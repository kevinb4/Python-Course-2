def id_check(id):
    """Checks that a valid id was entered
        Arguments:
            id [number] -- passed value to check
        Returns:
            True/False [boolean] -- based off of result
    """

    if id.isdigit() and len(id) <= 7: # make sure input is a valid number and that it's 7 or less digits
        return True
    else:
        return False

def bad_char_check(passed_input, data_type, required):
    """Checks the passed value based off of the data type to see if it's required and if it passed validation
    Arguments:
        passed_input [variable] -- the input that's being validated
        data_type [variable] -- the type of data to check
        required [boolean] -- if the value is required or not
    Returns:
        True/False [boolean] -- based off of result
    """
        
    passed = False
    char_list = []

    if required and not passed_input:
        # if the input is required and it's not set, then return false
        return False
    elif not required and not passed_input:
        # if the input is not required and nothing was passed, then the check will pass
        return True
    elif data_type == "name":
        # setup custom char filter - add numbers since a name cannot contain numbers because using isalpha would return false if the user has a period in their name, which isn't on the special characters list
        char_list = ['!', '"', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{' '}', '\\',
                          '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    elif data_type == "email":
        # setup custom char filter
        char_list = ['!', '"', '\'', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\']
    elif data_type == "address":
        # setup custom char filter
        char_list = ['!', '"', '\'', '@', '$', '%', '^', '&', '*', '_', '=', '+', '<', '>', '?', ';', ':', '[', ']', '{', '}']
    else: # this shouldn't happen but it's good to have a safety net
        print("Failed to get illegal character list")
        return False

    for char in passed_input:
        if char in char_list:
            passed = False
            break # stop if a bad char is found or else it could be set to true from the next char
        else:
            passed = True
            
    return passed

def get_data(data_type):
    """Gets the user input and runs checks against the inputted data
    Arguments:
        data_type [variable] -- the type of data that's being collected
    Returns:
        data [variable] -- the inputted data after it has been validated
    """

    msg = f"Please enter your employee {data_type}"

    # inform the user address is optional when prompted
    if data_type == "address":
        msg = f"{msg} (optional): "
    else:
        msg = f"{msg}: "

    data = input(msg) # get data
    data_ok = False

    while not data_ok:
        if data_type == "id":
            data_ok = id_check(data) # special handler for id since it doesn't use the char checker
        else:
            data_ok = bad_char_check(data, data_type, data_type != "address") # if data does not equal address, this check will return true since everything but address is required

        if not data_ok:
            data = input(f"The {data_type} you entered is not valid, please enter characters only used in a {data_type}: ")

    return data