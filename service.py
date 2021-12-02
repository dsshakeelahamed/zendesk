import requests
from requests.auth import HTTPBasicAuth
import config as cfg
from exception import NoDataException, InvalidTicketIDException, InvalidSubDomainException, UnauthorizedException, ForbiddenException, ServerErrorException


class Service:
    """
    A Class to act as an interface between ticket viewer application and zendesk API
    """
    def __init__(self):
        pass

    def __request_data(self, path):
        """
        To connect to zendesk server and retrieve data

        :param path:
            type - string
            description - the http path to connect on zendesk server (ex - /api/requests)
        :return:
            type - json
            description - the api response is returned
        """
        url = "https://%s.zendesk.com/%s/%s" % (cfg.subdomain, cfg.api_prefix, path)
        response = requests.get(url=url, auth=HTTPBasicAuth(username='%s/token' % cfg.username, password=cfg.api_token))
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise UnauthorizedException
        elif response.status_code == 403:
            raise ForbiddenException
        elif response.status_code == 404:
            error_data = response.json().get("error")
            if isinstance(error_data, dict):
                raise InvalidSubDomainException
            elif isinstance(error_data, str):
                raise NoDataException
        elif response.status_code >= 500:
            raise ServerErrorException

    def fetch_per_id(self, id):
        """
        To validate ticket id and request data for a ticket

        :param id:
            type - string
            description - ticket id
        :return:
            type - json
            description - the api response is returned
        """
        if not id.isnumeric():
            raise InvalidTicketIDException
        path = "requests/%s" % id
        data = self.__request_data(path)
        return data

    def fetch_all(self):
        """
        To trigger request for fetching data of all tickets

        :return:
            type - json
            description - the api response is returned
        """
        path = "requests"
        data = self.__request_data(path)
        return data




