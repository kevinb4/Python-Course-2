from classes.event import Event # import events to ensure events being added belong to the event class

class Calendar:
    """A class that represents a calendar/planner"""

    def __init__(self, cal_name = "", cal_owner = "", cal_events = []):
        """Initialize the class and the needed variables for the calendar"""
        self.cal_name = cal_name
        self.cal_owner = cal_owner
        self.cal_events = cal_events

    def add_event(self, cal_event):
        """Adds a new event to the calendar
        Arguments:
            cal_event [event] -- an event to add to the calendar object"""
        if isinstance(cal_event, Event): # make sure what's being added is an event object
            self.cal_events.append(cal_event)
            print(f"The event \"{cal_event.event_name}\" has been added!")
        else:
            print("An invalid event cannot be added")

    def get_input(self, data_type):
        """Asks the user for a specific input and validates it
        Arguments:
            data_type [string] -- the type of data to gather
        Returns:
            data [string] -- valid type of data"""
        data = input(f"Enter the calendar's {data_type}: ")

        data_ok = False

        while not data_ok:
            data_ok = data.isalpha()

            if not data_ok:
                data = input(f"The value you entered is not valid, please enter only letters for the calendar's {data_type}: ")

        return data

    def get_remove_input(self):
        """Handles obtaining which event the user would like to remove"""
        if len(self.cal_events) == 0:
            print("There are no events to remove")
            return

        # loop through to display all events and add 1 so it's not 0 indexed (easier for user to understand)
        # note: getting the length does not need to be modified since it does not use 0 index
        for i in range(len(self.cal_events)):
            print(f"{i + 1} - {self.cal_events[i].event_name}")

        response = input(f"Please enter the number of which event you'd like to remove (1-{len(self.cal_events)}): ")

        # make sure a valid digit was entered prior to converting to int
        if not response.isdigit():
            print("You must enter a number")
            return

        response = int(response)

        # make sure it's within range of the options
        if response < 1 or response > len(self.cal_events):
            print(f"{response} is out of range from 1-{len(self.cal_events)}")
            return

        self.remove_event(response)

    def remove_event(self, del_int):
        """Removes a known event from the calendar via list index
        Arguments:
            del_int [int] -- the index of the item to delete in the calendar object"""
        try: # in case something goes wrong
            del_int -= 1 # adjust for 0 indexing by subtracting 1 from what the user inputted
            name = self.cal_events[del_int].event_name # save the name so it can be used in the success message
            del self.cal_events[del_int]
            print(f"The event \"{name}\" has been removed")
        except:
            print("There was an issue removing the event")