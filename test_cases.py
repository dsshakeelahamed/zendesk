import sys
import unittest

from process import Process
from exception import *


class TestTicketService(unittest.TestCase):
    def setUp(self):
        self.process_obj = Process()
        pass

    def tearDown(self):
        pass

    # Test when a single valid ticket id is provided
    def test_single_ticket_success(self):
        ticket_id = 3
        ticket = self.process_obj._process_single_ticket(str(ticket_id))[0]
        self.assertEqual(ticket.ticket_id, ticket_id)

    # Test when ticket id with no data is provided
    def test_single_ticket_failure(self):
        self.assertRaises(NoDataException, self.process_obj._process_single_ticket, "999")

    # Test when an invalid id is provided
    def test_single_ticket_invalid_id(self):
        self.assertRaises(InvalidTicketIDException, self.process_obj._process_single_ticket, "abc")

    # Test for tickets
    def test_all_tickets_success(self):
        self.assertEqual(100, len(self.process_obj._process_all()))

    # Test when single ticket provides valid id
    def test_process_single_ticket(self):
        with open("test_all_pages.txt", 'r') as file:
            sys.stdin = file
            self.assertFalse(self.assertRaises(Exception, self.process_obj._process_request("1")))

    # Test when single ticket process provides invalid id
    def test_process_single_failure(self):
        sys.stdin = "abc"
        self.assertFalse(self.assertRaises(Exception, self.process_obj._process_request("1")))

    # To test when _process_input returns True value
    def test_process_bool_input_true(self):
        # sys.stdin = "3"
        self.assertFalse(self.assertRaises(Exception, self.process_obj._process_request(True)))

    # To test when _process_input returns False value
    def test_process_bool_input_false(self):
        self.assertFalse(self.assertRaises(Exception, self.process_obj._process_request(False)))

    # Test if all pages are printed
    def test_process_all_tickets(self):
        with open("test_all_pages.txt", 'r') as file:
            sys.stdin = file
            self.assertFalse(self.assertRaises(Exception, self.process_obj._process_request("2")))

    # Test if Display doesn't raise an Exception
    def test_display_content(self):
        with open("test_help_display.txt", 'r') as file:
            sys.stdin = file
            self.assertFalse(self.assertRaises(Exception, self.process_obj._process_input()))
            self.assertFalse(self.assertRaises(Exception, self.process_obj._process_input()))


