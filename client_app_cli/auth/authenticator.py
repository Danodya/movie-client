import requests
from client_app_cli.constants import constant
from client_app_cli.exceptions.exceptions import AuthenticationException


class Authenticator:
    """
    Authenticator class that handles authentication
    """
    def __init__(self, username: str, password: str):
        """
        Initializes the Authenticator with user credentials

        :param username: Username for authentication
        :param password: Password for authentication
        """
        self.username = username
        self.password = password

    def __validate(self):
        if not self.username or not isinstance(self.username, str):
            raise AuthenticationException('username must be a non-empty string')
        if not self.password or not isinstance(self.password, str):
            raise AuthenticationException('password must be a non-empty string')

    def authenticate(self) -> str:
        """
        Authenticates the user using the username and password provided at instantiation.
        :return: bearer token
        """
        url = constant.BASE_URL + constant.AUTH_API
        payload = {"username": self.username, "password": self.password}
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        bearer_token = response.json()['bearer']
        return bearer_token
