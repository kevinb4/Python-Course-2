from classes.individual import Individual

class Student(Individual):
    """Defines the student class that inherits from the Individual class"""

    def __init__(self, id, name, email, program):
        """Initializes the student class which inherits the individual class"""

        super().__init__(id, name, email)

        self.program = program

    def displayInformation(self):
        """Prints of all the data in the student class"""

        print(f"Student ID: {self.id}, Name: {self.name}, Email: {self.email}, and Program of Study: {self.program}.")