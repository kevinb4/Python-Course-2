import unittest
import os.path
import time
from functions.my_functions import *
from classes.database_access import DB_Connect

class FunctionsTestCase(unittest.TestCase):
    """Tests for functions in the my_functions.py file"""

    def setUp(self):
        """Connent to the database to use for all tests"""
        self.db = DB_Connect('root', '1234', 'python_final')

    def test_add_valid_customer(self):
        """Tests adding a valid customer to the database"""
        customer = {"first_name": "Bob", "last_name": "Sanders", "address": "31131 Wide Rd", "city": "Troy", "state": "MI", "zip": 48093, "company": "Sanders Co.", "primary_phone": "596-452-7741", "email_address": "bob@sanders.co"}
        add_customer(self.db, customer)
        self.assertIn(customer, self.db.executeSelectQuery(f"SELECT address, city, state, zip, company, primary_phone, email_address, f_name, l_name FROM crm_data WHERE email_address = '{customer['email_address']}';"))
        self.assertIn({"name": build_name(customer), "company": customer['company'], "address": build_address(customer)}, self.db.executeSelectQuery(f"SELECT name, company, address FROM mailings WHERE address = '{build_address(customer)}'"))
        
        # remove customer after so this test is repeatable
        remove_customer(self.db, self.db.executeSelectQuery(f"SELECT crm_id FROM crm_data WHERE email_address = '{customer['email_address']}';")[0]['crm_id'], "crm_data")
        remove_customer(self.db, self.db.executeSelectQuery(f"SELECT mail_id FROM mailings WHERE address = '{build_address(customer)}';")[0]['mail_id'], "mailings")

    def test_add_invalid_customer(self):
        """Tests adding an invalid customer to the database"""
        customer = {"first_name": "", "last_name": "%!", "address": "1212431343242344324234 industrial technical district road", "city": "1", "state": "ZZ", "zip": "1234567890987654321", "primary_phone": None, "email_address": "null@none.co"}
        add_customer(self.db, customer)
        self.assertNotIn(customer, self.db.executeSelectQuery(f"SELECT f_name AS first_name, l_name AS last_name, address, city, state, zip, company, primary_phone, email_address FROM crm_data WHERE email_address = '{customer['email_address']}';"))
        self.assertNotIn({"name": build_name(customer), "company": customer.get('company'), "address": build_address(customer)}, self.db.executeSelectQuery(f"SELECT name, company, address FROM mailings WHERE address = '{build_address(customer)}'"))

    def test_build_valid_address(self):
        """Tests building a valid address"""
        customer = {"address": "31131 Wide Rd", "city": "Troy", "state": "MI", "zip": "48093"}
        self.assertEqual(build_address(customer), "31131 Wide Rd, Troy, MI 48093")

    def test_build_invalid_address(self):
        """Tests building an invalid address"""
        customer = {"addy": "123", "cit": "roy", "st": "MI", "zp": "48093"}
        self.assertNotEqual(build_address(customer), "123, roy, MI 48093")

    def test_build_valid_dict(self):
        """Tests building a valid dictionary to a string"""
        customer = {"first_name": "Bob", "last_name": "Sanders", "address": "31131 Wide Rd", "city": "Troy", "state": "MI", "zip": "48093", "company": "Sanders Co.", "primary_phone": "596-452-7741", "email_address": "bob@sanders.co"}
        self.assertEqual(build_dict(customer), "First Name: Bob, Last Name: Sanders, Address: 31131 Wide Rd, City: Troy, State: MI, Zip: 48093, Company: Sanders Co., Primary Phone: 596-452-7741, Email Address: bob@sanders.co")

    def test_build_invalid_dict(self):
        """Tests building an invalid dictionary to a string"""
        customer = {"first name": "B0b", "last name": " ", "address": "12345", "city": "!@#", "state": "ZZ", "zip": "48093", "primary_phone": "596-452-7741"}
        self.assertNotEqual(build_dict(customer), "first name: B0b, last name:  , address: 12345, city: !@#, state: ZZ, zip: 48093, company: None, primary_phone: 596-452-7741, email_address: None")

    def test_build_valid_list(self):
        """Tests building a valid list to a string"""
        items = ["first_name", "last_name", "address", "city", "state", "zip", "company", "primary_phone", "email_address"]
        self.assertEqual(build_list(items), "first_name, last_name, address, city, state, zip, company, primary_phone, email_address")

    def test_build_invalid_list(self):
        """Tests building an invalid list to a string"""
        items = {" ": "_", "   ": "$@", '[]': None}
        self.assertNotEqual(build_list(items), " , _,    , $@, [], None")

    def test_build_valid_name(self):
        """Tests building a valid name"""
        customer = {"first_name": "Bob", "last_name": "Sanders"}
        self.assertEqual(build_name(customer), "Bob Sanders")

    def test_build_valid_name(self):
        """Tests building an invalid name"""
        customer = {"name": "B0B", "last name": "Sandy"}
        self.assertNotEqual(build_name(customer), "B0B Sandy")

    def test_build_valid_values(self):
        """Tests building valid values for mysql queries"""
        self.assertTrue(build_values(3), "%s, %s, %s")

    def test_build_valid_values(self):
        """Tests building invalid values for mysql queries"""
        tests = [" ", "%*63", None, []]
        for test in tests:
            self.assertFalse(build_values(test), "%s")

    def test_get_valid_id_name(self):
        """Tests getting the valid id attribute name of a specific table"""
        self.assertEqual(get_id_name("crm_data"), "crm_id")
        self.assertEqual(get_id_name("mailings"), "mail_id")

    def test_get_invalid_id_name(self):
        """Tests getting the invalid id attribute name of a specific table"""
        self.assertNotEqual(get_id_name("CRm data"), "crm_id")
        self.assertNotEqual(get_id_name("M@IL"), "mail_id")

    def test_import_valid_data(self):
        """Tests importing a valid data file"""
        data = import_data("text_files/customer_export.txt")

        self.assertEqual("Butt", data[0]['last_name'])

    def test_import_invalid_data(self):
        """Tests importing an invalid data file"""
        data = import_data({})

        self.assertNotEqual("Butt", data)

    def test_modify_valid_customer(self):
        """Tests modifying a valid customer successfully"""
        id = 1
        table = "crm_data"
        data_type = "first_name"
        data = "John"
        modify_customer(self.db, id, table, data_type, data)
        self.assertIn({data_type: data}, self.db.executeSelectQuery(f"SELECT f_name AS first_name FROM {table} WHERE {get_id_name(table)} = {id}"))

    def test_modify_invalid_customer(self):
        """Tests modifying an invalid customer unsuccessfully"""
        id = 1
        table = "crm_data"
        data_type = "name"
        data = "J0hn"
        modify_customer(self.db, id, table, data_type, data)
        self.assertNotIn({data_type: data}, self.db.executeSelectQuery(f"SELECT f_name AS first_name FROM {table} WHERE {get_id_name(table)} = {id}"))

    def test_remove_valid_customer(self):
        """Tests removing a valid customer successfully"""
        customer = {"first_name": "Dan", "last_name": "Canty", "address": "31121 Narrow Rd", "city": "Troy", "state": "MI", "zip": "48093", "company": "Canty Cans", "primary_phone": "556-452-7721", "email_address": "dan@canty.com"}
        add_customer(self.db, customer) # add a customer to remove

        crm_id = self.db.executeSelectQuery(f"SELECT crm_id FROM crm_data WHERE email_address = '{customer.get('email_address')}'")[0]['crm_id'] # get the id from the crm_data table
        mail_id = self.db.executeSelectQuery(f"SELECT mail_id FROM mailings WHERE address = '{build_address(customer)}'")[0]['mail_id'] # get the id from the mailings table

        remove_customer(self.db, crm_id, "crm_data")
        remove_customer(self.db, mail_id, "mailings")

        self.assertNotIn(customer, self.db.executeSelectQuery(f"SELECT f_name AS first_name, l_name AS last_name, address, city, state, zip, company, primary_phone, email_address FROM crm_data WHERE crm_id = '{crm_id}'"))
        self.assertNotIn({"name": build_name(customer), "company": customer['company'], "address": build_address(customer)}, self.db.executeSelectQuery(f"SELECT name, company, address FROM mailings WHERE mail_id = '{mail_id}'"))

    def test_remove_invalid_customer(self):
        """Tests removing an invalid customer unsuccessfully"""
        customer = {"first_name": "Dan", "last_name": "Canty", "address": "31121 Narrow Rd", "city": "Troy", "state": "MI", "zip": 48093, "company": "Canty Cans", "primary_phone": "556-452-7721", "email_address": "dan@canty.com"}
        add_customer(self.db, customer) # add a customer to remove

        crm_id = self.db.executeSelectQuery(f"SELECT crm_id FROM crm_data WHERE email_address = '{customer.get('email_address')}'")[0]['crm_id'] # get the id from the crm_data table
        mail_id = self.db.executeSelectQuery(f"SELECT mail_id FROM mailings WHERE address = '{build_address(customer)}'")[0]['mail_id'] # get the id from the mailings table

        remove_customer(self.db, customer, "crm_data")
        remove_customer(self.db, customer, "mailings")

        self.assertIn(customer, self.db.executeSelectQuery(f"SELECT address, city, state, zip, company, primary_phone, email_address, f_name, l_name FROM crm_data WHERE crm_id = '{crm_id}'"))
        self.assertIn({"name": build_name(customer), "company": customer['company'], "address": build_address(customer)}, self.db.executeSelectQuery(f"SELECT name, company, address FROM mailings WHERE mail_id = '{mail_id}'"))

    def test_save_to_valid_CSV(self):
        """Tests saving a valid CSV file"""
        path = f"text_files/test_valid_customer_export_{time.time()}.csv"
        data = import_data("text_files/customer_export.txt")

        save_to_CSV(path, data)
        self.assertTrue(os.path.exists(path))

    def test_save_to_invalid_CSV(self):
        """Tests saving an invalid CSV file"""
        path = f"text_files/test_invalid_customer_export_{time.time()}.csv"
        
        save_to_CSV(path, 1)
        self.assertFalse(os.path.exists(path))

    def test_save_to_valid_JSON(self):
        """Tests saving a valid JSON file"""
        path = f"text_files/test_valid_customer_export_{time.time()}.json"
        data = import_data("text_files/customer_export.txt")

        save_to_JSON(path, data)
        self.assertTrue(os.path.exists(path))

    def test_save_to_invalid_JSON(self):
        """Tests saving an invalid JSON file"""
        path = f"text_files/test_invalid_customer_export_{time.time()}.json"

        save_to_JSON(path, "")
        self.assertFalse(os.path.exists(path))

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

    def test_validate_valid_attribute(self):
        """Validates a valid attribute in a dict"""
        customer = {"first_name": "Bob", "last_name": "Sanders"}
        attribute = "first_name"

        self.assertTrue(validate_attribute(customer, attribute))

    def test_validate_invalid_attribute(self):
        """Validates an invalid attribute in a dict"""
        customer = '{"first_name": "Bob", "last_name": "Sanders"}'
        attribute = "first_name"

        self.assertFalse(validate_attribute(customer, attribute))

    def test_validate_valid_char(self):
        """Test the char validator with valid entries"""
        tests = [" ", "1312 Space Ave.", "test", "\\"]
        for test in tests:
            self.assertTrue(validate_char(test, "address", "disallowed"))

        tests = ["Troy", "Semi-Auto", "Van Ark", " "]
        for test in tests:
            self.assertTrue(validate_char(test, "city", "allowed"))

        tests = ["notmy@email.com", "just.testing@domain.abc", "is_this_possible.question.mark"]
        for test in tests:
            self.assertTrue(validate_char(test, "email_address", "disallowed"))

        tests = ["Tom's Code", "Jack Van-Argo", "Kevin Nivek"]
        for test in tests:
            self.assertTrue(validate_char(test, "name", "allowed"))

        tests = ["123", "646-466-3302", "-----------"]
        for test in tests:
            self.assertTrue(validate_char(test, "primary_phone", "allowed"))

    def test_validate_invalid_char(self):
        """Test the char validator with invalid entries"""
        tests = ["", "It's@Home", "!1", "           ;"]
        for test in tests:
            self.assertFalse(validate_char(test, "address", "disallowed"))

        tests = ["TR0Y", [], ""]
        for test in tests:
            self.assertFalse(validate_char(test, "city", "allowed"))

        tests = ["(not)my@email.com", "    .@a,", "is_this_possible@?"]
        for test in tests:
            self.assertFalse(validate_char(test, "email_address", "disallowed"))

        tests = ["T0M", [], "ît's not ok to have special characters in your name"]
        for test in tests:
            self.assertFalse(validate_char(test, "name", "allowed"))

        tests = ["one", "", "12345678998767654632?"]
        for test in tests:
            self.assertFalse(validate_char(test, "primary_phone", "allowed"))

    def test_validate_valid_id(self):
        """Tests to make sure the id is valid numerically"""
        tests = ["1", "0", "1000000001"]

        for test in tests:
            self.assertTrue(validate_id(test))

    def test_validate_invalid_id(self):
        """Tests to make sure the id is valid numerically"""
        tests = [[], None, "one two 3"]

        for test in tests:
            self.assertFalse(validate_id(test))

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

    def test_validate_valid_state(self):
        """Tests input with valid state abbrivations"""
        tests = ["MI", "ZZ", "AZ", "CA"]

        for test in tests:
            self.assertTrue(validate_state(test))

    def test_validate_invalid_state(self):
        """Tests input with invalid state abbrivations"""
        tests = ["mi", "    ", "Z", {}]

        for test in tests:
            self.assertFalse(validate_state(test))

    def test_validate_valid_zipcode(self):
        """Tests input with valid zip codes"""
        tests = ["1234", "48089", "0000"]

        for test in tests:
            self.assertTrue(validate_zipcode(test))

    def test_validate_invalid_zipcode(self):
        """Tests input with invalid zip codes"""
        tests = [123456, "            12", 12345.6]

        for test in tests:
            self.assertFalse(validate_zipcode(test))