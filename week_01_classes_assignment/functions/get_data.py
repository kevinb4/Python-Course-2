from classes.validator import Validator

def get_data(data_type, individual = ""):
    """Obtains data from the user and validates it
    Arguments:
        data_type [variable] -- the type of data to be collected
        individual [variable] -- the type of individual (not required)
    Returns:
        data [variable] -- the inputted data after it has been validated
    """

    message = "Please enter the "

    # modify the message depending on the data type
    if data_type == "individual":
        message += "type of individual (student or instructor): "
    else:
        message += f"{individual}'s {data_type}: "

    data = input(message)
    data_ok = False

    while not data_ok:
        check = Validator() # initiate the validator class right away since it will be used regardless of the type

        # handle specific data types with the specific validator methods
        if data_type == "individual":
            data_ok = check.validate_individual(data)
        elif data_type == "id":
            data_ok = check.validate_id(data, individual)
        elif data_type == "name" or data_type == "email": # name and email use the same method for good code reuse
            data_ok = check.validate_char(data, data_type)
        else: # handles the remaining info required for the individual
            data_ok = check.validate_input(data)

        if not data_ok:
            data = input(f"\"{data}\" is an invalid entry for a(n) {data_type}, please try again: ")

    return data