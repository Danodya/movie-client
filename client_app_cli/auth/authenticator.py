import requests
from client_app_cli.constants import constant
from client_app_cli.exceptions.exceptions import AuthenticationException


class Authenticator:
    """
    Authenticator class that handles authentication
    """

    def __init__(self, username: str, password: str, base_url: str):
        """
        Initializes the Authenticator with user credentials

        :param username: Username for authentication
        :param password: Password for authentication
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.__validate()

    def __validate(self):
        if not self.username or not isinstance(self.username, str):
            raise AuthenticationException("username must be a non-empty string")
        if not self.password or not isinstance(self.password, str):
            raise AuthenticationException("password must be a non-empty string")

    def authenticate(self) -> str:
        """
        Authenticates the user using the username and password provided at instantiation.
        :return: bearer token
        """
        url = self.base_url + constant.AUTH_API
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            bearer_token = response.json()["bearer"]
        else:
            raise AuthenticationException(response.json()["error"])
        return bearer_token
