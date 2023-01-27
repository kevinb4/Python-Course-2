from functions.my_functions import *
import os.path

reqired_data = load_json("text_files/basic_config.json") # if this file is not available, the program cannot run
config_data = reqired_data # incase the custom data does not exist, set the required data as default

# if the custom data file exists, overwrite the config data
if os.path.isfile("text_files/config_override.json"):
    data = load_json("text_files/config_override.json")

    if data: # just in case the function returns false (if the file were to be empty for ex), the program can still run with the required config
        config_data = data

if reqired_data:
    counter = 1
    for value, data in config_data.items():
        print(f"{counter}. {value} - \"{data}\"")
        counter += 1

    ask = True

    while ask:
        option = input("\nPlease use the following menu to pick an option\nA - Add a configuration item\nM - Modify/Remove a configeration item\nE - Exit the app\n> ")

        if option.lower() == "m":
            config_data = modify(config_data, reqired_data)
        elif option.lower() == "a":
            config_data = add(config_data)
        elif option.lower() == "e":
            ask = False
        else:
            print("Unknown response, please enter a valid option.")