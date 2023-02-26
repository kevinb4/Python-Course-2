import unittest
from functions.my_functions import *
from classes.database_access import DB_Connect

class FunctionsTestCase(unittest.TestCase):
    """Tests for functions in the my_functions.py file"""

    def setUp(self):
        """Connent to the database to use for all tests"""
        self.db = DB_Connect('root', '1234', 'dealership')

    def test_add_valid_vehicle(self):
        """Tests adding a valid vehicle to the db"""
        # this test will still pass if run multiple times, but it won't properly test due to the VIN being unique in the db (so be sure to change it)
        vehicle = {"make": "Tesla", "model": "Testa", "vin": "T54YE34FDJ", "previous_owner": "Elon Musk", "price_paid": 25000.00, "sale_price": 45000.00, "description": "this is a test car"}

        add_vehicle(self.db, vehicle)
        self.assertIn(vehicle, self.db.executeSelectQuery(f"SELECT make, model, vin, previous_owner, price_paid, sale_price, description FROM VEHICLE WHERE VIN = '{vehicle['vin']}'"))

    def test_add_invalid_vehicle(self):
        """Tests adding an invalid vehicle to the db"""
        vehicle = {"make": "T#S!A", "model": " ", "vin": None, "sale_price": "22", "description": "--"}

        add_vehicle(self.db, vehicle)
        self.assertNotIn(vehicle, self.db.executeSelectQuery(f"SELECT make, model, vin, previous_owner, price_paid, sale_price, description FROM VEHICLE WHERE VIN = '{vehicle['vin']}'"))

    def test_build_valid_dict(self):
        """Tests building a valid dictionary to a string"""
        vehicle = {"make": "Tesla", "model": "Testa", "vin": "T54YE34FDJ", "previous_owner": "Elon Musk", "price_paid": None, "sale_price": 45000.25, "description": "this is a test car"}
        self.assertEqual(build_dict(vehicle), "make: Tesla, model: Testa, vin: T54YE34FDJ, previous owner: Elon Musk, sale price: 45000.25, description: this is a test car")

    def test_build_invalid_dict(self):
        """Tests building an invalid dictionary to a string"""
        vehicle = {"make": "T3SL@", "model": " ", "vin": "T54YE34FDJ", "sale price": 85, "description": "this is a test car"}
        self.assertNotEqual(build_dict(vehicle), "make: T3SL@, model:  , vin: T54YE34FDJ, previous owner: None, price paid: 0.00, sale price: 85, description: this is a test car")

    def test_build_valid_list(self):
        """Tests building a valid list to a string"""
        items = ["make", "model", "vin", "previous_owner", "price_paid", "sale_price", "description"]
        self.assertEqual(build_list(items), "make, model, vin, previous_owner, price_paid, sale_price, description")

    def test_build_invalid_list(self):
        """Tests building an invalid list to a string"""
        items = {" ": "$R*U", "": "370=-", 956765: None}
        self.assertNotEqual(build_list(items), " , $R*U, , 370=-, 956765, None")

    def test_build_valid_values(self):
        """Tests building valid values for mysql queries"""
        self.assertTrue(build_values(2), "%s, %s")

    def test_build_valid_values(self):
        """Tests building invalid values for mysql queries"""
        tests = [" ", "%*63", None, []]
        for test in tests:
            self.assertFalse(build_values(test), "%s")

    def test_modify_valid_vehicle(self):
        """Tests successfully modifying a vehicle"""
        id = 1
        data_type = "make"
        data = "Ford"
        modify_vehicle(self.db, id, data_type, data)
        self.assertIn({"make": "Ford"}, self.db.executeSelectQuery(f"SELECT make FROM vehicle WHERE id = {id}"))

    def test_modify_invalid_vehicle(self):
        """Tests unsuccessfully modifying a vehicle"""
        id = 1
        data_type = " "
        data = "F0RD"
        modify_vehicle(self.db, id, data_type, data)
        self.assertNotIn({"make": "F0RD"}, self.db.executeSelectQuery(f"SELECT make FROM vehicle WHERE id = {id}"))

    def test_remove_valid_vehicle(self):
        """Tests removing a valid vehicle"""
        vehicle = {"make": "Tesla", "model": "Testa", "vin": "JRYTJTJ45", "previous_owner": "Elon Musk", "price_paid": 25000.00, "sale_price": 45000.00, "description": "this is a test car"}

        add_vehicle(self.db, vehicle)
        id = self.db.executeSelectQuery(f"SELECT id FROM vehicle WHERE vin = '{vehicle['vin']}'")[0]['id'] # get the id of the added vehicle
        remove_vehicle(self.db, id)
        self.assertNotIn(vehicle, self.db.executeSelectQuery(f"SELECT make, model, vin, previous_owner, price_paid, sale_price, description FROM VEHICLE WHERE VIN = '{vehicle['vin']}'"))

    def test_remove_invalid_vehicle(self):
        """Tests removing an invalid vehicle"""
        vehicle = {"make": "Tesla", "model": "Testa", "vin": "JRYTJTJ45", "previous_owner": "Elon Musk", "price_paid": 25000.00, "sale_price": 45000.00, "description": "this is a test car"}

        add_vehicle(self.db, vehicle)
        remove_vehicle(self.db, vehicle)
        self.assertIn(vehicle, self.db.executeSelectQuery(f"SELECT make, model, vin, previous_owner, price_paid, sale_price, description FROM VEHICLE WHERE VIN = '{vehicle['vin']}'"))

    def test_underscore_valid_add(self):
        """Tests adding underscores to a string successfully"""
        self.assertEqual(underscore_add("this is a test"), "this_is_a_test")

    def test_underscore_invalid_add(self):
        """Tests adding underscores to a string unsuccessfully"""
        self.assertNotEqual(underscore_add("thisisatest"), "this_is_a_test")

    def test_underscore_valid_remove(self):
        """Tests removing underscores to a string successfully"""
        self.assertEqual(underscore_remove("this_is_a_test_"), "this is a test ")
    
    def test_underscore_invalid_remove(self):
        """Tests removing underscores to a string unsuccessfully"""
        self.assertNotEqual(underscore_remove("this is a test"), "this_is_a_test")

    def test_validate_valid_char(self):
        """Test the char validator with valid entries"""
        tests = [" ", "F0rd", "ARM&HAMMER", "TESLA"]
        for test in tests:
            self.assertTrue(validate_char(test, "model", "disallowed"))

        tests = ["Bob J. Jenkins", "Jolly-R", "Tom's", " "]
        for test in tests:
            self.assertTrue(validate_char(test, "previous_owner", "allowed"))

    def test_validate_invalid_char(self):
        """Test the char validator with invalid entries"""
        tests = ["a!", "#^A", "32R;", "     \"     @"]
        for test in tests:
            self.assertFalse(validate_char(test, "model", "disallowed"))

        tests = [" &32", "√erizon", " ", "------.-.--.-.-.--.-.-..----_"]
        for test in tests:
            self.assertFalse(validate_char(test, "previous_owner", "allowed"))

    def test_validate_valid_input(self):
        """Tests the input validator with valid entries"""
        tests = ["   ", "asd", 52, "{}"]
        for test in tests:
            self.assertTrue(validate_input(test))

    def test_validate_invalid_input(self):
        """Tests the input validator with invalid entries"""
        tests = ["", [], None, {}]
        for test in tests:
            self.assertFalse(validate_input(test))

    def test_validate_valid_price(self):
        """Tests the price validator with valid entries"""
        tests = [0.00, 25, 1234567890, "123", "122.22"]
        for test in tests:
            self.assertTrue(validate_price(test))

    def test_validate_invalid_price(self):
        """Tests the price validator with invalid entries"""
        tests = ["1,000", "", "one.one", " ", "!"]
        for test in tests:
            self.assertFalse(validate_price(test))