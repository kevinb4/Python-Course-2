class Event:
    """Represents events added on a calendar"""

    def __init__(self, event_name = "", event_date = "", event_time = "", event_type = ""):
        """Initializes the event class"""
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.event_type = event_type

        # define options here to make adding/removing easy
        self.allowed_types = ["single occurrence", "recurring", "fixed number of meetings"]

    def get_input(self, data_type):
        """Validates all inputs necessary
        Arguments:
            data_type [string] -- the type of data to gather
        Returns:
            data [string] -- valid type of data"""
        data = input(f"Enter the event's {data_type} ({self.get_requirements(data_type)}): ")

        data_ok = False

        while not data_ok:
            if data_type == "name":
                data_ok = data.isalpha()
            elif data_type == "date" or data_type == "time":
                data_ok = self.validate_char(data, data_type)
            elif data_type == "type":
                data_ok = self.validate_type(data)

            if not data_ok:
                data = input(f"The value \"{data}\" is not valid. Please enter the {data_type} which {self.get_requirements(data_type)}: ")

        return data

    def get_requirements(self, data_type):
        """A small function to easily get the requirements added onto an outputted message
        Arguments:
            data_type [string] -- the type of data to get the requirements for
        Returns:
            msg [string] -- string containing requirements info"""
        msg = "must only contain "
        if data_type == "name":
            msg += "letters"
        elif data_type == "date":
            msg += "numbers and the - symbol"
        elif data_type == "time":
            msg += "numbers and the : symbol"
        elif data_type == "type":
            # msg += ', '.join(f"\"{item}\"" for item in self.allowed_types) # organize items in a comma'd list without a trailing comma
            for i in range(len(self.allowed_types)): # the ugly way of printing a comma'd list without a trailing comma
                msg += f"\"{self.allowed_types[i]}\""

                if (i + 1) != len(self.allowed_types):
                    msg += ", "

        return msg

    def validate_char(self, data, data_type):
        """Validates date or time
        Arguments:
            data [string] -- the user inputted data to test
            data_type [string] -- the type of data to test
        Returns:
            boolean -- whether the test passed or not"""
        char_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] # since both require all numbers, add them right away

        if data_type == "date":
            char_list.append('-')
        elif data_type == "time":
            char_list.append(':')
        else: # this should not happen, but just in case
            return False

        passed = False

        for char in data:
            if char in char_list:
                # we only want the characters that are in the lists
                passed = True
            else:
                passed = False
                break # stop if a bad char is found or else it could be set to true from the next char

        return passed

    def validate_type(self, data):
        """Validates the only types allowed
        Arguments:
            data [string] -- the user input to test
        Returns:
            boolean -- whether the test passed or not"""
        if str(data).lower() in self.allowed_types:
            return True
        else:
            return False