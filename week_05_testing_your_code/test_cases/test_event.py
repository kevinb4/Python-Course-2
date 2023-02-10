import unittest
from classes.event import Event

class TestEventClass(unittest.TestCase):
    """Test the Event Class"""

    def setUp(self):
        """Create an instance of the Event class for testing all class functions"""
        self.my_event = Event("Test", "11/12/12", "12:00", "recurring")

    def test_valid_date_chars(self):
        """Test valid date chars"""
        valid = ["5", "24", "-", "1", "31"]

        for item in valid:
            self.assertTrue(self.my_event.validate_char(item, "date"))

    def test_invalid_date_chars(self):
        """Test invalid date chars"""
        invalid = [" a", '!-', [], {}]

        for item in invalid:
            self.assertFalse(self.my_event.validate_char(item, "date"))

    def test_valid_time_chars(self):
        """Test valid time chars"""
        valid = [":", "12", "5", "24"]

        for item in valid:
            self.assertTrue(self.my_event.validate_char(item, "time"))

    def test_invalid_time_chars(self):
        """Test invalid time chars"""
        invalid = [" 12", ':::♀', {}, "12.12"]

        for item in invalid:
            self.assertFalse(self.my_event.validate_char(item, "time"))

    def test_valid_type(self):
        """Tests for valid types"""
        types = ["single occurrence", "Recurring", "fixed number of meetings"]

        for item in types:
            self.assertTrue(self.my_event.validate_type(item))

    def test_invalid_type(self):
        """Tests for invalid types"""
        types = ["singleoccurrence", 12, "╖", []]

        for item in types:
            self.assertFalse(self.my_event.validate_type(item))