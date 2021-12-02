
class InvalidTicketIDException(Exception):
    def __init__(self):
        print("The Ticket ID is invalid, please provide a valid Ticket ID")


class NoDataException(Exception):
    def __init__(self):
        print("No Data available for the request")


class InvalidSubDomainException(Exception):
    def __init__(self):
        print("The sub domain is invalid, please provide a valid subdomain")


class UnauthorizedException(Exception):
    def __init__(self):
        print("Invalid Credentials, please provide valid Credentials")


class ForbiddenException(Exception):
    def __init__(self):
        print("The user has insufficient priviliges to access the resource")


class ServerErrorException(Exception):
    def __init__(self):
        print("The server could not process the request, please try after sometime")

