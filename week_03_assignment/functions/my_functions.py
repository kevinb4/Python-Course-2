import json

def load_json(path):
    """Loads the json file
    Arguments:
        path [string] -- location of the json file
    Returns:
        data [json dict/boolean] -- will return the data that was loaded from the json file or returns false if it failed to load
    """
    try:
        with open(path) as json_obj:
            config_data = json.load(json_obj)
            return config_data
    except:
        print("The config file was not found.")
        return False

def save_prompt(config_data):
    """Prompts the user if they'd like to save their changes
    Arguments:
        config_data [dict] -- the current config data dict
    """
    response = input("Would you like to (S)ave your changes or (D)iscard them? (enter S or D) ")

    if response.lower() == "s": # only check for s since discarding requires no further code
        with open("text_files/config_override.json", 'w') as json_obj:
            json.dump(config_data, json_obj)
        
        print("Your changes have been saved.")

def required_input(question):
    """Validates input to make sure something was entered
    Arguments:
        question [string] -- contains what the program will ask for the user
    Returns:
        data [string] -- what the user entered
    """
    valid = False
    data = input(question)

    while not valid:
        if data:
            valid = True
        else:
            data = input(f"No data was entered. {question}")

    return data

def add(config_data):
    """Handles adding new data to the config
    Arguments:
        config_data [dict] -- the current config data dict
    """
    ask = True

    while ask: # use a loop to allow the user to enter multiple items without restarting the app
        add_key = required_input("Please enter the data key: ")
        add_data = required_input("Please enter the data: ")

        config_data[add_key] = add_data
        
        print(f"The config \"{add_key}\" has been added with the value of \"{add_data}\".")
        response = input("Would you like to add another item? (Y/N) ")

        if response.lower() == "n":
            ask = False

    save_prompt(config_data)

def modify(config_data, required_data):
    """Handles modifying and removing values in the config data
    Arguments:
        config_data [dict] -- the current config data dict
        required_data [dict] -- the required items that cannot be deleted
    """
    ask = True

    while ask: # use a loop to allow the user to modify multiple items without restarting the app
        item = input("Which item would you like to modify? (Type it in exactly as it appears) ")

        if item in config_data.keys(): # check if the item exists
            edit = input(f"Enter the new value for \"{item}\" (or enter nothing to remove it): ")
            if edit: # if the user entered something, save it
                config_data[item] = edit
            else: # if they entered nothing, it should be removed
                if item in required_data.keys(): # see if the item is required
                    print(f"The item \"{item}\" is required and cannot be deleted.")
                else: # if not, allow it to be removed
                    del config_data[item]
                    print(f"The item \"{item}\" has been removed.")
        else:
            print(f"Item \"{item}\" was not found in the config.")

        response = input("Would you like to modify another item? (Y/N) ")

        if response.lower() == "n":
            ask = False

    save_prompt(config_data)