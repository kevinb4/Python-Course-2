import unittest
from classes.calendar import Calendar
from classes.event import Event

class TestCalendarClass(unittest.TestCase):
    """Test the Calendar Class"""

    def setUp(self):
        """Create an instance of the Calendar class for testing all class functions"""
        self.my_calendar = Calendar()

        # create a new event to test adding/removing
        self.new_event = Event("Test", "11/12/12", "12:00", "recurring")

    def test_add_event(self):
        """Test adding an event to the Calendar"""
        self.my_calendar.add_event(self.new_event)
        self.assertIn(self.new_event, self.my_calendar.cal_events)

    def test_add_invalid_event(self):
        """Test trying to add invalid items to the events list"""
        invalid = [1, 'a', [], 'ô']

        for item in invalid:
            self.my_calendar.add_event(item)
            self.assertNotIn(item, self.my_calendar.cal_events)

    def test_remove_event(self):
        """Tests removing a valid event from the calendar"""
        self.my_calendar.add_event(self.new_event) # add the event to remove
        self.my_calendar.remove_event(0) # the only item in the class will be indexed at 0
        self.assertNotIn(self.new_event, self.my_calendar.cal_events)

    def test_remove_invalid_event(self):
        """Tests removing invalid items from the calendar"""
        self.my_calendar.add_event(self.new_event) # add the event to ensure it's still there after testing invalid values
        invalid = [-10, "≡", [], {}, 0.1, " "]

        for item in invalid:
            self.my_calendar.remove_event(item) # try to remove an invalid index
        
        self.assertIn(self.new_event, self.my_calendar.cal_events) # item should still be in there since it wasn't in the invalid list above