import requests
import base64
from requests.auth import HTTPBasicAuth
import config as cfg
from exception import NoDataException, InvalidTicketIDException, InvalidSubDomainException, UnauthorizedException, ForbiddenException, ServerErrorException


class Service:
    def __init__(self):
        pass

    def __request_data(self, path):

        url = "https://%s.zendesk.com/%s/%s" % (cfg.subdomain, cfg.api_prefix, path)
        response = requests.get(url=url, auth=HTTPBasicAuth(username='%s/token' % cfg.username, password=base64.b64decode(cfg.api_token)))
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
        if not id.isnumeric():
            raise InvalidTicketIDException
        # raise custom Exceptions here
        path = "requests/%s" % id
        data = self.__request_data(path)
        return data

    def fetch_all(self):
        path = "requests"
        data = self.__request_data(path)
        return data

    # def fetch_user(self, user_id):
    #     path = "users/%s" % user_id
    #     data = self.__request_data(path)
    #     return data



