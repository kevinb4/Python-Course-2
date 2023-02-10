from classes.calendar import Calendar
from classes.event import Event

cal = Calendar()

cal.cal_name = cal.get_input("name")
cal.cal_owner = cal.get_input("owner")

print(f"\nSuccess! Welcome to {cal.cal_owner}'s {cal.cal_name}.")

ask = True

while ask:
    response = input("\nWhat would you like to do?\nA - Add new event\nR - Remove an event\nE - Exit\n> ")
    
    if response.lower() == "a":
        new_event = Event()

        new_event.event_name = new_event.get_input("name")
        new_event.event_date = new_event.get_input("date")
        new_event.event_time = new_event.get_input("time")
        new_event.event_type = new_event.get_input("type")

        cal.add_event(new_event)
    elif response.lower() == "r":
        cal.get_remove_input()
    elif response.lower() == "e":
        ask = False
    else:
        print("Invalid response, please try again.")

