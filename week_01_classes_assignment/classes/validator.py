class Validator():
    """Defines the validator class that will validate user input"""

    def __init__(self):
        """Initializes the validator class"""

    def validate_input(self, data):
        """Ensures the user entered a value"""

        if data:
            return True
        else:
            return False

    def validate_individual(self, data):
        """Validates the type of individual"""

        if data.lower() == "student" or data.lower() == "instructor":
            return True
        else:
            return False

    def validate_id(self, data, individual_type):
        """Validates the ID for students or instructors"""

        length = 0

        if individual_type == "student":
            length = 7
        elif individual_type == "instructor":
            length = 5
        else: # this should not happen, but just in case
            return False

        if data.isdigit() and len(data) <= length:
            return True
        else:
            return False

    def validate_char(self, data, data_type):
        """Validates name or email"""

        char_list = []

        if data_type == "name":
            # setup custom char filter - add numbers since a name cannot contain numbers because using isalpha would return false if the user has a period in their name, which isn't on the special characters list
            char_list = ['!', '"', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        elif data_type == "email":
            # setup custom char filter
            char_list = ['!', '"', '\'', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', ',', '<', '>', '/', '?', ';', ':', '[', ']', '{', '}', '\\']
        else: # this should not happen, but just in case
            return False

        passed = False

        for char in data:
            if char in char_list:
                passed = False
                break # stop if a bad char is found or else it could be set to true from the next char
            else:
                passed = True

        return passed