import datetime
import math
import json
from requests.exceptions import ConnectionError, Timeout
from service import Service
from ticket import Ticket
from exception import NoDataException, InvalidTicketIDException, UnauthorizedException, ForbiddenException, InvalidSubDomainException, ServerErrorException
import config as cfg


class Process:
    """
    A Class which acts as in interface between user input and Service class.
    """

    def __init__(self):
        self.service = Service()

    def start_request(self):
        """
        The infinite loop method to serve user requests
        """
        print("Enter 'help' to view options and 'quit' to exit")
        process_response = True
        while process_response:
            input_data = self._process_input()
            process_response = self._process_request(input_data)

    def _process_request(self, input_data):
        """
        The method which process user input after it's parsed

        :param input_data:
            type: bool/string
            description: bool input is basically static input where no processing is done and same is returned
                        string input is the user input that needs to be processed further to fetch ticket data
        :return:
            type - bool
            description - To continue or exit the application
        """
        try:
            if isinstance(input_data, bool):
                if input_data:
                    return True
                else:
                    return False
            else:
                if input_data == "1":
                    ticket_id = input("Enter ticket id\n")
                    if ticket_id.isnumeric():
                        ticket = self._process_single_ticket(ticket_id)
                        self._display_tickets(ticket)
                    else:
                        print("Invalid ticket id, closing request")
                elif input_data == "2":
                    print("Please wait while tickets are fetched")
                    tickets = self._process_all()
                    self._display_tickets(tickets)
                else:
                    print("Invalid Input. Please type 'help' to know valid options")
            return True
        except Timeout:
            print("Server is busy, please try after sometime!")
        except ConnectionError:
            print("Could not connect to Server, Please try again later.")
        except InvalidTicketIDException:
            pass
        except UnauthorizedException:
            pass
        except ForbiddenException:
            pass
        except InvalidSubDomainException:
            pass
        except NoDataException:
            pass
        except ServerErrorException:
            pass
        except Exception as e:
            try:
                with open("error_logs.txt", "a") as error_file:
                    error = {}
                    error["error_log"] = e.__str__()
                    error["timestamp"] = str(datetime.datetime.now())
                    error_file.write(json.dumps(error))
                    error_file.write("\n")
            except:
                pass
            print("The ticket viewer could not handle this request.")
        return True




    def _process_single_ticket(self, ticket_id):
        """
        Method to parse api response from service class for a single ticket data to generate Ticket object
        :param ticket_id:
                type - int
                description - ticket id
        :return:
            type - List of Ticket objects
            description - returns a list of Ticket objects to be used for display
        """
        ticket_data = self.service.fetch_per_id(ticket_id)
        ticket_data = ticket_data.get("request", {})
        ticket_object = Ticket(ticket_data)
        return [ticket_object]

    def _process_all(self):
        """
        Method to parse api response from service class for all tickets data to generate Ticket objects
        :return:
            type - List of Ticket objects
            description - returns a list of Ticket objects to be used for display
        """
        ticket_data = self.service.fetch_all()
        ticket_data = ticket_data.get("requests", {})
        tickets = []
        for i, ticket_data_per_id in enumerate(ticket_data):
            ticket_object = Ticket(ticket_data_per_id)
            tickets.append(ticket_object)
        return tickets

    def _display_tickets(self, tickets):
        """
        Method to display all the tickets on console in a paginated manner

        :param tickets:
                type - List of Ticket objects
                description - list of Ticket objects to be displayed
        """
        print("*********Ticket Details**********")
        pages = math.ceil(len(tickets)/cfg.records_per_page)
        page = 1
        start = 0
        end = page * cfg.records_per_page
        s_no = 1

        while page <= pages:

            for ticket in tickets[start: end]:
                print("S_no : %s" % s_no)
                ticket.display()
                print("\n")
                s_no += 1
            print("***** Page %s of %s ****" % (page, pages))
            if page == pages:
                return
            input_request = input("Press 1 to continue to next page, any other key to stop\n")
            if input_request == "1":
                page += 1
                start = end
                end = page * cfg.records_per_page
            else:
                print("Stopping next page display")
                return
        print("End of request")
        return

    def _process_input(self):
        """
        Method which parses user input from console
        :return:
            type - bool/string
            description - returns bool values if static inputs (ex - help , quit) are entered, else string values are returned
        """
        input_data = input("\n")
        if input_data.lower() == "help":
            self._display_options()
            return True
        elif input_data.lower() == "quit":
            return False
        else:
            return input_data

    def _display_options(self):
        """
        Static method to print ticket viewing options on console
        """
        print("Below are the ticket viewing options")
        print("*** Enter '1' to view a ticket ***")
        print("*** Enter '2' to view all tickets ***")
        print("*** Enter 'quit' to exit ***\n")
