from classes.individual import Individual

class Instructor(Individual):
    """Defines the instructor class that inherits from the Individual class"""

    def __init__(self, id, name, email, institution_graduated, highest_degree_earned):
        """Initializes the instructor class that inherits the individual class"""

        super().__init__(id, name, email)

        self.institution_graduated = institution_graduated
        self.highest_degree_earned = highest_degree_earned

    def displayInformation(self):
        """Prints of all the data in the instructor class"""

        print(f"Instructor ID: {self.id}, Name: {self.name}, Email: {self.email}, Institution Graduated: {self.institution_graduated}, and the Higest Degree Earned: {self.highest_degree_earned}.")