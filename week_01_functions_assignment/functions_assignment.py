from functions.my_functions import *

cont = True
employees = []

while cont:
    id = get_data("id")
    name = get_data("name")
    email = get_data("email")
    address = get_data("address")

    # make sure to only include addresses if the user entered one
    if address:
        employees.append({ 'id': id, 'name': name, 'email': email, 'address': address })
    else:
        employees.append({ 'id': id, 'name': name, 'email': email })

    # check to make sure the max amount of employees hasn't been reached
    if len(employees) < 5:
        response = input("Add another employee? (Y/N): ")
        if response.lower() == "n":
            cont = False # we only need to set continue to false since it's already true
    else:
        cont = False # to make sure it doesn't ask more than five times

print(employees)