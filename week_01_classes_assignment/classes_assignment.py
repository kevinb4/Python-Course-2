from classes.individual import Individual
from classes.student import Student
from classes.instructor import Instructor
from functions.get_data import get_data

cont = True
college_records = []

while cont:
    individual = get_data("individual")
    id = get_data("id", individual)
    name = get_data("name", individual)
    email = get_data("email", individual)

    if individual == "student": # handle student's specific information
        program = get_data("program of study", individual)

        # create new student instance and add the collected data
        student = Student(id, name, email, program)

        # append the data to the list using the displayInformation method so the data is readable
        college_records.append(student)
    elif individual == "instructor": # handle instructor's specific information
        institution = get_data("institution graduated", individual)
        degree = get_data("highest degree earned", individual)

        # create new instructor instance and add the collected data
        instructor = Instructor(id, name, email, institution, degree)

        # append the data to the list using the displayInformation method so the data is readable
        college_records.append(instructor)

    response = input("Add another individual? (Y/N): ")
    if response.lower() == "n":
        cont = False # we only need to set continue to false since it's already true

# output all of the entries in the list
for record in college_records:
    record.displayInformation()
