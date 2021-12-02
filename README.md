# Zendesk Ticket Viewer 
This repo consists of a ticket viewer application to connect to Zendesk server and view tickets.\
To begin with, clone this repo and install dependencies using `pip install -r requirements.txt` \
Ensure `Python3` is installed on the system.


The Application can be started by calling `python main.py`

The Application is divided into 2 main sections:
1) `Process class` - Process mainly handles the interaction with user input and initiates requests to service class.
2) `Service class` - Service class queries the zendesk API based on the request initiated by user.

* `exception.py` houses all the custom exceptions thrown during processing the request.\
* `ticket.py` consists of the `Ticket` class which carries the definition to ticket\
* `config.py` consists of all the constants/properties.

The application can be tested by running ` coverage run -m unittest test_cases.py` and report can be viewed by running `coverage report -m` 

To configure authorization, update the config with below details
1) `api_token` - Should be a valid api token 
2) `subdomain` - the domain name
3) `username` - username